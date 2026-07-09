DEFAULT_AEOS_THREATS = [
    "prompt_injection",
    "tool_poisoning",
    "mcp_tool_poisoning",
    "secret_leakage",
    "package_tampering",
    "zip_path_traversal",
    "evidence_tampering",
    "approval_forgery",
    "policy_bypass",
    "agent_scope_creep",
    "cache_poisoning",
    "dependency_confusion",
    "unsafe_shell_execution",
    "browser_session_leakage",
]

def build_basic_threat_model():
    return {
        "threats": [{"id": t, "status": "requires_control_validation"} for t in DEFAULT_AEOS_THREATS]
    }
