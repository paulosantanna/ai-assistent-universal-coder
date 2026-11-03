"""Refusal gate for synthetic voice rendering.

The engine creates original parametric voices. It does not clone a donor,
impersonate a named person, or render sexual content. Child profiles are
acoustic narration presets only.
"""
import re

BLOCKED = re.compile(
    r"("
    r"\bclon(?:e|ar|agem)\b|"
    r"\bimpersonat\w*\b|\bimpersonar\b|\bpersonificar\b|"
    r"\bdeepfake\b|\bfraude?\b|\bgolpe\b|\bscam\b|\bphishing\b|"
    r"\bporn\w*\b|\ber[oó]tic\w*\b|\bsexual\b|\bsexo\b|\bnudes?\b|\bpelad[oa]s?\b|"
    r"\bgroom(?:ing)?\b|\bseduz\w*\b|"
    r"\bvoz\s+do\s+presidente\b|\bvoz\s+da\s+presidente\b|"
    r"\bemergency\s+services?\b|\bsocorro\s+falso\b"
    r")",
    re.IGNORECASE,
)


class VoiceRefusal(Exception):
    """The requested render is outside the engine contract."""

    def __init__(self, reason):
        super().__init__(reason)
        self.reason = reason


def assert_allowed(text, use_context, presentation, age, extra=None):
    """Raise VoiceRefusal when the request asks for cloning, fraud or sexual use."""
    extra = extra or {}
    if extra.get("reference_audio") or extra.get("donor_audio") or extra.get("clone"):
        raise VoiceRefusal("donor-audio-cloning-refused")
    if extra.get("impersonate") or extra.get("target_person"):
        raise VoiceRefusal("impersonation-refused")
    blob = " ".join(str(part or "") for part in (text, use_context, extra.get("notes", "")))
    if BLOCKED.search(blob):
        raise VoiceRefusal("blocked-use-context")
    if presentation not in ("masculine", "feminine"):
        raise VoiceRefusal("unknown-presentation")
    if age not in ("child", "adult", "older"):
        raise VoiceRefusal("unknown-age")
    if age == "child" and not str(use_context or "").strip():
        raise VoiceRefusal("child-profile-needs-nonsexual-use-context")
    return {
        "allowed": True,
        "age": age,
        "presentation": presentation,
        "child_profile": age == "child",
        "policy": "original-parametric-voice; no-donor; no-impersonation; no-sexual-use",
    }
