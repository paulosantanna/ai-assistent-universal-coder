# CVE Report — Continuous Training Pipeline

## Baseline ({{ date }})

### Critical
{% for cve in critical_cves %}
- **{{ cve.id }}** ({{ cve.source }}): {{ cve.description }}
  - Affected: {{ cve.package }} {{ cve.version }}
  - Fix: {{ cve.fixed_in }}
  - Status: {{ cve.status }}
{% endfor %}

### High
{% for cve in high_cves %}
- **{{ cve.id }}** ({{ cve.source }}): {{ cve.description }}
  - Affected: {{ cve.package }} {{ cve.version }}
  - Fix: {{ cve.fixed_in }}
  - Status: {{ cve.status }}
{% endfor %}

### Medium
{% for cve in medium_cves %}
- **{{ cve.id }}** ({{ cve.source }}): {{ cve.description }}
  - Affected: {{ cve.package }} {{ cve.version }}
  - Fix: {{ cve.fixed_in }}
  - Status: {{ cve.status }}
{% endfor %}

### Summary
- Critical: {{ critical_count }} ({{ critical_resolved }} resolved)
- High: {{ high_count }} ({{ high_resolved }} resolved)
- Medium: {{ medium_count }} ({{ medium_resolved }} resolved)
- Low: {{ low_count }} ({{ low_resolved }} resolved)
