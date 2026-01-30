# Programmatic TMX Handling

## Python Libraries for TMX

### 1. PythonTmx (Recommended)

**Installation:**
```bash
pip install pythontmx
```

**Features:**
- Fully typed with type hints
- TMX 1.4 Level 2 compliant (supports all elements and attributes)
- Built on lxml for performance

**Reading TMX:**
```python
from pythontmx import TmxFile

# Load TMX file
tmx = TmxFile.read("translation-memory.tmx")

# Iterate through translation units
for tu in tmx.body.translation_units:
    # Get source segment
    source_lang = tmx.header.source_lang
    source_seg = tu.get_variant(source_lang).segment

    # Get target segment
    target_seg = tu.get_variant("fr-FR").segment

    print(f"{source_seg} -> {target_seg}")
```

**Creating TMX:**
```python
from pythontmx import TmxFile, TranslationUnit, TranslationUnitVariant

# Create new TMX
tmx = TmxFile(source_lang="en-US")

# Add translation unit
tu = TranslationUnit()
tu.add_variant(TranslationUnitVariant(lang="en-US", segment="Hello"))
tu.add_variant(TranslationUnitVariant(lang="fr-FR", segment="Bonjour"))

tmx.body.add_translation_unit(tu)

# Write to file
tmx.write("output.tmx")
```

**Source:** [PythonTmx Documentation](https://python-tmx.readthedocs.io/en/stable/)

### 2. python-tmx (Alternative)

**Installation:**
```bash
pip install python-tmx
```

**Features:**
- Strictly typed, policy-driven parser
- Handles messy translation memories without crashing
- Configurable deserialization policy
- Lxml backend (fast) or standard backend (portable)

**Use Case:** Robust parsing of potentially malformed TMX files from various sources

**Source:** [python-tmx on PyPI](https://pypi.org/project/python-tmx/)

### 3. Direct lxml Usage

For simple needs, use lxml directly:

```python
from lxml import etree

# Parse TMX
tree = etree.parse("memory.tmx")
root = tree.getroot()

# Find all translation units
for tu in root.findall('.//{http://www.lisa.org/tmx14}tu'):
    # Get translation unit variants
    tuvs = tu.findall('.//{http://www.lisa.org/tmx14}tuv')

    # Extract segments
    for tuv in tuvs:
        lang = tuv.get('{http://www.w3.org/XML/1998/namespace}lang')
        seg = tuv.find('.//{http://www.lisa.org/tmx14}seg')
        print(f"{lang}: {seg.text}")
```

**Source:** [Medium: Converting TMX Files to Excel using Python](https://medium.com/@said.surucu/step-by-step-guide-to-converting-tmx-files-to-excel-using-python-c4dc72ef0875)

## Common Operations

### Converting TMX to Excel/CSV

```python
import pandas as pd
from pythontmx import TmxFile

tmx = TmxFile.read("memory.tmx")
data = []

for tu in tmx.body.translation_units:
    source = tu.get_variant("en-US").segment
    target = tu.get_variant("fr-FR").segment
    data.append({"Source": source, "Target": target})

df = pd.DataFrame(data)
df.to_excel("memory.xlsx", index=False)
```

### Deduplicating TMX

```python
from pythontmx import TmxFile

tmx = TmxFile.read("memory.tmx")
seen = set()
deduplicated = TmxFile(source_lang=tmx.header.source_lang)

for tu in tmx.body.translation_units:
    source_seg = tu.get_variant(tmx.header.source_lang).segment

    # Create fingerprint
    fingerprint = (source_seg, tuple((v.lang, v.segment) for v in tu.variants))

    if fingerprint not in seen:
        seen.add(fingerprint)
        deduplicated.body.add_translation_unit(tu)

deduplicated.write("deduplicated.tmx")
```

**Source:** [Medium: Optimizing TMX Files - Python Script to Remove Duplicates](https://medium.com/@said.surucu/optimizing-tmx-files-a-python-script-to-remove-duplicates-363eb46bce8a)

### Merging Multiple TMX Files

```python
from pythontmx import TmxFile

# Load primary TM
merged = TmxFile.read("primary.tmx")

# Load additional TMs
for tmx_path in ["secondary.tmx", "tertiary.tmx"]:
    tmx = TmxFile.read(tmx_path)

    for tu in tmx.body.translation_units:
        merged.body.add_translation_unit(tu)

# Deduplicate and save
# (use deduplication code from above)
merged.write("merged.tmx")
```

### Filtering by Date

```python
from datetime import datetime
from pythontmx import TmxFile

tmx = TmxFile.read("memory.tmx")
filtered = TmxFile(source_lang=tmx.header.source_lang)

cutoff_date = datetime(2025, 1, 1)

for tu in tmx.body.translation_units:
    # Check creation date
    if tu.creation_date and tu.creation_date > cutoff_date:
        filtered.body.add_translation_unit(tu)

filtered.write("recent-only.tmx")
```

## Building Custom TM Services

### Simple TM Lookup API

```python
from flask import Flask, request, jsonify
from pythontmx import TmxFile
from difflib import SequenceMatcher

app = Flask(__name__)

# Load TM on startup
tmx = TmxFile.read("memory.tmx")
source_lang = tmx.header.source_lang

def fuzzy_match(source, segment, threshold=0.7):
    """Calculate similarity between two segments"""
    ratio = SequenceMatcher(None, source, segment).ratio()
    return ratio >= threshold

@app.route('/lookup', methods=['POST'])
def lookup():
    data = request.json
    query = data['segment']
    target_lang = data['target_lang']
    threshold = data.get('threshold', 0.7)

    matches = []
    for tu in tmx.body.translation_units:
        source_seg = tu.get_variant(source_lang).segment

        # Calculate match percentage
        ratio = SequenceMatcher(None, query, source_seg).ratio()

        if ratio >= threshold:
            target_var = tu.get_variant(target_lang)
            if target_var:
                matches.append({
                    'source': source_seg,
                    'target': target_var.segment,
                    'match_percentage': int(ratio * 100)
                })

    # Sort by match percentage
    matches.sort(key=lambda x: x['match_percentage'], reverse=True)

    return jsonify({'matches': matches})

if __name__ == '__main__':
    app.run()
```

**Usage:**
```bash
curl -X POST http://localhost:5000/lookup \
  -H "Content-Type: application/json" \
  -d '{"segment": "Hello world", "target_lang": "fr-FR", "threshold": 0.8}'
```

## Sources

- [PythonTmx Documentation](https://python-tmx.readthedocs.io/en/stable/)
- [python-tmx on PyPI](https://pypi.org/project/python-tmx/)
- [Medium: Converting TMX Files to Excel using Python](https://medium.com/@said.surucu/step-by-step-guide-to-converting-tmx-files-to-excel-using-python-c4dc72ef0875)
- [Medium: Optimizing TMX Files - Python Script to Remove Duplicates](https://medium.com/@said.surucu/optimizing-tmx-files-a-python-script-to-remove-duplicates-363eb46bce8a)
- [Medium: Automating TMX Creation from Phrase Strings](https://medium.com/@christelle_77574/automating-tmx-creation-from-phrase-strings-a-localization-engineers-best-friend-8d4471cffce5)
