import React from 'react';
import { Scale } from 'lucide-react';
import './Header.css';

const Header: React.FC = () => {
  return (
    <header className="header">
      <div className="header-container">
        <div className="header-brand">
          <Scale className="header-icon" size={32} />
          <div className="header-text">
            <h1 className="header-title">Case Law AI Assistant</h1>
            <p className="header-subtitle">Intelligent Legal Research for Law Enforcement</p>
          </div>
        </div>
        <div className="header-info">
          <span className="header-badge">Beta</span>
        </div>
      </div>
    </header>
  );
};

export default Header;
