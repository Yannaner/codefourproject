export interface CaseSummary {
  case_name: string;
  citation: string;
  year: number;
  court: string;
  summary: string;
  key_takeaways: string[];
  facts: string;
  legal_principle: string;
  ruling: string;
  relevance_score: number;
  full_text_link?: string;
  jurisdiction?: string;
}

export interface QueryClarification {
  needs_clarification: boolean;
  clarification_message: string;
  suggested_refinements: string[];
  original_query: string;
}

export interface QueryResponse {
  query: string;
  results: CaseSummary[];
  total_results: number;
  processing_time: number;
  jurisdiction_filter?: string;
  clarification?: QueryClarification;
}

export interface QueryRequest {
  query: string;
  jurisdiction?: string;
}

export interface ActionableInsight {
  category: string;
  insight: string;
  action_items: string[];
  legal_considerations: string[];
}

export interface ReportResponse {
  query: string;
  executive_summary: string;
  key_insights: ActionableInsight[];
  procedural_recommendations: string[];
  legal_warnings: string[];
  jurisdiction_specific_notes: string[];
  generated_at: string;
}

export interface ReportRequest {
  query: string;
  case_results: CaseSummary[];
  jurisdiction?: string;
}

export interface Jurisdiction {
  value: string;
  label: string;
}
