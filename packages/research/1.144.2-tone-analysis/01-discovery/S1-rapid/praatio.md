# praatio: Python Library for Praat TextGrids

## Overview
Pure Python library for working with Praat TextGrid files and running Praat scripts from Python.

**Version**: 6.2.0 (current as of 2026)
**Python Support**: 3.7-3.12

## Core Functionality

### Pitch Extraction
`pitch_and_intensity.extractPI()` - Extracts F0 and intensity via Praat

### TextGrid Operations
- Reading/writing TextGrid files (short, long, JSON formats)
- Tier manipulation (union, difference, intersection)
- Time-aligned annotation management
- Hierarchical annotations (utterance > word > syllable > phone)

## Basic Usage

```python
from praatio import pitch_and_intensity
from praatio.utilities import utils
from os.path import join

# Setup paths
wavPath = "path/to/wavfiles"
outputFolder = "path/to/output"
pitchPath = join(outputFolder, "pitch")

# Praat executable location
praatEXE = "/Applications/Praat.app/Contents/MacOS/Praat"  # Mac
# praatEXE = r"C:\Praat.exe"  # Windows

# Create output directories
utils.makeDir(outputFolder)
utils.makeDir(pitchPath)

# Extract pitch and intensity
# Male: 50-350 Hz, Female: 75-450 Hz
pitchData = pitch_and_intensity.extractPI(
    join(wavPath, "audio.wav"),
    join(pitchPath, "audio.txt"),
    praatEXE,
    50,   # minPitch
    350,  # maxPitch
    forceRegenerate=False
)

# Result: list of tuples (time, pitch, intensity)
pitchOnly = [(time, pitch) for time, pitch, _ in pitchData]
```

## Strengths

1. **Leverages Praat accuracy** - Uses proven Praat algorithms
2. **TextGrid integration** - Excellent for time-aligned annotations
3. **Phonetics research standard** - Praat is gold standard
4. **Multi-tier support** - Complex hierarchical annotations
5. **Pure Python for files** - No Praat scripting needed for TextGrid ops
6. **Tutorial resources** - IPython notebooks available

## Weaknesses

1. **Requires Praat installation** - Must have separate Praat executable
2. **External process overhead** - Slower than native Python
3. **Maintenance concerns** - May be inactive project (sources vary)
4. **Limited functionality** - Primarily file manipulation, not full Praat access
5. **No real-time processing** - External calls unsuitable for interactive use
6. **Manual parameter tuning** - Requires Praat expertise

## Important Note: Parselmouth Alternative

**Parselmouth** (v0.5.0.dev0, Jan 2026) may be superior for acoustic analysis:

- **Direct C/C++ access** - Accesses Praat internals (no external process)
- **Identical results** - Exact same algorithms as Praat GUI
- **Full functionality** - Complete Praat feature access
- **Better performance** - No external process overhead
- **Active development** - Recent 2026 release

### Parselmouth Example

```python
import parselmouth

# Load sound
sound = parselmouth.Sound('audio.wav')

# Extract pitch (exactly like Praat's 'To Pitch (ac)...')
pitch = sound.to_pitch_ac(
    time_step=0.01,
    pitch_floor=75.0,
    pitch_ceiling=600.0
)

# Get pitch values
pitch_values = pitch.selected_array['frequency']
```

### When to Use Which

- **Parselmouth**: Acoustic analysis using Praat algorithms from Python
- **praatio**: TextGrid manipulation and annotation work only

## Use Cases for CJK

✅ **Good for:**
- Projects already using Praat workflows
- Time-aligned tone annotations
- Phonetics research requiring Praat-level accuracy
- Multi-tier annotation management

❌ **Not ideal for:**
- Pure Python environments (requires Praat install)
- Real-time or interactive applications
- High-throughput batch processing (external process overhead)

## Sources
- [praatio GitHub repository](https://github.com/timmahrt/praatIO)
- [praatio PyPI page](https://pypi.org/project/praatio/)
- [Parselmouth documentation](https://parselmouth.readthedocs.io/)
