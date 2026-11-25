# Examples

## Examples

Command-shape review only (no setup or execution):

```bash
python skills/nv-generate-mr-brain/scripts/run_mr_brain.py \
  PATH_TO_MR_BRAIN_CONFIG.json \
  --output-dir runs/nv_generate_mr_brain_demo \
  --modality mri_t1 \
  --random-seed 1234
```

For an executable run, use the setup-aware command under
[Usage](#usage).

## Out of scope

- clinical diagnosis
- CT segmentation
- real PHI training approval
