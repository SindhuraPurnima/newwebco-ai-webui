# app/main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Any, Optional
import os

from utils.document_processor import DocumentProcessor
from utils.search_engine import SearchEngine
from utils.text_generation import TextGenerator
from utils.domain_classifier import DomainClassifier
from utils.custom_embeddings import E5EmbeddingModel

app = FastAPI(
    title="NewWebCo AI Agents API",
    description="API for orchestrating AI agents for productivity enhancement",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
document_processor = DocumentProcessor()
classifier = DomainClassifier()

# Setup paths
data_dir = os.path.join(os.path.dirname(__file__), "data")
vector_db_dir = os.path.join(os.path.dirname(__file__), "vector_db")
os.makedirs(vector_db_dir, exist_ok=True)

# Define domains and their document sources
DOMAINS = {
    "clinical": {
        "description": "Medical topics, healthcare, diseases, symptoms, treatment, diagnosis",
        "pdf_files": ["ctg-studies.pdf"]
    },
    "food_security": {
        "description": "Agriculture, farming, crops, food production, nutrition, policy",
        "pdf_files": ["cd1254en.pdf"]
    },
    "general": {
        "description": "General knowledge, technology, science, history, AI, computers",
        "pdf_files": []  # No PDFs for general knowledge as we'll use the model
    }
}

# Initialize with domain awareness
document_collections = {}

# Process each domain's documents
for domain_name, domain_info in DOMAINS.items():
    domain_pdfs = domain_info["pdf_files"]
    domain_docs = []
    
    for pdf_file in domain_pdfs:
        pdf_path = os.path.join(data_dir, pdf_file)
        vector_db_path = os.path.join(vector_db_dir, f"{domain_name}_{pdf_file}.pkl")
        
        if os.path.exists(pdf_path):
            if os.path.exists(vector_db_path):
                # Load existing embeddings
                domain_docs.extend(document_processor.load_vector_store(vector_db_path))
                print(f"Loaded {pdf_file} embeddings for {domain_name}")
            else:
                # Process new PDF with domain awareness
                new_docs = document_processor.process_pdf(pdf_path, vector_db_path, domain_name)
                domain_docs.extend(new_docs)
                print(f"Created embeddings for {pdf_file} in {domain_name} domain")
    
    document_collections[domain_name] = domain_docs

# Initialize search engine with document collections
search_engine = SearchEngine(document_collections)
embedding_model = E5EmbeddingModel()
search_engine.set_embedding_model(embedding_model)

# Initialize text generator (LLM)
text_generator = TextGenerator()

# Define request/response models
class QueryRequest(BaseModel):
    query: str
    context: Optional[Dict[str, Any]] = None
    conversation_id: Optional[str] = None

class QueryResponse(BaseModel):
    response: str
    sources: List[Dict[str, Any]]
    domain: str
    confidence: float

@app.get("/")
async def root():
    return {"message": "Welcome to NewWebCo AI Agents API"}

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "document_collections": list(document_collections.keys())
    }

@app.post("/query", response_model=QueryResponse)
async def process_query(request: QueryRequest):
    try:
        # 1. Log the incoming query for debugging
        print(f"Processing query: {request.query}")
        
        # 2. Classify the query
        classification = classifier.classify_query(request.query)
        domain = classification["domain"]
        confidence = classification["confidence"]
        print(f"Query classified as '{domain}' with confidence {confidence}")
        
        # 3. Verify query classification makes sense
        if "artificial intelligence" in request.query.lower() or "ai" in request.query.lower().split():
            print("Query contains AI terminology, forcing general domain")
            domain = "general"
            
        # 4. Retrieve relevant documents
        relevant_docs = search_engine.search(
            request.query, 
            domain=domain,
            top_k=5
        )
        
        # 5. Check if we have meaningful results
        has_relevant_docs = any(doc.get("score", 0) > 0.4 for doc in relevant_docs)
        
        # 6. Generate appropriate response
        if domain != "general" and not has_relevant_docs:
            # For specialized domains with no good matches, try general domain
            print(f"No good matches in {domain}, trying general domain")
            general_docs = search_engine.search(request.query, domain="general", top_k=3)
            
            # Combine results
            relevant_docs = general_docs + relevant_docs
        
        # 7. Generate response with domain context
        text_response = text_generator.generate_response(
            request.query,
            relevant_docs,
            domain=domain
        )
        
        # 8. Return results
        return {
            "response": text_response["response"],
            "sources": relevant_docs,
            "domain": domain,
            "confidence": float(confidence)
        }
        
    except Exception as e:
        print(f"Error processing query: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)