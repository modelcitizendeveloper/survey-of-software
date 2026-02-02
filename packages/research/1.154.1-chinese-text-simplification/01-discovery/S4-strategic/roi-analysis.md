# ROI Analysis: Build vs Wait vs Manual

## 3-Year TCO Comparison

### Scenario: 2K texts/month (typical language learning app)

| Approach | Year 1 | Year 2 | Year 3 | Total | Notes |
|----------|--------|--------|--------|-------|-------|
| **Manual editing** | $36K | $36K | $36K | **$108K** | Baseline |
| **Rule-based** | $15K | $5K | $5K | **$25K** | 77% savings |
| **Hybrid** | $30K | $8K | $8K | **$46K** | 57% savings, better quality |
| **Full neural** | $60K | $15K | $15K | **$90K** | 17% savings, best quality |

**Verdict**: Rule-based or hybrid (neural not justified at this volume)

---

### Scenario: 10K texts/month (large platform)

| Approach | Year 1 | Year 2 | Year 3 | Total | Notes |
|----------|--------|--------|--------|-------|-------|
| **Manual editing** | $180K | $180K | $180K | **$540K** | Baseline |
| **Rule-based** | $20K | $5K | $5K | **$30K** | 94% savings, quality plateau |
| **Hybrid** | $40K | $10K | $10K | **$60K** | 89% savings |
| **Full neural** | $70K | $20K | $20K | **$110K** | 80% savings, best quality |

**Verdict**: Hybrid or neural (savings justify investment)

---

## Break-Even Timeline

**Rule-based**:
- Payback: 6-9 months at 1K texts/month
- Payback: 3-4 months at 5K texts/month

**Hybrid**:
- Payback: 12-18 months at 2K texts/month
- Payback: 6-8 months at 10K texts/month

**Neural**:
- Payback: 18-24 months at 5K texts/month
- Payback: 8-12 months at 20K texts/month

## Risk-Adjusted ROI

### Optimistic (90th percentile)
- Development faster than expected
- Quality better than expected
- Maintenance costs lower

**Result**: ROI +50% better

### Realistic (50th percentile)
- Numbers as stated above
- Some rework needed
- Expected maintenance

**Result**: ROI as modeled

### Pessimistic (10th percentile)
- Development 2x longer
- Quality requires more iteration
- Hidden maintenance costs

**Result**: ROI -50%, may not break even until Year 2

**Mitigation**: Start with rule-based MVP (lower risk, faster validation)

---

## Competitive Advantage Analysis

### Build Now (2026)

**Advantages**:
- First-mover in nascent market
- Collect user feedback data → improve model
- Data moat (your domain-specific corpus)
- Control over quality/latency

**Disadvantages**:
- Technology immature (no turnkey libraries)
- Must build custom solution
- Ongoing maintenance burden

### Wait 2-3 Years (2028-2029)

**Advantages**:
- Mature libraries may emerge
- Commercial APIs possible (like English has)
- Learn from others' mistakes
- Lower development cost

**Disadvantages**:
- Competitors already have 2-3 years of data
- Miss early market opportunity
- May still need custom solution (libraries might not fit your use case)

### Never Build (Manual Forever)

**Advantages**:
- No technical risk
- Editors can handle edge cases
- Quality ceiling is higher

**Disadvantages**:
- 5-10x more expensive at scale
- Can't scale to 100K+ texts/month
- Latency (humans need hours/days)

---

## Strategic Decision Framework

### BUILD NOW if:
1. Volume > 500 texts/month (automation ROI positive)
2. Need latency < 1 hour (humans too slow)
3. Have budget ($15K+ Year 1)
4. Technical capability (mid-level dev + Chinese speaker)

### WAIT 2-3 YEARS if:
1. Volume < 500 texts/month (manual cheaper)
2. Budget < $10K (can't build properly)
3. No technical team (can't maintain)
4. Accuracy needs > 95% (technology not ready)

### MANUAL FOREVER if:
1. Volume < 100 texts/month
2. High-stakes content (legal, medical) where errors unacceptable
3. Domain too niche (no training data exists)

---

## Investment Priorities

**If budget is $15K (rule-based)**:
- $8K: Development (2-3 weeks, mid-level dev)
- $3K: HSK vocabulary + synonym dictionary curation
- $2K: Testing + validation (50-100 samples)
- $2K: Deployment + infrastructure

**If budget is $40K (hybrid)**:
- $15K: Rule-based foundation
- $10K: Neural model training + integration
- $8K: Testing + human evaluation
- $7K: Infrastructure + monitoring

**If budget is $70K (full neural)**:
- $25K: Model training (mT5/mBART on MCTS)
- $15K: Data preparation + fine-tuning
- $12K: Evaluation + iteration
- $10K: Production deployment
- $8K: Infrastructure (GPU inference)

---

## Hidden Costs to Budget

1. **Ongoing curation** (10-20% of Year 1 cost annually)
   - HSK vocabulary updates (3.0 migration)
   - New slang, technical terms
   - User-reported errors

2. **Infrastructure scaling**
   - 10K → 100K texts/month: 10x compute cost
   - Budget $500-2K/month for hosting at scale

3. **Quality drift**
   - Models degrade over time (language evolves)
   - Re-train every 12-18 months (~$5K-10K)

4. **Support & monitoring**
   - On-call for failures
   - Debugging edge cases
   - A/B testing improvements

**Total ongoing**: 20-30% of Year 1 cost per year

---

## Scenarios Where ROI is Negative

1. **Volume too low**: < 300 texts/month (manual cheaper)
2. **Accuracy too high**: Need 98%+ (humans required anyway)
3. **No technical team**: Outsource development + maintenance = 3x cost
4. **Domain too niche**: Legal Chinese, classical Chinese (no training data)
5. **Short-term project**: < 18 months (won't reach break-even)

---

## Expected Value Calculation

**Language learning app scenario (2K texts/month)**:

| Outcome | Probability | Cost (3yr) | Savings vs Manual | Expected Value |
|---------|-------------|------------|-------------------|----------------|
| Success (rule-based works) | 70% | $25K | $83K | +$58K |
| Partial (need hybrid) | 25% | $46K | $62K | +$16K |
| Failure (revert to manual) | 5% | $15K + $108K | -$15K | -$1K |
| **Expected** | **100%** | | | **+$73K** |

**Verdict**: Strong positive expected value (build rule-based MVP)

---

## Strategic Recommendations

1. **Most teams**: Start rule-based, iterate to hybrid if needed
2. **Large platforms**: Go straight to hybrid (skip learning phase)
3. **Publishers**: Neural + editorial (quality matters most)
4. **Startups**: Wait until PMF, then automate (manual until 500 texts/month)

**The mistake**: Jumping to neural too early (before you understand the problem)
**The opportunity**: Building now while market is nascent (2026-2028 window)
