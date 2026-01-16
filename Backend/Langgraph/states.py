from typing import TypedDict, Optional
import pandas as pd

class DataState(TypedDict):
    file_path: str
    df: Optional[pd.DataFrame]
    metadata: Optional[dict]
    eda: Optional[dict]
    charts: Optional[dict]
    insights: Optional[dict]
    report: Optional[dict]
