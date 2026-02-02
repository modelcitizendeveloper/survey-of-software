#!/usr/bin/env python3
"""
Strict library extraction - only from pip install and import statements.

This conservative approach reduces false positives by only extracting
libraries from code contexts, not prose.
"""

import json
import re
from pathlib import Path
from collections import defaultdict

def extract_libraries_strict(content: str) -> set:
    """
    Extract libraries only from code contexts.

    Patterns:
    - pip install <library>
    - import <library>
    - from <library> import
    - Libraries in subtitle (explicitly listed comma-separated)
    """
    libraries = set()

    # Pattern 1: pip install
    pip_matches = re.findall(r'pip install\s+([a-zA-Z0-9_\-]+)', content)
    libraries.update(pip_matches)

    # Pattern 2: import statements
    import_matches = re.findall(r'^import ([a-zA-Z0-9_]+)', content, re.MULTILINE)
    libraries.update(import_matches)

    from_matches = re.findall(r'^from ([a-zA-Z0-9_]+) import', content, re.MULTILINE)
    libraries.update(from_matches)

    # Pattern 3: Subtitle library lists (high-confidence)
    # Format: "subtitle: Library1, Library2, Library3"
    subtitle_match = re.search(r'subtitle:\s*"([^"]+)"', content)
    if subtitle_match:
        subtitle = subtitle_match.group(1)
        # Split on comma, dash, or "and"
        parts = re.split(r'[,\-]|\s+and\s+', subtitle)
        for part in parts:
            # Extract CamelCase or lowercase library names
            lib_match = re.search(r'([A-Z][a-zA-Z0-9]*|[a-z][a-z0-9_\-]+)', part.strip())
            if lib_match:
                libraries.add(lib_match.group(1))

    # Filter out builtins and common false positives
    builtins = {
        'time', 'json', 'os', 'sys', 're', 'csv', 'math', 'random',
        'collections', 'datetime', 'itertools', 'functools', 'pathlib',
        'typing', 'unittest', 'logging', 'io', 'copy', 'pickle',
        # MDX components
        'Tabs', 'TabItem', 'theme',
        # Common words
        'Performance', 'Risk', 'Cost', 'Context', 'print'
    }

    libraries = {lib for lib in libraries
                 if lib not in builtins
                 and len(lib) >= 3
                 and not lib.startswith('--')
                 and not lib.isupper()}  # Exclude all-caps acronyms

    return libraries

def parse_markdown_strict(docs_dir: Path):
    """Parse markdown files with strict library extraction."""
    markdown_files = sorted(docs_dir.glob("1-*.md"))
    print(f"Found {len(markdown_files)} markdown files")

    all_libraries = defaultdict(lambda: {
        'name': '',
        'research_mentions': []
    })

    research_topics = []

    for md_file in markdown_files:
        try:
            content = md_file.read_text()

            # Extract ID and title
            id_match = re.search(r'^id:\s*([^\n]+)', content, re.MULTILINE)
            title_match = re.search(r'^title:\s*"([^"]+)"', content, re.MULTILINE)

            research_id = id_match.group(1).strip() if id_match else md_file.stem
            research_title = title_match.group(1) if title_match else 'Unknown'

            # Strict library extraction
            libraries = extract_libraries_strict(content)

            if libraries:
                research_topics.append({
                    'id': research_id,
                    'title': research_title,
                    'libraries': sorted(list(libraries))
                })

                for lib_name in libraries:
                    all_libraries[lib_name]['name'] = lib_name
                    all_libraries[lib_name]['research_mentions'].append({
                        'research_id': research_id,
                        'research_title': research_title
                    })

        except Exception as e:
            print(f"Error parsing {md_file.name}: {e}")

    return dict(all_libraries), research_topics

def merge_with_structured(structured_file: Path, markdown_libs: dict, markdown_topics: list) -> dict:
    """Merge markdown libraries with structured metadata."""
    # Load structured metadata (from metadata.yaml)
    with open(structured_file) as f:
        structured = json.load(f)

    structured_libs = structured.get('libraries', {})

    # Merge
    for lib_name, lib_data in markdown_libs.items():
        if lib_name in structured_libs:
            # Append markdown mentions to structured data
            structured_libs[lib_name]['research_mentions'].extend(
                lib_data['research_mentions']
            )
        else:
            # Add as new library (but mark as markdown-only)
            structured_libs[lib_name] = lib_data
            structured_libs[lib_name]['source'] = 'markdown'

    # Update counts
    structured['metadata']['num_libraries'] = len(structured_libs)
    structured['metadata']['sources'] = [
        'packages/research/*.yaml (structured)',
        'docs/survey/*.md (strict parsing)'
    ]

    # Add markdown topics
    existing_ids = {t['id'] for t in structured.get('research_topics', [])}
    for topic in markdown_topics:
        if topic['id'] not in existing_ids:
            structured['research_topics'].append(topic)

    structured['metadata']['num_research_topics'] = len(structured['research_topics'])

    return structured

def print_report(data: dict):
    """Print extraction report."""
    libraries = data['libraries']

    print(f"\nTotal libraries: {len(libraries)}")

    # Count by source
    structured_count = sum(1 for lib in libraries.values()
                          if 'tags' in lib or 'categories' in lib)
    markdown_count = len(libraries) - structured_count

    print(f"  - From structured metadata: {structured_count}")
    print(f"  - From markdown (pip/import): {markdown_count}")

    # Mention distribution
    mention_counts = defaultdict(int)
    for lib_data in libraries.values():
        count = len(lib_data.get('research_mentions', []))
        mention_counts[count] += 1

    print("\nMention distribution:")
    for count in sorted(mention_counts.keys(), reverse=True)[:5]:
        print(f"  {count} topics: {mention_counts[count]} libraries")

    # Top libraries
    print("\nMost-mentioned libraries:")
    by_mentions = sorted(
        libraries.items(),
        key=lambda x: len(x[1].get('research_mentions', [])),
        reverse=True
    )

    for name, lib_data in by_mentions[:20]:
        mentions = len(lib_data.get('research_mentions', []))
        has_metadata = 'tags' in lib_data or 'categories' in lib_data
        source = '(structured)' if has_metadata else '(markdown)'
        print(f"  {name:25} - {mentions:2} mentions {source}")

def main():
    """Extract libraries with strict parsing."""
    docs_dir = Path(__file__).parent / "docs" / "survey"
    structured_file = Path(__file__).parent / "library-metadata.json"

    if not docs_dir.exists():
        print(f"Error: {docs_dir} not found")
        return

    print("Parsing markdown with strict extraction...")
    markdown_libs, markdown_topics = parse_markdown_strict(docs_dir)
    print(f"Extracted {len(markdown_libs)} libraries from markdown")

    print("\nMerging with structured metadata...")
    merged = merge_with_structured(structured_file, markdown_libs, markdown_topics)

    # Write output
    output_file = Path(__file__).parent / "library-metadata-clean.json"
    with open(output_file, 'w') as f:
        json.dump(merged, f, indent=2)

    print(f"\n✓ Wrote {output_file}")

    print_report(merged)

if __name__ == '__main__':
    main()
