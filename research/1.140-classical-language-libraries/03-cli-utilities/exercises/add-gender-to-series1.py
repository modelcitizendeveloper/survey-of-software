#!/usr/bin/env python3
"""Add gender field to all Series 1 (model-nouns) exercises."""

import json
from pathlib import Path

# Gender for model nouns
GENDER_MAP = {
    'puella': 'f',
    'ventus': 'm',
    'miles': 'm',
    'usus': 'm',
    'res': 'f'
}

series_dir = Path(__file__).parent / 'model-nouns'

for jsonl_file in sorted(series_dir.glob('*.jsonl')):
    print(f"Processing {jsonl_file.name}...")

    lines = []
    with open(jsonl_file, 'r', encoding='utf-8') as f:
        for line in f:
            data = json.loads(line)

            # Skip metadata lines
            if data.get('_metadata'):
                lines.append(line)
                continue

            # Add gender to each word
            for word in data['words']:
                lemma = word['lemma']
                if lemma in GENDER_MAP and 'gender' not in word:
                    word['gender'] = GENDER_MAP[lemma]

            lines.append(json.dumps(data) + '\n')

    # Write back
    with open(jsonl_file, 'w', encoding='utf-8') as f:
        f.writelines(lines)

    print(f"  ✅ Added gender to {jsonl_file.name}")

print("\n✅ All Series 1 files updated with gender")
