import os
import pandas as pd
from typing_extensions import TypedDict,Dict,List,Literal,Any
import numpy as np


# Read CSV into Pandas
# Normalize column names
# Handle missing values
# Infer data types
# Remove duplicates


def LoadData(file_path: str) -> pd.DataFrame:
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    df = pd.read_csv(file_path)
    print(f"Data loaded successfully ====> Length: {len(df)}")
    return df



def normalize_column_name(df:pd.DataFrame):
    """
        Normalize column names:
        - lowercase
        - remove spaces
        - replace special characters with underscore
    """
    df.columns = (
            df.columns
            .str.strip()
            .str.lower()
            .str.replace(" ", "_")
            .str.replace(r"[^\w]", "", regex=True)
        )
    return df


def Infer_datatypes(df: pd.DataFrame) -> pd.DataFrame:
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="ignore")

        if df[col].dtype == "object":
            try:
                df[col] = pd.to_datetime(df[col])
            except Exception:
                pass
    print("Datatypes inferred successfully............") 
    return df


def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Handle missing values from the dataframe
    numerical columns: fill with median (more robust to outliers than mean)
    categorical columns: fill with mode
    binary columns: fill with mode
    """
    
    df_copy = df.copy()  
    
    for col in df_copy.columns:
        if df_copy[col].isnull().sum() > 0:
            if df_copy[col].dtype == "object":
                mode_values = df_copy[col].mode()
                if not mode_values.empty:
                    df_copy[col].fillna(mode_values[0], inplace=True)
                else:
                    df_copy[col].fillna("Unknown", inplace=True)
            
            elif np.issubdtype(df_copy[col].dtype, np.number):
                median_value = df_copy[col].median()
                df_copy[col].fillna(median_value, inplace=True)
            
            elif df_copy[col].dtype == "bool":
                mode_values = df_copy[col].mode()
                if not mode_values.empty:
                    df_copy[col].fillna(mode_values[0], inplace=True)
                else:
                    df_copy[col].fillna(False, inplace=True)
    print("Missing Value Handeld Successfully..........")
    return df_copy

def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove duplicate rows
    """
    print('Duplicate remove successfully........')
    return df.drop_duplicates()

def generate_metadata(df: pd.DataFrame) -> Dict[str, Any]:
    return {
        "rows": int(df.shape[0]),
        "columns": list(df.columns),
        "numeric_columns": df.select_dtypes(include="number").columns.tolist(),
        "categorical_columns": df.select_dtypes(include="object").columns.tolist(),
        "datetime_columns": df.select_dtypes(include="datetime").columns.tolist(),
        "missing_values": {
            col: int(val) for col, val in df.isnull().sum().items()
        }
    }


def Preprocess_data(file_path:str):
    """
    Complete data preprocessing pipeline
    """
    try:
        df = LoadData(file_path)
        df = normalize_column_name(df)
        df = remove_duplicates(df) 
        df = Infer_datatypes(df)
        df = handle_missing_values(df)
        df = remove_duplicates(df)
        metadata = generate_metadata(df)
        
        return {
            "dataframe": df,
            "metadata": metadata,
            "status": "success",
            "message": "Data preprocessing completed successfully"
        }
        
    except Exception as e:
        return {
            "dataframe": None,
            "metadata": {},
            "status": "error",
            "message": f"Error during preprocessing: {str(e)}"
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
    pprint(response['metadata'])