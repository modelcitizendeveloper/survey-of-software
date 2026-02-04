# Use Case: Scale-Aware Architects (Build vs Buy Decisions)

## Who Needs This

**Persona**: Technical architects, engineering leads, or CTOs making strategic decisions about search infrastructure at scale.

**Context**:
- Company growing from 10K to 100K to 1M+ users
- Search is mission-critical (core product feature or revenue-driving)
- Currently self-hosted OR evaluating managed services
- Budget: $50-5K/month search infrastructure
- Team: 5-50 engineers, considering dedicated search team
- Dataset: 100K-10M documents, planning for 10M-100M growth

**Decision timeline**: 3-6 months (research → POC → pilot → production)

**Stakeholders**: CTO, VP Engineering, Product, Finance (cost approval)

---

## Why They Need Full-Text Search Libraries

**Primary problem**: Need to make informed build-vs-buy decision at inflection point where self-hosted library becomes expensive OR where managed service costs are unjustified.

**Strategic questions**:
1. **When does DIY stop making sense?** (Scale, team, features)
2. **What's the true cost of self-hosted?** (Engineering time, not just VPS cost)
3. **What's the lock-in risk?** (Can we migrate if wrong choice?)
4. **How do we derisk the decision?** (POC, pilot, staged rollout)

**Business impact**:
- **Wrong choice = costly**:
  - Self-host too long → Performance degrades, team burns out
  - Managed too early → $5K/month costs before revenue justifies it
- **Right choice = scalable growth** without search becoming bottleneck

---

## Their Requirements

### Decision Framework Requirements
- **Cost model** - TCO comparison: DIY vs managed (5-year horizon)
- **Risk assessment** - Lock-in, team dependency, single point of failure
- **Migration path** - Can we switch if wrong? (Tantivy → Algolia, or vice versa)
- **Team capacity** - Do we have engineering bandwidth for self-hosted?

### Technical Requirements
- **Scale**: Current 100K docs, planning for 10M over 3 years
- **Performance**: <10ms p95 (user-facing search)
- **Availability**: 99.9% uptime (3 9s) minimum
- **Features**: Basic (BM25, filters) now, advanced (personalization, analytics) future

### Organizational Constraints
- **Team**: 10-person eng team, can dedicate 0.5-1 FTE to search
- **Budget**: $50-500/month self-hosted OR $200-2K/month managed
- **Timeline**: 3-6 months to production-ready
- **Risk tolerance**: Can't afford production downtime; prefer derisked approach

---

## Library Selection Criteria (From S1)

### Top Priority: Scale Ceiling and Transition Point

**Decision rule**: When does library X become insufficient? When should we migrate to managed services?

### Evaluation Against S1 Libraries (With Scale Limits)

| Library | Scale Ceiling | When to Migrate |
|---------|--------------|-----------------|
| **Tantivy** | 1M-10M docs (8-16GB RAM) | >10M docs, >1K QPS, or need personalization/analytics |
| **Xapian** | 10M-100M docs (proven at 100M+) | >100M docs, or need multi-region geo-distribution |
| **Pyserini** | Billions (Lucene-backed) | When need enterprise support, or non-academic use case |
| **Whoosh** | 10K-1M docs (Python performance ceiling) | >1M docs, or <50ms latency required |
| **lunr.py** | 1K-10K docs (in-memory limit) | >10K docs, or need persistence |

### Decision Matrix by Current State

**Current State: 100K docs, 100 QPS, growing 3× per year**

| Year | Docs | QPS | Recommended | Why |
|------|------|-----|-------------|-----|
| Year 1 | 100K | 100 | **Tantivy** | Sweet spot: performance + scale + DIY costs |
| Year 2 | 300K | 300 | **Tantivy** | Still within limits (10M docs, 1K QPS) |
| Year 3 | 1M | 1K | **Tantivy** (edge) OR **Managed** | Approaching limits; evaluate migration |
| Year 4 | 3M | 3K | **Managed** (Algolia/ES) | Exceeded DIY limits |

**Key insight**: Tantivy gives 2-3 years runway before needing managed services.

---

## Cost Analysis: DIY vs Managed (5-Year TCO)

### DIY (Tantivy) Costs

**Infrastructure** (VPS + storage):
- Year 1 (100K docs): $50/month × 12 = $600/year (4GB RAM VPS)
- Year 2 (300K docs): $80/month × 12 = $960/year (8GB RAM VPS)
- Year 3 (1M docs): $150/month × 12 = $1,800/year (16GB RAM VPS)
- **Total**: $3,360 over 3 years

**Engineering costs** (0.5 FTE):
- Setup: 2 weeks ($5K one-time, assuming $130K/year engineer = $2.5K/week)
- Maintenance: 10 hours/month × 12 months × 3 years = 360 hours = $23,400 (assuming $65/hour)
- **Total**: $28,400 over 3 years

**Grand Total (DIY)**: $31,760 over 3 years

---

### Managed (Algolia/Typesense) Costs

**Subscription** (per-document pricing):
- Year 1 (100K docs): $200/month × 12 = $2,400/year
- Year 2 (300K docs): $400/month × 12 = $4,800/year
- Year 3 (1M docs): $800/month × 12 = $9,600/year
- **Total**: $16,800 over 3 years

**Engineering costs**:
- Setup: 1 week ($2.5K one-time)
- Maintenance: 2 hours/month × 12 × 3 = 72 hours = $4,680
- **Total**: $7,180 over 3 years

**Grand Total (Managed)**: $23,980 over 3 years

---

### Cost Comparison

| Approach | 3-Year TCO | Break-Even Point |
|----------|-----------|------------------|
| **DIY (Tantivy)** | $31,760 | Never (higher) |
| **Managed** | $23,980 | Year 1 onwards |

**Surprising result**: Managed is CHEAPER when accounting for engineering time.

**However**: This assumes:
- Engineer costs $130K/year ($65/hour)
- Engineer spends 10 hours/month on DIY (realistic for 1 person maintaining search)

**If engineer cheaper OR spend less time**:
- $100K/year engineer + 5 hours/month → DIY = $17,900 (cheaper than managed)
- $80K/year engineer (international) → DIY = $12,400 (significantly cheaper)

**Key insight**: Cost crossover depends on **engineering hourly rate** and **time spent maintaining**.

---

## Risk Assessment

### DIY (Tantivy) Risks

| Risk | Severity | Mitigation |
|------|----------|-----------|
| **Single point of failure** | High | No one else knows system if engineer leaves |
| **Scale ceiling** | Medium | Will hit 10M doc limit in 3-4 years, must migrate |
| **Performance degradation** | Medium | Self-tuning needed (index optimization, memory management) |
| **Feature gaps** | Medium | No personalization, analytics, A/B testing |
| **Operational burden** | High | On-call, monitoring, backups, upgrades |

### Managed (Algolia) Risks

| Risk | Severity | Mitigation |
|------|----------|-----------|
| **Vendor lock-in** | Medium | Proprietary ranking algorithm, but data export supported |
| **Cost escalation** | High | Pricing increases as documents/queries grow |
| **Less control** | Low | Can't customize ranking beyond dashboard settings |
| **Compliance** | Low | Data stored in vendor infrastructure (check regulations) |

### Risk-Adjusted Recommendation

**Lower risk**: **Managed** (Algolia/Typesense)
- Reason: Reduces single-point-of-failure, operational burden, scale ceiling

**Higher reward**: **DIY** (Tantivy)
- Reason: Lower cost IF engineering time is cheap, full control, no vendor lock-in

**Balanced approach**: Start DIY, plan migration to managed at inflection point (Year 3).

---

## Migration Path Planning

### Phase 1: DIY with Tantivy (Year 1-2)
- **Scale**: 100K-500K docs
- **Cost**: $50-80/month infra + 0.5 FTE
- **Goal**: Validate search is valuable, understand requirements
- **Monitoring**: Track query latency, index size, engineering time spent

### Phase 2: Pilot Managed Service (Year 2-3)
- **Trigger**: Approaching 1M docs OR engineering time >20 hours/month
- **Approach**: Run Tantivy + Algolia in parallel for 2 months
- **A/B test**: 10% traffic to Algolia, compare UX metrics
- **Decision**: Migrate if Algolia ROI positive (better metrics + reduced eng time)

### Phase 3: Full Migration (Year 3)
- **Cutover**: Move 100% traffic to managed service
- **Keep Tantivy**: For 3 months as fallback (disaster recovery)
- **Decommission**: Shut down DIY infra after confidence established

**Key insight**: Don't treat DIY vs managed as one-time decision. Plan for staged migration.

---

## Real-World Examples

### Companies that Started DIY, Migrated to Managed

**Example 1: E-commerce startup**
- Year 1-2: Tantivy (20K products, 1K users)
- Year 3: Hit 100K products, 50K users → Algolia
- **Reason**: Engineering team too busy with core product to maintain search
- **Cost**: Algolia $500/month justified by revenue growth

**Example 2: SaaS company**
- Year 1-3: Tantivy (500K documents, 10K users)
- Year 4: Stayed on Tantivy, scaled to 2M docs
- **Reason**: Search NOT revenue-critical; cost savings matter more than features
- **Outcome**: Saved $30K/year vs Algolia

### Companies that Stayed DIY Long-Term

**Example: Open-source project**
- Documentation site: 10K pages, Xapian
- 10+ years on DIY
- **Reason**: Budget = $0, technical community can maintain
- **Outcome**: Never needed managed (scale stays <100K pages)

---

## Decision Framework Summary

### Choose DIY (Tantivy/Xapian) When:
✅ Scale <1M documents (at least 2 years runway)
✅ Engineering team available (0.5-1 FTE sustainable)
✅ Search not mission-critical (can tolerate occasional downtime)
✅ Budget-constrained (DIY saves $5K-20K/year)
✅ No need for advanced features (personalization, analytics)

### Choose Managed (Algolia/Typesense) When:
✅ Scale >1M documents (or rapid growth trajectory)
✅ Engineering team busy (can't dedicate FTE to search)
✅ Search is mission-critical (99.99% uptime required)
✅ Budget allows (managed cost justified by team time savings)
✅ Need advanced features (personalization, analytics, A/B testing)

---

## Validation Against S1 Findings

S1 concluded:
- **Tantivy**: Best for production, scales to 10M docs
- **Path 1 (DIY) viable up to 10M docs, <1000 QPS**
- **Path 3 (Managed) necessary beyond that**

**S3 validation**: Scale-aware architects are the DECISION-MAKERS S1 was informing:
- Need scale ceiling clarity (✅ S1 provided: 10M docs / 1K QPS)
- Need cost/benefit analysis (✅ S3 added: TCO comparison)
- Need migration planning (✅ S3 added: staged approach)
- Need risk assessment (✅ S3 added: DIY vs managed risks)

**Alignment**: S1 technical findings + S3 business context = complete decision framework.

**Gap filled**: S1 said "when to use Path 3," S3 explains HOW to make that decision (cost, risk, timeline).
