"""
ChromaDB Bridge Python Script.

This script serves as the Python subprocess that manages an in-memory ChromaDB
instance for LAYA training vector storage. It:

1. Initializes ChromaDB in in-memory mode (no persistent state on disk)
2. Listens for stdio commands from the Node.js client
3. Performs vector operations (store, query, filter by heat score)
4. On exit, ensures no persistent state remains (by design, in-memory mode)

Key guarantees:
- No data written to disk during operation
- Automatic cleanup on process exit
- Minimal API for LAYA heat scoring integration
"""

import sys
import os
import json
import atexit

# Ensure chromaDB is imported from the bundled location
try:
    import chromadb
    from chromadb.config import Settings
except ImportError:
    # Try to find chromaDB in common locations
    import site
    for prefix in site.getsitepackages():
        try:
            import importlib.util
            spec = importlib.util.find_spec("chromadb", [prefix])
            if spec:
                break
        except Exception:
            pass
    # Fallback to default import
    import chromadb
    from chromadb.config import Settings

# ---------------------------------------------------------------------------
# In-memory ChromaDB client (guaranteed no persistent state)
# ---------------------------------------------------------------------------

# Create client with explicit in-memory settings
client = chromadb.Client(Settings(
    anonymized_telemetry=False,
    is_persistent=False
))

# Create collection for LAYA training vectors
collection = client.get_or_create_collection(
    name="laya_vectors",
    metadata={"description": "LAYA training vectors for heat scoring"}
)

# In-memory mode: collection data is automatically lost on process exit
# No explicit cleanup needed - is_persistent=False guarantees no disk writes

# Register atexit for defensive cleanup only
atexit.register(lambda: None)

# ---------------------------------------------------------------------------
# Command handler
# ---------------------------------------------------------------------------

def handle_request():
    """Read commands from stdin and respond."""
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        
        try:
            req = json.loads(line)
        except json.JSONDecodeError:
            # Send error response for malformed JSON
            try:
                sys.stdout.write(
                    json.dumps({"id": None, "result": {"error": "invalid_json"}}) + "\n"
                )
                sys.stdout.flush()
            except Exception:
                pass
            continue

        cmd = req.get("cmd")
        id_ = req.get("id")

        if cmd == "store_vector":
            vector_id = req["args"].get("vector_id", "")
            embedding = req["args"].get("embedding", [])
            metadata = req["args"].get("metadata", {})
            collection.add(
                embeddings=[embedding],
                ids=[vector_id],
                metadatas=[metadata]
            )
            send_response(id_, {"status": "ok", "vector_id": vector_id})

        elif cmd == "get_by_heat_score":
            min_score = req["args"].get("min_score", 0)
            max_score = req["args"].get("max_score", 1)
            results = collection.get(
                where={"heat_score": {"$gte": min_score, "$lte": max_score}}
            )
            send_response(id_, {
                "ids": results.get("ids", []),
                "metadatas": results.get("metadatas", [])
            })

        elif cmd == "query_similar":
            embedding = req["args"].get("embedding", [])
            n_results = req["args"].get("n_results", 5)
            results = collection.query(
                query_embeddings=[embedding],
                n_results=n_results
            )
            send_response(id_, {
                "ids": results.get("ids", [[]])[0],
                "distances": results.get("distances", [[]])[0],
                "metadatas": results.get("metadatas", [[]])[0]
            })

        elif cmd == "get_all":
            results = collection.get()
            send_response(id_, {
                "ids": results.get("ids", []),
                "metadatas": results.get("metadatas", [])
            })

        elif cmd == "count":
            send_response(id_, {"count": collection.count()})

        elif cmd == "shutdown":
            # In-memory mode: no persistent state to clean up
            # But ensure collection is cleared
            collection.delete(ids=collection.get(ids=None)[0] or [])
            send_response(id_, {"status": "shutdown"})

        else:
            send_response(id_, {"error": f"unknown command: {cmd}"})

def send_response(id_, result):
    """Send a JSON response to stdout."""
    response = json.dumps({"id": id_, "result": result}) + "\n"
    sys.stdout.write(response)
    sys.stdout.flush()

if __name__ == "__main__":
    handle_request()