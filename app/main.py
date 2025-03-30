from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Any, Optional
import uvicorn

# Import agent modules
from agents.chat_agent import ChatAgent
from agents.classification_agent import ClassificationAgent
from agents.orchestrator_agent import OrchestratorAgent
from agents.web_agent import WebAgent
from agents.clinical_agent import ClinicalAgent
from agents.food_security_agent import FoodSecurityAgent

# Initialize the FastAPI app
app = FastAPI(
    title="NewWebCo AI Agents API",
    description="API for orchestrating AI agents for productivity enhancement",
    version="1.0.0"
)

# Configure CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize specialized agents
web_agent = WebAgent()
clinical_agent = ClinicalAgent(data_path="data/ctg-studies.pdf")
food_security_agent = FoodSecurityAgent(data_path="data/cd1254en.pdf")

# Initialize orchestration agents
orchestrator = OrchestratorAgent(
    web_agent=web_agent,
    clinical_agent=clinical_agent,
    food_security_agent=food_security_agent
)
classification_agent = ClassificationAgent()
chat_agent = ChatAgent(classification_agent=classification_agent, orchestrator=orchestrator)

# Define request models
class QueryRequest(BaseModel):
    query: str
    context: Optional[Dict[str, Any]] = None
    conversation_id: Optional[str] = None

class QueryResponse(BaseModel):
    response: str
    sources: Optional[List[Dict[str, Any]]] = None
    additional_info: Optional[Dict[str, Any]] = None
    agent_used: str

# Define API routes
@app.get("/")
async def root():
    return {"message": "Welcome to NewWebCo AI Agents API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/query", response_model=QueryResponse)
async def process_query(request: QueryRequest):
    try:
        # The chat agent handles all initial queries
        response = chat_agent.process_query(
            request.query, 
            context=request.context,
            conversation_id=request.conversation_id
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Run the application when executed directly
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 