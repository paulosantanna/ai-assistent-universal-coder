OWASP_GENAI_2025={
 "LLM01":"Prompt Injection","LLM02":"Sensitive Information Disclosure","LLM03":"Supply Chain",
 "LLM04":"Data and Model Poisoning","LLM05":"Improper Output Handling","LLM06":"Excessive Agency",
 "LLM07":"System Prompt Leakage","LLM08":"Vector and Embedding Weaknesses",
 "LLM09":"Misinformation","LLM10":"Unbounded Consumption",
}
CONTROLS={
 "LLM01":["instruction-data separation","tool authorization"],
 "LLM02":["redaction","least-data access"],
 "LLM03":["SBOM","artifact provenance","multi-source advisories"],
 "LLM04":["source allowlist","dataset checksums","poisoning tests"],
 "LLM05":["schema validation","no direct execution"],
 "LLM06":["least privilege","approval gates"],
 "LLM07":["secret isolation","prompt minimization"],
 "LLM08":["tenant isolation","metadata authorization"],
 "LLM09":["citations","abstention","contradiction retrieval"],
 "LLM10":["token budgets","rate limits","timeouts","bounded recursion"],
}
def security_checklist(enabled_controls: list[str]) -> dict:
    enabled=set(enabled_controls)
    results={k:{"name":OWASP_GENAI_2025[k],"missing":[c for c in v if c not in enabled]} for k,v in CONTROLS.items()}
    return {"passed":all(not x["missing"] for x in results.values()),"results":results}
