from __future__ import annotations

import json
from typing import Any

from aeos_lsp.index.sqlite_store import SqliteStore


def _rank_symbol(row: dict[str, Any], query: str) -> float:
    name: str = row.get("name", "")
    stable_id: str = row.get("stable_id", "")
    kind: str = row.get("kind", "")

    score = 0.0
    q = query.lower()

    if name.lower() == q:
        score += 100.0
    elif name.lower().startswith(q):
        score += 50.0
    elif q in name.lower():
        score += 20.0
    elif stable_id.lower() == q:
        score += 60.0
    elif q in stable_id.lower():
        score += 10.0

    if kind == "workspace":
        score += 5.0
    elif kind in ("agent", "skill", "playbook"):
        score += 3.0
    elif kind in ("tool", "command"):
        score += 2.0

    return score


class SymbolIndex:
    def __init__(self, store: SqliteStore) -> None:
        self._store = store

    # ── workspace symbol queries ───────────────────────────────────

    def search_by_prefix(self, prefix: str, limit: int = 100, offset: int = 0) -> list[dict[str, Any]]:
        if not prefix:
            return []
        pattern = prefix.replace("%", "\\%").replace("_", "\\_") + "%"
        rows = self._store.conn.execute(
            "SELECT * FROM symbols WHERE name LIKE ? ESCAPE '\\' ORDER BY name LIMIT ? OFFSET ?",
            (pattern, limit, offset),
        ).fetchall()
        return [dict(r) for r in rows]

    def search_by_fuzzy(self, query: str, limit: int = 100, offset: int = 0) -> list[dict[str, Any]]:
        if not query:
            return []
        pattern = f"%{query.replace('%', '\\%').replace('_', '\\_')}%"
        rows = self._store.conn.execute(
            "SELECT * FROM symbols WHERE name LIKE ? ESCAPE '\\' OR stable_id LIKE ? ESCAPE '\\' "
            "ORDER BY name LIMIT ? OFFSET ?",
            (pattern, pattern, limit, offset),
        ).fetchall()
        results = [dict(r) for r in rows]
        results.sort(key=lambda r: _rank_symbol(r, query), reverse=True)
        return results

    def search_by_exact(self, name: str) -> dict[str, Any] | None:
        row = self._store.conn.execute(
            "SELECT * FROM symbols WHERE name = ?", (name,)
        ).fetchone()
        return dict(row) if row else None

    def search(
        self,
        query: str,
        kind: str | None = None,
        uri: str | None = None,
        workspace: str | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[dict[str, Any]]:
        if not query:
            return []

        conditions: list[str] = []
        params: list[Any] = []

        pattern = f"%{query.replace('%', '\\%').replace('_', '\\_')}%"
        conditions.append("(name LIKE ? ESCAPE '\\' OR stable_id LIKE ? ESCAPE '\\')")
        params.extend([pattern, pattern])

        if kind is not None:
            conditions.append("kind = ?")
            params.append(kind)
        if uri is not None:
            conditions.append("uri = ?")
            params.append(uri)
        if workspace is not None:
            conditions.append("uri LIKE ?")
            params.append(f"{workspace}%")

        sql = f"SELECT * FROM symbols WHERE {' AND '.join(conditions)} ORDER BY name LIMIT ? OFFSET ?"
        params.extend([limit, offset])

        rows = self._store.conn.execute(sql, params).fetchall()
        results = [dict(r) for r in rows]
        results.sort(key=lambda r: _rank_symbol(r, query), reverse=True)
        return results

    # ── document symbol queries ────────────────────────────────────

    def get_document_symbols(
        self,
        uri: str,
        kind: str | None = None,
        limit: int = 500,
        offset: int = 0,
    ) -> list[dict[str, Any]]:
        if kind is not None:
            rows = self._store.conn.execute(
                "SELECT * FROM symbols WHERE uri = ? AND kind = ? ORDER BY name LIMIT ? OFFSET ?",
                (uri, kind, limit, offset),
            ).fetchall()
        else:
            rows = self._store.conn.execute(
                "SELECT * FROM symbols WHERE uri = ? ORDER BY kind, name LIMIT ? OFFSET ?",
                (uri, limit, offset),
            ).fetchall()
        return [dict(r) for r in rows]

    # ── filter queries ─────────────────────────────────────────────

    def get_by_kind(self, kind: str, limit: int = 500, offset: int = 0) -> list[dict[str, Any]]:
        rows = self._store.conn.execute(
            "SELECT * FROM symbols WHERE kind = ? ORDER BY name LIMIT ? OFFSET ?",
            (kind, limit, offset),
        ).fetchall()
        return [dict(r) for r in rows]

    def get_by_uri(self, uri: str) -> list[dict[str, Any]]:
        return self._store.get_symbols_by_uri(uri)

    def get_by_stable_id(self, stable_id: str) -> dict[str, Any] | None:
        return self._store.get_symbol(stable_id)

    def count_by_uri(self, uri: str) -> int:
        row = self._store.conn.execute(
            "SELECT COUNT(*) FROM symbols WHERE uri = ?", (uri,)
        ).fetchone()
        return row[0] if row else 0

    def count_by_kind(self, kind: str) -> int:
        row = self._store.conn.execute(
            "SELECT COUNT(*) FROM symbols WHERE kind = ?", (kind,)
        ).fetchone()
        return row[0] if row else 0

    def count_total(self) -> int:
        row = self._store.conn.execute("SELECT COUNT(*) FROM symbols").fetchone()
        return row[0] if row else 0

    # ── aggregation ────────────────────────────────────────────────

    def get_kind_counts(self) -> dict[str, int]:
        rows = self._store.conn.execute(
            "SELECT kind, COUNT(*) as cnt FROM symbols GROUP BY kind ORDER BY cnt DESC"
        ).fetchall()
        return {r["kind"]: r["cnt"] for r in rows}

    def get_uri_counts(self, limit: int = 50) -> list[dict[str, Any]]:
        rows = self._store.conn.execute(
            "SELECT uri, COUNT(*) as cnt FROM symbols GROUP BY uri ORDER BY cnt DESC LIMIT ?",
            (limit,),
        ).fetchall()
        return [dict(r) for r in rows]

    # ── pagination ─────────────────────────────────────────────────

    def list_all(self, limit: int = 100, offset: int = 0) -> list[dict[str, Any]]:
        rows = self._store.conn.execute(
            "SELECT * FROM symbols ORDER BY kind, name LIMIT ? OFFSET ?",
            (limit, offset),
        ).fetchall()
        return [dict(r) for r in rows]
