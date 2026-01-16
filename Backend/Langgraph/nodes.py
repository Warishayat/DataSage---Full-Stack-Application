from Langgraph.states import DataState
from Agents.data_cleaning import Preprocess_data
from Agents.eda import run_eda_agent
from Agents.visualization import visualization_agent
from Agents.insight import insight_agent
from Agents.reports import report_agent


def cleaning_node(state: DataState):
    result = Preprocess_data(state["file_path"])
    return {
        "df": result["dataframe"],
        "metadata": result["metadata"]
    }

def eda_node(state: DataState):
    return {
        "eda": run_eda_agent(state["df"])
    }

def visualization_node(state: DataState):
    return {
        "charts": visualization_agent(state["df"],state['metadata']),
    }


def insight_node(state: DataState):
    return {
        "insights": insight_agent(
            state["eda"],
            state["metadata"]
        )
    }

def report_node(state: DataState):
    return {
        "report": report_agent(
            eda=state["eda"],
            charts=state["charts"],
            insights=state["insights"]
        )
    }


def chat_node(state: DataState):
    return {
        "answer": chat_agent(
            question=state["question"],
            eda=state["eda"],
            insights=state["insights"]
        )
    }
