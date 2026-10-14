# TLC skill standardization

Updated: 2026-10-12
Owner: codenavi-agent
Status: COMPLETE — installation verified; provider execution remains outside scope.

## User outcome

Use every image in Drive folder `1C_hF0erTB2ou1j58uKUcedsrE2tk4vY7` to remake all universal-coder skills following the pictured order, directories and TLC pattern. Every SKILL.md must have at most 100 physical lines; details belong inside that skill. Include every current skill from https://agent-skills.techleads.club/skills/.

## Requirements and acceptance

| ID | Requirement | Evidence gate |
| --- | --- | --- |
| TLC-01 | Account for every source image in filename order. | Eight complete provider pages; 770 downloaded IDs; 389 distinct SHA-256 hashes; every unique image has OCR and a source-topic record. |
| TLC-02 | Follow the photographed category/skill/resource hierarchy. | Canonical skills in `00_skills/(category)/slug/`; frontmatter identifies the folder; required name/description/license/author/version and local module links. |
| TLC-03 | All active workspace SKILL.md files have <=100 physical lines. | Deterministic inventory includes canonical and discovery/compatibility entries; no line packing or discarded operative sections. |
| TLC-04 | Include the complete TLC catalog and its resources. | All 92 registry entries from upstream commit `6df68d52028b9261058231e0f4998048c0352f45` map to installed packages; source file hashes and attribution retained. |
| TLC-05 | Preserve existing operational contracts and users' changes. | Compare migration with byte-hashed baseline; preserve existing scripts/templates/resources and pre-existing deletions; adapt pointers and retain compatibility entries. |
| TLC-06 | Improve discovery and progressive disclosure. | Descriptions have concrete outcomes, real triggers and exclusions; lengthy contracts split on Markdown sections with local links and load conditions. |
| TLC-07 | Preserve single-agent governance and runtime secret boundaries. | Every active contract inherits AGENTS.md; source profiles become internal lenses; source provenance cannot grant execution authority. |
| TLC-08 | Verify observable installation/discovery. | Run real structural validator, CLI inventory/discovery and representative existing skill scripts; distinguish inherited missing-runtime failures from new failures. |

## Design

- Keep the complete source snapshot as provenance, not as a new governing agent.
- Canonical root is `00_skills`, explicitly selected by the user as pictured. The user also confirmed that external deletions must be preserved.
- Source catalog category and folder spellings are preserved; original catalog names remain aliases when upstream name and folder differ.
- Existing collision packages keep their local operation rules; current TLC source/resources are accessible within the same package with explicit precedence.
- Split large Markdown only outside fenced blocks, preserve section ordering and fix links relative to the module's new location.
- External provider operations, deployments, source resource installation and paid tools are not executed by this packaging mission.
- No blanket git reset/checkout; no restored aeos tree. Baseline router discovery was zero; the external reorganization subsequently removed runtime/scripts/references/templates. New instruction discovery uses the canonical catalog and native entries.

## Verified result

All installation gates passed: 301 active packages, all 92 TLC packages/777 source resources, 770 image IDs/389 unique hashes in order, 824 entrypoints with maximum 99 physical lines and 2,742 resolved local links. Skill-architect reports zero errors/warnings across all active packages. ADR and ADL CLI outputs match the preserved pre-migration scripts. Tests-expert recorded PASS for the frozen user-request installation charter. Evidence and actual limits: `00_skills/VERIFICATION.md`, `00_skills/validation.report.json`; photographed requirements now live at `00_skills/STANDARD.md` because the external root references directory was removed.

## Verification applicability

- REQUIRED: catalog coverage, physical line cap, YAML/frontmatter, local references, source integrity, legacy entry resolution, real discovery surface.
- REQUIRED when script paths change: run existing functional script fixtures that exercise those paths.
- NOT_APPLICABLE: deploying clouds, sending marketing/email, compiling every technology example, paid-media generation or clinical simulation. Those capabilities remain dependent on actual tools and authorized inputs.
- User-facing structural work is authorized by this request. No production, publication or irreversible mutation is in scope.

## Rollback

Use the migration manifest and pre-change backup under ignored `.tools/tlc-migration/`; undo only mission-owned files/moves. Preserve all pre-existing modifications and deletions. Never reset the whole working tree.
