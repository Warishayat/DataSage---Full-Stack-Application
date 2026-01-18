import pandas as pd
import numpy as np
from typing import Dict, Any, List

def clean_for_json(obj):
    if isinstance(obj, list):
        return [clean_for_json(i) for i in obj]
    if isinstance(obj, dict):
        return {k: clean_for_json(v) for k, v in obj.items()}
    if isinstance(obj, (float, np.float64, np.float32)):
        return 0.0 if np.isnan(obj) or np.isinf(obj) else float(obj)
    if isinstance(obj, (int, np.int64, np.int32)):
        return int(obj)
    return obj

def make_histogram(df: pd.DataFrame, column: str) -> Dict[str, Any]:
    data_series = df[column].dropna()
    if len(data_series) > 1000:
        data_series = data_series.sample(1000)
    return {
        "id": f"hist_{column}",
        "type": "histogram",
        "column": column,
        "data": clean_for_json(data_series.astype(float).tolist()),
        "title": f"Distribution of {column}"
    }

def make_bar_chart(df: pd.DataFrame, column: str, top_k: int = 15) -> Dict[str, Any]:
    value_counts = df[column].value_counts().head(top_k)
    return {
        "id": f"bar_{column}",
        "type": "bar",
        "column": column,
        "x": value_counts.index.astype(str).tolist(),
        "y": [int(v) for v in value_counts.values],
        "title": f"Total Counts by {column}"
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
        "y": grouped["count"].astype(int).tolist(),
        "title": f"Trend Analysis: {datetime_col}"
    }

def make_scatter(df: pd.DataFrame, x_col: str, y_col: str) -> Dict[str, Any]:
    temp_df = df[[x_col, y_col]].dropna()
    if len(temp_df) > 800:
        temp_df = temp_df.sample(800)
    return {
        "id": f"scatter_{x_col}_vs_{y_col}",
        "type": "scatter",
        "x": clean_for_json(temp_df[x_col].astype(float).tolist()),
        "y": clean_for_json(temp_df[y_col].astype(float).tolist()),
        "x_label": x_col,
        "y_label": y_col,
        "title": f"Correlation: {x_col} vs {y_col}"
    }

def make_correlation_heatmap(df: pd.DataFrame) -> Dict[str, Any]:
    corr = df.corr(numeric_only=True).fillna(0)
    return {
        "id": "correlation_heatmap",
        "type": "heatmap",
        "x": corr.columns.tolist(),
        "y": corr.index.tolist(),
        "z": clean_for_json(corr.values.tolist()),
        "title": "Feature Correlation Heatmap"
    }

def make_boxplot(df: pd.DataFrame, column: str) -> Dict[str, Any]:
    data_series = df[column].dropna()
    if len(data_series) > 1000:
        data_series = data_series.sample(1000)
    return {
        "id": f"box_{column}",
        "type": "boxplot",
        "column": column,
        "data": clean_for_json(data_series.astype(float).tolist()),
        "title": f"Outliers Detection: {column}"
    }

def visualization_agent(
    df: pd.DataFrame,
    metadata: Dict[str, Any],
    max_numeric_charts: int = 6
) -> Dict[str, Any]:
    charts: List[Dict[str, Any]] = []
    numeric_cols = metadata.get("numeric_columns", [])
    categorical_cols = metadata.get("categorical_columns", [])
    datetime_cols = metadata.get("datetime_columns", [])

    if len(numeric_cols) >= 2:
        charts.append(make_correlation_heatmap(df[numeric_cols]))

    for col in numeric_cols[:max_numeric_charts]:
        charts.append(make_histogram(df, col))
        charts.append(make_boxplot(df, col))

    for col in categorical_cols[:5]:
        charts.append(make_bar_chart(df, col))

    for col in datetime_cols:
        charts.append(make_line_chart(df, col))

    if len(numeric_cols) >= 2:
        for i in range(min(1, len(numeric_cols))):
            for j in range(i + 1, min(3, len(numeric_cols))):
                charts.append(make_scatter(df, numeric_cols[i], numeric_cols[j]))

    return {
        "status": "success",
        "charts": charts,
        "total_charts": int(len(charts))
    }