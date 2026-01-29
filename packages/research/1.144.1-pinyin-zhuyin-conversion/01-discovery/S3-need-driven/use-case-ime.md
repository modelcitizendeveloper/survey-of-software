# Use Case: IME (Input Method Editor)

## Scenario Description
Users typing Chinese characters using romanization input. As they type "zhong" or "ㄓㄨㄥ", the IME suggests matching Chinese characters or converts between input formats.

## User Persona
- **Primary**: Desktop/mobile users in Chinese-speaking regions
- **Secondary**: Language learners using romanization-based input
- **Platforms**: Windows, macOS, Linux, iOS, Android
- **Volume**: Millions of keystrokes daily for active users

## Technical Requirements

### Core Capabilities
1. **Bidirectional conversion**: Pinyin ↔ Zhuyin ↔ Characters
2. **Real-time processing**: Sub-100ms latency per keystroke
3. **Input validation**: Detect valid vs invalid romanization
4. **Format detection**: Auto-identify if user is typing Pinyin or Zhuyin
5. **Character suggestions**: Given romanization, suggest matching characters

### Performance Constraints
- **Latency**: Must feel instant (< 100ms response time)
- **Memory**: Should run on mobile devices
- **CPU**: Minimal impact on system resources
- **Battery**: Low power consumption on mobile

### Accuracy Requirements
- **Critical**: Correct character suggestions
- **Important**: Proper tone handling
- **Nice-to-have**: Context-aware suggestions (like pypinyin's heteronym handling)

## Library Analysis

### pypinyin Assessment
**Strengths for IME**:
- ✅ Context-aware character suggestions (heteronym handling)
- ✅ Memory optimization options (`PYPINYIN_NO_PHRASES`)
- ✅ Multiple tone input formats supported

**Weaknesses for IME**:
- ❌ Primarily character → Pinyin (reverse of IME workflow)
- ❌ No Pinyin → Character function (IME needs this)
- ❌ No input validation/detection
- ❌ No Pinyin ↔ Zhuyin conversion (users might want to switch)

**Verdict**: **Not ideal for IME**. pypinyin is designed for the opposite direction (characters → romanization).

### dragonmapper Assessment
**Strengths for IME**:
- ✅ Pinyin ↔ Zhuyin conversion (switch input methods)
- ✅ Input validation (`is_pinyin()`, `is_zhuyin()`)
- ✅ Format detection (`identify()`)
- ✅ Fast transcription conversion

**Weaknesses for IME**:
- ❌ No romanization → Character conversion (critical missing feature)
- ❌ Requires separate dictionary for character suggestions

**Verdict**: **Partial fit**. Good for format detection and conversion, but missing core IME feature (romanization → characters).

### Neither Library is Complete for IME
**Gap**: Neither library provides **romanization → Chinese character** conversion, which is the core IME function.

**What IME Actually Needs**:
1. Pinyin/Zhuyin → Character suggestions (NOT provided)
2. Ranking candidates by frequency (NOT provided)
3. Learning user preferences (NOT provided)
4. Context-aware predictions (pypinyin has character → Pinyin context, but not the reverse)

## Realistic IME Architecture

### Required Components
1. **Input processor** (dragonmapper's transcriptions module)
   - Validate and detect input format
   - Convert between Pinyin/Zhuyin if user switches

2. **Character dictionary** (external, e.g., CC-CEDICT)
   - Map romanization → character candidates
   - Rank by frequency

3. **Context engine** (external, e.g., language model)
   - Predict likely character sequences
   - Learn user preferences

4. **Romanization converter** (pypinyin or dragonmapper)
   - Display Pinyin/Zhuyin annotations for candidates

### Code Pattern (Conceptual)
```python
from dragonmapper import transcriptions
import cc_cedict  # Hypothetical dictionary

def handle_ime_input(user_input):
    # Step 1: Detect input format (dragonmapper)
    input_type = transcriptions.identify(user_input)

    if input_type not in ['Pinyin', 'Zhuyin']:
        return []  # Invalid input

    # Step 2: Normalize to Pinyin (dragonmapper)
    if input_type == 'Zhuyin':
        pinyin_query = transcriptions.zhuyin_to_pinyin(user_input)
    else:
        pinyin_query = user_input

    # Step 3: Look up characters (external dictionary)
    candidates = cc_cedict.lookup(pinyin_query)

    # Step 4: Rank and return
    return rank_by_context(candidates)
```

## Where These Libraries Add Value to IME

### dragonmapper's Role
- **Format switching**: User types Pinyin, IME shows Zhuyin preview (or vice versa)
- **Input validation**: Reject invalid romanization early
- **Normalization**: Convert different input formats to canonical form

```python
# Allow users to switch between Pinyin and Zhuyin input
def switch_input_mode(text, current_mode, target_mode):
    if current_mode == 'Pinyin' and target_mode == 'Zhuyin':
        return transcriptions.pinyin_to_zhuyin(text)
    elif current_mode == 'Zhuyin' and target_mode == 'Pinyin':
        return transcriptions.zhuyin_to_pinyin(text)
```

### pypinyin's Role
- **Candidate annotation**: Show Pinyin/Zhuyin for character candidates
- **Verification**: Double-check if suggested character matches input romanization

```python
# Annotate character candidates with romanization
def annotate_candidates(characters):
    return [
        {
            'char': char,
            'pinyin': lazy_pinyin(char),
            'zhuyin': pinyin(char, style=Style.BOPOMOFO)
        }
        for char in characters
    ]
```

## Recommendation

### Primary Recommendation: **Neither library alone**
Neither pypinyin nor dragonmapper provides the core IME functionality (romanization → characters). You need an additional character dictionary.

### Supplementary Libraries
If building an IME, use these libraries for:

1. **dragonmapper** (RECOMMENDED)
   - Input format detection and validation
   - Pinyin ↔ Zhuyin conversion for format switching
   - Input normalization

2. **pypinyin** (OPTIONAL)
   - Annotating character candidates with romanization
   - Verifying character pronunciations

### Also Required (Not Covered by These Libraries)
- Character dictionary (CC-CEDICT, Unihan, or commercial)
- Frequency data for ranking candidates
- Context-aware prediction (language model)
- User preference learning

## Trade-offs

### If You Must Choose One
**Choose dragonmapper** for IME work:
- Input validation is critical for IME
- Format switching is a common feature request
- More aligned with IME workflow (processing romanized input)

### When to Use Both
Use both if your IME needs:
- Rich romanization options for candidate display
- Context-aware pronunciation hints
- Dual Pinyin/Zhuyin modes with seamless switching

## Missing Capabilities

Neither library helps with:
- ❌ Romanization → Character lookup (core IME function)
- ❌ Candidate ranking by frequency
- ❌ Context-aware character prediction
- ❌ User dictionary and learning
- ❌ Phrase/word boundary detection

For a production IME, you need additional components beyond these romanization libraries.

## Real-World Examples

### Existing IMEs
Most popular IMEs (Sogou, Google Pinyin, RIME) use:
- Custom character dictionaries (not pypinyin or dragonmapper)
- Statistical language models for ranking
- Cloud-based updates for new words

These libraries could be used as **supplementary components**, not the core engine.

### Realistic Use Case
A simple IME for language learners or assistive tools:
1. Use dragonmapper for input validation and format switching
2. Use a lightweight dictionary for character lookup
3. Use pypinyin to annotate results for learning

This wouldn't compete with production IMEs but could serve educational or accessibility needs.
