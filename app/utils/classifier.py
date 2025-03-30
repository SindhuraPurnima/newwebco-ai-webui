# app/utils/classifier.py
from langchain.embeddings import HuggingFaceEmbeddings
import numpy as np

class QueryClassifier:
    def __init__(self):
        # Use HuggingFace embeddings
        self.embedding_model = HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2"
        )
        
        # Domain descriptions for classification
        self.domains = {
            "clinical": "medical health clinical patient disease treatment doctor hospital symptoms diagnosis therapy healthcare medicine",
            "food_security": "food agriculture farming crop nutrition hunger sustainable production harvest farming agricultural security",
            "general": "information technology company business product service general help guide explain question"
        }
        
        # Pre-compute embeddings for domains
        self.domain_embeddings = {}
        for domain, desc in self.domains.items():
            self.domain_embeddings[domain] = self.embedding_model.embed_query(desc)
    
    def classify_query(self, query):
        """
        Classify a query into one of the predefined domains
        
        Args:
            query: User query string
            
        Returns:
            Dictionary with domain classification and confidence
        """
        # Get embedding for query
        query_embedding = self.embedding_model.embed_query(query)
        
        # Calculate cosine similarity with each domain
        similarities = {}
        for domain, domain_emb in self.domain_embeddings.items():
            similarity = self._cosine_similarity(query_embedding, domain_emb)
            similarities[domain] = similarity
        
        # Get the domain with highest similarity
        best_domain = max(similarities, key=similarities.get)
        confidence = similarities[best_domain]
        
        return {
            "domain": best_domain,
            "confidence": confidence,
            "all_scores": similarities
        }
    
    def _cosine_similarity(self, emb1, emb2):
        """Calculate cosine similarity between two embeddings"""
        dot_product = np.dot(emb1, emb2)
        norm1 = np.linalg.norm(emb1)
        norm2 = np.linalg.norm(emb2)
        return dot_product / (norm1 * norm2)