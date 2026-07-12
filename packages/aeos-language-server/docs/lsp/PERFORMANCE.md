# AEOS Language Server — Performance

## Target Metrics

The AEOS Language Server targets the following performance metrics for typical workspace sizes:

| Metric | Target | Acceptable | Notes |
|---|---|---|---|
| **Startup time** | < 2s | < 5s | Time from `initialize` to ready for requests |
| **Index time** | < 1s per 100 files | < 3s per 100 files | Full workspace index |
| **Validation time** | < 100ms per file | < 500ms per file | Schema + semantic validation |
| **Completion latency** | < 50ms | < 200ms | Time from request to response |
| **Hover latency** | < 30ms | < 100ms | Time from request to response |
| **Definition latency** | < 20ms | < 50ms | Time from request to response |
| **Memory (idle)** | < 100 MB | < 200 MB | Baseline memory usage |
| **Memory (peak)** | < 250 MB | < 500 MB | During full workspace index |
| **Diagnostic push** | < 200ms | < 500ms | From file change to diagnostic publish |
| **File watcher latency** | < 100ms | < 500ms | From FS event to index update |

## Indexing Performance

### Full Index

When the server starts, it performs a full workspace index:

1. **File discovery** — Walk the workspace directory tree, collecting `.yaml`, `.yml`, `.json` files
2. **File parsing** — Parse each AEOS file into its document model
3. **Schema validation** — Validate each file against its corresponding schema
4. **Graph resolution** — Resolve cross-references (`$id`, `stable_id`, skill references, etc.)
5. **Semantic analysis** — Run semantic validation rules
6. **Cache population** — Populate the LRU cache with parsed documents

### Incremental Index

File changes trigger incremental updates:

1. **File watcher** detects a change event
2. **Debounce** — Multiple rapid changes are batched (configurable, default 500ms)
3. **Re-parse** — Only the changed file is re-parsed
4. **Re-validate** — Only the changed file is re-validated
5. **Graph update** — Only references involving the changed file are re-resolved

### Indexing Time By Workspace Size

| File Count | Full Index | Incremental Index | Notes |
|---|---|---|---|
| 10 | < 100ms | < 20ms | Small workspace |
| 100 | < 500ms | < 50ms | Medium workspace |
| 1,000 | < 5s | < 200ms | Large workspace |
| 10,000 | < 30s | < 1s | Very large workspace (warning issued) |

### Parallelism

Indexing operations use worker threads for parallelism:
- File parsing: concurrent across files
- Schema validation: concurrent across files
- Graph resolution: sequential (depends on resolved references)

## Memory Usage

### Memory Breakdown

| Component | Typical Size | Notes |
|---|---|---|
| **Document models** | ~10 KB per file | Parsed document in memory |
| **Schema cache** | ~50 KB per schema | 10 schemas = ~500 KB |
| **Graph index** | ~1 KB per reference | 1000 references = ~1 MB |
| **Validation cache** | ~2 KB per file | Cached validation results |
| **LRU cache** | Configurable (default 50 MB) | Cached parsed documents |
| **Plugin runtime** | Variable | Depends on loaded plugins |

### Configuration

```jsonc
{
  "aeos": {
    "performance": {
      "memory": {
        "maxDocumentCacheMB": 50,      // LRU cache size
        "maxSchemaCacheMB": 10,        // Schema cache size
        "maxGraphCacheMB": 20,         // Graph index cache size
        "enableGarbageCollection": true // Force GC between large operations
      }
    }
  }
}
```

### Memory Optimization Tips

1. **Reduce `maxFiles`** — Limit the number of indexed files
2. **Increase `excludePatterns`** — Exclude non-AEOS directories
3. **Disable semantic rules** — Reduces memory for rule evaluation
4. **Reduce cache size** — Smaller LRU cache uses less memory
5. **Use "fast" profile** — Minimal indexing, no graph resolution

## Caching Strategy

### Cache Layers

```
Layer 1: File Content Cache
  - Key: file path + modification time
  - Value: raw file content (string)
  - Size: configurable (default 50 MB)
  - Eviction: LRU

Layer 2: Document Model Cache
  - Key: file path + content hash
  - Value: parsed document model (AST)
  - Size: configurable (default 50 MB)
  - Eviction: LRU

Layer 3: Validation Results Cache
  - Key: file path + document hash
  - Value: validation results (diagnostics array)
  - TTL: configurable (default 300s)
  - Invalidation: on file change

Layer 4: Graph Cache
  - Key: reference source + target
  - Value: resolved reference location
  - TTL: configurable (default 600s)
  - Invalidation: on workspace change

Layer 5: Schema Cache
  - Key: schema $id
  - Value: compiled schema validator
  - Persistence: kept for server lifetime
```

### Cache Invalidation

| Event | Invalidated Caches |
|---|---|
| File changed | Layer 1-4 for that file, Layer 4 for files referencing it |
| File deleted | Layer 1-4 for that file, Layer 4 for all files referencing it |
| File created | Layer 4 (new references may be resolved) |
| Schema changed | Layer 3 for all files (re-validation needed) |
| Configuration changed | Layer 3-5 |
| Workspace folders changed | All layers |

### Cache Configuration

```jsonc
{
  "aeos": {
    "performance": {
      "cache": {
        "enabled": true,
        "fileContent": {
          "maxSizeMB": 50,
          "ttlSeconds": 600
        },
        "documentModel": {
          "maxSizeMB": 50,
          "ttlSeconds": 600
        },
        "validation": {
          "enabled": true,
          "ttlSeconds": 300
        },
        "graph": {
          "enabled": true,
          "ttlSeconds": 600
        }
      }
    }
  }
}
```

## Profile Recommendations

### Workspace Size Guide

| Workspace Size | File Count | Recommended Profile | Notes |
|---|---|---|---|
| **Small** | 1-50 files | Balanced (default) | Full features, fast performance |
| **Medium** | 50-500 files | Balanced (default) | Full features, acceptable performance |
| **Large** | 500-5,000 files | Balanced with tuning | Adjust cache, debounce, exclude patterns |
| **Very Large** | 5,000-10,000 files | Fast | Minimal features, optimize indexing |
| **Monorepo** | 10,000+ files | Fast with heavy exclusion | Exclude non-AEOS directories aggressively |

### Use Case Guide

| Use Case | Recommended Profile | Notes |
|---|---|---|
| **Quick edit** | Fast | Minimal latency for simple edits |
| **Development** | Balanced | Best balance of features and speed |
| **Code review** | Thorough | Full validation for quality assurance |
| **Security audit** | Thorough | All security checks enabled |
| **Compliance review** | Thorough | Evidence and judge validation |
| **CI pipeline** | Fast | Minimize resource usage in CI |
| **Large refactor** | Balanced | Need cross-reference resolution |

## Benchmark Results Format

When running performance benchmarks, results should be reported in the following format:

```json
{
  "benchmark": {
    "name": "AEOS Language Server Performance Benchmark",
    "version": "1.0.0",
    "date": "2025-07-11T12:00:00Z",
    "system": {
      "platform": "win32",
      "cpu": "AMD Ryzen 9 7950X 16-Core Processor",
      "cpu_cores": 16,
      "ram_gb": 64,
      "disk_type": "NVMe SSD",
      "node_version": "20.15.0"
    },
    "workspace": {
      "file_count": 500,
      "total_size_mb": 12.5,
      "artifact_types": {
        "agents": 50,
        "skills": 150,
        "playbooks": 100,
        "policies": 30,
        "permissions": 10,
        "registries": 20,
        "profiles": 40,
        "budgets": 20,
        "evidence": 30,
        "judge": 10,
        "other_yaml": 40
      }
    },
    "results": {
      "startup": {
        "cold_start_ms": 1850,
        "warm_start_ms": 420,
        "index_time_ms": 3200
      },
      "validation": {
        "full_workspace_ms": 4500,
        "per_file_avg_ms": 9,
        "per_file_p95_ms": 25,
        "incremental_ms": 45
      },
      "completions": {
        "simple_ms": 12,
        "reference_ms": 35,
        "snippet_ms": 8,
        "p95_latency_ms": 45
      },
      "hover": {
        "schema_hover_ms": 8,
        "reference_hover_ms": 20,
        "p95_latency_ms": 25
      },
      "definition": {
        "local_definition_ms": 5,
        "cross_file_definition_ms": 18,
        "p95_latency_ms": 30
      },
      "memory": {
        "idle_mb": 85,
        "indexing_peak_mb": 210,
        "validation_peak_mb": 165
      },
      "caching": {
        "cache_hit_rate": 0.92,
        "avg_cache_lookup_ms": 0.5,
        "cache_miss_penalty_ms": 45
      }
    },
    "notes": "Balanced profile. Default cache settings. No plugins loaded."
  }
}
```

### Running Benchmarks

```bash
# Run full benchmark
aeos-language-server --benchmark

# Run specific benchmark
aeos-language-server --benchmark=startup,validation

# Run benchmark with custom workspace
aeos-language-server --benchmark --workspace=./test-workspace

# Run benchmark and output results
aeos-language-server --benchmark --output=benchmark-results.json
```

### Benchmark Profiles

The built-in benchmark suite measures:

1. **Startup** — Cold start (no cache) and warm start (with cache)
2. **Indexing** — Full workspace index time
3. **Validation** — Full validation and incremental validation
4. **Completions** — Completion latency at various cursor positions
5. **Hover** — Hover latency for different element types
6. **Definition** — Go-to-definition latency (local and cross-file)
7. **Memory** — Memory usage at idle, during indexing, during validation
8. **Caching** — Cache hit rate, lookup time, miss penalty
