# app/utils/llm_handler.py
from langchain.llms import HuggingFacePipeline
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

class LLMHandler:
    def __init__(self, model_name="TheBloke/Llama-2-7B-Chat-GGML"):
        # For smaller machines, use a lighter model
        # Alternate choices:
        # - "gpt2" (very light but low quality)
        # - "facebook/opt-125m" (very light)
        # - "TheBloke/Phi-2-GGUF" (medium)
        # - "TheBloke/Llama-2-7B-Chat-GGML" (higher quality but needs more RAM)
        
        try:
            # Try to load a larger model if hardware supports it
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForCausalLM.from_pretrained(
                model_name, 
                torch_dtype=torch.float16,
                device_map="auto",
                low_cpu_mem_usage=True
            )
            
            pipe = pipeline(
                "text-generation",
                model=self.model,
                tokenizer=self.tokenizer,
                max_length=512,
                temperature=0.7,
                top_p=0.95,
                repetition_penalty=1.2
            )
            
            self.llm = HuggingFacePipeline(pipeline=pipe)
            
        except (RuntimeError, ValueError, OSError):
            # Fall back to a much smaller model if hardware is limited
            print("Falling back to smaller model due to hardware limitations")
            fallback_model = "distilgpt2"
            self.tokenizer = AutoTokenizer.from_pretrained(fallback_model)
            self.model = AutoModelForCausalLM.from_pretrained(fallback_model)
            
            pipe = pipeline(
                "text-generation",
                model=self.model,
                tokenizer=self.tokenizer,
                max_length=256
            )
            
            self.llm = HuggingFacePipeline(pipeline=pipe)
    
    def generate_response(self, query, context_docs):
        """
        Generate a response based on the query and retrieved documents
        
        Args:
            query: User query
            context_docs: List of retrieved documents
            
        Returns:
            Generated response
        """
        # Extract content from documents
        context = "\n\n".join([doc["content"] for doc in context_docs[:3]])  # Limit to top 3 docs
        
        # Create prompt with context
        prompt_template = """
        You are an AI assistant helping with information retrieval.
        
        User Query: {query}
        
        Relevant Information:
        {context}
        
        Based on the provided information, please answer the user's query.
        If the information doesn't contain enough context to provide a complete answer,
        state that clearly and provide what you can based on the available information.
        
        Response:
        """
        
        prompt = PromptTemplate(
            input_variables=["query", "context"],
            template=prompt_template
        )
        
        # Create chain and run
        chain = LLMChain(llm=self.llm, prompt=prompt)
        response = chain.run(query=query, context=context)
        
        return {
            "response": response.strip(),
            "sources": context_docs
        }