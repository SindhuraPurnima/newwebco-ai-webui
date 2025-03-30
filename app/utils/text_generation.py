from transformers import T5ForConditionalGeneration, T5Tokenizer

class TextGenerator:
    """Generate text responses using a pretrained language model"""
    
    def __init__(self):
        """Initialize with a text generation model"""
        try:
            self.model_name = "google/flan-t5-base"
            self.tokenizer = T5Tokenizer.from_pretrained(self.model_name)
            self.model = T5ForConditionalGeneration.from_pretrained(self.model_name)
            print(f"Loaded text generation model: {self.model_name}")
        except Exception as e:
            print(f"Error loading text generation model: {e}")
            raise
    
    def generate_response(self, query, context_docs, domain="general"):
        """Generate response with proper handling of domain and context"""
        # Format based on available context
        if context_docs and any(doc.get('content') for doc in context_docs):
            # RAG approach - using retrieved documents
            context_text = "\n\n".join([f"Document {i+1}: {doc['content']}" 
                                      for i, doc in enumerate(context_docs[:3]) if doc.get('content')])
            
            input_text = f"Based on this context, answer the question: {query}\n\nContext: {context_text}"
        else:
            # No context documents available
            if domain == "general":
                # For general domain, allow the model to use its knowledge
                input_text = f"Answer this question: {query}"
            else:
                # For specialized domains, we need context documents
                return {
                    "response": "I don't have enough information in my specialized knowledge base to answer this question.",
                    "sources": []
                }
        
        # Generate the response
        try:
            inputs = self.tokenizer(input_text, return_tensors="pt", max_length=512, truncation=True)
            outputs = self.model.generate(
                inputs.input_ids,
                max_length=256,
                do_sample=True,
                temperature=0.7,
                num_return_sequences=1
            )
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            return {
                "response": response,
                "sources": context_docs
            }
        except Exception as e:
            print(f"Error generating response: {e}")
            return {
                "response": f"I encountered an error while generating a response: {str(e)}",
                "sources": []
            }
