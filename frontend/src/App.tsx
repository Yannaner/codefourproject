import React from 'react';
import Header from './components/Header';
import SearchInterface from './components/SearchInterface';
import './App.css';

function App() {
  return (
    <div className="app">
      <Header />
      <main className="main-content">
        <SearchInterface />
      </main>
    </div>
  );
}

export default App;
