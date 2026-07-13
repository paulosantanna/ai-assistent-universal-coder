# Continuous Training Maintenance Report

## Execution: {{ execution_id }}

### Summary
- **Date**: {{ timestamp }}
- **Intent**: {{ intent }}
- **Status**: {{ status }}

### Baseline
- CVEs found: {{ baseline_cves }}
- SAST findings: {{ baseline_sast }}
- Tests passing: {{ baseline_tests_passed }}
- Tests failing: {{ baseline_tests_failed }}

### Changes Made
{% for change in changes %}
- `{{ change.file }}`: {{ change.description }} (SHA256: {{ change.sha256_after }})
{% endfor %}

### Results
- CVEs resolved: {{ cves_resolved }} / {{ cves_found }}
- SAST findings resolved: {{ sast_resolved }} / {{ sast_findings }}
- Tests passing: {{ final_tests_passed }}
- Tests failing: {{ final_tests_failed }}

### Rollback Snapshot
- **Ref**: {{ rollback_ref }}

### Remaining Risks
{% for risk in risks %}
- **{{ risk.severity }}**: {{ risk.description }}
{% endfor %}

### Lessons Learned
{% for lesson in lessons %}
- [{{ lesson.type }}] {{ lesson.description }}
{% endfor %}

### Next Steps
{{ next_steps }}
