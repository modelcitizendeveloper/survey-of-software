# S3 Scenario: Academic Research Interviews
## Experiment 3.202: Speech & Audio AI Services

**Scenario Type**: Academic Researcher with IRB Compliance
**Date**: 2025-11-24
**Audience**: Academic researchers, PhD students, qualitative researchers, IRB-regulated studies

---

## 1. Persona Summary

**Meet Dr. Maria Chen, Assistant Professor of Sociology**

Maria conducts qualitative research interviewing 20-30 participants per study about workplace experiences. Each interview lasts 60-90 minutes and is recorded with participant consent under IRB protocol. Her workflow: record on iPhone → manually transcribe 5-10 hours of audio per interview → code transcripts in NVivo → publish findings.

**Current Pain**: Transcription costs $1-2/minute for human services ($60-180 per interview) or requires 4-6 hours of manual transcription per interview. Grant budgets allow $1,000-5,000 for transcription across 30 interviews.

**Success Criteria**: Platform must deliver verbatim transcripts (95%+ accuracy), export to qualitative analysis software (NVivo, Atlas.ti, MAXQDA), comply with IRB data privacy requirements, and cost <$50/hour of audio (vs $60-120 human transcription).

---

## 2. Requirements Matrix

### Functional Requirements

| Requirement | Must-Have | Nice-to-Have |
|-------------|-----------|--------------|
| **Verbatim accuracy** (95%+ WER) | ✅ | |
| **Speaker diarization** (interviewer vs participant) | ✅ | |
| **Export formats** (DOCX, TXT, SRT for NVivo/Atlas.ti) | ✅ | |
| **Timestamps** (for coding in analysis software) | ✅ | |
| **Batch upload** (process 10-30 audio files at once) | ✅ | |
| **Custom vocabulary** (research-specific jargon) | | ✅ |
| **Multiple languages** (if international participants) | | ✅ |

### Non-Functional Requirements (IRB Compliance)

| Requirement | Must-Have | Notes |
|-------------|-----------|-------|
| **IRB-compliant data handling** | ✅ | No AI training on participant data |
| **Participant confidentiality** | ✅ | Auto-redact names, locations (or manual review) |
| **Data retention control** | ✅ | Delete transcripts after study ends |
| **Secure storage** | ✅ | SOC 2 or university-approved platform |
| **Audit trail** | | Nice-to-have for IRB documentation |

### Budget Constraints

- Grant budget: $100-1,000/year ($3-30 per interview)
- Break-even vs human transcription: Must be <$50/hour (vs $60-120/hour human)
- Preferred: Free tier or usage-based API

---

## 3. Platform Evaluation

### Option A: Rev AI (Highest Accuracy)

**Fit Score**: 8.5/10 (best for accuracy-critical research)

**Cost**: $2.10/hour (standard) or $1.20/hour (enterprise volume)
- 30 interviews × 1.5 hours × $1.20 = **$54/year** (enterprise)
- 3-Year: $162

**Pros**:
- ✅ 96%+ accuracy (best for verbatim quotes in publications)
- ✅ Hybrid AI+human option (upgrade critical interviews to 99% accuracy)
- ✅ Export SRT, TXT, DOCX (compatible with NVivo)
- ✅ IRB-compliant (SOC 2, data privacy guarantees)

**Cons**:
- ❌ Highest cost among APIs
- ❌ No bulk discount for researchers (vs rev.com $1.50/min for "low priority")

**Use Case Fit**: Best for research requiring verbatim accuracy for publication. Justify higher cost if NSF/NIH grant covers transcription.

---

### Option B: Whisper API (Cost Leader)

**Fit Score**: 9/10 (best cost/accuracy balance)

**Cost**: $0.36/hour
- 30 interviews × 1.5 hours × $0.36 = **$16/year**
- 3-Year: $48

**Pros**:
- ✅ Cheapest API (94x cheaper than human transcription)
- ✅ Good accuracy (92% / 7.88% WER) for clean audio
- ✅ 99 languages (international research)
- ✅ Export TXT, VTT, SRT (NVivo-compatible)
- ✅ Self-hosted option (100% local = IRB compliant by design)

**Cons**:
- ❌ Slower processing (~40% of audio duration)
- ❌ No speaker diarization native (requires WhisperX add-on)
- ❌ Hallucination issues on silence/music

**Use Case Fit**: Best for budget-conscious researchers. Self-hosted option ideal for sensitive participant data.

---

### Option C: Otter Pro (Ease of Use)

**Fit Score**: 7/10 (easiest for non-technical researchers)

**Cost**: $100/year (annual) or $204/year (monthly)
- 3-Year: $300

**Pros**:
- ✅ Zero technical setup (<30 min)
- ✅ 1,200 min/month (sufficient for 8 interviews × 90 min)
- ✅ Export DOCX, TXT, SRT
- ✅ Real-time transcription (review during interview)
- ✅ Educational discount (20% off with .edu email = $80/year)

**Cons**:
- ❌ Free tier limited (300 min/month, 30 min/meeting cap)
- ❌ No bulk upload (must upload interviews one-by-one)
- ❌ IRB concerns (data uploaded to Otter cloud, no HIPAA BAA disclosure)

**Use Case Fit**: Best for researchers who are non-technical and can afford $80-100/year. Not ideal if IRB requires self-hosted or HIPAA.

---

### Option D: AssemblyAI (PII Redaction)

**Fit Score**: 8/10 (best for sensitive participant data)

**Cost**: $0.37/hour
- 30 interviews × 1.5 hours × $0.37 = **$17/year**
- 3-Year: $51

**Pros**:
- ✅ PII redaction (auto-remove participant names, locations, phone numbers)
- ✅ Best accuracy (93.3% / 6.68% WER, fewer hallucinations)
- ✅ IRB-compliant (SOC 2, HIPAA BAA, data privacy guarantees)
- ✅ Custom vocabulary (research jargon)
- ✅ Export JSON, TXT, SRT

**Cons**:
- ❌ Requires API integration (not beginner-friendly)
- ❌ No bulk upload UI (must script batch processing)

**Use Case Fit**: Best for researchers handling sensitive participant data (medical, trauma, criminal justice studies). PII redaction ensures IRB compliance.

---

## 4. Recommendation

### Option A: Primary Recommendation (Budget-Conscious)

**Platform**: Whisper API (batch processing)

**Justification**:
- **$16/year** for 30 interviews (vs $1,800-5,400 human transcription)
- 99% cost savings vs human transcription
- Good accuracy (92%) for most research
- Self-hosted option (IRB-compliant by design)

**When to Use**: Grant budget <$500, international participants (99 languages), need self-hosted for IRB

**Implementation** (see Section 5 for full guide):
1. Install Whisper: `pip install openai-whisper` (5 min)
2. Batch process 30 interviews: `for f in *.m4a; do whisper "$f" --model large-v3 --output_format txt; done`
3. Import TXT files into NVivo/Atlas.ti

**3-Year TCO**: $48 (API) or $0 (self-hosted)

---

### Option B: Alternative (Accuracy-Critical)

**Platform**: Rev AI (Hybrid AI+Human)

**Justification**:
- **96%+ accuracy** (best for verbatim quotes in publications)
- Hybrid option (upgrade 5 critical interviews to 99% human accuracy)
- IRB-compliant (SOC 2, data privacy)

**When to Use**: NSF/NIH grant covers transcription ($1,000+ budget), accuracy critical for publication, need verbatim quotes

**3-Year TCO**: $162 (enterprise volume pricing)

---

### Option C: Easiest Setup (Non-Technical)

**Platform**: Otter Pro (with .edu discount)

**Justification**:
- **$80/year** with educational discount
- Zero technical setup
- Real-time transcription (review during interview)

**When to Use**: Non-technical researcher, can afford $80/year, IRB allows cloud SaaS

**3-Year TCO**: $240 (with .edu discount)

---

### Decision Matrix

| Situation | Recommended Platform | Cost (3-Year) | Key Benefit |
|-----------|---------------------|---------------|-------------|
| **Grant budget <$500** | Whisper API | $48 | 99% cost savings vs human |
| **IRB requires self-hosted** | Whisper (self-hosted) | $0 | 100% local processing |
| **Accuracy-critical (publication)** | Rev AI Hybrid | $162-486 | 96-99% accuracy |
| **Non-technical researcher** | Otter Pro (.edu) | $240 | Zero setup, real-time |
| **Sensitive participant data** | AssemblyAI | $51 | Auto-PII redaction |

---

## 5. Implementation Guide (Whisper API Batch Processing)

### Setup for Batch Transcription (30 Interviews)

**Prerequisites**:
- Audio files in folder: `~/Research/Interviews/Audio/`
- Interviews named: `Interview_01.m4a`, `Interview_02.m4a`, ..., `Interview_30.m4a`

**Step 1: Install Whisper** (5 min)

```bash
pip install openai-whisper
```

**Step 2: Batch Process All Interviews** (overnight)

```bash
cd ~/Research/Interviews/Audio/

# Process all interviews (takes ~45 min for 30 × 90-min interviews)
for audio_file in *.m4a; do
  whisper "$audio_file" \
    --model large-v3 \
    --language en \
    --output_format txt \
    --output_dir ../Transcripts/
done
```

**Processing Time**: 30 interviews × 90 min audio × 40% processing time = **1,080 min (18 hours)**

**Step 3: Add Speaker Diarization** (optional, +2 hours)

```bash
pip install whisperx

for audio_file in *.m4a; do
  whisperx "$audio_file" \
    --model large-v3 \
    --diarize \
    --hf_token YOUR_HUGGINGFACE_TOKEN \
    --output_dir ../Transcripts/
done
```

**Step 4: Import to NVivo**

1. Open NVivo → Import → Files → Select all TXT transcripts
2. NVivo auto-codes timestamps for easy reference
3. Begin qualitative coding (themes, patterns)

**Total Time**: 30 min setup + 18 hours processing (overnight) = **1 day**

---

### Sample Workflow

**Week 1: Conduct Interviews**
- Record 10 interviews on iPhone (Voice Memos app)
- Export audio files to Mac: `~/Research/Interviews/Audio/`

**Week 2: Transcribe**
- Run batch Whisper script (overnight)
- Wake up to 10 transcripts ready

**Week 3: Review & Code**
- Spot-check transcripts for accuracy (fix names, jargon)
- Import to NVivo
- Begin qualitative coding

**Time Saved**: 10 interviews × 5 hours manual transcription = **50 hours saved** (vs $600-1,800 if outsourced)

---

## 6. Architecture (Batch Processing Workflow)

### System Diagram

```
[Audio Recordings] (10-30 interviews, .m4a format)
    ↓
[Whisper API Batch Processing]
    ├─ Model: large-v3 (best accuracy)
    ├─ Language: en (or auto-detect)
    ├─ Output: TXT with timestamps
    └─ Processing: ~40% of audio duration
    ↓
[Transcript Files] (Interview_01.txt, Interview_02.txt, ...)
    ↓ (optional: manual review & anonymization)
[Anonymized Transcripts] (replace participant names with pseudonyms)
    ↓
[Import to Qualitative Analysis Software]
    ├─ NVivo (Import Files → Auto-code by paragraph)
    ├─ Atlas.ti (Create Project → Add Documents)
    └─ MAXQDA (Import Texts → Code Segments)
    ↓
[Qualitative Coding & Analysis]
```

---

### Python Script for Batch Processing + Anonymization

```python
#!/usr/bin/env python3
# batch_transcribe_anonymize.py

import subprocess
import re
from pathlib import Path

AUDIO_DIR = Path("~/Research/Interviews/Audio").expanduser()
OUTPUT_DIR = Path("~/Research/Interviews/Transcripts").expanduser()

# Participant pseudonyms (map real names to anonymous IDs)
PSEUDONYMS = {
    "John Smith": "Participant_01",
    "Jane Doe": "Participant_02",
    # Add all participant names here
}

# Step 1: Batch transcribe
audio_files = list(AUDIO_DIR.glob("*.m4a"))

for audio_file in audio_files:
    print(f"Transcribing {audio_file.name}...")
    subprocess.run([
        "whisper", str(audio_file),
        "--model", "large-v3",
        "--language", "en",
        "--output_format", "txt",
        "--output_dir", str(OUTPUT_DIR)
    ])

# Step 2: Anonymize transcripts (replace names with pseudonyms)
for transcript_file in OUTPUT_DIR.glob("*.txt"):
    with open(transcript_file, 'r') as f:
        text = f.read()

    # Replace real names with pseudonyms
    for real_name, pseudonym in PSEUDONYMS.items():
        text = re.sub(re.escape(real_name), pseudonym, text, flags=re.IGNORECASE)

    # Save anonymized version
    anonymized_file = OUTPUT_DIR / f"ANON_{transcript_file.name}"
    with open(anonymized_file, 'w') as f:
        f.write(text)

    print(f"✓ Anonymized: {anonymized_file.name}")

print("\n✓ All interviews transcribed and anonymized")
```

**Run**: `python batch_transcribe_anonymize.py`

---

## 7. Success Metrics

### Cost Savings

**Baseline** (human transcription):
- 30 interviews × 1.5 hours × $80/hour = **$3,600**

**Target** (Whisper API):
- 30 interviews × 1.5 hours × $0.36/hour = **$16**

**Savings**: $3,584 (99.6% cost reduction)

---

### Time Savings

**Baseline** (manual transcription):
- 30 interviews × 5 hours/interview = **150 hours**

**Target** (Whisper API):
- Setup: 0.5 hours
- Processing: 18 hours (overnight, automated)
- Review/anonymization: 30 hours (1 hour per interview)
- **Total**: 48.5 hours

**Time Saved**: 101.5 hours → **Value at $50/hr researcher time = $5,075**

---

### Quality

**Transcription Accuracy**:
- Manual: 99%+ (but takes 150 hours)
- Whisper: 92% (7.88% WER) - good for most research
- Rev AI: 96%+ (best if accuracy critical)

**IRB Compliance**:
- Self-hosted Whisper: 100% compliant (data never leaves device)
- Cloud APIs (Rev AI, AssemblyAI): Require BAA or data privacy review

---

### 3-Year ROI

**Scenario: PhD Student (Whisper API)**

**Investment**: $16/year × 3 years = $48

**Returns**:
- Cost savings vs human: $3,584/year
- Time savings: 101.5 hours/year × $50/hr = $5,075/year
- **Total Annual Return**: $8,659/year
- **3-Year Return**: $25,977

**Net ROI**: ($25,977 - $48) / $48 = **54,018%** (540x return)

---

## Summary

**Best for Budget-Conscious Researchers**: Whisper API ($48 over 3 years, 99% cost savings vs human)

**Best for Self-Hosted (IRB)**: Whisper self-hosted ($0, 100% local processing)

**Best for Accuracy-Critical**: Rev AI Hybrid ($162-486, 96-99% accuracy)

**Best for Non-Technical**: Otter Pro with .edu discount ($240, zero setup)

**Key Insight**: Automated transcription reduces costs by 99% and time by 68% vs manual/human transcription, making qualitative research accessible to grant-constrained academics.

---

**Last Updated**: 2025-11-24
**Scenario Type**: Academic Research Interviews
**Next Scenario**: content-podcast-transcription.md (content creator)
