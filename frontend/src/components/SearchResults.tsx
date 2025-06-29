import React from 'react';
import { Clock, ExternalLink, Scale, CheckCircle } from 'lucide-react';
import type { QueryResponse } from '../types';
import CaseCard from './CaseCard';
import './SearchResults.css';

interface SearchResultsProps {
  results: QueryResponse;
}

const SearchResults: React.FC<SearchResultsProps> = ({ results }) => {
  return (
    <div className="search-results">
      <div className="results-header">
        <div className="results-info">
          <Scale className="results-icon" size={24} />
          <div>
            <h3 className="results-title">Search Results</h3>
            <p className="results-meta">
              Found {results.total_results} relevant cases in {results.processing_time}s
            </p>
          </div>
        </div>
        <div className="results-query">
          <strong>Query:</strong> "{results.query}"
        </div>
      </div>

      {results.results.length === 0 ? (
        <div className="no-results">
          <p>No relevant cases found. Try rephrasing your query or using different legal terms.</p>
        </div>
      ) : (
        <div className="cases-grid">
          {results.results.map((caseData, index) => (
            <CaseCard key={`${caseData.citation}-${index}`} caseData={caseData} rank={index + 1} />
          ))}
        </div>
      )}
    </div>
  );
};

export default SearchResults;
