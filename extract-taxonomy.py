#!/usr/bin/env python3
"""
Extract taxonomy from content/_index.md to data/survey-taxonomy.yaml.
Run once to bootstrap. Subsequent regeneration uses update-survey-index.py.
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent
INDEX_FILE = ROOT / 'content/_index.md'
TAXONOMY_FILE = ROOT / 'data/survey-taxonomy.yaml'


def code_to_slug(code):
    """Convert survey code to URL slug: 1.033.1 → 1-033-1"""
    return code.replace('.', '-')


def parse_entry_line(line):
    """
    Parse a single entry line. Returns dict with keys:
      code, title, subtitle (optional), future (bool), sub (bool)
    """
    raw = line.rstrip()
    sub = raw.startswith('  -')
    stripped = raw.lstrip().lstrip('- ').strip()

    # Future slot: **1.046** _Available for future use_
    future_match = re.match(r'\*\*(.+?)\*\*\s+_Available for future use_', stripped)
    if future_match:
        return {'code': future_match.group(1), 'future': True, 'sub': sub}

    # Completed: ✅ [**1.001** Title text](/survey/slug) - subtitle
    completed_match = re.match(
        r'✅\s+\[\*\*(.+?)\*\*\s+(.*?)\]\(/survey/(.+?)\)(?:\s+-\s+(.*))?$',
        stripped
    )
    if completed_match:
        code = completed_match.group(1)
        link_title = completed_match.group(2).strip()
        slug = completed_match.group(3)
        after_subtitle = completed_match.group(4)

        # Subtitle placement: either inside link text ("Title - Sub") or after link ("Title](url) - Sub")
        subtitle_in_link = False
        if ' - ' in link_title and not after_subtitle:
            # Subtitle is INSIDE the link text
            parts = link_title.split(' - ', 1)
            title = parts[0].strip()
            subtitle = parts[1].strip()
            subtitle_in_link = True
        elif after_subtitle:
            title = link_title
            subtitle = after_subtitle.strip()
        else:
            title = link_title
            subtitle = None

        entry = {'code': code, 'title': title, 'sub': sub, 'published': True}
        if subtitle:
            entry['subtitle'] = subtitle
        if subtitle_in_link:
            entry['subtitle_in_link'] = True
        # Only store slug if it differs from default (code → slug)
        expected_slug = code_to_slug(code)
        if slug != expected_slug:
            entry['slug'] = slug
        return entry

    # Planned (non-completed): **1.026** Title - subtitle
    planned_match = re.match(r'\*\*(.+?)\*\*\s+(.*?)$', stripped)
    if planned_match:
        code = planned_match.group(1)
        rest = planned_match.group(2).strip()

        # Split title from subtitle on " - "
        if ' - ' in rest:
            parts = rest.split(' - ', 1)
            title = parts[0].strip()
            subtitle = parts[1].strip()
        else:
            title = rest
            subtitle = None

        entry = {'code': code, 'title': title, 'sub': sub}
        if subtitle:
            entry['subtitle'] = subtitle
        return entry

    return None


def yaml_str(s, indent=0):
    """Produce a safe YAML string value (quoted if needed)."""
    if not s:
        return '""'
    # Check if needs quoting: contains special chars
    needs_quote = any(c in s for c in [':', '#', '[', ']', '{', '}', ',', '&', '*', '?', '|', '-', '<', '>', '=', '!', '%', '@', '`', "'", '"', '\n'])
    if needs_quote:
        escaped = s.replace('\\', '\\\\').replace('"', '\\"')
        return f'"{escaped}"'
    return s


def write_taxonomy(sections, output_file):
    """Write taxonomy YAML file."""
    lines = ['# Survey taxonomy — auto-extracted from content/_index.md',
             '# Edit here to add/remove slots. Completion status is detected dynamically.',
             '# Run update-survey-index.py to regenerate content/_index.md',
             '# Run update-sidebar.py to regenerate sidebars.ts',
             '',
             'sections:']

    for section in sections:
        lines.append(f'  - range: {yaml_str(section["range"])}')
        lines.append(f'    title: {yaml_str(section["title"])}')
        if section['entries']:
            lines.append('    entries:')
            for entry in section['entries']:
                _write_entry(lines, entry, indent=6)

    output_file.write_text('\n'.join(lines) + '\n', encoding='utf-8')


def _write_entry(lines, entry, indent):
    prefix = ' ' * indent
    bullet = prefix + '- '

    # Always quote codes to prevent YAML float parsing (1.010 → 1.01)
    quoted_code = f'"{entry["code"]}"'
    if entry.get('future'):
        lines.append(f'{bullet}code: {quoted_code}')
        lines.append(f'{prefix}  future: true')
    else:
        lines.append(f'{bullet}code: {quoted_code}')
        lines.append(f'{prefix}  title: {yaml_str(entry["title"])}')
        if entry.get('subtitle'):
            lines.append(f'{prefix}  subtitle: {yaml_str(entry["subtitle"])}')
        if entry.get('published'):
            lines.append(f'{prefix}  published: true')
        if entry.get('subtitle_in_link'):
            lines.append(f'{prefix}  subtitle_in_link: true')
        if entry.get('slug'):
            lines.append(f'{prefix}  slug: {yaml_str(entry["slug"])}')
        if entry.get('children'):
            lines.append(f'{prefix}  children:')
            for child in entry['children']:
                _write_entry(lines, child, indent + 4)


def main():
    content = INDEX_FILE.read_text(encoding='utf-8')
    lines = content.split('\n')

    sections = []
    current_section = None
    current_parent = None  # Track current top-level entry for sub-entries

    for line in lines:
        # Section header: ## 1.001-009: Title
        section_match = re.match(r'^## ([\d\.\-]+): (.+)$', line)
        if section_match:
            current_section = {
                'range': section_match.group(1),
                'title': section_match.group(2),
                'entries': []
            }
            sections.append(current_section)
            current_parent = None
            continue

        if not current_section:
            continue

        # Entry lines start with "- " or "  - "
        if not (line.startswith('- ') or line.startswith('  - ')):
            continue

        entry = parse_entry_line(line)
        if not entry:
            continue

        is_sub = entry.pop('sub', False)

        if is_sub:
            # Add as child of current parent
            if current_parent is not None:
                if 'children' not in current_parent:
                    current_parent['children'] = []
                current_parent['children'].append(entry)
            else:
                # Orphaned sub-entry, add to section directly
                current_section['entries'].append(entry)
        else:
            current_section['entries'].append(entry)
            current_parent = entry if not entry.get('future') else None

    TAXONOMY_FILE.parent.mkdir(parents=True, exist_ok=True)
    write_taxonomy(sections, TAXONOMY_FILE)
    print(f'✓ Wrote {TAXONOMY_FILE}')

    # Summary
    total_entries = sum(
        len(s['entries']) + sum(len(e.get('children', [])) for e in s['entries'])
        for s in sections
    )
    print(f'  {len(sections)} sections, {total_entries} total entries')


if __name__ == '__main__':
    main()
