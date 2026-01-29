# Use Case: Transcription & Conversion Tools

## Scenario Description
Tools for converting between different Chinese romanization systems, processing text that's already romanized, or working with linguistic data in multiple transcription formats.

## User Persona
- **Primary**: Translators, linguists, academic researchers
- **Secondary**: Data processors, document converters, archivists
- **Platforms**: Desktop applications, web tools, batch processing scripts
- **Scale**: Individual documents to large text corpora

## Examples of Real Applications
- **Academic publishing**: Convert Pinyin papers to Zhuyin for Taiwan journals
- **Subtitle conversion**: Convert romanized subtitles between formats
- **Data migration**: Standardize mixed-format historical data
- **Linguistic research**: Analyze romanization patterns across formats
- **Translation workflows**: Convert client-provided romanization to preferred format
- **Legacy system integration**: Bridge systems using different romanization standards

## Technical Requirements

### Core Capabilities
1. **Bidirectional conversion**: Pinyin ↔ Zhuyin ↔ IPA
2. **Format detection**: Auto-identify source format
3. **Format validation**: Verify input is valid romanization
4. **Batch processing**: Handle large volumes efficiently
5. **Preserve spacing/formatting**: Maintain original text structure
6. **Error handling**: Gracefully handle invalid input

### Performance Constraints
- **Throughput**: Process documents/corpora efficiently (batch mode)
- **Accuracy**: Must be lossless (no information lost in conversion)
- **Automation**: Minimal manual intervention for large datasets

### Accuracy Requirements
- **Critical**: Exact conversion (e.g., 'nǐ' ↔ 'ㄋㄧˇ' must be 100% accurate)
- **Important**: Handle edge cases (punctuation, numbers, mixed text)
- **Critical**: Preserve tone information exactly

## Library Analysis

### pypinyin Assessment
**Strengths for Transcription Tools**:
- ✅ Character → Pinyin/Zhuyin conversion
- ✅ Multiple Pinyin formats (accented, numbered)
- ✅ Batch processing capable

**Weaknesses for Transcription Tools**:
- ❌ **NO Pinyin → Zhuyin direct conversion** (must go through characters)
- ❌ NO Zhuyin → Pinyin conversion
- ❌ NO format detection
- ❌ NO format validation
- ❌ Can't process text that's already romanized

**Verdict**: **Poor fit**. pypinyin works with Chinese characters, not romanized text. Wrong direction for transcription conversion tools.

### dragonmapper Assessment
**Strengths for Transcription Tools**:
- ✅ **Direct Pinyin ↔ Zhuyin conversion** (no Chinese text needed)
- ✅ **Format detection** (`identify()`)
- ✅ **Format validation** (`is_pinyin()`, `is_zhuyin()`, `is_ipa()`)
- ✅ **Bidirectional support** (all conversions work both ways)
- ✅ **IPA support** (unique capability)
- ✅ **Preserves formatting** (punctuation, spacing)

**Weaknesses for Transcription Tools**:
- ⚠️ Syllable-level validation (not full text robustness)
- ⚠️ Limited to transcription conversion (doesn't involve characters)

**Verdict**: **Purpose-built for this use case**. dragonmapper is designed exactly for transcription conversion tasks.

## Detailed Feature Comparison for Transcription

| Feature | pypinyin | dragonmapper | Transcription Value |
|---------|----------|--------------|---------------------|
| **Pinyin → Zhuyin** | ❌ (indirect) | ✅ Direct | Critical |
| **Zhuyin → Pinyin** | ❌ | ✅ Direct | Critical |
| **IPA ↔ Pinyin** | ❌ | ✅ | High (linguistics) |
| **IPA ↔ Zhuyin** | ❌ | ✅ | High (linguistics) |
| **Format detection** | ❌ | ✅ | Critical (automation) |
| **Format validation** | ❌ | ✅ | High (error handling) |
| **Works with romanized text** | ❌ | ✅ | Critical |
| **Tone conversion** | N/A | ✅ (numbered ↔ accented) | High |

## Recommendation

### Primary Recommendation: **dragonmapper**
dragonmapper is THE tool for transcription conversion. It's designed specifically for this use case and provides all necessary capabilities.

### When pypinyin is Relevant:
Only if you need to convert **from Chinese characters** as a source:
- Source is Chinese text (not romanization)
- Need to generate initial romanization before converting formats

### Typical Workflow:
```python
# If source is Chinese:
Chinese text → pypinyin → Pinyin → dragonmapper → Zhuyin

# If source is already romanized:
Pinyin → dragonmapper → Zhuyin (pypinyin not needed)
```

## Implementation Patterns

### Pattern 1: Automatic Format Detection & Conversion
Build a universal converter that detects and converts any format:

```python
from dragonmapper import transcriptions

def universal_convert(text, target_format='Pinyin'):
    """Automatically detect source format and convert to target"""
    # Detect source format
    source_format = transcriptions.identify(text)

    if source_format == 'Unknown':
        raise ValueError(f"Cannot identify format: {text}")

    # Convert to target
    if source_format == target_format:
        return text  # Already in target format

    # Pinyin → Zhuyin
    if source_format == 'Pinyin' and target_format == 'Zhuyin':
        return transcriptions.pinyin_to_zhuyin(text)

    # Zhuyin → Pinyin
    elif source_format == 'Zhuyin' and target_format == 'Pinyin':
        return transcriptions.zhuyin_to_pinyin(text)

    # Pinyin → IPA
    elif source_format == 'Pinyin' and target_format == 'IPA':
        return transcriptions.pinyin_to_ipa(text)

    # IPA → Pinyin
    elif source_format == 'IPA' and target_format == 'Pinyin':
        return transcriptions.ipa_to_pinyin(text)

    # Add more combinations as needed
    else:
        raise ValueError(f"Conversion {source_format} → {target_format} not supported")

# Usage
input_text = "Wǒ shì yīgè měiguórén."  # Pinyin
output = universal_convert(input_text, target_format='Zhuyin')
# Result: "ㄨㄛˇ ㄕˋ ㄧ ㄍㄜˋ ㄇㄟˇ ㄍㄨㄛˊ ㄖㄣˊ."
```

### Pattern 2: Batch Document Conversion
Convert entire documents between formats:

```python
from dragonmapper import transcriptions
import re

def convert_document(content, source_format, target_format):
    """Convert document preserving non-romanized content"""
    # Split into sentences or paragraphs
    segments = content.split('\n')

    converted = []
    for segment in segments:
        # Detect if segment contains romanization
        if transcriptions.identify(segment) == source_format:
            # Convert romanization
            if source_format == 'Pinyin' and target_format == 'Zhuyin':
                converted_segment = transcriptions.pinyin_to_zhuyin(segment)
            elif source_format == 'Zhuyin' and target_format == 'Pinyin':
                converted_segment = transcriptions.zhuyin_to_pinyin(segment)
            else:
                converted_segment = segment  # Unsupported conversion

            converted.append(converted_segment)
        else:
            # Keep non-romanized content as-is
            converted.append(segment)

    return '\n'.join(converted)

# Example: Convert Pinyin document to Zhuyin
pinyin_doc = """
Title: Chinese Language Guide
Nǐ hǎo. Wǒ jiào Lǐ Míng.
"""

zhuyin_doc = convert_document(pinyin_doc, 'Pinyin', 'Zhuyin')
```

### Pattern 3: Data Cleaning & Validation
Validate and standardize mixed-format datasets:

```python
from dragonmapper import transcriptions

def validate_and_standardize(entries, target_format='Pinyin'):
    """Process dataset with mixed romanization formats"""
    results = {
        'valid': [],
        'invalid': [],
        'converted': []
    }

    for entry in entries:
        # Detect format
        detected = transcriptions.identify(entry)

        if detected == 'Unknown':
            results['invalid'].append(entry)
            continue

        # Validate
        if detected == 'Pinyin' and transcriptions.is_pinyin(entry):
            valid = True
        elif detected == 'Zhuyin' and transcriptions.is_zhuyin(entry):
            valid = True
        else:
            valid = False

        if not valid:
            results['invalid'].append(entry)
            continue

        # Convert to target format
        if detected == target_format:
            results['valid'].append(entry)
        else:
            # Convert
            if detected == 'Pinyin' and target_format == 'Zhuyin':
                converted = transcriptions.pinyin_to_zhuyin(entry)
            elif detected == 'Zhuyin' and target_format == 'Pinyin':
                converted = transcriptions.zhuyin_to_pinyin(entry)
            else:
                converted = entry  # Can't convert

            results['converted'].append({
                'original': entry,
                'converted': converted,
                'source_format': detected
            })

    return results

# Usage: Clean mixed dataset
mixed_data = ['Wǒ hǎo', 'ㄋㄧˇ ㄏㄠˇ', 'invalid_text', 'zhōngwén']
cleaned = validate_and_standardize(mixed_data, target_format='Pinyin')
```

### Pattern 4: Tone Format Conversion
Convert between tone notation styles within Pinyin:

```python
from dragonmapper import transcriptions

def convert_tone_format(pinyin_text, output_format='accented'):
    """Convert between accented Pinyin and numbered Pinyin"""
    # Split into syllables
    syllables = pinyin_text.split()

    converted_syllables = []
    for syllable in syllables:
        if output_format == 'numbered':
            # Accented → numbered
            converted = transcriptions.accented_syllable_to_numbered(syllable)
        elif output_format == 'accented':
            # Numbered → accented
            converted = transcriptions.numbered_syllable_to_accented(syllable)
        else:
            converted = syllable

        converted_syllables.append(converted)

    return ' '.join(converted_syllables)

# Usage
accented = "Wǒ shì Lǐ Míng"
numbered = convert_tone_format(accented, output_format='numbered')
# Result: "Wo3 shi4 Li3 Ming2"

back_to_accented = convert_tone_format(numbered, output_format='accented')
# Result: "Wǒ shì Lǐ Míng"
```

### Pattern 5: Academic Publishing Workflow
Convert research papers between romanization standards:

```python
from dragonmapper import transcriptions

class AcademicDocumentConverter:
    """Convert academic documents between romanization formats"""

    def __init__(self, source_format='Pinyin', target_format='Zhuyin'):
        self.source_format = source_format
        self.target_format = target_format

    def convert_paper(self, paper_text):
        """Convert entire paper preserving citations and formatting"""
        # Process line by line to preserve structure
        lines = paper_text.split('\n')
        converted_lines = []

        for line in lines:
            # Skip empty lines
            if not line.strip():
                converted_lines.append(line)
                continue

            # Check if line contains romanization
            detected = transcriptions.identify(line)

            if detected == self.source_format:
                # Convert the line
                converted_line = self._convert_line(line)
                converted_lines.append(converted_line)
            else:
                # Keep as-is (English, Chinese, or other)
                converted_lines.append(line)

        return '\n'.join(converted_lines)

    def _convert_line(self, line):
        """Convert a single line"""
        if self.source_format == 'Pinyin' and self.target_format == 'Zhuyin':
            return transcriptions.pinyin_to_zhuyin(line)
        elif self.source_format == 'Zhuyin' and self.target_format == 'Pinyin':
            return transcriptions.zhuyin_to_pinyin(line)
        return line

# Usage
converter = AcademicDocumentConverter(source_format='Pinyin', target_format='Zhuyin')
paper = """
Abstract
This paper discusses Mandarin phonology. The word "nǐ hǎo" means hello.

Introduction
...
"""
converted_paper = converter.convert_paper(paper)
```

## Trade-offs

### Accuracy vs Automation
**Trade-off**: Automatic format detection vs manual specification

**Automatic (dragonmapper.identify)**:
- ✅ Convenient for mixed-format data
- ✅ Reduces manual work
- ⚠️ May misidentify edge cases

**Manual specification**:
- ✅ Always correct
- ✅ Better for uniform datasets
- ❌ More tedious for mixed data

**Recommendation**: Use automatic detection for exploratory work, manual for production pipelines.

### Validation Strictness
**Trade-off**: Strict validation (reject errors) vs lenient (best-effort conversion)

**Strict validation**:
```python
if not transcriptions.is_pinyin(input_text):
    raise ValueError("Invalid Pinyin")
```
- ✅ Ensures data quality
- ❌ Requires manual cleanup of errors

**Lenient conversion**:
```python
try:
    result = transcriptions.pinyin_to_zhuyin(input_text)
except:
    result = input_text  # Keep original if conversion fails
```
- ✅ Handles messy data
- ❌ May produce incorrect results

**Recommendation**: Use strict validation for critical applications (academic publishing), lenient for exploratory data analysis.

## Performance Considerations

### Batch Processing Performance
dragonmapper is fast for transcription conversion:
- **Typical throughput**: Thousands of syllables per second
- **Bottleneck**: Usually I/O (reading/writing files), not conversion

### Optimization Tips
```python
# Process files in parallel for large corpora
from concurrent.futures import ProcessPoolExecutor
from dragonmapper import transcriptions

def convert_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    converted = transcriptions.pinyin_to_zhuyin(content)

    output_filename = filename.replace('.txt', '_zhuyin.txt')
    with open(output_filename, 'w', encoding='utf-8') as f:
        f.write(converted)

# Parallel processing
files = ['doc1.txt', 'doc2.txt', 'doc3.txt', ...]
with ProcessPoolExecutor() as executor:
    executor.map(convert_file, files)
```

## Real-World Example: Subtitle Converter

```python
from dragonmapper import transcriptions
import re

class SubtitleConverter:
    """Convert subtitle files between romanization formats"""

    def __init__(self, source_format='Pinyin', target_format='Zhuyin'):
        self.source_format = source_format
        self.target_format = target_format

    def convert_srt(self, srt_content):
        """Convert SRT subtitle file"""
        # SRT format:
        # 1
        # 00:00:01,000 --> 00:00:03,000
        # Nǐ hǎo

        lines = srt_content.split('\n')
        converted_lines = []

        for line in lines:
            # Skip timestamp lines and sequence numbers
            if '-->' in line or line.strip().isdigit():
                converted_lines.append(line)
                continue

            # Skip empty lines
            if not line.strip():
                converted_lines.append(line)
                continue

            # Convert subtitle text
            detected = transcriptions.identify(line)
            if detected == self.source_format:
                converted_line = self._convert_text(line)
                converted_lines.append(converted_line)
            else:
                converted_lines.append(line)

        return '\n'.join(converted_lines)

    def _convert_text(self, text):
        if self.source_format == 'Pinyin' and self.target_format == 'Zhuyin':
            return transcriptions.pinyin_to_zhuyin(text)
        elif self.source_format == 'Zhuyin' and self.target_format == 'Pinyin':
            return transcriptions.zhuyin_to_pinyin(text)
        return text

# Usage
converter = SubtitleConverter(source_format='Pinyin', target_format='Zhuyin')

srt_content = """1
00:00:01,000 --> 00:00:03,000
Nǐ hǎo, wǒ jiào Lǐ Míng.

2
00:00:03,500 --> 00:00:05,000
Hěn gāoxìng rènshi nǐ.
"""

converted_srt = converter.convert_srt(srt_content)
# Romanization converted, timestamps and structure preserved
```

## Missing Capabilities

Neither library helps with:
- ❌ Character-level conversion within mixed text (romanization + Chinese)
- ❌ Context-aware conversion for heteronyms in romanized text
- ❌ Preserving complex document formatting (Word, PDF)
- ❌ Translation between romanization and Chinese (need separate dictionary)
- ❌ Handling non-standard romanization schemes (Wade-Giles, etc.)

## Conclusion

**dragonmapper is THE tool for transcription conversion.** It's purpose-built for this exact use case and provides all necessary capabilities:
- Direct transcription-to-transcription conversion
- Format detection and validation
- Bidirectional support (including IPA)

pypinyin is irrelevant for this use case unless you're starting from Chinese characters.

### When to Use Both Libraries
Only if your workflow involves:
1. Chinese characters → pypinyin → Pinyin
2. Pinyin → dragonmapper → Zhuyin/IPA

For pure transcription conversion tasks (working with romanized text), dragonmapper alone is sufficient and appropriate.
