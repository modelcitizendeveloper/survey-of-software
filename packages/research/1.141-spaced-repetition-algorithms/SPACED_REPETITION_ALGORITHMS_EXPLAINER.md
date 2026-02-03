# Spaced Repetition Algorithms: Technical Concepts for Business Stakeholders

**Purpose**: Explain spaced repetition algorithms (SM-2, SM-18, FSRS) and terminology for CTOs, PMs, and technical decision-makers evaluating SRS implementation.

---

## What Are Spaced Repetition Algorithms?

**Spaced repetition algorithms** are mathematical models that optimize the timing of review sessions to maximize long-term memory retention while minimizing study time. These algorithms calculate when a learner should review information based on how well they remembered it previously.

**Analogy**: If traditional studying is like watering plants on a fixed schedule, spaced repetition is like a smart irrigation system that waters each plant precisely when it needs it—less water (study time) for better results (retention).

### Why Spaced Repetition Algorithms Matter

1. **Efficiency**: 50-70% time reduction compared to traditional study methods
2. **Retention**: Scientifically proven to improve long-term memory
3. **Scalability**: Manages thousands of facts without overwhelming learners
4. **Personalization**: Adapts to individual learning patterns

---

## Key Terminology

### Core Concepts

| Term | Definition | Business Impact |
|------|------------|-----------------|
| **Interval** | Time (days) until next review | Longer intervals = less review burden |
| **Easiness Factor (EF)** | Difficulty rating of an item (SM-2) | Lower EF = more frequent reviews needed |
| **Stability (S)** | Duration of memory before 90% recall (FSRS, SM-18) | Higher S = longer intervals possible |
| **Retrievability (R)** | Probability of successful recall (FSRS, SM-18) | Target R = desired retention rate (e.g., 90%) |
| **Difficulty (D)** | Inherent complexity of information (FSRS) | Higher D = slower progress |

### Quality Ratings

| Grade | Meaning | Impact on Next Interval |
|-------|---------|------------------------|
| **Perfect (5)** | Instant recall | Longest interval increase |
| **Correct (4)** | Hesitation but correct | Moderate increase |
| **Difficult (3)** | Hard recall but correct | Small increase |
| **Wrong (0-2)** | Incorrect recall | Interval resets to 1 day |

---

## Algorithm Comparison for Business Stakeholders

### SM-2: The Classic Standard

**Release**: 1988 (38 years proven)
**Used By**: Anki (legacy), Mnemosyne, countless custom apps
**License**: Public domain (free)

**How It Works**:
- Tracks 3 numbers per card: repetitions (n), easiness factor (EF), interval (I)
- Simple formula adjusts EF based on recall quality (0-5 scale)
- Interval doubles/triples each review (1 day → 6 days → 15 days → 38 days...)

**Strengths**:
- ✅ Simple to understand and implement (~50 lines of code)
- ✅ Zero licensing cost (public domain)
- ✅ Proven effectiveness (50-70% time savings)
- ✅ No setup required (works immediately)

**Weaknesses**:
- ❌ Lower performance (47-60% success rate in 2025 benchmarks)
- ❌ Assumes item difficulty never changes
- ❌ Hardcoded first intervals (1 day, 6 days) don't account for individual differences

**Best For**:
- MVPs and prototypes
- Simple flashcard apps
- Budget-constrained projects
- Teams unfamiliar with ML/advanced algorithms

**Example**: Basic language learning app where users rate vocabulary 0-5 after each review

---

### FSRS: The Modern ML-Driven Standard

**Release**: 2023 (3 years, rapidly adopted)
**Used By**: Anki (native since 23.10), RemNote, custom apps
**License**: Open-source (MIT)

**How It Works**:
- Tracks 3 variables per card: Difficulty (D), Stability (S), Retrievability (R)
- Uses 21 parameters optimized by machine learning on user review history
- Predicts forgetting curve: R(t, S) = probability of recall at time t given stability S
- Continuously learns from user's review patterns

**Strengths**:
- ✅ High performance (89.6% success rate in 2025 benchmarks)
- ✅ 20-30% fewer reviews than SM-2 for same retention
- ✅ Dynamic difficulty modeling (adapts as items become easier)
- ✅ Configurable retention target (balance workload vs retention)
- ✅ Open-source, no licensing cost

**Weaknesses**:
- ❌ More complex to implement (~100-200 lines of code)
- ❌ Requires parameter optimization (initial setup: 1-5 minutes per user)
- ❌ Less intuitive than SM-2 (21 parameters vs simple formula)

**Best For**:
- Production applications
- Language learning apps competing with Duolingo
- Medical education platforms
- Apps where user retention is critical

**Example**: Medical student board exam prep app that adapts to individual forgetting patterns

**Sources**:
- [What spaced repetition algorithm does Anki use?](https://faqs.ankiweb.net/what-spaced-repetition-algorithm)
- [FSRS vs SM-2 Guide](https://memoforge.app/blog/fsrs-vs-sm2-anki-algorithm-guide-2025/)

---

### SM-18: The Proprietary Gold Standard

**Release**: 2019 (7 years, proprietary)
**Used By**: SuperMemo 18 (exclusive)
**License**: Proprietary (licensing required)

**How It Works**:
- Two-component memory model: Stability (S) and Retrievability (R)
- Proprietary matrices track stabilization patterns
- Accounts for **anchoring**: new mnemonic context can convert difficult → easy overnight
- Dynamically adjusts item difficulty based on learning patterns

**Strengths**:
- ✅ Best-in-class performance (proprietary benchmarks claim superiority)
- ✅ Most sophisticated model (accounts for changing difficulty)
- ✅ Production-proven (SuperMemo has 30+ year track record)

**Weaknesses**:
- ❌ Proprietary licensing required (cost unknown publicly)
- ❌ SuperMemo exclusive (can't integrate into custom apps easily)
- ❌ Source code not publicly available
- ❌ Not suitable for open-source projects

**Best For**:
- Enterprise budgets with licensing capacity
- Absolute best performance requirement
- SuperMemo integration/licensing deal

**Example**: Enterprise learning platform with SuperMemo licensing agreement

**Sources**:
- [Algorithm SM-18](https://supermemo.guru/wiki/Algorithm_SM-18)
- [SuperMemo Algorithm](https://help.supermemo.org/wiki/SuperMemo_Algorithm)

---

## Performance Benchmarks (2025)

### Success Rate Comparison

| Algorithm | Success Rate | Notes |
|-----------|--------------|-------|
| **LECTOR** (emerging) | 90.2% | LLM-enhanced, high compute cost |
| **FSRS** | 89.6% | Open-source, production-ready |
| **SSP-MMC** | 88.4% | Research algorithm |
| **Anki SM-2** | 60.5% | Anki's modified SM-2 |
| **SM-2** | 47.1% | Original algorithm |
| **SM-18** | Unknown | Proprietary benchmarks only |

**Interpretation**: FSRS is nearly on par with cutting-edge LLM methods while being practical for production

**Sources**:
- [LECTOR: LLM-Enhanced SRS](https://arxiv.org/html/2508.03275v1)
- [Benchmark of Spaced Repetition Algorithms](https://expertium.github.io/Benchmark.html)

### Review Efficiency

**FSRS vs SM-2**:
- **20-30% fewer reviews** for same 90% retention rate
- Example: Medical student saves 20-30 minutes/day while maintaining exam scores

**SM-2 vs Traditional Methods**:
- **50-70% time reduction** compared to cramming or fixed-schedule review

**Sources**:
- [What algorithm does Anki use?](https://faqs.ankiweb.net/what-spaced-repetition-algorithm)

---

## Real-World Use Cases

### Medical Education (Proven ROI)

**Evidence**: KKSOM Class of 2026 study (n=36 students)

**Results**:
- Course I: **+6.4%** exam performance (p < 0.001)
- Course II: **+6.2%** (p = 0.002)
- Course III: **+7.0%** (p = 0.002)
- CBSE: **+12.9%** (p = 0.003)
- Step 1: Daily Anki use → higher scores (p = 0.039)

**Bonus**: Association with **increased sleep quality** (p = 0.01)

**Business Impact**: Medical students using SRS outperform peers by 6-13% while sleeping better

**Sources**:
- [Exploring Impact of Anki on Preclinical Performance](https://journals.sagepub.com/doi/10.1177/23821205251369705)
- [PMC Article](https://pmc.ncbi.nlm.nih.gov/articles/PMC12357012/)

### Language Learning

**Effectiveness**: 50-70% time reduction vs traditional vocabulary drills

**Market Demand**: Primary driver of $1.23B spaced repetition software market (2024)

**Applications**:
- Vocabulary acquisition
- Grammar pattern memorization
- Pronunciation practice

**Sources**:
- [Effective SRS Language Learning](https://www.fluentu.com/blog/learn/srs-spaced-repetition-language-learning/)

### Professional Certification

**Use Cases**:
- Bar exam preparation
- CPA (accounting)
- Technical certifications

**Growth Driver**: Post-pandemic e-learning surge

### Other Applications

- K-12 education
- Corporate training (onboarding, compliance)
- Healthcare (patient education, nursing)

---

## Development Costs (2026)

### Budget Ranges by Complexity

| Complexity | Cost | Timeline | Features |
|------------|------|----------|----------|
| **MVP** | $30K-$80K | 3-4 months | Basic SM-2, local storage, review UI |
| **Medium** | $80K-$150K | 4-6 months | FSRS, cloud sync, analytics, notifications |
| **Complex** | $150K-$250K+ | 6-12 months | AI-driven, multi-platform, advanced features |

### 4-Week MVP Breakdown (SM-2)

| Week | Deliverable | Cost |
|------|-------------|------|
| **Week 1** | Data model, local persistence | $7.5K-$15K |
| **Week 2** | SM-2 scheduling, review UI | $7.5K-$15K |
| **Week 3** | Onboarding, notifications | $7.5K-$15K |
| **Week 4** | Import/export, analytics | $7.5K-$15K |
| **Total** | **Working MVP** | **$30K-$60K** |

**Sources**:
- [How to Implement SRS](https://techbuzzonline.com/spaced-repetition-implementation-guide/)
- [App Development Costs 2026](https://topflightapps.com/ideas/app-development-costs/)

### Cost-Saving Strategies

1. **Cross-Platform Development**: React Native/Flutter saves 30-40% vs native iOS + Android
2. **Open-Source Algorithms**: SM-2 or FSRS (zero licensing cost)
3. **Self-Hosted Infrastructure**: $50-$500/month vs managed services $100-$2K/month

**Sources**:
- [Mobile App Development Cost 2026](https://saigontechnology.com/blog/mobile-app-development-cost/)

---

## Operating Costs

### Infrastructure (Monthly)

| Tier | Cost | Hosting | Use Case |
|------|------|---------|----------|
| **MVP** | $50-$200 | DigitalOcean, AWS t3.medium | <10K users |
| **Growth** | $200-$1K | Load balancing, scaling | 10K-100K users |
| **Scale** | $1K-$10K+ | Multi-region, CDN | 100K+ users |

### Algorithm Licensing

| Algorithm | Cost | Notes |
|-----------|------|-------|
| **SM-2** | **$0** | Public domain |
| **FSRS** | **$0** | Open-source (MIT) |
| **SM-18** | **Unknown** | SuperMemo licensing required |

**Strategic Implication**: Open-source algorithms (SM-2, FSRS) eliminate licensing costs

### Annual Maintenance

**15-20% of development cost** (industry standard)

Example: $100K app → $15K-$20K/year
- Bug fixes: 30-40%
- OS updates: 20-30%
- Feature enhancements: 30-40%
- Security patches: 10-20%

---

## Decision Framework: Which Algorithm to Choose?

### For Fastest Time-to-Market
→ **SM-2** (3-4 weeks, $30K-$50K, zero learning curve)

### For Best User Retention
→ **FSRS** (20-30% fewer reviews, 4-6 months, $80K-$150K)

### For Best-in-Class Performance
→ **SM-18** (proprietary licensing, enterprise budget required)

### For Open-Source Projects
→ **FSRS** (modern, ML-optimized, free)

### For Budget-Constrained Startups
→ **SM-2** (MVP), migrate to **FSRS** post-PMF (product-market fit)

---

## Migration Paths

### SM-2 → FSRS Migration

**Complexity**: Moderate
**Duration**: 2-4 weeks
**Cost**: $10K-$30K

**Process**:
1. Export review history (CSV or database)
2. Map SM-2 state to FSRS state (EF → D/S approximation)
3. Optimize FSRS parameters using review history
4. A/B test with subset of users
5. Gradual rollout

**Anki Example**: Built-in migration takes 1-5 minutes per user, preserves history, can revert

**Sources**:
- [How to use FSRS on Anki](https://forums.ankiweb.net/t/how-to-use-the-next-generation-spaced-repetition-algorithm-fsrs-on-anki/25415)

### FSRS → SM-2 Migration

**Complexity**: High (data loss)
**Duration**: 1-2 weeks
**Cost**: $5K-$15K

**Challenge**: FSRS has 3 variables (D, S, R) → SM-2 has 2 (EF, I)
**Data Loss**: Retrievability (R) discarded, 21 parameters lost

**When Necessary**: Downgrading to simpler system, regulatory compliance (explainability)

### SM-18 → FSRS Migration

**Complexity**: Very High (proprietary state)
**Duration**: 4-8 weeks
**Cost**: $20K-$50K

**Challenge**: SuperMemo state is proprietary, no public mapping
**Approach**: Treat as new FSRS dataset, optimize parameters from scratch

---

## Lock-in Risk Analysis

### Lock-in Scores (0-10 scale, 10 = highest risk)

| Algorithm | Algorithm | Data | Platform | Ecosystem | Knowledge | **Total** | **Risk** |
|-----------|-----------|------|----------|-----------|-----------|-----------|----------|
| **SM-2** | 0 | 1 | 0 | 2 | 2 | **5** | Very Low |
| **FSRS** | 1 | 3 | 0 | 4 | 5 | **13** | Low |
| **SM-18** | 10 | 8 | 9 | 7 | 6 | **40** | Very High |

**Analysis**:
- **SM-2**: Minimal lock-in (public domain, simple state, widely implemented)
- **FSRS**: Low lock-in (open-source, active community, but 21 parameters create data migration complexity)
- **SM-18**: Very high lock-in (proprietary, SuperMemo exclusive, licensing required)

---

## Market Landscape (2026)

### Market Size

- **Spaced Repetition Software**: $1.23B (2024)
- **Flashcard Apps** (broader category): Projected $4B by 2035
- **CAGR**: 6.3% (2025-2035)
- **Education Segment**: $900M (2024)

**Growth Drivers**:
- Personalized/adaptive learning demand
- Scientific validation of SRS
- Expansion beyond education (healthcare, corporate training)
- Post-pandemic e-learning surge

**Sources**:
- [SRS Market Research 2033](https://dataintelo.com/report/spaced-repetition-software-market)
- [Flashcard App Market 2035](https://www.wiseguyreports.com/reports/flashcard-app-market)

### Competitive Landscape

| App | Algorithm | License | Market Position |
|-----|-----------|---------|-----------------|
| **Anki** | SM-2 + FSRS | Open-source | Dominant (medical, academic) |
| **SuperMemo** | SM-18 | Proprietary | Premium (licensing model) |
| **Duolingo** | Custom | Proprietary | Language learning leader |
| **Memrise** | SM-2 variant | Freemium | Language learning |
| **Quizlet** | Basic SRS | Freemium | K-12 education |

**Trend**: Open-source (Anki/FSRS) vs Proprietary (SuperMemo/SM-18) competition

---

## Strategic Recommendations

### For Startups (<10 employees, <$500K revenue)

**Phase 1 (MVP)**: **SM-2**
- Fast implementation (3-4 weeks)
- Zero licensing cost
- Validate product-market fit

**Phase 2 (Post-PMF)**: **Migrate to FSRS**
- After achieving product-market fit
- 20-30% fewer reviews = competitive advantage

**Why not SM-18?**: Licensing cost unjustified for startups

### For Mid-Market (10-100 employees, $500K-$10M revenue)

**Default Choice**: **FSRS**
- Production-ready from day 1
- Proven performance gains
- Open-source eliminates licensing risk

**Alternative**: **SM-2 → FSRS migration** (if already using SM-2)

### For Enterprise (100+ employees, $10M+ revenue)

**Default Choice**: **FSRS** (open-source preferred)

**Alternative**: **SM-18** (if budget allows proprietary licensing)

**Avoid**: SM-2 (insufficient for enterprise scale)

### For Agencies/Consultancies

**Default**: **FSRS**
- Flexibility across clients
- No licensing fees to pass through
- Modern, ML-driven

**Avoid**: SM-18 (client lock-in concerns)

---

## Common Production Patterns

### Pattern 1: Language Learning App (FSRS)

**Stack**: React Native + FSRS + Firebase
**Use Case**: Vocabulary acquisition, grammar drills
**Why FSRS**: 20-30% fewer reviews → better user retention
**Timeline**: 4-6 months MVP → production
**Budget**: $100K-$200K

### Pattern 2: Medical Education Platform (FSRS)

**Stack**: Web app + FSRS + PostgreSQL
**Use Case**: Board exam preparation (USMLE, COMLEX)
**Why FSRS**: Evidence-based (Anki adoption in medical schools)
**Timeline**: 6-9 months MVP → production
**Budget**: $150K-$300K (includes medical content management)

### Pattern 3: Corporate Training (SM-2)

**Stack**: Web app + SM-2 + Company LMS integration
**Use Case**: Compliance training, onboarding
**Why SM-2**: Simple, sufficient for basic retention needs
**Timeline**: 3-6 months MVP → production
**Budget**: $50K-$150K

### Pattern 4: K-12 Educational App (SM-2)

**Stack**: Mobile app + SM-2 + Local storage
**Use Case**: Vocabulary, math facts, science concepts
**Why SM-2**: Simplicity valued, budget constraints (schools)
**Timeline**: 3-4 months MVP → production
**Budget**: $30K-$80K

---

## Glossary of Terms

| Term | Definition |
|------|------------|
| **Spaced Repetition** | Study technique using increasing intervals between reviews |
| **SRS** | Spaced Repetition System/Software |
| **Interval** | Time (days) until next review |
| **Easiness Factor (EF)** | Difficulty rating in SM-2 (1.1 to 2.5) |
| **Stability (S)** | Duration of memory in FSRS/SM-18 (days) |
| **Retrievability (R)** | Probability of recall in FSRS/SM-18 (0-1) |
| **Difficulty (D)** | Inherent complexity in FSRS (higher = harder) |
| **Forgetting Curve** | Mathematical model of memory decay over time |
| **DSR Model** | Difficulty, Stability, Retrievability model (FSRS) |
| **Two-Component Model** | Stability + Retrievability model (SM-18) |
| **Retention Target** | Desired recall probability (e.g., 90%) |
| **Lapse** | Forgetting an item (requires interval reset) |
| **Mature Card** | Item with long interval (e.g., >21 days) |

---

## Resources

### Official Documentation

- [SuperMemo 2 Algorithm](https://super-memory.com/english/ol/sm2.htm)
- [FSRS Algorithm Wiki](https://github.com/open-spaced-repetition/fsrs4anki/wiki/The-Algorithm)
- [SM-18 Documentation](https://supermemo.guru/wiki/Algorithm_SM-18)
- [Anki Manual](https://docs.ankiweb.net/)
- [Open Spaced Repetition GitHub](https://github.com/open-spaced-repetition)

### Research Papers

- [Academic and Wellness Outcomes with Anki - 2023](https://journals.sagepub.com/doi/full/10.1177/23821205231173289)
- [Anki Impact on Preclinical Exam Performance - 2025](https://journals.sagepub.com/doi/10.1177/23821205251369705)
- [LECTOR: LLM-Enhanced SRS - 2025](https://arxiv.org/html/2508.03275v1)

### Implementation Guides

- [How to Implement SRS: Beginner's Guide](https://techbuzzonline.com/spaced-repetition-implementation-guide/)
- [FSRS vs SM-2 Guide](https://memoforge.app/blog/fsrs-vs-sm2-anki-algorithm-guide-2025/)
- [Implementing FSRS in 100 Lines](https://borretti.me/article/implementing-fsrs-in-100-lines)

---

**Last Updated**: 2026-01-16
**Next Review**: When major algorithm versions release or market share shifts significantly
