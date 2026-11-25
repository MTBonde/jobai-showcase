# Sources for stats.json

Every number in `stats.json` is a measurement, dated. Only aggregates are published.

| Number | Measured | How |
|---|---|---|
| Funnel, round 14 | 23 Nov 2026 | The round's prefilter run and the round log |
| Corrections: 13,752 automatic, 331 by me | 25 Nov 2026 | The correction table, counted per source; a one-off re-score after a scoring-model change in summer is left out |
| 5,594 new rows in 56 days, median 103 per harvest day | 15 Oct 2026 | Harvest timestamps, 20 Aug - 14 Oct |
| 929 relevant for review | 15 Oct 2026 | Same period, after the shortlist and title filter |

Rows are counted, not jobs: the same job can be listed on several portals before
dedup folds them together.
