from __future__ import annotations

import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from aeos.core.permissions.capability_loader import CapabilityLoader
from aeos.core.permissions.permission_engine import PermissionEngine
from aeos.core.permissions.permission_models import PermissionRequest
from aeos.core.policy.policy_engine import PolicyEngine
from aeos.core.policy.policy_models import PolicyRequest
from aeos.core.evidence.evidence_store import EvidenceStore
from aeos.core.evidence.audit_logger import AuditLogger
from aeos.core.evidence.evidence_reporter import EvidenceReporter
from aeos.core.governance.governance_gate import GovernanceGate
from aeos.core.governance.governance_models import GovernanceRequest
from aeos.core.governance.governance_reporter import GovernanceReporter


def run_smoke_tests(workspace_root: str = "."):
    execution_id = "smoke-test-001"
    results = []
    errors = []

    def check(name: str, condition: bool, detail: str = ""):
        if condition:
            print(f"  [PASS] {name}")
            results.append((name, True, detail))
        else:
            msg = f"  [FAIL] {name}"
            if detail:
                msg += f" - {detail}"
            print(msg)
            results.append((name, False, detail))
            errors.append(name)

    print("=" * 60)
    print("AEOS Governance Smoke Test")
    print("=" * 60)

    print("\n[1] Permission Engine: deny-all default")
    perm = PermissionEngine(workspace_root)
    perm.initialize()
    req = PermissionRequest(
        execution_id=execution_id, actor="ghost", role="", action="test", capability="READ_FILES", resource=""
    )
    d = perm.evaluate(req)
    check("actor without role => deny", not d.allowed and "no role" in d.reason.lower())

    print("\n[2] Permission Engine: role without capability => deny")
    req2 = PermissionRequest(
        execution_id=execution_id, actor="tester", role="tester", action="test", capability="MAP_ARCHITECTURE", resource=""
    )
    d2 = perm.evaluate(req2)
    assert_msg = f"allowed={d2.allowed}, reason='{d2.reason}'"
    check("role without capability => deny", not d2.allowed and "does not have" in d2.reason.lower(), assert_msg)

    print("\n[3] Permission Engine: capability inexistente => deny")
    req3 = PermissionRequest(
        execution_id=execution_id, actor="coder", role="coder", action="test", capability="NONEXISTENT_CAP", resource=""
    )
    d3 = perm.evaluate(req3)
    check("capability inexistente => deny", not d3.allowed and "does not exist" in d3.reason.lower())

    print("\n[4] Policy Engine: write sandbox permitido")
    pol = PolicyEngine(workspace_root)
    pol.initialize()
    req4 = PolicyRequest(
        execution_id=execution_id, action="filesystem.write", resource=".aeos/sandbox/test.txt"
    )
    d4 = pol.evaluate(req4)
    check("sandbox write allowed", d4.allowed)

    print("\n[5] Policy Engine: write fora do sandbox bloqueado")
    req5 = PolicyRequest(
        execution_id=execution_id, action="filesystem.write", resource="src/main.py"
    )
    d5 = pol.evaluate(req5)
    check("outside sandbox write blocked", not d5.allowed)

    print("\n[6] Policy Engine: shell allowlisted permitido")
    req6 = PolicyRequest(
        execution_id=execution_id, action="shell.run", command="pytest", resource="pytest"
    )
    d6 = pol.evaluate(req6)
    check("allowlisted shell allowed", d6.allowed)

    print("\n[7] Policy Engine: shell não allowlisted bloqueado")
    req7 = PolicyRequest(
        execution_id=execution_id, action="shell.run", command="rm -rf /", resource="rm -rf /"
    )
    d7 = pol.evaluate(req7)
    check("unlisted shell blocked", not d7.allowed)

    print("\n[8] Policy Engine: git merge bloqueado")
    req8 = PolicyRequest(execution_id=execution_id, action="git.merge")
    d8 = pol.evaluate(req8)
    check("git merge blocked", not d8.allowed)

    print("\n[9] Policy Engine: force push bloqueado")
    req9 = PolicyRequest(execution_id=execution_id, action="git.force_push")
    d9 = pol.evaluate(req9)
    check("force push blocked", not d9.allowed)

    print("\n[10] Policy Engine: package extract sem verify bloqueado")
    req10 = PolicyRequest(
        execution_id=execution_id, action="package.extract", resource="pkg.zip", details={"verified": False}
    )
    d10 = pol.evaluate(req10)
    check("unverified package extract blocked", not d10.allowed)

    print("\n[11] Policy Engine: approval wildcard bloqueado")
    req11 = PolicyRequest(execution_id=execution_id, action="approval.wildcard")
    d11 = pol.evaluate(req11)
    check("wildcard approval blocked", not d11.allowed)

    print("\n[12] Policy Engine: protected branch blocked")
    req12 = PolicyRequest(execution_id=execution_id, action="branch.protected", branch="main")
    d12 = pol.evaluate(req12)
    check("protected branch blocked", not d12.allowed)

    print("\n[13] Evidence Store: manifest gerado")
    store = EvidenceStore()
    rep = EvidenceReporter()
    rid = store.store_record(execution_id, "audit", {"action": "smoke_test", "status": "running"})
    manifest_path = rep.generate_manifest(execution_id, {"audit": 1})
    check("evidence manifest generated", Path(manifest_path).exists(), manifest_path)

    print("\n[14] Evidence Store: hash-chain gerada")
    chain = store.get_hash_chain()
    check("hash-chain generated", len(chain) == 1, f"{len(chain)} links")

    print("\n[15] Governance Gate: BLOCKED quando permission denied")
    gate = GovernanceGate(workspace_root)
    gate.initialize()
    g_req = GovernanceRequest(
        execution_id=execution_id, action="filesystem.delete",
        actor="coder", role="coder", capability="WRITE_SANDBOX_FILES",
        resource="src/main.py"
    )
    g_res = gate.evaluate(g_req)
    check("governance blocks permission denied", g_res.status == "BLOCKED")

    print("\n[16] Governance Gate: WAITING_APPROVAL")
    g_req2 = GovernanceRequest(
        execution_id=execution_id, action="secrets.read",
        actor="tester", role="tester", capability="READ_FILES",
        resource=".env", approval_present=False,
    )
    g_res2 = gate.evaluate(g_req2)
    assert_msg = f"status={g_res2.status}, perm={g_res2.permission_allowed}, policy={g_res2.policy_allowed}, approval={g_res2.requires_approval}"
    check("governance WAITING_APPROVAL", g_res2.status == "WAITING_APPROVAL", assert_msg)

    print("\n[17] Governance Gate: PASS quando tudo ok")
    root_caps = perm.loader.get_role_capabilities("root")
    if root_caps:
        cap = root_caps[0]
    else:
        cap = "GENERATE_REPORT"
    g_req3 = GovernanceRequest(
        execution_id=execution_id, action="reports.generate",
        actor="root", role="root", capability=cap,
        resource=".aeos/reports/test.md",
    )
    g_res3 = gate.evaluate(g_req3)
    check("governance PASS", g_res3.status == "PASS")

    print(f"\n{'=' * 60}")
    total = len(results)
    passed = sum(1 for _, ok, _ in results if ok)
    failed = total - passed
    print(f"Results: {passed}/{total} passed, {failed} failed")

    if failed > 0:
        print(f"\nFailed tests:")
        for name, ok, detail in results:
            if not ok:
                print(f"  - {name}")
        print("\n  STATUS: FAIL")
    else:
        print("\n  STATUS: PASS")
    print(f"{'=' * 60}")

    return passed == total, results


if __name__ == "__main__":
    success, _ = run_smoke_tests()
    sys.exit(0 if success else 1)
