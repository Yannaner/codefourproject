import React, { useState } from 'react';
import { ExternalLink, CheckCircle, Calendar, Building2, ChevronDown, ChevronUp, Scale, Gavel } from 'lucide-react';
import type { CaseSummary } from '../types';
import './CaseCard.css';

interface CaseCardProps {
  caseData: CaseSummary;
  rank: number;
}

const CaseCard: React.FC<CaseCardProps> = ({ caseData, rank }) => {
  const [isExpanded, setIsExpanded] = useState(false);
  const relevancePercentage = Math.round(caseData.relevance_score * 20); // Convert to percentage

  const getRelevanceColor = (percentage: number) => {
    if (percentage >= 80) return 'high';
    if (percentage >= 60) return 'medium';
    return 'low';
  };

  const getJurisdictionColor = (jurisdiction: string) => {
    const colors = {
      'federal': 'blue',
      'new_jersey': 'green',
      'pennsylvania': 'purple',
      'new_york': 'orange'
    };
    return colors[jurisdiction as keyof typeof colors] || 'gray';
  };

  return (
    <div className={`case-card ${isExpanded ? 'expanded' : ''}`}>
      <div className="case-header">
        <div className="case-ranking">
          <div className="rank-badge">
            <span className="rank-number">#{rank}</span>
            <div className="rank-label">Result</div>
          </div>
        </div>
        
        <div className="case-relevance">
          <div className="relevance-container">
            <div className={`relevance-bar ${getRelevanceColor(relevancePercentage)}`}>
              <div 
                className="relevance-fill" 
                style={{ width: `${relevancePercentage}%` }}
              ></div>
            </div>
            <span className="relevance-text">{relevancePercentage}% Match</span>
          </div>
        </div>
      </div>

      <div className="case-title-section">
        <h4 className="case-title">
          <Scale size={18} />
          {caseData.case_name}
        </h4>
        <div className="case-citation">{caseData.citation}</div>
        
        <div className="case-meta">
          <div className="meta-item">
            <Calendar size={14} />
            <span>{caseData.year}</span>
          </div>
          <div className="meta-item">
            <Building2 size={14} />
            <span>{caseData.court}</span>
          </div>
          {caseData.jurisdiction && (
            <div className={`jurisdiction-badge ${getJurisdictionColor(caseData.jurisdiction)}`}>
              <span className="jurisdiction-label">
                {caseData.jurisdiction.replace('_', ' ').toUpperCase()}
              </span>
            </div>
          )}
        </div>
      </div>

      <div className="case-summary">
        <div className="summary-content">
          <p>{caseData.summary}</p>
        </div>
      </div>

      <div className={`case-details ${isExpanded ? 'expanded' : ''}`}>
        <div className="details-grid">
          <div className="detail-section">
            <h5 className="section-title">
              <Gavel size={16} />
              Key Facts
            </h5>
            <p className="section-content">{caseData.facts}</p>
          </div>

          <div className="detail-section">
            <h5 className="section-title">Legal Principle</h5>
            <p className="section-content">{caseData.legal_principle}</p>
          </div>

          <div className="detail-section">
            <h5 className="section-title">Court Ruling</h5>
            <p className="section-content">{caseData.ruling}</p>
          </div>

          <div className="detail-section takeaways-section">
            <h5 className="section-title">Officer Takeaways</h5>
            <div className="takeaways-grid">
              {caseData.key_takeaways.map((takeaway, index) => (
                <div key={index} className="takeaway-item">
                  <CheckCircle className="takeaway-icon" size={16} />
                  <span>{takeaway}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      <div className="case-footer">
        <div className="footer-actions">
          <button 
            onClick={() => setIsExpanded(!isExpanded)}
            className="expand-button"
          >
            {isExpanded ? (
              <>
                <ChevronUp size={16} />
                Show Less
              </>
            ) : (
              <>
                <ChevronDown size={16} />
                Show Details
              </>
            )}
          </button>
          
          {caseData.full_text_link && (
            <a 
              href={caseData.full_text_link} 
              target="_blank" 
              rel="noopener noreferrer"
              className="full-text-link"
            >
              <ExternalLink size={16} />
              Full Text
            </a>
          )}
        </div>
      </div>
    </div>
  );
};

export default CaseCard;
