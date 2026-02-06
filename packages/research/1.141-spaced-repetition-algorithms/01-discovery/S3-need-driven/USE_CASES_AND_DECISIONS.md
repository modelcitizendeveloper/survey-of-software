# S3-Need-Driven: Use Cases and Decision Criteria

**Research Date**: 2026-01-16
**Focus**: Production use cases, cost analysis, framework selection criteria
**Target Audience**: Product managers, CTOs, educational app developers

---

## Production Use Cases

### Medical Education (Primary Use Case)

**Adoption Scale**: Widespread across medical schools globally

**Recent Research (2026 Class)**:
- Kirk Kerkorian School of Osteopathic Medicine (KKSOM) class of 2026 study (n=36)
- **Results**: Anki use correlated with increased CBSE exam performance
- **Metrics**: Higher matured card counts → higher exam scores

**Performance Gains**:
- Course I: +6.4% (p < 0.001)
- Course II: +6.2% (p = 0.002)
- Course III: +7.0% (p = 0.002)
- CBSE: +12.9% (p = 0.003)

**Board Exam Correlation**:
- Daily Anki use → increased Step 1 scores (p = 0.039)
- No significant correlation with Step 2 scores

**Wellness Benefits**:
- Association with increased sleep quality (p = 0.01)

**Sources**:
- [Exploring Impact of Spaced Repetition Through Anki - 2025](https://journals.sagepub.com/doi/10.1177/23821205251369705)
- [PMC Article on Preclinical Exam Performance](https://pmc.ncbi.nlm.nih.gov/articles/PMC12357012/)
- [Academic and Wellness Outcomes - 2023](https://journals.sagepub.com/doi/full/10.1177/23821205231173289)

### Language Learning

**Market Demand**: Core driver of SRS market growth

**Effectiveness**: 50-70% time reduction vs traditional methods

**Popular Applications**:
- Vocabulary acquisition
- Grammar pattern memorization
- Pronunciation practice
- Reading comprehension

**Sources**:
- [Effective SRS Language Learning Guide](https://www.fluentu.com/blog/learn/srs-spaced-repetition-language-learning/)
- [Best Language Learning Apps with SRS 2025](https://www.taalhammer.com/best-language-learning-apps-with-spaced-repetition-srs-and-ai-in-2025-taalhammer-vs-11-other-apps/)

### Professional Certification

**Use Cases**:
- Bar exam preparation (legal)
- CPA exam (accounting)
- Professional certification programs
- Technical skill retention

**Growth Driver**: Post-pandemic e-learning surge

### Other Applications

1. **Academic Learning**: K-12 and university courses
2. **Corporate Training**: Employee onboarding, compliance training
3. **Personal Development**: Skill acquisition, hobby learning
4. **Healthcare**: Patient education, medical terminology for nurses

**Sources**:
- [Spaced Repetition Software Market Research 2033](https://dataintelo.com/report/spaced-repetition-software-market)

---

## Development Costs (2026)

### SRS App Development Budget

**Budget Ranges**:

| Complexity | Cost Range | Timeline | Features |
|------------|------------|----------|----------|
| **MVP/Simple** | $30,000-$80,000 | 3-4 months | Basic SM-2, local storage, review UI |
| **Medium** | $80,000-$150,000 | 4-6 months | FSRS, cloud sync, analytics, notifications |
| **Complex** | $150,000-$250,000+ | 6-12 months | AI-driven, multi-platform, advanced analytics |

**Sources**:
- [App Development Costs 2026](https://topflightapps.com/ideas/app-development-costs/)
- [Education App Development Cost 2026](https://www.appverticals.com/blog/education-app-development-cost/)
- [How Much Does Education App Cost](https://www.technource.com/blog/cost-to-build-education-app/)

### General Mobile App Development Costs (2026)

**Industry Averages**:
- **Overall range**: $40,000-$400,000+
- **Average**: $80,000-$250,000
- **Simple apps**: $5,000-$50,000 (few screens, minimal backend)
- **Medium complexity**: $50,000-$180,000 (richer UX, integrations)
- **Complex apps**: $100,000-$500,000+ (custom backends, third-party integrations)

**Sources**:
- [Mobile App Development Cost 2026](https://appinventiv.com/guide/mobile-app-development-cost/)
- [Complete Pricing Guide](https://www.scalacode.com/blog/cost-to-develop-an-app/)

### Educational App Specific Costs

**Range**: $30,000-$600,000+

**By Type**:
- **Content-focused**: $30,000-$100,000
- **Interactive**: $100,000-$300,000
- **AI-driven**: $200,000-$600,000+

**Sources**:
- [Cost to Build Education App 2026](https://www.technource.com/blog/cost-to-build-education-app/)
- [eLearning App Development Costs 2026](https://ozvid.com/blog/343/elearning-app-development-in-2026-costs-features-business-benefits)

### MVP Development Timeline

**4-Week SRS MVP Plan**:

**Week 1**: Data model and local persistence
- Establish interfaces for decks, notes, and cards
- Budget: ~$7,500-$15,000

**Week 2**: Basic scheduling function
- Implement simplified SM-2
- Create review interface
- Budget: ~$7,500-$15,000

**Week 3**: User experience features
- Onboarding and daily review features
- Notification systems
- Budget: ~$7,500-$15,000

**Week 4**: Import/export and analytics
- Export/import functionalities
- Metrics dashboard
- Budget: ~$7,500-$15,000

**Total MVP Budget**: $30,000-$60,000 (4 weeks)

**Sources**:
- [How to Implement SRS: Beginner's Guide](https://techbuzzonline.com/spaced-repetition-implementation-guide/)

### Cost-Saving Strategies

**Cross-Platform Development**:
- React Native or Flutter
- **Savings**: 30-40% lower cost vs native (iOS + Android separately)
- **Trade-off**: Near-native performance, single codebase

**Open-Source Algorithms**:
- Use SM-2 (zero licensing cost)
- Use FSRS (open-source, free)
- **Savings**: Avoid SuperMemo licensing fees

**Cloud vs Self-Hosted**:
- Self-hosted (AWS, DigitalOcean): $50-$500/month
- Managed services (Firebase, Supabase): $100-$2,000/month
- **Trade-off**: Management complexity vs convenience

**Sources**:
- [Mobile App Development Cost 2026](https://saigontechnology.com/blog/mobile-app-development-cost/)

---

## Operating Costs

### Infrastructure Costs

**Backend Hosting**:
- **Tier 1 (MVP)**: $50-$200/month (DigitalOcean droplet, AWS t3.medium)
- **Tier 2 (Growth)**: $200-$1,000/month (Load balancing, database scaling)
- **Tier 3 (Scale)**: $1,000-$10,000+/month (Multi-region, CDN, high availability)

**Database**:
- **SQLite (local)**: $0 (mobile-only, no sync)
- **PostgreSQL (hosted)**: $15-$500/month (Supabase, AWS RDS)
- **Firebase**: Free tier, $25-$500/month (scale-dependent)

**Storage**:
- **User data**: ~1-5MB per active user (cards, review history)
- **Media (images, audio)**: Variable (10-100MB per user for language apps)
- **Cost**: $0.023/GB/month (S3), $0.01-$0.03/GB (CDN transfer)

### Algorithm Licensing

| Algorithm | License | Cost |
|-----------|---------|------|
| **SM-2** | Public domain | $0 |
| **FSRS** | Open-source (MIT) | $0 |
| **SM-18** | Proprietary | Unknown (SuperMemo licensing) |

**Strategic Implication**: Open-source dominance (SM-2, FSRS) eliminates licensing costs for startups

### Maintenance Costs

**Annual Maintenance**: 15-20% of development cost
- Example: $100K app → $15K-$20K/year

**Breakdown**:
- Bug fixes: 30-40%
- OS updates (iOS/Android): 20-30%
- Feature enhancements: 30-40%
- Security patches: 10-20%

---

## Algorithm Selection Decision Framework

### Step 1: Define Complexity Needs

**Use SM-2 if**:
- MVP/prototype stage
- Tight budget (<$50K)
- Simple use case (flashcards only)
- No personalization required
- Team has limited ML expertise

**Use FSRS if**:
- Production app
- Moderate budget ($80K+)
- Need performance optimization (20-30% fewer reviews)
- Willing to invest in parameter optimization
- Have user review history data

**Use SM-18 if**:
- Licensed SuperMemo integration
- Budget allows proprietary licensing
- Need absolute best performance
- Not building open-source product

### Step 2: Assess Technical Requirements

**Implementation Complexity**:

| Feature | SM-2 | FSRS | SM-18 |
|---------|------|------|-------|
| **Lines of code** | ~50 | ~100-200 | Unknown |
| **Dependencies** | None | ML libs | Proprietary |
| **Setup time** | Minutes | 1-5 min (migration) | N/A |
| **Ongoing training** | Never | Optional (monthly) | Unknown |

**Performance Requirements**:

| Metric | SM-2 | FSRS | SM-18 |
|--------|------|------|-------|
| **Success rate** | 47-60% | 89.6% | Unknown (likely >90%) |
| **Review reduction** | Baseline | 20-30% fewer | Best-in-class |
| **Retention target** | Fixed | Configurable | Adaptive |

### Step 3: Evaluate Team Constraints

**Team Size**:
- **Solo/Small (1-3)**: SM-2 (fast, simple)
- **Medium (3-10)**: FSRS (balance of performance and complexity)
- **Large (10+)**: FSRS or SM-18 (resources for optimization)

**Team Expertise**:
- **Beginners**: SM-2 (minimal learning curve)
- **Intermediate**: FSRS (moderate ML familiarity helpful)
- **Advanced**: FSRS or SM-18 (full optimization capability)

**Open-Source Requirement**:
- **Yes**: SM-2 or FSRS only
- **No**: SM-2, FSRS, or SM-18

### Step 4: Budget Considerations

**Development Budget**:
- **<$50K**: SM-2 (MVP, simple implementation)
- **$50K-$150K**: FSRS (production-ready)
- **>$150K**: FSRS with advanced features, or explore SM-18 licensing

**Operating Budget** (per 10K active users):
- **SM-2**: $200-$500/month (minimal compute)
- **FSRS**: $300-$800/month (parameter optimization compute)
- **SM-18**: Unknown (licensing fees)

---

## Market Positioning Recommendations

### For Language Learning Apps

**Algorithm**: FSRS
**Rationale**:
- 20-30% fewer reviews → better user retention
- Competitive with Duolingo, Memrise (both using advanced SRS)
- Open-source avoids licensing costs
- ML-driven optimization appeals to users

**Budget**: $100K-$200K development
**Timeline**: 4-6 months MVP → production

### For Medical Education Apps

**Algorithm**: FSRS (or SM-2 for MVP)
**Rationale**:
- Medical students already familiar with Anki (FSRS native since 23.10)
- Performance critical (board exam preparation)
- Evidence-based (multiple studies supporting efficacy)

**Budget**: $150K-$300K development (includes specialized medical content management)
**Timeline**: 6-9 months MVP → production

### For Corporate Training Apps

**Algorithm**: SM-2 (simple) or FSRS (if budget allows)
**Rationale**:
- Focus on compliance/onboarding (lower engagement than language learning)
- SM-2 sufficient for basic retention needs
- FSRS if competing on user experience

**Budget**: $50K-$150K development
**Timeline**: 3-6 months MVP → production

### For K-12 Educational Apps

**Algorithm**: SM-2
**Rationale**:
- Simplicity valued over optimization
- Lower budget constraints (schools)
- Proven effectiveness (50-70% time reduction)

**Budget**: $30K-$80K development
**Timeline**: 3-4 months MVP → production

---

## ROI Analysis

### User Retention Impact

**FSRS Advantage**: 20-30% fewer reviews
- **Implication**: Higher user retention (less review fatigue)
- **Metric**: 15-25% increase in DAU (daily active users) estimated

**SM-2 Baseline**: Standard SRS performance
- **50-70% time savings vs traditional methods**
- **Sufficient for most use cases**

### Competitive Advantage

**Market Leaders Using Advanced SRS**:
- Anki: FSRS (integrated 2023)
- Duolingo: Custom algorithm (likely FSRS-inspired)
- SuperMemo: SM-18 (proprietary)

**Competitive Positioning**:
- SM-2: Commodity feature (table stakes)
- FSRS: Competitive advantage (proven performance gains)
- SM-18: Best-in-class (but licensing barrier)

### Development Cost vs Performance Trade-off

| Algorithm | Dev Cost Premium | Performance Gain | ROI Break-Even |
|-----------|------------------|------------------|----------------|
| **SM-2** | Baseline ($0) | Baseline | Immediate |
| **FSRS** | +$20K-$40K | +20-30% fewer reviews | 6-12 months |
| **SM-18** | +$50K-$100K+ (licensing) | +30-40% (estimated) | 12-24 months |

**Recommendation**: FSRS offers best ROI for most production apps

---

## Decision Tree

```
1. Are you building an MVP or prototype?
   ├─ Yes → SM-2 (fast, simple, proven)
   └─ No → Go to 2

2. Do you have >10K expected users?
   ├─ Yes → Go to 3
   └─ No → SM-2 (sufficient for small scale)

3. Is user retention critical to business model?
   ├─ Yes → FSRS (20-30% fewer reviews → better retention)
   └─ No → SM-2 (cost-effective)

4. Do you have review history data for training?
   ├─ Yes → FSRS (optimize from day 1)
   └─ No → SM-2 initially, migrate to FSRS after 3-6 months

5. Is licensing cost acceptable?
   ├─ Yes → Evaluate SM-18 (best performance, but licensing fees)
   └─ No → FSRS (open-source, no licensing)

6. Is open-source a requirement?
   ├─ Yes → SM-2 or FSRS only
   └─ No → FSRS or SM-18
```

---

## Summary: Choosing Your Algorithm

### For Fastest Time-to-Market
→ **SM-2** (3-4 weeks MVP, $30K-$50K)

### For Best User Retention
→ **FSRS** (20-30% fewer reviews, 4-6 months, $80K-$150K)

### For Best-in-Class Performance
→ **SM-18** (proprietary licensing, enterprise budget)

### For Open-Source Projects
→ **FSRS** (modern, ML-optimized, free)

### For Budget-Constrained Startups
→ **SM-2** (MVP), migrate to **FSRS** post-PMF

---

**Research Duration**: 2 hours
**Primary Sources**: Medical research papers, app development cost reports, market analysis
**Confidence Level**: High for use cases and development costs, Medium for operating cost estimates (variable by scale)
