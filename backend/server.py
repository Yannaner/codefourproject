from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
from dotenv import load_dotenv
import openai
import json
import anthropic

# Load environment variables
# Try to load from both root and backend directories
load_dotenv()  # This will load from current working directory
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))  # This will load from backend directory

app = FastAPI(title="Case Law AI Assistant", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173", 
        "http://127.0.0.1:5173", 
        "http://localhost:5174", 
        "http://127.0.0.1:5174",
        "http://localhost:5175", 
        "http://127.0.0.1:5175"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Anthropic client
anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
if not anthropic_api_key:
    print("Warning: ANTHROPIC_API_KEY not found in environment variables")
    anthropic_client = None
else:
    try:
        anthropic_client = anthropic.Anthropic(api_key=anthropic_api_key)
        print("Anthropic client initialized successfully")
    except Exception as e:
        print(f"Error initializing Anthropic client: {e}")
        anthropic_client = None

# Pydantic models
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

class QueryResponse(BaseModel):
    query: str
    results: List[CaseSummary]
    total_results: int
    processing_time: float
    jurisdiction_filter: Optional[str] = None

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


MOCK_CASE_DATABASE = [
    {
        "case_name": "Terry v. Ohio",
        "citation": "392 U.S. 1 (1968)",
        "year": 1968,
        "court": "U.S. Supreme Court",
        "facts": "Police officer observed suspicious behavior and conducted a pat-down search for weapons",
        "legal_principle": "Fourth Amendment protection against unreasonable searches and seizures",
        "ruling": "Police may conduct limited search for weapons based on reasonable suspicion",
        "keywords": ["terry stop", "pat down", "reasonable suspicion", "search", "weapons", "fourth amendment"],
        "jurisdiction": "federal"
    },
    {
        "case_name": "Pennsylvania v. Mimms",
        "citation": "434 U.S. 106 (1977)", 
        "year": 1977,
        "court": "U.S. Supreme Court",
        "facts": "Officer ordered driver out of vehicle during routine traffic stop",
        "legal_principle": "Officer safety during traffic stops",
        "ruling": "Officers may order drivers out of vehicles during lawful traffic stops",
        "keywords": ["traffic stop", "officer safety", "vehicle", "driver", "exit vehicle"],
        "jurisdiction": "federal"
    },
    {
        "case_name": "United States v. Ross",
        "citation": "456 U.S. 798 (1982)",
        "year": 1982,
        "court": "U.S. Supreme Court", 
        "facts": "Police searched vehicle and containers within based on probable cause",
        "legal_principle": "Automobile exception to warrant requirement",
        "ruling": "Police may search vehicle and containers within if they have probable cause",
        "keywords": ["vehicle search", "automobile exception", "probable cause", "containers", "warrant"],
        "jurisdiction": "federal"
    },
    {
        "case_name": "California v. Acevedo",
        "citation": "500 U.S. 565 (1991)",
        "year": 1991,
        "court": "U.S. Supreme Court",
        "facts": "Police searched closed container in vehicle based on probable cause to believe it contained contraband",
        "legal_principle": "Container searches in vehicles",
        "ruling": "Police may search containers in vehicles without warrant if they have probable cause",
        "keywords": ["container search", "vehicle", "probable cause", "contraband", "closed container"],
        "jurisdiction": "federal"
    },
    {
        "case_name": "Illinois v. Caballes",
        "citation": "543 U.S. 405 (2005)",
        "year": 2005,
        "court": "U.S. Supreme Court",
        "facts": "Drug dog alerted to vehicle during traffic stop",
        "legal_principle": "Use of drug detection dogs during traffic stops",
        "ruling": "Dog sniff during lawful traffic stop does not violate Fourth Amendment",
        "keywords": ["drug dog", "canine", "traffic stop", "sniff", "fourth amendment", "detection"],
        "jurisdiction": "federal"
    },
    {
        "case_name": "State v. Johnson",
        "citation": "234 N.J. 567 (2018)",
        "year": 2018,
        "court": "New Jersey Supreme Court",
        "facts": "Officer conducted search incident to arrest for marijuana possession",
        "legal_principle": "Search incident to arrest in marijuana cases",
        "ruling": "Limited search incident to arrest permitted for officer safety",
        "keywords": ["search incident", "arrest", "marijuana", "officer safety", "new jersey"],
        "jurisdiction": "new_jersey"
    },
    {
        "case_name": "Commonwealth v. Smith",
        "citation": "456 Pa. 123 (2019)",
        "year": 2019,
        "court": "Pennsylvania Supreme Court",
        "facts": "Traffic stop led to vehicle search based on odor of marijuana",
        "legal_principle": "Probable cause from marijuana odor",
        "ruling": "Marijuana odor alone may not constitute probable cause in some circumstances",
        "keywords": ["marijuana odor", "probable cause", "vehicle search", "traffic stop", "pennsylvania"],
        "jurisdiction": "pennsylvania"
    },
    {
        "case_name": "People v. Rodriguez",
        "citation": "789 N.Y.2d 456 (2020)",
        "year": 2020,
        "court": "New York Court of Appeals",
        "facts": "Stop and frisk conducted in high-crime area based on suspicious behavior",
        "legal_principle": "Stop and frisk in high-crime areas",
        "ruling": "Location in high-crime area alone insufficient for reasonable suspicion",
        "keywords": ["stop and frisk", "high crime area", "reasonable suspicion", "terry stop", "new york"],
        "jurisdiction": "new_york"
    }
]

def search_cases_by_keywords(query: str, jurisdiction: str = "federal", max_results: int = 10) -> List[dict]:
    """Search mock database for relevant cases based on keywords and jurisdiction"""
    query_lower = query.lower()
    relevant_cases = []
    
    for case in MOCK_CASE_DATABASE:
        # Filter by jurisdiction
        if jurisdiction != "all" and case.get("jurisdiction", "federal") != jurisdiction:
            continue
            
        relevance_score = 0
        
        # Check keywords
        for keyword in case["keywords"]:
            if keyword in query_lower:
                relevance_score += 2
        
        # Check case name
        if any(word in case["case_name"].lower() for word in query_lower.split()):
            relevance_score += 1
            
        # Check facts and legal principle
        if any(word in case["facts"].lower() for word in query_lower.split()):
            relevance_score += 1
        if any(word in case["legal_principle"].lower() for word in query_lower.split()):
            relevance_score += 1
            
        if relevance_score > 0:
            case_copy = case.copy()
            case_copy["relevance_score"] = relevance_score
            relevant_cases.append(case_copy)
    
    # Sort by relevance score
    relevant_cases.sort(key=lambda x: x["relevance_score"], reverse=True)
    return relevant_cases[:max_results]

async def generate_ai_summary(case_data: dict, query: str, jurisdiction: str = "federal") -> CaseSummary:
    """Generate AI-powered summary and key takeaways for a case using Anthropic"""
    
    # Fallback summary and takeaways in case AI fails
    fallback_summary = f"In {case_data['case_name']}, the {case_data['court']} addressed {case_data['legal_principle'].lower()}. The court ruled that {case_data['ruling'].lower()}."
    fallback_takeaways = [
        "Review specific facts and circumstances of your situation",
        "Consider consulting department legal counsel for complex situations", 
        "Document all observations and justifications clearly in reports",
        "Follow department policies and procedures"
    ]
    
    # Check if Anthropic client is available
    if anthropic_client is None:
        print("Anthropic client not available, using fallback response")
        return CaseSummary(
            case_name=case_data["case_name"],
            citation=case_data["citation"], 
            year=case_data["year"],
            court=case_data["court"],
            summary=fallback_summary,
            key_takeaways=fallback_takeaways,
            facts=case_data["facts"],
            legal_principle=case_data["legal_principle"],
            ruling=case_data["ruling"],
            relevance_score=case_data["relevance_score"],
            jurisdiction=case_data.get("jurisdiction", "federal"),
            full_text_link=f"https://scholar.google.com/scholar_case?q={case_data['citation'].replace(' ', '+')}"
        )
    
    try:
        # Create a comprehensive prompt for Anthropic
        prompt = f"""
        You are a legal AI assistant helping police officers understand case law. 
        
        Case Information:
        - Case Name: {case_data['case_name']}
        - Citation: {case_data['citation']}
        - Year: {case_data['year']}
        - Court: {case_data['court']}
        - Facts: {case_data['facts']}
        - Legal Principle: {case_data['legal_principle']}
        - Ruling: {case_data['ruling']}
        - Jurisdiction: {case_data.get('jurisdiction', 'federal')}
        
        Officer's Query: "{query}"
        Target Jurisdiction: {jurisdiction}
        
        Please provide:
        1. A clear, concise summary (2-3 sentences) of how this case relates to the officer's query
        2. 4-6 specific, actionable key takeaways for police officers
        
        Focus on practical application and officer safety. Make the language clear and professional.
        """
        
        response = anthropic_client.messages.create(
            model="claude-3-5-haiku-20241022",
            max_tokens=1000,
            temperature=0.3,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        
        ai_response = response.content[0].text
        
        # Parse the AI response to extract summary and key takeaways
        lines = ai_response.strip().split('\n')
        summary_lines = []
        takeaways = []
        
        current_section = None
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            if 'summary' in line.lower() or line.startswith('1.'):
                current_section = 'summary'
                if line.startswith('1.'):
                    summary_lines.append(line[2:].strip())
                continue
            elif 'takeaway' in line.lower() or 'key points' in line.lower() or line.startswith('2.'):
                current_section = 'takeaways'
                continue
                
            if current_section == 'summary' and not line.startswith('-') and not line.startswith('•'):
                summary_lines.append(line)
            elif current_section == 'takeaways' and (line.startswith('-') or line.startswith('•') or line.startswith('*')):
                takeaway = line.lstrip('-•* ').strip()
                if takeaway:
                    takeaways.append(takeaway)
        
        # Use AI response if parsing successful, otherwise use fallback
        if not summary_lines:
            summary = fallback_summary
        else:
            summary = ' '.join(summary_lines)
            
        if not takeaways:
            takeaways = fallback_takeaways
            
    except Exception as e:
        print(f"AI generation error: {e}")
        # Use fallback content
        summary = fallback_summary
        takeaways = fallback_takeaways
    
    return CaseSummary(
        case_name=case_data["case_name"],
        citation=case_data["citation"], 
        year=case_data["year"],
        court=case_data["court"],
        summary=summary,
        key_takeaways=takeaways,
        facts=case_data["facts"],
        legal_principle=case_data["legal_principle"],
        ruling=case_data["ruling"],
        relevance_score=case_data["relevance_score"],
        jurisdiction=case_data.get("jurisdiction", "federal"),
        full_text_link=f"https://scholar.google.com/scholar_case?q={case_data['citation'].replace(' ', '+')}"
    )

async def generate_actionable_report(query: str, case_results: List[CaseSummary], jurisdiction: str = "federal") -> ReportResponse:
    """Generate comprehensive actionable insights report using Anthropic AI"""
    
    # Fallback response in case AI fails
    from datetime import datetime
    
    fallback_response = ReportResponse(
        query=query,
        executive_summary=f"Based on available case law, officers should exercise caution and follow established procedures when dealing with situations involving: {query}",
        key_insights=[
            ActionableInsight(
                category="General Guidance",
                insight="Follow constitutional and department requirements",
                action_items=["Document all actions", "Seek supervisor guidance"],
                legal_considerations=["Ensure legal compliance", "Avoid constitutional violations"]
            )
        ],
        procedural_recommendations=[
            "Document all observations thoroughly",
            "Follow department procedures",
            "Consult legal counsel when uncertain"
        ],
        legal_warnings=[
            "Ensure constitutional compliance",
            "Document legal justification for all actions"
        ],
        jurisdiction_specific_notes=[
            "Verify local laws and regulations",
            "Consult department legal resources"
        ],
        generated_at=datetime.now().isoformat()
    )
    
    # Check if Anthropic client is available
    if anthropic_client is None:
        print("Anthropic client not available, using fallback report")
        return fallback_response
    
    try:
        # Prepare case summaries for the prompt
        cases_text = ""
        for i, case in enumerate(case_results, 1):
            cases_text += f"""
            Case {i}: {case.case_name} ({case.citation})
            Court: {case.court}
            Year: {case.year}
            Facts: {case.facts}
            Legal Principle: {case.legal_principle}
            Ruling: {case.ruling}
            Key Takeaways: {', '.join(case.key_takeaways)}
            
            """
        
        prompt = f"""
        You are a legal expert providing actionable insights to police officers. Based on the officer's query and relevant case law, generate a comprehensive report with practical guidance.

        Officer's Query: "{query}"
        Target Jurisdiction: {jurisdiction}
        
        Relevant Case Law:
        {cases_text}
        
        Please provide a structured report with:

        1. EXECUTIVE SUMMARY (2-3 sentences summarizing the legal landscape for this query)

        2. KEY INSIGHTS (3-4 categorized insights with specific action items):
           - Format: Category | Insight | Action Items | Legal Considerations

        3. PROCEDURAL RECOMMENDATIONS (4-6 specific steps officers should follow)

        4. LEGAL WARNINGS (Critical legal pitfalls to avoid)

        5. JURISDICTION-SPECIFIC NOTES (How {jurisdiction} law may differ from federal precedent)

        Focus on:
        - Officer safety and legal compliance
        - Clear, actionable guidance
        - Risk mitigation
        - Documentation requirements
        - When to seek legal counsel

        Use professional law enforcement language.
        """
        
        response = anthropic_client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2000,
            temperature=0.2,
            messages=[
                {
                    "role": "user", 
                    "content": prompt
                }
            ]
        )
        
        ai_response = response.content[0].text
        
        # Parse the AI response
        sections = {
            'executive_summary': '',
            'key_insights': [],
            'procedural_recommendations': [],
            'legal_warnings': [],
            'jurisdiction_notes': []
        }
        
        current_section = None
        lines = ai_response.strip().split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Identify sections
            if 'executive summary' in line.lower():
                current_section = 'executive_summary'
                continue
            elif 'key insights' in line.lower():
                current_section = 'key_insights'
                continue
            elif 'procedural recommendations' in line.lower():
                current_section = 'procedural_recommendations'
                continue
            elif 'legal warnings' in line.lower():
                current_section = 'legal_warnings'
                continue
            elif 'jurisdiction' in line.lower() and 'notes' in line.lower():
                current_section = 'jurisdiction_notes'
                continue
                
            # Parse content based on current section
            if current_section == 'executive_summary' and not line.startswith('-') and not line.startswith('•'):
                sections['executive_summary'] += line + ' '
            elif current_section in ['procedural_recommendations', 'legal_warnings', 'jurisdiction_notes']:
                if line.startswith('-') or line.startswith('•') or line.startswith('*'):
                    clean_line = line.lstrip('-•* ').strip()
                    if clean_line:
                        sections[current_section].append(clean_line)
            elif current_section == 'key_insights':
                if '|' in line:
                    parts = [p.strip() for p in line.split('|')]
                    if len(parts) >= 4:
                        insight = ActionableInsight(
                            category=parts[0],
                            insight=parts[1],
                            action_items=[parts[2]] if parts[2] else [],
                            legal_considerations=[parts[3]] if parts[3] else []
                        )
                        sections['key_insights'].append(insight)
                elif line.startswith('-') or line.startswith('•'):
                    # Fallback parsing for insights
                    clean_line = line.lstrip('-•* ').strip()
                    if clean_line and len(sections['key_insights']) < 4:
                        insight = ActionableInsight(
                            category="General",
                            insight=clean_line,
                            action_items=["Follow department protocols"],
                            legal_considerations=["Consult legal counsel if uncertain"]
                        )
                        sections['key_insights'].append(insight)
        
        # Generate fallback content if parsing fails
        if not sections['executive_summary'].strip():
            sections['executive_summary'] = f"Based on relevant case law, officers dealing with {query.lower()} situations must balance constitutional requirements with operational safety."
            
        if not sections['key_insights']:
            sections['key_insights'] = [
                ActionableInsight(
                    category="Constitutional Compliance",
                    insight="Ensure all actions meet Fourth Amendment standards",
                    action_items=["Document reasonable suspicion/probable cause", "Follow established procedures"],
                    legal_considerations=["Constitutional violations can lead to evidence suppression", "Civil liability concerns"]
                ),
                ActionableInsight(
                    category="Officer Safety",
                    insight="Prioritize officer and public safety in all interactions",
                    action_items=["Maintain situational awareness", "Use appropriate officer safety measures"],
                    legal_considerations=["Safety measures must be legally justified", "Excessive force issues"]
                )
            ]
            
        if not sections['procedural_recommendations']:
            sections['procedural_recommendations'] = [
                "Document all observations and actions thoroughly",
                "Articulate reasonable suspicion or probable cause clearly",
                "Follow department standard operating procedures",
                "Seek supervisor consultation for complex situations"
            ]
            
        if not sections['legal_warnings']:
            sections['legal_warnings'] = [
                "Avoid actions that could violate constitutional rights",
                "Ensure proper legal justification before conducting searches",
                "Be aware of changing legal precedents"
            ]
            
        if not sections['jurisdiction_notes']:
            sections['jurisdiction_notes'] = [
                f"Verify current {jurisdiction} statutes and regulations",
                "Local case law may provide additional guidance or restrictions",
                "Consult department legal counsel for jurisdiction-specific questions"
            ]
        
        return ReportResponse(
            query=query,
            executive_summary=sections['executive_summary'].strip(),
            key_insights=sections['key_insights'],
            procedural_recommendations=sections['procedural_recommendations'],
            legal_warnings=sections['legal_warnings'],
            jurisdiction_specific_notes=sections['jurisdiction_notes'],
            generated_at=datetime.now().isoformat()
        )
        
    except Exception as e:
        print(f"Report generation error: {e}")
        # Return fallback response
        return fallback_response

@app.get("/")
async def root():
    return {"message": "Case Law AI Assistant API", "version": "1.0.0"}

@app.post("/search", response_model=QueryResponse)
async def search_case_law(request: QueryRequest):
    """Search for relevant case law based on natural language query and jurisdiction"""
    import time
    start_time = time.time()
    
    try:
        # Search for relevant cases with jurisdiction filtering
        relevant_cases = search_cases_by_keywords(request.query, request.jurisdiction or "federal")
        
        # Generate AI summaries for each case
        case_summaries = []
        for case_data in relevant_cases:
            summary = await generate_ai_summary(case_data, request.query, request.jurisdiction or "federal")
            case_summaries.append(summary)
        
        processing_time = time.time() - start_time
        
        return QueryResponse(
            query=request.query,
            results=case_summaries,
            total_results=len(case_summaries),
            processing_time=round(processing_time, 3),
            jurisdiction_filter=request.jurisdiction
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")

@app.post("/generate-report", response_model=ReportResponse)
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

@app.get("/jurisdictions")
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

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": "2025-06-29"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)