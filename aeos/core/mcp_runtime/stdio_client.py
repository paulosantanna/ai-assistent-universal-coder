class StdioMCPClient:
    """
    Placeholder for stdio MCP client.

    Security requirements before production use:
    - command allowlist;
    - cwd isolation;
    - env allowlist;
    - timeout;
    - input schema validation;
    - output schema validation;
    - redaction;
    - evidence logging.
    """

    def __init__(self, command: str, args=None, cwd=None, env=None, timeout_seconds: int = 30):
        self.command = command
        self.args = args or []
        self.cwd = cwd
        self.env = env or {}
        self.timeout_seconds = timeout_seconds

    def call(self, method: str, params: dict) -> dict:
        raise NotImplementedError("Real stdio MCP transport must be implemented behind ToolRouter only.")
