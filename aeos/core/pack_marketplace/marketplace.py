class PackMarketplace:
    """
    Local pack marketplace controller.

    Packs must flow:
    quarantine -> staging -> active

    Direct import to active is forbidden.
    """

    valid_transitions = {
        "quarantine": {"staging", "rejected"},
        "staging": {"active", "archived", "rejected"},
        "active": {"archived"},
        "archived": set(),
        "rejected": set(),
    }

    def can_transition(self, current: str, target: str) -> bool:
        return target in self.valid_transitions.get(current, set())
