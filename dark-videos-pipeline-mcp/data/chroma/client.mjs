/**
 * ChromaDB Bridge Client - Node.js wrapper for in-memory ChromaDB.
 * 
 * This module spawns a Python subprocess that manages an in-memory ChromaDB
 * instance for LAYA training vector storage. The Python process lives while
 * the Node.js app lives and is automatically killed on exit.
 * 
 * Usage:
 *   import { initChroma, storeLayaVector, getLayaVectorsByHeatScore } from './data/chroma/client.mjs';
 *   await initChroma();
 *   await storeLayaVector('video_1', embedding, { title: 'Test', heat_score: 0.85 });
 *   const vectors = await getLayaVectorsByHeatScore(0.7, 1.0);
 */

import { spawn } from "node:child_process";
import { writeFileSync, readFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";

// ---------------------------------------------------------------------------
// Subprocess management
// ---------------------------------------------------------------------------

let pythonProcess = null;
let initializationPromise = null;

// Communication helpers
const REQUEST_TIMEOUT = 5000; // 5 seconds

function sendMessage(message) {
  return new Promise((resolve, reject) => {
    if (!pythonProcess) {
      reject(new Error("ChromaDB process not running"));
      return;
    }

    const msgJson = JSON.stringify(message) + "\n";
    pythonProcess.stdin.write(msgJson);

    // Set up a one-time timeout
    const timeoutId = setTimeout(() => {
      reject(new Error("ChromaDB request timeout"));
      cleanupListeners();
    }, REQUEST_TIMEOUT);

    const cleanupListeners = () => {
      pythonProcess.removeListener("error", onError);
      pythonProcess.removeListener("exit", onExit);
    };

    function onError(err) {
      reject(err);
      cleanupListeners();
    }

    function onExit(code) {
      if (code !== null) {
        reject(new Error(`ChromaDB process exited with code ${code}`));
      }
      cleanupListeners();
    }

    pythonProcess.once("error", onError);
    pythonProcess.once("exit", onExit);
  });
}

// ---------------------------------------------------------------------------
// Initialize ChromaDB Python subprocess
// ---------------------------------------------------------------------------

/**
 * Initialize the ChromaDB Python subprocess.
 * Creates an in-memory ChromaDB instance for LAYA training vectors.
 */
export async function initChroma() {
  if (pythonProcess) {
    // Already initialized
    return;
  }

  // Find the Python executable
  const pythonPath = "python"; // Assumes python is in PATH

  // Path to the ChromaDB integration script
  const scriptPath = join(
    process.cwd(),
    "data",
    "chroma",
    "chroma_bridge.py"
  );

  pythonProcess = spawn(pythonPath, [scriptPath], {
    stdio: ["pipe", "pipe", "pipe"],
    cwd: process.cwd(),
    env: { ...process.env, PYTHONUNBUFFERED: "1" },
  });

  // Handle errors
  pythonProcess.on("error", (err) => {
    console.error("❌ ChromaDB Python process error:", err);
    pythonProcess = null;
    throw err;
  });

  pythonProcess.on("exit", (code) => {
    console.log(`⚠️ ChromaDB Python process exited with code ${code}`);
    pythonProcess = null;
  });

  // Wait for initialization to complete
  if (initializationPromise) {
    await initializationPromise;
  }
}

// ---------------------------------------------------------------------------
// ChromaDB Bridge Python Script
// ---------------------------------------------------------------------------

/*
The chroma_bridge.py script is a Python script that:
1. Initializes in-memory ChromaDB
2. Listens for stdio commands
3. Performs vector operations
4. On exit, ensures no persistent state remains
*/

/*
import chromadb
from chromadb.config import Settings
import json
import sys

# In-memory only ChromaDB client
client = chromadb.Client(Settings(anonymized_telemetry=False, is_persistent=False))
collection = client.get_or_create_collection(
    name="laya_vectors",
    metadata={"description": "LAYA training vectors for heat scoring"}
)

def handle_request():
    """Read commands from stdin and respond."""
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
        except json.JSONDecodeError:
            continue

        cmd = req.get("cmd")
        id_ = req.get("id")

        if cmd == "store_vector":
            vector_id = req["args"]["vector_id"]
            embedding = req["args"]["embedding"]
            metadata = req["args"]["metadata"]
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
            embedding = req["args"]["embedding"]
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
            # No persistent state to clean up (in-memory mode)
            send_response(id_, {"status": "shutdown"})
            break

        else:
            send_response(id_, {"error": f"unknown command: {cmd}"})

def send_response(id_, result):
    """Send a JSON response to stdout."""
    response = json.dumps({"id": id_, "result": result}) + "\n"
    sys.stdout.write(response)
    sys.stdout.flush()

if __name__ == "__main__":
    handle_request()
*/

// ---------------------------------------------------------------------------
// API functions for Node.js
// ---------------------------------------------------------------------------

/**
 * Store a LAYA training vector in ChromaDB.
 * 
 * @param {string} vectorId - Unique vector identifier
 * @param {number[]} embedding - 1536-dimensional embedding vector
 * @param {object} metadata - Metadata object (title, heat_score, etc.)
 * @returns {Promise<object>} Response from ChromaDB
 */
export async function storeLayaVector(vectorId, embedding, metadata) {
  await initChroma();
  
  const response = await sendMessage({
    cmd: "store_vector",
    id: "store_" + vectorId,
    args: {
      vector_id: vectorId,
      embedding: embedding,
      metadata: metadata
    }
  });
  
  return response.result;
}

/**
 * Get LAYA vectors filtered by heat score range.
 * 
 * @param {number} minScore - Minimum heat score (inclusive, 0-1)
 * @param {number} maxScore - Maximum heat score (inclusive, 0-1)
 * @returns {Promise<object>} Response with vector IDs and metadata
 */
export async function getLayaVectorsByHeatScore(minScore, maxScore) {
  await initChroma();
  
  const response = await sendMessage({
    cmd: "get_by_heat_score",
    id: "heat_query",
    args: {
      min_score: minScore !== undefined ? minScore : 0,
      max_score: maxScore !== undefined ? maxScore : 1
    }
  });
  
  return response.result;
}

/**
 * Query for similar LAYA vectors using cosine similarity.
 * 
 * @param {number[]} embedding - Query embedding vector (1536-dimensional)
 * @param {number} [nResults=5] - Number of similar vectors to return
 * @returns {Promise<object>} Response with similar vector IDs, distances, and metadata
 */
export async function querySimilarLaya(embedding, nResults = 5) {
  await initChroma();
  
  const response = await sendMessage({
    cmd: "query_similar",
    id: "similar_query",
    args: {
      embedding: embedding,
      n_results: nResults
    }
  });
  
  return response.result;
}

/**
 * Get all stored LAYA vectors.
 * 
 * @returns {Promise<object>} Response with all vector IDs and metadata
 */
export async function getAllLayaVectors() {
  await initChroma();
  
  const response = await sendMessage({
    cmd: "get_all",
    id: "all_query"
  });
  
  return response.result;
}

/**
 * Get the total count of stored LAYA vectors.
 * 
 * @returns {Promise<object>} Response with vector count
 */
export async function getLayaVectorCount() {
  await initChroma();
  
  const response = await sendMessage({
    cmd: "count",
    id: "count_query"
  });
  
  return response.result;
}

/**
 * Shut down the ChromaDB Python process.
 * Call this when the application is closing to ensure cleanup.
 */
export async function shutdownChroma() {
  if (!pythonProcess) {
    return;
  }
  
  await sendMessage({
    cmd: "shutdown",
    id: "shutdown_query"
  });
  
  if (pythonProcess && !pythonProcess.killed) {
    pythonProcess.kill();
  }
  pythonProcess = null;
}

// Auto-exit handler: ensure ChromaDB process is killed on Node.js exit
// This is registered at the module level
if (require.main === module) {
  // Only for direct execution, not as import
}

// Register process exit handler
process.on("beforeExit", async () => {
  try {
    await shutdownChroma();
  } catch (e) {
    console.error("Error during ChromaDB shutdown:", e);
  }
});

process.on("exit", async () => {
  try {
    await shutdownChroma();
  } catch (e) {
    console.error("Error during ChromaDB shutdown:", e);
  }
});
