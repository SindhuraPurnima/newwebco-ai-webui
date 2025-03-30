# NewWebCo AI Assistant

An advanced productivity WebUI using Agentic AI with Retrieval Augmented Generation (RAG) capabilities.

## Project Overview

This application enables employees to achieve more with less effort using Agentic AI orchestration. It features three specialized agents:

1. **Clinical Agent**: For processing healthcare and clinical information
2. **Food Security Agent**: For agricultural and food security queries
3. **General Web Agent**: For handling general knowledge queries

## Features

- Domain-specific intelligent agents with semantic query classification
- Document processing and embedding using E5 large language model
- Real-time query classification and routing
- Advanced chunking strategies for large documents

## Architecture

The system follows a multi-agent architecture:
- Frontend: React-based user interface
- Backend: FastAPI orchestration service
- Agents: Specialized AI agents for different domains

## Prerequisites

- Python 3.9+ with conda or venv
- Node.js and npm for the frontend
- PDF documents placed in the `app/data/` directory

## Getting Started

### Backend Setup

1. **Create and activate a conda environment**:
   ```bash
   conda create -n cmpe280_hackathon python=3.10
   conda activate cmpe280_hackathon
   ```

2. **Install required packages**:
   ```bash
   pip install fastapi uvicorn transformers torch scikit-learn pypdf numpy tqdm
   ```

3. **Ensure your PDF documents are in place**:
   - Place clinical PDFs (e.g., `ctg-studies.pdf`) in `app/data/`
   - Place food security PDFs (e.g., `cd1254en.pdf`) in `app/data/`

### Frontend Setup

1. **Navigate to the frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

## Running the Application

### Starting the Backend

1. **Navigate to the app directory from the project root**:
   ```bash
   cd app
   ```

2. **Start the FastAPI backend**:
   ```bash
   python -m uvicorn main:app --reload
   ```

3. **First-run note**: The first time you run the backend, it will:
   - Download the E5 embedding model (may take a few minutes)
   - Process PDF documents and create embeddings (progress will be displayed)
   - Save embeddings to disk for faster future startup

The backend will be available at `http://127.0.0.1:8000`

### Starting the Frontend

1. **Open a new terminal window/tab**

2. **Navigate to the frontend directory from the project root**:
   ```bash
   cd frontend
   ```

3. **Start the development server**:
   ```bash
   npm start
   ```

The frontend will be available at `http://localhost:3000`

## Usage

1. Open your browser and navigate to `http://localhost:3000`
2. Enter your query in the text box
3. The system will:
   - Classify your query into the appropriate domain (Clinical, Food Security, or General)
   - Retrieve relevant information from the appropriate knowledge base
   - Generate a response based on the retrieved information

## Troubleshooting

- **Backend startup issues**: 
  - Ensure you have activated the correct conda environment
  - Check that all required packages are installed
  - Verify that the PDFs are in the correct location

- **Slow PDF processing**: 
  - Large PDFs (especially the food security PDF) may take several minutes to process
  - Progress indicators will show status during processing
  - This only happens on first run; subsequent starts will be faster

- **"No module found" errors**: 
  - Run `pip install -r requirements.txt` from the project root
  - Make sure your Python environment is activated

- **Poor responses**: 
  - Try queries that match the content of your PDFs
  - For clinical queries, ask about cardiotocography (CTG) or fetal monitoring
  - For food security queries, ask about agriculture or food production

## Technologies Used

- **Frontend**: React, React Router
- **Backend**: FastAPI, PyTorch, Transformers
- **AI/ML**: RAG (Retrieval Augmented Generation), E5 embeddings

## Project Status

- [x] Frontend UI
- [x] Backend API
- [x] Agent Implementation
- [x] PDF Knowledge Integration