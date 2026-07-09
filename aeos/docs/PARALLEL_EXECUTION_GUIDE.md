# Parallel Execution Guide

## Implement only after

- Task Graph exists.
- Agent Runtime exists.
- Evidence Store exists.
- Judge exists.
- Permission/Policy decisions are logged.
- Read/write set detection exists.

## Safe initial parallel steps

- stack detection;
- documentation inspection;
- dependency file reading;
- git status/diff read-only;
- package inspection.

## Unsafe parallel steps

- patch apply;
- package extraction;
- git mutation;
- test runner against same workspace;
- evidence manifest writing without lock;
- hash-chain writing without order control.
