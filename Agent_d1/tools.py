"""
Tools module for the RAG Agent.
Contains ingest and search functions for managing the knowledge base.
"""

import json
import os
import numpy as np
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Configuration
KNOWLEDGE_BASE_PATH = os.path.join(os.path.dirname(__file__), "knowledge_base.json")
EMBEDDING_MODEL = "text-embedding-3-small"

# Initialize OpenAI client
client = OpenAI()


def load_knowledge_base() -> list[dict]:
    """Load the knowledge base from disk."""
    if os.path.exists(KNOWLEDGE_BASE_PATH):
        with open(KNOWLEDGE_BASE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_knowledge_base(data: list[dict]) -> None:
    """Save the knowledge base to disk."""
    with open(KNOWLEDGE_BASE_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def get_embedding(text: str) -> list[float]:
    """Generate embedding for a text using OpenAI API."""
    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=text
    )
    return response.data[0].embedding


def cosine_similarity(vec1: list[float], vec2: list[float]) -> float:
    """Calculate cosine similarity between two vectors."""
    a = np.array(vec1)
    b = np.array(vec2)
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


def ingest(text: str, source: str = None) -> dict:
    """
    Ingest text into the knowledge base.
    
    Args:
        text: The text content to ingest
        source: Optional source identifier (e.g., filename)
    
    Returns:
        Confirmation dictionary with ingestion details
    """
    # Generate embedding
    embedding = get_embedding(text)
    
    # Create entry
    entry = {
        "text": text,
        "embedding": embedding,
        "source": source,
        "timestamp": datetime.now().isoformat()
    }
    
    # Load, append, and save
    kb = load_knowledge_base()
    kb.append(entry)
    save_knowledge_base(kb)
    
    return {
        "status": "success",
        "message": f"Text ingested successfully",
        "source": source,
        "text_length": len(text)
    }


def search(query: str, top_k: int = 3) -> list[dict]:
    """
    Search the knowledge base for relevant documents.
    
    Args:
        query: The search query
        top_k: Number of top results to return
    
    Returns:
        List of relevant documents with similarity scores
    """
    kb = load_knowledge_base()
    
    if not kb:
        return []
    
    # Generate query embedding
    query_embedding = get_embedding(query)
    
    # Calculate similarities
    results = []
    for entry in kb:
        similarity = cosine_similarity(query_embedding, entry["embedding"])
        results.append({
            "text": entry["text"],
            "source": entry.get("source"),
            "similarity": similarity
        })
    
    # Sort by similarity and return top_k
    results.sort(key=lambda x: x["similarity"], reverse=True)
    return results[:top_k]


def ingest_file(file_path: str) -> dict:
    """
    Ingest a file into the knowledge base.
    Supports text files (.txt, .md, .py, etc.) and PDF files.
    
    Args:
        file_path: Path to the file to ingest
    
    Returns:
        Confirmation dictionary with ingestion details
    """
    if not os.path.exists(file_path):
        return {
            "status": "error",
            "message": f"File not found: {file_path}"
        }
    
    file_ext = os.path.splitext(file_path)[1].lower()
    
    try:
        if file_ext == ".pdf":
            # Handle PDF files
            from PyPDF2 import PdfReader
            reader = PdfReader(file_path)
            content = ""
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    content += text + "\n"
            
            if not content.strip():
                return {
                    "status": "error",
                    "message": "Could not extract text from PDF (may be image-based)"
                }
        else:
            # Handle text files
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
        
        return ingest(content, source=os.path.basename(file_path))
    
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

