# Heat and the top 20

Default `target_count` is 20. A saved value of 10, the previous default, is promoted to 20 once. An operator can set another count afterwards, including 10.

Sort key stays `0.65 * baseline velocity + 0.35 * JEV signal`. `heat` is the mean JEV probability times 10, clamped to 0–10. It is stored on the breakdown for the mining table.

The table shows that note. `heat >= 9.5` gets a `9.5+` badge. The badge does not remove the video from the top 20.

Without a TypeSafe key, the baseline predictor supplies the probability and the run still ranks. Judgments that need the key stay empty until the key and the videos exist.
