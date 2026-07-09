from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class BaseToolAdapter(ABC):
    tool_id: str = ""

    @abstractmethod
    def execute(self, action: str, resource: str, input_data: dict[str, Any]) -> dict[str, Any]:
        ...
