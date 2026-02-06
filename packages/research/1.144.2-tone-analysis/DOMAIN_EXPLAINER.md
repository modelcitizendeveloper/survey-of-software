# Tone Analysis for CJK Languages: Domain Explainer

## What This Solves

### The Problem in Plain Language

In tonal languages like Mandarin Chinese and Cantonese, the same syllable can mean completely different things depending on pitch contour. "Ma" spoken with a high-level pitch means "mother" (妈 mā), with a rising pitch means "hemp" (麻 má), with a dipping pitch means "horse" (马 mǎ), and with a falling pitch means "to scold" (骂 mà). Getting the tone wrong isn't like having an accent—it's like saying a different word entirely.

Tone analysis technology automatically detects and evaluates whether someone produced the correct pitch pattern. It's like spell-check, but for the melody of speech instead of the letters.

### Who Encounters This Problem

**Language learners:** English speakers learning Mandarin struggle to hear and produce tone differences. Without feedback, they reinforce incorrect patterns for months.

**Speech recognition systems:** Voice assistants like Siri need to distinguish "买" (mǎi, "to buy") from "卖" (mài, "to sell") based solely on pitch. Getting tones wrong means misunderstanding user intent.

**Content creators:** Audiobook narrators and podcast hosts working in Mandarin need quality control. One mispronounced tone can make listeners think the narrator doesn't speak the language fluently.

**Speech therapists:** Children with cochlear implants or adults recovering from stroke need assessment: Can they perceive and produce tones? Progress tracking requires objective measurements.

**Linguistic researchers:** Studying how tones change in connected speech (tone sandhi) or vary by dialect requires analyzing thousands of recordings. Manual analysis takes months; automatic tools reduce this to days.

### Why It Matters

**Scale:** Over 1.3 billion people speak Mandarin Chinese. The global language learning market is $4.4 billion and growing 17% annually. Mandarin is the #2 most-studied language worldwide.

**Accuracy barrier:** Current automatic tone analysis achieves 87-90% accuracy. This is "good enough" for language learning feedback but not sufficient for clinical diagnostics or high-stakes testing. The remaining 10-13% error rate is a persistent challenge.

**Economic opportunity:** The niche market for tone-specific training tools is $100-150 million (2026), but faces disruption risk. Tech giants like Google and ByteDance could commoditize basic tone analysis by 2028-2029 through foundation models (think "Whisper for tones").

## Accessible Analogies

### Pitch Detection: Finding the Melody in Speech

Imagine trying to transcribe a melody while an orchestra is playing. You need to isolate the lead violin's pitch from all the drums, horns, and background noise. That's pitch detection—extracting the fundamental frequency (F0) from a complex audio signal.

**The challenge:** Human speech isn't a pure tone like a tuning fork. It's noisy, it starts and stops (consonants have no pitch), and everyone's natural pitch range is different. A man saying "mā" might peak at 150 Hz, while a woman peaks at 300 Hz—same tone, different frequencies.

**Established solutions:** The Praat software (developed in phonetics labs, used for 25+ years) is the gold standard. It's like the Adobe Photoshop of speech analysis—professional-grade, trusted by academics, but has a steep learning curve. Tools like Parselmouth bring Praat's accuracy to Python with zero dependencies, making it accessible to software developers.

**The trade-off:** Accurate pitch detection takes 2-3 seconds per audio file. For batch processing (analyzing 1000 recordings for research), that's acceptable. For real-time feedback (language learning app), that's too slow—users need responses in under 200 milliseconds to feel "instant."

### Tone Classification: Pattern Recognition in Melodies

Once you have the pitch contour (the melody), you need to classify it: Is this Tone 1 (high-level, like a sustained note), Tone 2 (rising, like asking a question), Tone 3 (dipping then rising, like a valley), or Tone 4 (falling, like a command)?

**Analogy:** Think of reading handwriting. An expert can glance at "Hello" written in cursive and know immediately what it says, even if the 'o' looks a bit like an 'a'. They've seen thousands of examples and learned the pattern. Machine learning models do the same with pitch contours—trained on thousands of examples, they learn to recognize the characteristic shapes of each tone.

**Accuracy levels:**
- **Rule-based (80-85% accurate):** Like following explicit instructions ("If pitch rises more than 50 Hz, it's Tone 2"). Fast and explainable, but brittle to edge cases.
- **CNN neural networks (87-88% accurate):** Like an expert who's seen 10,000 examples. Can handle variations, but you can't easily explain *why* it made a decision.
- **State-of-the-art hybrids (90%+ accurate):** Combining multiple techniques, but adds complexity and cost.

**The persistent gap:** That final 10-13% error rate is stubborn. It's often Tone 3 (the dipping tone), which speakers sometimes produce incompletely in casual speech. Teaching a model to distinguish "sloppy but acceptable Tone 3" from "actually Tone 2" requires human-like contextual understanding—a current frontier.

### Tone Sandhi: Rules That Change in Context

In connected speech, tones don't occur in isolation. Mandarin has "tone sandhi rules"—the tone of one syllable changes based on what comes next. It's like how English speakers say "I'm gonna go" instead of "I am going to go"—the casual form follows implicit rules.

**Example:** The word 不 (bù, "not") is normally Tone 4 (falling). But before another Tone 4, it changes to Tone 2 (rising). So "不是" (bù shì, "is not") is pronounced "bú shì" with the first syllable rising instead of falling.

**Detection challenge:** A tone analysis system hearing "bú shì" needs to recognize: (1) the speaker produced Tone 2, but (2) this is the *correct* realization of an underlying Tone 4 due to a sandhi rule, not an error.

**Solution landscape:**
- **Rule-based (88-97% accurate):** Hard-code the known sandhi rules. Fast and transparent, but only handles documented patterns.
- **Machine learning (97%+ accurate):** Train models on thousands of examples of tone sandhi. Can discover patterns, but requires labeled data and careful validation.
- **Hybrid approach (97%+, low false positives):** Use rules to flag potential sandhi, then ML to verify. Combines explainability with accuracy.

## When You Need This

### Clear Decision Criteria

**You NEED tone analysis if:**

1. **Language learning app for tonal languages:** Your users are learning Mandarin, Cantonese, Vietnamese, or Thai and need automated feedback on pronunciation. Manual correction by tutors doesn't scale.

2. **Speech recognition for tonal languages:** You're building ASR (automatic speech recognition) and need to distinguish homophones. "Tone-deaf" ASR confuses "buy" (mǎi) with "sell" (mài), leading to frustrating user experiences.

3. **Quality control for audio content:** Your audiobook narrators or podcast hosts work in tonal languages, and you need to catch pronunciation errors before publication. Manual QC takes too long.

4. **Phonetics research on tones:** You're studying tone variation, dialect differences, or tone sandhi, and manually annotating 1000+ recordings would take 6+ months.

5. **Clinical assessment (future):** You're developing tools for speech-language pathologists to diagnose tone perception deficits in children with cochlear implants or patients recovering from stroke. **Note:** This use case requires 3-5 years of validation studies and regulatory clearance—technology is not yet production-ready.

### When You DON'T Need This

**Skip tone analysis if:**

1. **Non-tonal languages only:** If you're working with English, Spanish, French, etc., pitch carries emotion and emphasis (prosody), not lexical meaning. Standard speech recognition handles this.

2. **Casual accuracy is sufficient:** If your learners just need to be "understandable, not perfect," tone errors may be acceptable. Native speakers are forgiving—context often clarifies meaning. Focus budget elsewhere (vocabulary, grammar).

3. **Small user base, high-touch:** If you have 50 learners and 5 tutors, human feedback may be more cost-effective than building automated tools. Break-even is typically 500-1000+ learners.

4. **Technology not mature for your use case:** Clinical diagnostics requires 95%+ accuracy, test-retest reliability, and FDA clearance. Current technology is at 87-90% accuracy and lacks clinical validation. Wait 3-5 years or invest in validation studies yourself ($100K-500K).

### Concrete Use Case Examples

**Duolingo-style language app:**
- Use case: Give learners instant feedback on tone accuracy
- Stack: Real-time pitch detection (PESTO, <10ms latency) + lightweight neural network
- Cost: $50-60K for MVP (4-8 weeks)
- Success metric: 85%+ tone classification accuracy, <200ms latency

**Baidu-style Mandarin ASR:**
- Use case: Improve speech recognition accuracy by 2-5% relative WER
- Stack: Batch pitch extraction (Parselmouth) + tone features for acoustic model
- Cost: $17-37K per corpus (one-time)
- Success metric: Reduce tone-related ASR errors by 50%+

**Audiobook QC tool:**
- Use case: Flag potential tone errors for narrator re-recording
- Stack: ASR (Whisper) + dictionary lookup + tone verification (CNN)
- Cost: $62-68K Year 1
- Success metric: 80%+ error catch rate, <5% false positives

**University phonetics lab:**
- Use case: Analyze tone variation across 100 speakers, 10 hours of audio
- Stack: Praat/Parselmouth (batch F0 extraction) + manual verification
- Cost: $15-20K (including data collection)
- Success metric: Publication acceptance, reproducible results

## Trade-offs

### Accuracy vs. Speed vs. Cost

There's no free lunch—you choose where to optimize:

| Priority | Approach | Accuracy | Speed | Cost (Year 1) | Use Case |
|----------|----------|----------|-------|---------------|----------|
| **Speed First** | PESTO + Rules | 80-85% | <10ms (real-time) | $50-60K | Language learning app (mobile) |
| **Balanced** | Parselmouth + CNN | 87-88% | 2-3s per file | $12-20K | Most production use cases |
| **Accuracy First** | CREPE + CNN-LSTM | 90-95% | 0.5-1s (GPU) | $22-30K | Research, high-stakes assessment |

**The 87-90% plateau:** Current technology hits a wall here. Exceeding 90% requires:
- More training data (10,000+ hours vs. 1,000 hours)
- Contextual understanding (what word was intended?)
- Speaker adaptation (learn individual's pitch range)
- Foundation models (2028-2029 timeline, not available today)

### Build vs. Buy vs. Wait

**Build custom (2-6 months, $50K-200K) if:**
- Your use case has specific requirements (regulatory, integration, custom UX)
- You need differentiation (competitors use off-the-shelf tools)
- You have in-house ML expertise (don't outsource your core competency)

**Buy or integrate open-source (2-4 weeks, $0-30K) if:**
- Standard use case (pronunciation practice, ASR features)
- Speed to market > customization
- Budget-constrained or testing market fit

**Wait 2-3 years if:**
- You need 95%+ accuracy (clinical, high-stakes testing)
- Foundation models may commoditize (2028-2029)
- Regulatory path unclear (FDA for medical devices)

### Self-Hosted vs. Cloud Services

**Self-hosted (on-device or on-premise):**
- ✅ Data privacy (HIPAA, GDPR compliant by default)
- ✅ Low latency (no network round-trip)
- ✅ Predictable costs (no per-API-call pricing)
- ❌ Deployment complexity (model updates, cross-platform)
- ❌ Upfront investment (optimize models for mobile)

**Cloud API (SaaS):**
- ✅ Easy deployment (just API calls)
- ✅ Always up-to-date (models improve automatically)
- ❌ Privacy concerns (voice data leaves device)
- ❌ Variable costs (scales with users, can balloon)
- ❌ Internet dependency (unusable offline)

**Recommendation for tone analysis:** Self-hosted preferred for consumer apps (privacy, latency) and clinical tools (HIPAA). Cloud acceptable for B2B enterprise if BAA (Business Associate Agreement) in place.

### Language Coverage

**Mandarin (4 tones + neutral):**
- Most mature technology (90% of research focuses here)
- Datasets: AISHELL-1 (170 hours), AISHELL-3 (85 hours)
- Production-ready (87-88% accuracy achievable)

**Cantonese (6 tones):**
- Less mature (fewer datasets, pre-trained models scarce)
- Requires custom training or fine-tuning
- Add 30-50% to timeline and budget

**Vietnamese (6 tones):**
- Similar maturity to Cantonese
- Research active but fewer production tools

**Thai (5 tones):**
- Less researched than Mandarin/Cantonese
- Expect to build from scratch or adapt Mandarin models

**Trade-off:** Start with Mandarin for fastest time-to-market. Expand to Cantonese/Vietnamese once validated. Avoid multi-language from day one (complexity explodes).

## Implementation Reality

### Realistic Timeline Expectations

**Language Learning App (Pronunciation Practice):**
- MVP (rule-based, 80-85% accuracy): 4-8 weeks
- Production (CNN, 87% accuracy): 3-4 months
- State-of-the-art (90%+): 6-9 months + validation

**Speech Recognition (F0 Features):**
- Integrate Parselmouth: 1-2 weeks
- Train ASR with tone features: 2-4 weeks (if corpus ready)
- Optimize and deploy: 1-2 weeks
- **Total:** 1-2 months

**Linguistic Research Tool:**
- Script Parselmouth pipeline: 1-2 weeks
- Test on pilot data: 1 week
- Full corpus analysis: Depends on size (100 hours = 1-2 weeks compute)
- **Total:** 1-2 months

**Clinical Assessment Tool:**
- Build core functionality: 3-6 months
- Validation study (reliability, accuracy): 6-12 months
- FDA 510(k) submission (if medical device): 12-24 months
- **Total:** 2-5 years to market

**The rule of thumb:** Consumer/research use cases = months. Clinical/regulated = years.

### Team Skill Requirements

**Minimum viable team (for language learning app):**
- 1 full-stack developer (mobile app, backend API)
- 1 ML engineer (pitch detection, tone classification)
- 1 linguist consultant (part-time, validate tone labels)
- **Total:** 2.5 FTE for 3-4 months

**Ideal team (for production-grade product):**
- 2 mobile developers (iOS + Android)
- 1 backend engineer (API, infrastructure)
- 1-2 ML engineers (pitch, tone classification, sandhi)
- 1 linguist (full-time, data annotation, validation)
- 1 UX designer (learner feedback is subtle, needs iteration)
- **Total:** 6-7 FTE

**Key skills:**
- **Must have:** Python, speech processing (Parselmouth/librosa), basic ML (scikit-learn)
- **Nice to have:** Deep learning (PyTorch/TensorFlow), Praat expertise, Mandarin fluency
- **Can outsource:** Data annotation (hire native speakers), UI/UX design

**Talent availability:** 50-100 PhD graduates per year specialize in tone analysis (globally). Concentrated in China, Taiwan, Singapore, and North America. Hiring is competitive—budget $120K-180K/year for experienced ML engineer with speech expertise.

### Common Pitfalls and Misconceptions

**Pitfall 1: "Tone analysis is a solved problem."**
- Reality: 87-90% accuracy is state-of-the-art. The remaining 10-13% is hard. Tone 3 is especially tricky.
- Mitigation: Set realistic expectations with stakeholders. 85%+ is "good enough" for most consumer use cases.

**Pitfall 2: "We'll just use Praat."**
- Reality: Praat is powerful but has a steep learning curve. GUI-based workflows don't scale. Researchers can use it; app developers need Parselmouth.
- Mitigation: Use Parselmouth (Praat algorithms, Python interface) for programmatic access.

**Pitfall 3: "Real-time tone feedback is easy."**
- Reality: Real-time means <200ms latency. Most pitch detectors take 2-3s per file. You need specialized algorithms (PESTO) and lightweight models.
- Mitigation: Budget 2-3× more time for real-time vs. batch processing. Test on mid-range devices (not just your MacBook).

**Pitfall 4: "87% accuracy sounds low."**
- Reality: Context matters. For language learning, 87% is sufficient—false positives are infrequent, learners improve despite imperfect feedback. For clinical diagnostics, 87% is unacceptable—misdiagnosis has consequences.
- Mitigation: Match accuracy requirements to use case. Don't over-engineer.

**Pitfall 5: "Big Tech will never care about tone analysis."**
- Reality: Mandarin is the #2 language. Google Translate, Duolingo, and ByteDance already use tone features in ASR. Foundation models may commoditize tone analysis by 2028-2029.
- Mitigation: Build data moat (collect learner pronunciation data 2026-2027) before commoditization. Differentiate on UX, personalization, or domain specificity.

**Pitfall 6: "We'll expand to Cantonese/Vietnamese later."**
- Reality: Multi-language adds 30-50% complexity per language (new datasets, models, validation). Design for it upfront or accept refactoring.
- Mitigation: If multi-language is core to your strategy, budget accordingly from day one. Otherwise, perfect Mandarin first.

### First 90 Days: What to Expect

**Month 1: Setup and Prototyping**
- Week 1-2: Evaluate open-source tools (Parselmouth, librosa, PESTO). Pick one.
- Week 3-4: Build proof-of-concept (record audio → extract pitch → classify tone → display result).
- Deliverable: Rule-based MVP (80% accuracy) that runs on your machine.

**Month 2: Data and Training**
- Week 5-6: Acquire dataset (AISHELL-1 or collect custom data from target users).
- Week 7-8: Train CNN tone classifier (TensorFlow or PyTorch).
- Deliverable: Model checkpoint (87% accuracy on test set).

**Month 3: Integration and Validation**
- Week 9-10: Integrate model into app (mobile or web).
- Week 11-12: User testing with 10-20 target users (language learners, narrators, etc.).
- Deliverable: Feedback report (accuracy, latency, UX issues).

**Expect:**
- **Good surprises:** Parselmouth works out-of-box. Pre-trained models (if available) save weeks.
- **Bad surprises:** Tone 3 classification is worse than expected (70-75% vs. 87% average). Real-world noise breaks pitch detection. Users find latency frustrating.
- **Typical roadblocks:** Dataset licensing (AISHELL requires citation, some corpora are restricted). Deployment (model too large for mobile, need quantization). User expectations (they expect 100% accuracy, need to set realistic expectations).

### After 90 Days: Path to Production

**If MVP validates (users find it useful despite imperfections):**
- Invest in CNN model (2-4 weeks training time)
- Optimize for production (model compression, latency)
- Scale infrastructure (handle 1000+ concurrent users)
- Launch beta (invite-only, collect feedback)

**If MVP reveals issues:**
- Pivot tone classification approach (try hybrid rule-based + ML)
- Reduce scope (focus on Tone 1 and 4 first, add Tone 2 and 3 later)
- Consider outsourcing (hire contractor with speech expertise)

**If MVP fails (users don't engage):**
- Revisit use case (was tone feedback actually the pain point?)
- Check UX (is feedback too subtle? Too slow?)
- Assess accuracy (is 80-85% too low for your users?)

**The litmus test:** After 90 days, you should know whether tone analysis adds value to your product. Don't over-invest until validated.

---

## Summary: Making the Decision

### Decision Framework

**Choose tone analysis if:**
- ✅ Working with tonal language (Mandarin, Cantonese, Vietnamese, Thai)
- ✅ User base large enough (500+ users or growing 50%+ annually)
- ✅ Acceptable accuracy exists (87-90% for consumer, 95%+ for clinical)
- ✅ Budget aligns ($50K-200K for custom, $0-30K for off-shelf)
- ✅ Timeline fits (3-4 months for MVP, 2-5 years for clinical)

**Skip tone analysis if:**
- ❌ Non-tonal language or prosody is "nice-to-have"
- ❌ Small user base (<500) with high-touch service model
- ❌ Accuracy insufficient for use case (clinical needs 95%+, current = 87-90%)
- ❌ Commoditization risk high (Big Tech may dominate 2028-2029)

### Key Takeaway

Tone analysis is **production-ready for language learning and speech recognition** (87-90% accuracy sufficient, technology mature). It's **emerging for content creation** (QC tools being built, market validation in progress). It's **not yet ready for clinical diagnostics** (requires validation studies, regulatory clearance, 3-5 year timeline).

The optimal stack varies by use case (see full research for details), but **Parselmouth + CNN** is the safe default for 80% of use cases. For real-time mobile apps, use **PESTO + lightweight models**. For clinical, wait or invest in validation.

**Timeline to commoditization:** Expect foundation models ("Whisper for tones") by 2028-2029 to achieve 92-95% accuracy. If building a business, differentiate on data (user-specific models), UX (personalized feedback), or domain specificity (clinical workflows). Generic tone analysis APIs will be cheap or free by 2029.

---

## Related Research

- See [01-discovery/DISCOVERY_TOC.md](01-discovery/DISCOVERY_TOC.md) for complete technical deep-dive (25+ documents, 400 KB)
- See [01-discovery/S3-need-driven/](01-discovery/S3-need-driven/) for use case-specific implementation guides
- See [01-discovery/S4-strategic/](01-discovery/S4-strategic/) for market analysis and 3-5 year outlook

**Research bead:** research-bo34 (1.144.2 Tone Analysis)
**Date:** January 2026
**Researcher:** Ivan (research/crew/ivan)
