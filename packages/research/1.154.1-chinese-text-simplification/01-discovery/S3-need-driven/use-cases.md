# Use Case Implementation Guide

## 1. Language Learning Apps (B2C)

### Requirements
- Volume: 1K-10K texts/month
- Accuracy: 75-85% acceptable (users read output, can adapt)
- Latency: < 2s per text
- Cost: Must be cheaper than manual editing

### Recommended Approach
**Phase 1 (MVP)**: Rule-based
- jieba + OpenCC + custom rules
- Timeline: 2-4 weeks
- Cost: $5K-15K

**Phase 2 (Scale)**: Hybrid
- Rules for 70% (simple cases)
- Neural for 30% (complex sentences)
- Timeline: +1 month
- Cost: +$10K-20K

### 3-Year TCO
| Year | Rule-Based | Hybrid | Manual Editing |
|------|------------|--------|----------------|
| 1    | $15K       | $25K   | $36K           |
| 2    | $5K        | $8K    | $36K           |
| 3    | $5K        | $8K    | $36K           |
| **Total** | **$25K** | **$41K** | **$108K** |

**Break-even**: 500 texts/month (automation cheaper than editors)

**Success metrics**:
- 90%+ learners complete articles
- < 5% complaints about difficulty
- HSK coverage 95%+

---

## 2. Accessibility Services (Government)

### Requirements
- Volume: 100-1K documents/month
- Accuracy: 90%+ (public-facing, legal implications)
- Auditability: Must explain simplifications
- Consistency: Same input → same output

### Recommended Approach
**Hybrid with human review**
- Rule-based for consistency
- Neural for complex legal language
- Mandatory human review before publication

**Timeline**: 3 months (includes compliance review)
**Cost**: $30K-50K (development + legal review)

### 3-Year TCO
| Year | Hybrid + Review | Manual Only |
|------|----------------|-------------|
| 1    | $60K           | $48K        |
| 2    | $25K           | $48K        |
| 3    | $25K           | $48K        |
| **Total** | **$110K** | **$144K** |

**Break-even**: 200 documents/month

**Constraints**:
- Must log all simplifications (auditability)
- Rule-based preferred (explainable)
- Human QA on 100% of output

---

## 3. Educational Publishers

### Requirements
- Volume: 500-2K texts/year (textbooks, readers)
- Accuracy: 95%+ (high stakes)
- Multiple levels: Need HSK 2, 3, 4, 5 versions
- Editorial workflow: Integrate with existing process

### Recommended Approach
**Neural + editorial workflow**
- Train separate models per HSK level
- Output 3 candidates per level
- Editors select best + refine
- Builds dataset for future improvement

**Timeline**: 4-6 months
**Cost**: $50K-80K (development + training)

### 3-Year TCO
| Year | Neural + Editorial | Manual Only |
|------|--------------------|-------------|
| 1    | $90K               | $80K        |
| 2    | $30K               | $80K        |
| 3    | $25K               | $80K        |
| **Total** | **$145K**      | **$240K**   |

**Break-even**: 1K texts/year

**Workflow**:
1. Author writes at natural level
2. Neural generates HSK 3, 4, 5 versions
3. Editors review and refine
4. Collect edits for model improvement

---

## 4. AI Tutoring Systems

### Requirements
- Volume: 10K+ per day (real-time)
- Accuracy: 80%+ (AI can re-explain if confused)
- Latency: < 500ms (conversational)
- Personalization: Adapt to individual learner, not just HSK level

### Recommended Approach
**Optimized neural with caching**
- mT5-small (fast inference)
- ONNX runtime on CPU
- Cache common simplifications
- Fine-tune on user feedback

**Timeline**: 3-4 months
**Cost**: $40K-70K

### Operating Costs
| Volume/day | Infrastructure | Cost/month |
|------------|----------------|------------|
| 10K        | 2x CPU (8 core)| $200       |
| 50K        | GPU (T4)       | $400       |
| 100K       | 2x GPU         | $800       |

**Latency optimization**:
- Caching: 50% hit rate → 250ms avg
- Batching: 5-10x throughput
- Model quantization: 2x faster

---

## Decision Matrix

| Scenario | Volume/month | Accuracy Need | Recommended | Timeline | Year 1 Cost |
|----------|--------------|---------------|-------------|----------|-------------|
| Learner app MVP | 500-2K | 75%+ | Rule-based | 3 weeks | $10K |
| Learner app scale | 5K-20K | 80%+ | Hybrid | 2 months | $25K |
| Government docs | 100-500 | 90%+ | Hybrid + review | 3 months | $60K |
| Publishers | 1K-3K/year | 95%+ | Neural + editorial | 5 months | $90K |
| AI tutoring | 10K+/day | 80%+ | Neural (optimized) | 3 months | $50K |

## General Guidelines

**< 500 texts/month**: Manual editing cheaper (unless latency matters)
**500-5K/month**: Rule-based MVP, upgrade to hybrid if limited
**5K-20K/month**: Hybrid (rules + neural)
**> 20K/month**: Full neural with optimization

**Accuracy requirements**:
- < 80%: Rule-based sufficient
- 80-90%: Hybrid
- > 90%: Neural + human review

**Budget constraints**:
- < $15K: Rule-based only
- $15K-$40K: Hybrid possible
- > $40K: Full neural viable
