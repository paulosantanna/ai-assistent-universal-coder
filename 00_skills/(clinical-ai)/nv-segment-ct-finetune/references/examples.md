# Examples

## Examples

Smoke run on a staged tiny dataset:

```bash
python skills/nv-segment-ct-finetune/scripts/run_finetune.py \
  runs/with_vs_without_nv/_inputs/nv_segment_ct_finetune/input_dataset \
  --smoke \
  --patch-size '[64,64,64]' \
  --output-dir runs/nvseg_smoke
```

Task06 sanity run on a local MSD cache:

```bash
python skills/nv-segment-ct-finetune/scripts/run_finetune.py \
  .workbench_data/datasets/Task06_Lung \
  --sanity \
  --output-dir runs/nvseg_task06_sanity
```

## Out of scope

- MRI generation
- diagnosis
- Megatron training
