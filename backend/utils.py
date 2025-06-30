from typing import Optional
import re
from models import QueryClarification

def analyze_query_clarity(query: str) -> Optional[QueryClarification]:
    """Analyze if query is too vague and needs clarification"""
    query_lower = query.lower().strip()
    
    # Define vague query patterns
    vague_patterns = [
        # Single word queries
        r'^(search|arrest|traffic|stop|rights|law|case|legal|searching)$',
        # Very short queries (less than 3 words)
        r'^\w+\s*\w*$',
        # Generic questions
        r'^(what|how|when|why|can|should|may)\s+(i|we|you|police|officer)',
        # Overly broad terms
        r'^(help|info|information|about|regarding)(\s+\w+)?$'
    ]
    
    vague_keywords = [
        'help', 'info', 'information', 'about', 'general', 'basic', 
        'anything', 'everything', 'law', 'legal', 'rights', 'procedure'
    ]
    
    # Check for vague patterns
    is_vague = False
    for pattern in vague_patterns:
        if re.match(pattern, query_lower):
            is_vague = True
            break
    
    # Check if query is too short and generic
    words = query_lower.split()
    if len(words) <= 2 and any(word in vague_keywords for word in words):
        is_vague = True
    
    # Check if query contains only very general legal terms
    general_terms = ['law', 'legal', 'case', 'court', 'rule', 'procedure', 'right', 'rights']
    if len(words) <= 3 and all(word in general_terms or len(word) <= 2 for word in words):
        is_vague = True
    
    if not is_vague:
        return None
    
    # Generate clarification suggestions based on query content
    suggestions = []
    
    if 'search' in query_lower:
        suggestions = [
            "vehicle search without consent",
            "search incident to arrest",
            "search warrant requirements",
            "consent to search procedures"
        ]
    elif 'traffic' in query_lower or 'stop' in query_lower:
        suggestions = [
            "traffic stop duration limits",
            "vehicle search during traffic stop", 
            "passenger rights during traffic stop",
            "DUI investigation procedures"
        ]
    elif 'arrest' in query_lower:
        suggestions = [
            "arrest warrant requirements",
            "warrantless arrest authority",
            "arrest procedures for specific crimes",
            "Miranda rights timing"
        ]
    elif 'rights' in query_lower:
        suggestions = [
            "Miranda rights requirements",
            "Fourth Amendment search rights",
            "suspect's right to counsel",
            "passenger rights during stops"
        ]
    else:
        # Generic suggestions for very vague queries
        suggestions = [
            "vehicle search procedures",
            "traffic stop authority",
            "arrest warrant requirements", 
            "evidence collection rules",
            "Miranda rights timing",
            "use of force guidelines"
        ]
    
    clarification_message = "Your query seems quite broad. To provide more relevant case law and guidance, could you be more specific about the situation or legal issue you're dealing with?"
    
    return QueryClarification(
        needs_clarification=True,
        clarification_message=clarification_message,
        suggested_refinements=suggestions[:4],
        original_query=query
    )
