import pandas as pd
import numpy as np
from typing import Dict, Any, List
import os



def make_histogram(df: pd.DataFrame, column: str) -> Dict[str, Any]:
    return {
        "id": f"hist_{column}",
        "type": "histogram",
        "column": column,
        "data": df[column].dropna().tolist(),
        "title": f"Distribution of {column}"
    }


def make_histogram(df: pd.DataFrame, column: str) -> Dict[str, Any]:
    return {
        "id": f"hist_{column}",
        "type": "histogram",
        "column": column,
        "data": df[column].dropna().tolist(),
        "title": f"Distribution of {column}"
    }


def make_bar_chart(df: pd.DataFrame, column: str, top_k: int = 20) -> Dict[str, Any]:
    value_counts = df[column].value_counts().head(top_k)

    return {
        "id": f"bar_{column}",
        "type": "bar",
        "column": column,
        "x": value_counts.index.astype(str).tolist(),
        "y": value_counts.values.tolist(),
        "title": f"Distribution of {column}"
    }


def make_line_chart(df: pd.DataFrame, datetime_col: str) -> Dict[str, Any]:
    temp_df = df.copy()
    temp_df["count"] = 1

    grouped = (
        temp_df
        .groupby(datetime_col)["count"]
        .sum()
        .reset_index()
        .sort_values(datetime_col)
    )

    return {
        "id": f"line_{datetime_col}",
        "type": "line",
        "x": grouped[datetime_col].astype(str).tolist(),
        "y": grouped["count"].tolist(),
        "title": f"Trend over time ({datetime_col})"
    }

def make_scatter(df: pd.DataFrame, x_col: str, y_col: str) -> Dict[str, Any]:
    return {
        "id": f"scatter_{x_col}_vs_{y_col}",
        "type": "scatter",
        "x": df[x_col].dropna().tolist(),
        "y": df[y_col].dropna().tolist(),
        "x_label": x_col,
        "y_label": y_col,
        "title": f"{x_col} vs {y_col}"
    }

def make_correlation_heatmap(df: pd.DataFrame) -> Dict[str, Any]:
    corr = df.corr(numeric_only=True)

    return {
        "id": "correlation_heatmap",
        "type": "heatmap",
        "x": corr.columns.tolist(),
        "y": corr.index.tolist(),
        "z": corr.values.tolist(),
        "title": "Correlation Heatmap"
    }

def make_boxplot(df: pd.DataFrame, column: str) -> Dict[str, Any]:
    return {
        "id": f"box_{column}",
        "type": "boxplot",
        "column": column,
        "data": df[column].dropna().tolist(),
        "title": f"Boxplot of {column}"
    }

def visualization_agent(
    df: pd.DataFrame,
    metadata: Dict[str, Any],
    max_numeric_charts: int = 6
) -> Dict[str, Any]:
    """
    Generates visualization specifications for React frontend.
    Works for ANY CSV.
    """

    charts: List[Dict[str, Any]] = []

    numeric_cols = metadata.get("numeric_columns", [])
    categorical_cols = metadata.get("categorical_columns", [])
    datetime_cols = metadata.get("datetime_columns", [])


    for col in numeric_cols[:max_numeric_charts]:
        charts.append(make_histogram(df, col))
        charts.append(make_boxplot(df, col))


    for col in categorical_cols:
        charts.append(make_bar_chart(df, col))

    for col in datetime_cols:
        charts.append(make_line_chart(df, col))

    if len(numeric_cols) >= 2:
        for i in range(min(2, len(numeric_cols))):
            for j in range(i + 1, min(3, len(numeric_cols))):
                charts.append(
                    make_scatter(df, numeric_cols[i], numeric_cols[j])
                )

    if len(numeric_cols) >= 2:
        charts.append(make_correlation_heatmap(df[numeric_cols]))

    return {
        "status": "success",
        "charts": charts,
        "total_charts": len(charts)
    }


if __name__ == "__main__":
    import os
    from pprint import pprint
    from Agents.data_cleaning import Preprocess_data
    from Agents.eda import run_eda_agent

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    filepath = os.path.join(
        BASE_DIR,
        "Data",
        "Heart_Disease_Prediction.csv"
    )
    response = Preprocess_data(file_path=filepath)

    df = response["dataframe"]
    metadata = response["metadata"]
    eda_response = run_eda_agent(df=df)
    charts = visualization_agent(
        df=df,
        metadata=metadata
    )
    pprint(charts)
