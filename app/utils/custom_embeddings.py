import torch
from transformers import AutoTokenizer, AutoModel
import numpy as np

class E5EmbeddingModel:
    """Embedding model using the E5 transformer model"""
    
    def __init__(self):
        """Initialize the E5 embedding model"""
        try:
            # Load E5 model and tokenizer
            self.model_name = "intfloat/e5-large-v2"
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModel.from_pretrained(self.model_name)
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
            self.model.to(self.device)
            print(f"Loaded E5 embedding model: {self.model_name} on {self.device}")
        except Exception as e:
            print(f"Error loading E5 embedding model: {e}")
            raise
    
    def get_embeddings(self, texts):
        """
        Generate embeddings for a list of texts
        
        Args:
            texts: String or list of strings to generate embeddings for
            
        Returns:
            List of embeddings (numpy arrays)
        """
        # Handle single string input
        if isinstance(texts, str):
            texts = [texts]
            
        # E5 models expect "query: " or "passage: " prefix for better performance
        processed_texts = [f"passage: {text}" for text in texts]
        
        # Process in batches to handle memory constraints
        batch_size = 8
        all_embeddings = []
        
        for i in range(0, len(processed_texts), batch_size):
            batch_texts = processed_texts[i:i+batch_size]
            
            # Tokenize and generate embeddings
            inputs = self.tokenizer(batch_texts, padding=True, truncation=True, 
                                   return_tensors="pt", max_length=512)
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            # Generate embeddings
            with torch.no_grad():
                outputs = self.model(**inputs)
                
            # Use mean pooling to get document embeddings
            attention_mask = inputs['attention_mask']
            embeddings = self._mean_pooling(outputs.last_hidden_state, attention_mask)
            
            # Normalize embeddings
            embeddings = torch.nn.functional.normalize(embeddings, p=2, dim=1)
            
            # Convert to numpy and add to results
            embeddings_np = embeddings.cpu().numpy()
            all_embeddings.extend(embeddings_np)
            
        return all_embeddings

    def get_query_embedding(self, query):
        """Generate embedding specifically for a query with proper prefixing"""
        # E5 models expect "query: " prefix for queries
        prefixed_query = f"query: {query}"
        
        # Tokenize
        inputs = self.tokenizer(prefixed_query, padding=True, truncation=True, 
                               return_tensors="pt", max_length=512)
        inputs = {k: v.to(self.device) for k, v in inputs.items()}
        
        # Generate embeddings
        with torch.no_grad():
            outputs = self.model(**inputs)
            
        # Mean pooling
        attention_mask = inputs['attention_mask']
        embeddings = self._mean_pooling(outputs.last_hidden_state, attention_mask)
        
        # Normalize
        embeddings = torch.nn.functional.normalize(embeddings, p=2, dim=1)
        
        return embeddings.cpu().numpy()[0]  # Return as numpy array
    
    def _mean_pooling(self, token_embeddings, attention_mask):
        """Mean pooling operation to get sentence embeddings"""
        input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
        return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)
