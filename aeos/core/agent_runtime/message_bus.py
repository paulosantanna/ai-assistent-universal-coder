from __future__ import annotations

from typing import Any, Optional

from aeos.core.agent_runtime.agent_models import AgentMessage


class MessageBus:
    def __init__(self):
        self._messages: list[AgentMessage] = []
        self._ack_map: dict[str, bool] = {}

    def send(self, message: AgentMessage) -> str:
        self._messages.append(message)
        if message.requires_ack:
            self._ack_map[message.message_id] = False
        return message.message_id

    def ack(self, message_id: str) -> bool:
        if message_id in self._ack_map:
            self._ack_map[message_id] = True
            return True
        return False

    def is_acked(self, message_id: str) -> bool:
        return self._ack_map.get(message_id, True)

    def get_messages_for_agent(self, agent_id: str) -> list[dict[str, Any]]:
        return [
            m.to_dict() for m in self._messages
            if m.to_agent == agent_id or m.to_agent is None
        ]

    def get_messages_by_task(self, task_id: str) -> list[dict[str, Any]]:
        return [m.to_dict() for m in self._messages if m.task_id == task_id]

    def get_all_messages(self) -> list[dict[str, Any]]:
        return [m.to_dict() for m in self._messages]

    def clear(self) -> None:
        self._messages.clear()
        self._ack_map.clear()
