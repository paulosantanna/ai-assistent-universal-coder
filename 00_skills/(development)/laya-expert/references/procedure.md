# Technical procedure
Updated: 2026-10-15
Entry point: ../SKILL.md.

## Typed inference
choice selects an allowlisted criterion, score predicts an ordinal distribution and noul represents a binary judgment. Validate question schemas and preserve probabilities. Treat the rendered question/options as part of the token budget. Check each checkpoint's config; long-context claims do not establish accuracy on your data.

## SDK and MCP
Use laya.load/Router and documented prediction APIs; inspect installed signatures. The upstream MCP exposes typed tools and can share an HTTP serving runtime. Shortlist/tournament availability differs between local and remote modes. Do not recreate the decision model or invent generation capabilities. Never use decision confidence as authorization.

## Training and calibration
Use laya.train.finetune with TrainConfig. Scalar labels belong in JSONL {state,questions,expected}; gold requires per-question probability distributions. Use the installed dry_run preprocessing before training and reject skipped/invalid targets. Verify labels and per-type sample balance. RLCD and soft-ce are distinct configured objectives. Preserve encoder/head learning rates, seed, state/head limits, option layout, augmentation, calibration split and hardware. Fit temperature/abstention only on permitted calibration data; a tiny sample is an explicit limitation.

## Evaluation
Report choice accuracy, ordinal errors and ECE/Brier where probabilities support them, alongside throughput/latency and abstention coverage/risk. Compare base and candidate on identical questions, including shuffled options, multilingual text and uncertain/irrelevant candidates. Synthetic labels and manual trigger inspection are not measured deployment accuracy.
