# polib: Deep Technical Analysis (TMX Conversion Context)

## Architecture Overview

### Module Structure

```
polib/
└── polib.py          # Single-file module (~3000 lines)
    ├── POFile        # PO file representation
    ├── MOFile        # MO (compiled) file representation
    ├── POEntry       # Single translation entry
    ├── _POFileParser # PO parser
    └── _MOFileParser # MO parser
```

**Design philosophy**: Pure Python, single-file, zero dependencies

### Core Abstractions

**Main classes**:
```python
class POFile:
    """Represents a PO (Portable Object) file"""
    def __init__(self, *args, **kwargs):
        self.metadata = {}           # Header metadata
        self.metadata_is_fuzzy = False
        self._encoding = 'utf-8'
        self.entries = []            # List of POEntry objects

class POEntry:
    """Represents a single translation entry"""
    def __init__(self, *args, **kwargs):
        self.msgid = ''              # Source text
        self.msgstr = ''             # Target text
        self.msgid_plural = ''       # Plural source (optional)
        self.msgstr_plural = {}      # Plural targets (optional)
        self.msgctxt = None          # Disambiguation context
        self.obsolete = False        # Commented-out entry
        self.encoding = 'utf-8'
        self.flags = []              # e.g., ['fuzzy', 'python-format']
        self.previous_msgid = None   # For fuzzy matching
        self.previous_msgid_plural = None
        self.previous_msgctxt = None
        self.comment = ''            # Translator comment
        self.tcomment = ''           # Automatic comment
        self.occurrences = []        # Source code locations
```

**Key design decisions**:
- List-based storage (not dict)
- Entries ordered as in file
- Metadata stored separately from entries
- Plural forms supported natively
- Context (msgctxt) for disambiguation

## TMX Relationship

### Indirect TMX Support

**polib does NOT parse TMX directly**. TMX support is via:

1. **translate-toolkit conversion**: External tool
2. **PO as intermediate format**: PO ↔ TMX bridge
3. **Programmatic manipulation**: polib for PO, then convert

### Conversion Pipeline Architecture

```
TMX → translate-toolkit (tmx2po) → PO → polib (manipulate) → PO → translate-toolkit (po2tmx) → TMX
```

**Why this matters**:
- TMX data model ≠ PO data model
- Conversion is lossy (some metadata lost)
- Round-trip not always perfect

## PO Format Internals

### File Structure

**Example PO file**:
```po
# Translation file for MyApp
# Copyright (C) 2026
msgid ""
msgstr ""
"Project-Id-Version: MyApp 1.0\n"
"Language: es\n"
"Content-Type: text/plain; charset=UTF-8\n"

#: src/main.py:42
#, fuzzy, python-format
msgid "Hello, {name}!"
msgstr "¡Hola, {name}!"

#: src/main.py:56
msgctxt "greeting"
msgid "Hello"
msgstr "Hola"

#: src/main.py:60
msgid "One item"
msgid_plural "{count} items"
msgstr[0] "Un elemento"
msgstr[1] "{count} elementos"
```

**Key components**:
- **Header entry**: Empty msgid, metadata in msgstr
- **Comments**: `#` (translator), `#.` (extracted), `#:` (location), `#,` (flags)
- **Context**: `msgctxt` for disambiguation
- **Plural forms**: `msgid_plural`, `msgstr[n]`
- **Flags**: `fuzzy`, `python-format`, `c-format`, etc.

### Internal Representation

**POEntry object for simple entry**:
```python
entry = POEntry(
    msgid='Hello',
    msgstr='Hola',
    occurrences=[('src/main.py', 42)],
    flags=['python-format'],
    comment='Greeting message',
)
```

**POEntry for plural entry**:
```python
entry = POEntry(
    msgid='One item',
    msgid_plural='{count} items',
    msgstr_plural={
        0: 'Un elemento',
        1: '{count} elementos',
    },
)
```

**Memory layout**:
- `POEntry` object: ~500 bytes (Python object overhead)
- Strings (msgid, msgstr): string length × 2
- Lists (flags, occurrences): ~100 bytes + items
- **Total**: ~1 KB per entry (typical)

### Metadata Handling

**Metadata storage** (in header entry):
```python
po = POFile()
po.metadata = {
    'Project-Id-Version': 'MyApp 1.0',
    'Language': 'es',
    'Content-Type': 'text/plain; charset=UTF-8',
    'Content-Transfer-Encoding': '8bit',
    'Plural-Forms': 'nplurals=2; plural=(n != 1);',
}
```

**Serialized as**:
```po
msgid ""
msgstr ""
"Project-Id-Version: MyApp 1.0\n"
"Language: es\n"
"Content-Type: text/plain; charset=UTF-8\n"
...
```

## TMX Conversion Mechanisms

### TMX → PO (via translate-toolkit)

**Conversion process**:
```bash
tmx2po -i memory.tmx -o output.po
```

**Internal steps** (in translate-toolkit):
```python
# Simplified from translate-toolkit tmx2po
from translate.storage import tmx, po

tmx_store = tmx.tmxfile()
tmx_store.parsefile('memory.tmx')

po_store = po.pofile()
po_store.encoding = 'UTF-8'

# Map TMX source/target to PO msgid/msgstr
for tmx_unit in tmx_store.units:
    po_unit = po_store.addsourceunit(tmx_unit.source)
    po_unit.target = tmx_unit.target
    # TMX notes → PO comments
    if tmx_unit.notes:
        po_unit.addnote(tmx_unit.notes)

po_store.save('output.po')
```

**Data mapping**:
```
TMX                     →  PO
<tu>                    →  POEntry
<tuv xml:lang="en">     →  msgid (source)
<tuv xml:lang="es">     →  msgstr (target)
<note>                  →  comment (translator comment)
<prop type="x-context"> →  msgctxt (if present)
tuid attribute          →  (lost - PO has no equivalent)
```

**Lossy conversion**:
- **Lost from TMX**: `tuid`, `<prop>` (most types), creation dates, inline markup structure
- **Retained**: Source/target text, notes (as comments), basic metadata
- **Not preserved**: Inline tags (`<bpt>`, `<ept>`) converted to plain text or escaped

### PO → TMX (via translate-toolkit)

**Conversion process**:
```bash
po2tmx -i translations.po -o memory.tmx
```

**Internal steps** (in translate-toolkit):
```python
# Simplified from translate-toolkit po2tmx
from translate.storage import po, tmx

po_store = po.pofile.parsefile('translations.po')

tmx_store = tmx.tmxfile()
# Language detection from PO metadata
tmx_store.setsourcelanguage(po_store.sourceLanguage)
tmx_store.settargetlanguage(po_store.targetlanguage)

# Map PO msgid/msgstr to TMX source/target
for po_unit in po_store.units:
    if po_unit.istranslated() and not po_unit.isobsolete():
        tmx_unit = tmx_store.addsourceunit(po_unit.source)
        tmx_unit.target = po_unit.target
        # PO comments → TMX notes
        if po_unit.getnotes():
            tmx_unit.addnote(po_unit.getnotes())

tmx_store.save('memory.tmx')
```

**Data mapping**:
```
PO                      →  TMX
POEntry                 →  <tu>
msgid                   →  <tuv xml:lang="source">
msgstr                  →  <tuv xml:lang="target">
comment                 →  <note>
msgctxt                 →  <prop type="x-context">
flags                   →  (lost - no TMX equivalent)
occurrences             →  (lost - no TMX equivalent)
```

**Lossy conversion**:
- **Lost from PO**: `flags`, `occurrences`, `previous_msgid`, obsolete status
- **Retained**: Source/target text, comments (as notes), context (if used)
- **Not supported**: Plural forms (PO plurals don't map cleanly to TMX)

### Round-Trip Integrity

**PO → TMX → PO** losses:
```python
# Original PO
entry = POEntry(
    msgid='Hello',
    msgstr='Hola',
    flags=['fuzzy', 'python-format'],
    occurrences=[('src/main.py', 42)],
    comment='Greeting',
)

# After PO → TMX → PO
# Flags: LOST
# Occurrences: LOST
# Comment: RETAINED (as TMX <note>)
```

**TMX → PO → TMX** losses:
```xml
<!-- Original TMX -->
<tu tuid="123" datatype="plaintext">
  <prop type="x-domain">software</prop>
  <tuv xml:lang="en"><seg>Hello</seg></tuv>
  <tuv xml:lang="es"><seg>Hola</seg></tuv>
</tu>

<!-- After TMX → PO → TMX -->
<!-- tuid: LOST -->
<!-- <prop>: LOST (unless x-context) -->
<!-- Source/target: RETAINED -->
```

**Recommendation**: Don't use PO as intermediate format if TMX fidelity is critical

## polib API Patterns

### Reading PO Files

```python
import polib

# Load from file
po = polib.pofile('translations.po')

# Load from string
content = open('file.po').read()
po = polib.pofile(content)

# Access entries
for entry in po:
    print(f"{entry.msgid} -> {entry.msgstr}")

# Filter entries
translated = po.translated_entries()
fuzzy = po.fuzzy_entries()
untranslated = po.untranslated_entries()
```

### Writing PO Files

```python
import polib

# Create new PO file
po = polib.POFile()
po.metadata = {
    'Project-Id-Version': '1.0',
    'Language': 'es',
    'Content-Type': 'text/plain; charset=UTF-8',
}

# Add entry
entry = polib.POEntry(
    msgid='Hello',
    msgstr='Hola',
    occurrences=[('main.py', 10)],
)
po.append(entry)

# Save to file
po.save('output.po')

# Save as MO (compiled)
po.save_as_mofile('output.mo')
```

### Modifying PO Files

```python
import polib

po = polib.pofile('app.po')

# Update translations
for entry in po:
    if entry.fuzzy:
        # Review and unfuzzy
        entry.flags.remove('fuzzy')
        entry.msgstr = review_translation(entry.msgstr)

# Merge with another PO file
updates = polib.pofile('updates.po')
po.merge(updates)

# Save changes
po.save()
```

### TMX Workflow with polib

**Complete workflow**:
```python
import polib
import subprocess

# Step 1: Convert TMX to PO (via translate-toolkit)
subprocess.run(['tmx2po', '-i', 'memory.tmx', '-o', 'temp.po'])

# Step 2: Load with polib
po = polib.pofile('temp.po')

# Step 3: Manipulate with polib
for entry in po:
    # Custom processing
    if needs_update(entry):
        entry.msgstr = update_translation(entry.msgstr)

# Step 4: Save modified PO
po.save('updated.po')

# Step 5: Convert back to TMX (via translate-toolkit)
subprocess.run(['po2tmx', '-i', 'updated.po', '-o', 'updated.tmx'])
```

## PO Format Parsing Implementation

### Parser Architecture

**Internal parser** (`_POFileParser` class):
```python
class _POFileParser:
    def __init__(self, pofile, **kwargs):
        self.pofile = pofile
        self.transitions = {}  # State machine
        self.current_entry = None
        self.current_state = 'ST'  # Start state

    def parse(self, input):
        # Line-by-line state machine parser
        for linenum, line in enumerate(input.split('\n')):
            self.process_line(line, linenum)
        return self.pofile
```

**State machine** (simplified):
```
States:
- ST: Start (waiting for entry)
- TC: Translator comment (#)
- GC: Generated comment (#.)
- OC: Occurrence (#:)
- FL: Flags (#,)
- CT: Context (msgctxt)
- ID: Message ID (msgid)
- IP: ID Plural (msgid_plural)
- MP: Message Plural (msgstr[n])
- MS: Message String (msgstr)

Transitions:
- # → TC (translator comment)
- #. → GC (generated comment)
- #: → OC (occurrence)
- #, → FL (flags)
- msgctxt → CT
- msgid → ID
- msgstr → MS
```

**Example parsing**:
```po
#: main.py:42
#, fuzzy
msgid "Hello"
msgstr "Hola"
```

**Parser steps**:
1. Line 1: `#: main.py:42` → State OC, store occurrence
2. Line 2: `#, fuzzy` → State FL, add flag
3. Line 3: `msgid "Hello"` → State ID, store msgid
4. Line 4: `msgstr "Hola"` → State MS, store msgstr, finalize entry

### Encoding Handling

**Auto-detection**:
```python
def detect_encoding(filename):
    # Check BOM
    with open(filename, 'rb') as f:
        bom = f.read(4)
        if bom[:3] == b'\xef\xbb\xbf':
            return 'utf-8-sig'
        if bom[:2] == b'\xff\xfe':
            return 'utf-16-le'
    # Parse Content-Type from metadata
    # Default: utf-8
    return 'utf-8'
```

**Encoding issues**:
- Invalid UTF-8: Falls back to Latin-1 (lenient)
- No strict mode (always attempts to parse)

### Malformed PO Handling

**Error recovery**:
- Syntax errors: Logged, entry skipped, parsing continues
- Missing msgstr: Creates entry with empty msgstr
- Unclosed strings: Best-effort recovery, may corrupt entry

**Example**:
```po
msgid "Unclosed string
msgstr "Valid"
```

**Behavior**: Parser may corrupt next entry or crash
- No strict validation mode
- Assumes well-formed input

## Performance Characteristics

### Parsing Performance

**Bottleneck**: Line-by-line state machine (pure Python)

**Estimated performance** (i7 CPU, 16 GB RAM):
- 10K entries, 1 MB file: ~0.5 seconds
- 100K entries, 10 MB file: ~5 seconds
- 1M entries, 100 MB file: ~50 seconds

**Comparison**:
- polib: ~0.5 seconds (10K entries)
- translate-toolkit (lxml): ~0.3 seconds (10K entries)
- **Trade-off**: Slower but zero dependencies

### Memory Usage

**Per entry overhead**:
- `POEntry` object: ~500 bytes
- Strings (msgid, msgstr): text length × 2
- Lists (flags, occurrences): ~100 bytes
- **Total**: ~1 KB per entry

**File vs memory**:
- 10 MB PO file: ~20-30 MB RAM (2-3x overhead)
- Lower than translate-toolkit TMX (3-5x overhead)

### Serialization Performance

**Bottleneck**: String concatenation (pure Python)

**Estimated**:
- 10K entries: ~0.3 seconds
- 100K entries: ~3 seconds

**Optimization**: Uses `str.join()` internally (efficient)

### Concurrent Access

**Thread safety**: NOT THREAD-SAFE

**Safe patterns**:
- Read-only: SAFE (after parsing complete)
- Concurrent modifications: UNSAFE (shared mutable state)
- Multi-process: SAFE (separate POFile instances)

### Scalability

**Practical limits** (16 GB RAM):
- 1M+ entries feasible
- 100+ MB PO files supported
- No hard limit (list-based storage)

**Comparison to TMX**:
- PO files smaller than equivalent TMX (less XML overhead)
- Faster to parse (simpler format)

## Extension Points

### Subclassing POFile

```python
import polib

class MyPOFile(polib.POFile):
    def save(self, fpath=None):
        # Custom pre-save validation
        self.validate()
        super().save(fpath)

    def validate(self):
        for entry in self:
            if not entry.msgstr and not entry.fuzzy:
                raise ValueError(f"Untranslated: {entry.msgid}")
```

### Custom Entry Processing

```python
class ValidatedPOEntry(polib.POEntry):
    def __setattr__(self, name, value):
        # Custom validation on assignment
        if name == 'msgstr' and '{' in self.msgid and '{' not in value:
            raise ValueError("Placeholder missing in translation")
        super().__setattr__(name, value)
```

### Custom Metadata Handling

```python
po = polib.POFile()

# Add custom metadata
po.metadata['X-Generator'] = 'MyTool 1.0'
po.metadata['X-Domain'] = 'software'

# Custom metadata preserved on save
po.save('output.po')
```

## Dependencies

### Required

- **Python**: 2.7, 3.6-3.11, PyPy
- **No external dependencies**: Pure Python stdlib only

**Installation**:
```bash
pip install polib
# No dependencies installed
```

### For TMX Workflow

- **translate-toolkit**: Required for PO ↔ TMX conversion
  - Brings lxml dependency
  - GPL-2.0+ license

**Installation**:
```bash
pip install polib translate-toolkit
# Now have: polib (MIT) + translate-toolkit (GPL) + lxml
```

## Edge Cases

### Plural Forms Complexity

**PO plural handling**:
```po
msgid "One item"
msgid_plural "{count} items"
msgstr[0] "Un elemento"
msgstr[1] "{count} elementos"
```

**No TMX equivalent**:
- TMX has one source, one target per `<tu>`
- Plurals require multiple `<tu>` elements
- Conversion: Splits into separate entries or loses plural info

### Context Disambiguation

**PO context**:
```po
msgctxt "button"
msgid "Save"
msgstr "Guardar"

msgctxt "menu"
msgid "Save"
msgstr "Guardar"
```

**TMX conversion**:
- Context stored in `<prop type="x-context">`
- Not all TMX tools recognize this property
- May lose disambiguation on import to CAT tools

### Fuzzy Flag Handling

**PO fuzzy flag**:
```po
#, fuzzy
msgid "Hello"
msgstr "Hola"
```

**TMX conversion**:
- No TMX equivalent for fuzzy status
- Flag lost on PO → TMX conversion
- Translation treated as confirmed in TMX

### Obsolete Entries

**PO obsolete entries** (commented out):
```po
#~ msgid "Old text"
#~ msgstr "Texto antiguo"
```

**TMX conversion**:
- Obsolete entries typically excluded from TMX export
- Manual inclusion requires custom conversion script

## polib + translate-toolkit Integration Patterns

### Pattern 1: PO-Centric Workflow

**Use case**: PO as source of truth, TMX for distribution

```python
import polib
import subprocess

# Maintain translations in PO (version control friendly)
po = polib.pofile('app.po')

# Update translations
for entry in po:
    # Custom logic
    pass

po.save('app.po')

# Export to TMX for CAT tools
subprocess.run(['po2tmx', '-i', 'app.po', '-o', 'dist/memory.tmx'])
```

### Pattern 2: TMX Import to PO Workflow

**Use case**: Receive TMX from translator, merge into PO

```python
import polib
import subprocess
import tempfile

# Convert TMX to temporary PO
with tempfile.NamedTemporaryFile(suffix='.po', delete=False) as tmp:
    subprocess.run(['tmx2po', '-i', 'from_translator.tmx', '-o', tmp.name])
    imported_po = polib.pofile(tmp.name)

# Merge into existing PO
existing_po = polib.pofile('app.po')
existing_po.merge(imported_po)
existing_po.save()
```

### Pattern 3: Batch PO to TMX Conversion

**Use case**: Combine multiple PO files into single TMX

```python
import polib
import subprocess
import tempfile
import os

# Collect all PO files
po_files = ['locale/es.po', 'locale/fr.po', 'locale/de.po']

# Merge into single PO (temporary)
merged_po = polib.POFile()
for po_file in po_files:
    po = polib.pofile(po_file)
    merged_po.merge(po)

# Save merged PO
with tempfile.NamedTemporaryFile(suffix='.po', delete=False) as tmp:
    merged_po.save(tmp.name)
    # Convert to TMX
    subprocess.run(['po2tmx', '-i', tmp.name, '-o', 'combined.tmx'])
    os.unlink(tmp.name)
```

## Technical Limitations

### Hard Constraints

1. **No native TMX support**: Requires external tool (translate-toolkit)
2. **No streaming API**: Entire file loaded into memory
3. **PO/POT/MO only**: Cannot parse XLIFF, TBX, or other formats
4. **No incremental save**: Must write entire file on save

### Design Trade-offs

**Pure Python** (pro/con):
- Pro: Zero dependencies, works everywhere
- Pro: Easy to install, debug, understand
- Con: Slower than C-compiled parsers (lxml)

**List-based storage** (pro/con):
- Pro: Preserves entry order
- Pro: Simple, predictable
- Con: O(n) search, no indexing

**Lenient parsing** (pro/con):
- Pro: Accepts messy real-world files
- Con: May silently corrupt data on malformed input

## Comparison to Direct TMX Libraries

| Aspect | polib (indirect TMX) | translate-toolkit (TMX) | hypomnema (TMX) |
|--------|---------------------|-------------------------|-----------------|
| **TMX native** | No (via conversion) | Yes (Level 1) | Yes (Level 2) |
| **Dependencies** | None | lxml | Optional lxml |
| **Performance** | Fast (simple format) | Medium (lxml DOM) | Fast (dataclasses) |
| **Memory/entry** | ~1 KB | ~2-4 KB | ~1.5 KB |
| **Streaming** | No | No | Yes |
| **License** | MIT | GPL-2.0+ | MIT |
| **Python** | 2.7-3.11 | ≥3.11 | ≥3.12 |
| **Maturity** | Stable | Stable | Pre-1.0 |

## When polib is Relevant to TMX

**Scenarios**:
1. **PO-first workflow**: PO files in version control, export to TMX
2. **CAT tool integration**: Import TMX, convert to PO for developers
3. **Framework integration**: Django/Flask i18n with TMX export
4. **Git-friendly TM**: PO diffs readable, TMX diffs not
5. **Offline processing**: No internet, no lxml compilation (pure Python)

**Not relevant**:
1. **TMX-only workflow**: No PO files involved
2. **CAT tool to CAT tool**: Direct TMX exchange
3. **Level 2 inline markup**: PO cannot represent structured inline tags

## Technical Risk Assessment

### Stability Risks

- **Mature codebase**: LOW (stable since 2010)
- **Infrequent updates**: LOW (feature-complete)
- **Breaking changes**: VERY LOW (stable API)

### Performance Risks

- **Large files**: LOW (efficient for PO format)
- **Conversion overhead**: MEDIUM (external tool dependency)
- **Concurrent access**: MEDIUM (not thread-safe)

### Compatibility Risks

- **Python version**: LOW (broad support 2.7-3.11)
- **Platform**: VERY LOW (pure Python, no compilation)
- **TMX fidelity**: HIGH (lossy conversion, metadata loss)

### Maintenance Risks

- **Community**: LOW (widely used, e.g., Weblate)
- **Commercial support**: MEDIUM (no official backing)
- **Dependency**: VERY LOW (zero dependencies)

## Summary of Technical Characteristics

| Aspect | Details |
|--------|---------|
| **Architecture** | Single-file, state machine parser, list-based storage |
| **Memory Model** | In-memory, ~2-3x file size overhead |
| **TMX Support** | Indirect (via translate-toolkit conversion) |
| **Validation** | Minimal (lenient, error recovery) |
| **Extensibility** | Subclassing POFile/POEntry |
| **Thread Safety** | Not thread-safe for writes |
| **Scalability** | Good (1M+ entries feasible) |
| **Error Handling** | Lenient (attempts recovery) |
| **Dependencies** | None (pure Python) |
| **API Style** | Object-oriented, list-based |
| **Type Safety** | None (no type hints) |

This analysis provides the technical foundation for understanding how polib works internally, its performance characteristics, and how it fits into TMX workflows as an indirect (conversion-based) solution via the PO format bridge.
