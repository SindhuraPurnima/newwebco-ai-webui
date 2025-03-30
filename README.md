# NewWebCo AI WebUI

A web-based productivity enhancement tool using Agentic AI, developed for NewWebCo employees.

## Project Overview

This application enables employees to achieve more with less effort using Agentic AI orchestration. It features three specialized agents:

1. **Web Agent**: For handling general WebUI queries
2. **Clinical RAG Agent**: For processing healthcare and clinical information
3. **Food Security Agent**: For agricultural and food security queries

## Architecture

The system follows a multi-agent architecture:
- Frontend: React-based user interface
- Backend: FastAPI orchestration service
- Agents: Specialized AI agents for different domains

## Getting Started

### Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

### Backend Setup (Coming Soon)

```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start FastAPI server
python app/main.py
```

## Technologies Used

- **Frontend**: React, React Router
- **Backend**: FastAPI, Langchain
- **AI/ML**: RAG (Retrieval Augmented Generation)

## Project Status

- [x] Frontend UI
- [ ] Backend API
- [ ] Agent Implementation
- [ ] PDF Knowledge Integration