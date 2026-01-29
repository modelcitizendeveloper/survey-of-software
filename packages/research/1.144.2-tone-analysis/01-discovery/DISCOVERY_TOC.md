# Discovery Table of Contents

## Overview

This directory contains comprehensive research on tone analysis technology for CJK languages, following the 4-Pass Structure (4PS):

- **S1 Rapid:** Quick survey of available libraries
- **S2 Comprehensive:** Deep technical analysis
- **S3 Need-Driven:** Use case-specific recommendations
- **S4 Strategic:** Market viability and long-term outlook

---

## S1: Rapid Pass (Initial Survey)

**Objective:** Quick identification of viable libraries for tone analysis

### Files
- [approach.md](S1-rapid/approach.md) - Research methodology
- [librosa.md](S1-rapid/librosa.md) - Python audio analysis library (pure Python)
- [praatio.md](S1-rapid/praatio.md) - Praat TextGrid manipulation from Python
- [recommendation.md](S1-rapid/recommendation.md) - Initial recommendation (Parselmouth winner)

### Key Findings
- **Discovered:** Parselmouth (not originally in spec, but superior to praatio)
- **Recommendation:** Parselmouth > librosa > praatio for most use cases
- **Libraries:**
  - Parselmouth: Praat-equivalent accuracy (r=0.999), zero dependencies
  - librosa: Pure Python, lower accuracy (r=0.730 for F0 mean)
  - praatio: Requires external Praat, primarily for TextGrid manipulation

---

## S2: Comprehensive Pass (Deep Dive)

**Objective:** Detailed technical analysis of tone analysis ecosystem

### Files
- [approach.md](S2-comprehensive/approach.md) - Research scope and methodology
- [01-parselmouth-deep-dive.md](S2-comprehensive/01-parselmouth-deep-dive.md) - Complete Parselmouth API and benchmarks
- [02-librosa-advanced.md](S2-comprehensive/02-librosa-advanced.md) - pYIN vs YIN vs piptrack comparison
- [03-praatio-textgrid-manipulation.md](S2-comprehensive/03-praatio-textgrid-manipulation.md) - TextGrid API details
- [04-tone-classification-algorithms.md](S2-comprehensive/04-tone-classification-algorithms.md) - HMM, CNN, RNN, hybrid approaches
- [05-tone-sandhi-detection.md](S2-comprehensive/05-tone-sandhi-detection.md) - Rule-based, ML-based, hybrid strategies
- [06-comparative-analysis.md](S2-comprehensive/06-comparative-analysis.md) - Performance benchmarks and decision tree
- [README.md](S2-comprehensive/README.md) - Navigation guide and quick reference
- [recommendation.md](S2-comprehensive/recommendation.md) - Production stack recommendations

### Key Findings
- **Pitch Detection:** Parselmouth (r=0.999 with Praat) recommended for production
- **Tone Classification:** CNN (87-88% accuracy) for production, CNN-LSTM-Attention (90%+) for state-of-the-art
- **Tone Sandhi:** Hybrid (Rule-based + CNN verification) achieves 97%+ accuracy
- **Recommended Stack:** Parselmouth + CNN + Hybrid sandhi (~$12K Year 1, 87-88% accuracy)

---

## S3: Need-Driven Pass (Use Case Analysis)

**Objective:** Map technology choices to specific user needs

### Files
- [approach.md](S3-need-driven/approach.md) - Use case selection methodology
- [use-case-01-pronunciation-practice.md](S3-need-driven/use-case-01-pronunciation-practice.md) - Mobile app for language learners
- [use-case-02-speech-recognition.md](S3-need-driven/use-case-02-speech-recognition.md) - ASR F0 feature extraction
- [use-case-03-linguistic-research.md](S3-need-driven/use-case-03-linguistic-research.md) - Academic phonetics studies
- [use-case-04-content-creation.md](S3-need-driven/use-case-04-content-creation.md) - Quality control for audiobooks/podcasts
- [use-case-05-clinical-assessment.md](S3-need-driven/use-case-05-clinical-assessment.md) - Speech therapy diagnostics
- [recommendation.md](S3-need-driven/recommendation.md) - Decision matrix and cross-cutting insights

### Key Findings by Use Case

| Use Case | Stack | Timeline | Budget | Critical Factor |
|----------|-------|----------|--------|-----------------|
| Pronunciation Practice | PESTO + Lightweight CNN + Mobile | 4-8 weeks | $50-60K | Latency (<200ms) |
| Speech Recognition | Parselmouth + CNN + Python | 2-4 weeks | $17-37K | Accuracy (r>0.95) |
| Linguistic Research | Parselmouth + Manual verification + R | 1-2 months | $15-20K | Praat compatibility |
| Content Creation | Parselmouth + Whisper + GUI | 3-6 months | $62-68K | Low false positives |
| Clinical Assessment | Parselmouth + Rule-based + Desktop | 12 months | $230-380K | Regulatory compliance |

---

## S4: Strategic Pass (Viability Analysis)

**Objective:** Assess long-term market and technology viability (3-5 year horizon)

### Files
- [approach.md](S4-strategic/approach.md) - Strategic assessment framework (TRL scale)
- [ecosystem-maturity.md](S4-strategic/ecosystem-maturity.md) - Datasets, tools, talent, commercial landscape
- [technology-risks.md](S4-strategic/technology-risks.md) - Limitations, failure modes, mitigation
- [market-viability.md](S4-strategic/market-viability.md) - Market sizing, business models, competition
- [regulatory-landscape.md](S4-strategic/regulatory-landscape.md) - FDA, HIPAA, GDPR, AI Act
- [future-outlook.md](S4-strategic/future-outlook.md) - Research trends, 3-5 year projections
- [recommendation.md](S4-strategic/recommendation.md) - Go/No-Go assessment, strategic priorities

### Key Findings

**Technology Readiness:**
- Pitch detection: TRL 9 (production-ready)
- Tone classification: TRL 7 (early production)
- Clinical applications: TRL 5-6 (research-grade)

**Market Opportunity:**
- Total Addressable Market (TAM): $4.4B language learning
- Serviceable Addressable Market (SAM): $100M-150M tone-specific
- Growing 17% CAGR

**Critical Risks:**
- Commoditization by Big Tech (40-50% probability by 2028-2029)
- Accuracy plateau at 87-90% (hard to exceed without breakthroughs)
- Regulatory complexity for clinical tools (2-5 year timeline, $100K-500K)

**Strategic Recommendation:**
- **GO:** Pronunciation practice and ASR use cases (launch 2026)
- **WAIT:** Clinical assessment (requires 3-5 years validation)
- **Build data moat early** (collect learner data 2026-2027) before commoditization
- **Monitor foundation models** (2028-2029) for potential pivot

---

## Cross-Pass Insights

### When to Use Which Tool

**Parselmouth (Recommended for Most Use Cases):**
- ✅ Publication-grade accuracy (r=0.999 with Praat)
- ✅ Zero dependencies (precompiled wheels)
- ✅ Complete Praat functionality from Python
- ❌ Slower (2-3s per file) - not suitable for real-time (<50ms)

**PESTO (For Real-Time Applications):**
- ✅ Ultra-low latency (<10ms)
- ✅ Tiny model (0.1 MB)
- ✅ Mobile-friendly
- ❌ Slightly lower accuracy than Parselmouth

**librosa (When Pure Python Required):**
- ✅ No external dependencies
- ✅ Probabilistic pYIN (uncertainty estimates)
- ❌ Lower accuracy (r=0.730 for F0 mean)
- ❌ Not recommended for production unless Praat install impossible

**CREPE (For Highest Accuracy):**
- ✅ State-of-the-art deep learning approach
- ✅ GPU-accelerated
- ❌ Requires GPU
- ❌ Larger model (64 MB)

### Tone Classification Approaches

| Approach | Accuracy | Use When | Cost (Year 1) |
|----------|----------|----------|---------------|
| Rule-based | 80-85% | Prototype, explainability required, low budget | ~$1K |
| CNN (ToneNet) | 87-88% | Production (most use cases) | ~$10K |
| RNN/LSTM | 88-90% | Tone sandhi learning, sequential context | ~$15K |
| CNN-LSTM-Attention | 90%+ | State-of-the-art accuracy needed | ~$22K |

### Tone Sandhi Detection

| Approach | Accuracy | False Positives | Use When |
|----------|----------|-----------------|----------|
| Rule-based only | 88-97% | Medium | Prototype, budget-constrained |
| CNN only | 97%+ | Low (<1.9%) | Discovering new patterns, data-rich |
| Hybrid (Rule+CNN) | 97%+ | Very low | Production (best precision) |

---

## Quick Start Guides

### For Pronunciation Practice App
1. Start with S3 [use-case-01-pronunciation-practice.md](S3-need-driven/use-case-01-pronunciation-practice.md)
2. Review S2 [01-parselmouth-deep-dive.md](S2-comprehensive/01-parselmouth-deep-dive.md) for PESTO vs. Parselmouth trade-off
3. Check S4 [market-viability.md](S4-strategic/market-viability.md) for business model options

### For ASR Engineers
1. Start with S3 [use-case-02-speech-recognition.md](S3-need-driven/use-case-02-speech-recognition.md)
2. Review S2 [04-tone-classification-algorithms.md](S2-comprehensive/04-tone-classification-algorithms.md) for feature engineering
3. See S2 [02-librosa-advanced.md](S2-comprehensive/02-librosa-advanced.md) for parameter tuning

### For Linguistic Researchers
1. Start with S3 [use-case-03-linguistic-research.md](S3-need-driven/use-case-03-linguistic-research.md)
2. Review S2 [01-parselmouth-deep-dive.md](S2-comprehensive/01-parselmouth-deep-dive.md) for Praat compatibility
3. See S1 [recommendation.md](S1-rapid/recommendation.md) for why Parselmouth > praatio

### For Clinical Applications
1. Start with S3 [use-case-05-clinical-assessment.md](S3-need-driven/use-case-05-clinical-assessment.md)
2. **CRITICAL:** Review S4 [regulatory-landscape.md](S4-strategic/regulatory-landscape.md) for FDA/HIPAA requirements
3. Check S4 [recommendation.md](S4-strategic/recommendation.md) for TRL assessment (currently TRL 5-6, not production-ready)

### For Content Creators/QC Tools
1. Start with S3 [use-case-04-content-creation.md](S3-need-driven/use-case-04-content-creation.md)
2. Review S2 [06-comparative-analysis.md](S2-comprehensive/06-comparative-analysis.md) for accuracy vs. false positive trade-offs
3. Check S4 [market-viability.md](S4-strategic/market-viability.md) for pricing and positioning

---

## Research Artifacts

### Datasets Identified
- **AISHELL-1:** 170+ hours, 400 speakers, open-source (most popular)
- **AISHELL-3:** 85 hours, 218 speakers, high quality (best for training)
- **THCHS-30:** 30 hours, 60 speakers, academic standard
- **KeSpeech:** 1,542 hours, multi-domain (largest corpus)

### Pre-trained Models
- **Limited availability** (mostly research code, few production-ready models)
- **WeNet, FunASR** provide Mandarin ASR models (can be adapted)
- **Expect "Whisper for tones"** by 2028-2029 (foundation model)

### Commercial Tools
- **Chinese Tone Gym** (B2C, $20/month)
- **CPAIT** (clinical, research-grade)
- **iFlytek, Alibaba Cloud** (B2B enterprise ASR)
- **Market is fragmented** (no dominant player)

---

## Common Pitfalls (From All Passes)

1. **Optimizing wrong metric** (S3: latency vs. accuracy vs. cost)
2. **Assuming one-size-fits-all** (S3: different use cases need different stacks)
3. **Over-engineering MVP** (S3: ship rule-based first, iterate)
4. **Ignoring regulatory early** (S4: FDA/HIPAA adds 12-24 months)
5. **Underestimating commoditization** (S4: Big Tech may dominate by 2028-2029)
6. **Skipping validation** (S2, S3, S4: test on target population before launch)

---

## Next Steps

After completing discovery research:

1. **Choose use case** based on S3 analysis and S4 strategic recommendation
2. **Select technology stack** using S2 comparative analysis
3. **Validate assumptions** with pilot study (10-50 users)
4. **Build MVP** following use case-specific guide from S3
5. **Measure success** using metrics defined in S3
6. **Monitor ecosystem** for foundation model breakthroughs (S4 future outlook)

---

## Research Lineage

- **Researched by:** Ivan (research/crew/ivan)
- **Date:** January 2026
- **Total documents:** 25+ files across 4 passes
- **Total size:** ~400 KB
- **Bead ID:** research-bo34 (1.144.2 Tone Analysis)

See [../DOMAIN_EXPLAINER.md](../DOMAIN_EXPLAINER.md) for non-technical overview and decision criteria.
