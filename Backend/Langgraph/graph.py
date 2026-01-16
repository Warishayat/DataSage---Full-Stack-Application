from langgraph.graph import StateGraph, END,START
from Langgraph.states import DataState
from Langgraph.nodes import (
    cleaning_node,
    eda_node,
    visualization_node,
    insight_node,
    report_node,
)


builder = StateGraph(DataState)

builder.add_node("cleaning_agent", cleaning_node)
builder.add_node("eda_agent", eda_node)
builder.add_node("visualization_agent", visualization_node)
builder.add_node("insight_agent", insight_node)
builder.add_node("report_agent", report_node)

builder.add_edge(START,"cleaning_agent")
builder.add_edge("cleaning_agent", "eda_agent")
builder.add_edge("eda_agent", "visualization_agent")
builder.add_edge("visualization_agent", "insight_agent")
builder.add_edge("insight_agent", "report_agent")
builder.add_edge("report_agent", END)

Analysis_graph = builder.compile()


if __name__ == "__main__":
    import os
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    filepath = os.path.join(
        BASE_DIR,
        "Data",
        "CVD Dataset.csv"
    )

    initial_state: DataState = {
        "file_path": filepath,
        "df": None,
        "metadata": None,
        "eda": None,
        "charts": None,
        "insights": None,
        "report": None,
    }
    result = Analysis_graph.invoke(initial_state)
    print(result)