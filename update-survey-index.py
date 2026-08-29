#!/usr/bin/env python3
"""
Regenerate the RANGE SECTIONS of content/_index.md from data/survey-taxonomy.yaml.

It rewrites only the text between <!-- SECTIONS:START --> and <!-- SECTIONS:END -->.
Everything else in the file -- front matter, the nav strip, the newsletter copy, the
POPULAR block, the footer -- is hand-maintained and passes through untouched. If the
markers are missing the script REFUSES to write, rather than guessing.

WHY IT WORKS THIS WAY (bead re-8la). It used to generate the whole file from a HEADER
and FOOTER constant, and both had drifted from what the site actually served. Running it
on 2026-08-29 would have deleted `newsletter_cta: true` (the subscriber capture on 179
pages), the Workshop nav link, the Field Notes copy, and the entire POPULAR block, and
would have rewritten the footer's /survey/method back to a /survey/methodology that does
not exist. 73 deletions in all. A generator whose template is a copy of the output will
drift from it; the fix is to stop keeping a copy.

COMPLETION IS MEASURED, NOT DECLARED. A survey is complete here if content/survey/<slug>.md
exists in this repo -- the site either carries the page or it does not. The old logic read
`published: true` from the taxonomy and a status field from packages/research/*/metadata.yaml,
and both undercounted: the taxonomy flag missed 21 surveys that have live pages, and
PACKAGES_DIR points at public/packages/research, which holds 12 stub directories rather
than the ~240 in the internal repo. Between them they scored 143 against 239 real pages,
so ~96 published surveys would have lost their checkmark AND their link.

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

SECTIONS_START = "<!-- SECTIONS:START -->"
SECTIONS_END = "<!-- SECTIONS:END -->"



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
    """Completed == content/survey/<slug>.md exists.

    The site either carries the page or it does not, and that is the only signal that
    cannot drift from what a reader sees. `published: true` in the taxonomy is kept as a
    union member so a hand-set flag still counts, but it is no longer the authority: it
    was false for 21 surveys that have live pages. The metadata.yaml scan is gone --
    PACKAGES_DIR resolves inside the PUBLIC repo, which carries a dozen stub directories,
    not the corpus.
    """
    from_pages = {p.stem.replace('-', '.') for p in CONTENT_DIR.glob('*.md')}
    completed = set()
    for entry_code in _all_codes(taxonomy):
        if code_to_slug(entry_code) in {p.stem for p in CONTENT_DIR.glob('*.md')}:
            completed.add(entry_code)
    completed |= get_taxonomy_published_codes(taxonomy)
    return completed


def _all_codes(taxonomy):
    """Every non-future code the taxonomy names, children included."""
    out = set()

    def walk(entries):
        for e in entries:
            if not e.get('future'):
                out.add(normalize_code(e.get('code', '')))
            walk(e.get('children', []))

    for section in taxonomy['sections']:
        walk(section.get('entries', []))
    return out


def report_untracked_pages(taxonomy):
    """Pages the taxonomy does not name. They can never appear in the index.

    Not an error and not fixable here -- the generator cannot invent a slot or decide
    which range it belongs in. It is reported so the drift is visible instead of silent;
    on 2026-08-29 there were 75, including 1-067-1, 1-110-6, 1-176, 1-212, 1-215 and 1-216.
    """
    named = {code_to_slug(c) for c in _all_codes(taxonomy)}
    stray = sorted(p.stem for p in CONTENT_DIR.glob('*.md') if p.stem not in named)
    if stray:
        print(f'  Note: {len(stray)} live page(s) have no taxonomy entry and cannot be '
              f'listed: {", ".join(stray[:8])}{" ..." if len(stray) > 8 else ""}',
              file=sys.stderr)
    return stray


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
        # A future line may name several disjoint codes, e.g. 1.303 and 1.305-1.309.
        codes = ', '.join(f'**{c.strip()}**' for c in str(code).split(','))
        return f'{prefix}- {codes} _Available for future use_'

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
            # Reserved slots are not work. The index has always counted "7/7" for a
            # range with seven surveys and a free block; counting the placeholder
            # made every such range read as permanently one short.
            continue
        total += 1
        if normalize_code(entry.get('code', '')) in completed_codes:
            completed += 1
        for child in entry.get('children', []):
            total += 1
            if normalize_code(child.get('code', '')) in completed_codes:
                completed += 1
    return completed, total


def generate_sections(taxonomy, completed_codes):
    """The range sections plus the status summary. NOT the whole file."""
    lines = []
    total_completed = 0
    total_defined = 0

    for section in taxonomy['sections']:
        section_completed, section_total = count_entries(section, completed_codes)
        total_completed += section_completed
        total_defined += section_total

        lines.append('')
        lines.append(f'## {section["range"]}: {section["title"]}')
        lines.append('')
        # A section may carry hand-written prose instead of a tally -- 2.070-089 explains
        # why the series exists at all, which a count cannot say.
        if section.get('note'):
            lines.append(section['note'].rstrip())
        else:
            lines.append(f'**Completed: {section_completed}/{section_total}**')
        lines.append('')

        for entry in section['entries']:
            lines.append(format_entry(entry, completed_codes, indent=0))
            for child in entry.get('children', []):
                lines.append(format_entry(child, completed_codes, indent=2))

        lines.append('')
        lines.append('---')

    remaining = total_defined - total_completed
    pct = int(100 * total_completed / total_defined) if total_defined else 0
    lines += ['', '## Research Status', '',
              f'**Total Defined**: {total_defined} research slots',
              f'**Completed**: {total_completed} pieces ({pct}%)',
              f'**Remaining**: {remaining} pieces', '',
              '**Navigation**: Use the sidebar to browse completed research, '
              'or select a category above.', '', '---']
    return '\n'.join(lines).strip('\n')


def splice(existing, sections):
    """Replace only the marked region. Refuse if the markers are not both present.

    Refusing is the point. The previous version rebuilt the file from a template, so a
    template that had fallen behind silently deleted whatever the file had gained since.
    """
    if existing.count(SECTIONS_START) != 1 or existing.count(SECTIONS_END) != 1:
        raise SystemExit(
            f'REFUSING TO WRITE: {OUTPUT_FILE} must contain exactly one '
            f'{SECTIONS_START} and one {SECTIONS_END}. Everything outside them is '
            f'hand-maintained and this script will not regenerate it. See bead re-8la.')
    head, rest = existing.split(SECTIONS_START, 1)
    _, tail = rest.split(SECTIONS_END, 1)
    return f'{head}{SECTIONS_START}\n{sections}\n{SECTIONS_END}{tail}'


def main():
    dry_run = '--dry-run' in sys.argv

    taxonomy = yaml.safe_load(TAXONOMY_FILE.read_text(encoding='utf-8'))
    completed_codes = get_completed_codes(taxonomy)
    print(f'Detected {len(completed_codes)} completed codes '
          f'({len(list(CONTENT_DIR.glob("*.md")))} pages on disk)')
    report_untracked_pages(taxonomy)

    existing = OUTPUT_FILE.read_text(encoding='utf-8')
    updated = splice(existing, generate_sections(taxonomy, completed_codes))

    if updated == existing:
        print('✓ No change — index already matches the taxonomy')
        return

    if dry_run:
        import difflib
        for line in difflib.unified_diff(existing.splitlines(), updated.splitlines(),
                                         'current', 'generated', lineterm='', n=1):
            print(line)
        return

    OUTPUT_FILE.write_text(updated, encoding='utf-8')
    print(f'✓ Wrote {OUTPUT_FILE}')
    print(f'  {updated.count("✅")} completed entries marked')


if __name__ == '__main__':
    main()
