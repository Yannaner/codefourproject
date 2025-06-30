from typing import List
from datetime import datetime
from models import CaseSummary, ActionableInsight, ReportResponse
from config import anthropic_client

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
