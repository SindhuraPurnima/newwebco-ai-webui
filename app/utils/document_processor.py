# app/utils/document_processor.py
import os
import pickle
import numpy as np
import time
from pypdf import PdfReader
from tqdm import tqdm
from .custom_embeddings import E5EmbeddingModel

class DocumentProcessor:
    """Process documents and create embeddings"""
    
    def __init__(self):
        self.embedding_model = E5EmbeddingModel()
        self.chunk_size = 1000
        self.chunk_overlap = 200
        
    def process_pdf(self, pdf_path, vector_db_path, domain_name=None):
        """Process a PDF into chunks and generate embeddings with progress indicators"""
        start_time = time.time()
        pdf_name = os.path.basename(pdf_path)
        print(f"Starting processing of {pdf_name} for domain: {domain_name or 'unknown'}")
        
        # Extract text from PDF with progress bar
        extract_start = time.time()
        print(f"[1/3] Extracting text from PDF...")
        chunks = self._extract_chunks_from_pdf(pdf_path)
        extract_time = time.time() - extract_start
        print(f"[1/3] ✓ Text extraction complete: {len(chunks)} chunks created in {extract_time:.2f} seconds")
        
        # Calculate embeddings for all chunks with progress bar
        embedding_start = time.time()
        print(f"[2/3] Generating embeddings for {len(chunks)} chunks...")
        embeddings = []
        
        # Process embeddings in batches with tqdm
        for i in tqdm(range(0, len(chunks), 8), desc="Embedding Chunks"):
            batch = chunks[i:i+8]
            batch_embeddings = self.embedding_model.get_embeddings(batch)
            embeddings.extend(batch_embeddings)
            
        embedding_time = time.time() - embedding_start
        print(f"[2/3] ✓ Embeddings generation complete in {embedding_time:.2f} seconds")
        
        # Create document metadata
        save_start = time.time()
        print(f"[3/3] Creating and saving document metadata...")
        documents = []
        
        for i, (chunk, embedding) in enumerate(tqdm(zip(chunks, embeddings), total=len(chunks), desc="Creating Documents")):
            documents.append({
                "content": chunk,
                "embedding": embedding,
                "metadata": {
                    "source": os.path.basename(pdf_path),
                    "chunk_id": i,
                    "domain": domain_name or "general"
                }
            })
        
        # Save to disk with progress indication
        os.makedirs(os.path.dirname(vector_db_path), exist_ok=True)
        print(f"Saving {len(documents)} documents to {os.path.basename(vector_db_path)}...")
        with open(vector_db_path, 'wb') as f:
            pickle.dump(documents, f)
            
        save_time = time.time() - save_start
        total_time = time.time() - start_time
        
        print(f"[3/3] ✓ Document metadata saved in {save_time:.2f} seconds")
        print(f"✓ PDF processing complete. Total time: {total_time:.2f} seconds")
        print(f"  - Extraction: {extract_time:.2f}s ({extract_time/total_time*100:.1f}%)")
        print(f"  - Embedding: {embedding_time:.2f}s ({embedding_time/total_time*100:.1f}%)")
        print(f"  - Saving: {save_time:.2f}s ({save_time/total_time*100:.1f}%)")
            
        return documents
    
    def _extract_chunks_from_pdf(self, pdf_path):
        """Extract text chunks from a PDF with progress indicators"""
        # Open the PDF
        reader = PdfReader(pdf_path)
        total_pages = len(reader.pages)
        text = ""
        
        # Extract text with progress bar
        print(f"  - Reading {total_pages} pages...")
        for page in tqdm(reader.pages, desc="Extracting Pages", total=total_pages):
            page_text = page.extract_text() or ""
            text += page_text + "\n"
        
        # Split into chunks with progress indication
        chunk_start = time.time()
        print(f"  - Splitting text into chunks...")
        
        # Split by paragraphs first for better semantic coherence
        paragraphs = text.split("\n\n")
        chunks = []
        current_chunk = ""
        
        for paragraph in tqdm(paragraphs, desc="Creating Chunks"):
            # If adding this paragraph would exceed chunk size
            if len(current_chunk) + len(paragraph) > self.chunk_size:
                # Add current chunk if not empty
                if current_chunk:
                    chunks.append(current_chunk.strip())
                # Start new chunk
                current_chunk = paragraph
            else:
                # Add to current chunk
                if current_chunk:
                    current_chunk += "\n\n" + paragraph
                else:
                    current_chunk = paragraph
        
        # Add the last chunk if not empty
        if current_chunk.strip():
            chunks.append(current_chunk.strip())
        
        print(f"  - ✓ Chunking complete: {len(chunks)} chunks created in {time.time() - chunk_start:.2f} seconds")
        return chunks
        
    def load_vector_store(self, vector_db_path):
        """Load embeddings from disk with progress indicator"""
        start_time = time.time()
        print(f"Loading embeddings from {os.path.basename(vector_db_path)}...")
        
        if os.path.exists(vector_db_path):
            with open(vector_db_path, 'rb') as f:
                documents = pickle.load(f)
            print(f"✓ Loaded {len(documents)} documents in {time.time() - start_time:.2f} seconds")
            return documents
        
        print(f"× No embeddings found at {vector_db_path}")
        return []