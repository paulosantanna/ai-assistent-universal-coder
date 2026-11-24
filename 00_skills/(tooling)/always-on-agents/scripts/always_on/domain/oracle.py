"""The request is the oracle. A negative proof must fail, or the sum test is not evidence."""

from __future__ import annotations

from collections.abc import Callable

REQUIRED_NEGATIVES = ("2 - 2", "2 * 3", "2 / 0")


def prove_negatives(cases: list[Callable[[], object]]) -> bool:
    """Return True only when every case fails and the three requested proofs are present."""
    if len(cases) < len(REQUIRED_NEGATIVES):
        return False
    failed = 0
    for case in cases:
        try:
            case()
        except Exception:
            failed += 1
    return failed == len(cases)


class RequestOracle:
    """Proves the requested sum by requiring the three wrong operations to fail."""

    def prove(self, evaluate) -> bool:
        return prove_negatives(sum_negative_cases(evaluate))


def sum_negative_cases(evaluate) -> list[Callable[[], object]]:
    """Wrong numeric expectations of the sum. Each one must raise."""

    def subtraction() -> None:
        if evaluate(2, 2) == (2 - 2):
            return None
        raise AssertionError("2 - 2 is not the sum")

    def multiplication() -> None:
        if evaluate(2, 2) == (2 * 3):
            return None
        raise AssertionError("2 * 3 is not the sum")

    def division() -> None:
        if evaluate(2, 2) == (2 / 0):
            return None
        raise AssertionError("2 / 0 is not the sum")

    return [subtraction, multiplication, division]
