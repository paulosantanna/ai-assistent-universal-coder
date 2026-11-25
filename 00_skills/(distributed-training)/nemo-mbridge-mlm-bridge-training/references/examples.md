# Examples

## Multi-GPU Examples

### MLM 2-GPU with TP=2

```bash
PYTHONPATH=3rdparty/Megatron-LM:$PYTHONPATH \
uv run python -m torch.distributed.run --nproc_per_node=2 \
  3rdparty/Megatron-LM/pretrain_gpt.py \
  --tensor-model-parallel-size 2 --sequence-parallel \
  --num-layers 4 --hidden-size 256 --num-attention-heads 4 \
  --seq-length 1024 --max-position-embeddings 1024 \
  --micro-batch-size 2 --global-batch-size 16 \
  --train-iters 10 --eval-iters 2 --eval-interval 10 \
  --mock-data --bf16 --use-mcore-models \
  --tokenizer-type NullTokenizer --vocab-size 1024 \
  --lr 1e-4 --log-interval 1
```

### Bridge 2-GPU with TP=2

```bash
rm -rf nemo_experiments && \
uv run python -m torch.distributed.run --nproc_per_node=2 \
  scripts/training/run_recipe.py \
  --recipe vanilla_gpt_pretrain_config \
  model.tensor_model_parallel_size=2 model.sequence_parallel=true \
  model.num_layers=4 model.hidden_size=256 \
  model.num_attention_heads=4 model.ffn_hidden_size=1024 \
  model.seq_length=1024 dataset.seq_length=1024 \
  train.train_iters=10 train.global_batch_size=16 train.micro_batch_size=2 \
  validation.eval_interval=10 validation.eval_iters=2 \
  scheduler.lr_warmup_iters=2 scheduler.lr_decay_iters=10 \
  logger.log_interval=1
```

## Out of scope

- lint and format
- TAO fine-tune
- inference serving
