# Examples

## Examples

Validate and stage a preflight finetune check from an input bundle (the recommended first step — no GPU, no training). This is the single canonical command; replace `INPUT_BUNDLE` and `OUT_DIR` with your paths:

```bash
export NV_GENERATE_ROOT="${NV_GENERATE_ROOT:-$HOME/.cache/nvidia-skills/upstreams/NV-Generate-CTMR-da438fe}" && \
python skills/nv-generate-mr-brain-finetune/scripts/run_mr_brain_finetune.py \
  INPUT_BUNDLE/preflight_datalist.json \
  --data-base-dir INPUT_BUNDLE/preflight_dataset \
  --output-dir OUT_DIR \
  --modality mri_t1 \
  --preflight
```

For real GPU finetuning and other variations, see [Usage](#2-usage-one-line-training) below.

Command-shape review for a requested training launch (no setup or execution):

```bash
python skills/nv-generate-mr-brain-finetune/scripts/run_mr_brain_finetune.py \
  PATH_TO_DATALIST.json \
  --data-base-dir PATH_TO_DATA_ROOT \
  --output-dir runs/nv_generate_mr_brain_finetune \
  --epochs 2 \
  --modality mri_t1
```

## Out of scope

- CT segmentation
- inference-only generation
- clinical approval
