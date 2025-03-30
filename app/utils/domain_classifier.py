from .custom_embeddings import E5EmbeddingModel
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

class DomainClassifier:
    """Classify queries into domains using E5 embeddings"""
    
    def __init__(self):
        """Initialize with domain descriptions"""
        self.embedding_model = E5EmbeddingModel()
        
        # Domain descriptions
        self.domains = {
            "clinical": "Medical topics, healthcare, diseases, symptoms, treatment, diagnosis, medication, patients, doctors, hospitals, clinical trials, medical research, medical technology, health conditions",
            
            "food_security": "Agriculture, farming, crops, livestock, irrigation, food production, hunger, malnutrition, sustainable agriculture, food systems, agricultural policy, food distribution, food supply chains",
            
            "general": "General knowledge, technology, science, history, culture, education, business, entertainment, sports, politics, news, information, arts, artificial intelligence, computers, internet"
        }
        
        # Pre-compute domain embeddings
        self.domain_embeddings = {}
        for domain, description in self.domains.items():
            # Use passage embedding for domains
            self.domain_embeddings[domain] = self.embedding_model.get_embeddings(description)[0]
    
    def classify_query(self, query):
        """Classify a query into a domain"""
        # Extract query terms for keyword matching
        query_lower = query.lower()
        
        # Check for explicit keywords
        clinical_keywords = ["medical", "disease", "symptom", "diagnosis", "doctor", "patient", "treatment"]
        food_keywords = ["food", "agriculture", "farm", "crop", "harvest", "nutrition", "hunger"]
        tech_keywords = ["ai", "artificial intelligence", "computer", "technology", "digital", "internet", "robot"]
        
        # Count keyword matches
        clinical_count = sum(keyword in query_lower for keyword in clinical_keywords)
        food_count = sum(keyword in query_lower for keyword in food_keywords)
        tech_count = sum(keyword in query_lower for keyword in tech_keywords)
        
        # Apply strong keyword override for technology questions to ensure they go to general
        if tech_count > 0 and tech_count >= clinical_count and tech_count >= food_count:
            return {"domain": "general", "confidence": 0.95}
        
        # Get query embedding - use the specialized query embedding method
        query_embedding = self.embedding_model.get_query_embedding(query)
        
        # Calculate similarity to each domain
        similarities = {}
        for domain, embedding in self.domain_embeddings.items():
            similarities[domain] = self.calculate_similarity(query_embedding, embedding)
        
        # Select domain with highest similarity
        best_domain = max(similarities.items(), key=lambda x: x[1])
        
        return {
            "domain": best_domain[0],
            "confidence": best_domain[1]
        }
    
    def calculate_similarity(self, embedding1, embedding2):
        """Calculate cosine similarity between embeddings"""
        return float(cosine_similarity(
            embedding1.reshape(1, -1), 
            np.array(embedding2).reshape(1, -1)
        )[0][0])
