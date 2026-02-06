# Chinese Dependency Parsing - Discovery Table of Contents

## How to Use This Research

**Choose your approach based on time and depth needs:**

### Quick Decision (15-30 minutes)
1. Read **DOMAIN_EXPLAINER.md** (if new to dependency parsing)
2. Read **S1-rapid/recommendation.md** (quick library comparison)
3. Pick the recommended tool, start prototyping

### Deep Analysis (2-3 hours)
1. **DOMAIN_EXPLAINER.md** (understand the problem space)
2. **S1-rapid/** (ecosystem overview)
3. **S4-strategic/recommendation.md** (long-term considerations)
4. **S2-comprehensive/feature-comparison.md** (technical details)
5. **S3-need-driven/** (find your use case)

### Architecture Planning (4-6 hours)
1. All of the above, plus:
2. **S2-comprehensive/** library deep-dives (technical architecture)
3. **S3-need-driven/** all use cases (understand trade-offs)
4. **S4-strategic/** viability analyses (risk assessment)

---

## Content Structure

### Domain Explainer (Start Here if New)
- **DOMAIN_EXPLAINER.md** - Universal analogies, when to use, trade-offs, implementation reality

### S1-Rapid: Ecosystem Scan (5-10 min read per file)

**Purpose**: Quick landscape overview for time-constrained decisions

- **approach.md** - Methodology and philosophy
- **universal-dependencies.md** - Framework and treebank collection
- **stanford-corenlp.md** - Legacy Java NLP suite
- **hanlp.md** - Modern multilingual neural library
- **stanza.md** - Stanford's neural Python toolkit
- **ltp.md** - HIT's Chinese-focused platform
- **recommendation.md** - Quick decision matrix

**Key takeaway**: Stanza for most projects, HanLP for semantic deps, LTP for Chinese-only, CoreNLP for legacy.

### S2-Comprehensive: Technical Analysis (20-30 min read per file)

**Purpose**: Deep technical understanding for informed decision-making

- **approach.md** - Methodology and evaluation framework
- **universal-dependencies.md** - UD format, treebanks, CoNLL-U specification
- **stanford-corenlp.md** - Graph-based parsing, pre-neural architecture, Java deployment
- **hanlp.md** - Biaffine parser, semantic deps, MTL architecture, PyTorch/TensorFlow
- **stanza.md** - Transition-based parsing, UD-native design, PyTorch, 80+ languages
- **ltp.md** - Knowledge distillation, MTL efficiency, HIT standards, Chinese optimization
- **feature-comparison.md** - Algorithm comparison, output formats, deployment patterns
- **recommendation.md** - Technical decision framework, performance analysis

**Key takeaway**: Algorithm trade-offs (transition vs graph vs biaffine), output formats (UD vs custom), deployment considerations.

### S3-Need-Driven: Use Case Analysis (15-20 min read per file)

**Purpose**: Match your specific scenario to library strengths

- **approach.md** - Requirements-first methodology
- **use-case-nlp-researchers.md** - Academic benchmarking, UD-native reproducibility → **Stanza**
- **use-case-enterprise-translation.md** - Large-scale MT/QA, multilingual pipelines → **Stanza + REST**
- **use-case-social-media-analytics.md** - Sentiment/opinion analysis, semantic deps → **HanLP**
- **use-case-multilingual-search.md** - Cross-lingual IR, query understanding → **Stanza**
- **use-case-edtech-language-learning.md** - Grammar checking, learner corpus → **Stanza (UD-CFL)**
- **recommendation.md** - Pattern recognition, decision matrix by requirements

**Key takeaway**: Stanza for 4/5 use cases (multilingual, UD, clean API), HanLP when semantic deps needed.

### S4-Strategic: Long-Term Viability (20-30 min read per file)

**Purpose**: Assess 2-5 year risks and ecosystem trends

- **approach.md** - Strategic methodology, time horizon, dimensions analyzed
- **stanza-viability.md** - Stanford backing, UD alignment, ecosystem health, exit strategy
- **recommendation.md** - Ecosystem trends, viability assessment, risk mitigation, team building

**Key takeaway**: Stanza safest long-term (Stanford, UD, healthy ecosystem). UD is winning standard. Multilingual parsers have economies of scale.

---

## Reading Paths by Role

### Software Engineer (New to NLP)
1. **DOMAIN_EXPLAINER.md** (understand problem)
2. **S1-rapid/recommendation.md** (quick choice)
3. **S3-need-driven/** (find similar use case)
4. Start prototyping with recommended tool

### ML Engineer
1. **S1-rapid/** (ecosystem overview)
2. **S2-comprehensive/feature-comparison.md** (algorithms, performance)
3. **S2-comprehensive/[tool].md** (deep-dive your top 2 choices)
4. **S3-need-driven/recommendation.md** (validation)

### Product Manager / Architect
1. **DOMAIN_EXPLAINER.md** (understand trade-offs)
2. **S1-rapid/recommendation.md** (quick landscape)
3. **S3-need-driven/** (find your use case)
4. **S4-strategic/recommendation.md** (long-term planning)

### Researcher
1. **S1-rapid/** (quick ecosystem scan)
2. **S2-comprehensive/** (technical deep-dive)
3. **S3-need-driven/use-case-nlp-researchers.md** (academic workflows)
4. **S4-strategic/stanza-viability.md** (reproducibility, community)

### Decision Maker (Busy, Need Summary)
1. **S1-rapid/recommendation.md** (5 minutes: decision matrix)
2. **S3-need-driven/recommendation.md** (10 minutes: use case patterns)
3. **S4-strategic/recommendation.md** (10 minutes: strategic risks)
4. **Total: 25 minutes for informed decision**

---

## Key Insights by Section

### From S1-Rapid
- **Stanza**: Most balanced (multilingual, UD, Stanford-backed)
- **HanLP**: Feature-rich (semantic deps, 130+ languages, MTL)
- **LTP**: Chinese-optimized (knowledge distillation, HIT standards)
- **CoreNLP**: Legacy (maintenance mode, use Stanza for new projects)

### From S2-Comprehensive
- **Algorithms**: Transition-based (fast), graph-based (global optimal), biaffine (SOTA neural)
- **Output formats**: UD CoNLL-U is standard (all modern parsers support)
- **Performance**: 85-95% UAS/LAS typical, domain-specific fine-tuning improves
- **Deployment**: CPU for latency, GPU for throughput, REST for microservices

### From S3-Need-Driven
- **Multilingual required** → Stanza (80+ langs) or HanLP (130+ langs)
- **Semantic deps required** → HanLP or LTP (Stanza is syntactic only)
- **CPU efficiency** → Stanza (transition-based, linear time)
- **Chinese-only** → LTP or HanLP (but Stanza still viable)

### From S4-Strategic
- **UD is winning** (100+ languages, academic/industry adoption)
- **Transformers dominate** (pre-neural parsers obsolete)
- **Stanza safest bet** (Stanford, UD, healthy ecosystem)
- **LLMs don't replace** (yet - 5+ year runway for dedicated parsers)

---

## Common Questions Answered

### "Which library should I use?"
**Short answer**: Stanza for most projects.
**Long answer**: Read S1-rapid/recommendation.md (decision matrix) and S3-need-driven/recommendation.md (use case patterns).

### "What's the difference between syntactic and semantic parsing?"
**Syntactic** (Stanza, CoreNLP): Grammatical structure (subject, object, modifier) - tree
**Semantic** (HanLP, LTP): Meaning structure (agent, patient, location) - graph
**When to care**: Semantic matters for question answering, knowledge graphs, opinion analysis.

### "How accurate are these parsers?"
**Typical**: 85-95% UAS/LAS on standard benchmarks
**Your domain**: May be lower (legal, medical, social media differ from news)
**Mitigation**: Fine-tune on domain corpus (100-1000+ annotated sentences)
**Read**: S2-comprehensive/feature-comparison.md (performance analysis)

### "Do I need GPU?"
**No, but**: GPU is 10-50x faster for batch processing
**CPU sufficient for**: Prototyping, low volume (<1K sentences/day), real-time single sentences
**GPU recommended for**: Production scale (>10K sentences/day), fine-tuning models
**Read**: S2-comprehensive/recommendation.md (resource considerations)

### "Can I use this for Japanese/Korean/other languages?"
**Stanza**: Yes (80+ languages)
**HanLP**: Yes (130+ languages)
**LTP**: No (Chinese-only)
**CoreNLP**: Limited (8 languages)
**Read**: S2-comprehensive/feature-comparison.md (multilingual capabilities)

### "How long does implementation take?"
**Prototype**: 1-2 weeks (use pre-trained models)
**Production**: 2-4 months (integration, optimization, monitoring)
**Custom training**: 6-12 months (annotation, architecture, evaluation)
**Read**: DOMAIN_EXPLAINER.md (implementation reality section)

### "What's the long-term risk?"
**Stanza**: Very low (Stanford-backed, UD-aligned, healthy community)
**HanLP**: Low (active development, but individual-led)
**LTP**: Moderate (Chinese-only limits ecosystem, academic funding)
**CoreNLP**: High (maintenance mode, pre-neural, superseded by Stanza)
**Read**: S4-strategic/recommendation.md (viability assessment)

---

## Research Metadata

**Topic**: 1.153.1 Chinese Dependency Parsing
**Methodology**: 4PS (Rapid, Comprehensive, Need-Driven, Strategic)
**Libraries Analyzed**: UD, CoreNLP, HanLP, Stanza, LTP
**Primary Recommendation**: Stanza (balanced, multilingual, UD-native)
**Alternative**: HanLP (semantic deps, Chinese focus)
**Date**: 2026-01-30
**Confidence**: S1: 70-80%, S2: 80-90%, S3: 75-85%, S4: 60-70%
