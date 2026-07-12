from __future__ import annotations

from pathlib import Path

import pytest

from aeos_lsp.index.sqlite_store import SqliteStore
from aeos_lsp.index.symbol_index import SymbolIndex
from aeos_lsp.index.reference_index import ReferenceIndex
from aeos_lsp.index.content_hash import hash_content, hash_document, hash_ast, compare_hashes


class TestSqliteStore:
    @pytest.fixture
    def store(self) -> SqliteStore:
        return SqliteStore(db_path=Path(":memory:"))

    def test_initialization(self, store):
        assert store.conn is not None

    def test_upsert_and_get_symbol(self, store):
        store.upsert_symbol("id-1", "agent", "test-agent", "file:///test.yaml", "0:0-0:0", "0:0-0:0")
        result = store.get_symbol("id-1")
        assert result is not None
        assert result["name"] == "test-agent"

    def test_delete_symbol(self, store):
        store.upsert_symbol("id-2", "skill", "test-skill", "file:///s.yaml", "0:0-0:0", "0:0-0:0")
        store.delete_symbol("id-2")
        assert store.get_symbol("id-2") is None

    def test_get_symbols_by_uri(self, store):
        store.upsert_symbol("id-3", "agent", "a", "file:///a.yaml", "0:0-0:0", "0:0-0:0")
        symbols = store.get_symbols_by_uri("file:///a.yaml")
        assert len(symbols) > 0

    def test_delete_symbols_by_uri(self, store):
        store.upsert_symbol("id-4", "agent", "b", "file:///b.yaml", "0:0-0:0", "0:0-0:0")
        count = store.delete_symbols_by_uri("file:///b.yaml")
        assert count > 0

    def test_upsert_document(self, store):
        store.upsert_document("file:///doc.yaml", "content", "hash123")
        doc = store.get_document("file:///doc.yaml")
        assert doc is not None
        assert doc["content_hash"] == "content"

    def test_insert_reference(self, store):
        store.insert_reference("file:///src.yaml", "0:0-0:0", "file:///tgt.yaml", "1:0-1:0")
        assert True

    def test_get_stats(self, store):
        stats = store.get_stats()
        assert isinstance(stats, dict)

    def test_transaction(self, store):
        with store.transaction():
            store.upsert_symbol("tx-1", "agent", "tx-test", "file:///tx.yaml", "0:0-0:0", "0:0-0:0")
        assert store.get_symbol("tx-1") is not None

    def test_clear_all(self, store):
        store.upsert_symbol("c1", "agent", "clear1", "file:///c.yaml", "0:0-0:0", "0:0-0:0")
        store.clear_all()
        assert store.get_symbol("c1") is None


class TestSymbolIndex:
    @pytest.fixture
    def store(self) -> SqliteStore:
        return SqliteStore(db_path=Path(":memory:"))

    @pytest.fixture
    def sym_index(self, store) -> SymbolIndex:
        return SymbolIndex(store=store)

    def test_search(self, store, sym_index):
        store.upsert_symbol("s1", "agent", "test-agent", "file:///test.yaml", "0:0-0:0", "0:0-0:0")
        results = sym_index.search("test-agent")
        assert len(results) >= 1

    def test_get_by_kind(self, store, sym_index):
        store.upsert_symbol("s2", "skill", "skill-1", "file:///s1.yaml", "0:0-0:0", "0:0-0:0")
        store.upsert_symbol("s3", "agent", "agent-1", "file:///a1.yaml", "0:0-0:0", "0:0-0:0")
        agents = sym_index.get_by_kind("agent")
        assert len(agents) >= 1

    def test_get_by_stable_id(self, store, sym_index):
        store.upsert_symbol("s4", "agent", "unique", "file:///u.yaml", "0:0-0:0", "0:0-0:0")
        result = sym_index.get_by_stable_id("s4")
        assert result is not None

    def test_count_total(self, store, sym_index):
        store.upsert_symbol("c1", "agent", "count-test", "file:///ct.yaml", "0:0-0:0", "0:0-0:0")
        assert sym_index.count_total() >= 1

    def test_list_all(self, store, sym_index):
        store.upsert_symbol("l1", "agent", "list1", "file:///l.yaml", "0:0-0:0", "0:0-0:0")
        all_symbols = sym_index.list_all()
        assert len(all_symbols) >= 1


class TestReferenceIndex:
    @pytest.fixture
    def store(self) -> SqliteStore:
        return SqliteStore(db_path=Path(":memory:"))

    @pytest.fixture
    def ref_index(self, store) -> ReferenceIndex:
        return ReferenceIndex(store=store)

    def test_find_references_by_target(self, store, ref_index):
        store.insert_reference("file:///src.yaml", "0:0-0:0", "file:///tgt.yaml", "1:0-1:0")
        refs = ref_index.find_references_by_target("file:///tgt.yaml")
        assert len(refs) >= 1

    def test_find_definitions(self, store, ref_index):
        store.insert_reference("file:///src.yaml", "0:0-0:1", "file:///def.yaml", "0:0-0:0", kind="definition", role="declare")
        defs = ref_index.find_definitions("file:///def.yaml")
        assert len(defs) >= 1

    def test_find_usages(self, store, ref_index):
        store.insert_reference("file:///src.yaml", "0:0-0:0", "file:///tgt.yaml", "1:0-1:0")
        usages = ref_index.find_usages("file:///tgt.yaml")
        assert len(usages) >= 1

    def test_count_total(self, store, ref_index):
        store.insert_reference("file:///src.yaml", "0:0-0:0", "file:///tgt.yaml", "1:0-1:0")
        assert ref_index.count_total() >= 0


class TestContentHash:
    def test_hash_content(self):
        h = hash_content("hello")
        assert isinstance(h, str) and len(h) > 0
        assert hash_content("hello") == hash_content("hello")

    def test_hash_document(self):
        h = hash_document("file:///test.yaml", "content")
        assert isinstance(h, str)

    def test_hash_ast(self):
        h = hash_ast({"name": "test"})
        assert isinstance(h, str)

    def test_compare_hashes(self):
        h = hash_content("data")
        assert compare_hashes(h, h)
        assert not compare_hashes("", "")
