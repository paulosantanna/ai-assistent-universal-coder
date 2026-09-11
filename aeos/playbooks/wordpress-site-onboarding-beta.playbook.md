# Playbook: wordpress-site-onboarding-beta

## Objective

Establish the first and only full Beta baseline for an authorized remote WordPress site, using current WordPress knowledge and without mutating production content/configuration.

## Required Agent

- `codenavi-agent` only.

## Required Skill

- `wordpress-expert`

## Required MCP

- `wordpress-expert`

## Steps

1. Load root governance and continuity state.
2. Confirm site URL, authorization scope and that the mission is read-only onboarding.
3. Consult `wordpress.knowledge.source_policy` and relevant official WordPress documentation.
4. Run `wordpress.site.map_status`.
5. If the Beta map already exists, return `REUSED` and stop full mapping.
6. If absent, run `wordpress.site.discover` to validate reachability/capability surface.
7. Run `wordpress.site.map_beta`; this is the only full baseline creation event.
8. Verify persisted fingerprint/map hash and confirm no secret values are present.
9. Generate a concise architecture/capability summary for later missions.
10. Record evidence and debrief.

## Mapping scope

- REST namespaces/routes and capability discovery;
- WordPress version hint when exposed;
- content types;
- active theme metadata when available;
- plugin metadata when authorized;
- safe settings metadata;
- templates, template parts, navigation and Site Editor surfaces;
- advertised Abilities API surface when present;
- authentication/capability mode without credentials.

## Prohibited

- production writes;
- password/token/cookie persistence;
- user/customer/order data ingestion;
- arbitrary crawling outside approved WordPress sources;
- overwriting an existing Beta baseline.

## Terminal states

- `PASS/CREATED`: first Beta map created and verified.
- `PASS/REUSED`: map already existed; no remap occurred.
- `BLOCKED`: authorization, connectivity, required evidence or safe persistence failed.
