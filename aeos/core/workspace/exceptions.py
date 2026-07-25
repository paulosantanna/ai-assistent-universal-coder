class WorkspaceError(Exception):
    """Base exception for workspace operations."""

class RevisionConflictError(WorkspaceError):
    """Raised when an operation observes a stale revision."""
    def __init__(self, message: str, expected_revision: int | None = None, actual_revision: int | None = None):
        self.expected_revision = expected_revision
        self.actual_revision = actual_revision
        super().__init__(message)
