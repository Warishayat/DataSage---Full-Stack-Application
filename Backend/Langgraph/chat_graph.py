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
from Langgraph.chat_state import GraphState

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

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
    print("data is getting loaded")
    loader = CSVLoader(file_path=file_path)
    return loader.load()


def preprocess_data(data):
    print("Data got preprocess")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=230,
        chunk_overlap=12
    )
    return splitter.split_documents(data)


def load_embeddings():
    print("Loading embedding model")
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )


def create_vectorstore(documents, embeddings):
    print("vectorstore created")
    return FAISS.from_documents(
        documents=documents,
        embedding=embeddings
    )

def build_prompt(metadata):
    return ChatPromptTemplate.from_template(
        """
You are an AI assistant answering questions about a CSV dataset.

Dataset Metadata:
- Total Columns: {total_columns}
- Column Names: {columns}

Rules:
- If the user asks about number of columns, answer ONLY using metadata.
- If the question is conceptual, use the provided context.
- If the answer is not present, say "Not available in dataset".

Context:
{context}

Question:
{question}

Answer:
"""
    )

def retrieve_node(state: GraphState):
    docs = retriever.invoke(state["question"])
    context = "\n".join([doc.page_content for doc in docs])
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

CHAT_GRPAH = graph.compile()

if __name__ == "__main__":

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    filepath = os.path.join(BASE_DIR, "Data", "CVD Dataset.csv")
    metadata = get_csv_metadata(filepath)
    raw_data = load_data(filepath)
    docs = preprocess_data(raw_data)
    embeddings = load_embeddings()
    vectorstore = create_vectorstore(docs, embeddings)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 4})
    prompt = build_prompt(metadata)
    print("\nLangGraph CSV Assistant (type 'exit' to quit)\n")

    while True:
        query = input("User: ")
        if query.lower() == "exit":
            break

        result = CHAT_GRPAH.invoke({"question": query})
        print("Assistant:", result["answer"], "\n")