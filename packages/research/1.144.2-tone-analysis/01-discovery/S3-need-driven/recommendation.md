# S3 Need-Driven Pass: Recommendation

## Executive Summary

After analyzing five distinct use cases, the **optimal tone analysis stack varies significantly by user needs**. There is no one-size-fits-all solution.

### Quick Decision Matrix

| Use Case | Pitch | Tone Classifier | Sandhi | Interface | Timeline | Budget |
|----------|-------|-----------------|--------|-----------|----------|--------|
| **Pronunciation Practice** | PESTO | Rule-based | Skip | Mobile app | 4-8 weeks | $50-60K |
| **Speech Recognition** | Parselmouth | Pre-trained CNN | Implicit | CLI/Python | 2-4 weeks | $17-37K |
| **Linguistic Research** | Parselmouth | Semi-auto | Manual | Praat GUI | 1-2 months | $15-20K |
| **Content Creation** | Parselmouth | Dictionary+CNN | Skip | Desktop GUI | 3-6 months | $62-68K |
| **Clinical Assessment** | Parselmouth | Rule-based | Skip | Desktop app | 12 months | $230-380K |

## Detailed Recommendations by Use Case

### 1. Pronunciation Practice Apps

**Recommended Stack:**
```
PESTO (pitch) + Lightweight CNN or Rule-based (tones) + Mobile app
```

**Why:**
- **Latency is king:** <200ms end-to-end required for "instant" feedback
- PESTO delivers <10ms pitch detection (only viable option)
- Lightweight CNN or rules fit 50ms classification budget
- Mobile-optimized (TensorFlow Lite, 2-5 MB model)

**Critical Trade-offs:**
- Accuracy (85%+) vs. Latency (<200ms): Chose latency
- Server-side (90%+ accuracy) vs. On-device (85%+): Chose on-device
- CNN (higher accuracy) vs. Rules (lower latency): Start rules, upgrade CNN if needed

**Success Criteria:**
- 85%+ tone classification accuracy
- <200ms 95th percentile latency
- 20% learner improvement after 10 hours

**Budget:** $50-60K Year 1 (app + backend)

---

### 2. Speech Recognition Systems

**Recommended Stack:**
```
Parselmouth (pitch) + Pre-trained CNN (tones) + Python pipeline
```

**Why:**
- **Accuracy matters more than speed:** ASR models amplify feature noise
- Parselmouth: Praat-level accuracy (r=0.999), CPU-only
- Pre-trained CNN: 87-88% tone accuracy (sufficient for F0 features)
- Batch processing: 10-50× real-time on CPU cluster

**Critical Trade-offs:**
- Parselmouth (accurate, slower) vs. librosa (faster, less accurate): Chose accuracy
- CPU cluster (cost-effective) vs. GPU (faster): Chose CPU for <1000 hours
- Explicit tone labels vs. Implicit (end-to-end): Explicit for <1000 hour corpora

**Success Criteria:**
- 2-5% WER reduction with F0 features
- >95% F0 extraction success rate
- Reproducible results (same input → same output)

**Budget:** $17-37K per corpus (one-time)

---

### 3. Linguistic Research

**Recommended Stack:**
```
Parselmouth → Praat TextGrids → Manual verification → R analysis
```

**Why:**
- **Peer review demands Praat:** Reviewers expect gold standard
- Parselmouth: Identical to Praat (r=0.999), but scriptable for batches
- Manual verification: Standard practice in phonetics (100% accuracy expected)
- R integration: Statistical analysis (mixed models, ANOVAs)

**Critical Trade-offs:**
- Automatic (85-90%) vs. Manual verification (100%): Manual required for publication
- Parselmouth (scriptable) vs. Praat GUI (manual): Parselmouth for batch, GUI for verification
- Small samples (10-50 speakers) vs. Large (1000+): Small samples allow manual work

**Success Criteria:**
- Publication acceptance (no methodology questions)
- Inter-rater agreement κ > 0.80
- Reproducibility (exact F0 values on re-run)

**Budget:** $15-20K per study (including data collection)

---

### 4. Content Creation & Quality Control

**Recommended Stack:**
```
Parselmouth (pitch) + Whisper (ASR) + Dictionary + CNN (tone) + Desktop GUI
```

**Why:**
- **False positives break workflow:** <5% false positive rate critical
- Whisper ASR: Get transcript → dictionary lookup → expected tones
- Compare realized vs. expected: Flag only high-confidence mismatches (>0.8)
- Desktop GUI: Waveform display, playback, "Keep/Re-record" buttons

**Critical Trade-offs:**
- Real-time feedback (disruptive) vs. Post-production QC: Chose post-production
- Server-side (easier deployment) vs. Desktop (offline): Chose desktop for pros
- Automatic-only (faster) vs. Human-in-loop (fewer false positives): Chose human-in-loop

**Success Criteria:**
- 80%+ real error catch rate
- <5% false positive rate
- 50% time savings vs. manual QC

**Budget:** $62-68K Year 1 (development + operations)

---

### 5. Clinical Assessment & Speech Therapy

**Recommended Stack:**
```
Parselmouth (pitch) + Rule-based (tone) + Normative data + Desktop app (HIPAA-compliant)
```

**Why:**
- **Regulatory and ethical constraints:** HIPAA requires offline, encrypted storage
- Rule-based classifier: Explainable to clinicians and regulators (FDA/CE clearance easier)
- Normative data: Percentile ranks essential for diagnosis
- Desktop app: No cloud processing (PHI security)

**Critical Trade-offs:**
- Rule-based (explainable, 80-85%) vs. CNN (accurate, 87-90%): Chose explainable
- Cloud (easier updates) vs. Desktop (HIPAA): Chose desktop
- Automatic segmentation vs. Manual annotation: Manual (clinician control)

**Success Criteria:**
- Test-retest reliability ICC > 0.90
- Inter-rater reliability ICC > 0.85
- Criterion validity r > 0.80 with expert SLPs

**Budget:** $230-380K Year 1 (including validation + optional FDA/CE)

---

## Cross-Cutting Insights

### When to Use Which Pitch Detector

| Detector | Use When | Don't Use When |
|----------|----------|----------------|
| **Parselmouth** | Publication quality needed, batch processing, offline required | Real-time required (<50ms) |
| **PESTO** | Real-time required (<10ms), mobile app, low latency critical | Absolute highest accuracy needed |
| **librosa pYIN** | Pure Python required, Praat install impossible | Accuracy critical (ASR, clinical) |
| **CREPE** | State-of-the-art accuracy needed, GPU available | CPU-only, cost-sensitive |

### When to Use Which Tone Classifier

| Classifier | Use When | Don't Use When |
|------------|----------|----------------|
| **Rule-based** | Explainability required (clinical, regulatory), fast prototyping | Accuracy >85% required |
| **Pre-trained CNN** | 87-88% accuracy sufficient, no time to train | Need >90% accuracy, domain mismatch |
| **Train custom CNN** | Domain-specific data available, accuracy critical | Small dataset (<1000 examples) |
| **RNN/LSTM** | Tone sandhi learning needed, sequential context | Simple isolated tone recognition |
| **Hybrid (Rule+CNN)** | Precision critical (low false positives), tone sandhi detection | Speed critical, complexity unacceptable |

### When to Include Tone Sandhi Detection

| Use Case | Include Sandhi? | Rationale |
|----------|-----------------|-----------|
| Pronunciation Practice | ❌ No (MVP) | Learners master individual tones first; add sandhi in advanced mode |
| Speech Recognition | ✅ Yes (implicit) | ASR learns from realized F0 (includes sandhi effects) |
| Linguistic Research | ✅ Yes (manual) | Research question often IS tone sandhi |
| Content Creation | ❌ No (MVP) | Focus on individual tone errors; sandhi rarely wrong in native speech |
| Clinical Assessment | ❌ No (MVP) | Diagnostic focus on basic tone production; sandhi is advanced skill |

---

## Common Pitfalls to Avoid

### Pitfall 1: Over-Engineering MVP
**Symptom:** First version includes every feature (real-time, sandhi, multi-language, GUI)
**Impact:** 12+ month timeline, budget overruns, delayed user feedback
**Solution:** Ship rule-based MVP in 4-8 weeks, iterate based on real usage

### Pitfall 2: Ignoring User Expertise
**Symptom:** Building command-line tool for speech therapists, or mobile app for researchers
**Impact:** User adoption fails (wrong interface for user archetype)
**Solution:** Match interface to user: CLI for engineers, GUI for clinicians, mobile for learners

### Pitfall 3: Optimizing Wrong Metric
**Symptom:** Maximizing tone accuracy (90%+) at expense of latency (500ms)
**Impact:** Pronunciation app feels "laggy" despite high accuracy
**Solution:** Identify critical constraint FIRST (latency vs. accuracy vs. cost), then optimize

### Pitfall 4: Skipping Validation
**Symptom:** Deploying CNN with 87% accuracy on test set, but poor real-world performance
**Impact:** User trust breaks (false positives, missed errors)
**Solution:** Validate on target population (learners, patients, professional narrators)

### Pitfall 5: Assuming Praat is Too Hard
**Symptom:** Building custom pitch detector to avoid Praat dependency
**Impact:** Lower accuracy, months of development, reinventing wheel
**Solution:** Use Parselmouth (Praat algorithms, Python interface, zero dependencies)

---

## Decision Trees

### Tree 1: Choosing Pitch Detection Algorithm

```
START: What's your critical constraint?

├─ Latency (<50ms required)
│  └─ PESTO (<10ms) or CREPE-Tiny (GPU, 20-30ms)
│
├─ Accuracy (publication-grade)
│  └─ Parselmouth (Praat-equivalent, r=0.999)
│
├─ Pure Python (no dependencies)
│  └─ librosa pYIN (acceptable if accuracy not critical)
│
└─ State-of-the-art accuracy + GPU available
   └─ CREPE (deep learning, highest accuracy)
```

### Tree 2: Choosing Tone Classification Approach

```
START: What's your use case?

├─ Real-time mobile app
│  └─ Lightweight CNN (TensorFlow Lite, 30-50ms) or Rule-based (10-20ms)
│
├─ Batch processing (ASR, research)
│  └─ Have training data + GPU?
│     ├─ YES → Train custom CNN or RNN (87-90%)
│     └─ NO  → Pre-trained CNN (87-88%) or Rule-based (80-85%)
│
├─ Clinical/regulatory use
│  └─ Rule-based (explainable, defensible) → Upgrade to CNN after validation study
│
└─ Content QC (low false positives)
   └─ Hybrid (Dictionary + CNN, confidence threshold >0.8)
```

### Tree 3: Build vs. Buy vs. Reuse

```
START: Should I build custom, use open-source, or buy commercial?

├─ Core research question IS tone analysis
│  └─ BUILD: Custom solution justified (your expertise)
│
├─ Supporting feature for larger system (ASR, language app)
│  └─ REUSE: Parselmouth + pre-trained CNN (don't reinvent)
│
├─ Clinical/regulated use
│  └─ BUY or BUILD: Buy if FDA-cleared tool exists, else build and validate
│
└─ Commercial product (SaaS, desktop)
   └─ BUILD: Differentiation requires custom implementation
```

---

## Implementation Checklist

Use this checklist to ensure you've considered key factors:

### Technical
- [ ] Identified critical constraint (latency, accuracy, cost)
- [ ] Selected pitch detector matching constraint
- [ ] Chosen tone classifier (rule-based, CNN, RNN, hybrid)
- [ ] Decided on tone sandhi handling (skip, implicit, rule-based, ML)
- [ ] Planned speaker normalization (z-score, min-max, adaptive)
- [ ] Considered edge cases (silence, noise, incomplete syllables)

### User Experience
- [ ] Matched interface to user archetype (CLI, GUI, mobile, web)
- [ ] Designed for user expertise level (expert, moderate, novice)
- [ ] Minimized false positives (especially for QC and clinical use)
- [ ] Provided explainability (confidence scores, visualizations)
- [ ] Planned feedback loop (user corrections improve model)

### Validation
- [ ] Defined success metrics (accuracy, latency, satisfaction)
- [ ] Planned validation study (target population, sample size)
- [ ] Established test-retest reliability (for clinical/research)
- [ ] Collected or identified normative data (if applicable)
- [ ] Documented methodology (for peer review or regulatory)

### Deployment
- [ ] Considered data privacy (HIPAA, GDPR, local storage)
- [ ] Planned offline capability (if required)
- [ ] Designed for scalability (batch processing, concurrent users)
- [ ] Budgeted for compute costs (GPU, cloud, storage)
- [ ] Planned update mechanism (bug fixes, model improvements)

---

## Next Steps for S4

Strategic analysis will address:
1. **Market viability** - Market size, competitors, business models
2. **Ecosystem maturity** - Availability of datasets, pre-trained models, tools
3. **Risk factors** - Technology limitations, regulatory barriers, user adoption
4. **Long-term outlook** - Research trends, emerging techniques, 3-5 year roadmap

For each use case, S4 will assess whether tone analysis technology is **ready for production** or **still research-grade**.

---

## Key Takeaway

**There is no universal "best" tone analysis stack.** The optimal choice depends on:
- User expertise (expert vs. novice)
- Critical constraint (latency vs. accuracy vs. cost)
- Regulatory context (clinical vs. consumer)
- Scale (10 files vs. 10,000 hours)

Match your stack to your use case, then iterate based on real-world validation.
