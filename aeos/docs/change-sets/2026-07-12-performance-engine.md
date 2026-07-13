# Change Set: AEOS Performance Engine

Date: 2026-07-12
Scope: Improve AEOS total performance across Python core, scanner, evidence, registry loading and TypeScript runtime.
Status: Verified

## Summary

This change set adds structural performance improvements to AEOS hot paths:

- Fingerprinted in-process cache for skill registry loading.
- Per-loader cache for resolved skill contracts.
- Shared skill loader between executor and validator to avoid duplicate registry/contract work.
- Pruned repository scanning with optional fast mode that skips counting ignored files.
- Batched evidence record writes with a single hash-chain flush per logical batch.
- TypeScript runtime YAML/Markdown parse cache with mtime/size invalidation.
- TypeScript registry lookup indexes for playbooks, agents, skills, MCPs and LCPs.
- Governed performance optimization skill and playbook.
- Performance budgets for registry, skill contract, evidence batch and runtime config hot paths.

## Files Changed In This Change Set

| File | Change | Current SHA-256 |
| --- | --- | --- |
| `aeos/core/skill_engine/skill_registry_resolver.py` | Added fingerprinted shared registry cache and cache controls. | `2d6849d69974bb375c33f7cdea38f80aad227e6240a110448fe2d3f8fbdacb5e` |
| `aeos/core/skill_engine/skill_loader.py` | Added per-instance skill contract cache. | `f7b5f46a9a62e7e53360022e2752cf9f19af3a6e94c5b3f4dd433339cc0dcb31` |
| `aeos/core/skill_engine/skill_contract_validator.py` | Allows validator to reuse an existing `SkillLoader`. | `e6551a02cdfe6da54de080c6c82b34ce4ad9fa9160e0f7d6812873af0491b230` |
| `aeos/core/skill_engine/skill_executor.py` | Reuses the executor loader for contract validation. | `8201b6b4b714fa25d42a422bcfc7387cb1bee29df9fa92d914640a81ad7896dc` |
| `aeos/core/scanner/fast_repo_scanner.py` | Replaced broad `rglob` scan with pruned `os.walk` traversal. | `d6ab1d37b53fe9dd2e9030e355bff0eded79d7f178cad20c2857a2b953baadf3` |
| `aeos/core/evidence/evidence_store.py` | Added `store_records` batch write path and batched `store_decisions`. | `b225590585cc62016464f8dd9e70b0c73f23c46b8b1f3ce3ca310c73e3c14e15` |
| `aeos/core/performance/performance_optimizer.py` | New deterministic performance optimization planner. | `6218d4ddce1ec799b9c1727d11d5e0c317b3bb1cf58379d2028929db72a5e57c` |
| `runtime/src/kernel/config-loader.ts` | Added YAML and Markdown cache with mtime/size invalidation. | `c1aef47c8b6d39791b12724bd38a06fc384dcddbe4f8f03655c7d456e9588cbb` |
| `runtime/src/kernel/registry-loader.ts` | Added id indexes and O(1) registry resolution paths. | `4c945f0619daeaca597e19735fe4f411f154689f0afddc17f23478da04d5d5e5` |
| `aeos/tests/skill_engine/test_skill_loader.py` | Added cache behavior tests. | `1420a3ff54ef968d7d3452d177f18a6077db22640eadcd3b17a4cb33d0e395f3` |
| `aeos/tests/scanner/test_fast_repo_scanner.py` | Added scanner fast-prune test. | `779c48b735c20c7c9c799eda1911876c5c7b62475c4b4ddd4673b34f539217d8` |
| `aeos/tests/evidence/test_evidence_store.py` | Added evidence batch hash-chain test. | `0ff97dd0d07c3a1ad16a25188a419bf4b0a69798e7c26e7935b0d8be3d7a2d90` |
| `aeos/tests/enterprise/test_performance_optimizer.py` | New tests for performance optimizer plans. | `0d9cc1800a6d18de75ff8b857befc7330da4bda15e32836aad2820dfb590d3ea` |
| `aeos/config/performance-budgets.yaml` | Added hot-path performance budgets and policies. | `bf8bb30f1cbe772863ca7852db09b37c690298477e1a758ff6b5f7f9c55559a6` |
| `aeos/config/capabilities.yaml` | Added `PERFORMANCE_OPTIMIZATION`. | `5b10461cecbeeb8ed346563b398ec3c26f46720a4ea5e2f990ae2cd5fc48af99` |
| `aeos/config/permissions.yaml` | Granted performance optimization capability to governed roles. | `8879025a5571e05c177ce82f82553f76009bdb9b95edf6e4a91e25a736114e96` |
| `aeos/skills/core/performance-optimizer.skill.md` | New performance optimization skill contract. | `32d044ae7a8518a9bfabeeae74a39c2a701b1f3b24d8ef4226248d8a1feee32a` |
| `aeos/playbooks/performance-optimization.playbook.md` | New performance optimization playbook. | `99bbb3710b4a52fb238dedbd386349e433d6a76c0bd58e86d1b911ef1a9cd492` |
| `aeos/registries/skills.registry.yaml` | Registered `performance-optimizer`. | `5e321f941bdaf3a46c53e3f98413480f7bd99c71272b0f0395b6b223acdbb2b2` |
| `aeos/registries/playbooks.registry.yaml` | Registered `performance-optimization`. | `b5a20bd2007c623e69fe0fb367ead7e0473751475692391628b0feb5e50f1a86` |

## Rollback Plan

Rollback this performance change set as a single group.

1. Remove these new files:
   - `aeos/core/performance/performance_optimizer.py`
   - `aeos/tests/enterprise/test_performance_optimizer.py`
   - `aeos/skills/core/performance-optimizer.skill.md`
   - `aeos/playbooks/performance-optimization.playbook.md`
   - `aeos/docs/change-sets/2026-07-12-performance-engine.md`
2. Revert only the performance hunks in:
   - `aeos/core/skill_engine/skill_registry_resolver.py`
   - `aeos/core/skill_engine/skill_loader.py`
   - `aeos/core/skill_engine/skill_contract_validator.py`
   - `aeos/core/skill_engine/skill_executor.py`
   - `aeos/core/scanner/fast_repo_scanner.py`
   - `aeos/core/evidence/evidence_store.py`
   - `runtime/src/kernel/config-loader.ts`
   - `runtime/src/kernel/registry-loader.ts`
   - `aeos/tests/skill_engine/test_skill_loader.py`
   - `aeos/tests/scanner/test_fast_repo_scanner.py`
   - `aeos/tests/evidence/test_evidence_store.py`
   - `aeos/config/performance-budgets.yaml`
   - `aeos/config/capabilities.yaml`
   - `aeos/config/permissions.yaml`
   - `aeos/registries/skills.registry.yaml`
   - `aeos/registries/playbooks.registry.yaml`
3. Re-run `npm run build` in `runtime/` if TypeScript files are reverted.
4. Re-run the validation commands listed below.

Do not use broad reset commands for this rollback because the worktree contains unrelated earlier AEOS evolution changes.

## Validation

Commands executed:

```bash
python -m py_compile aeos/core/skill_engine/skill_registry_resolver.py aeos/core/skill_engine/skill_loader.py aeos/core/skill_engine/skill_contract_validator.py aeos/core/skill_engine/skill_executor.py aeos/core/scanner/fast_repo_scanner.py aeos/core/evidence/evidence_store.py aeos/core/performance/performance_optimizer.py
python -m aeos.cli.main registry validate
/tmp/aeos-venv/bin/python -m pytest aeos/tests/skill_engine/test_skill_loader.py aeos/tests/skill_engine/test_skill_executor.py aeos/tests/scanner/test_fast_repo_scanner.py aeos/tests/evidence/test_evidence_store.py aeos/tests/enterprise/test_performance_budget.py aeos/tests/enterprise/test_performance_optimizer.py -q
npm run build
/tmp/aeos-venv/bin/python aeos/scripts/verify.py --suite full --python /tmp/aeos-venv/bin/python
```

Results:

- Python compile: PASS
- YAML load check: PASS
- Registry validation: PASS, 189 entries across 5 types
- Focused tests: PASS, 45 passed
- TypeScript build: PASS
- Full AEOS verification: PASS
  - Core tests: 434 passed
  - Skills tests: 13 passed
  - MCP tests: 69 passed, 1 skipped
  - Universal project MCP tests: 8 passed
  - LSP tests: 518 passed
  - Runtime build: OK
