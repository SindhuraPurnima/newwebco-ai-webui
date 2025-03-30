# app/utils/ir_search.py
from langchain.vectorstores import FAISS
from typing import List, Dict, Any

class IRSearchEngine:
    def __init__(self, vector_stores):
        """
        Initialize with multiple vector stores
        vector_stores: Dict[str, FAISS] mapping names to vector stores
        """
        self.vector_stores = vector_stores
    
    def search(self, query, domain=None, top_k=5):
        """
        Search for relevant documents
        
        Args:
            query: The search query
            domain: Specific domain to search (e.g., 'clinical', 'food_security')
            top_k: Number of results to return
            
        Returns:
            List of relevant documents with metadata
        """
        results = []
        
        # If domain is specified, only search in that domain
        if domain:
            if domain in self.vector_stores:
                docs = self.vector_stores[domain].similarity_search_with_score(query, k=top_k)
                for doc, score in docs:
                    results.append({
                        "content": doc.page_content,
                        "metadata": doc.metadata,
                        "score": score,
                        "domain": domain
                    })
        else:
            # Search across all domains
            for domain_name, vector_store in self.vector_stores.items():
                docs = vector_store.similarity_search_with_score(query, k=top_k//len(self.vector_stores) + 1)
                for doc, score in docs:
                    results.append({
                        "content": doc.page_content,
                        "metadata": doc.metadata,
                        "score": score,
                        "domain": domain_name
                    })
        
        # Sort by relevance score
        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:top_k]