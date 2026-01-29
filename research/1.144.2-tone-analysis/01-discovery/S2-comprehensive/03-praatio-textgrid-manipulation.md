# S2 Comprehensive: praatio Advanced Features

## Executive Summary

**praatio** (formerly praatIO) is a Python library for working with Praat, TextGrids, time-aligned audio transcripts, and audio files. It's primarily designed for feature extraction and manipulations on hierarchical time-aligned transcriptions.

**Key Verdict:**
- ✅ **Specialized for TextGrid manipulation** (robust API)
- ✅ **Multiple output formats** (short, long, JSON)
- ✅ **Praat script integration** (run Praat scripts from Python)
- ⚠️ **External Praat dependency** for acoustic analysis
- ⚠️ **Limited maintenance** (fewer updates than Parselmouth)

**Use Case:** Choose praatio when you need advanced TextGrid manipulation but don't need acoustic analysis, OR when integrating existing Praat script workflows into Python.

**Recommendation:** **Use Parselmouth instead** for most use cases—it provides TextGrid support PLUS acoustic analysis in a more integrated package.

---

## 1. Complete API Overview

### 1.1 Core Components

praatio organizes data around three main classes:

1. **Textgrid** - Container for multiple annotation tiers
2. **IntervalTier** - Tier containing interval data (start, end, label)
3. **PointTier** - Tier containing point data (time, label)

**Hierarchy:**
```
Textgrid
├── IntervalTier (e.g., "words", "syllables", "phones")
│   └── Interval(xmin, xmax, text)
└── PointTier (e.g., "tones", "events")
    └── Point(time, text)
```

### 1.2 Reading TextGrids

```python
from praatio import textgrid

# Read TextGrid from file
tg = textgrid.openTextgrid('annotation.TextGrid', includeEmptyIntervals=False)

# Access tiers
tier = tg.getTier('words')  # By name
tier = tg.tiers[0]          # By index

# Get tier info
print(f"Tier name: {tier.name}")
print(f"Tier type: {tier.tierType}")  # 'IntervalTier' or 'PointTier'
print(f"Min time: {tier.minTimestamp}")
print(f"Max time: {tier.maxTimestamp}")
print(f"Number of entries: {len(tier.entries)}")
```

### 1.3 Creating TextGrids

```python
from praatio.data_classes import textgrid

# Create new TextGrid
tg = textgrid.Textgrid()
tg.minTimestamp = 0.0
tg.maxTimestamp = 10.0

# Create interval tier
from praatio.data_classes.interval_tier import IntervalTier

word_tier = IntervalTier(
    name='words',
    entries=[
        (0.0, 1.5, 'hello'),
        (1.5, 3.0, 'world'),
        (3.0, 10.0, '')
    ],
    minT=0.0,
    maxT=10.0
)

# Add tier to TextGrid
tg.addTier(word_tier)

# Create point tier (for tone markers)
from praatio.data_classes.point_tier import PointTier

tone_tier = PointTier(
    name='tones',
    entries=[
        (0.75, 'T1'),  # Tone 1 at midpoint of "hello"
        (2.25, 'T4')   # Tone 4 at midpoint of "world"
    ],
    minT=0.0,
    maxT=10.0
)

tg.addTier(tone_tier)

# Save TextGrid
tg.save('output.TextGrid', format='long_textgrid', includeBlankSpaces=True)
```

### 1.4 Modifying TextGrids

```python
# Insert new interval
tier.insertEntry((3.0, 4.5, 'new_word'), collisionMode='replace')

# Delete interval
tier.deleteEntry((1.5, 3.0, 'world'))

# Modify interval
tier.modifyEntries(
    entries=[(0.0, 1.5, 'hello')],
    newEntries=[(0.0, 1.5, 'HELLO')],  # Change label
    collisionMode='replace'
)

# Crop tier to time range
tier.crop(startTime=1.0, endTime=8.0, mode='truncated', rebaseToZero=True)

# Merge consecutive intervals with same label
from praatio import tgio

tier_merged = tgio.eraseRegion(tier, start=None, end=None, mode='strict')
```

---

## 2. File Format Support

### 2.1 Four Output Formats

praatio supports 4 TextGrid output file types:

1. **Short TextGrid** - Praat native, more concise
2. **Long TextGrid** - Praat native, more human-readable
3. **JSON** - Standard JSON format
4. **TextGrid-like JSON** - Custom JSON format

**Comparison:**

```python
# Save in different formats
tg.save('output_short.TextGrid', format='short_textgrid')
tg.save('output_long.TextGrid', format='long_textgrid')
tg.save('output.json', format='json')
tg.save('output_tg.json', format='textgrid_json')
```

**Format Details:**

| Format | Praat Native | Human-Readable | File Size | Use Case |
|--------|--------------|----------------|-----------|----------|
| **Short** | ✅ Yes | ⭐⭐ Fair | Small | Production, storage |
| **Long** | ✅ Yes | ⭐⭐⭐⭐ Good | Large | Manual editing, review |
| **JSON** | ❌ No | ⭐⭐⭐⭐⭐ Excellent | Medium | Web apps, APIs |
| **TextGrid JSON** | ❌ No | ⭐⭐⭐⭐ Good | Medium | praatio-specific workflows |

### 2.2 Format Conversion

```python
from praatio import textgrid

# Read in any format
tg = textgrid.openTextgrid('input.TextGrid')

# Convert format by saving
tg.save('output.json', format='json')
tg.save('output_long.TextGrid', format='long_textgrid')
```

---

## 3. Batch Processing Examples

### 3.1 Basic Batch Processing

```python
from pathlib import Path
from praatio import textgrid

def batch_process_textgrids(input_dir, output_dir, operation):
    """
    Apply operation to all TextGrids in directory.

    Args:
        input_dir: Directory containing .TextGrid files
        output_dir: Directory for output files
        operation: Function that takes Textgrid and returns modified Textgrid
    """

    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)

    for tg_file in input_path.glob('*.TextGrid'):
        print(f"Processing {tg_file.name}...")

        # Load TextGrid
        tg = textgrid.openTextgrid(str(tg_file))

        # Apply operation
        tg_modified = operation(tg)

        # Save
        output_file = output_path / tg_file.name
        tg_modified.save(str(output_file), format='long_textgrid')

# Example operation: Rename a tier
def rename_tier(tg):
    tg.renameTier('old_name', 'new_name')
    return tg

# Usage
batch_process_textgrids(
    input_dir='input_textgrids/',
    output_dir='output_textgrids/',
    operation=rename_tier
)
```

### 3.2 Extract Intervals to Individual Files

```python
from praatio import textgrid, audio

def extract_syllables_to_wav(audio_path, textgrid_path, output_dir, tier_name='syllables'):
    """
    Extract each syllable interval to separate WAV file.
    """

    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)

    # Load TextGrid
    tg = textgrid.openTextgrid(textgrid_path)
    tier = tg.getTier(tier_name)

    # Load audio (requires pydub or audioread)
    from pydub import AudioSegment
    sound = AudioSegment.from_wav(audio_path)

    # Extract each interval
    for i, (start, end, label) in enumerate(tier.entries):
        if not label.strip():
            continue  # Skip empty intervals

        # Extract audio segment
        start_ms = int(start * 1000)
        end_ms = int(end * 1000)
        segment = sound[start_ms:end_ms]

        # Save
        output_file = output_path / f"{label}_{i:03d}.wav"
        segment.export(str(output_file), format='wav')

        print(f"Exported {output_file.name}")

# Usage
extract_syllables_to_wav(
    audio_path='recording.wav',
    textgrid_path='recording.TextGrid',
    output_dir='extracted_syllables/',
    tier_name='syllables'
)
```

### 3.3 Align Boundaries Across Tiers

```python
from praatio.utilities import utils

def align_boundaries_across_tiers(tg, reference_tier_name, tolerance=0.01):
    """
    Align boundaries across tiers to fix manual annotation errors.

    Args:
        tg: Textgrid object
        reference_tier_name: Name of tier to use as reference
        tolerance: Maximum time difference for alignment (seconds)
    """

    reference_tier = tg.getTier(reference_tier_name)

    # Get reference boundaries
    reference_boundaries = set()
    for start, end, _ in reference_tier.entries:
        reference_boundaries.add(start)
        reference_boundaries.add(end)

    # Align other tiers
    for tier in tg.tiers:
        if tier.name == reference_tier_name:
            continue

        new_entries = []
        for start, end, label in tier.entries:
            # Find closest reference boundary
            closest_start = min(reference_boundaries, key=lambda x: abs(x - start))
            closest_end = min(reference_boundaries, key=lambda x: abs(x - end))

            # Only align if within tolerance
            if abs(closest_start - start) <= tolerance:
                start = closest_start
            if abs(closest_end - end) <= tolerance:
                end = closest_end

            new_entries.append((start, end, label))

        # Update tier
        tier.entries = new_entries

    return tg

# Usage
tg = textgrid.openTextgrid('annotation.TextGrid')
tg_aligned = align_boundaries_across_tiers(tg, reference_tier_name='words', tolerance=0.01)
tg_aligned.save('annotation_aligned.TextGrid', format='long_textgrid')
```

### 3.4 Merge TextGrids from Multiple Annotators

```python
def merge_textgrids_multi_annotator(textgrid_paths, output_path):
    """
    Merge TextGrids from multiple annotators into single file.

    Each annotator's tiers get prefixed with annotator name.
    """

    # Load first TextGrid as base
    tg_merged = textgrid.openTextgrid(textgrid_paths[0])

    # Rename tiers with annotator prefix
    for tier in tg_merged.tiers:
        tier.name = f"annotator1_{tier.name}"

    # Add tiers from other annotators
    for i, tg_path in enumerate(textgrid_paths[1:], start=2):
        tg = textgrid.openTextgrid(tg_path)

        for tier in tg.tiers:
            tier_copy = tier.new(name=f"annotator{i}_{tier.name}")
            tg_merged.addTier(tier_copy)

    # Save merged TextGrid
    tg_merged.save(output_path, format='long_textgrid')

    return tg_merged

# Usage
merge_textgrids_multi_annotator(
    textgrid_paths=[
        'annotator1.TextGrid',
        'annotator2.TextGrid',
        'annotator3.TextGrid'
    ],
    output_path='merged_annotations.TextGrid'
)
```

---

## 4. Integration with Praat Scripts

### 4.1 Running Praat Scripts from Python

praatio includes `praat_scripts.py` for running Praat scripts from Python:

```python
from praatio import praat_scripts

# Run Praat script
praat_scripts.runPraatScript(
    scriptFn='extract_f0.praat',
    argList=['input.wav', '75', '500'],  # Arguments to script
    outputFn='output.txt'
)
```

### 4.2 Extract Pitch and Intensity

```python
from praatio.utilities import pitch_and_intensity

# Extract pitch using Praat
pitch_data = pitch_and_intensity.extractPI(
    inputFN='audio.wav',
    outputFN='pitch.txt',
    praatEXE='/usr/bin/praat',  # Path to Praat executable
    minPitch=75,
    maxPitch=500,
    sampleStep=0.01,
    silenceThreshold=0.03,
    voiceThreshold=0.45
)
```

**Note:** This requires Praat to be installed separately.

### 4.3 Known Limitations

**Short segments issue (GitHub Issue #20):**
> "Short segments (word length or shorter) can cause errors from Praat even with fixes, as Praat needs a certain minimum window size to get good results, though phrase-length or longer segments work fine."

**PraatExecutionFailed errors:**
- Occurs when optional arguments receive incorrect values
- Praat's error messages may be cryptic
- Requires debugging Praat script directly

**Workaround:**
- Use Parselmouth for acoustic analysis (no external Praat needed)
- Use praatio only for TextGrid manipulation

---

## 5. Comparison: praatio vs. TextGridTools vs. Parselmouth

### 5.1 Feature Comparison

| Feature | praatio | TextGridTools | Parselmouth |
|---------|---------|---------------|-------------|
| **TextGrid Read/Write** | ✅ Excellent | ✅ Excellent | ✅ Good |
| **Multiple Formats** | ✅ 4 formats | ⭐⭐ 2 formats | ⭐⭐ 2 formats |
| **Interval Manipulation** | ✅ Extensive | ✅ Extensive | ⭐⭐⭐ Basic |
| **Point Tier Support** | ✅ Yes | ✅ Yes | ✅ Yes |
| **Batch Processing** | ✅ Examples | ⭐⭐ Manual | ⭐⭐ Manual |
| **Praat Script Integration** | ✅ Built-in | ❌ No | ✅ Built-in (better) |
| **Acoustic Analysis** | ⚠️ Via Praat | ❌ No | ✅ Built-in |
| **Interannotator Agreement** | ❌ No | ✅ Yes | ❌ No |
| **Dependencies** | Minimal | Minimal | Zero |
| **Maintenance** | ⭐⭐ Low | ⭐⭐ Low | ⭐⭐⭐⭐⭐ Active |

### 5.2 praatio Advantages

**✅ Choose praatio if:**
1. **Advanced TextGrid manipulation** required
2. **Multiple output formats** needed (JSON export)
3. **Existing Praat script workflows** to integrate
4. **Batch processing utilities** helpful

### 5.3 Parselmouth Advantages

**✅ Choose Parselmouth if:**
1. **Acoustic analysis + TextGrid** manipulation in one package
2. **No external Praat** installation possible
3. **Active maintenance** important
4. **TextGridTools integration** via `to_tgt()` sufficient

**Verdict:** For most tone analysis workflows, **Parselmouth is superior** because it combines TextGrid manipulation with acoustic analysis in a more integrated, actively maintained package.

---

## 6. Practical Workflow Example: Mandarin Tone Corpus

### 6.1 Complete Pipeline

```python
from praatio import textgrid, audio
from pathlib import Path
import pandas as pd
import parselmouth  # Using Parselmouth for F0 extraction

def process_mandarin_corpus(
    audio_dir='corpus/audio/',
    textgrid_dir='corpus/textgrids/',
    output_csv='tone_features.csv'
):
    """
    Extract tone features from Mandarin corpus with TextGrid annotations.
    """

    results = []

    audio_files = Path(audio_dir).glob('*.wav')

    for audio_file in audio_files:
        # Find corresponding TextGrid
        tg_file = Path(textgrid_dir) / f"{audio_file.stem}.TextGrid"

        if not tg_file.exists():
            print(f"Warning: No TextGrid for {audio_file.name}")
            continue

        # Load TextGrid (using praatio)
        tg = textgrid.openTextgrid(str(tg_file))

        # Get syllable tier
        syllable_tier = tg.getTier('syllables')

        # Load audio (using Parselmouth for F0 extraction)
        sound = parselmouth.Sound(str(audio_file))
        pitch = sound.to_pitch_ac(pitch_floor=75, pitch_ceiling=500)

        # Process each syllable
        for i, (start, end, label) in enumerate(syllable_tier.entries):
            if not label.strip():
                continue

            # Extract F0 values in interval
            f0_values = []
            for t in pitch.xs():
                if start <= t <= end:
                    f0 = pitch.get_value_at_time(t)
                    if f0 > 0:
                        f0_values.append(f0)

            if len(f0_values) < 3:
                continue  # Insufficient data

            # Compute features
            import numpy as np
            results.append({
                'file': audio_file.name,
                'syllable_index': i,
                'syllable': label,
                'start': start,
                'end': end,
                'duration': end - start,
                'f0_mean': np.mean(f0_values),
                'f0_std': np.std(f0_values),
                'f0_min': np.min(f0_values),
                'f0_max': np.max(f0_values),
                'f0_range': np.max(f0_values) - np.min(f0_values)
            })

    # Save to CSV
    df = pd.DataFrame(results)
    df.to_csv(output_csv, index=False)

    print(f"Processed {len(results)} syllables -> {output_csv}")

    return df

# Usage
df = process_mandarin_corpus()
print(df.head())
```

### 6.2 Create TextGrid from Forced Alignment

```python
from praatio.data_classes import textgrid, interval_tier

def create_textgrid_from_alignment(
    audio_path,
    alignment_data,
    output_path
):
    """
    Create TextGrid from forced alignment output.

    Args:
        audio_path: Path to audio file
        alignment_data: List of (start, end, label) tuples
        output_path: Path for output TextGrid
    """

    # Get audio duration
    sound = parselmouth.Sound(audio_path)
    duration = sound.duration

    # Create TextGrid
    tg = textgrid.Textgrid()
    tg.minTimestamp = 0.0
    tg.maxTimestamp = duration

    # Create word tier
    word_tier = interval_tier.IntervalTier(
        name='words',
        entries=alignment_data,
        minT=0.0,
        maxT=duration
    )

    tg.addTier(word_tier)

    # Save
    tg.save(output_path, format='long_textgrid')

    return tg

# Example alignment data (from Montreal Forced Aligner, etc.)
alignment = [
    (0.0, 0.5, 'ni3'),
    (0.5, 1.0, 'hao3'),
    (1.0, 1.5, 'ma1'),
    (1.5, 2.0, '')
]

create_textgrid_from_alignment(
    audio_path='greeting.wav',
    alignment_data=alignment,
    output_path='greeting.TextGrid'
)
```

---

## 7. Limitations & Workarounds

### 7.1 Known Limitations

1. **External Praat dependency for acoustic analysis**
   - **Workaround:** Use Parselmouth for F0/formant extraction

2. **Short segment issues with Praat scripts**
   - **Workaround:** Process only phrase-length or longer segments

3. **Limited maintenance compared to Parselmouth**
   - **Workaround:** Use Parselmouth for new projects

4. **No built-in interannotator agreement metrics**
   - **Workaround:** Use TextGridTools for this feature

5. **Manual error handling for Praat script failures**
   - **Workaround:** Wrap in try-except with fallback logic

### 7.2 Best Practices

**File Management:**
- Use consistent naming: `audio.wav` + `audio.TextGrid`
- Store TextGrids in separate directory from audio
- Use version control for TextGrid files

**Annotation Guidelines:**
- Enforce tier naming conventions across corpus
- Use empty intervals for pauses (don't delete them)
- Document tier structure in README

**Quality Control:**
- Always validate TextGrid structure after modifications
- Check for overlapping intervals
- Verify tier boundaries align with audio duration

**Performance:**
- Cache loaded TextGrids if accessing multiple times
- Use batch processing for large corpora
- Consider parallel processing with multiprocessing

---

## 8. Migration Guide: praatio → Parselmouth

If you're using praatio primarily for TextGrid manipulation, consider migrating to Parselmouth:

### 8.1 Equivalent Operations

| praatio | Parselmouth |
|---------|-------------|
| `textgrid.openTextgrid(path)` | `parselmouth.TextGrid.read(path)` |
| `tg.getTier('name')` | `tg['name']` |
| `tier.entries` | `tier.intervals` (for IntervalTier) |
| `(start, end, label)` | `interval.xmin, interval.xmax, interval.text` |
| `tg.save(path, format='long_textgrid')` | `tg.save(path)` |

### 8.2 Migration Example

**Before (praatio):**
```python
from praatio import textgrid

tg = textgrid.openTextgrid('annotation.TextGrid')
tier = tg.getTier('words')

for start, end, label in tier.entries:
    print(f"{label}: {start} - {end}")
```

**After (Parselmouth):**
```python
import parselmouth

tg = parselmouth.TextGrid.read('annotation.TextGrid')
tier = tg['words']

for interval in tier.intervals:
    print(f"{interval.text}: {interval.xmin} - {interval.xmax}")
```

### 8.3 What You Gain

- ✅ Acoustic analysis built-in (no external Praat)
- ✅ Active maintenance (v0.5.0.dev0, January 2026)
- ✅ Identical Praat accuracy for F0/formants
- ✅ Zero external dependencies

### 8.4 What You Lose

- ⚠️ Multiple output formats (Parselmouth has fewer)
- ⚠️ Some batch processing utilities (need to rebuild)
- ⚠️ Specific praatio convenience functions

---

## 9. Summary Recommendations

### ✅ Use praatio if:

1. **Legacy workflows** with existing praatio code
2. **JSON export** required for TextGrids
3. **Specialized TextGrid manipulation** not available in Parselmouth
4. **Already using Praat externally** for acoustic analysis

### ⚠️ Consider alternatives:

1. **Parselmouth** - For integrated TextGrid + acoustic analysis
2. **TextGridTools** - For interannotator agreement metrics
3. **Custom scripts** - For simple TextGrid parsing (standard text format)

### Overall Verdict:

For **new projects** involving CJK tone analysis, **use Parselmouth** instead of praatio. It provides:
- TextGrid manipulation (sufficient for most needs)
- Built-in acoustic analysis (no external Praat)
- Active development and maintenance
- Identical Praat accuracy

Use praatio **only if** you specifically need its advanced TextGrid manipulation features or JSON export capabilities.

---

## Sources

- [praatio GitHub Repository](https://github.com/timmahrt/praatIO)
- [praatio PyPI Package](https://pypi.org/project/praatio/)
- [praatio API Documentation](http://timmahrt.github.io/praatIO/praatio.html)
- [praatio TextGrid API](http://timmahrt.github.io/praatIO/praatio/textgrid.html)
- [praatio Issue #20: Wrong parameters with get_pitch_and_intensity](https://github.com/timmahrt/praatIO/issues/20)
- [TextGridTools Documentation](https://textgridtools.readthedocs.io/)
- [Praat Scripting Tutorial](https://hrbosker.github.io/resources/scripts/batch-processing/)
- [Praat Batch Processing Examples](http://www.mattwinn.com/praat.html)
