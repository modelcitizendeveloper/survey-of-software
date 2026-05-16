#!/usr/bin/env python3
"""
Auto-generate sidebars.ts from data/survey-taxonomy.yaml + completion detection.

Generates a Docusaurus-format sidebar listing all published survey entries
in numeric order.

Usage:
  uv run python update-sidebar.py [--dry-run]
"""

import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    import subprocess
    subprocess.run([sys.executable, '-m', 'pip', 'install', 'pyyaml', '-q'], check=True)
    import yaml

ROOT = Path(__file__).parent
TAXONOMY_FILE = ROOT / 'data/survey-taxonomy.yaml'
PACKAGES_DIR = ROOT / 'packages/research'
OUTPUT_FILE = ROOT / 'sidebars.ts'


def code_to_slug(code):
    """Convert survey code to URL slug: 1.033.1 → 1-033-1"""
    return str(code).replace('.', '-')


def normalize_code(raw):
    return str(raw)


def get_metadata_completed_codes():
    """Return set of codes completed per packages/research/*/metadata.yaml."""
    completed = set()
    for meta_path in PACKAGES_DIR.glob('*/metadata.yaml'):
        try:
            text = meta_path.read_text(encoding='utf-8')
            docs = list(yaml.safe_load_all(text))
            data = next((d for d in docs if d), None)
            if not data:
                continue
            status = data.get('status') or data.get('experiment_status', '')
            code = data.get('code') or data.get('experiment_number')
            if code and str(status).lower() in ('completed', 'complete'):
                completed.add(str(code))
        except Exception:
            try:
                text = meta_path.read_text(encoding='utf-8')
                code_match = re.search(r'^code:\s*[\'"]?([0-9.]+)[\'"]?', text, re.M)
                exp_match = re.search(r'^experiment_number:\s*[\'"]?([0-9.]+)[\'"]?', text, re.M)
                status_match = re.search(r'^(?:status|experiment_status):\s*[\'"]?(completed?|complete)[\'"]?', text, re.M | re.I)
                code_val = code_match or exp_match
                if code_val and status_match:
                    completed.add(code_val.group(1))
            except Exception:
                pass
    return completed


def get_taxonomy_published_codes(taxonomy):
    """Return set of codes marked published: true in taxonomy.yaml."""
    published = set()

    def collect(entries):
        for entry in entries:
            if entry.get('published'):
                published.add(normalize_code(entry.get('code', '')))
            collect(entry.get('children', []))

    for section in taxonomy['sections']:
        collect(section.get('entries', []))
    return published


def get_completed_codes(taxonomy):
    """Return set of completed codes from taxonomy + metadata.yaml."""
    completed = get_taxonomy_published_codes(taxonomy)
    completed |= get_metadata_completed_codes()
    return completed


def collect_published_entries(taxonomy, completed_codes):
    """
    Return sorted list of (code, slug) tuples for published entries.
    Sorted numerically by code.
    """
    entries = []

    def add_entry(entry):
        code = normalize_code(entry.get('code', ''))
        if not entry.get('future') and code in completed_codes:
            slug = entry.get('slug', code_to_slug(code))
            entries.append((code, slug))
        for child in entry.get('children', []):
            add_entry(child)

    for section in taxonomy['sections']:
        for entry in section.get('entries', []):
            add_entry(entry)

    # Sort numerically: 1.001 < 1.002 < 1.010 < 1.033.1 < 1.034
    def sort_key(item):
        code = item[0]
        parts = code.split('.')
        return tuple(int(p.split('-')[0]) if p.split('-')[0].isdigit() else 0 for p in parts)

    entries.sort(key=sort_key)
    return entries


def generate_sidebars(entries):
    """Generate sidebars.ts content."""
    lines = ['const sidebars = {', '  surveySidebar: [']
    lines.append('    {type: "doc", id: "survey/survey-intro"},')
    for code, slug in entries:
        lines.append(f'    {{type: "doc", id: "survey/{slug}"}},')
    lines.append('  ],')
    lines.append('};')
    lines.append('')
    lines.append('export default sidebars;')
    return '\n'.join(lines) + '\n'


def main():
    dry_run = '--dry-run' in sys.argv

    taxonomy = yaml.safe_load(TAXONOMY_FILE.read_text(encoding='utf-8'))
    completed_codes = get_completed_codes(taxonomy)
    entries = collect_published_entries(taxonomy, completed_codes)

    content = generate_sidebars(entries)

    if dry_run:
        print(content)
    else:
        OUTPUT_FILE.write_text(content, encoding='utf-8')
        print(f'✓ Wrote {OUTPUT_FILE}')
        print(f'  {len(entries)} sidebar entries')


if __name__ == '__main__':
    main()
