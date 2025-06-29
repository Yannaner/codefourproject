import React, { useState, useEffect } from 'react';
import { Search, Loader2, FileText, MapPin } from 'lucide-react';
import { searchCaseLaw, generateReport, getJurisdictions } from '../services/api';
import type { QueryResponse, ReportResponse, Jurisdiction } from '../types';
import SearchResults from './SearchResults';
import './SearchInterface.css';

const SearchInterface: React.FC = () => {
  const [query, setQuery] = useState('');
  const [jurisdiction, setJurisdiction] = useState('federal');
  const [jurisdictions, setJurisdictions] = useState<Jurisdiction[]>([]);
  const [results, setResults] = useState<QueryResponse | null>(null);
  const [report, setReport] = useState<ReportResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [generatingReport, setGeneratingReport] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchJurisdictions = async () => {
      try {
        const jurisdictionData = await getJurisdictions();
        setJurisdictions(jurisdictionData);
      } catch (err) {
        console.error('Failed to fetch jurisdictions:', err);
        // Fallback jurisdictions
        setJurisdictions([
          { value: 'all', label: 'All Jurisdictions' },
          { value: 'federal', label: 'Federal Courts' },
          { value: 'new_jersey', label: 'New Jersey' },
          { value: 'pennsylvania', label: 'Pennsylvania' },
          { value: 'new_york', label: 'New York' }
        ]);
      }
    };

    fetchJurisdictions();
  }, []);

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;

    setLoading(true);
    setError(null);
    setReport(null);

    try {
      const response = await searchCaseLaw({ 
        query: query.trim(), 
        jurisdiction: jurisdiction 
      });
      setResults(response);
      
      // Automatically generate the action report after getting results
      if (response && response.results.length > 0) {
        setGeneratingReport(true);
        try {
          const reportResponse = await generateReport({
            query: response.query,
            case_results: response.results,
            jurisdiction: jurisdiction
          });
          setReport(reportResponse);
        } catch (reportErr) {
          console.error('Failed to generate report:', reportErr);
          // Don't show error for report generation, just log it
        } finally {
          setGeneratingReport(false);
        }
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
      setResults(null);
    } finally {
      setLoading(false);
    }
  };

  const exampleQueries = [
    "Can I search a vehicle without consent if I smell marijuana?",
    "What are the legal requirements for a Terry stop?",
    "Case law on plain view doctrine",
    "When can I order a driver out of their vehicle?",
    "Drug dog searches during traffic stops"
  ];

  return (
    <div className="search-interface">
      <div className="search-container">
        <div className="search-header">
          <h2 className="search-title">Search Case Law</h2>
          <p className="search-description">
            Ask questions in plain English about legal procedures, constitutional rights, and case law precedents.
          </p>
        </div>

        <form onSubmit={handleSearch} className="search-form">
          <div className="jurisdiction-selector">
            <MapPin className="jurisdiction-icon" size={16} />
            <select 
              value={jurisdiction} 
              onChange={(e) => setJurisdiction(e.target.value)}
              className="jurisdiction-select"
              disabled={loading}
            >
              {jurisdictions.map((j) => (
                <option key={j.value} value={j.value}>
                  {j.label}
                </option>
              ))}
            </select>
          </div>

          <div className="search-input-container">
            <Search className="search-icon" size={20} />
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="e.g., Can I search a vehicle without consent if I smell marijuana?"
              className="search-input"
              disabled={loading}
            />
          </div>
          <button 
            type="submit" 
            className="search-button"
            disabled={loading || !query.trim()}
          >
            {loading ? (
              <Loader2 className="loading-icon" size={20} />
            ) : (
              'Search'
            )}
          </button>
        </form>

        <div className="example-queries">
          <h3 className="example-title">Example Queries:</h3>
          <div className="example-buttons">
            {exampleQueries.map((example, index) => (
              <button
                key={index}
                onClick={() => setQuery(example)}
                className="example-button"
                disabled={loading}
              >
                {example}
              </button>
            ))}
          </div>
        </div>

        {error && (
          <div className="error-message">
            <p>Error: {error}</p>
          </div>
        )}

        {results && (
          <div className="results-container">
            {/* Executive Summary First - Full Width Banner */}
            {report && (
              <div className="executive-summary-banner">
                <div className="summary-header">
                  <FileText size={24} />
                  <h3>Executive Summary</h3>
                </div>
                <p className="summary-text">{report.executive_summary}</p>
                <div className="summary-meta">
                  <span>Query: "{report.query}"</span>
                  <span>Generated {new Date(report.generated_at).toLocaleString()}</span>
                </div>
              </div>
            )}
            
            {generatingReport && !report && (
              <div className="executive-summary-banner loading">
                <div className="summary-header">
                  <Loader2 className="loading-icon" size={24} />
                  <h3>Generating Executive Summary...</h3>
                </div>
                <div className="loading-placeholder">
                  <div className="loading-line"></div>
                  <div className="loading-line short"></div>
                  <div className="loading-line"></div>
                </div>
              </div>
            )}

            <div className="results-layout">
              <div className="results-section">
                <div className="section-header">
                  <h3 className="section-title">📚 Case Law Results</h3>
                  <div className="results-meta">
                    <span className="results-count">{results.total_results} cases found</span>
                    <span className="processing-time">({results.processing_time}s)</span>
                  </div>
                </div>
                <SearchResults results={results} />
              </div>
              
              <div className="insights-section">
                <div className="section-header">
                  <h3 className="section-title">💡 Actionable Insights</h3>
                  {generatingReport && (
                    <div className="generating-indicator">
                      <Loader2 className="loading-icon" size={16} />
                      <span>Generating insights...</span>
                    </div>
                  )}
                </div>
                
                {report && (
                  <div className="insights-content">
                    <div className="insights-sections">
                      <div className="insight-section-item key-insights">
                        <h4 className="insight-section-title">🎯 Key Insights</h4>
                        <div className="insights-grid">
                          {report.key_insights.map((insight, index) => (
                            <div key={index} className="insight-card" style={{animationDelay: `${index * 0.1}s`}}>
                              <div className="insight-header">
                                <span className="insight-category">{insight.category}</span>
                              </div>
                              <p className="insight-text">{insight.insight}</p>
                              <div className="insight-details">
                                <div className="insight-actions">
                                  <h6>✅ Action Items:</h6>
                                  <ul>
                                    {insight.action_items.map((action, idx) => (
                                      <li key={idx}>{action}</li>
                                    ))}
                                  </ul>
                                </div>
                                <div className="insight-legal">
                                  <h6>⚖️ Legal Considerations:</h6>
                                  <ul>
                                    {insight.legal_considerations.map((consideration, idx) => (
                                      <li key={idx}>{consideration}</li>
                                    ))}
                                  </ul>
                                </div>
                              </div>
                            </div>
                          ))}
                        </div>
                      </div>

                      <div className="insight-section-item procedures">
                        <h4 className="insight-section-title">📋 Procedural Recommendations</h4>
                        <ul className="insight-list">
                          {report.procedural_recommendations.map((rec, index) => (
                            <li key={index} className="insight-list-item" style={{animationDelay: `${index * 0.05}s`}}>{rec}</li>
                          ))}
                        </ul>
                      </div>

                      <div className="insight-section-item warnings">
                        <h4 className="insight-section-title">⚠️ Legal Warnings</h4>
                        <ul className="insight-list warning-list">
                          {report.legal_warnings.map((warning, index) => (
                            <li key={index} className="insight-list-item warning-item" style={{animationDelay: `${index * 0.05}s`}}>{warning}</li>
                          ))}
                        </ul>
                      </div>

                      <div className="insight-section-item jurisdiction-notes">
                        <h4 className="insight-section-title">
                          <MapPin size={18} />
                          Jurisdiction-Specific Notes
                        </h4>
                        <ul className="insight-list">
                          {report.jurisdiction_specific_notes.map((note, index) => (
                            <li key={index} className="insight-list-item" style={{animationDelay: `${index * 0.05}s`}}>{note}</li>
                          ))}
                        </ul>
                      </div>
                    </div>
                  </div>
                )}
                
                {!report && !generatingReport && (
                  <div className="insights-placeholder">
                    <div className="placeholder-icon">💡</div>
                    <p>Actionable insights will appear here after search results are loaded.</p>
                  </div>
                )}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default SearchInterface;
