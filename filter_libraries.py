#!/usr/bin/env python3
"""
Filter extracted libraries to remove noise and false positives.

Strategy: Keep libraries that appear in multiple research topics
or match known Python library naming patterns.
"""

import json
import re
from pathlib import Path
from collections import Counter

def is_likely_library(name: str, mention_count: int) -> bool:
    """
    Determine if a name is likely a real library.

    Criteria:
    - Mentioned in 2+ research topics (high confidence)
    - OR matches common Python library patterns
    - AND doesn't match exclusion patterns
    """
    # Exclude obvious false positives
    exclusions = {
        # Command-line flags
        r'^--',
        # Single uppercase letters or short acronyms
        r'^[A-Z]{1,2}$',
        # All caps words (likely acronyms not libraries)
        r'^[A-Z]+$',
        # Common words
        r'^(True|False|None|Optional|List|Dict|Set|Type|String|Any|Union)$',
        # Status words
        r'^(ABANDONED|ACCEPTABLE|ADAPT|GOOD|BEST|RECOMMENDED)$',
        # Numbers
        r'^\d+$',
        # Very short
        r'^.{1,2}$'
    }

    for pattern in exclusions:
        if re.match(pattern, name):
            return False

    # High confidence: mentioned in multiple topics
    if mention_count >= 2:
        return True

    # Library naming patterns
    library_patterns = [
        # lowercase with optional underscores/hyphens
        r'^[a-z][a-z0-9_\-]*$',
        # CamelCase starting with uppercase (many Python libs)
        r'^[A-Z][a-z]+[A-Z][a-z]+',
        # Common library suffixes
        r'.*(?:py|lib|kit|tools|utils)$',
    ]

    for pattern in library_patterns:
        if re.match(pattern, name, re.IGNORECASE):
            # Additional check: reasonable length
            if 3 <= len(name) <= 30:
                return True

    return False

def filter_libraries(data: dict) -> dict:
    """Filter out low-quality library extractions."""
    libraries = data.get('libraries', {})

    # Count mentions per library
    mention_counts = {
        name: len(lib_data.get('research_mentions', []))
        for name, lib_data in libraries.items()
    }

    # Filter
    filtered = {}
    removed = []

    for name, lib_data in libraries.items():
        mention_count = mention_counts[name]

        if is_likely_library(name, mention_count):
            filtered[name] = lib_data
        else:
            removed.append(name)

    # Update data
    data['libraries'] = filtered
    data['metadata']['num_libraries'] = len(filtered)
    data['metadata']['filtering'] = {
        'removed_count': len(removed),
        'kept_count': len(filtered),
        'criteria': 'mention_count >= 2 OR matches library naming patterns'
    }

    return data, removed

def print_statistics(data: dict):
    """Print statistics about the filtered data."""
    libraries = data['libraries']

    # Count mentions
    mention_counts = Counter()
    for lib_data in libraries.values():
        count = len(lib_data.get('research_mentions', []))
        mention_counts[count] += 1

    print("\nLibrary mention distribution:")
    for count in sorted(mention_counts.keys(), reverse=True)[:10]:
        print(f"  {count} mentions: {mention_counts[count]} libraries")

    # Sample well-connected libraries
    print("\nMost-mentioned libraries:")
    by_mentions = sorted(
        libraries.items(),
        key=lambda x: len(x[1].get('research_mentions', [])),
        reverse=True
    )

    for name, lib_data in by_mentions[:15]:
        mentions = len(lib_data.get('research_mentions', []))
        categories = lib_data.get('categories', [])
        tags = lib_data.get('tags', [])
        cat_str = ', '.join(categories[:2]) if categories else '(from markdown)'
        print(f"  {name:20} - {mentions:2} mentions - {cat_str}")

def main():
    """Filter the merged library metadata."""
    input_file = Path(__file__).parent / "library-metadata-merged.json"

    if not input_file.exists():
        print(f"Error: {input_file} not found")
        print("Run parse_markdown_research.py first")
        return

    with open(input_file) as f:
        data = json.load(f)

    print(f"Before filtering: {len(data['libraries'])} libraries")

    filtered_data, removed = filter_libraries(data)

    print(f"After filtering: {len(filtered_data['libraries'])} libraries")
    print(f"Removed: {len(removed)} false positives")

    # Write filtered output
    output_file = Path(__file__).parent / "library-metadata-filtered.json"
    with open(output_file, 'w') as f:
        json.dump(filtered_data, f, indent=2)

    print(f"\n✓ Wrote {output_file}")

    print_statistics(filtered_data)

if __name__ == '__main__':
    main()
