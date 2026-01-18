import os
import pandas as pd
from typing import TypedDict

from dotenv import load_dotenv
from langgraph.graph import StateGraph, END

from langchain_community.document_loaders import CSVLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate


load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")


class GraphState(TypedDict):
    question: str
    context: str
    answer: str


llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0,
    api_key=GROQ_API_KEY
)


def get_csv_metadata(file_path: str):
    df = pd.read_csv(file_path)
    return {
        "columns": list(df.columns),
        "total_columns": len(df.columns)
    }


def load_data(file_path: str):
    loader = CSVLoader(file_path=file_path)
    return loader.load()


def preprocess_data(data):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=230,
        chunk_overlap=12
    )
    return splitter.split_documents(data)


def load_embeddings():
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )


def create_vectorstore(documents, embeddings):
    return FAISS.from_documents(
        documents=documents,
        embedding=embeddings
    )


def build_prompt(metadata):
    return ChatPromptTemplate.from_template(
        """
You are an AI assistant chatting with a CSV dataset.

STRICT OUTPUT RULES (MANDATORY):
- Never use bold text.
- Never use markdown.
- Never format text into columns or lists.
- Write plain sentences only.
- Do not emphasize words.
- Do not decorate the response in any way.

BEHAVIOR RULES:
- Never count rows or values unless explicitly asked.
- Column-related questions must be answered using metadata only.
- Do not infer numbers from context text.
- If a question is ambiguous, ask for clarification in one simple sentence.
- If information is not available, say: Not available in dataset.

Dataset Metadata:
Total Columns: {total_columns}
Column Names: {columns}

Context (only for data-level questions):
{context}

Question:
{question}

Answer:
"""
    )


def build_csv_chat_graph(retriever, metadata, llm):

    prompt = build_prompt(metadata)

    def retrieve_node(state: GraphState):
        docs = retriever.invoke(state["question"])
        context = "\n".join(d.page_content for d in docs)
        return {"context": context}

    def generate_node(state: GraphState):
        messages = prompt.format_messages(
            question=state["question"],
            context=state["context"],
            columns=", ".join(metadata["columns"]),
            total_columns=metadata["total_columns"]
        )
        response = llm.invoke(messages)
        return {"answer": response.content}

    graph = StateGraph(GraphState)
    graph.add_node("retrieve", retrieve_node)
    graph.add_node("generate", generate_node)
    graph.set_entry_point("retrieve")
    graph.add_edge("retrieve", "generate")
    graph.add_edge("generate", END)

    return graph.compile()


if __name__ == "__main__":

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    filepath = os.path.join(BASE_DIR, "Data", "CVD Dataset.csv")

    metadata = get_csv_metadata(filepath)
    raw_data = load_data(filepath)
    docs = preprocess_data(raw_data)
    embeddings = load_embeddings()
    vectorstore = create_vectorstore(docs, embeddings)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

    CHAT_GRAPH = build_csv_chat_graph(
        retriever=retriever,
        metadata=metadata,
        llm=llm
    )

    print("\nCSV Chat Ready (type 'exit' to quit)\n")

    while True:
        query = input("User: ")
        if query.lower() == "exit":
            break

        result = CHAT_GRAPH.invoke({"question": query})
        print("Assistant:", result["answer"], "\n")
