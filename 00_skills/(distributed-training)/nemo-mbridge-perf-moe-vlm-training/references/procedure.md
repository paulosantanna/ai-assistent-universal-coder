# Procedure

## Contents

- TLC gates
- Adapted upstream instructions
- Upstream modules

## TLC gates

These gates win when the adapted text disagrees.

- Confirm account, partition, node count, and the exact command before sbatch, torchrun on a shared cluster, or a container launch.
- Measured tables in the upstream text are NVIDIA point-in-time reports. Re-read the checkout and do not present them as results from this workspace.
- A destructive delete runs only when the user names the generated path and it sits inside the authorized work tree.
- Missing source, tool, permission, or checkout blocks the dependent step. Continue only independent authorized work.
- Do not create another agent identity. A role in the upstream text is a lens of `codenavi-agent`.

## Adapted upstream instructions

Upstream measured numbers below are point-in-time NVIDIA reports. Re-read the checkout before copying a flag, and do not report them as results from this workspace.

# MoE VLM Training

Stable docs: @docs/training/moe-optimization.md
Card: @skills/nemo-mbridge-perf-moe-vlm-training/card.yaml

## FSDP vs 3D Parallel

| Approach | Strength | Best fit |
|---|---|---|
| FSDP | Simplest path to a working multimodal run | first bring-up, memory-first tuning, awkward PP boundaries |
| 3D parallel | Higher ceiling after tuning | stable models with a clean PP layout and time for deeper sweeps |

For MoE VLMs, the practical workflow is usually:

1. get the first reliable run with FSDP
2. stabilize real-data input, recompute, and memory behavior
3. move to 3D parallel only if the throughput headroom is worth the extra work

## Rounded Findings From Recent VLM Runs

### Qwen3-VL class models

The main patterns were consistent across the tracker:

- FSDP on GB200-class systems can already reach healthy high-teens utilization
  with a comparatively simple setup
- B200 FSDP runs are viable, but more sensitive to recompute choice and frozen
  vision settings
- 3D parallel can recover to a similar or better operating point, but only after
  tuning MBS, recompute, and the real vision path together

### Real data vs mock data

Mock-data VLM runs are not trustworthy performance proxies. In the experiments,
image-free mock runs looked closer to "roughly twice as fast" than "slightly
optimistic" when compared with real multimodal input.

Use real or realistic image payloads before drawing any conclusion about VLM
throughput.

### Smaller multimodal MoE runs

The smaller Qwen3.5-style multimodal experiments reinforce the same lessons:

- HybridEP is a solid default on GB200
- TE-scoped CUDA graphs help once the training loop is stable
- larger MBS can pay off, but only if the vision encoder does not become the
  next bottleneck

## Decision Guide

### Choose FSDP when

- you are bringing up a new VLM for the first time
- the model has awkward stage boundaries across embedding, vision, and decoder
- memory fit matters more than absolute throughput
- you may freeze the vision stack during decoder-focused tuning

### Choose 3D parallel when

- the model is already stable under FSDP
- the PP layout is clear and repeatable
- you can sweep MBS, recompute, and CUDA-graph scope together
- the goal is best steady-state throughput, not easiest bring-up

## Key Tuning Knobs

1. **Freeze the vision stack when appropriate**: if the work is decoder-focused,
   freezing the vision side often gives a small but real throughput gain and
   reduces memory pressure.

2. **Sweep MBS aggressively**: VLMs are more MBS-sensitive than text-only MoE
   runs because the vision path changes the compute-to-overhead balance.

3. **Prefer selective recompute once the model fits**: full recompute is a
   useful bring-up tool, but selective recompute is usually the better steady
   state.

4. **Match CUDA-graph scope to the workload**: `attn moe_router moe_preprocess`
   is the safer MoE default, while narrower scopes can still be useful for
   controlled experiments.

5. **Use ETP only when EP alone is insufficient**: it can unlock a layout, but
   it also introduces more communication and more tuning surface.

## Representative Config Families

### FSDP-first GB200 path

```text
TP=1  CP=1  PP=1
EP sized to the expert topology, often large
Dispatcher: HybridEP on GB200-class systems
Recompute: start with full, then relax toward selective recompute
```

### 3D-parallel GB200 path

```text
TP=1  CP=1  PP=1 or modest PP
EP and ETP sized to the expert topology
Dispatcher: HybridEP
CUDA Graph: start narrow, then widen only after the real-data path is stable
```

## Compatibility

| Feature | FSDP | 3D parallel |
|---|---|---|
| HybridEP on GB200 | strong default | strong default once topology is stable |
| CUDA graphs | useful after bring-up | useful, but more scope-sensitive |
| Freeze vision | natural fit | possible, but less often used as the headline perf path |
| Selective recompute | recommended | recommended |

## Pitfalls

1. **Mock multimodal data is misleading**: it can make the decoder look much
   healthier than the real end-to-end VLM path.

2. **The vision encoder can dominate unexpectedly**: profile encoder, projector,
   and decoder separately before attributing everything to the dispatcher.

3. **Do not compare FSDP and 3D-parallel runs with different effective work**:
   normalize by useful tokens and workload shape, not only by step time.

4. **ETP is not free**: use it as a fit or topology tool, not as the default.

5. **Recompute and CUDA-graph choices are coupled**: the setting that gets the
   model to fit is often not the setting that gives the best steady-state speed.

## Upstream modules

Read a module only when the request matches that mode.

- No additional upstream notes were part of this package.
