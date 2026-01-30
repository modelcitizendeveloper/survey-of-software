# S3-Need-Driven: Recommendation

## Use Case Summary

We analyzed five distinct use cases for Chinese dependency parsing:

1. **NLP Researchers** - Academic benchmarking and model development
2. **Enterprise Translation** - Large-scale MT post-editing and QA
3. **Social Media Analytics** - Sentiment and opinion analysis on Chinese platforms
4. **Multilingual Search** - Cross-lingual IR and question answering
5. **EdTech Language Learning** - Grammar checking and educational feedback

## Pattern Recognition Across Use Cases

### When Stanza is Preferred

**Common characteristics**:
- Multilingual requirements (Chinese + others)
- Standard benchmarks/reproducibility critical
- UD output format needed
- CPU efficiency prioritized
- Clean API and documentation valued
- Team lacks deep NLP expertise

**Use cases where Stanza won**:
- NLP Researchers (UD-native, reproducibility)
- Enterprise Translation (multilingual, CPU-efficient)
- Multilingual Search (80+ languages, UD consistency)
- EdTech (UD-CFL learner corpus, explainable)

**Why**: Stanza's UD-native design, multilingual consistency, and Stanford backing make it the "safe default" for most scenarios.

### When HanLP is Preferred

**Common characteristics**:
- Semantic dependencies needed (not just syntactic)
- Chinese-specific optimization critical
- Multiple NLP tasks required (beyond parsing)
- GPU resources available
- Advanced ML team (comfortable with complexity)

**Use cases where HanLP won**:
- Social Media Analytics (semantic deps for ABSA)
- (Alternative for Translation and Search when semantic features needed)

**Why**: HanLP's semantic dependency parsing and Chinese-specific optimizations fill gaps that Stanza can't address.

### When LTP is Preferred

**Common characteristics**:
- Chinese-only project (confirmed, no future multilingual plans)
- Multi-task efficiency valued (one model, six tasks)
- HIT academic standards preferred
- Comfortable with Chinese documentation

**Use cases where LTP viable**:
- Social Media Analytics (Chinese-only alternative to HanLP)
- (Rarely primary choice, usually "acceptable alternative")

**Why**: LTP's Chinese-only focus is both strength (optimization) and weakness (limits growth). Choose only when Chinese-only is certain.

### When CoreNLP is Avoided

**Across all use cases, CoreNLP was "not recommended" due to**:
- Pre-neural architecture (lower accuracy)
- Java dependency (Python dominates)
- Slower inference (not competitive)
- Maintenance mode (Stanza supersedes)

**Exception**: Legacy Java systems maintenance only.

## Decision Matrix by Requirements

### By Primary Need

| Requirement | Recommended | Alternative | Avoid |
|-------------|-------------|-------------|-------|
| **Multilingual** | Stanza | HanLP | LTP |
| **Semantic deps** | HanLP | LTP | Stanza |
| **CPU efficiency** | Stanza | LTP (MTL) | HanLP (without MTL) |
| **UD compliance** | Stanza | HanLP | LTP (custom) |
| **Chinese-only** | LTP or HanLP | Stanza | CoreNLP |
| **Academic reproducibility** | Stanza | - | CoreNLP (outdated) |
| **Explainability** | Stanza (UD) | HanLP | LTP (less docs) |

### By Organization Type

**Startups / Small Teams**:
- **Recommended**: Stanza (simplest, fastest to integrate)
- **Rationale**: Limited engineering resources, need plug-and-play solution
- **Avoid**: HanLP (steeper learning curve), LTP (Chinese-only limits pivot)

**Research Labs**:
- **Recommended**: Stanza (UD benchmarks, reproducibility)
- **Alternative**: HanLP (semantic deps research)
- **Rationale**: Academic credibility, standard evaluation

**Enterprises**:
- **Recommended**: Stanza or HanLP (depends on use case)
- **Rationale**: Can handle complexity, have ML teams
- **Consider**: Cost optimization (GPU vs CPU), scale requirements

**EdTech**:
- **Recommended**: Stanza (UD-CFL learner corpus)
- **Rationale**: Explainable output, pedagogical value

### By Scale

**Small scale** (<10K sentences/day):
- Any tool works (performance not bottleneck)
- Choose based on features, not speed
- Stanza simplest to deploy

**Medium scale** (10K-1M sentences/day):
- CPU: Stanza (best efficiency)
- GPU: HanLP or LTP (batch processing)
- Horizontal scaling (multiple workers)

**Large scale** (>1M sentences/day):
- GPU clusters required (any neural parser)
- Architecture matters more than parser choice
- Optimize for cost (GPU utilization, caching)

## Anti-Patterns (What NOT to Do)

### Don't Choose Based on Single Metric

**Bad decision**: "HanLP has highest accuracy on CTB, so use it"
- Ignores your use case (do you need CTB-specific accuracy?)
- Ignores your constraints (do you have GPU budget?)
- Ignores your skills (can your team use PyTorch/TensorFlow?)

**Better**: Match tool to complete context (accuracy + speed + ease + future needs).

### Don't Over-Optimize Prematurely

**Bad decision**: "LTP MTL is 20% faster, so use it for everything"
- Ignores multilingual limitation (can't expand to English later)
- Ignores documentation (team struggles with Chinese docs)
- Saves compute, loses engineering velocity

**Better**: Start with simplest (Stanza), optimize if bottleneck proven.

### Don't Ignore Future Requirements

**Bad decision**: "Chinese-only now, so use LTP"
- 6 months later: "We need Japanese parsing"
- Now rebuilding with Stanza (wasted LTP investment)

**Better**: Ask "might we need other languages in 12-24 months?" If uncertain, choose multilingual (Stanza/HanLP).

### Don't Choose Semantic Deps Without Validating Need

**Bad decision**: "Semantic parsing sounds cool, let's use HanLP"
- Downstream models don't actually use semantic features
- Paying GPU cost for unused capabilities
- Could have used simpler Stanza

**Better**: A/B test syntactic vs semantic (measure actual value).

## Recommendation Process

### Step 1: Filter by Hard Constraints

**Multilingual required?**
- Yes → Stanza or HanLP
- No → Any tool (move to Step 2)

**Semantic dependencies required?**
- Yes → HanLP or LTP only
- No → Any tool (move to Step 2)

**Java required?**
- Yes → CoreNLP only (no alternatives)
- No → Any Python tool (move to Step 2)

### Step 2: Match to Use Case Patterns

**Which use case resembles yours most?**
- Academic research → Stanza (UD-native)
- Translation/IR → Stanza (multilingual)
- Social media analysis → HanLP (semantic deps)
- EdTech → Stanza (UD-CFL)

**No match?** Use Stanza as safe default, validate with prototype.

### Step 3: Validate with Prototype

**Build quick test**:
1. Integrate tool (1-2 days)
2. Parse 1K sample sentences from your domain
3. Measure accuracy (manual review or automated if gold labels)
4. Measure latency/throughput (meet requirements?)
5. Assess integration friction (team comfortable with API?)

**Red flags**:
- Accuracy <80% (domain mismatch, need fine-tuning)
- Latency >100ms (optimization needed or different tool)
- Integration frustration (team struggles with API, try simpler tool)

### Step 4: Plan for Production

**Before committing**:
- Read S4 (strategic considerations for long-term)
- Consider maintenance (who updates models, monitors performance?)
- Plan scaling (horizontal workers, GPU procurement, caching)
- Document decision (why this tool, for future team members)

## Confidence Level

**75-85% confidence** - Recommendations based on documented use case patterns and technical analysis. Your specific context may have unique constraints (compliance, existing infrastructure, team skills) that affect the optimal choice.

## When to Seek Additional Guidance

**Consult domain experts if**:
- Accuracy requirements >95% (need custom training, gold evaluation)
- Scale >10M sentences/day (architecture design matters more)
- Regulatory constraints (data residency, model explainability for compliance)
- Novel use case (no pattern match in S3, need custom analysis)

**Read other sections**:
- S1 for quick overview (if you haven't)
- S2 for deep technical details (algorithm trade-offs)
- S4 for strategic considerations (long-term maintenance, ecosystem trends)

## Final Recommendation Summary

**Default choice for most projects**: **Stanza**
- Multilingual (80+ languages)
- UD-native (standard, reproducible)
- CPU-efficient (cost-effective)
- Well-documented (easy to learn)
- Stanford-backed (credible, maintained)

**Choose HanLP when**:
- Semantic dependencies needed
- Chinese-specific optimization critical
- Building comprehensive Chinese NLP pipeline

**Choose LTP when**:
- Chinese-only (confirmed, no multilingual future)
- Multi-task efficiency valued
- Comfortable with HIT standards

**Avoid CoreNLP unless**:
- Maintaining legacy Java system
- Exact research reproduction required

**Key decision factors**:
1. Multilingual requirement (yes → Stanza/HanLP, no → any)
2. Semantic vs syntactic (semantic → HanLP/LTP, syntactic → any)
3. Team skills (NLP experts → HanLP/LTP, generalists → Stanza)
4. Scale/budget (small → Stanza CPU, large → HanLP/LTP GPU)
5. Use case pattern (match to analyzed scenarios)
