from aeos.core.supply_chain.provenance import ArtifactProvenance, ProvenanceValidator

def test_provenance_missing_blocks():
    validator = ProvenanceValidator()
    result = validator.validate(ArtifactProvenance("", "", "", None, None))
    assert result["status"] == "BLOCKED"
