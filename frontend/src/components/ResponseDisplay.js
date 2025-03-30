import React from 'react';
import './ResponseDisplay.css';

const ResponseDisplay = ({ response }) => {
  return (
    <div className="response-display">
      <h3>Response</h3>
      <div className="response-content">
        {response}
      </div>
    </div>
  );
};

export default ResponseDisplay; 