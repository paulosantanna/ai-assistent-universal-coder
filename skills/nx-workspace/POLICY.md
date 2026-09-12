# Nx Workspace Policy

- read_only: `nx show` / graph inspection.
- medium: local `nx.json`, project config, cache and boundary changes.
- high: CI workflow edits; use DevOps pipeline gates.
- destructive: remote cache credentials, force-push, production deploy — explicit approval.

Do not persist Nx Cloud or registry tokens in the repo or notebook.
