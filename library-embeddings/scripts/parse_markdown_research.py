#!/usr/bin/env python3
"""
Parse library names and relationships from published markdown research files.

Extracts library mentions from docs/survey/*.md to supplement the
structured metadata from packages/research/.
"""

import json
import re
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Set, Tuple

def extract_frontmatter(content: str) -> Dict[str, str]:
    """Extract YAML frontmatter from markdown."""
    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return {}

    frontmatter = {}
    for line in match.group(1).split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            frontmatter[key.strip()] = value.strip().strip('"')
    return frontmatter

def extract_library_names(content: str) -> Set[str]:
    """
    Extract library names from markdown content.

    Heuristics:
    - Code blocks with package names
    - pip install commands
    - import statements
    - Library names in headers and bold text
    """
    libraries = set()

    # Pattern 1: pip install commands
    pip_pattern = r'pip install ([a-zA-Z0-9_\-]+)'
    libraries.update(re.findall(pip_pattern, content))

    # Pattern 2: import statements
    import_pattern = r'import ([a-zA-Z0-9_]+)'
    libraries.update(re.findall(import_pattern, content))

    from_pattern = r'from ([a-zA-Z0-9_]+) import'
    libraries.update(re.findall(from_pattern, content))

    # Pattern 3: Code blocks with library names (simple heuristic)
    code_blocks = re.findall(r'```(?:python|bash)?\n(.*?)```', content, re.DOTALL)
    for block in code_blocks:
        # Look for common library names in code
        libraries.update(re.findall(r'\b([a-z][a-z0-9_]*)\s*\(', block))

    # Pattern 4: Bold library names (often used in headings)
    bold_pattern = r'\*\*([A-Z][a-zA-Z0-9_\-]+)\*\*'
    libraries.update(re.findall(bold_pattern, content))

    # Pattern 5: Library names in subtitle/title
    # These are often comma-separated in the title
    if '(' in content[:500]:  # Check near start of file
        subtitle_match = re.search(r'subtitle:.*?"([^"]+)"', content[:500])
        if subtitle_match:
            subtitle_libs = re.findall(r'([A-Z][a-zA-Z0-9_\-]+)', subtitle_match.group(1))
            libraries.update(subtitle_libs)

    # Filter out common Python builtins and false positives
    builtins = {'Python', 'True', 'False', 'None', 'List', 'Dict', 'Set', 'Tuple',
                'Any', 'Optional', 'Union', 'Type', 'String', 'Integer', 'Float',
                'GitHub', 'PyPI', 'API', 'HTTP', 'JSON', 'XML', 'CSV', 'SQL',
                'Linux', 'Windows', 'Mac', 'OS', 'CPU', 'GPU', 'RAM', 'Docker',
                'MIT', 'Apache', 'BSD', 'GPL', 'License', 'Open', 'Source'}

    libraries = {lib for lib in libraries if lib not in builtins and len(lib) > 2}

    return libraries

def parse_markdown_files(docs_dir: Path) -> Tuple[Dict, List]:
    """Parse all published markdown research files."""
    markdown_files = sorted(docs_dir.glob("1-*.md"))
    print(f"Found {len(markdown_files)} markdown files")

    research_topics = []
    all_libraries = defaultdict(lambda: {
        'name': '',
        'research_mentions': [],
        'source': 'markdown_parse'
    })

    for md_file in markdown_files:
        try:
            content = md_file.read_text()
            frontmatter = extract_frontmatter(content)

            research_id = frontmatter.get('id', md_file.stem)
            research_title = frontmatter.get('title', 'Unknown')

            # Extract library names from content
            libraries = extract_library_names(content)

            # Record research topic
            topic = {
                'id': research_id,
                'title': research_title,
                'libraries': sorted(list(libraries)),
                'source': str(md_file.name)
            }
            research_topics.append(topic)

            # Record library mentions
            for lib_name in libraries:
                all_libraries[lib_name]['name'] = lib_name
                all_libraries[lib_name]['research_mentions'].append({
                    'research_id': research_id,
                    'research_title': research_title
                })

        except Exception as e:
            print(f"Error parsing {md_file.name}: {e}")

    return dict(all_libraries), research_topics

def merge_with_existing(existing_file: Path, markdown_data: Dict) -> Dict:
    """Merge markdown-parsed data with existing metadata."""
    if not existing_file.exists():
        return markdown_data

    with open(existing_file) as f:
        existing = json.load(f)

    # Merge libraries
    existing_libs = existing.get('libraries', {})
    markdown_libs, markdown_topics = markdown_data

    for lib_name, lib_data in markdown_libs.items():
        if lib_name in existing_libs:
            # Merge mentions
            existing_libs[lib_name]['research_mentions'].extend(
                lib_data['research_mentions']
            )
        else:
            # Add new library
            existing_libs[lib_name] = lib_data

    # Update metadata
    existing['metadata']['num_libraries'] = len(existing_libs)
    existing['metadata']['sources'] = [
        'packages/research/ (structured YAML)',
        'docs/survey/ (markdown parsed)'
    ]

    # Add markdown research topics
    existing_topics = {t['id']: t for t in existing.get('research_topics', [])}
    for topic in markdown_topics:
        if topic['id'] not in existing_topics:
            existing['research_topics'].append(topic)

    existing['metadata']['num_research_topics'] = len(existing['research_topics'])

    return existing

def main():
    """Parse markdown files and merge with existing data."""
    docs_dir = Path(__file__).parent / "docs" / "survey"
    existing_file = Path(__file__).parent / "library-metadata.json"

    if not docs_dir.exists():
        print(f"Error: {docs_dir} not found")
        return

    print("Parsing markdown files...")
    markdown_libs, markdown_topics = parse_markdown_files(docs_dir)
    print(f"Parsed {len(markdown_libs)} libraries from markdown")

    print("\nMerging with existing metadata...")
    merged = merge_with_existing(
        existing_file,
        (markdown_libs, markdown_topics)
    )

    # Write merged output
    output_file = Path(__file__).parent / "library-metadata-merged.json"
    with open(output_file, 'w') as f:
        json.dump(merged, f, indent=2)

    print(f"\n✓ Wrote {output_file}")
    print(f"  - {merged['metadata']['num_libraries']} total libraries")
    print(f"  - {merged['metadata']['num_research_topics']} research topics")

    # Show sample of markdown-extracted libraries
    print("\nSample markdown-extracted libraries:")
    markdown_only = [name for name, data in merged['libraries'].items()
                     if data.get('source') == 'markdown_parse']
    for lib_name in sorted(markdown_only)[:10]:
        lib = merged['libraries'][lib_name]
        mentions = len(lib['research_mentions'])
        print(f"  {lib_name} (mentioned in {mentions} topics)")

if __name__ == '__main__':
    main()
