# Architecture Decision Log Policy

The log is append-only: never delete records, never reuse numbers and never rewrite accepted decisions. Writes are limited to record status lines and the marked index block inside the log directory. Commits require explicit approval.
