<!-- Package: 00_skills/(cloud)/kubernetes-code-context-mapper; relative command/resource examples resolve from that package or workspace root. -->

## 9. Evidence

Use evidence appropriate to the mapping:

- Kubernetes manifests, exported YAML or JSON, events and conditions;
- pod logs and previous container logs when supplied;
- Metrics API or dashboard evidence with query boundaries;
- labels, annotations, selectors and owner references;
- repository file and line references;
- CI, GitOps, Helm or Kustomize metadata;
- OpenTelemetry resource and semantic convention names;
- official references in `references/SOURCES.md`.

Kubernetes labels are grouping tools, not proof of uniqueness. Use selectors, owner references and deployment metadata to confirm mapping.
