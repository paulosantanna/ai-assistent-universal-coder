# Examples

## Examples

### TP plus PP for a large multi-node model

Recommend `strategy: fsdp2`. Mention `tp_size`, `pp_size`, `cp_size`,
`ep_size`, and the `pipeline` sub-config. State that `dp_size` is inferred from
`world_size / (tp_size * pp_size * cp_size)`.

```yaml
distributed:
  strategy: fsdp2
  tp_size: 8
  pp_size: 4
  cp_size: 1
  ep_size: 1
  pipeline:
    pp_schedule: interleaved1f1b
    pp_microbatch_size: 1
```

### MoE expert parallelism

Recommend `strategy: fsdp2` with `ep_size > 1`. Say this creates a separate
`moe_mesh`; include the `moe` sub-config when relevant; state that `ep_size`
must divide `dp_size * cp_size`. Do not recommend `megatron_fsdp` or `ddp`.

```yaml
distributed:
  strategy: fsdp2
  ep_size: 8
  moe:
    reshard_after_forward: false
```

### MegatronFSDP limitations

Say no for pipeline parallelism, expert parallelism, and `sequence_parallel`.
Recommend `fsdp2` for PP, EP, or `sequence_parallel`; mention that DDP is only
simple data parallelism.


### Example (8B model on 8 GPUs, PP=2 + DP=4)

```yaml
distributed:
  strategy: fsdp2
  pp_size: 2

  pipeline:
    pp_schedule: interleaved1f1b
    pp_microbatch_size: 4
    scale_grads_in_schedule: false

checkpoint:
  model_save_format: safetensors
  save_consolidated: final
```


### Full MoE example (Qwen3-30B-A3B on 8 GPUs)

```yaml
distributed:
  strategy: fsdp2
  tp_size: 1
  cp_size: 1
  pp_size: 1
  ep_size: 8
  sequence_parallel: false
  activation_checkpointing: true
```

## Out of scope

- Megatron-LM lint
- TAO fine-tune
- RAG serving
