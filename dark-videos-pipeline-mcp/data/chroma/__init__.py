"""
ChromaDB integration for LAYA training data - in-memory only.

This module provides a ChromaDB-based vector store for LAYA training vectors,
used for heat scoring in the dark-videos application.

Key design principles:
- In-memory only: no persistent state on disk
- Lives while the app lives, dies on app closure
- No installation required - uses bundled chromaDB Python package
- Minimal API: storeVector(), getVectorsByHeatScore(), querySimilar()
"""

import sys
import os
import atexit
import json
import numpy as np
from chromadb.config import Settings
from chromadb import Client

# ---------------------------------------------------------------------------
# In-memory ChromaDB client (no persistent state)
# ---------------------------------------------------------------------------

_CLIENT = None
_COLLECTION = None

def init_chroma():
    """Initialize in-memory ChromaDB client."""
    global _CLIENT, _COLLECTION
    
    # In-memory only - is_persistent=False ensures no disk write
    _CLIENT = Client(Settings(
        anonymized_telemetry=False,
        is_persistent=False
    ))
    
    _COLLECTION = _CLIENT.get_or_create_collection(
        name="laya_vectors",
        metadata={"description": "LAYA training vectors for heat scoring"}
    )
    
    return True

def shutdown_chroma():
    """Clean up ChromaDB resources on exit."""
    global _COLLECTION, _CLIENT
    _COLLECTION = None
    _CLIENT = None

# ---------------------------------------------------------------------------
# Minimal API for LAYA vector operations
# ---------------------------------------------------------------------------

def store_vector(vector_id, embedding, metadata):
    """
    Store a LAYA training vector.
    
    Args:
        vector_id: Unique identifier for the vector
        embedding: List of floats (1536-dimensional)
        metadata: Dict with metadata (title, heat_score, etc.)
    """
    if _COLLECTION is None:
        raise RuntimeError("ChromaDB not initialized")
    
    _COLLECTION.add(
        embeddings=[embedding],
        ids=[vector_id],
        metadatas=[metadata]
    )

def get_vectors_by_heat_score(min_score=0, max_score=1):
    """
    Get LAYA vectors filtered by heat score range.
    
    Args:
        min_score: Minimum heat score (inclusive)
        max_score: Maximum heat score (inclusive)
    
    Returns:
        Tuple of (vector_ids, metadatas) matching the heat score filter
    """
    if _COLLECTION is None:
        raise RuntimeError("ChromaDB not initialized")
    
    results = _COLLECTION.get(
        where={"heat_score": {"$gte": min_score, "$lte": max_score}}
    )
    
    return results.get('ids', []), results.get('metadatas', [])

def query_similar(embedding, n_results=5):
    """
    Query for similar LAYA vectors using cosine similarity.
    
    Args:
        embedding: Query embedding vector (1536-dimensional list)
        n_results: Number of similar vectors to return
    
    Returns:
        Tuple of (ids, distances, metadatas)
    """
    if _COLLECTION is None:
        raise RuntimeError("ChromaDB not initialized")
    
    results = _COLLECTION.query(
        query_embeddings=[embedding],
        n_results=n_results
    )
    
    return (
        results.get('ids', [[]])[0],
        results.get('distances', [[]])[0],
        results.get('metadatas', [[]])[0]
    )

def get_all_vectors():
    """Get all stored LAYA vectors."""
    if _COLLECTION is None:
        raise RuntimeError("ChromaDB not initialized")
    
    results = _COLLECTION.get()
    return results.get('ids', []), results.get('metadatas', [])

def vector_count():
    """Get the total number of stored LAYA vectors."""
    if _COLLECTION is None:
        raise RuntimeError("ChromaDB not initialized")
    
    return _COLLECTION.count()

# Export public API
__all__ = [
    'init_chroma', 'store_vector', 'get_vectors_by_heat_score',
    'query_similar', 'get_all_vectors', 'vector_count'
]