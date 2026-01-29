# S3 Recommendation: Scenario Selection Guide

## Quick Reference Matrix

| Your Situation | Recommended Tool | Key Workflow | Est. Time | Est. Cost |
|----------------|------------------|--------------|-----------|-----------|
| **MT training data (10M+ pairs)** | Hunalign | Parallel chunks + filtering | 5-6 hours | <$5 |
| **Multilingual CMS (100K sentences)** | vecalign | Extract + embed + TM database | 1-2 hours | <$3 |
| **Research corpus (high quality)** | vecalign or Bleualign | Manual validation + iteration | 2-4 hours | Variable |
| **Web-crawled data (noisy)** | Hunalign → vecalign hybrid | Fast filter + accurate refine | 3-5 hours | <$10 |

## Workflow Selection Decision Tree

```
Start: What's your primary constraint?

├─ SPEED (need results in minutes)
│  └─> Use Hunalign
│      • Best for: >1M pairs
│      • Trade-off: 90% accuracy (good enough for most)
│      • Workflow: MT Training Data

├─ ACCURACY (need >95% precision)
│  └─> Use vecalign or Bleualign
│      • Best for: <500K pairs
│      • Trade-off: Slower, more resources
│      • Workflow: Multilingual CMS or Research Corpus

├─ BUDGET (limited compute resources)
│  └─> Use Hunalign (CPU-only)
│      • Best for: Any size on commodity hardware
│      • Trade-off: Lower accuracy on divergent texts
│      • Workflow: MT Training Data (CPU variant)

└─ LANGUAGE PAIR (low-resource, no dictionaries)
   └─> Use vecalign
       • Best for: Any language in LASER (93 languages)
       • Trade-off: Requires GPU for reasonable performance
       • Workflow: Multilingual CMS
```

## Scenario Deep Dives

### Scenario 1: Startup Building MT System
**Context**: Limited budget, need large corpus, European languages

**Recommended Approach**:
1. **Tool**: Hunalign with dictionary
2. **Workflow**: MT Training Data (CPU variant)
3. **Timeline**: 2-3 days
4. **Cost**: <$50 (compute + human validation sample)
5. **Expected Result**: 8-10M pairs at 90-92% accuracy

**Key Steps**:
- Download public dictionaries (OPUS, etc.)
- Use GNU parallel for CPU parallelization
- Sample 1000 pairs for validation
- Iterate on threshold if quality insufficient

### Scenario 2: Enterprise with Existing Infrastructure
**Context**: Have GPU clusters, need high quality, multiple language pairs

**Recommended Approach**:
1. **Tool**: vecalign
2. **Workflow**: Multilingual CMS + TM Database
3. **Timeline**: 1 week (including integration)
4. **Cost**: Marginal (GPU already available)
5. **Expected Result**: 96-98% accuracy, reusable TM

**Key Steps**:
- Set up vecalign on GPU cluster
- Build translation memory database
- Integrate with CMS via API/webhook
- Deploy validation dashboard

### Scenario 3: Academic Research
**Context**: Need publication-quality alignments, moderate corpus size

**Recommended Approach**:
1. **Tool**: vecalign or Bleualign (compare both)
2. **Workflow**: Research Corpus workflow
3. **Timeline**: 2-3 weeks (including validation)
4. **Cost**: <$100 (cloud GPU time)
5. **Expected Result**: >97% accuracy, documented methodology

**Key Steps**:
- Run both vecalign and bleualign
- Compute inter-annotator agreement on sample
- Manual validation by native speakers
- Document parameters and report precision/recall

### Scenario 4: Content Localization Company
**Context**: Ongoing translations, need consistency, tight deadlines

**Recommended Approach**:
1. **Tool**: vecalign with incremental updates
2. **Workflow**: Multilingual CMS + continuous integration
3. **Timeline**: 1 day setup, then automated
4. **Cost**: ~$50/month (GPU instance)
5. **Expected Result**: Real-time TM updates, high reuse

**Key Steps**:
- Deploy vecalign as microservice
- Set up webhook for content updates
- Build TM query API for translators
- Monitor quality metrics dashboard

## Common Pitfalls and Solutions

### Pitfall 1: Choosing vecalign Without GPU
**Problem**: Alignment takes hours or days instead of minutes
**Solution**:
- Use cloud GPU (AWS, GCP, Azure) for one-time processing
- Or switch to Hunalign for CPU-based speed
- Or process in batches overnight

### Pitfall 2: Using Hunalign on Highly Divergent Text
**Problem**: Literary translation or paraphrased content gets misaligned
**Solution**:
- Switch to vecalign or Bleualign
- Or use hunalign as first pass, then manually review low-confidence pairs
- Or build domain-specific dictionary to improve hunalign

### Pitfall 3: Not Validating Quality
**Problem**: Discover alignment errors after building dependent systems
**Solution**:
- Always sample and validate (1000 pairs minimum)
- Compute precision/recall before committing to tool
- Set up continuous monitoring for production systems

### Pitfall 4: Over-Engineering for Small Corpora
**Problem**: Setting up complex hybrid pipeline for 10K pairs
**Solution**:
- Just use vecalign (simple, accurate, fast enough for small data)
- Save hybrid approaches for >1M pairs

## Next Steps by Scenario

### If Building MT System
→ **Proceed with**: MT Training Data workflow
→ **Next**: S4 for scaling to 100M+ pairs

### If Building TM/CMS Integration
→ **Proceed with**: Multilingual CMS workflow
→ **Next**: S4 for production deployment strategies

### If Academic/Research
→ **Proceed with**: Custom combination of S2 (algorithms) + S3 (workflows)
→ **Next**: S4 for reproducibility and publication guidelines

### If Still Undecided
→ **Quick experiment**:
1. Take 10K sentence sample
2. Run all three tools (1-2 hours)
3. Validate 100 pairs each
4. Choose based on accuracy/speed tradeoff

## References

- MT Training Data: See `mt-training-data.md`
- Multilingual CMS: See `multilingual-cms.md`
- Hybrid Approaches: See S4 strategic recommendations
