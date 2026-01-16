import pandas as pd
import numpy as np
import os
from typing import Dict,Any,List
from Agents.data_cleaning import Preprocess_data


def dataset_overview(df:pd.DataFrame)->Dict[str, int]:
    "this will return the number of rows and  dataframe shape"
    return{
        "rows":int(df.shape[0]),
        "columns":int(df.shape[1])
    }


def columns_types(df:pd.DataFrame)->Dict[str, List]:
    return{
        "numeric" : df.select_dtypes(include="number").columns.tolist(),
        "categorical" : df.select_dtypes(include="object").columns.tolist(),
        "datetime": df.select_dtypes(include="datetime").columns.tolist()
    }


def Summary_statistics(df:pd.DataFrame)->Dict[str,Dict[str,float]]:
    stats = {}
    numeric_cols = df.select_dtypes(include="number")
    for col in numeric_cols.columns:
        stats[col] = {
            "count": int(numeric_cols[col].count()),
            "mean": float(numeric_cols[col].mean()),
            "median": float(numeric_cols[col].median()),
            "std": float(numeric_cols[col].std()),
            "min": float(numeric_cols[col].min()),
            "max": float(numeric_cols[col].max())
        }
    return stats



def categorical_distribution(df:pd.DataFrame)->Dict[str,Dict[str,int]]:
    distributions = {}
    cat_cols = df.select_dtypes(include="object")
    for col in cat_cols.columns:
        value_counts = cat_cols[col].value_counts()
        distributions[col]={
            str(k):int(v) for k,v in value_counts.items()
        }
    return distributions

def correlations(df:pd.DataFrame):
    corr_result = {}
    numeric_df = df.select_dtypes(include="number")

    if numeric_df.shape[1] < 2:
        return corr_result

    corr_matrix = numeric_df.corr()
    for col1 in corr_matrix.columns:
        for col2 in corr_matrix.columns:
            if col1 < col2:
                corr_result[f"{col1}_vs_{col2}"] = float(
                    corr_matrix.loc[col1, col2]
                )

    return corr_result

def missing_values(df: pd.DataFrame) -> Dict[str, int]:
        return {
            col: int(df[col].isnull().sum())
            for col in df.columns
        }

def detect_outliers(df: pd.DataFrame) -> Dict[str, Dict[str, float]]:
        outliers = {}
        numeric_cols = df.select_dtypes(include="number")

        for col in numeric_cols.columns:
            q1 = numeric_cols[col].quantile(0.25)
            q3 = numeric_cols[col].quantile(0.75)
            iqr = q3 - q1

            lower = q1 - 1.5 * iqr
            upper = q3 + 1.5 * iqr

            count = int(((numeric_cols[col] < lower) | (numeric_cols[col] > upper)).sum())

            outliers[col] = {
                "lower_bound": float(lower),
                "upper_bound": float(upper),
                "outliers_count": count
            }

        return outliers


def run_eda_agent(df: pd.DataFrame):
    """
    This agent will basically create the deep analysis of the data.
    """
    return {
        "overview": dataset_overview(df),
        "column_types": columns_types(df),
        "summary_statistics": Summary_statistics(df),
        "categorical_distributions": categorical_distribution(df),
        "correlations": correlations(df),
        "missing_values": missing_values(df),
        "outliers": detect_outliers(df)
    }


if __name__ == "__main__":
    from pprint import pprint
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    filepath = os.path.join(
        BASE_DIR,
        "Data",
        "Heart_Disease_Prediction.csv"
    )
    response=Preprocess_data(file_path=filepath)
    response=run_eda_agent(df=response['dataframe'])
    pprint(response)