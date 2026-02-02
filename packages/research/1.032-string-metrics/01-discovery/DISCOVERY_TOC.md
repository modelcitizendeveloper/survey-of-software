# Discovery Table of Contents: String Metric Libraries

## Quick Navigation

- **New to string similarity?** Start with [DOMAIN_EXPLAINER.md](../DOMAIN_EXPLAINER.md)
- **Need a quick decision?** Read [S1 Rapid Discovery](#s1-rapid-discovery)
- **Deep technical dive?** Go to [S2 Comprehensive Analysis](#s2-comprehensive-analysis)
- **Know your exact use case?** Check [S3 Need-Driven Discovery](#s3-need-driven)
- **Long-term planning?** Review [S4 Strategic Selection](#s4-strategic)

---

## S1: Rapid Discovery

**Goal:** Quick library comparison for fast decision-making

**Time to read:** 15-20 minutes

### Contents

- [Approach](S1-rapid/approach.md) - Methodology and decision criteria
- [rapidfuzz](S1-rapid/rapidfuzz.md) - Python, C++ core, production-grade performance
- [textdistance](S1-rapid/textdistance.md) - Python, 40+ algorithms, research-friendly
- [string-similarity](S1-rapid/string-similarity.md) - JavaScript, lightweight, zero deps
- [strsim](S1-rapid/strsim.md) - Rust, memory-safe, systems programming
- [apache-commons-text](S1-rapid/apache-commons-text.md) - Java, enterprise-stable
- [Recommendation](S1-rapid/recommendation.md) - Decision flowchart and quick selection guide

**Key outputs:**
- Algorithm → Library mapping
- Ecosystem-specific recommendations
- When to deep-dive vs when to decide now

---

## S2: Comprehensive Analysis

**Goal:** Technical deep-dive for architecture and implementation decisions

**Time to read:** 45-60 minutes

### Contents

- [Approach](S2-comprehensive/approach.md) - Technical evaluation methodology
- [rapidfuzz - Technical](S2-comprehensive/rapidfuzz.md) - Performance benchmarks, API design, integration patterns
- [textdistance - Technical](S2-comprehensive/textdistance.md) - Algorithm catalog, extensibility, pure Python vs C backends
- [Feature Comparison Matrix](S2-comprehensive/feature-comparison.md) - Algorithm coverage, performance, API ergonomics, unicode support
- [Recommendation](S2-comprehensive/recommendation.md) - Optimization strategies, profiling templates, integration best practices

**Key outputs:**
- Benchmark data (ops/sec, latency, memory)
- Algorithm complexity analysis
- Integration code examples
- Performance tuning strategies

**Use this section when:**
- Performance requirements are strict (SLA-driven)
- Choosing between similar libraries (rapidfuzz vs textdistance)
- Implementing production systems (need optimization guidance)
- Evaluating algorithm trade-offs (Levenshtein vs Jaro-Winkler)

---

## S3: Need-Driven Discovery

**Goal:** Map real-world use cases to technical requirements

**Time to read:** 30-40 minutes

### Contents

- [Approach](S3-need-driven/approach.md) - User-centered research methodology
- [E-commerce Search](S3-need-driven/use-case-ecommerce-search.md) - Autocomplete, typo tolerance, product discovery
- [Data Deduplication](S3-need-driven/use-case-data-deduplication.md) - Record linkage, master data management, CRM cleanup
- [Developer Tools/CLI](S3-need-driven/use-case-developer-tools.md) - Command suggestions, IDE autocomplete, config validation
- [Recommendation](S3-need-driven/recommendation.md) - Use case → Algorithm mapping, validation checklists, anti-patterns

**Key outputs:**
- WHO needs string metrics (personas)
- WHY they need it (pain points, business impact)
- Requirements and constraints by use case
- Success criteria and validation questions

**Use this section when:**
- Validating if string metrics solve your problem
- Defining requirements (precision, recall, latency)
- Building business case for implementation
- Checking if your use case is common (learn from others)

---

## S4: Strategic Selection

**Goal:** Long-term viability analysis for informed architectural decisions

**Time to read:** 25-35 minutes

### Contents

- [Approach](S4-strategic/approach.md) - Strategic evaluation methodology
- [rapidfuzz Viability](S4-strategic/rapidfuzz-viability.md) - Ecosystem health, maintenance burden, vendor risk
- [Recommendation](S4-strategic/recommendation.md) - TCO analysis, organizational fit, multi-year trends, decision template

**Key outputs:**
- 5-year total cost of ownership estimates
- Bus factor and abandonment risk assessment
- Organizational fit by risk tolerance
- Migration path considerations
- Build vs integrate vs buy decision framework

**Use this section when:**
- Making multi-year architectural decisions
- Evaluating organizational risk (low-risk vs high-risk orgs)
- Planning for team growth (hiring, skills)
- Concerned about dependency health and vendor lock-in

---

## Reading Paths

### Quick Decision (15-30 minutes)
1. Read S1 Approach + Recommendation
2. Skim S1 for your language ecosystem
3. Validate with S3 use case (if matches)
4. Decide and implement

### Thorough Analysis (2-3 hours)
1. Read DOMAIN_EXPLAINER (if new to domain)
2. Read S1 Rapid Discovery (context)
3. Read S4 Strategic (long-term fit)
4. Deep-dive S2 for technical details
5. Validate with S3 use case
6. Make informed decision

### Domain Learning (4-6 hours)
1. Read DOMAIN_EXPLAINER
2. Read S1 Rapid Discovery
3. Study S3 use cases (all 3)
4. Skim S2 for algorithm understanding
5. Read S4 for ecosystem context
6. Build proof-of-concept

### Architectural Planning (1-2 days)
1. Read S4 first (strategic context)
2. Read S3 to validate use case fit
3. Deep-dive S2 for implementation details
4. Use S1 as quick reference
5. Draft architecture doc
6. Build POC and validate assumptions

---

## Cross-References

### By Algorithm Type

**Edit Distance (Levenshtein, Damerau-Levenshtein):**
- S1: rapidfuzz, textdistance, strsim
- S2: Performance benchmarks, optimization strategies
- S3: Typo tolerance, CLI suggestions

**Jaro-Winkler:**
- S1: rapidfuzz, strsim, Apache Commons Text
- S2: Name matching implementations
- S3: Medical records, person name matching

**Token-Based (Jaccard, Dice):**
- S1: textdistance, string-similarity
- S2: Multi-word comparison strategies
- S3: E-commerce product matching, company name deduplication

**Cosine Similarity:**
- S1: textdistance (Python), strsim (Rust)
- S2: Document similarity patterns
- S3: Long-text comparison, semantic search

### By Use Case

**Search/Autocomplete:**
- S1: string-similarity (frontend), rapidfuzz (backend)
- S2: Latency optimization, caching strategies
- S3: E-commerce search use case

**Data Quality:**
- S1: rapidfuzz (Python), Apache Commons (Java)
- S2: Multi-field weighted similarity
- S3: Data deduplication use case

**Developer Experience:**
- S1: strsim (Rust), leven (Go)
- S2: Binary size optimization
- S3: CLI tools use case

### By Language Ecosystem

**Python:**
- S1: rapidfuzz vs textdistance decision
- S2: Performance comparison, API patterns
- S3: Integration with Django, Flask, FastAPI
- S4: Ecosystem health, TCO analysis

**JavaScript:**
- S1: string-similarity (primary recommendation)
- S2: Frontend bundle size considerations
- S3: React/Vue autocomplete patterns

**Rust:**
- S1: strsim (primary recommendation)
- S2: Memory safety, no_std support
- S3: CLI tools, systems programming
- S4: Ecosystem maturity, community governance

**Java:**
- S1: Apache Commons Text (primary recommendation)
- S2: JVM optimization, thread safety
- S3: Spring integration, enterprise patterns
- S4: Apache Foundation backing, institutional stability

---

## Research Completeness

This discovery covers:
- ✅ 5 major libraries across 4 language ecosystems
- ✅ 6+ string similarity algorithms (Levenshtein, Jaro-Winkler, Hamming, LCS, Jaccard, Cosine)
- ✅ 3 detailed use cases with personas
- ✅ Performance benchmarks and optimization strategies
- ✅ Strategic viability and TCO analysis
- ✅ Integration patterns for 8+ frameworks

**What's NOT covered:**
- Domain-specific libraries (genomics, chemistry)
- Proprietary/commercial solutions (assume open-source preference)
- Experimental algorithms (academic research without production use)
- Non-English-centric languages (CJK, Arabic - see separate research topics)

**Next steps after reading:**
1. Select library based on your decision path
2. Build proof-of-concept on your data
3. Validate performance and accuracy metrics
4. Tune thresholds based on real-world results
5. Deploy to production with monitoring

---

## Feedback and Contributions

This research reflects the library ecosystem as of January 2025. String metric libraries evolve:
- New libraries emerge
- Performance improves
- Ecosystems shift

**If you notice:**
- Outdated benchmark numbers
- New libraries worth including
- Use cases not covered

Consider this research a starting point, not absolute truth. Always validate with your specific data and requirements.
