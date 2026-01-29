# Strategic Analysis: Build vs Buy vs Open Source

## Decision Framework

### The Three Options

| Option | Capital Investment | Ongoing Cost | Control | Flexibility | Time to Production |
|--------|-------------------|--------------|---------|-------------|--------------------|
| **Buy** (SaaS API) | Low | High | Low | Low | Days |
| **Open Source** | Medium | Low | High | High | Weeks |
| **Build** | High | Medium | Highest | Highest | Months |

## Option 1: Buy (SaaS Alignment API)

### Current Market (2026)

**Commercial Offerings**:
1. **ModernMT Align API**
   - Pricing: $0.10 per 1K alignments
   - Quality: 95-97% F1 (neural-based)
   - Languages: 200+ pairs
   - SLA: 99.9% uptime

2. **Phrase TMS Alignment**
   - Pricing: Bundled with TMS ($500-2000/month)
   - Quality: 93-96% F1
   - Languages: 100+ pairs
   - Integration: Native TMS integration

3. **Google Cloud Translation Alignment** (Beta)
   - Pricing: $0.08 per 1K alignments
   - Quality: 96-98% F1 (leverages Google Translate)
   - Languages: 130+ pairs
   - SLA: Standard Cloud SLA

### When to Buy

✅ **Choose SaaS if**:
- Corpus size: <10M pairs/year
- Team size: <5 engineers
- Need fast time-to-market (days, not months)
- Willing to pay premium for convenience
- No sensitivity to data leaving your infrastructure

❌ **Avoid SaaS if**:
- Processing >10M pairs/month (cost explodes)
- Data sovereignty requirements (GDPR, HIPAA)
- Need custom algorithm tuning
- Vendor lock-in unacceptable

### TCO Analysis (SaaS)

**Scenario**: Localization company, 5M pairs/year

| Year | Usage Cost | Integration Cost | Total |
|------|------------|------------------|-------|
| Year 1 | $5,000 | $10,000 | $15,000 |
| Year 2 | $5,000 | $1,000 | $6,000 |
| Year 3 | $5,000 | $1,000 | $6,000 |
| **3-Year Total** | | | **$27,000** |

*Assumes $0.10/1K pairs, 5M pairs/year, integration effort year 1*

## Option 2: Open Source (Hunalign, vecalign, Bleualign)

### Current Landscape

**Mature Options**:
1. **Hunalign**
   - Maturity: Production-ready (10+ years)
   - Maintenance: Community-maintained
   - Support: None (DIY)
   - Risk: Low (stable, simple)

2. **vecalign**
   - Maturity: Research to production
   - Maintenance: Active (Facebook AI)
   - Support: GitHub issues
   - Risk: Medium (complex dependencies)

3. **Bleualign**
   - Maturity: Stable
   - Maintenance: Sporadic
   - Support: Minimal
   - Risk: Medium (requires MT)

### When to Use Open Source

✅ **Choose Open Source if**:
- Team has ML/NLP expertise
- Processing >10M pairs (cost advantage over SaaS)
- Need full control and customization
- Can invest in setup and maintenance
- On-premise deployment required

❌ **Avoid Open Source if**:
- No in-house ML expertise
- Need vendor support and SLA
- Cannot dedicate engineering time to ops
- Prefer predictable monthly costs

### TCO Analysis (Open Source)

**Scenario**: Enterprise, 50M pairs/year, in-house team

| Year | Infrastructure | Engineering Time | Total |
|------|----------------|------------------|-------|
| Year 1 | $10,000 | $80,000 (0.5 FTE setup) | $90,000 |
| Year 2 | $10,000 | $40,000 (0.25 FTE maintenance) | $50,000 |
| Year 3 | $10,000 | $40,000 (0.25 FTE) | $50,000 |
| **3-Year Total** | | | **$190,000** |

*Assumes GPU infrastructure, 1 senior engineer ($160K/year)*

**Break-even vs SaaS**: ~4-5M pairs/year

## Option 3: Build Custom Solution

### What "Build" Means

Not recommended to build alignment algorithm from scratch. "Build" means:
- Custom pipeline orchestration
- Domain-specific tuning of open-source tools
- Proprietary quality filtering
- Integration with proprietary systems

### When to Build

✅ **Consider Building if**:
- Alignment is core business differentiation
- Existing tools don't meet accuracy needs
- Have unique data characteristics (e.g., code + text)
- Team >10 ML engineers
- Budget for 6-12 month project

❌ **Don't Build if**:
- Alignment is a commodity input (use open source)
- Team <5 engineers
- Timeline is critical
- Not a core competency

### TCO Analysis (Custom Build)

**Scenario**: Large MT company, 500M pairs/year

| Year | Infrastructure | Engineering | Research | Total |
|------|----------------|-------------|----------|-------|
| Year 1 | $50,000 | $320,000 (2 FTE) | $100,000 | $470,000 |
| Year 2 | $50,000 | $160,000 (1 FTE) | $50,000 | $260,000 |
| Year 3 | $50,000 | $160,000 (1 FTE) | $50,000 | $260,000 |
| **3-Year Total** | | | | **$990,000** |

*Break-even vs SaaS*: ~20M pairs/year (but higher quality)

## Decision Matrix by Organization Type

### Startup (Seed Stage, <10 people)
**Recommendation**: **Buy (SaaS)**
- Rationale: Focus on core product, not infrastructure
- Timeline: Days
- Cost: Low upfront, scales with usage
- Risk: Low (can always switch later)

### Startup (Series A/B, 10-50 people)
**Recommendation**: **Open Source (vecalign or hunalign)**
- Rationale: Cost efficiency, team can handle ops
- Timeline: 2-4 weeks
- Cost: Medium upfront, low ongoing
- Risk: Medium (need ML expertise)

### Mid-Size Company (50-200 people)
**Recommendation**: **Open Source + Internal Tools**
- Rationale: Control + customization, cost effective at scale
- Timeline: 1-2 months
- Cost: Higher upfront, low ongoing
- Risk: Low (can hire/train for expertise)

### Enterprise (200+ people)
**Recommendation**: **Open Source or Build (if core competency)**
- Rationale: Full control, potential competitive advantage
- Timeline: 1-6 months
- Cost: High upfront, economies of scale
- Risk: Low (resources available)

## Hybrid Strategies

### Strategy 1: Start SaaS, Migrate to Open Source
**Timeline**:
- Month 1-6: Use SaaS, validate use case
- Month 7-12: Build open-source pipeline in parallel
- Month 13+: Migrate to self-hosted, keep SaaS as backup

**Benefits**:
- Fast time-to-market
- De-risk open-source investment
- Learn requirements before committing

### Strategy 2: Open Source + SaaS Fallback
**Architecture**:
- Primary: Self-hosted vecalign (95% of traffic)
- Fallback: SaaS API for edge cases or spikes
- Cost: Mostly self-hosted savings, SaaS for reliability

**Benefits**:
- Cost efficiency of open source
- Reliability of SaaS backup
- Graceful degradation

### Strategy 3: Multi-Vendor
**Architecture**:
- Route different language pairs to different tools
- High-resource: Open source (en-de, en-fr)
- Low-resource: SaaS (rare pairs)

**Benefits**:
- Optimize cost per language pair
- Best accuracy for each scenario

## Risk Assessment

### SaaS Risks
| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Price increase | High | Medium | Negotiate long-term contract |
| Service shutdown | Low | High | Always have export capability |
| Data breach | Low | High | Due diligence on vendor security |
| Vendor lock-in | High | Medium | Abstract API, keep data portable |

### Open Source Risks
| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Maintenance burden | Medium | Medium | Budget 0.25 FTE for ops |
| Breaking changes | Low | Medium | Pin versions, test upgrades |
| Security vulnerabilities | Medium | High | Monitor CVEs, update dependencies |
| Abandoned project | Low | High | Choose mature projects (hunalign) |

### Build Risks
| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Cost overruns | High | High | Phased approach, MVP first |
| Team turnover | Medium | High | Document extensively, cross-train |
| Complexity creep | High | Medium | Strict scope control |
| Opportunity cost | High | High | Only build if core differentiator |

## Recommendation Framework

### Start Here
Ask yourself:
1. **Is alignment a core competency?**
   - Yes → Consider build or advanced open source
   - No → Use SaaS or simple open source

2. **What's your annual volume?**
   - <1M pairs → SaaS
   - 1M-10M pairs → Open source
   - >10M pairs → Open source or build

3. **What's your team size and ML expertise?**
   - <5 people, no ML → SaaS
   - 5-20 people, some ML → Open source
   - >20 people, strong ML → Open source or build

4. **What's your timeline?**
   - Need it now → SaaS
   - 1-2 months okay → Open source
   - 6+ months okay → Build

### Most Common Path (Recommended for 80% of Cases)

1. **Start**: SaaS for MVP (month 1-3)
2. **Validate**: Confirm use case and volume (month 4-6)
3. **Decide**:
   - If low volume: Stay on SaaS
   - If high volume: Migrate to open source
4. **Operate**: Self-hosted open source with SaaS backup (month 7+)

## References

- [ModernMT Align API](https://www.modernmt.com/)
- [Google Cloud Translation](https://cloud.google.com/translate)
- [Open Source Tool Comparison](../S2-comprehensive/recommendation.md)
