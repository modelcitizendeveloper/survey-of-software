#!/usr/bin/env python3
"""
Auto-generate content/_index.md from data/survey-taxonomy.yaml + metadata.yaml files.

Completion detection (in priority order):
  1. published: true in data/survey-taxonomy.yaml (bootstrapped from original index)
  2. packages/research/<code*>/metadata.yaml with status=completed or experiment_status=complete

Usage:
  uv run python update-survey-index.py [--dry-run]
"""

import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("Installing pyyaml...")
    import subprocess
    subprocess.run([sys.executable, '-m', 'pip', 'install', 'pyyaml', '-q'], check=True)
    import yaml

ROOT = Path(__file__).parent
TAXONOMY_FILE = ROOT / 'data/survey-taxonomy.yaml'
PACKAGES_DIR = ROOT / 'packages/research'
CONTENT_DIR = ROOT / 'content/survey'
OUTPUT_FILE = ROOT / 'content/_index.md'

HEADER = """---
title: "Survey of Software"
weight: 1
bookFlatSection: false
bookCollapseSection: false
aliases: ["/survey/"]
description: "Software library research across sorting, search, NLP, ML, frontend, LLMs — benchmarks, decision frameworks, production patterns."
---

# Survey of Software

> **Systematic coverage of general-purpose software libraries.**
> Measured research on algorithms, data structures, ML, and infrastructure—so you can build with confidence instead of guessing.

**[What is this? →](/about)** | **[The Vision →](/vision)** | **[Method →](/survey/method)**

**[Claude Skill →](/skill/)** Let Claude consult this research library directly in conversations. Ask about library selection, and Claude fetches surveys, synthesizes recommendations, or runs live research on uncovered topics.

---

**Newsletter:** New library research published as it's ready. Monthly digest of what's new — [subscribe to stay current →](https://modelcitizendeveloper.com/)

---
"""

FOOTER = """---

**Want to understand our approach?** [Read the Vision →](/vision)

**Want to replicate this research?** [See the Methodology →](/survey/methodology)

---

© 2026 Ivan Schneider · [Model Citizen Developer](https://modelcitizendeveloper.com/)
Licensed under [CC BY 4.0](/license/)
"""


def code_to_slug(code):
    """Convert survey code to URL/filename slug: 1.033.1 → 1-033-1"""
    return str(code).replace('.', '-')


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
            # Fall back to regex for malformed YAML
            try:
                text = meta_path.read_text(encoding='utf-8')
                code_match = re.search(r'^code:\s*[\'"]?([0-9.]+)[\'"]?', text, re.M)
                exp_match = re.search(r'^experiment_number:\s*[\'"]?([0-9.]+)[\'"]?', text, re.M)
                status_match = re.search(r'^(?:status|experiment_status):\s*[\'"]?(completed?|complete)[\'"]?', text, re.M | re.I)
                code_val = code_match or exp_match
                if code_val and status_match:
                    completed.add(code_val.group(1))
            except Exception:
                print(f'  Warning: could not parse {meta_path}', file=sys.stderr)
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
    """
    Return set of completed codes. Priority:
    1. published: true in taxonomy.yaml (bootstrapped from original index)
    2. packages/research/*/metadata.yaml with completed status
    """
    completed = get_taxonomy_published_codes(taxonomy)
    completed |= get_metadata_completed_codes()
    return completed


def get_entry_title_info(entry, completed_codes):
    """Get title and subtitle for an entry, checking metadata.yaml for overrides."""
    code = normalize_code(entry.get('code', ''))
    title = str(entry.get('title', code))
    subtitle = entry.get('subtitle', '')

    if code not in completed_codes:
        return title, subtitle

    # Check metadata.yaml for richer title data
    code_prefix = code.rstrip('.')
    for meta_path in PACKAGES_DIR.glob('*/metadata.yaml'):
        try:
            data = yaml.safe_load(meta_path.read_text(encoding='utf-8'))
            if not data:
                continue
            meta_code = str(data.get('code') or data.get('experiment_number', ''))
            if meta_code == code_prefix:
                meta_title = data.get('title', '')
                meta_subtitle = data.get('subtitle', '')
                if meta_title:
                    title = meta_title
                if meta_subtitle and not subtitle:
                    subtitle = meta_subtitle
                break
        except Exception:
            pass

    return title, subtitle


def normalize_code(raw):
    """Ensure code is a properly formatted string like '1.001', '1.033.1'."""
    s = str(raw)
    # Handle float-parsed codes: '1.01' should stay as-is, but check if it's
    # a truncated 3-digit group (e.g. 1.01 from YAML parsing of 1.010)
    # Since we now quote all codes in taxonomy.yaml, this shouldn't happen,
    # but keep as safety net.
    return s


def format_entry(entry, completed_codes, indent=0):
    """Format a single taxonomy entry as a markdown line."""
    code = normalize_code(entry.get('code', ''))
    prefix = '  ' * (indent // 2)

    if entry.get('future'):
        return f'{prefix}- **{code}** _Available for future use_'

    title, subtitle = get_entry_title_info(entry, completed_codes)
    slug = entry.get('slug', code_to_slug(code))

    if code in completed_codes:
        subtitle_in_link = entry.get('subtitle_in_link', False)
        if subtitle and subtitle_in_link:
            return f'{prefix}- ✅ [**{code}** {title} - {subtitle}](/survey/{slug})'
        elif subtitle:
            return f'{prefix}- ✅ [**{code}** {title}](/survey/{slug}) - {subtitle}'
        else:
            return f'{prefix}- ✅ [**{code}** {title}](/survey/{slug})'
    else:
        if subtitle:
            return f'{prefix}- **{code}** {title} - {subtitle}'
        else:
            return f'{prefix}- **{code}** {title}'


def count_entries(section, completed_codes):
    """Count (completed, total) for a section including sub-entries."""
    completed = 0
    total = 0
    for entry in section['entries']:
        if entry.get('future'):
            # Future slots (single or range) each count as 1 placeholder
            total += 1
            continue
        total += 1
        if normalize_code(entry.get('code', '')) in completed_codes:
            completed += 1
        for child in entry.get('children', []):
            total += 1
            if normalize_code(child.get('code', '')) in completed_codes:
                completed += 1
    return completed, total


def generate_index(taxonomy, completed_codes):
    """Generate the full content/_index.md text."""
    lines = [HEADER.rstrip()]

    total_completed = 0
    total_defined = 0

    for section in taxonomy['sections']:
        section_completed, section_total = count_entries(section, completed_codes)
        total_completed += section_completed
        total_defined += section_total

        lines.append(f'')
        lines.append(f'## {section["range"]}: {section["title"]}')
        lines.append(f'')
        lines.append(f'**Completed: {section_completed}/{section_total}**')
        lines.append(f'')

        for entry in section['entries']:
            lines.append(format_entry(entry, completed_codes, indent=0))
            for child in entry.get('children', []):
                lines.append(format_entry(child, completed_codes, indent=2))

        lines.append(f'')
        lines.append('---')

    # Status summary
    remaining = total_defined - total_completed
    lines.append(f'')
    lines.append(f'## Research Status')
    lines.append(f'')
    lines.append(f'**Total Defined**: {total_defined} research slots')
    lines.append(f'**Completed**: {total_completed} pieces ({int(100*total_completed/total_defined)}%)')
    lines.append(f'**Remaining**: {remaining} pieces')
    lines.append(f'')
    lines.append(f'**Navigation**: Use the sidebar to browse completed research, or select a category above.')
    lines.append(f'')
    lines.append('---')

    lines.append(FOOTER.rstrip())
    return '\n'.join(lines) + '\n'


def main():
    dry_run = '--dry-run' in sys.argv

    taxonomy = yaml.safe_load(TAXONOMY_FILE.read_text(encoding='utf-8'))
    completed_codes = get_completed_codes(taxonomy)

    print(f'Detected {len(completed_codes)} completed codes')

    index_content = generate_index(taxonomy, completed_codes)

    if dry_run:
        print(index_content)
    else:
        OUTPUT_FILE.write_text(index_content, encoding='utf-8')
        print(f'✓ Wrote {OUTPUT_FILE}')

        # Count ✅ entries written
        check_count = index_content.count('✅')
        print(f'  {check_count} completed entries marked')


if __name__ == '__main__':
    main()
