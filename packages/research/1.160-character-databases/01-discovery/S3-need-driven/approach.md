# S3: Need-Driven Discovery - Approach

## Methodology: Requirement-First Database Selection

**Time Budget:** 20 minutes
**Philosophy:** "Start with requirements, find exact-fit solutions"
**Goal:** Validate database selection against specific real-world use cases, identify gaps and perfect-fit scenarios

## Discovery Strategy

### 1. Use Case Extraction

**Sources:**
- Common CJK application patterns (IMEs, search engines, e-commerce, learning apps)
- Real-world pain points (Stack Overflow, GitHub issues)
- Production deployments (Android/iOS CJK keyboards, WeChat, Taobao, Duolingo)

**Selection criteria:**
- Representative (covers 80% of applications)
- Diverse (different requirements)
- Testable (can validate database fit)

### 2. Requirement Decomposition

For each use case, identify:
- **Must-have features** (non-negotiable, app fails without these)
- **Nice-to-have features** (improves UX, not critical)
- **Constraints** (performance, cost, licensing, complexity)
- **Failure modes** (what breaks if database is insufficient)

### 3. Database Mapping

**Validation questions:**
- Does the database provide required properties?
- Is performance adequate for use case?
- Is coverage sufficient?
- Is integration complexity acceptable?

**Scoring:**
- ✅ Fully meets requirement
- ⚠️ Partially meets (workarounds needed)
- ❌ Does not meet requirement

### 4. Gap Analysis

Identify:
- Requirements satisfied by multiple databases (redundancy)
- Requirements satisfied by only one database (critical dependency)
- Requirements satisfied by none (external solution needed)

## Use Case Selection Rationale

### Selected Use Cases (5)

1. **Multi-Locale E-Commerce Search** (Cross-border retail)
2. **IME Development** (Handwriting/structure-based input)
3. **Language Learning Application** (Character etymology, mnemonics)
4. **Content Management System** (Multi-region publishing)
5. **CJK Text Analysis** (NLP, sentiment analysis, entity extraction)

### Why These Five?

**Coverage:**
- Use case 1: Represents e-commerce, search engines (high-volume)
- Use case 2: Represents IMEs, handwriting recognition (input methods)
- Use case 3: Represents learning apps, dictionaries (education)
- Use case 4: Represents publishing, CMS (content platforms)
- Use case 5: Represents NLP, AI (emerging applications)

**Diversity:**
- Performance-critical (1, 2) vs quality-critical (3, 5)
- Broad coverage (1, 2, 4) vs deep semantics (3, 5)
- Consumer apps (1, 2, 3) vs enterprise (4, 5)

**Real-world validation:**
- All five exist in production at scale
- Success/failure patterns documented
- Clear requirement boundaries

## Requirement Categories

### Category A: Core Properties
- Character codepoint → properties lookup
- Radical-stroke indexing
- Total stroke count
- Basic definitions

**All databases must provide these.**

### Category B: Cross-Language Support
- Multi-language pronunciation (Mandarin, Japanese, Korean)
- Simplified ↔ Traditional variants
- Regional glyph selection
- Cross-script equivalence

**Critical for multi-locale applications.**

### Category C: Structural Analysis
- IDS decomposition
- Component search
- Hierarchical structure
- Stroke order (if available)

**Critical for IMEs, handwriting, learning.**

### Category D: Semantic Features
- Rich definitions (beyond glosses)
- Etymology (historical forms)
- Semantic relationships (ontology)
- Contextual meaning

**Critical for learning, NLP, research.**

### Category E: Performance & Scale
- Query latency (<1ms, <10ms, <100ms)
- Batch throughput (chars/sec)
- Memory footprint (<100MB, <500MB, <1GB)
- Startup time (<100ms, <1s, <10s)

**Critical for production systems.**

## Validation Methodology

### Step 1: Requirement Checklist

For each use case:
```markdown
## Must-Have Requirements
- [ ] Requirement 1 (property X, performance Y)
- [ ] Requirement 2 (coverage Z)
...

## Nice-to-Have
- [ ] Feature A (improves UX)
- [ ] Feature B (reduces complexity)
...

## Constraints
- Latency: <X ms
- Memory: <Y MB
- Integration: <Z days
- Cost: Open source preferred
```

### Step 2: Database Fit Matrix

```markdown
| Requirement | Unihan | CHISE | IDS | CJKVI | Winner |
|-------------|--------|-------|-----|-------|--------|
| Req 1       | ✅     | ✅    | ❌  | ❌    | Both   |
| Req 2       | ⚠️     | ✅    | ❌  | ❌    | CHISE  |
| ...
```

### Step 3: Integration Complexity Assessment

**Factors:**
- Lines of code required
- Dependencies needed
- Setup time (from zero to working)
- Maintenance burden

**Scale:**
- Low: <50 lines, stdlib only, <1 day
- Medium: <200 lines, few deps, <1 week
- High: >200 lines, complex deps, >1 week

### Step 4: Recommendation

For each use case:
1. **Minimal viable stack** (what's absolutely required)
2. **Recommended stack** (optimal balance)
3. **Overkill stack** (avoid over-engineering)

## Expected Outcomes

### Convergence Patterns

**Strong convergence** (3+ use cases agree):
- "Unihan is mandatory" (expect 5/5 use cases)
- "IDS for structural needs" (expect 3/5 use cases)
- "CJKVI for multi-locale" (expect 2/5 use cases)

**Divergence patterns:**
- Use case 3 (learning) needs CHISE, others don't
- Use case 2 (IME) needs IDS, e-commerce might not

**Insights from divergence:**
- CHISE is niche but irreplaceable for its domain
- IDS is broadly useful but not universal
- CJKVI is conditional on multi-locale requirement

### Gap Identification

**Expected gaps:**
- Stroke order (none of the four databases provide this)
- Word-level dictionaries (character databases don't cover phrases)
- Contextual disambiguation (one-to-many variant mappings)
- Pronunciation in sentences (tone sandhi, readings vary by context)

**Mitigation strategies:**
- External data sources (stroke order databases, word dictionaries)
- NLP augmentation (word segmentation, context analysis)
- User feedback loops (learn from corrections)

## Time Allocation

- **5 min:** Use case requirement extraction
- **10 min:** Database fit validation (all 5 use cases)
- **3 min:** Gap analysis (what's missing)
- **2 min:** Synthesis (recommendations per use case)

**Total: 20 minutes**

## Confidence Targets

**S3 aims for 75-85% confidence** through:
- Real-world use case validation (not hypothetical)
- Requirement checklist (systematic, not gut feel)
- Production examples (Android IME, WeChat search)
- Gap identification (honest about limitations)

## Output Structure

### Per Use Case
1. **Context:** What is the application?
2. **Requirements:** Must-have, nice-to-have, constraints
3. **Database Fit:** Which databases satisfy requirements?
4. **Gap Analysis:** What's missing?
5. **Recommendation:** Minimal/recommended/overkill stacks
6. **Real-World Example:** Production deployment that validates approach

### Final Recommendation
- Use case → database mapping
- Common patterns across use cases
- Conditional recommendations (if X, then Y)

---

**S3 Need-Driven Discovery methodology defined.** Proceeding to use case analysis.
