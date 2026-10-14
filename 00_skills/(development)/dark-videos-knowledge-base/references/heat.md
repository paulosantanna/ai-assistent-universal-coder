# Heat Scoring and Top 20 Ranking

## Heat Formula

**Heat = 0.65 * baseline_velocity + 0.35 * LAYA_signal**

## Components

### baseline_velocity

- Measures video velocity (views/likes per unit time)
- Based on historical performance data
- Core metric for ranking

### LAYA_signal

- LAYA fine-tuning confidence score (0-10)
- Updated through learning loop
- Feeds post-performance data back into future rankings
- Calibrated weight: 35% of total heat

## Top 20 Rules

1. Top 20 list ordered by heat score (highest to lowest)
2. A score under 9.5 still stays in the top 20
3. Heat >= 9.5 badge does **not** remove from top 20
4. If heat under 9.5 remains inside top 20, do not re-rank solely for badge
5. Repeats of used videos (including same caption simhash) leave the ranking
6. Next candidate takes the slot when a video is removed

## Real Run Failure

- A real run that still selects fewer than `target_count` fails in `RankStage`
- Does not edit or schedule the shortened short list
- Insufficient candidates trigger `insufficient_candidates` failure

## Learning Loop Integration

- Post-performance data from published videos feeds back into LAYA model
- LAYA signals updated after each publishing cycle
- Improves future heat scoring accuracy