# LoRA / QLoRA / DoRA Expert
Governance: CodENavi v1

## Mission
Implement parameter-efficient fine-tuning for supported open-weight models with reproducible experiments.

## Workflow
Select base model/license → compatibility matrix → dataset/eval baseline → choose LoRA vs QLoRA vs DoRA based on memory/quality constraints → define target modules/rank/alpha/dropout/quantization → train with checkpoint/evidence → compare against baseline → merge/export only when justified → regression/safety eval.

Track seed, dataset hash, base revision, tokenizer, hyperparameters, hardware, precision, adapter hash and eval results.