# Use Case 04: Content Creation & Quality Control

## User Archetype

**Who:** Audiobook narrators, podcast hosts, dubbing actors, content moderators
**Context:** Professional audio production in tonal languages (Mandarin, Cantonese)
**Goal:** Quality control for tone accuracy before publication/distribution
**Technical sophistication:** Low (non-technical creatives, not programmers)

## Core Requirements

### Functional
1. **Spot-check tone errors** - Quickly scan recording for mispronounced tones
2. **Visual feedback** - Highlight suspicious segments (not "your Tone 3 is 2.3 semitones too low")
3. **No false alarms** - Wrong corrections break creative flow
4. **Batch processing** - Process entire podcast episode (30-60 minutes)
5. **Export reports** - Flag timestamps for re-recording ("Minute 12:34 - check tone")

### Non-Functional
- **False positive rate:** <5% (prefer missing errors to false alarms)
- **Processing time:** 1-2× real-time (30-minute podcast → 30-60 minute analysis)
- **Ease of use:** No command-line, drag-and-drop interface
- **Integration:** Works with Adobe Audition, Audacity, or standalone
- **Cost:** <$50/month subscription (professional tool budget)

## Technical Challenges

### Challenge 1: Natural Speech Variation
- Professional narrators have consistent style (not errors)
- Emotional delivery changes F0 (intentional, not mistakes)
- Need to distinguish: stylistic choice vs. wrong tone

### Challenge 2: Expressive Speech
- Audiobooks: Character voices (high-pitched child vs. low-pitched elder)
- Podcasts: Laughter, excitement, sarcasm all affect F0
- Need to handle: intonation overlaid on lexical tone

### Challenge 3: Non-Technical Users
- Can't debug Python scripts or tune thresholds
- Need clear explanations: "This syllable sounds flat (Tone 1), but the word expects rising (Tone 2)"
- GUI required, not command-line

### Challenge 4: Professional Quality Standards
- Listeners notice tone errors (unlike casual speech)
- One mispronounced tone ruins immersion in audiobook
- But: over-correction slows production (time is money)

## Recommended Stack: GUI-Based QC Tool

### Architecture
```
Audio File (WAV/MP3)
↓
Parselmouth (F0 extraction)
↓
Whisper ASR (transcript with timestamps)
↓
Dictionary lookup (expected tones)
↓
Compare: Realized tone vs. Expected tone
↓
Flag mismatches (with confidence scores)
↓
GUI: Highlight suspicious segments
↓
User: Listen, decide keep/re-record
```

### Component Choices

**Pitch Detection: Parselmouth**
- Rationale: Accurate, robust to expressive speech
- Batch processing: 30-minute episode in 60 minutes (1-2× real-time)

**Speech Recognition: Whisper (OpenAI)**
- Rationale: State-of-the-art Mandarin ASR, provides transcript + timestamps
- Necessary for: Knowing which word was said (to look up expected tone)
- Alternative: User provides transcript manually (slower)

**Tone Classification: Hybrid (Dictionary + Verification)**

*Step 1: Dictionary lookup*
- Use transcript to get expected tone (e.g., "妈" = Tone 1)
- Chinese dictionary with pinyin (CC-CEDICT or similar)

*Step 2: Realized tone detection*
- Extract F0 contour from audio (Parselmouth)
- Classify realized tone (rule-based or CNN)

*Step 3: Compare and flag*
- If expected ≠ realized AND confidence > 0.8, flag for review
- If confidence < 0.8, don't flag (avoid false positives)

**GUI: Electron or Web App**
- Waveform display (like Audacity)
- Highlighted regions for flagged errors
- Play button to listen to segment
- "Keep" or "Re-record" buttons
- Export report (CSV with timestamps)

### Implementation

**Backend (Python):**
```python
import parselmouth
import whisper
import pandas as pd

# Load Whisper model
model = whisper.load_model("large")

def analyze_audio(audio_path):
    """Main QC pipeline"""

    # Step 1: ASR transcript with timestamps
    result = model.transcribe(audio_path, language="zh", word_timestamps=True)
    transcript = result["text"]
    words = result["segments"]  # [(word, start_time, end_time), ...]

    # Step 2: F0 extraction
    sound = parselmouth.Sound(audio_path)
    pitch = sound.to_pitch_ac(time_step=0.01, pitch_floor=75.0, pitch_ceiling=500.0)

    # Step 3: For each word, check tone
    errors = []
    for word_data in words:
        word = word_data["word"]
        start = word_data["start"]
        end = word_data["end"]

        # Dictionary lookup (expected tone)
        expected_tone = dictionary_lookup(word)  # Returns 1, 2, 3, 4, or 0 (neutral)

        if expected_tone is None:
            continue  # Word not in dictionary (proper noun, etc.)

        # Extract F0 contour for this word
        f0_contour = extract_f0_segment(pitch, start, end)

        # Classify realized tone
        realized_tone, confidence = classify_tone_with_confidence(f0_contour)

        # Compare
        if realized_tone != expected_tone and confidence > 0.8:
            errors.append({
                "timestamp": start,
                "word": word,
                "expected": expected_tone,
                "realized": realized_tone,
                "confidence": confidence
            })

    return errors

def dictionary_lookup(word):
    """Look up expected tone from dictionary"""
    # Use CC-CEDICT or custom dictionary
    # Example: "妈" (mā) → Tone 1
    # Return: 1, 2, 3, 4, or 0 (neutral)
    pass

def classify_tone_with_confidence(f0_contour):
    """Classify tone and return confidence score"""
    # Use CNN or rule-based
    # Return: (tone, confidence)
    # Example: (2, 0.92) means "Tone 2 with 92% confidence"
    pass

# Run analysis
errors = analyze_audio("podcast_episode.mp3")
df = pd.DataFrame(errors)
df.to_csv("qc_report.csv")
print(f"Found {len(errors)} potential tone errors.")
```

**Frontend (Electron app):**
```javascript
// Pseudocode for GUI
const { app, BrowserWindow, ipcMain } = require('electron');
const { spawn } = require('child_process');

// User drops audio file
ipcMain.on('analyze-file', (event, filePath) => {
  // Run Python backend
  const python = spawn('python', ['analyze.py', filePath]);

  python.stdout.on('data', (data) => {
    const errors = JSON.parse(data);
    // Display errors in GUI (waveform with highlights)
    event.reply('analysis-complete', errors);
  });
});

// User clicks "Keep" or "Re-record"
ipcMain.on('user-decision', (event, timestamp, decision) => {
  // Remove from report if "Keep"
  // Export final report with only "Re-record" items
});
```

## MVP Definition

### Must-Have (Month 1-2)
1. Drag-and-drop audio file input
2. Parselmouth F0 extraction
3. Whisper ASR for transcript + timestamps
4. Dictionary-based expected tone lookup
5. Rule-based tone classification
6. Flag mismatches (expected vs. realized)
7. CSV report export

### Should-Have (Month 3-4)
8. Waveform GUI with highlighted errors
9. In-app audio playback (click timestamp → hear segment)
10. "Keep" / "Re-record" buttons (filter false positives)
11. Confidence threshold slider (user adjusts sensitivity)

### Nice-to-Have (Month 5-6)
12. CNN tone classifier (better accuracy than rule-based)
13. User feedback loop (learn from "Keep" decisions)
14. Adobe Audition plugin (open in Audition at timestamp)
15. Cloud processing (upload → email report, no local install)

## Success Metrics

### User-Facing
- **Time savings:** 50% reduction in QC time vs. manual listening
- **Error catch rate:** 80%+ of real errors flagged
- **False positive rate:** <5% (minimal disruption to workflow)
- **User satisfaction:** "Helpful" rating from 75%+ users

### Technical
- **Processing speed:** 1-2× real-time (30-minute audio in 30-60 minutes)
- **Tone classification accuracy:** 87-90% (high enough to avoid false positives)
- **Whisper ASR accuracy:** >95% character error rate

## Cost Estimate

### Development (Months 1-6)
- Backend pipeline: $16,000 (Python, Parselmouth, Whisper integration)
- GUI development: $24,000 (Electron app, waveform display, audio playback)
- Dictionary integration: $4,000 (CC-CEDICT, pinyin lookup)
- Testing with narrators: $8,000 (user testing, iterate)
- **Subtotal:** $52,000

### Ongoing (Year 1)
- Cloud infrastructure: $6,000 ($500/month × 12, if cloud-based)
- Or desktop app: $0 (local processing)
- Whisper API costs: $0 (open-source model, run locally)
- Maintenance: $10,000
- **Subtotal:** $10,000-$16,000

### Revenue (SaaS Model)
- Subscription: $20-50/month per user
- Target users: Audiobook narrators (1000s), podcast studios (100s)
- Break-even: ~100 subscribers (× $30/month × 12 = $36K/year)

**Total Year 1:** $62,000-$68,000 (development + operations)

## Critical Risks

### Risk 1: False Positives Annoy Users
**Probability:** High (tone classification is imperfect)
**Impact:** High (users abandon tool)
**Mitigation:**
- Conservative threshold (only flag high-confidence errors)
- User feedback loop ("Keep" button removes from report)
- Display confidence scores (let user decide)
- Start with "suggestions" not "errors"

### Risk 2: Whisper ASR Errors Cascade
**Probability:** Medium (ASR is 95-98% accurate, not 100%)
**Impact:** High (wrong transcript → wrong expected tone → wrong flag)
**Mitigation:**
- Show transcript in GUI (user can correct)
- Skip low-confidence ASR segments
- Allow user to provide transcript manually (skip ASR)

### Risk 3: Expressive Speech False Alarms
**Probability:** High (F0 contours in expressive speech deviate from canonical)
**Impact:** Medium (flags are correct but user disagrees)
**Mitigation:**
- Train model on expressive speech (audiobook corpus, not read speech)
- Allow user to set "expressiveness threshold"
- Document: "This tool checks lexical tone, not emotional intonation"

## Alternatives Considered

### Alternative 1: Manual Listening (No Tool)
**Approach:** Narrator listens to entire recording, catches own errors

**Pros:**
- 100% accuracy (no false positives)
- No cost

**Cons:**
- Time-consuming (3-4× real-time, 30-minute podcast = 90-120 minutes QC)
- Human fatigue (miss errors after 30+ minutes)
- Expensive (narrator hourly rate)

**Verdict:** Tool reduces QC time by 50%+, worth the investment.

### Alternative 2: Peer Review (Human QC)
**Approach:** Second person listens and flags errors

**Pros:**
- Fresh ears catch errors narrator missed
- Human judgment (understands context)

**Cons:**
- Double the labor cost
- Requires Mandarin-speaking QC staff
- Still time-consuming

**Verdict:** Tool assists QC, doesn't replace (hybrid approach).

### Alternative 3: Real-Time Feedback (During Recording)
**Approach:** Flag errors while narrator is speaking (like pronunciation practice apps)

**Pros:**
- Immediate correction (no re-recording phase)

**Cons:**
- Disrupts flow (creative process vs. practice)
- Higher latency tolerance (<200ms, harder to achieve)
- False alarms more disruptive

**Verdict:** Post-production QC is less intrusive, better fit for professionals.

## User Workflow Example

**Scenario:** Audiobook narrator records Chapter 5 (45 minutes)

1. **Record:** Narrator records in one take, uploads to QC tool
2. **Process:** Tool runs analysis (45-90 minutes, narrator takes break)
3. **Review:** Tool highlights 8 potential tone errors
   - Timestamp 5:23 - "妈" (mā) sounded like Tone 3 (falling-rising), expected Tone 1 (high level)
   - Timestamp 12:47 - "买" (mǎi) sounded like Tone 2 (rising), expected Tone 3 (dipping)
   - ... (6 more)
4. **Decide:**
   - Listens to 5:23 → "Yes, that's wrong" → Mark for re-record
   - Listens to 12:47 → "No, that's correct (expressive delivery)" → Keep
   - Reviews all 8 → 5 real errors, 3 false positives
5. **Re-record:** Punch in fixes for 5 segments (10 minutes)
6. **Export:** Final chapter with corrections

**Time saved:**
- Without tool: Listen to 45 minutes (180 minutes @ 4× slowdown for careful listening)
- With tool: Review 8 flagged segments (8 minutes) + re-record (10 minutes) = 18 minutes
- Savings: 162 minutes (2.7 hours)

## Integration with Pro Tools

### Adobe Audition Plugin
- Export timestamps as markers
- Open audio in Audition with markers at error locations
- Narrator uses "Punch and Roll" to re-record segments

### Audacity Integration
- Export as label track (.txt)
- Import into Audacity project
- Labels appear on timeline

### Standalone GUI
- Waveform display with highlighted regions
- Built-in audio playback and editing

## Next Steps After MVP

1. **Beta test with narrators** - 10 professionals, collect feedback
2. **False positive analysis** - Which errors are real vs. false alarms?
3. **Model fine-tuning** - Train on audiobook/podcast data (not read speech)
4. **Expand to Cantonese** - 6 tones, different F0 ranges
5. **Real-time version** - Assist during recording (advanced feature)

## References

- [Whisper ASR](https://github.com/openai/whisper) (OpenAI 2022)
- [CC-CEDICT Chinese dictionary](https://www.mdbg.net/chinese/dictionary?page=cc-cedict) (community)
- [Parselmouth for Python](https://github.com/YannickJadoul/Parselmouth)
- Professional audio tools: Adobe Audition, Audacity
- Use case inspiration: Descript (transcription QC tool)
