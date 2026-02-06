# Discovery Table of Contents: Classical Chinese Parsing

## Research Overview

**Topic**: 1.148.2 Classical Chinese Parsing
**Research ID**: research-6xnj
**Focus**: Tools and techniques for parsing Classical Chinese (文言文) texts

## Four-Pass Survey Summary

### S1: Rapid Discovery
Quick assessment of primary tools for Classical Chinese parsing

**Key Finding**: No ready-made production solution exists. Gap between modern Chinese NLP tools and Classical Chinese needs.

**Tools Evaluated**:
- Stanford CoreNLP: Strong for modern Chinese, poor for classical
- ctext.org API: Excellent corpus access, no parsing
- Jiayan: Best for Classical Chinese segmentation, limited beyond that

### S2: Comprehensive Analysis
Deep dive into tools, feature comparison, and implementation options

**Key Finding**: Must build custom solution using existing components. Jiayan + custom POS/parsing + ctext.org corpus is viable path.

**Feature Matrix**: Comprehensive comparison across segmentation, POS tagging, parsing, NER
**Gap Analysis**: Missing pieces include Classical Chinese POS tagger, dependency parser, historical NER
**Implementation Path**: Phased approach - segmentation (Jiayan) → custom POS → custom parsing → NER

### S3: Need-Driven Evaluation
Analysis through concrete use cases

**Key Finding**: Different use cases have different accuracy requirements. Most can tolerate imperfect parsing (70-85%) with good UX.

**Use Cases**:
1. **Reading Assistant** (Educational) - High feasibility, clear market
2. **Document Digitization** (Cultural Preservation) - High impact, institutional funding
3. **Literature Search Engine** (Research) - Academic impact, grant-funded

**Market Validation**: 50K-200K potential users globally, $500K-$5M revenue potential

### S4: Strategic Assessment
Maturity analysis and long-term viability

**Key Finding**: Ecosystem is immature but viable. Strategic window of 2-3 years to establish position.

**Maturity Scores**:
- ctext.org (TRL 8): Essential infrastructure, use with contingency
- Jiayan (TRL 5-6): Best segmenter, fork and maintain
- Stanford CoreNLP (TRL 8 for modern, TRL 3 for classical): Reference only

**Strategic Recommendation**: Hybrid incremental approach - Start with reading assistant, pursue grants, build platform

## Cross-Cutting Themes

### 1. Modern vs Classical Gap
Every modern Chinese NLP tool struggles with Classical Chinese due to:
- Different grammar (classical syntax patterns)
- Different word boundaries (compounds follow different rules)
- Different function words (particles like 也、矣、焉)
- Training data mismatch (corpora are modern Chinese news)

**Implication**: Can't use modern tools off-the-shelf; adaptation or custom building required

### 2. No Standard Annotated Corpus
Unlike modern Chinese (Chinese Treebank), Classical Chinese lacks:
- Large-scale annotated training data
- Standardized POS tagset for classical grammar
- Dependency/constituency treebanks
- Benchmark evaluation datasets

**Implication**: Must create training data or use rule-based approaches initially

### 3. Niche but Global Market
- **Small**: 50K-200K users worldwide (students, researchers)
- **Global**: China, Taiwan, Japan, Korea, Western universities
- **Underserved**: No dominant commercial tools
- **Willing to pay**: Evidence from Pleco, Wenlin sales

**Implication**: Sustainable niche business or grant-funded infrastructure, not venture-scale

### 4. Infrastructure Dependency
All approaches depend critically on:
- **ctext.org** for corpus access
- **Jiayan** for segmentation
- **Academic partnerships** for credibility and funding

**Implication**: Need redundancy (local caching, forks, alternative sources)

## Convergence Analysis

### What All 4 Passes Agree On

1. ✅ **No production-ready solution exists** - Must build custom
2. ✅ **Jiayan is best for segmentation** - Use it as foundation
3. ✅ **ctext.org is essential** - Corpus access critical
4. ✅ **Market is viable but niche** - Right expectations needed
5. ✅ **Incremental approach works** - Don't try to build everything at once

### Where Passes Differ

**S1** says: "Need comprehensive search to find specialized tools"
**S2** confirms: "No specialized tools found, must build"

**S2** says: "Production system requires 6-12 months"
**S3** refines: "Reading assistant: 3-6 months; Full platform: 12-24 months"

**S3** says: "Multiple use cases viable"
**S4** prioritizes: "Start with reading assistant, then digitization, then search"

### Evolution of Understanding

**S1 (Initial Hypothesis)**: Maybe specialized Classical Chinese tools exist but weren't found

**S2 (Comprehensive Search)**: No, specialized tools mostly don't exist. Jiayan is the exception.

**S3 (Market Validation)**: But users need this badly enough to pay. Different use cases have different requirements.

**S4 (Strategic Synthesis)**: The gap is an opportunity. Ecosystem is ready for someone to fill this niche.

## Recommendations by Audience

### For Researchers
**Recommendation**: Use Jiayan for segmentation + ctext.org for corpus access. Build custom analysis tools for your specific needs. Share code with community.

**Why**: Academic timeline allows building custom solutions. Open-source model fits academic culture. Citation credit for shared tools.

### For Product Developers
**Recommendation**: Build reading assistant (freemium model). Use Jiayan + ctext.org + custom POS. Launch beta in 6 months.

**Why**: Fastest path to market, clear user need, manageable scope. Can expand later if successful.

### For Institutions (Libraries, Universities)
**Recommendation**: Apply for NEH Digital Humanities grant. Build document digitization pipeline. Open-source with institutional hosting.

**Why**: Aligns with mission, grant funding available, long-term impact on field.

### For Foundations
**Recommendation**: Fund open-source Classical Chinese NLP platform ($500K-$1M over 3-4 years).

**Why**: Field-building impact, enables research, public good. Underserved area with clear need.

### For Commercial Ed-Tech (Pleco, Skritter, etc.)
**Recommendation**: License or build Classical Chinese parsing features. Add to existing products as premium feature.

**Why**: Existing distribution, incremental revenue, strategic differentiation.

## Implementation Roadmap

Based on insights from all 4 passes:

### Immediate (Month 1)
1. Fork Jiayan (secure segmentation component)
2. Set up ctext.org API access with local caching
3. Create abstraction layer for components
4. Build minimal proof-of-concept

### Short-term (Months 2-6)
1. Develop reading assistant MVP
2. Beta test with 50-100 users
3. Validate willingness to pay
4. Prepare grant application

### Medium-term (Months 7-18)
1. Productize reading assistant OR execute grant
2. Build custom POS tagger (rule-based → ML)
3. Partner with 2-3 universities
4. Grow user base to 1000+

### Long-term (Years 2-5)
1. Full NLP pipeline (parsing, NER)
2. Research tools (search, digitization)
3. Open-source platform
4. Academic consortium governance

## Open Questions & Future Research

### Technical
1. **Transformer approach**: Could BERT/GPT be fine-tuned for Classical Chinese? Might outperform traditional parsing.
2. **Transfer learning**: Can modern Chinese models transfer to Classical with limited training data?
3. **Multi-period models**: Do different dynasties need different models? (Pre-Qin vs Han vs Tang)
4. **Benchmark creation**: What would a standard evaluation dataset look like?

### Market
1. **Willingness to pay**: What's the optimal price point for students? For institutions?
2. **Feature priorities**: What features matter most to users? (Accuracy vs speed vs coverage)
3. **Integration opportunities**: Which existing tools would users want integration with?
4. **Competition timeline**: When will major players (Google, Baidu) enter this space?

### Strategic
1. **Sustainability model**: What mix of grants/subscriptions/services is most stable?
2. **Governance**: What organizational structure ensures long-term maintenance?
3. **Standards**: Should there be a Classical Chinese NLP standard/consortium?
4. **Data sharing**: How to enable community contribution of training data?

## Confidence Levels

### High Confidence (95%+)
- ✅ No production-ready Classical Chinese parser currently exists
- ✅ Jiayan is best available segmentation tool
- ✅ ctext.org is essential infrastructure
- ✅ Market is niche but real

### Medium Confidence (70-95%)
- ⚠️ Hybrid approach (Jiayan + custom) will work
- ⚠️ Reading assistant can reach profitability
- ⚠️ Grant funding is available for this work
- ⚠️ Accuracy of 75-85% is achievable

### Low Confidence (50-70%)
- ❓ Market size estimates (50K-200K users)
- ❓ Revenue potential ($500K-$5M)
- ❓ Timeline estimates (6-24 months)
- ❓ Long-term sustainability model

### Speculation (<50%)
- 🔮 Will transformers (BERT/GPT) replace traditional parsing?
- 🔮 Will major tech companies enter this space?
- 🔮 Will annotated Classical Chinese corpus be created?
- 🔮 What will field look like in 10 years?

## Conclusion

Classical Chinese parsing is an **underserved niche with real user needs and achievable solutions**. The ecosystem is immature but the foundation exists (corpus + segmentation). The path forward is clear: start with reading assistant, pursue grants, build platform incrementally.

**Success requires**:
- Technical competence (Python, NLP, ML)
- Domain knowledge (Classical Chinese linguistics)
- Patience (2-3 years to maturity)
- Realistic expectations (niche market, not venture-scale)

**For the right team with the right expectations, this is a viable and impactful opportunity.**

---

## Document Index

### S1: Rapid Discovery
- `S1-rapid/approach.md` - Evaluation methodology
- `S1-rapid/stanford-corenlp.md` - Initial assessment
- `S1-rapid/ctext-api.md` - Corpus platform overview
- `S1-rapid/recommendation.md` - Quick findings and next steps

### S2: Comprehensive Analysis
- `S2-comprehensive/approach.md` - Deep dive methodology
- `S2-comprehensive/stanford-corenlp.md` - Technical deep dive
- `S2-comprehensive/ctext-api.md` - API and integration details
- `S2-comprehensive/jiayan.md` - Specialized segmenter analysis
- `S2-comprehensive/feature-comparison.md` - Comprehensive matrix
- `S2-comprehensive/recommendation.md` - Implementation paths

### S3: Need-Driven Evaluation
- `S3-need-driven/approach.md` - Use case analysis method
- `S3-need-driven/use-case-reading-assistant.md` - Educational tool
- `S3-need-driven/use-case-document-digitization.md` - Cultural preservation
- `S3-need-driven/use-case-literature-search.md` - Research infrastructure
- `S3-need-driven/recommendation.md` - Market validation and priorities

### S4: Strategic Assessment
- `S4-strategic/approach.md` - Maturity analysis framework
- `S4-strategic/stanford-corenlp-maturity.md` - Ecosystem health
- `S4-strategic/ctext-maturity.md` - Platform sustainability
- `S4-strategic/jiayan-maturity.md` - Open-source project health
- `S4-strategic/recommendation.md` - Strategic options and path forward
