from fastapi import APIRouter, HTTPException
import time
import asyncio
from models import QueryRequest, QueryResponse, ReportRequest, ReportResponse
from database import search_cases_by_keywords
from ai_services import generate_ai_summary, generate_actionable_report
from utils import analyze_query_clarity

router = APIRouter()

@router.get("/")
async def root():
    return {"message": "Case Law AI Assistant API", "version": "1.0.0"}

@router.post("/search", response_model=QueryResponse)
async def search_case_law(request: QueryRequest):
    """Search for relevant case law based on natural language query and jurisdiction"""
    start_time = time.time()
    
    try:
        # Check if query needs clarification
        clarification = analyze_query_clarity(request.query)
        
        if clarification:
            # Return clarification request instead of search results
            return QueryResponse(
                query=request.query,
                results=[],
                total_results=0,
                processing_time=round(time.time() - start_time, 3),
                jurisdiction_filter=request.jurisdiction,
                clarification=clarification
            )
        
        # Search for relevant cases with jurisdiction filtering
        relevant_cases = search_cases_by_keywords(request.query, request.jurisdiction or "federal")
        
        # Generate AI summaries for each case concurrently
        if relevant_cases:
            # Create tasks for concurrent processing
            tasks = [
                generate_ai_summary(case_data, request.query, request.jurisdiction or "federal")
                for case_data in relevant_cases
            ]
            
            # Execute all AI generation tasks concurrently
            case_summaries = await asyncio.gather(*tasks)
        else:
            case_summaries = []
        
        processing_time = time.time() - start_time
        
        return QueryResponse(
            query=request.query,
            results=case_summaries,
            total_results=len(case_summaries),
            processing_time=round(processing_time, 3),
            jurisdiction_filter=request.jurisdiction,
            clarification=None
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")

@router.post("/generate-report", response_model=ReportResponse)
async def generate_report(request: ReportRequest):
    """Generate actionable insights report based on case law search results"""
    try:
        report = await generate_actionable_report(
            request.query, 
            request.case_results, 
            request.jurisdiction or "federal"
        )
        return report
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating report: {str(e)}")

@router.get("/jurisdictions")
async def get_jurisdictions():
    """Get available jurisdictions for filtering"""
    return {
        "jurisdictions": [
            {"value": "all", "label": "All Jurisdictions"},
            {"value": "federal", "label": "Federal Courts"},
            {"value": "new_jersey", "label": "New Jersey"},
            {"value": "pennsylvania", "label": "Pennsylvania"},
            {"value": "new_york", "label": "New York"}
        ]
    }

@router.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": "2025-06-29"}
