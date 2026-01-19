import os
import pandas as pd
from typing import TypedDict

from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
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

# ---------- CSV HELPERS (LIGHTWEIGHT) ----------

def load_csv_once(file_path: str) -> pd.DataFrame:
    return pd.read_csv(file_path)

def get_csv_metadata(df: pd.DataFrame):
    return {
        "columns": list(df.columns),
        "total_columns": len(df.columns),
        "total_rows": len(df),
        "dtypes": df.dtypes.astype(str).to_dict()
    }

def build_csv_summary(df: pd.DataFrame, max_rows: int = 5) -> str:
    sample = df.head(max_rows)
    return sample.to_csv(index=False)

def get_relevant_rows(df: pd.DataFrame, question: str, limit: int = 8) -> str:
    keywords = question.lower().split()
    mask = pd.Series([False] * len(df))

    for col in df.columns:
        if df[col].dtype == object:
            mask = mask | df[col].str.lower().str.contains("|".join(keywords), na=False)

    filtered = df[mask].head(limit)
    if filtered.empty:
        return "No directly matching rows found."

    return filtered.to_csv(index=False)

# ---------- PROMPT ----------

def build_prompt(metadata):
    return ChatPromptTemplate.from_template(
        """
You are an AI assistant answering questions about a CSV dataset.

STRICT OUTPUT RULES:
Never use bold.
Never use markdown.
Never create lists or tables.
Only plain sentences.

DATASET INFO:
Total Rows: {total_rows}
Total Columns: {total_columns}
Columns: {columns}
Data Types: {dtypes}

SAMPLE ROWS:
{sample}

RELEVANT ROWS (question-based):
{context}

Question:
{question}

Answer clearly using only the dataset.
If data is not available, say: Not available in dataset.
"""
    )

# ---------- GRAPH ----------

def build_csv_chat_graph(df, metadata, llm):

    prompt = build_prompt(metadata)

    def retrieve_node(state: GraphState):
        relevant_text = get_relevant_rows(df, state["question"])
        return {"context": relevant_text}

    def generate_node(state: GraphState):
        messages = prompt.format_messages(
            question=state["question"],
            context=state["context"],
            columns=", ".join(metadata["columns"]),
            total_columns=metadata["total_columns"],
            total_rows=metadata["total_rows"],
            dtypes=metadata["dtypes"],
            sample=build_csv_summary(df)
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

# ---------- MAIN ----------

if __name__ == "__main__":

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    filepath = os.path.join(BASE_DIR, "Data", "CVD Dataset.csv")

    df = load_csv_once(filepath)
    metadata = get_csv_metadata(df)

    CHAT_GRAPH = build_csv_chat_graph(
        df=df,
        metadata=metadata,
        llm=llm
    )

    print("Lightweight CSV Chat Ready\n")

    while True:
        q = input("User: ")
        if q.lower() == "exit":
            break
        result = CHAT_GRAPH.invoke({"question": q})
        print("Assistant:", result["answer"], "\n")
