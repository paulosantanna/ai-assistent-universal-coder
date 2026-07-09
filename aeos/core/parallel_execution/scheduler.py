class DeterministicParallelScheduler:
    """
    Creates deterministic execution groups from a task graph.

    This skeleton groups tasks only after conflict detection has passed.
    """

    def __init__(self, max_parallel_steps: int = 4):
        self.max_parallel_steps = max_parallel_steps

    def schedule(self, ready_steps: list[str]) -> list[list[str]]:
        ordered = sorted(ready_steps)
        return [
            ordered[i:i + self.max_parallel_steps]
            for i in range(0, len(ordered), self.max_parallel_steps)
        ]
