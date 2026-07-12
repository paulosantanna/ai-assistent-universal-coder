from __future__ import annotations

from typing import Any

from aeos_lsp.index.sqlite_store import SqliteStore


class ReferenceIndex:
    def __init__(self, store: SqliteStore) -> None:
        self._store = store

    # ── find references by source URI ──────────────────────────────

    def find_references_by_source(
        self,
        source_uri: str,
        limit: int = 200,
        offset: int = 0,
    ) -> list[dict[str, Any]]:
        rows = self._store.conn.execute(
            "SELECT * FROM references_ WHERE source_uri = ? ORDER BY kind, role LIMIT ? OFFSET ?",
            (source_uri, limit, offset),
        ).fetchall()
        return [dict(r) for r in rows]

    def count_by_source(self, source_uri: str) -> int:
        row = self._store.conn.execute(
            "SELECT COUNT(*) FROM references_ WHERE source_uri = ?", (source_uri,)
        ).fetchone()
        return row[0] if row else 0

    # ── find references by target URI ──────────────────────────────

    def find_references_by_target(
        self,
        target_uri: str,
        limit: int = 200,
        offset: int = 0,
    ) -> list[dict[str, Any]]:
        rows = self._store.conn.execute(
            "SELECT * FROM references_ WHERE target_uri = ? ORDER BY kind, role LIMIT ? OFFSET ?",
            (target_uri, limit, offset),
        ).fetchall()
        return [dict(r) for r in rows]

    def count_by_target(self, target_uri: str) -> int:
        row = self._store.conn.execute(
            "SELECT COUNT(*) FROM references_ WHERE target_uri = ?", (target_uri,)
        ).fetchone()
        return row[0] if row else 0

    # ── definitions ────────────────────────────────────────────────

    def find_definitions(
        self,
        target_uri: str,
        limit: int = 50,
        offset: int = 0,
    ) -> list[dict[str, Any]]:
        rows = self._store.conn.execute(
            "SELECT * FROM references_ WHERE target_uri = ? AND kind = 'definition' "
            "ORDER BY source_uri LIMIT ? OFFSET ?",
            (target_uri, limit, offset),
        ).fetchall()
        return [dict(r) for r in rows]

    def find_definitions_by_stable_id(
        self,
        stable_id: str,
        limit: int = 50,
        offset: int = 0,
    ) -> list[dict[str, Any]]:
        symbol = self._store.get_symbol(stable_id)
        if symbol is None:
            return []
        return self.find_definitions(symbol["uri"], limit, offset)

    # ── usages ─────────────────────────────────────────────────────

    def find_usages(
        self,
        target_uri: str,
        limit: int = 200,
        offset: int = 0,
    ) -> list[dict[str, Any]]:
        rows = self._store.conn.execute(
            "SELECT * FROM references_ WHERE target_uri = ? AND kind != 'definition' "
            "ORDER BY source_uri LIMIT ? OFFSET ?",
            (target_uri, limit, offset),
        ).fetchall()
        return [dict(r) for r in rows]

    def find_usages_by_stable_id(
        self,
        stable_id: str,
        limit: int = 200,
        offset: int = 0,
    ) -> list[dict[str, Any]]:
        symbol = self._store.get_symbol(stable_id)
        if symbol is None:
            return []
        return self.find_usages(symbol["uri"], limit, offset)

    # ── combined queries ──────────────────────────────────────────

    def find_all_references(
        self,
        target_uri: str,
        include_definitions: bool = False,
        limit: int = 200,
        offset: int = 0,
    ) -> list[dict[str, Any]]:
        if include_definitions:
            return self.find_references_by_target(target_uri, limit, offset)
        return self.find_usages(target_uri, limit, offset)

    def find_references_for_symbol(
        self,
        stable_id: str,
        include_definitions: bool = False,
        limit: int = 200,
        offset: int = 0,
    ) -> list[dict[str, Any]]:
        symbol = self._store.get_symbol(stable_id)
        if symbol is None:
            return []
        return self.find_all_references(
            symbol["uri"], include_definitions, limit, offset,
        )

    # ── cross-workspace ────────────────────────────────────────────

    def find_cross_workspace_references(
        self,
        target_uri: str,
        workspace_prefixes: list[str],
        limit: int = 200,
        offset: int = 0,
    ) -> list[dict[str, Any]]:
        if not workspace_prefixes:
            return self.find_references_by_target(target_uri, limit, offset)

        placeholders = ",".join("?" for _ in workspace_prefixes)
        like_clause = " OR ".join(f"source_uri LIKE ?" for _ in workspace_prefixes)
        params: list[str] = []
        for prefix in workspace_prefixes:
            params.append(f"{prefix}%")
        params.append(target_uri)
        params.extend(workspace_prefixes)
        params.extend(str(x) for x in [limit, offset])
        like_params = " OR ".join(f"source_uri LIKE ?" for _ in workspace_prefixes)
        rows = self._store.conn.execute(
            f"SELECT * FROM references_ WHERE "
            f"target_uri = ? AND ({like_params}) "
            f"ORDER BY source_uri LIMIT ? OFFSET ?",
            [target_uri] + [f"{p}%" for p in workspace_prefixes] + [limit, offset],
        ).fetchall()
        return [dict(r) for r in rows]

    # ── by kind / role ─────────────────────────────────────────────

    def find_by_kind(
        self,
        kind: str,
        limit: int = 200,
        offset: int = 0,
    ) -> list[dict[str, Any]]:
        rows = self._store.conn.execute(
            "SELECT * FROM references_ WHERE kind = ? ORDER BY source_uri LIMIT ? OFFSET ?",
            (kind, limit, offset),
        ).fetchall()
        return [dict(r) for r in rows]

    def find_by_role(
        self,
        role: str,
        limit: int = 200,
        offset: int = 0,
    ) -> list[dict[str, Any]]:
        rows = self._store.conn.execute(
            "SELECT * FROM references_ WHERE role = ? ORDER BY source_uri LIMIT ? OFFSET ?",
            (role, limit, offset),
        ).fetchall()
        return [dict(r) for r in rows]

    def count_by_kind_and_role(self) -> list[dict[str, Any]]:
        rows = self._store.conn.execute(
            "SELECT kind, role, COUNT(*) as cnt FROM references_ GROUP BY kind, role ORDER BY cnt DESC"
        ).fetchall()
        return [dict(r) for r in rows]

    # ── aggregation ────────────────────────────────────────────────

    def count_total(self) -> int:
        row = self._store.conn.execute("SELECT COUNT(*) FROM references_").fetchone()
        return row[0] if row else 0

    def get_most_referenced(self, limit: int = 20) -> list[dict[str, Any]]:
        rows = self._store.conn.execute(
            "SELECT target_uri, COUNT(*) as ref_count FROM references_ "
            "GROUP BY target_uri ORDER BY ref_count DESC LIMIT ?",
            (limit,),
        ).fetchall()
        return [dict(r) for r in rows]

    def get_most_referencing(self, limit: int = 20) -> list[dict[str, Any]]:
        rows = self._store.conn.execute(
            "SELECT source_uri, COUNT(*) as ref_count FROM references_ "
            "GROUP BY source_uri ORDER BY ref_count DESC LIMIT ?",
            (limit,),
        ).fetchall()
        return [dict(r) for r in rows]
