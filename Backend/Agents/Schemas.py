from pydantic import BaseModel
from typing import List

class InsightResponse(BaseModel):
    summary: str
    key_insights: List[str]
    risks: List[str]
    recommendations: List[str]
