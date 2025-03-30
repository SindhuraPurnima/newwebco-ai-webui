import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './App.css';

// We'll create these components
const Header = () => (
  <header className="app-header">
    <h1>NewWebCo AI Assistant</h1>
  </header>
);

const QueryInterface = () => {
  const [query, setQuery] = useState('');
  const [response, setResponse] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [conversationId] = useState(`conv_${Date.now()}_${Math.random().toString(36).substring(2, 9)}`);
  const [agentUsed, setAgentUsed] = useState(null);

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

//   const handleSubmit = async () => {
//     if (!query.trim()) return;

//     setIsLoading(true);
//     setError(null);

//     try {
//       // In a real implementation, this would call your API
//       // Simulating API response for now
//       setTimeout(() => {
//         const agentTypes = ['web', 'clinical', 'food_security'];
//         const selectedAgent = agentTypes[Math.floor(Math.random() * agentTypes.length)];
        
//         const result = {
//           response: `This is a simulated response to: "${query}"`,
//           sources: [
//             { title: "Sample Source", page: 42, relevance: 0.89 }
//           ],
//           agent_used: selectedAgent
//         };
        
//         setResponse(result);
//         setAgentUsed(result.agent_used);
//         setIsLoading(false);
//       }, 1000);
//     } catch (err) {
//       setError('Failed to get response from the agent. Please try again.');
//       console.error(err);
//       setIsLoading(false);
//     }
//   };


  return (
    <div className="query-interface">
      <h2>Ask me anything</h2>
      
      <div className="query-container">
        <textarea
          className="query-input"
          value={query}
          onChange={handleQueryChange}
          placeholder="Enter your query here..."
          disabled={isLoading}
        />
        <button 
          className="submit-button" 
          onClick={handleSubmit} 
          disabled={isLoading || !query.trim()}
        >
          {isLoading ? 'Processing...' : 'Submit'}
        </button>
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
                 'Food Security Agent'}
              </span>
            </div>
          )}
          
          <div className="response-display">
            <h3>Response</h3>
            <div className="response-content">
              {response.response}
            </div>
          </div>
          
          {response.sources && response.sources.length > 0 && (
            <div className="sources-display">
              <h3>Sources</h3>
              <ul className="sources-list">
                {response.sources.map((source, index) => (
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
          )}
        </div>
      )}
    </div>
  );
};

function App() {
  return (
    <Router>
      <div className="app">
        <Header />
        <div className="main-container">
          <div className="content">
            <Routes>
              <Route path="/" element={<QueryInterface />} />
            </Routes>
          </div>
        </div>
      </div>
    </Router>
  );
}

export default App; 