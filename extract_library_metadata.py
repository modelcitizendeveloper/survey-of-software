#!/usr/bin/env python3
"""
Extract library metadata from Survey of Software research packages.

Parses metadata.yaml files from packages/research/*/ and consolidates
into a structured JSON file for embeddings training.
"""

import json
import yaml
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Any

def load_metadata_files(base_dir: Path) -> List[Dict[str, Any]]:
    """Load all metadata.yaml files from research packages."""
    metadata_files = list(base_dir.glob("*/metadata.yaml"))
    print(f"Found {len(metadata_files)} metadata.yaml files")

    all_metadata = []
    for yaml_file in sorted(metadata_files):
        try:
            with open(yaml_file) as f:
                data = yaml.safe_load(f)
                if data:
                    data['_source_file'] = str(yaml_file.relative_to(base_dir))
                    all_metadata.append(data)
        except Exception as e:
            print(f"Error loading {yaml_file}: {e}")

    return all_metadata

def extract_libraries(metadata_list: List[Dict]) -> Dict[str, Dict]:
    """Extract unique libraries with their metadata."""
    libraries = {}

    for research in metadata_list:
        research_id = research.get('id') or research.get('code') or research.get('experiment', {}).get('id', 'unknown')
        research_title = research.get('title', 'Unknown')

        # Extract from libraries_evaluated field
        libs_evaluated = research.get('libraries_evaluated', [])
        for lib in libs_evaluated:
            lib_name = lib.get('name')
            if not lib_name:
                continue

            if lib_name not in libraries:
                libraries[lib_name] = {
                    'name': lib_name,
                    'research_mentions': [],
                    'tags': set(),
                    'categories': set(),
                    'use_cases': [],
                    'algorithms': [],
                    'metadata': {}
                }

            # Add research mention
            libraries[lib_name]['research_mentions'].append({
                'research_id': research_id,
                'research_title': research_title,
                'recommendation': lib.get('recommendation'),
                'primary_use': lib.get('primary_use')
            })

            # Add metadata
            for key in ['stars', 'license', 'downloads_monthly', 'performance', 'language']:
                if key in lib:
                    libraries[lib_name]['metadata'][key] = lib[key]

        # Add tags from research
        tags = research.get('tags', [])
        for lib_name in [l.get('name') for l in libs_evaluated if l.get('name')]:
            if lib_name in libraries:
                libraries[lib_name]['tags'].update(tags)

        # Add categories
        category = research.get('category')
        cluster = research.get('cluster')
        for lib_name in [l.get('name') for l in libs_evaluated if l.get('name')]:
            if lib_name in libraries:
                if category:
                    libraries[lib_name]['categories'].add(category)
                if cluster:
                    libraries[lib_name]['categories'].add(cluster)

        # Add use cases
        use_cases = research.get('use_cases', [])
        for lib_name in [l.get('name') for l in libs_evaluated if l.get('name')]:
            if lib_name in libraries:
                for uc in use_cases:
                    if uc.get('library_recommendation') == lib_name:
                        libraries[lib_name]['use_cases'].append({
                            'persona': uc.get('persona'),
                            'need': uc.get('primary_need')
                        })

        # Add algorithm support
        algo_support = research.get('algorithm_support', {})
        for algo, supporting_libs in algo_support.items():
            for lib_name in supporting_libs:
                if lib_name in libraries:
                    libraries[lib_name]['algorithms'].append(algo)

    # Convert sets to lists for JSON serialization
    for lib in libraries.values():
        lib['tags'] = sorted(list(lib['tags']))
        lib['categories'] = sorted(list(lib['categories']))
        lib['algorithms'] = sorted(list(set(lib['algorithms'])))

    return libraries

def build_research_graph(metadata_list: List[Dict]) -> Dict[str, List[str]]:
    """Build graph of related research topics."""
    graph = {}

    for research in metadata_list:
        research_id = research.get('id') or research.get('code') or research.get('experiment', {}).get('id')
        if not research_id:
            continue

        related = research.get('related_research', [])
        graph[research_id] = related

    return graph

def extract_research_metadata(metadata_list: List[Dict]) -> List[Dict]:
    """Extract research topic metadata."""
    research_topics = []

    for research in metadata_list:
        research_id = research.get('id') or research.get('code') or research.get('experiment', {}).get('id', 'unknown')

        topic = {
            'id': research_id,
            'title': research.get('title', 'Unknown'),
            'category': research.get('category'),
            'cluster': research.get('cluster'),
            'tags': research.get('tags', []),
            'libraries': [lib.get('name') for lib in research.get('libraries_evaluated', []) if lib.get('name')],
            'related_research': research.get('related_research', []),
            'key_findings': research.get('key_findings', [])
        }

        research_topics.append(topic)

    return research_topics

def main():
    """Extract and consolidate library metadata."""
    base_dir = Path(__file__).parent / "packages" / "research"

    if not base_dir.exists():
        print(f"Error: {base_dir} not found")
        return

    print("Loading metadata files...")
    metadata_list = load_metadata_files(base_dir)

    print("Extracting libraries...")
    libraries = extract_libraries(metadata_list)
    print(f"Found {len(libraries)} unique libraries")

    print("Building research graph...")
    research_graph = build_research_graph(metadata_list)
    print(f"Found {len(research_graph)} research topics with relations")

    print("Extracting research metadata...")
    research_topics = extract_research_metadata(metadata_list)

    # Consolidate output
    output = {
        'metadata': {
            'source': 'Survey of Software - packages/research/',
            'num_libraries': len(libraries),
            'num_research_topics': len(research_topics),
            'extraction_date': '2026-02-02'
        },
        'libraries': libraries,
        'research_topics': research_topics,
        'research_graph': research_graph
    }

    # Write output
    output_file = Path(__file__).parent / "library-metadata.json"
    with open(output_file, 'w') as f:
        json.dump(output, f, indent=2)

    print(f"\n✓ Wrote {output_file}")
    print(f"  - {len(libraries)} libraries")
    print(f"  - {len(research_topics)} research topics")
    print(f"  - {sum(len(v) for v in research_graph.values())} research relations")

    # Print sample
    print("\nSample libraries:")
    for lib_name in sorted(libraries.keys())[:5]:
        lib = libraries[lib_name]
        print(f"  {lib_name}")
        print(f"    - Categories: {', '.join(lib['categories'][:3])}")
        print(f"    - Tags: {', '.join(lib['tags'][:3])}")
        print(f"    - Mentioned in {len(lib['research_mentions'])} research topics")

if __name__ == '__main__':
    main()
