import React from 'react';
import './SourcesDisplay.css';

const SourcesDisplay = ({ sources }) => {
  return (
    <div className="sources-display">
      <h3>Sources</h3>
      <ul className="sources-list">
        {sources.map((source, index) => (
          <li key={index} className="source-item">
            <div className="source-title">{source.title}</div>
            {source.page && <div className="source-page">Page: {source.page}</div>}
            {source.relevance && (
              <div className="source-relevance">
                Relevance: {Math.round(source.relevance * 100)}%
              </div>
            )}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default SourcesDisplay; 