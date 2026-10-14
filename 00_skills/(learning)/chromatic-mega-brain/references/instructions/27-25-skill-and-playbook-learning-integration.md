<!-- Package: 00_skills/(learning)/chromatic-mega-brain; relative command/resource examples resolve from that package or workspace root. -->

## 25. Skill and playbook learning integration

The Chromatic Mega Brain owns the repository-wide integration index for skills and playbooks.

Use `scripts/chromatic_brain.py sync-integration --workspace-root . --output-dir 00_skills/(learning)/chromatic-mega-brain/memory` after adding, removing or materially changing any skill or playbook.

The generated index must record, for every discovered `SKILL.md`, `playbook.yaml` and `*.playbook.yaml`:

- entity type;
- entity id;
- source path;
- Chromatic entrypoint;
- memory scope;
- do guidance;
- do_not guidance;
- evidence references.

Do not treat the generated index as promoted institutional knowledge. It is candidate learning until Judge or Knowledge Curator validation.
