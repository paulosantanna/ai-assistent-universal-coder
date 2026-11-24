"""Sum is the bounded context of the request 'faça uma calculadora somar 2 + 2'."""

from __future__ import annotations


class UnsupportedOperation(Exception):
    """Subtraction, multiplication and division are outside the requested sum."""


class Sum:
    @staticmethod
    def evaluate(left: int, right: int) -> int:
        return left + right

    @staticmethod
    def evaluate_operation(name: str, left: int, right: int) -> int:
        if name == "add":
            return left + right
        if name == "div" and right == 0:
            raise ZeroDivisionError("2 / 0 is not the requested sum")
        raise UnsupportedOperation(name)
