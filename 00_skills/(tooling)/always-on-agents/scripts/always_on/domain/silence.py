"""Stdout is questions only. Plans and progress belong in files, not the transcript."""

from __future__ import annotations

import re

NARRATION = re.compile(
    r"(\bi will\b|\bi'll\b|\blet me\b|\bvou \b|\bplano\b|\bnext i\b|\bfirst,\b|\bhere's the plan\b|\bhere is the plan\b)",
    re.IGNORECASE,
)


def writer_is_silent(stdout: str) -> bool:
    for line in (stdout or "").splitlines():
        text = line.strip()
        if not text:
            continue
        if text.startswith("QUESTION:"):
            continue
        return False
    return True


def narration_present(stdout: str) -> bool:
    return bool(NARRATION.search(stdout or ""))
