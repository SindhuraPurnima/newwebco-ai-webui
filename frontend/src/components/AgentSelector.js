import React from 'react';
import './AgentSelector.css';

const AgentSelector = ({ selectedAgent, onAgentChange }) => {
  return (
    <div className="agent-selector">
      <h3>Select AI Agent</h3>
      <div className="agent-options">
        <div
          className={`agent-option ${selectedAgent === 'general' ? 'selected' : ''}`}
          onClick={() => onAgentChange('general')}
        >
          <div className="agent-icon general-icon">🤖</div>
          <div className="agent-info">
            <h4>General Agent</h4>
            <p>For general inquiries and tasks</p>
          </div>
        </div>
        
        <div
          className={`agent-option ${selectedAgent === 'clinical' ? 'selected' : ''}`}
          onClick={() => onAgentChange('clinical')}
        >
          <div className="agent-icon clinical-icon">🩺</div>
          <div className="agent-info">
            <h4>Clinical RAG Agent</h4>
            <p>For clinical and healthcare inquiries</p>
          </div>
        </div>
        
        <div
          className={`agent-option ${selectedAgent === 'food_security' ? 'selected' : ''}`}
          onClick={() => onAgentChange('food_security')}
        >
          <div className="agent-icon food-icon">🌾</div>
          <div className="agent-info">
            <h4>Food Security Agent</h4>
            <p>For food security and agriculture inquiries</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AgentSelector; 