from pydantic import BaseModel
from typing import List, Optional

class QueryRequest(BaseModel):
    query: str
    jurisdiction: Optional[str] = "federal"

class CaseSummary(BaseModel):
    case_name: str
    citation: str
    year: int
    court: str
    summary: str
    key_takeaways: List[str]
    facts: str
    legal_principle: str
    ruling: str
    relevance_score: float
    full_text_link: Optional[str] = None
    jurisdiction: Optional[str] = "federal"

class QueryClarification(BaseModel):
    needs_clarification: bool
    clarification_message: str
    suggested_refinements: List[str]
    original_query: str

class QueryResponse(BaseModel):
    query: str
    results: List[CaseSummary]
    total_results: int
    processing_time: float
    jurisdiction_filter: Optional[str] = None
    clarification: Optional[QueryClarification] = None

class ReportRequest(BaseModel):
    query: str
    case_results: List[CaseSummary]
    jurisdiction: Optional[str] = "federal"

class ActionableInsight(BaseModel):
    category: str
    insight: str
    action_items: List[str]
    legal_considerations: List[str]

class ReportResponse(BaseModel):
    query: str
    executive_summary: str
    key_insights: List[ActionableInsight]
    procedural_recommendations: List[str]
    legal_warnings: List[str]
    jurisdiction_specific_notes: List[str]
    generated_at: str
