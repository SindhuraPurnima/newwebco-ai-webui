from typing import Dict, List, Any, Optional
from .base_agent import BaseAgent

class ChatAgent(BaseAgent):
    """
    The Chat Agent is the first point of contact for user queries.
    It manages the conversation flow and delegates to other agents.
    """
    
    def __init__(self, classification_agent, orchestrator):
        self.classification_agent = classification_agent
        self.orchestrator = orchestrator
        # Initialize conversation memory
        self.conversations = {}
        
    def process_query(self, query: str, context: Optional[Dict[str, Any]] = None, conversation_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Process a user query, maintain conversation context, and delegate to appropriate agents
        
        Args:
            query: The user's query text
            context: Optional context information
            conversation_id: Optional ID to maintain conversation state
            
        Returns:
            Dictionary containing response and any additional information
        """
        # Create or retrieve conversation context
        if conversation_id not in self.conversations:
            self.conversations[conversation_id] = []
            
        # Add the current query to conversation history
        self.conversations[conversation_id].append({"role": "user", "content": query})
        
        try:
            # First, classify the query to determine which agent should handle it
            classification_result = self.classification_agent.process_query(
                query, 
                context=context, 
                conversation_history=self.conversations.get(conversation_id, [])
            )
            
            # Get the classified agent type
            agent_type = classification_result.get("agent_type", "web")
            
            # Use the orchestrator to get a response from the appropriate agent
            response = self.orchestrator.process_query(
                query, 
                agent_type=agent_type,
                context=context, 
                conversation_history=self.conversations.get(conversation_id, [])
            )
            
            # Add the response to conversation history
            self.conversations[conversation_id].append({"role": "assistant", "content": response["response"]})
            
            # Include the agent type in the response
            response["agent_used"] = agent_type
            
            return response
            
        except Exception as e:
            error_response = {
                "response": f"I encountered an error processing your query: {str(e)}",
                "sources": [],
                "additional_info": {"error": str(e)},
                "agent_used": "chat"
            }
            
            self.conversations[conversation_id].append({"role": "assistant", "content": error_response["response"]})
            return error_response 