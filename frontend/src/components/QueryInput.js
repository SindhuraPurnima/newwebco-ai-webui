import React from 'react';
import './QueryInput.css';

const QueryInput = ({ value, onChange, onSubmit, isLoading }) => {
  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      onSubmit();
    }
  };

  return (
    <div className="query-input-container">
      <textarea
        className="query-input"
        value={value}
        onChange={onChange}
        onKeyDown={handleKeyDown}
        placeholder="Enter your query here..."
        disabled={isLoading}
      />
      <button 
        className="submit-button" 
        onClick={onSubmit} 
        disabled={isLoading || !value.trim()}
      >
        {isLoading ? 'Processing...' : 'Submit'}
      </button>
    </div>
  );
};

export default QueryInput; 