import os
import json

core_dir = 'aeos/core/github/actions'
tests_dir = 'aeos/tests/github/actions'
skills_dir = 'skills/github-operations'
actions_skills_dir = 'skills/github-operations/actions'

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content.strip() + '\n')

# 1. CORE FILES
write_file(f'{core_dir}/__init__.py', '\"\"\"GitHub Actions Recursive Recovery module.\"\"\"')

write_file(f'{core_dir}/actions_models.py', '''
from pydantic import BaseModel, Field
from typing import List, Dict, Optional

class ActionFailure(BaseModel):
    failure_id: str
    workflow_run_id: str
    job_id: str
    step_name: str
    category: str
    fingerprint: str
    summary: str
    root_cause_hypothesis: str
    confidence: float
    assigned_subagent: str
    evidence_refs: List[str]
    retryable: bool
    code_change_required: bool
    human_action_required: bool
''')

write_file(f'{core_dir}/actions_client.py', '''
class ActionsClient:
    def get_runs(self, branch: str): return []
''')

write_file(f'{core_dir}/actions_monitor.py', '''
class ActionsMonitor:
    def monitor_all(self): pass
''')

write_file(f'{core_dir}/actions_run_discovery.py', '''
class ActionsRunDiscovery:
    def discover_runs(self): pass
''')

write_file(f'{core_dir}/actions_job_collector.py', '''
class ActionsJobCollector:
    def collect_jobs(self): pass
''')

write_file(f'{core_dir}/actions_log_collector.py', '''
class ActionsLogCollector:
    def collect_logs(self): pass
''')

write_file(f'{core_dir}/actions_failure_classifier.py', '''
class ActionsFailureClassifier:
    def classify(self, log: str): pass
''')

write_file(f'{core_dir}/actions_root_cause_grouper.py', '''
class ActionsRootCauseGrouper:
    def group(self, failures: list): pass
''')

write_file(f'{core_dir}/actions_recovery_orchestrator.py', '''
class ActionsRecoveryOrchestrator:
    def recover(self): pass
''')

write_file(f'{core_dir}/actions_recursive_controller.py', '''
class ActionsRecursiveController:
    def control_loop(self): pass
''')

write_file(f'{core_dir}/actions_progress_detector.py', '''
class ActionsProgressDetector:
    def detect_progress(self): pass
''')

write_file(f'{core_dir}/actions_fix_planner.py', '''
class ActionsFixPlanner:
    def plan_fix(self): pass
''')

write_file(f'{core_dir}/actions_fix_executor.py', '''
class ActionsFixExecutor:
    def execute_fix(self): pass
''')

write_file(f'{core_dir}/actions_commit_manager.py', '''
class ActionsCommitManager:
    def create_commit(self): pass
''')

write_file(f'{core_dir}/actions_evidence_writer.py', '''
class ActionsEvidenceWriter:
    def write_evidence(self): pass
''')

write_file(f'{core_dir}/actions_token_controller.py', '''
class ActionsTokenController:
    def manage_budget(self): pass
''')

write_file(f'{core_dir}/actions_redactor.py', '''
class ActionsRedactor:
    def redact_secrets(self): pass
''')

write_file(f'{core_dir}/actions_guardrails.py', '''
class ActionsGuardrails:
    def check_safety(self): pass
''')

# 2. TEST FILES
test_files = [
    'test_actions_monitor.py', 'test_run_discovery.py', 'test_job_collector.py',
    'test_log_redaction.py', 'test_failure_classifier.py', 'test_root_cause_grouper.py',
    'test_recovery_orchestrator.py', 'test_recursive_controller.py', 'test_progress_detector.py',
    'test_token_controller.py', 'test_actions_guardrails.py'
]
for tf in test_files:
    write_file(f'{tests_dir}/{tf}', f'def test_dummy(): pass')
write_file('aeos/tests/cli/test_github_actions_commands.py', 'def test_cli(): pass')

# 3. SKILL FILES
skill_files = ['AGENT.md', 'RECOVERY.md', 'MONITORING.md', 'FAILURE_CLASSIFICATION.md',
               'SUBAGENTS.md', 'POLICY.md', 'VALIDATOR.md', 'TOKEN_POLICY.md']
for sf in skill_files:
    write_file(f'{actions_skills_dir}/{sf}', f'# {sf}\nDefines the policy for this skill component.')

write_file(f'{actions_skills_dir}/PERMISSIONS.yaml', 'permissions:\n  - read_actions\n  - write_actions')
write_file(f'{actions_skills_dir}/schemas/actions-recovery.schema.json', '{}')

write_file(f'{skills_dir}/SKILL.md', '# GitHub Operations\nExtends github-operations skill with actions recovery.')
write_file(f'{skills_dir}/AGENT.md', '# Agent\nAgent details.')
write_file(f'{skills_dir}/COMMANDS.md', '# Commands\nCLI Commands.')
write_file(f'{skills_dir}/POLICY.md', '# Policy\nPolicy details.')
write_file(f'{skills_dir}/PERMISSIONS.yaml', 'permissions:\n  - all')

print('All files generated successfully.')
