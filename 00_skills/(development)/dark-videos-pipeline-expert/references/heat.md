# Heat and the top 20

## LAYA Learning System

The LAYA (Learn Yet Another) heat score is the pipeline's core quality signal, rating each video on a 0–10 scale. This score drives the ranking algorithm and informs content quality assessment.

### Heat Calculation
```
heat = mean_LAYA_probability × 10, clamped to 0–10
```

Where `mean_LAYA_probability` is the average LAYA probability across all evaluated features (content quality, engagement potential, relevance, etc.).

### Sorting Algorithm (Top 20 Ranking)
```
sort_key = 0.65 × baseline_velocity + 0.35 × LAYA_signal
```

- **baseline_velocity**: How fast the video is gaining traction/views (external performance metric)
- **LAYA_signal**: LAYA heat score divided by 10 (normalized 0–1)
- **0.65 weight**: Velocity dominates (65% influence) - measures actual performance
- **0.35 weight**: LAYA moderates (35% influence) - measures inherent quality/potential

This balance prevents purely viral but low-quality content from always winning, while also preventing high-quality but new content from being overlooked.

### Heat Score Interpretation

| Heat (0-10) | LAYA Probability | Interpretation | Action |
|-------------|------------------|----------------|--------|
| 8.0 - 10.0 | 0.8 - 1.0 | Excellent quality | High potential, prioritize for posting |
| 6.0 - 7.9 | 0.6 - 0.79 | Good quality | Solid performance, normal priority |
| 4.0 - 5.9 | 0.4 - 0.59 | Average quality | Moderate potential, monitor |
| 2.0 - 3.9 | 0.2 - 0.39 | Below average | Low potential, consider replacement |
| 0.0 - 1.9 | 0.0 - 0.19 | Poor quality | Unlikely to perform well, replace |

### The 9.5+ Badge

- Videos with `heat >= 9.5` receive a `9.5+` badge
- **Critical**: The badge does NOT remove the video from the top 20
- Helps identify highest-quality candidates for special handling
- May influence dispatch prioritization (high-HEAT posts get priority queue position)
- Visual indicator only, no functional change to ranking algorithm
- Represents top ~5% of evaluated content quality

### Learning Loop Integration

The LAYA system feeds into a continuous learning cycle:

1. **Mining Phase**: Videos mined from connectors (YouTube API, provider URLs)
2. **Ranking Phase**: LAYA scores computed alongside velocity metrics
3. **Framing Phase**: Description + tags generated, LAYA score stored per video
4. **Posting Phase**: Videos posted, performance data collected (views, engagement, etc.)
5. **Learning Phase**: Post-performance data feeds back to improve future LAYA predictions
6. **Next Run**: Improved LAYA predictions lead to better ranking in subsequent runs

**Learning Feedback Signals:**
- Actual view counts vs. predicted
- Engagement rates (likes, comments, shares)
- Completion rates (watch time % for You Shorts/IG Reels)
- Share velocity
- Comment sentiment

**TypeSafe Key Impact:**
- With TypeSafe key: LAYA predictions backed by trained ML model
- Without TypeSafe key: Baseline predictor supplies probability; model improves with data over time
- Judgments that need the key stay empty until key and sufficient data exist
- Lookback widening: 7 → 14 → 30 → 90 days to gather enough candidates for scoring

### Target Count System

- **Default**: 20 videos in top list (`target_count: 20`)
- **Alternative**: Can set to 10 or other values
- **Promotion**: Saved value of 10 gets promoted to 20 once set
- **Purpose**: Controls pool size for ranking and dispatch queue
- **Reserve**: Pipeline aims for `target_count` plus reserve candidates

### Lookback Widening (No TypeSafe Key / Insufficient Candidates)

When mining doesn't produce enough candidates:

```
7 days → 14 days → 30 days → 90 days
```

- Widen progressively until pool fills `target_count` plus reserve
- Each widening extends the mining search period
- Prevents pipeline stalling with too-narrow lookback
- Ultimate fallback: 90-day historical search

### Practical LAYA Score Examples

**Example A: Viral Potential, Moderate Quality**
- Velocity: 9.0 (very high, trending topic)
- LAYA: 5.0 (moderate quality signal)
- Heat: 5.0
- Sort key: `0.65 × 9.0 + 0.35 × 5.0 = 5.85 + 1.75 = 7.60`
- Ranking: High due to velocity, but LAYA prevents top spot
- Outcome: Will rank well but may not sustain performance long-term

**Example B: Quality Content, New Channel**
- Velocity: 3.0 (low, new channel with few views)
- LAYA: 8.5 (high quality signal)
- Heat: 8.5
- Sort key: `0.65 × 3.0 + 0.35 × 8.5 = 1.95 + 2.975 = 4.925`
- Ranking: Moderate, but LAYA helps offset low velocity
- Outcome: Good chance of sustained performance as channel grows

**Example C: Both Excellent**
- Velocity: 8.0 (high, gaining traction)
- LAYA: 9.0 (excellent quality)
- Heat: 9.0
- Sort key: `0.65 × 8.0 + 0.35 × 9.0 = 5.2 + 3.15 = 8.35`
- Ranking: Top 3 material
- Outcome: Likely to perform well and sustain; gets `9.5+` consideration if velocity also high enough

**Example D: Both Poor**
- Velocity: 2.0 (low, no traction)
- LAYA: 2.0 (low quality signal)
- Heat: 2.0
- Sort key: `0.65 × 2.0 + 0.35 × 2.0 = 1.3 + 0.7 = 2.0`
- Ranking: Bottom of top 20 or eliminated
- Outcome: May not make final publish list

## Troubleshooting LAYA Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Low LAYA scores across the board | No TypeSafe key configured | Configure TypeSafe key or rely on baseline predictor |
| High LAYA but low ranking | Velocity very low | Widen mining lookback, check trending topics |
| Low LAYA but high ranking | Velocity very high | Monitor for quality drop-off; plan content refresh |
| `insufficient_candidates` | Not enough videos mined | Widen lookback (7→14→30→90 days), check connectors |
| `heat >= 9.5` badge not appearing | Insufficient data for accurate scoring | Run more pipelines, gather performance feedback |
| LAYA scores not improving | Learning loop not feeding | Ensure post-performance data is collected and cached |
