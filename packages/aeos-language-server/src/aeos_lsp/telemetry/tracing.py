from __future__ import annotations

import json
import logging
import threading
import time
import uuid
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class SpanContext:
    trace_id: str
    span_id: str
    parent_span_id: str | None = None
    baggage: dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "trace_id": self.trace_id,
            "span_id": self.span_id,
            "parent_span_id": self.parent_span_id,
            "baggage": dict(self.baggage),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> SpanContext:
        return cls(
            trace_id=data["trace_id"],
            span_id=data["span_id"],
            parent_span_id=data.get("parent_span_id"),
            baggage=data.get("baggage", {}),
        )


@dataclass
class Span:
    context: SpanContext
    operation_name: str
    start_time: float
    end_time: float | None = None
    status: str = "ok"
    tags: dict[str, Any] = field(default_factory=dict)
    events: list[dict[str, Any]] = field(default_factory=list)
    attributes: dict[str, Any] = field(default_factory=dict)

    def finish(self, status: str = "ok") -> None:
        self.end_time = time.monotonic()
        self.status = status

    def add_event(self, name: str, attributes: dict[str, Any] | None = None) -> None:
        self.events.append({
            "name": name,
            "timestamp": time.monotonic(),
            "attributes": attributes or {},
        })

    def set_tag(self, key: str, value: Any) -> None:
        self.tags[key] = value

    def set_attribute(self, key: str, value: Any) -> None:
        self.attributes[key] = value

    def duration_ms(self) -> float:
        end = self.end_time or time.monotonic()
        return round((end - self.start_time) * 1000, 2)

    def to_dict(self) -> dict[str, Any]:
        return {
            "context": self.context.to_dict(),
            "operation_name": self.operation_name,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "duration_ms": self.duration_ms(),
            "status": self.status,
            "tags": dict(self.tags),
            "events": list(self.events),
            "attributes": dict(self.attributes),
        }


class _SpanStack(threading.local):
    def __init__(self) -> None:
        self.stack: list[Span] = []


class Tracer:
    def __init__(self, service_name: str = "aeos-lsp") -> None:
        self._service_name = service_name
        self._spans: dict[str, Span] = {}
        self._lock = threading.RLock()
        self._local = _SpanStack()
        self._enabled = True

    @property
    def enabled(self) -> bool:
        return self._enabled

    @enabled.setter
    def enabled(self, value: bool) -> None:
        self._enabled = value

    def start_span(
        self,
        operation_name: str,
        parent_context: SpanContext | None = None,
        tags: dict[str, Any] | None = None,
    ) -> Span:
        if not self._enabled:
            return self._create_noop_span(operation_name)

        trace_id = parent_context.trace_id if parent_context else uuid.uuid4().hex[:16]
        parent_span_id = parent_context.span_id if parent_context else None
        span_id = uuid.uuid4().hex[:16]

        if parent_context is None:
            current_span = self._local.stack[-1] if self._local.stack else None
            if current_span is not None:
                trace_id = current_span.context.trace_id
                parent_span_id = current_span.context.span_id

        context = SpanContext(
            trace_id=trace_id,
            span_id=span_id,
            parent_span_id=parent_span_id,
        )

        span = Span(
            context=context,
            operation_name=operation_name,
            start_time=time.monotonic(),
            tags=tags or {},
        )

        with self._lock:
            self._spans[span_id] = span

        self._local.stack.append(span)
        logger.debug("Started span: %s (%s)", operation_name, span_id)
        return span

    def end_span(self, span: Span | None = None, status: str = "ok") -> None:
        if span is None:
            if self._local.stack:
                span = self._local.stack.pop()
            else:
                return
        else:
            if self._local.stack and self._local.stack[-1].context.span_id == span.context.span_id:
                self._local.stack.pop()

        span.finish(status)
        logger.debug("Ended span: %s (%s, %s)", span.operation_name, span.context.span_id, status)

    def current_span(self) -> Span | None:
        if self._local.stack:
            return self._local.stack[-1]
        return None

    def current_context(self) -> SpanContext | None:
        span = self.current_span()
        return span.context if span is not None else None

    def inject_headers(self, span: Span | None = None) -> dict[str, str]:
        ctx = span.context if span else self.current_context()
        if ctx is None:
            return {}
        return {
            "X-Trace-Id": ctx.trace_id,
            "X-Span-Id": ctx.span_id,
            "X-Parent-Span-Id": ctx.parent_span_id or "",
        }

    def extract_from_headers(self, headers: dict[str, str]) -> SpanContext | None:
        trace_id = headers.get("X-Trace-Id")
        span_id = headers.get("X-Span-Id")
        parent_span_id = headers.get("X-Parent-Span-Id")

        if trace_id and span_id:
            return SpanContext(
                trace_id=trace_id,
                span_id=span_id,
                parent_span_id=parent_span_id or None,
            )
        return None

    def get_span(self, span_id: str) -> Span | None:
        with self._lock:
            return self._spans.get(span_id)

    def get_trace_spans(self, trace_id: str) -> list[Span]:
        with self._lock:
            return [s for s in self._spans.values() if s.context.trace_id == trace_id]

    def trace_as_tree(self, trace_id: str) -> list[dict[str, Any]]:
        spans = self.get_trace_spans(trace_id)
        span_map: dict[str, dict[str, Any]] = {}
        roots: list[dict[str, Any]] = []

        for s in spans:
            node = {
                **s.to_dict(),
                "children": [],
            }
            span_map[s.context.span_id] = node

        for s in spans:
            node = span_map[s.context.span_id]
            parent_id = s.context.parent_span_id
            if parent_id and parent_id in span_map:
                span_map[parent_id]["children"].append(node)
            else:
                roots.append(node)

        return roots

    def flush(self) -> list[dict[str, Any]]:
        with self._lock:
            snapshot = [s.to_dict() for s in self._spans.values()]
            self._spans.clear()
        return snapshot

    def _create_noop_span(self, operation_name: str) -> Span:
        return Span(
            context=SpanContext(
                trace_id="",
                span_id="",
            ),
            operation_name=operation_name,
            start_time=time.monotonic(),
        )

    def __repr__(self) -> str:
        return f"Tracer(service={self._service_name}, enabled={self._enabled}, spans={len(self._spans)})"
