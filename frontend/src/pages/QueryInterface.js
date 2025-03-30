import React, { useState, useEffect } from 'react';
import QueryInput from '../components/QueryInput';
import ResponseDisplay from '../components/ResponseDisplay';
import SourcesDisplay from '../components/SourcesDisplay';
import './QueryInterface.css';

const QueryInterface = () => {
  const [query, setQuery] = useState('');
  const [response, setResponse] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [conversationId, setConversationId] = useState(null);
  const [agentUsed, setAgentUsed] = useState(null);

  // Generate a unique conversation ID when the component mounts
  useEffect(() => {
    setConversationId(`conv_${Date.now()}_${Math.random().toString(36).substring(2, 9)}`);
  }, []);

  const handleQueryChange = (e) => {
    setQuery(e.target.value);
  };

  const handleSubmit = async () => {
    if (!query.trim()) return;
  
    setIsLoading(true);
    setError(null);
  
    try {
      const apiUrl = 'http://localhost:8000/query';
      
      const response = await fetch(apiUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query: query,
          context: {},
          conversation_id: conversationId
        }),
      });
  
      if (!response.ok) {
        throw new Error(`API error: ${response.status}`);
      }
  
      const result = await response.json();
      
      setResponse({
        response: result.response,
        sources: result.sources,
        agent_used: result.domain // Map domain to agent_used
      });
      setAgentUsed(result.domain);
      
    } catch (err) {
      setError('Failed to get response from the agent. Please try again.');
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  const sendQuery = async (queryText) => {
    // In a real application, this would call your API
    const apiUrl = 'http://localhost:8000/query';
    
    try {
      const response = await fetch(apiUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query: queryText,
          context: {},
          conversation_id: conversationId
        }),
      });

      if (!response.ok) {
        throw new Error(`API error: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error querying agent:', error);
      throw error;
    }
  };

  return (
    <div className="query-interface">
      <h1>WebUI Copilot</h1>
      
      <div className="query-container">
        <QueryInput 
          value={query} 
          onChange={handleQueryChange} 
          onSubmit={handleSubmit} 
          isLoading={isLoading}
        />
      </div>
      
      {error && <div className="error-message">{error}</div>}
      
      {response && (
        <div className="response-container">
          {agentUsed && (
            <div className="agent-indicator">
              <span className="agent-label">Handling Agent:</span>
              <span className={`agent-name ${agentUsed}`}>
                {agentUsed === 'web' ? 'Web Agent' : 
                 agentUsed === 'clinical' ? 'Clinical Agent' : 
                 agentUsed === 'food_security' ? 'Food Security Agent' : 'Chat Agent'}
              </span>
            </div>
          )}
          
          <ResponseDisplay response={response.response} />
          
          {response.sources && response.sources.length > 0 && (
            <SourcesDisplay sources={response.sources} />
          )}
        </div>
      )}
    </div>
  );
};

export default QueryInterface; 