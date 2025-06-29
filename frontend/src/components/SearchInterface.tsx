import React, { useState, useEffect, useRef, useCallback } from 'react';
import { Search, Loader2, FileText, MapPin, Sparkles, ArrowRight } from 'lucide-react';
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
  const [suggestions, setSuggestions] = useState<string[]>([]);
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [selectedSuggestionIndex, setSelectedSuggestionIndex] = useState(-1);
  const [isTyping, setIsTyping] = useState(false);
  const [animationPhase, setAnimationPhase] = useState(0);
  const inputRef = useRef<HTMLInputElement>(null);
  const suggestionsRef = useRef<HTMLDivElement>(null);

  // Legal search suggestions database
  const searchSuggestions = [
    "search vehicle without consent",
    "search warrant requirements",
    "search incident to arrest",
    "search and seizure",
    "search plain view doctrine",
    "Terry stop requirements",
    "Terry frisk limitations",
    "traffic stop duration",
    "traffic stop passenger rights",
    "traffic stop vehicle search",
    "consent search",
    "consent withdrawal",
    "Fourth Amendment",
    "Fourth Amendment violations",
    "probable cause",
    "probable cause vehicle",
    "reasonable suspicion",
    "reasonable suspicion standards",
    "Miranda rights",
    "Miranda warnings timing",
    "arrest warrant",
    "arrest without warrant",
    "drug dog searches",
    "drug dog sniff",
    "vehicle inventory search",
    "vehicle passenger compartment",
    "weapon search",
    "weapon frisk",
    "plain view seizure",
    "plain smell doctrine",
    "hot pursuit",
    "hot pursuit doctrine",
    "exigent circumstances",
    "exigent circumstances search",
    "stop and frisk",
    "stop and identify",
    "constitutional rights",
    "constitutional violations",
    "evidence suppression",
    "evidence exclusion",
    "illegal search",
    "illegal seizure",
    "warrantless search",
    "warrantless arrest"
  ];

  // Add typing animation effect
  useEffect(() => {
    const interval = setInterval(() => {
      setAnimationPhase(prev => (prev + 1) % 4);
    }, 2000);
    return () => clearInterval(interval);
  }, []);

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

  const generateSuggestions = useCallback((input: string) => {
    if (!input.trim() || input.length < 2) {
      setSuggestions([]);
      return;
    }

    const inputLower = input.toLowerCase();
    const words = inputLower.split(' ');
    const lastWord = words[words.length - 1];
    
    // Find suggestions that match the current input
    const matchingSuggestions = searchSuggestions
      .filter(suggestion => {
        const suggestionLower = suggestion.toLowerCase();
        // Match if suggestion starts with input or contains all words
        return suggestionLower.includes(inputLower) || 
               words.every(word => word.length > 1 && suggestionLower.includes(word));
      })
      .slice(0, 6) // Limit to 6 suggestions
      .sort((a, b) => {
        const aLower = a.toLowerCase();
        const bLower = b.toLowerCase();
        // Prioritize exact starts
        if (aLower.startsWith(inputLower) && !bLower.startsWith(inputLower)) return -1;
        if (!aLower.startsWith(inputLower) && bLower.startsWith(inputLower)) return 1;
        return a.length - b.length; // Shorter suggestions first
      });

    setSuggestions(matchingSuggestions);
  }, []);

  const debouncedGenerateSuggestions = useCallback(
    debounce((input: string) => generateSuggestions(input), 200),
    [generateSuggestions]
  );

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setQuery(value);
    setSelectedSuggestionIndex(-1);
    setIsTyping(true);
    
    // Clear typing indicator after delay
    setTimeout(() => setIsTyping(false), 1000);
    
    if (value.trim()) {
      debouncedGenerateSuggestions(value);
      setShowSuggestions(true);
    } else {
      setSuggestions([]);
      setShowSuggestions(false);
    }
  };

  const handleInputFocus = () => {
    if (query.trim() && suggestions.length > 0) {
      setShowSuggestions(true);
    }
  };

  const handleInputBlur = () => {
    // Delay hiding suggestions to allow clicking
    setTimeout(() => setShowSuggestions(false), 150);
  };

  const handleSuggestionClick = (suggestion: string) => {
    setQuery(suggestion);
    setShowSuggestions(false);
    setSuggestions([]);
    inputRef.current?.focus();
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (!showSuggestions || suggestions.length === 0) return;

    switch (e.key) {
      case 'ArrowDown':
        e.preventDefault();
        setSelectedSuggestionIndex(prev => 
          prev < suggestions.length - 1 ? prev + 1 : 0
        );
        break;
      case 'ArrowUp':
        e.preventDefault();
        setSelectedSuggestionIndex(prev => 
          prev > 0 ? prev - 1 : suggestions.length - 1
        );
        break;
      case 'Enter':
        if (selectedSuggestionIndex >= 0) {
          e.preventDefault();
          handleSuggestionClick(suggestions[selectedSuggestionIndex]);
        }
        break;
      case 'Escape':
        setShowSuggestions(false);
        setSelectedSuggestionIndex(-1);
        break;
    }
  };

  return (
    <div className="search-interface">
      {/* Animated Background */}
      <div className="search-background">
        <div className="bg-gradient"></div>
        <div className="bg-grid"></div>
        <div className="bg-orbs">
          <div className="orb orb-1"></div>
          <div className="orb orb-2"></div>
          <div className="orb orb-3"></div>
        </div>
      </div>

      <div className="search-container">
        {/* Hero Section */}
        <div className="search-hero">
          <div className="hero-content">
            <div className="hero-icon-container">
              <Sparkles className="hero-icon" size={32} />
            </div>
            <h1 className="hero-title">
              <span className="title-gradient">Search Case Law</span>
            </h1>
            <p className="hero-description">
              Ask questions in plain English about legal procedures, constitutional rights,
              <br />and case law precedents powered by AI.
            </p>
          </div>
        </div>

        {/* Search Form */}
        <div className="search-form-container">
          <form onSubmit={handleSearch} className="search-form-modern">
            {/* Jurisdiction Selector */}
            <div className="form-section">
              <div className="jurisdiction-wrapper">
                <MapPin className="jurisdiction-icon" size={18} />
                <select 
                  value={jurisdiction} 
                  onChange={(e) => setJurisdiction(e.target.value)}
                  className="jurisdiction-select-modern"
                  disabled={loading}
                >
                  {jurisdictions.map((j) => (
                    <option key={j.value} value={j.value}>
                      {j.label}
                    </option>
                  ))}
                </select>
              </div>
            </div>

            {/* Main Search Input */}
            <div className="search-input-section">
              <div className="search-input-wrapper">
                <div className="input-container">
                  <Search className={`search-icon-modern ${isTyping ? 'typing' : ''}`} size={20} />
                  <input
                    ref={inputRef}
                    type="text"
                    value={query}
                    onChange={handleInputChange}
                    onFocus={handleInputFocus}
                    onBlur={handleInputBlur}
                    onKeyDown={handleKeyDown}
                    placeholder={`Start typing... e.g., ${searchSuggestions[animationPhase % searchSuggestions.length]}`}
                    className="search-input-modern"
                    disabled={loading}
                    autoComplete="off"
                  />
                  
                  {/* Star Border Button */}
                  <button 
                    type="submit" 
                    className={`search-button-star ${loading ? 'loading' : ''} ${!query.trim() ? 'disabled' : ''}`}
                    disabled={loading || !query.trim()}
                  >
                    <div className="button-stars">
                      <div className="star star-1">✦</div>
                      <div className="star star-2">✦</div>
                      <div className="star star-3">✦</div>
                      <div className="star star-4">✦</div>
                    </div>
                    <div className="button-content">
                      {loading ? (
                        <Loader2 className="loading-icon-modern" size={18} />
                      ) : (
                        <>
                          <span>Search</span>
                          <ArrowRight size={16} className="arrow-icon" />
                        </>
                      )}
                    </div>
                  </button>
                </div>
                
                {/* Enhanced Suggestions */}
                {showSuggestions && suggestions.length > 0 && (
                  <div ref={suggestionsRef} className="search-suggestions-modern">
                    <div className="suggestions-header">
                      <Sparkles size={14} />
                      <span>Popular searches</span>
                    </div>
                    {suggestions.map((suggestion, index) => (
                      <div
                        key={suggestion}
                        className={`suggestion-item-modern ${index === selectedSuggestionIndex ? 'selected' : ''}`}
                        onClick={() => handleSuggestionClick(suggestion)}
                        style={{ animationDelay: `${index * 50}ms` }}
                      >
                        <Search size={14} className="suggestion-icon-modern" />
                        <span className="suggestion-text-modern">{suggestion}</span>
                        <ArrowRight size={12} className="suggestion-arrow" />
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          </form>

          {/* Quick Actions */}
          <div className="quick-actions">
            <div className="quick-action-item" onClick={() => setQuery("search vehicle without consent")}>
              <span>🚗</span>
              <span>Vehicle Searches</span>
            </div>
            <div className="quick-action-item" onClick={() => setQuery("Fourth Amendment violations")}>
              <span>⚖️</span>
              <span>Constitutional Rights</span>
            </div>
            <div className="quick-action-item" onClick={() => setQuery("Miranda rights")}>
              <span>🗣️</span>
              <span>Miranda Rights</span>
            </div>
            <div className="quick-action-item" onClick={() => setQuery("probable cause")}>
              <span>🔍</span>
              <span>Probable Cause</span>
            </div>
          </div>
        </div>

        {/* Error Message */}
        {error && (
          <div className="error-message-modern">
            <div className="error-content">
              <div className="error-icon">⚠️</div>
              <div>
                <h4>Something went wrong</h4>
                <p>{error}</p>
              </div>
            </div>
          </div>
        )}

        {/* Results Section - Only show when there are results */}
        {results && (
          <div className="results-container-modern">
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

// Debounce utility function
function debounce<T extends (...args: any[]) => any>(
  func: T,
  wait: number
): (...args: Parameters<T>) => void {
  let timeout: NodeJS.Timeout;
  return (...args: Parameters<T>) => {
    clearTimeout(timeout);
    timeout = setTimeout(() => func(...args), wait);
  };
}

export default SearchInterface;
