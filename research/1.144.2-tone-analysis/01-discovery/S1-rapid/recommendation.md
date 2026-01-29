# S1 Rapid Pass: Recommendation

## Quick Summary

For CJK tone analysis and pitch detection, the landscape has **three viable options**, not two:

1. **Parselmouth** - Direct Praat access from Python (discovered during research)
2. **librosa** - Pure Python audio analysis
3. **praatio** - Python wrapper for Praat TextGrid manipulation

## Primary Recommendation: Parselmouth

**Winner: Parselmouth** for most CJK tone analysis use cases.

### Why Parselmouth?

✅ **Best of both worlds:**
- Praat-level accuracy (identical algorithms, direct C/C++ access)
- Pythonic interface (no external process, no scripting)
- Full Praat functionality (acoustic analysis + TextGrid manipulation)
- Active development (v0.5.0.dev0 released Jan 2026)

✅ **Ideal for:**
- Pronunciation practice tools (accurate pitch feedback)
- Speech recognition tuning (F0 feature extraction)
- Tone sandhi research (accurate F0 contours)
- Production applications (reliable, fast)

## Secondary Option: librosa

**When to use librosa:**

✅ **Choose librosa if:**
- Pure Python environment required (no Praat installation possible)
- Praat-level accuracy not critical
- Batch processing at scale (millions of files)
- Experimentation/prototyping phase
- Integration with music/audio pipelines

⚠️ **Be aware:**
- Lower accuracy for F0 mean and std dev vs. Praat
- Different voice onset/offset behavior
- Manual verification recommended for critical applications

## Tertiary Option: praatio

**When to use praatio:**

✅ **Choose praatio if:**
- Only need TextGrid file manipulation (not acoustic analysis)
- Already using external Praat scripts
- Legacy workflow compatibility required

⚠️ **Consider Parselmouth instead:**
- Parselmouth handles TextGrids AND acoustic analysis
- Better performance (no external process)
- More Pythonic interface

## Tone Sandhi Detection

⚠️ **None of these libraries provide built-in tone sandhi detection.**

Current approaches:
1. **Statistical modeling** - Growth curve analysis, F0 target models
2. **Neural networks** - CNNs achieving 97%+ accuracy
3. **Specialized tools** - SPPAS, ProsodyPro
4. **Custom implementation** - Pitch tracking + rule-based or ML models

**Recommendation:** Use Parselmouth for accurate pitch extraction, then implement custom tone sandhi rules on top.

## Implementation Path

### Phase 1: Pitch Detection
```python
# Install: pip install praat-parselmouth
import parselmouth

sound = parselmouth.Sound('audio.wav')
pitch = sound.to_pitch_ac(
    time_step=0.01,
    pitch_floor=80.0,   # Adjust for Mandarin/Cantonese
    pitch_ceiling=400.0
)
```

### Phase 2: Tone Classification
- Extract F0 contour from Parselmouth
- Normalize for speaker (z-score or min-max)
- Classify into tone categories (statistical or ML)

### Phase 3: Tone Sandhi Rules
- Implement rule-based system (e.g., 不 tone change before tone 4)
- Or train ML model on annotated tone sandhi examples

## Next Steps for S2

Deeper investigation needed:
1. **Parselmouth performance benchmarks** - Speed, memory, accuracy vs. Praat GUI
2. **Feature comparison matrix** - Parselmouth vs. librosa vs. praatio
3. **Tone classification algorithms** - HMM, GMM, CNN approaches
4. **Tone sandhi detection** - Existing research, implementation strategies
5. **Real-world examples** - Code samples for Mandarin/Cantonese

## Decision Matrix

| Factor | Parselmouth | librosa | praatio |
|--------|-------------|---------|---------|
| Accuracy | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Pure Python | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| Performance | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ |
| Ease of Use | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| Maintenance | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ |
| Dependencies | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ |

**Overall:** Parselmouth wins for most use cases. Use librosa only if Praat installation is impossible.
