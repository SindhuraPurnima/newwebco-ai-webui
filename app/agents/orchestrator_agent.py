from typing import Dict, List, Any, Optional
from .base_agent import BaseAgent

class OrchestratorAgent(BaseAgent):
    """
    The Orchestrator Agent coordinates between different specialized agents
    and manages the flow of information between them.
    """
    
    def __init__(self, web_agent, clinical_agent, food_security_agent):
        self.web_agent = web_agent
        self.clinical_agent = clinical_agent
        self.food_security_agent = food_security_agent
        
    def process_query(self, query: str, agent_type: str, context: Optional[Dict[str, Any]] = None, conversation_history: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        """
        Route the query to the appropriate specialized agent and return its response
        
        Args:
            query: The user's query text
            agent_type: The type of agent to use (web, clinical, food_security)
            context: Optional context information
            conversation_history: Optional conversation history for context
            
        Returns:
            Dictionary containing the specialized agent's response
        """
        try:
            # Route to the appropriate agent based on the agent_type
            if agent_type == "clinical":
                return self.clinical_agent.process_query(query, context=context)
            elif agent_type == "food_security":
                return self.food_security_agent.process_query(query, context=context)
            else:
                # Default to web agent for general queries or unknown agent types
                return self.web_agent.process_query(query, context=context)
                
        except Exception as e:
            # Handle any errors in agent processing
            return {
                "response": f"The orchestrator encountered an error: {str(e)}",
                "sources": [],
                "additional_info": {
                    "error": str(e),
                    "agent_type": agent_type
                }
            } 