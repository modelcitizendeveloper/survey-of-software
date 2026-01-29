# Use Case 05: Clinical Assessment & Speech Therapy

## User Archetype

**Who:** Speech-language pathologists (SLPs), audiologists, neurologists
**Context:** Clinical diagnosis and treatment of tone perception/production deficits
**Goal:** Measure tone accuracy for patients with hearing loss, aphasia, or L2 accent
**Technical sophistication:** Moderate (clinical training, not programming)

## Core Requirements

### Functional
1. **Diagnostic precision** - Quantify tone accuracy for clinical records
2. **Progress tracking** - Measure improvement over therapy sessions
3. **Standardized assessment** - Consistent metrics across patients and clinics
4. **Report generation** - Professional reports for referrals, insurance claims
5. **Normative data** - Compare patient to age/gender-matched controls

### Non-Functional
- **Accuracy:** 95%+ (diagnostic precision required)
- **Reproducibility:** Exact same score on re-test (test-retest reliability)
- **Regulatory compliance:** HIPAA (US), GDPR (EU) for patient data
- **Defensible measurements:** Published algorithms, peer-reviewed methods
- **Clinician-friendly:** No command-line, clear visualizations
- **Cost:** <$500/year per clinic (professional budget constraints)

## Technical Challenges

### Challenge 1: Atypical Speech
- Patients with hearing loss: Distorted F0, hoarse voice
- Aphasia: Slow, effortful speech with pauses
- L2 learners: Non-native accents, hesitations
- Need robust to: Irregular voicing, incomplete syllables, slow speech rate

### Challenge 2: Normative Data Requirements
- Diagnosis requires comparison to "normal" (age/gender-matched controls)
- Need database of: Mandarin tone norms (children, adults, elderly)
- Norms don't exist for many populations (must collect)

### Challenge 3: Regulatory and Ethical Constraints
- Patient data is PHI (Protected Health Information)
- Cannot use cloud processing (HIPAA violation unless BAA)
- Must be offline-capable (no internet in clinic)
- Audit trail required (who accessed data, when)

### Challenge 4: Inter-Clinician Reliability
- Multiple SLPs must get same results (inter-rater reliability)
- Automatic scoring reduces subjectivity
- But: Clinicians need to trust the algorithm (explainability)

## Recommended Stack: Clinical-Grade Desktop App

### Architecture
```
Patient Audio (WAV, recorded in clinic)
↓
Parselmouth (F0 extraction, offline)
↓
Speaker normalization (age/gender-adjusted)
↓
Tone classification (CNN or rule-based, validated)
↓
Compare to normative data
↓
Generate report (percentile scores, progress charts)
↓
Store in EHR (Electronic Health Record)
```

### Component Choices

**Pitch Detection: Parselmouth**
- Rationale: Praat-level accuracy (gold standard in phonetics)
- Offline: No internet required (HIPAA-friendly)
- Published algorithm: YIN (de Cheveigné & Kawahara 2002), citable

**Tone Classification: Validated Algorithm**

*Option A: Rule-based (Recommended for FDA/CE clearance)*
- Simple, explainable algorithm (clinicians understand)
- Validated on clinical populations (published norms)
- Easier to get regulatory approval (transparent logic)

*Option B: Pre-trained CNN*
- Higher accuracy (87-90% vs. 80-85% rule-based)
- But: "Black box" (harder to explain to clinicians/regulators)
- Requires validation study on clinical population

**Recommendation:** Start with rule-based (defensible, citable), upgrade to CNN if validation study shows improvement.

**Normative Data: Published Norms + Local Database**
- Use published F0 norms (e.g., [Chen & Xu 2006](https://doi.org/10.1121/1.2217362))
- Allow clinics to build local norms (regional dialects vary)
- Age bands: Children (5-12), Adults (18-65), Elderly (65+)
- Gender: Male, Female

**GUI: Desktop App (Not Web)**
- No cloud processing (HIPAA)
- Waveform display + F0 contour
- Patient database (encrypted, local storage)
- Report templates (PDF export for medical records)

### Implementation

**Backend (Python):**
```python
import parselmouth
import pandas as pd
from datetime import datetime

class ToneAssessment:
    def __init__(self, patient_id, age, gender):
        self.patient_id = patient_id
        self.age = age
        self.gender = gender
        self.normative_data = load_norms(age, gender)

    def assess_recording(self, audio_path, syllable_labels):
        """
        Assess patient's tone production
        Returns: Tone accuracy score (0-100%)
        """
        # Step 1: Extract F0
        sound = parselmouth.Sound(audio_path)
        pitch = sound.to_pitch_ac(
            time_step=0.01,
            pitch_floor=75.0,  # Adjust for age/gender
            pitch_ceiling=500.0
        )

        # Step 2: For each syllable, extract F0 contour
        results = []
        for syllable in syllable_labels:
            start, end, expected_tone = syllable["start"], syllable["end"], syllable["tone"]

            # Extract F0 for this syllable
            f0_contour = extract_f0_segment(pitch, start, end)

            # Normalize for speaker (z-score)
            f0_norm = normalize_f0(f0_contour, self.age, self.gender)

            # Classify realized tone
            realized_tone = classify_tone_rule_based(f0_norm)

            # Score: Correct (1) or Incorrect (0)
            correct = 1 if realized_tone == expected_tone else 0

            results.append({
                "syllable": syllable["text"],
                "expected": expected_tone,
                "realized": realized_tone,
                "correct": correct,
                "f0_contour": f0_norm.tolist()
            })

        # Step 3: Calculate overall accuracy
        accuracy = sum(r["correct"] for r in results) / len(results) * 100

        # Step 4: Compare to normative data
        percentile = self.normative_data.get_percentile(accuracy)

        return {
            "patient_id": self.patient_id,
            "date": datetime.now().isoformat(),
            "accuracy": accuracy,
            "percentile": percentile,
            "details": results
        }

def load_norms(age, gender):
    """Load published normative data"""
    # Age bands: 5-12, 18-65, 65+
    # Gender: M, F
    # Returns: Distribution of tone accuracy scores
    # Example: Adult Male mean=92%, SD=5%
    pass

def classify_tone_rule_based(f0_contour):
    """
    Simple rule-based classification
    Explainable for clinicians
    """
    # 5-point time-normalized contour
    f0_norm = interpolate(f0_contour, 5)

    # Decision tree (published algorithm)
    if is_flat(f0_norm):
        return 1 if is_high(f0_norm) else 0  # T1 or neutral
    elif is_rising(f0_norm):
        return 2  # T2
    elif is_falling(f0_norm):
        return 4  # T4
    elif is_dipping(f0_norm):
        return 3  # T3
    else:
        return None  # Uncertain

# Generate clinical report
def generate_report(assessment_result):
    """
    Create PDF report for medical records
    """
    # Include:
    # - Patient demographics (age, gender)
    # - Test date, assessor name
    # - Tone accuracy score (% correct)
    # - Percentile rank (compared to norms)
    # - Individual syllable breakdown
    # - F0 contour plots
    # - Recommendations (e.g., "Consider hearing evaluation")
    pass
```

**Frontend (Qt or Electron):**
```python
# Pseudocode for GUI (using PyQt5)
from PyQt5 import QtWidgets

class ClinicalToneAssessment(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.patient_db = PatientDatabase()  # Encrypted local DB

    def new_assessment(self):
        # Step 1: Select patient
        patient = self.patient_db.select_patient()

        # Step 2: Record or load audio
        audio_path = record_audio()  # Or browse file

        # Step 3: Label syllables (clinician marks boundaries)
        syllables = annotate_syllables(audio_path)

        # Step 4: Run assessment
        assessment = ToneAssessment(patient.id, patient.age, patient.gender)
        result = assessment.assess_recording(audio_path, syllables)

        # Step 5: Display results
        self.show_results(result)

    def show_results(self, result):
        # Waveform with F0 overlay
        # Table: Syllable, Expected, Realized, Correct
        # Summary: 85% accuracy (32nd percentile)
        # Recommendations
        pass

    def generate_report_pdf(self, result):
        # Export to PDF for EHR
        pass
```

## MVP Definition

### Must-Have (Month 1-3)
1. Patient database (encrypted, local)
2. Audio recording or file import
3. Syllable annotation interface (clinician marks boundaries + expected tones)
4. Parselmouth F0 extraction
5. Rule-based tone classification
6. Accuracy score calculation
7. Basic report (text summary)

### Should-Have (Month 4-6)
8. Normative data comparison (percentile ranks)
9. F0 contour visualizations (plots for report)
10. Progress tracking (compare across sessions)
11. PDF report export (for EHR integration)
12. Age/gender-adjusted normalization

### Nice-to-Have (Month 7-12)
13. CNN tone classifier (if validation study shows improvement)
14. Automatic syllable segmentation (reduce clinician labor)
15. Multi-language support (Cantonese, Vietnamese)
16. EHR integration (HL7 FHIR export)
17. Tele-health mode (remote assessment, encrypted video)

## Success Metrics

### Clinical Validity
- **Test-retest reliability:** ICC > 0.90 (same patient, same recording, same score)
- **Inter-rater reliability:** ICC > 0.85 (two clinicians, same patient, similar scores)
- **Criterion validity:** r > 0.80 with gold standard (expert clinician rating)
- **Sensitivity/specificity:** >80% correctly identify patients with deficits

### Usability
- **Clinician training time:** <2 hours to proficiency
- **Assessment time:** <10 minutes per patient (including setup)
- **User satisfaction:** "Would recommend" from 80%+ SLPs

### Regulatory
- **HIPAA compliance:** Pass security audit
- **FDA clearance:** (Optional, if marketed as medical device) Class II clearance
- **CE mark:** (EU) Medical device directive compliance

## Cost Estimate

### Development (Months 1-12)
- Clinical-grade software: $80,000 (secure, offline, EHR-ready)
- Validation study: $40,000 (recruit patients, test reliability, publish paper)
- Regulatory consulting: $20,000 (HIPAA, FDA, CE guidance)
- Normative data collection: $30,000 (recruit 200 controls, test)
- **Subtotal:** $170,000

### Regulatory (If Pursuing FDA/CE)
- FDA 510(k) submission: $50,000-$100,000 (predicate device, clinical data)
- CE mark (EU): $30,000-$50,000 (ISO 13485, technical file)
- **Subtotal:** $80,000-$150,000 (optional, depends on marketing claims)

### Ongoing (Year 1)
- Support and maintenance: $20,000
- Continued validation (expand norms): $10,000
- Marketing to SLPs: $30,000
- **Subtotal:** $60,000

**Total Year 1 (No regulatory):** $230,000
**Total Year 1 (With FDA/CE):** $310,000-$380,000

### Revenue (Per-Clinic License)
- One-time license: $1,000-$2,000 per clinic
- Or annual subscription: $300-$500/year per clinic
- Target: 100-200 clinics Year 1 → $100K-$200K revenue

## Critical Risks

### Risk 1: Atypical Speech Not Recognized
**Probability:** High (patients have abnormal voicing, pauses)
**Impact:** High (misdiagnosis)
**Mitigation:**
- Test on clinical populations (hearing loss, aphasia, L2)
- Allow manual override (clinician can correct)
- Provide confidence scores (flag uncertain cases)
- Validation study with SLP gold standard

### Risk 2: Lack of Normative Data
**Probability:** High (norms don't exist for many groups)
**Impact:** Medium (can't determine percentiles)
**Mitigation:**
- Use published norms where available (adult Mandarin speakers)
- Collect local norms (regional dialects, age groups)
- Report raw scores + percentiles (clinicians interpret)

### Risk 3: Regulatory Delays
**Probability:** Medium (FDA clearance can take 6-12 months)
**Impact:** High (delays market entry)
**Mitigation:**
- Start without FDA clearance (wellness tool, not diagnostic device)
- Pursue 510(k) in Year 2 (predicate device exists)
- CE mark first (easier than FDA)

### Risk 4: Clinician Adoption
**Probability:** Medium (SLPs may prefer subjective judgment)
**Impact:** High (no sales)
**Mitigation:**
- Involve SLPs in design (user-centered development)
- Validation study shows reliability (publish in JSLHR)
- Continuing education credits (train SLPs, build trust)
- Frame as "assistant" not "replacement"

## Alternatives Considered

### Alternative 1: Cloud-Based SaaS
**Approach:** Web app, audio uploaded to cloud for processing

**Pros:**
- Easier deployment (no installation)
- Automatic updates

**Cons:**
- HIPAA violation (unless BAA with cloud provider)
- Clinics won't trust (patient data privacy)
- Requires internet (not all clinics have reliable)

**Verdict:** Rejected. Desktop app required for clinical use.

### Alternative 2: Paper-Based Assessment (Manual Rating)
**Approach:** Clinician listens, rates tone accuracy on scale (1-5)

**Pros:**
- No software cost
- Clinician control

**Cons:**
- Subjective (low inter-rater reliability)
- Time-consuming
- No F0 measurements (can't track progress quantitatively)

**Verdict:** Automatic tool improves objectivity and efficiency.

### Alternative 3: Use Praat GUI Directly
**Approach:** Train clinicians to use Praat (free software)

**Pros:**
- Free, well-validated
- No development cost

**Cons:**
- Steep learning curve (not clinician-friendly)
- No patient database or progress tracking
- Manual F0 analysis (time-consuming)

**Verdict:** Praat is for researchers, not clinicians. Build clinician-friendly tool on top of Praat algorithms (Parselmouth).

## Clinical Use Case Examples

### Example 1: Pediatric Cochlear Implant
**Patient:** 6-year-old with cochlear implant (CI)
**Question:** Can child perceive and produce Mandarin tones after CI activation?

**Protocol:**
1. Pre-CI baseline: Tone accuracy = 25% (chance level for 4 tones)
2. 6 months post-CI: Tone accuracy = 60% (15th percentile for age)
3. 12 months post-CI: Tone accuracy = 75% (40th percentile)
4. Conclusion: Gradual improvement, recommend continued therapy

### Example 2: Post-Stroke Aphasia
**Patient:** 55-year-old with Broca's aphasia (left hemisphere stroke)
**Question:** Is lexical tone preserved (right hemisphere) or impaired?

**Protocol:**
1. Test comprehension: Minimal pairs (mā vs. má) → 95% accuracy (preserved)
2. Test production: Tone accuracy = 70% (below 5th percentile for age)
3. Breakdown: Tone 3 = 40% correct, others = 80%+ correct
4. Conclusion: Selective Tone 3 deficit, target in therapy

### Example 3: L2 Accent Modification
**Patient:** 30-year-old English speaker learning Mandarin
**Question:** Which tones need practice?

**Protocol:**
1. Initial assessment: Tone accuracy = 55% (T1=80%, T2=60%, T3=30%, T4=50%)
2. 10 weeks of practice (focus on T3): Tone accuracy = 75% (T3=60%)
3. Compare to native speaker norms: Still below 10th percentile
4. Recommendation: Continue T3 practice, add T4

## Next Steps After MVP

1. **Validation study** - Recruit 50 patients + 100 controls, test reliability
2. **Publish in JSLHR** - Journal of Speech, Language, and Hearing Research
3. **Pilot with 5 clinics** - Beta test, collect feedback
4. **Expand normative database** - More age groups, regional dialects
5. **Regulatory path** - Decide on FDA 510(k) or wellness tool

## References

### Clinical Assessment Tools
- [CAPT (Computer-Assisted Prosody Training)](https://doi.org/10.1044/1058-0360(2009/08-0016))
- [Praat for clinical voice analysis](https://doi.org/10.1044/2019_AJSLP-19-0017)

### Tone Perception and Production
- [Cochlear implant tone perception](https://doi.org/10.1121/1.4990968)
- [Aphasia and lexical tone](https://doi.org/10.1080/02687038.2016.1262867)
- [L2 tone acquisition](https://doi.org/10.1017/S0272263109990039)

### Normative Data
- [F0 norms for Mandarin](https://doi.org/10.1121/1.2217362) (Chen & Xu 2006)
- [Cantonese tone norms](https://doi.org/10.1159/000515438) (Ng et al. 2022)

### Regulatory
- [FDA Software as Medical Device guidance](https://www.fda.gov/medical-devices/software-medical-device-samd)
- [HIPAA compliance for health IT](https://www.hhs.gov/hipaa/for-professionals/index.html)
