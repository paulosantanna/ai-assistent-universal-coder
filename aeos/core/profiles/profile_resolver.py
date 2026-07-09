class ProfileResolver:
    def __init__(self, profiles: list[dict]):
        self.profiles = profiles

    def resolve(self, indicators: list[str]) -> dict:
        scored = []
        indicator_set = set(indicators)
        for profile in self.profiles:
            required = set(profile.get("indicators", []))
            score = len(required.intersection(indicator_set))
            scored.append((score, profile))
        scored.sort(key=lambda item: item[0], reverse=True)
        if not scored or scored[0][0] == 0:
            return {"id": "generic", "confidence": 0.0, "reason": "no_profile_indicators"}
        best = scored[0][1]
        return {"id": best.get("id"), "confidence": min(1.0, scored[0][0] / max(1, len(best.get("indicators", []))))}
