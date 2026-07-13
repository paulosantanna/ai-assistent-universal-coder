from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[2] / "scripts" / "ecosystem_contracts.py"
spec = importlib.util.spec_from_file_location("ecosystem_contracts", MODULE_PATH)
ecosystem_contracts = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules["ecosystem_contracts"] = ecosystem_contracts
spec.loader.exec_module(ecosystem_contracts)


def test_all_ecosystem_contracts_pass_in_repository():
    root = Path(__file__).resolve().parents[3]

    results = [ecosystem_contracts.validate_contract(name, root) for name in ecosystem_contracts.CONTRACTS]

    assert {result["status"] for result in results} == {"PASS"}
    assert {result["name"] for result in results} == {"java-maven", "java-gradle", "go", "rust", "dotnet"}


def test_unknown_ecosystem_contract_fails_clearly():
    try:
        ecosystem_contracts.validate_contract("unknown")
    except KeyError as exc:
        assert "Unknown ecosystem contract" in str(exc)
    else:
        raise AssertionError("expected KeyError")
