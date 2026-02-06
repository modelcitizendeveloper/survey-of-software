# S3-need-driven Recommendations

## Quick Decision Tree

```
Volume/month?
├─ < 500
│  └─ Manual editing ($3K-6K/month)
│     OR rule-based if need latency < 5min
│
├─ 500-5K
│  ├─ Accuracy < 80%? → Rule-based ($10K-15K year 1)
│  └─ Accuracy 80%+? → Hybrid ($25K-40K year 1)
│
└─ > 5K
   ├─ Accuracy < 85%? → Hybrid ($30K-50K year 1)
   └─ Accuracy 90%+? → Neural + review ($50K-90K year 1)
```

## Use Case Mapping

| Use Case | Approach | Why |
|----------|----------|-----|
| **Language learning app** | Rule-based → Hybrid | Users tolerate 75-85%, scale gradually |
| **Government accessibility** | Hybrid + mandatory review | Need 90%+ + auditability |
| **Publishers** | Neural + editorial | 95%+ needed, editors refine output |
| **AI tutoring** | Neural (optimized) | 10K+/day needs speed + personalization |
| **News sites** | Hybrid | Daily content, 80%+ acceptable |

## Break-Even Analysis

**Automation vs manual editing**:
- **100 texts/month**: Manual cheaper ($1.2K vs $1.7K/month amortized)
- **500 texts/month**: Break-even point
- **2K texts/month**: Automation 3x cheaper
- **10K texts/month**: Automation 5x cheaper

**Rule-based vs neural**:
- **< 5K/month**: Rule-based cheaper
- **5K-20K/month**: Hybrid best ROI
- **> 20K/month**: Full neural justified

## Key Insight

**Most teams should start rule-based** even if they'll eventually need neural:
1. Learn the domain (what fails? what patterns?)
2. Collect data (input → desired output)
3. Fine-tune neural on YOUR data (better than MCTS alone)

**Exception**: If you have > $50K budget and 10K+ texts/month from day 1, skip to neural.

## Cost Optimization

**Year 1 costs high** (development), **Year 2-3 drop 70%** (maintenance only):
- Rule-based: $15K → $5K/year
- Hybrid: $30K → $8K/year
- Neural: $60K → $15K/year

**Mistake to avoid**: Comparing Year 1 automation cost to Year 1 manual cost. Compare 3-year TCO.

## Success Criteria by Use Case

**Learner apps**:
- 90%+ completion rate
- < 5% difficulty complaints
- 95%+ HSK coverage

**Accessibility**:
- 0 legal challenges due to unclear language
- 90%+ users report "easy to understand"
- Audit trail for all simplifications

**Publishers**:
- Editors spend 50% less time vs writing from scratch
- 95%+ accuracy (minimal edits needed)
- Consistent style across levels

**AI tutoring**:
- < 500ms latency
- 80%+ learners report helpful explanations
- Adapt to user over time (personalization)
