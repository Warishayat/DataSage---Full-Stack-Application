from dotenv import load_dotenv
import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from typing import Any, Dict
from Agents.Schemas import InsightResponse
from Agents.State import DataState
import re
import json
import warnings
warnings.filterwarnings("ignore")

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

Model = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0.3,
    api_key=GROQ_API_KEY
)

prompt = ChatPromptTemplate.from_messages([
    ("system", """
You are a senior data analyst AI.
You MUST return a JSON object with these fields only:
summary, key_insights, risks, recommendations.
No field can be missing.
"""),
    ("human", """
EDA:
{eda}

Metadata:
{metadata}
""")
])

def sanitize(obj: Any) -> Any:
    if isinstance(obj, dict):
        return {k: sanitize(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [sanitize(v) for v in obj]
    if hasattr(obj, "item"):
        return obj.item()
    return obj

def prepare_insight_context(eda: Dict[str, Any], metadata: Dict[str, Any]) -> Dict[str, Any]:
    return sanitize({
        "overview": eda.get("overview", {}),
        "column_types": eda.get("column_types", {}),
        "summary_statistics": eda.get("summary_statistics", {}),
        "categorical_distributions": eda.get("categorical_distributions", {}),
        "correlations": eda.get("correlations", {}),
        "outliers": eda.get("outliers", {}),
        "missing_values": eda.get("missing_values", {}),
        "dataset_info": {
            "rows": metadata.get("rows"),
            "columns": metadata.get("columns")
        }
    })

def insight_agent(state: DataState) -> DataState:
    clean_eda = prepare_insight_context(state["eda"], state["metadata"])

    response = Model.invoke(
        prompt.format_messages(
            eda=clean_eda,
            metadata=clean_eda["dataset_info"]
        )
    )

    text = response.content
    match = re.search(r"\{.*\}", text, re.DOTALL)

    if match:
        try:
            insights = json.loads(match.group())
        except Exception:
            insights = {}
    else:
        insights = {}

    insights.setdefault("summary", "")
    insights.setdefault("key_insights", [])
    insights.setdefault("risks", [])
    insights.setdefault("recommendations", [])

    return {
        **state,
        "insights": insights
    }
