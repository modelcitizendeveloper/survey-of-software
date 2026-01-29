# Use Case 03: Linguistic Research

## User Archetype

**Who:** Phonetics researcher, linguistics PhD student, language documentation specialist
**Context:** Academic research on tone variation, sociolinguistics, tone sandhi
**Goal:** Publish peer-reviewed papers with reproducible F0 analysis
**Technical sophistication:** Moderate (comfortable with Praat, some Python)

## Core Requirements

### Functional
1. **Publication-grade accuracy** - Results must match or exceed Praat GUI
2. **Reproducibility** - Analysis scripts for peer review and replication
3. **Manual verification** - Tools for checking/correcting automatic annotations
4. **Statistical analysis** - Export F0 data for R/SPSS (ANOVAs, mixed models)
5. **Corpus annotation** - Time-aligned TextGrids with tone labels

### Non-Functional
- **Accuracy:** 95%+ tone classification (manual verification expected)
- **Praat compatibility:** Output readable by Praat GUI (for collaborators)
- **Reproducibility:** Exact same results on re-run (no randomness)
- **Documentation:** Clear methodology for Methods section
- **Citation:** Published, peer-reviewed algorithms (YIN, pYIN, Praat)

## Technical Challenges

### Challenge 1: The Praat Standard
- Praat is the de facto standard in phonetics research
- Reviewers expect Praat or explicit justification for alternatives
- Need to prove results are "Praat-equivalent"

### Challenge 2: Small Sample Sizes
- Research studies often use 10-50 speakers (not 1000+)
- Statistical power concerns with noisy features
- Manual verification is feasible (and expected)

### Challenge 3: Interdisciplinary Collaboration
- Co-authors may not be programmers
- Need GUI tools, not just Python scripts
- Praat scripting is common skill in phonetics

### Challenge 4: Specific Research Questions
Not just "classify tones", but:
- Tone variation across dialects (Beijing vs. Taiwan Mandarin)
- Tone sandhi domains (prosodic word, phrase)
- Tone perception vs. production
- Tone acquisition in L2 learners

## Recommended Stack: Praat-Centric Workflow

### Architecture
```
Audio Corpus (WAV)
↓
Parselmouth (automatic F0 extraction)
↓
Export to Praat TextGrids
↓
Manual verification in Praat GUI
↓
Statistical analysis in R
↓
Publication (with Praat screenshots and F0 plots)
```

### Component Choices

**Pitch Detection: Parselmouth → Praat TextGrids**
- Rationale: Identical to Praat (r=0.999), but scriptable for batch processing
- Output: Praat TextGrid files (open in Praat GUI for verification)
- Justification for reviewers: "We used Praat's To Pitch (ac) algorithm"

**Why not Praat GUI manually?**
- Batch processing efficiency (100 files × 2 minutes = 3+ hours manual)
- Reproducibility (GUI clicks not documented, scripts are)
- Still allows manual verification on subset

**Tone Classification: Semi-Automatic**

*Phase 1: Automatic labeling*
- Use rule-based or CNN for initial labels
- Accuracy: 85-90% (good enough for first pass)

*Phase 2: Manual verification*
- Researcher checks 100% of labels in Praat GUI
- Corrects errors (especially Tone 3, which is often misclassified)
- This is standard practice in phonetics research

**Tone Sandhi: Manual Annotation**
- Automatic sandhi detection (rule-based) as starting point
- Manual verification required (sandhi domains are theory-dependent)
- Researcher decides sandhi boundaries based on research question

### Implementation

**Python Script (Parselmouth):**
```python
import parselmouth
from parselmouth.praat import call
import textgrid  # For TextGrid export

def extract_f0_to_textgrid(wav_path, textgrid_path):
    """
    Extract F0 and create Praat TextGrid
    Exactly replicates Praat GUI workflow
    """
    # Load sound
    sound = parselmouth.Sound(wav_path)

    # To Pitch (ac) - EXACT Praat parameters
    pitch = call(sound, "To Pitch", 0.0, 75.0, 500.0)
    # 0.0 = time_step (auto), 75-500 Hz = range

    # Extract F0 values
    f0_values = []
    for time in pitch.xs():
        f0 = call(pitch, "Get value at time", time, "Hertz", "Linear")
        f0_values.append((time, f0))

    # Create TextGrid
    tg = call(sound, "To TextGrid", "syllables tones", "")

    # Populate with automatic labels (simplified example)
    # Researcher will verify/correct in Praat GUI
    for i, syllable_interval in enumerate(get_syllable_intervals(sound)):
        start, end = syllable_interval
        # Extract F0 contour for this syllable
        f0_contour = get_f0_contour(pitch, start, end)
        # Classify tone (rule-based or CNN)
        tone_label = classify_tone(f0_contour)
        # Insert label into TextGrid
        call(tg, "Insert point", 1, (start + end) / 2, tone_label)

    # Save TextGrid
    call(tg, "Save as text file", textgrid_path)

    return f0_values

# Batch process corpus
for wav_file in corpus:
    wav_path = f"audio/{wav_file}.wav"
    tg_path = f"textgrids/{wav_file}.TextGrid"
    extract_f0_to_textgrid(wav_path, tg_path)

print("Automatic annotation complete. Open TextGrids in Praat for verification.")
```

**Praat Script (for manual verification):**
```praat
# Open audio and TextGrid
sound_file$ = "audio/speaker01.wav"
textgrid_file$ = "textgrids/speaker01.TextGrid"

Read from file: sound_file$
Read from file: textgrid_file$

# Open editor for manual checking
selectObject: "Sound speaker01"
plusObject: "TextGrid speaker01"
Edit

# Researcher manually verifies and corrects labels
# (No script for this - human judgment required)
```

**R Script (statistical analysis):**
```r
library(tidyverse)
library(lme4)

# Load F0 data exported from Praat/Parselmouth
f0_data <- read_csv("f0_measurements.csv")

# Mixed-effects model: Tone variation by speaker and context
model <- lmer(f0_max ~ tone * context + (1 | speaker), data = f0_data)
summary(model)

# Post-hoc tests
emmeans(model, pairwise ~ tone | context)

# Visualize
ggplot(f0_data, aes(x = time_norm, y = f0_norm, color = tone)) +
  geom_smooth() +
  facet_wrap(~ speaker) +
  labs(title = "F0 contours by tone and speaker",
       x = "Normalized time", y = "Normalized F0")
```

## MVP Definition

### Must-Have (Week 1-2)
1. Batch F0 extraction with Parselmouth
2. Export to Praat TextGrid format
3. Automatic tone labels (rule-based or CNN)
4. Documentation of methodology (for Methods section)

### Should-Have (Week 3-4)
5. Manual verification workflow in Praat GUI
6. Export F0 data to CSV for R analysis
7. Example statistical analysis scripts (R)
8. Quality checks (detect failed F0 extraction, outliers)

### Nice-to-Have (Week 5-6)
9. Inter-annotator agreement calculations (if multiple annotators)
10. Visualization scripts (F0 contour plots for paper figures)
11. Batch export to R-ready format (long-form data frame)
12. Integration with ProsodyPro (popular Praat plugin)

## Success Metrics

### Accuracy
- **Automatic tone classification:** 85-90% (before manual correction)
- **After manual correction:** 100% (gold standard for publication)
- **Inter-annotator agreement:** κ > 0.80 (if using multiple annotators)

### Reproducibility
- **Exact replication:** 100% same F0 values on re-run
- **Praat compatibility:** TextGrids open correctly in Praat 6.x
- **Statistical replication:** Same p-values in R analysis

### Publication
- **Accepted by reviewers:** No questions about methodology
- **Cited appropriately:** Parselmouth (Jadoul et al. 2018) + Praat (Boersma & Weenink)
- **Data/code sharing:** Scripts on OSF or GitHub for replication

## Cost Estimate

### Development (Month 1)
- Parselmouth pipeline development: $4,000 (1 week)
- R statistical analysis scripts: $2,000 (0.5 week)
- Documentation (Methods section): $2,000 (0.5 week)
- **Subtotal:** $8,000

### Data Collection (if needed)
- Participant recruitment: $2,000 (20 speakers × $100)
- Recording setup: $1,000 (microphone, audio interface)
- Recording sessions: $4,000 (20 hours × $200/hour)
- **Subtotal:** $7,000

### Manual Annotation (Researcher Time)
- Manual verification: 40 hours (100 files × 24 minutes each)
- Assuming PhD student: $0 (their research time)
- Or Research Assistant: $1,600 (40 hours × $40/hour)

### Publication
- Open access fee: $1,500-3,000 (varies by journal)
- Data repository: $0 (OSF or GitHub are free)

**Total (Typical PhD study):** $15,000-$20,000 (including data collection)

## Critical Risks

### Risk 1: Reviewers Reject Automatic Methods
**Probability:** Low (Praat-based methods widely accepted)
**Impact:** High (paper rejection)
**Mitigation:**
- Use Parselmouth with explicit "Praat-equivalent" claim
- Cite Parselmouth validation paper (Jadoul et al. 2018)
- Include manual verification step (standard practice)
- Provide F0 plots in supplementary materials

### Risk 2: Tone 3 Misclassification
**Probability:** High (Tone 3 is notoriously difficult - dipping contour, often incomplete)
**Impact:** Medium (affects subset of data)
**Mitigation:**
- Manual verification catches errors
- Discuss Tone 3 challenge in paper (common issue)
- Report classification accuracy per tone in Methods
- Consider treating Tone 3 separately in analysis

### Risk 3: Inter-Annotator Disagreement
**Probability:** Medium (tone boundaries are subjective)
**Impact:** Medium (lowers statistical power)
**Mitigation:**
- Train annotators together (develop consensus guidelines)
- Calculate Cohen's κ or Fleiss' κ (report in paper)
- If κ < 0.80, have annotators re-adjudicate disagreements
- Common in phonetics research (not a fatal flaw)

## Alternatives Considered

### Alternative 1: Pure Praat GUI (No Scripting)
**Approach:** Manually analyze each file in Praat GUI

**Pros:**
- No programming required
- Full control over every annotation
- Reviewers love it (gold standard)

**Cons:**
- Time-consuming (100 files = 40+ hours)
- Not reproducible (GUI clicks not documented)
- Human fatigue → errors

**Verdict:** Acceptable for small studies (10-20 files). Use Parselmouth for larger corpora.

### Alternative 2: librosa for Speed
**Approach:** Use librosa pYIN instead of Parselmouth

**Pros:**
- Slightly faster
- Probabilistic uncertainty estimates

**Cons:**
- Lower accuracy (r=0.730 vs. r=0.999)
- Not Praat-compatible (reviewers may object)
- Would need to justify in Methods section

**Verdict:** Not worth reviewer pushback. Stick with Parselmouth (Praat-equivalent).

### Alternative 3: Fully Automatic (No Manual Verification)
**Approach:** Trust CNN tone classification (87-88% accuracy)

**Pros:**
- Faster (no manual verification)
- Scalable to large corpora

**Cons:**
- 12-13% error rate is too high for publication
- Reviewers expect manual verification in phonetics
- Small sample sizes don't justify "big data" trade-offs

**Verdict:** Unacceptable for peer review. Manual verification is standard.

## Research Question Examples

### Example 1: Tone Variation Across Dialects
**Question:** Do Tone 3 F0 contours differ between Beijing and Taiwan Mandarin?

**Method:**
1. Record 20 Beijing speakers + 20 Taiwan speakers
2. Extract F0 contours for Tone 3 syllables with Parselmouth
3. Normalize F0 (z-score per speaker)
4. Mixed-effects model: F0 ~ dialect × time + (1 | speaker)
5. Report: Taiwan Tone 3 is "lower and flatter" than Beijing (with p-values)

### Example 2: Tone Sandhi Domains
**Question:** Where do Tone 3 sandhi rules apply? Phonological word or prosodic phrase?

**Method:**
1. Design stimuli with ambiguous sandhi domains (e.g., "很好看" vs. "很 好看")
2. Record 15 native speakers producing both structures
3. Extract F0 with Parselmouth, manually annotate sandhi application in Praat
4. Statistical analysis: Does pause duration predict sandhi?
5. Report: Sandhi applies within prosodic phrases (support for theory X)

### Example 3: L2 Tone Acquisition
**Question:** Which Mandarin tones are hardest for English L2 learners?

**Method:**
1. Record 30 L2 learners (English L1) producing 4 tones
2. Extract F0 contours with Parselmouth
3. Compare to native speaker reference contours (DTW distance)
4. ANOVA: Tone accuracy ~ tone × proficiency_level
5. Report: Tone 3 and Tone 2 are most difficult (match previous research)

## Next Steps After MVP

1. **Pilot study** - Test pipeline on small corpus (10 speakers)
2. **Inter-annotator reliability** - Train second annotator, calculate κ
3. **Statistical power** - Simulate sample size requirements for planned analyses
4. **Preregistration** - Register analysis plan on OSF before data collection
5. **Write Methods section** - Document every step for peer review

## References

- [Parselmouth: Praat in Python](https://doi.org/10.1016/j.wocn.2017.12.001) (Jadoul et al. 2018)
- [Praat manual](http://www.fon.hum.uva.nl/praat/manual/Intro.html) (Boersma & Weenink)
- [ProsodyPro for Praat](https://sites.google.com/site/prosodypro/) (Xu 2013)
- [Best practices for phonetic research](https://doi.org/10.5334/labphon.196) (Roettger et al. 2019)
- Example papers using Parselmouth:
  - [Tone perception in Mandarin](https://doi.org/10.1121/10.0001730)
  - [Cantonese tone variation](https://doi.org/10.1159/000515438)
