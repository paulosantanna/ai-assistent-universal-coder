from medical_research_mcp.bm25 import BM25Index, tokenize


def test_tokenize_is_case_insensitive() -> None:
    assert tokenize("Diabetes INSULIN") == ["diabetes", "insulin"]


def test_bm25_ranks_relevant_document_first() -> None:
    documents = [
        "type 1 diabetes insulin beta cell autoimmunity",
        "astronomy black hole event horizon",
        "type 2 diabetes insulin resistance obesity",
    ]
    result = BM25Index(documents).search("diabetes insulin beta cell", top_k=1)
    assert result[0][0] == 0
    assert result[0][1] > 0
