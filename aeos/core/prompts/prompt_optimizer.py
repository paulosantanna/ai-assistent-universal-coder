class PromptOptimizer:
    def optimize(self, goal: str, constraints: list[str], output_schema: dict) -> str:
        return f"""
Objective:
{goal}

Constraints:
{chr(10).join('- ' + c for c in constraints)}

Output schema:
{output_schema}

Stop if:
- required evidence is missing;
- permission is denied;
- policy is denied;
- secret appears in output;
- tool access is not routed through Tool Router.
""".strip()
