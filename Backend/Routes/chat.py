import os
import pandas as pd
from typing import TypedDict, Dict

from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from dotenv import load_dotenv

from langgraph.graph import StateGraph, END
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

from Utils.Security import get_current_user

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

chat_router = APIRouter(prefix="/csv-chat", tags=["CSV Chat"])

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0,
    api_key=GROQ_API_KEY
)


ACTIVE_CHAT_CSV: Dict[str, Dict] = {}

class GraphState(TypedDict):
    question: str
    answer: str


def load_csv_once(file_path: str) -> pd.DataFrame:
    df = pd.read_csv(file_path)
    df.columns = [c.strip() for c in df.columns]
    return df

def get_csv_metadata(df: pd.DataFrame):
    return {
        "columns": list(df.columns),
        "total_columns": len(df.columns),
        "total_rows": len(df)
    }

def dataframe_to_context(df: pd.DataFrame, max_rows: int = 50) -> str:
    sample = df.head(max_rows)
    return sample.to_csv(index=False)

def build_prompt(metadata):
    return ChatPromptTemplate.from_template(
        """
You are an AI assistant chatting with a CSV dataset.

STRICT OUTPUT RULES:
- Never use bold text.
- Never use markdown.
- Never create lists or tables.
- Plain sentences only.

BEHAVIOR RULES:
- Do not guess values.
- Do not count rows unless explicitly asked.
- Column questions must use metadata.
- If info not present say: Not available in dataset.

Dataset Metadata:
Total Columns: {total_columns}
Column Names: {columns}

CSV Preview:
{context}

Question:
{question}

Answer:
"""
    )

def build_csv_chat_graph(df: pd.DataFrame, metadata, llm):

    prompt = build_prompt(metadata)
    context = dataframe_to_context(df)

    def generate_node(state: GraphState):
        messages = prompt.format_messages(
            question=state["question"],
            context=context,
            columns=", ".join(metadata["columns"]),
            total_columns=metadata["total_columns"]
        )
        response = llm.invoke(messages)
        return {"answer": response.content}

    graph = StateGraph(GraphState)
    graph.add_node("generate", generate_node)
    graph.set_entry_point("generate")
    graph.add_edge("generate", END)

    return graph.compile()

@chat_router.post("/upload")
async def upload_csv_for_chat(
    file: UploadFile = File(...),
    user = Depends(get_current_user)
):
    try:
        user_id = str(user.id)
        temp_path = f"/tmp/chat_{user_id}.csv"

        content = await file.read()
        with open(temp_path, "wb") as f:
            f.write(content)

        df = load_csv_once(temp_path)
        metadata = get_csv_metadata(df)

        graph = build_csv_chat_graph(
            df=df,
            metadata=metadata,
            llm=llm
        )

        ACTIVE_CHAT_CSV[user_id] = {
            "df": df,
            "graph": graph,
            "metadata": metadata
        }

        return {"message": "CSV uploaded. You can now chat with it."}

    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")


@chat_router.post("/chat")
async def chat_with_csv(
    question: str,
    user = Depends(get_current_user)
):
    try:
        user_id = str(user.id)

        if user_id not in ACTIVE_CHAT_CSV:
            return {"error": "Upload a CSV first"}

        graph = ACTIVE_CHAT_CSV[user_id]["graph"]

        result = graph.invoke({"question": question})

        return {"answer": result["answer"]}

    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")
