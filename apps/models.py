# apps/models.py
from pydantic import BaseModel
from typing import Any, Dict, List

class QueryRequest(BaseModel):
    question: str


class QueryResponse(BaseModel):
    question: str
    sql: str
    result: List[Dict[str, Any]]
    answer: str
