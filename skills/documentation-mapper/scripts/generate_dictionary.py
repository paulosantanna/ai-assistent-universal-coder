#!/usr/bin/env python3
"""Generate data dictionary from project analysis."""

import json
import os
import sys
import yaml
from pathlib import Path


def main():
    analysis_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("./output/data")
    output_dir = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("./output/data")

    output_dir.mkdir(parents=True, exist_ok=True)

    # Load analysis
    analysis_file = analysis_dir / "analise_camadas.yaml"
    if not analysis_file.exists():
        print("ERROR: analysis file not found. Run analyze_layers.py first.")
        sys.exit(1)

    with open(analysis_file, "r", encoding="utf-8") as f:
        analysis = yaml.safe_load(f)

    dictionary = {
        "metadata": {
            "generated_at": analysis.get("metadata", {}).get("analyzed_at", ""),
            "repository": analysis.get("metadata", {}).get("repository", ""),
            "version": "1.0.0"
        },
        "databases": {}
    }

    # Extract MongoDB collections
    data_layer = analysis.get("layers", {}).get("data_persistence", {})
    mongo_info = data_layer.get("findings", {}).get("mongodb", {})

    if mongo_info.get("status") == "FOUND":
        mongo_collections = extract_mongo_collections(mongo_info.get("files", []))
        if mongo_collections:
            dictionary["databases"]["mongodb"] = {
                "type": "MongoDB",
                "collections": mongo_collections
            }

    # Extract ChromaDB collections
    chroma_info = data_layer.get("findings", {}).get("chromadb", {})
    if chroma_info.get("status") == "FOUND":
        chroma_collections = extract_chroma_collections(chroma_info.get("files", []))
        if chroma_collections:
            dictionary["databases"]["chromadb"] = {
                "type": "ChromaDB",
                "collections": chroma_collections
            }

    # Extract SQL tables
    sql_info = data_layer.get("findings", {}).get("sql", {})
    if sql_info.get("status") == "FOUND":
        sql_tables = extract_sql_tables(sql_info.get("files", []))
        if sql_tables:
            dictionary["databases"]["sql"] = {
                "type": "SQL",
                "tables": sql_tables
            }

    dictionary_file = output_dir / "dicionario_de_dados.yaml"
    with open(dictionary_file, "w", encoding="utf-8") as f:
        yaml.dump(dictionary, f, allow_unicode=True, default_flow_style=False, sort_keys=False)

    print(f"Data dictionary saved to: {dictionary_file}")


def extract_mongo_collections(files: list[str]) -> list[dict]:
    """Extract MongoDB collection information from schema/model files."""
    collections = []
    for filepath in files:
        full_path = Path(filepath)
        if not full_path.exists():
            # Try relative to CWD
            full_path = Path.cwd() / filepath
        if not full_path.exists():
            continue

        try:
            content = full_path.read_text(encoding="utf-8", errors="replace")

            # Try to infer collection name from filename
            collection_name = full_path.stem.replace(".model", "").replace(".schema", "")
            if collection_name.endswith("s"):
                pass  # likely pluralized collection name
            else:
                collection_name = collection_name  # keep as is

            fields = extract_fields_from_code(content)

            collections.append({
                "collection": collection_name,
                "source_file": str(full_path),
                "fields": fields if fields else [{"name": "UNKNOWN", "type": "UNKNOWN", "description": "Could not parse schema automatically"}],
                "indexes": extract_indexes(content),
                "relationships": extract_relationships(content),
                "document_count_estimate": "UNKNOWN"
            })
        except Exception as e:
            print(f"  Warning: could not parse {filepath}: {e}")

    return collections


def extract_chroma_collections(files: list[str]) -> list[dict]:
    """Extract ChromaDB collection information."""
    collections = []
    for filepath in files:
        full_path = Path(filepath)
        if not full_path.exists():
            full_path = Path.cwd() / filepath
        if not full_path.exists():
            continue

        try:
            content = full_path.read_text(encoding="utf-8", errors="replace")
            collections.append({
                "collection": full_path.stem,
                "source_file": str(full_path),
                "embedding_dimension": "UNKNOWN",
                "metadata_schema": "UNKNOWN",
                "distance_function": "cosine",
                "use_case": "UNKNOWN",
                "document_count_estimate": "UNKNOWN"
            })
        except Exception:
            pass

    return collections


def extract_sql_tables(files: list[str]) -> list[dict]:
    """Extract SQL table information."""
    tables = []
    for filepath in files:
        full_path = Path(filepath)
        if not full_path.exists():
            full_path = Path.cwd() / filepath
        if not full_path.exists():
            continue

        try:
            content = full_path.read_text(encoding="utf-8", errors="replace")
            columns = extract_sql_columns(content)

            tables.append({
                "table": full_path.stem,
                "source_file": str(full_path),
                "columns": columns if columns else [{"name": "UNKNOWN", "type": "UNKNOWN"}],
                "row_count_estimate": "UNKNOWN"
            })
        except Exception:
            pass

    return tables


def extract_fields_from_code(content: str) -> list[dict]:
    """Extract field definitions from various schema formats."""
    fields = []
    lines = content.split("\n")

    for i, line in enumerate(lines):
        line = line.strip()

        # Mongoose schema
        if ":" in line and ("type:" in line.lower() or "type:" in line):
            parts = line.split(":")
            name = parts[0].strip().replace('"', "").replace("'", "")
            type_info = parts[1].strip() if len(parts) > 1 else "String"
            fields.append({
                "name": name,
                "type": type_info.split(",")[0].strip() if "," in type_info else type_info.strip(),
                "required": "required" in line.lower() or "true" in line.split("required")[-1][:5] if "required" in line.lower() else "unknown",
                "default": extract_default(line)
            })

        # Prisma / TypeORM
        if any(kw in line for kw in ["@Field", "@Column", "@Prop"]):
            parts = line.split()
            for j, part in enumerate(parts):
                if "(" in part and ")" in part:
                    # Extract type from decorator
                    pass

    return fields


def extract_default(line: str) -> str:
    """Extract default value from a code line."""
    if "default:" in line.lower():
        idx = line.lower().find("default:")
        rest = line[idx + 8:].strip()
        return rest.split(",")[0].split(")")[0].strip()
    return "none"


def extract_indexes(content: str) -> list[dict]:
    """Extract index definitions from code."""
    indexes = []
    lines = content.split("\n")
    for line in lines:
        if "index" in line.lower() and ("unique" in line.lower() or "true" in line.lower()):
            indexes.append({"definition": line.strip(), "unique": "unique" in line.lower()})
    return indexes


def extract_relationships(content: str) -> list[dict]:
    """Extract relationship definitions from code."""
    rels = []
    lines = content.split("\n")
    for line in lines:
        if any(kw in line.lower() for kw in ["ref:", "references", "foreignkey", "relation", "populate"]):
            rels.append({"definition": line.strip()})
    return rels


def extract_sql_columns(content: str) -> list[dict]:
    """Extract column definitions from SQL or ORM files."""
    columns = []
    lines = content.split("\n")
    for line in lines:
        stripped = line.strip()
        if stripped and not stripped.startswith("--") and not stripped.startswith("//") and not stripped.startswith("#"):
            if any(kw in stripped.upper() for kw in ["INT", "VARCHAR", "TEXT", "BOOLEAN", "FLOAT", "DECIMAL", "DATE", "TIMESTAMP", "UUID", "JSON", "SERIAL"]):
                parts = stripped.split()
                if len(parts) >= 2:
                    columns.append({
                        "name": parts[0].strip().replace('"', ""),
                        "type": parts[1].strip().rstrip(","),
                        "nullable": "NOT NULL" not in stripped.upper(),
                        "constraints": [kw for kw in ["PRIMARY KEY", "UNIQUE", "REFERENCES", "DEFAULT", "CHECK"] if kw in stripped.upper()]
                    })
    return columns


if __name__ == "__main__":
    main()
