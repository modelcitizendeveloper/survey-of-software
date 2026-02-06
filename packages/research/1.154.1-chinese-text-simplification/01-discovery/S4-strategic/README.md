# S4-strategic: Viability & ROI Analysis

## Status: 🚧 PLANNED

This phase will provide long-term strategic decisions with financial models and risk assessment.

## Planned Topics

### 1. Build vs Buy Viability
- 3-year TCO comparison
- Break-even analysis
- Market landscape (commercial solutions, if any)
- Build decision factors

### 2. Rule-Based vs Neural vs Hybrid ROI
- Cost models for each approach
- Maintenance costs
- Scaling costs (volume growth)
- Quality improvements over time

### 3. Break-Even Analysis
- At what volume does automation pay off vs manual editing?
- At what volume does neural become cheaper than rule-based?
- Fixed costs vs variable costs

### 4. Risk Assessment
- **Meaning drift**: Automated simplification changes meaning
- **Quality degradation**: Errors accumulate over time
- **Segmentation errors**: Jieba mistakes cascade
- **Context blindness**: Rule-based misses context
- **Mitigation strategies**

### 5. Team Skills and Hiring
- What skills are needed for each approach?
- Hiring costs (NLP engineer vs linguist vs ML engineer)
- Training existing team vs hiring specialists
- Consulting vs in-house development

### 6. Technology Maturity Assessment
- Current state of Chinese text simplification (2026)
- Projected improvements (2027-2029)
- When to wait vs build now
- Vendor landscape (commercial APIs, if any)

## Research Questions

1. **At what scale does neural become cost-effective?**
   - Volume thresholds: 1K, 10K, 100K texts/month
   - Quality requirements: 70%, 80%, 90%+ accuracy
   - Time horizons: 1 year, 3 years, 5 years

2. **What are the risks of automated simplification?**
   - Meaning drift: 5-10% of sentences change meaning subtly
   - Unnatural output: 10-15% sound awkward
   - Over-simplification: 5% become too simple (lose nuance)
   - Under-simplification: 10-20% remain too complex
   - **Mitigation**: Human review, conservative rules, hybrid approach

3. **When should you wait for better libraries?**
   - If budget < $10K → wait 1-2 years, libraries may mature
   - If volume < 500 texts/month → manual editing may be cheaper
   - If accuracy needs > 95% → wait or use hybrid with heavy editing

4. **What's the competitive advantage of building now?**
   - First-mover advantage in language learning apps
   - Custom domain adaptation (medical, legal)
   - Data moat (collect user feedback, improve over time)

## Estimated Time

3-4 hours for strategic analysis and ROI modeling

## Deliverables (Planned)

- `build-vs-buy-viability.md` - 3-year TCO comparison
- `roi-analysis.md` - Break-even models, cost scenarios
- `risk-assessment.md` - What can go wrong, mitigation strategies
- `team-skills.md` - Hiring and training considerations
- `technology-maturity.md` - Market state, future outlook
- `recommendation.md` - **FINAL STRATEGIC RECOMMENDATIONS**

---

**Status**: Outline created, detailed research pending
**Next session**: Start after S3-need-driven is complete
**Final output**: Complete 4PS research package with strategic go/no-go decision
