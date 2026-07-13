# Change Set: Change Tracking And Rollback Traceability

Date: 2026-07-12
Scope: Make AEOS-generated file changes traceable for review and rollback.
Status: Verified

## Summary

This change set adds a governed change tracking layer for sandbox scaffold generation. Generated files now produce a change manifest, rollback plan and rollback summary, and the zero-to-production flow requires a trace audit before applying generated artifacts.

## Files Changed In This Change Set

| File | Change | Current SHA-256 |
| --- | --- | --- |
| `aeos/core/change_tracking/__init__.py` | New package export for change tracking primitives. | `cd90059a8e9e9906204244a86dd61afabba90dc1b4e0845b0fd03659f4c148c8` |
| `aeos/core/change_tracking/change_tracker.py` | New tracker that records before/after hashes and writes rollback manifests. | `186a70605234f6aced47488df26e7cfd2694dc91e306e3de4ef7d4e3c834db59` |
| `aeos/tests/change_tracking/test_change_tracker.py` | New unit tests for create/update/out-of-root tracking behavior. | `75aab4c8714fc9e083eb614a2f9ce349ef7b0905fff68a3d296d32e2f073e4db` |
| `aeos/core/skill_engine/skill_executor.py` | Integrated `ChangeTracker` into `universal-project-factory` scaffold writes and evidence refs. | `fc2712414b9b8890629ebdc7091a5576ece97d541347f74a3eedf0c702e267b3` |
| `aeos/tests/skill_engine/test_skill_executor.py` | Added assertions for change manifest, rollback plan and evidence refs. | `c95b01296f685a7cc5f287b680a102fc95a40784ecb774f41b637f51a7dd345e` |
| `aeos/config/change-tracking.config.yaml` | New fail-closed policy for tracked mutations and rollback metadata. | `45ff531b3c2571162948c7791823b7a339e8ad5e9867cc02beb7a921d4b8b5e6` |
| `aeos/config/agent.runtime.yaml` | Enabled required change tracking in runtime config. | `13cb34f5147c01cbdb6b3d02987281e4613cf962d5330574d688eddca144e01b` |
| `aeos/config/capabilities.yaml` | Added `TRACK_CHANGES`. | `3bc4cdfcb6af912ff10fa51c0a0e2d246d8b4cf64b4f3d30e1d7747cda0b6f2f` |
| `aeos/config/permissions.yaml` | Granted trace/rollback capabilities to relevant governed roles. | `755d4ddfad332022eacd34961f242641bd4a21286de70ae87abbfe68fe3c6b9a` |
| `aeos/skills/core/change-trace-auditor.skill.md` | New Judge-owned skill for auditing change manifests and rollback coverage. | `0ed80f7492713f5f2483be8bdfb89fe9802bc026ca9ff88eeac0e6038dc9da21` |
| `aeos/skills/core/universal-project-factory.skill.md` | Updated contract to require manifest and rollback outputs. | `4e73bb4c50bfcf02545e61370451d36acf0bf7943cd963c8060abbdb4e3b2b8c` |
| `aeos/lcps/zero-to-production.lcp.yaml` | Added LCP rules for generated-file tracking and rollback coverage. | `ed1aed308d93eadf506bdb9259be67060266c05815bdd5003eeb87ec5f293c46` |
| `aeos/playbooks/zero-to-production-project.playbook.md` | Added change trace audit step to the zero-to-production flow. | `5d36f39319d33e171851d34cf192fde2218bb21016e28e37c6f1e111c13f80f4` |
| `aeos/registries/playbooks.registry.yaml` | Registered `change-trace-auditor` in the zero-to-production playbook. | `375c1f773ebb84cdd48ed0164c9368ad3e6353d3acd3ba47d2d79010284a2129` |
| `aeos/registries/skills.registry.yaml` | Registered `change-trace-auditor` and expanded `universal-project-factory` schema. | `b5658c0f9c07425bd43cd3fc5155c5ae50efd712843925475d3eacec3a9cde7b` |

## Rollback Plan

Rollback this change set as a single group.

1. Remove these new files:
   - `aeos/core/change_tracking/__init__.py`
   - `aeos/core/change_tracking/change_tracker.py`
   - `aeos/tests/change_tracking/test_change_tracker.py`
   - `aeos/config/change-tracking.config.yaml`
   - `aeos/skills/core/change-trace-auditor.skill.md`
   - `aeos/docs/change-sets/2026-07-12-change-tracking-rollback.md`
2. Revert only the change-tracking additions in:
   - `aeos/core/skill_engine/skill_executor.py`
   - `aeos/tests/skill_engine/test_skill_executor.py`
   - `aeos/config/agent.runtime.yaml`
   - `aeos/config/capabilities.yaml`
   - `aeos/config/permissions.yaml`
   - `aeos/skills/core/universal-project-factory.skill.md`
   - `aeos/lcps/zero-to-production.lcp.yaml`
   - `aeos/playbooks/zero-to-production-project.playbook.md`
   - `aeos/registries/playbooks.registry.yaml`
   - `aeos/registries/skills.registry.yaml`
3. Re-run the validation commands listed below.

Because the worktree already contained unrelated changes before this change set, do not use a broad reset for rollback. Revert only the files and hunks listed above.

## Validation

Commands executed:

```bash
python -m py_compile aeos/core/change_tracking/change_tracker.py aeos/core/skill_engine/skill_executor.py
python -m aeos.cli.main registry validate
/tmp/aeos-venv/bin/python -m pytest aeos/tests/change_tracking aeos/tests/skill_engine/test_skill_executor.py -q
/tmp/aeos-venv/bin/python aeos/scripts/verify.py --suite full --python /tmp/aeos-venv/bin/python
```

Results:

- Python compile: PASS
- YAML load check: PASS
- Registry validation: PASS, 187 entries across 5 types
- Focused tests: PASS, 11 passed
- Full AEOS verification: PASS
