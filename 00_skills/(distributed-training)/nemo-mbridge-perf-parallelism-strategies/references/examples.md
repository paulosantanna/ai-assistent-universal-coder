# Examples

### Examples

| Config | Wrong (PP·TP·CP·EP·ETP) | Correct (PP·max(TP·CP, EP·ETP)) |
|---|---|---|
| PP=1, TP=2, CP=1, EP=8, ETP=1 | 16 | **8** (1 node) |
| PP=1, TP=4, CP=1, EP=8, ETP=1 | 32 | **8** (max(4, 8)) |
| PP=1, TP=2, CP=2, EP=8, ETP=1 | 32 | **8** (max(4, 8)) |
| PP=1, TP=2, CP=4, EP=8, ETP=1 | 64 | **8** (max(8, 8)) |
| PP=2, TP=2, CP=1, EP=8, ETP=1 | 32 | **16** (2 · max(2, 8)) |
| PP=1, TP=2, CP=1, EP=4, ETP=2 | 16 | **8** (max(2, 8)) |

## Out of scope

- lint
- CUDA graph enablement
- Slurm script conversion
