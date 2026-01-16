from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate
import json
from typing_extensions import TypedDict,Dict,List,Literal,Any
from Agents.Schemas import InsightResponse
import warnings
warnings.filterwarnings('ignore')

load_dotenv()

GOOGLE_API_KEY =  os.getenv("GOOGLE_API_KEY")
Model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.3,
    api_key=GOOGLE_API_KEY
)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a senior data analyst AI."),
    ("human", """
Analyze the following EDA results and metadata.
Generate clear business insights.

EDA:
{eda}

Metadata:
{metadata}
""")
])

Json_model = Model.with_structured_output(schema=InsightResponse)


def prepare_insight_context(eda: dict, metadata: dict) -> dict:
    return {
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
    }

def insight_agent(eda: dict, metadata: dict) -> InsightResponse:
    response = Json_model.invoke(
        prompt.format_messages(
            eda=eda,
            metadata=metadata
        )
    )
    return response

if __name__ == "__main__":
    from pprint import pprint
    from Agents.data_cleaning import Preprocess_data
    from Agents.eda import run_eda_agent
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    filepath = os.path.join(
        BASE_DIR,
        "Data",
        "Heart_Disease_Prediction.csv"
    )
    data = Preprocess_data("Data/Heart_Disease_Prediction.csv")
    df = data["dataframe"]
    metadata = data["metadata"]

    eda = run_eda_agent(df)
    insights = insight_agent(eda, metadata)
    pprint(insights)
