# Scenario: Multilingual Content Management

## Context

**Goal**: Align content across 10+ language versions of documentation site
**Starting point**: Markdown files in /docs/en/, /docs/de/, /docs/fr/, etc.
**Quality requirement**: 98%+ precision (user-facing content)
**Use case**: Translation memory, content reuse, consistency checking

## Tool Selection: vecalign

**Rationale**:
- High accuracy needed for user-facing content
- Multiple language pairs (10+ languages)
- Single tool works for all pairs (no per-language dictionaries)
- Moderate corpus size (~100K sentences total)

**Not hunalign because**: Need higher accuracy, multiple language pairs
**Not bleualign because**: No MT infrastructure available

## Complete Workflow

### Step 1: Extract Content from Markdown
```python
# extract_sentences.py
import os
import re
from pathlib import Path

def extract_text_from_markdown(md_file):
    """
    Extract text content from Markdown, removing code blocks and metadata
    """
    with open(md_file) as f:
        content = f.read()

    # Remove frontmatter
    content = re.sub(r'^---\n.*?\n---\n', '', content, flags=re.DOTALL)

    # Remove code blocks
    content = re.sub(r'```.*?```', '', content, flags=re.DOTALL)
    content = re.sub(r'`[^`]+`', '', content)

    # Remove markdown syntax
    content = re.sub(r'#{1,6}\s', '', content)  # Headers
    content = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', content)  # Links
    content = re.sub(r'[*_]{1,2}([^*_]+)[*_]{1,2}', r'\1', content)  # Emphasis

    # Split into sentences (simple approach)
    sentences = re.split(r'[.!?]+\s+', content)
    return [s.strip() for s in sentences if s.strip()]

def process_docs_directory(docs_dir, output_file, lang_code):
    """
    Process all markdown files in docs directory
    """
    sentences = []
    file_mapping = []

    for md_file in Path(docs_dir).rglob('*.md'):
        sents = extract_text_from_markdown(md_file)
        for sent in sents:
            sentences.append(sent)
            file_mapping.append(str(md_file))

    # Write sentences
    with open(output_file, 'w') as f:
        for sent in sentences:
            f.write(sent + '\n')

    # Write mapping (for later reference)
    with open(f'{output_file}.map', 'w') as f:
        for mapping in file_mapping:
            f.write(mapping + '\n')

if __name__ == '__main__':
    languages = ['en', 'de', 'fr', 'es', 'ja', 'zh']

    for lang in languages:
        process_docs_directory(
            f'docs/{lang}/',
            f'extracted/{lang}.txt',
            lang
        )
```

### Step 2: Set Up vecalign
```bash
#!/bin/bash
# setup_vecalign.sh

# Clone vecalign
git clone https://github.com/thompsonb/vecalign
cd vecalign

# Install dependencies
pip install -r requirements.txt

# Download LASER models (one-time, ~1.2GB)
bash download_models.sh

cd ..
```

### Step 3: Generate Embeddings for All Languages
```bash
#!/bin/bash
# generate_embeddings.sh

LANGUAGES=("en" "de" "fr" "es" "ja" "zh")
LANG_CODES=("en" "de" "fr" "es" "ja" "zh")

for i in "${!LANGUAGES[@]}"; do
    lang=${LANGUAGES[$i]}
    code=${LANG_CODES[$i]}

    python3 vecalign/embed.py \
        --text extracted/${lang}.txt \
        --lang ${code} \
        --output embeddings/${lang}.emb

    echo "Embedded $lang"
done
```

### Step 4: Align All Language Pairs Against English (as pivot)
```python
# align_all_pairs.py
import subprocess
from itertools import combinations

def align_pair(src_lang, tgt_lang):
    """
    Align a language pair using vecalign
    """
    cmd = [
        'python3', 'vecalign/vecalign.py',
        '--src', f'extracted/{src_lang}.txt',
        '--tgt', f'extracted/{tgt_lang}.txt',
        '--src_embed', f'embeddings/{src_lang}.emb',
        '--tgt_embed', f'embeddings/{tgt_lang}.emb',
        '--alignment_max_size', '4',
        '--min_sim', '0.4'
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)

    output_file = f'alignments/{src_lang}-{tgt_lang}.txt'
    with open(output_file, 'w') as f:
        f.write(result.stdout)

    return output_file

if __name__ == '__main__':
    languages = ['en', 'de', 'fr', 'es', 'ja', 'zh']

    # Align all against English (pivot)
    for lang in languages:
        if lang != 'en':
            print(f"Aligning en-{lang}")
            align_pair('en', lang)
```

### Step 5: Build Translation Memory Database
```python
# build_tm_database.py
import sqlite3
from collections import defaultdict

def create_tm_database(db_path='translation_memory.db'):
    """
    Create SQLite database for translation memory
    """
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    # Create tables
    c.execute('''
        CREATE TABLE IF NOT EXISTS segments (
            id INTEGER PRIMARY KEY,
            segment_id TEXT UNIQUE,
            source_file TEXT
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS translations (
            segment_id TEXT,
            lang TEXT,
            text TEXT,
            FOREIGN KEY (segment_id) REFERENCES segments(segment_id)
        )
    ''')

    c.execute('''
        CREATE INDEX idx_segment_id ON translations(segment_id)
    ''')

    c.execute('''
        CREATE INDEX idx_lang ON translations(lang)
    ''')

    conn.commit()
    return conn

def load_alignments(alignment_file, src_lang, tgt_lang):
    """
    Parse vecalign output
    """
    alignments = []
    with open(alignment_file) as f:
        for line in f:
            parts = line.strip().split('\t')
            if len(parts) >= 2:
                src_indices = parts[0].split(',')
                tgt_indices = parts[1].split(',')
                alignments.append((src_indices, tgt_indices))
    return alignments

def populate_database(conn):
    """
    Populate TM database from alignments
    """
    languages = ['en', 'de', 'fr', 'es', 'ja', 'zh']

    # Load source sentences
    source_texts = {}
    for lang in languages:
        with open(f'extracted/{lang}.txt') as f:
            source_texts[lang] = [line.strip() for line in f]

    # Load alignments (English as pivot)
    segment_counter = 0
    segments = defaultdict(dict)  # segment_id -> {lang: text}

    for lang in languages:
        if lang == 'en':
            continue

        alignment_file = f'alignments/en-{lang}.txt'
        alignments = load_alignments(alignment_file, 'en', lang)

        for en_idx, tgt_idx in alignments:
            # Create segment ID from English indices
            segment_id = f"en:{','.join(map(str, en_idx))}"

            # Get English text
            en_text = ' '.join([source_texts['en'][int(i)] for i in en_idx])

            # Get target text
            tgt_text = ' '.join([source_texts[lang][int(i)] for i in tgt_idx])

            # Store in segments dict
            segments[segment_id]['en'] = en_text
            segments[segment_id][lang] = tgt_text

    # Insert into database
    c = conn.cursor()
    for segment_id, translations in segments.items():
        # Insert segment
        c.execute('INSERT OR IGNORE INTO segments (segment_id) VALUES (?)',
                  (segment_id,))

        # Insert translations
        for lang, text in translations.items():
            c.execute('''
                INSERT INTO translations (segment_id, lang, text)
                VALUES (?, ?, ?)
            ''', (segment_id, lang, text))

    conn.commit()

if __name__ == '__main__':
    conn = create_tm_database()
    populate_database(conn)
    print("Translation memory database created successfully")
```

### Step 6: Query Translation Memory
```python
# query_tm.py
import sqlite3
from difflib import SequenceMatcher

def find_translation(source_text, source_lang='en', target_lang='de',
                     threshold=0.8):
    """
    Find translation in TM, with fuzzy matching
    """
    conn = sqlite3.connect('translation_memory.db')
    c = conn.cursor()

    # Get all segments in source language
    c.execute('''
        SELECT segment_id, text FROM translations
        WHERE lang = ?
    ''', (source_lang,))

    best_match = None
    best_score = 0

    for segment_id, text in c.fetchall():
        # Compute similarity
        score = SequenceMatcher(None, source_text, text).ratio()

        if score > best_score:
            best_score = score
            best_match = segment_id

    # If good match found, get translation
    if best_score >= threshold:
        c.execute('''
            SELECT text FROM translations
            WHERE segment_id = ? AND lang = ?
        ''', (best_match, target_lang))

        result = c.fetchone()
        if result:
            return {
                'translation': result[0],
                'match_quality': best_score,
                'segment_id': best_match
            }

    return None

# Example usage
if __name__ == '__main__':
    result = find_translation(
        "This feature is currently in beta.",
        source_lang='en',
        target_lang='de',
        threshold=0.8
    )

    if result:
        print(f"Match: {result['match_quality']:.2%}")
        print(f"Translation: {result['translation']}")
    else:
        print("No match found")
```

## Integration with CMS

### Webhook for New Content
```python
# cms_webhook.py
from flask import Flask, request
import subprocess

app = Flask(__name__)

@app.route('/content_updated', methods=['POST'])
def content_updated():
    """
    Triggered when content is updated in CMS
    """
    data = request.json
    file_path = data['file_path']
    language = data['language']

    # Re-extract sentences
    subprocess.run(['python3', 'extract_sentences.py', file_path, language])

    # Re-generate embeddings
    subprocess.run(['python3', 'vecalign/embed.py',
                    '--text', f'extracted/{language}.txt',
                    '--lang', language,
                    '--output', f'embeddings/{language}.emb'])

    # Re-align (only affected language pair)
    subprocess.run(['python3', 'align_all_pairs.py', '--lang', language])

    # Update TM database
    subprocess.run(['python3', 'build_tm_database.py', '--incremental'])

    return {'status': 'success'}

if __name__ == '__main__':
    app.run(port=5000)
```

## Performance Benchmarks

### Hardware: GPU (NVIDIA V100), 16GB VRAM
| Corpus Size | Embedding Time | Alignment Time | Total |
|-------------|----------------|----------------|-------|
| 10K sentences | 1 minute | 30 seconds | 1.5 min |
| 100K sentences | 8 minutes | 5 minutes | 13 min |
| 500K sentences | 35 minutes | 25 minutes | 60 min |

### Expected Quality
- **Precision**: 97-99% (clean documentation)
- **Recall**: 95-98%
- **F1 Score**: 96-98%

## Cost Estimates

### One-Time Setup
- **GPU instance** (AWS p3.2xlarge): $3.06/hour
- **Model download**: Free (1.2GB, one-time)
- **Initial alignment** (100K sentences): ~15 minutes = **$0.77**

### Ongoing Maintenance
- **Incremental updates**: 5 minutes per content change = **$0.26/update**
- **Monthly cost** (10 updates/month): **$2.60**

## Quality Assurance

### Validation Dashboard
```python
# validation_dashboard.py
import streamlit as st
import sqlite3

st.title("Translation Memory Validation")

# Load random sample
conn = sqlite3.connect('translation_memory.db')
c = conn.cursor()

c.execute('''
    SELECT segment_id FROM segments
    ORDER BY RANDOM()
    LIMIT 100
''')

for (segment_id,) in c.fetchall():
    st.subheader(f"Segment: {segment_id}")

    # Get all translations
    c.execute('''
        SELECT lang, text FROM translations
        WHERE segment_id = ?
    ''', (segment_id,))

    translations = dict(c.fetchall())

    for lang, text in translations.items():
        st.text(f"{lang}: {text}")

    # Validation
    is_correct = st.checkbox(f"Correct alignment?", key=segment_id)

    st.markdown("---")
```

## Troubleshooting

### Problem: Misaligned Segments
**Cause**: Document structure differences (extra paragraphs in one language)
**Solution**: Use `--alignment_max_size 8` for more flexible alignment

### Problem: Low Similarity Scores
**Cause**: Creative translation, not literal
**Solution**: Lower `--min_sim` threshold to 0.2 or 0.3

### Problem: Slow Embedding Generation
**Cause**: CPU-only, no GPU available
**Solution**: Use batch processing, consider cloud GPU

## References

- [vecalign Documentation](https://github.com/thompsonb/vecalign)
- [LASER Multilingual Embeddings](https://github.com/facebookresearch/LASER)
- [Translation Memory Best Practices](https://en.wikipedia.org/wiki/Translation_memory)
