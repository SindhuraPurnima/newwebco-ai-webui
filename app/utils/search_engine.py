import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

class SearchEngine:
    """Improved search for relevant documents based on query embeddings"""
    
    def __init__(self, document_collections=None):
        """
        Initialize with document collections
        document_collections: Dict[str, List[Document]] mapping domain names to document lists
        """
        self.document_collections = document_collections or {}
        self.embedding_model = None
    
    def set_embedding_model(self, embedding_model):
        """Set the embedding model to use for queries"""
        self.embedding_model = embedding_model
    
    def search(self, query, domain=None, top_k=5):
        """
        Search for relevant documents
        
        Args:
            query: The search query
            domain: Specific domain to search (e.g., 'clinical', 'food_security')
            top_k: Number of results to return
            
        Returns:
            List of relevant documents with similarity scores
        """
        if not self.embedding_model:
            raise ValueError("Embedding model must be set before searching")
            
        # Get query embedding - use the specialized query embedding method
        query_embedding = self.embedding_model.get_query_embedding(query)
        
        # Extract key terms for keyword boosting
        key_terms = self._extract_key_terms(query)
        
        results = []
        
        # Determine which collections to search
        collections_to_search = {}
        if domain and domain in self.document_collections:
            collections_to_search[domain] = self.document_collections[domain]
        else:
            collections_to_search = self.document_collections
        
        # Search each collection
        for domain_name, docs in collections_to_search.items():
            domain_results = []
            
            for doc in docs:
                # Base semantic similarity score (cosine)
                if "embedding" in doc:
                    embedding_similarity = self._calculate_similarity(query_embedding, doc["embedding"])
                    
                    # Additional keyword-based boosting
                    keyword_boost = self._calculate_keyword_boost(doc["content"], key_terms)
                    
                    # Combined score with both semantic and keyword components
                    combined_score = (0.7 * embedding_similarity) + (0.3 * keyword_boost)
                    
                    # Only include docs with reasonable similarity
                    if combined_score > 0.2:  # Minimum threshold
                        domain_results.append({
                            "content": doc["content"],
                            "metadata": doc.get("metadata", {}),
                            "score": float(combined_score),
                            "domain": domain_name
                        })
            
            results.extend(domain_results)
        
        # Sort by score and take top-k
        results = sorted(results, key=lambda x: x["score"], reverse=True)[:top_k]
        
        # If no results found, try cross-domain search
        if not results and domain:
            print(f"No results in {domain} domain, searching all domains")
            return self.search(query, domain=None, top_k=top_k)
            
        # If still no results, add placeholder
        if not results:
            print(f"No relevant documents found for query: {query}")
            return [{
                "content": "No relevant information found.",
                "score": 0.0,
                "metadata": {"source": "system"},
                "domain": "unknown"
            }]
        
        return results
    
    def _calculate_similarity(self, query_embedding, doc_embedding):
        """Calculate cosine similarity between query and document"""
        query_embedding = query_embedding.reshape(1, -1)
        doc_embedding = np.array(doc_embedding).reshape(1, -1)
        return float(cosine_similarity(query_embedding, doc_embedding)[0][0])
    
    def _extract_key_terms(self, query):
        """Extract important terms from the query"""
        # Basic approach: remove stop words and get unique terms
        stop_words = {'the', 'is', 'and', 'of', 'to', 'a', 'in', 'that', 'for'}
        terms = [word.lower() for word in query.split() if word.lower() not in stop_words]
        return set(terms)
    
    def _calculate_keyword_boost(self, content, key_terms):
        """Calculate keyword-based relevance boost"""
        if not content or not key_terms:
            return 0.0
            
        content_lower = content.lower()
        term_count = sum(1 for term in key_terms if term in content_lower)
        
        # Normalize by total key terms
        if len(key_terms) > 0:
            return term_count / len(key_terms)
        return 0.0
