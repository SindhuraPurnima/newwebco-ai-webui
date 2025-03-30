from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional

class BaseAgent(ABC):
    """Base class for all AI agents"""
    
    @abstractmethod
    def process_query(self, query: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Process a user query and return a response
        
        Args:
            query: The user's query text
            context: Optional context information
            
        Returns:
            Dictionary containing response and any additional information
        """
        pass 