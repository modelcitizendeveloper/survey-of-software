#!/usr/bin/env python3
"""
Validate library embeddings against Libraries.io dependency data.

Hypothesis: Libraries with similar embeddings should have similar dependency patterns.

Uses Libraries.io API (60 req/min limit).
"""

import json
import time
import os
from pathlib import Path
from typing import Dict, List, Optional
import numpy as np
from gensim.models import Word2Vec

# Libraries.io API base
LIBRARIESIO_API_BASE = "https://libraries.io/api"

def get_api_key() -> Optional[str]:
    """Get Libraries.io API key from environment."""
    key = os.environ.get('LIBRARIESIO_API_KEY')
    if not key:
        print("WARNING: LIBRARIESIO_API_KEY not set in environment")
        print("Get a key at: https://libraries.io/api")
        print("Then: export LIBRARIESIO_API_KEY=your_key")
    return key

def fetch_package_info(package_name: str, platform: str = "pypi", api_key: str = None) -> Optional[Dict]:
    """Fetch package info from Libraries.io API."""
    if not api_key:
        return None

    import requests

    url = f"{LIBRARIESIO_API_BASE}/{platform}/{package_name}"
    params = {'api_key': api_key}

    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            print(f"  - {package_name}: not found on PyPI")
            return None
        elif response.status_code == 429:
            print(f"  - Rate limit hit, sleeping 60s...")
            time.sleep(60)
            return fetch_package_info(package_name, platform, api_key)  # Retry
        else:
            print(f"  - {package_name}: HTTP {response.status_code}")
            return None
    except Exception as e:
        print(f"  - {package_name}: error: {e}")
        return None

def fetch_dependencies(package_name: str, api_key: str) -> Optional[List[str]]:
    """Fetch dependencies for a package."""
    import requests

    url = f"{LIBRARIESIO_API_BASE}/pypi/{package_name}/latest/dependencies"
    params = {'api_key': api_key}

    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            # Extract dependency names
            deps = [dep['project_name'] for dep in data.get('dependencies', [])]
            return deps
        elif response.status_code == 404:
            return []
        elif response.status_code == 429:
            print(f"  - Rate limit, sleeping...")
            time.sleep(60)
            return fetch_dependencies(package_name, api_key)
        else:
            return []
    except Exception as e:
        print(f"  - Error fetching deps for {package_name}: {e}")
        return []

def load_embeddings(embeddings_dir: Path) -> Word2Vec:
    """Load trained Word2Vec model."""
    model_path = embeddings_dir / "embeddings_100d" / "word2vec.model"
    return Word2Vec.load(str(model_path))

def calculate_dependency_overlap(deps1: List[str], deps2: List[str]) -> float:
    """Calculate Jaccard similarity of dependency sets."""
    if not deps1 and not deps2:
        return 0.0
    set1, set2 = set(deps1), set(deps2)
    intersection = len(set1 & set2)
    union = len(set1 | set2)
    return intersection / union if union > 0 else 0.0

def validate_sample(model: Word2Vec, api_key: str, sample_size: int = 30):
    """Validate embeddings against Libraries.io for a sample of libraries."""
    print(f"\n{'='*70}")
    print(f"VALIDATION: Library Embeddings vs Libraries.io Dependencies")
    print(f"{'='*70}")

    # Sample libraries from vocabulary
    vocab = list(model.wv.index_to_key)
    # Prioritize libraries likely to be on PyPI (lowercase, not Python builtins)
    pypi_likely = [lib for lib in vocab
                   if lib.islower()
                   and lib not in {'abc', 'enum', 'time', 'inspect', 'contextlib'}]

    sample = pypi_likely[:min(sample_size, len(pypi_likely))]

    print(f"\nSampling {len(sample)} libraries from vocabulary...")
    print(f"Rate limit: 60 req/min, estimated time: {len(sample)/60:.1f} minutes")

    # Fetch dependency data
    dep_data = {}
    for i, lib in enumerate(sample, 1):
        print(f"\n[{i}/{len(sample)}] Fetching {lib}...")
        deps = fetch_dependencies(lib, api_key)
        if deps is not None:
            dep_data[lib] = deps
            print(f"  - Found {len(deps)} dependencies")

        # Respect rate limit
        if i < len(sample):
            time.sleep(1.1)  # ~55 req/min to be safe

    # Calculate correlations
    print(f"\n{'='*70}")
    print(f"CORRELATION ANALYSIS")
    print(f"{'='*70}")

    results = []

    # For each pair of libraries, compare:
    # 1. Embedding similarity (cosine)
    # 2. Dependency overlap (Jaccard)

    libs_with_deps = [lib for lib in sample if lib in dep_data]
    print(f"\nFound dependency data for {len(libs_with_deps)} libraries")

    for i, lib1 in enumerate(libs_with_deps):
        for lib2 in libs_with_deps[i+1:]:
            if lib1 in model.wv and lib2 in model.wv:
                emb_sim = model.wv.similarity(lib1, lib2)
                dep_overlap = calculate_dependency_overlap(dep_data[lib1], dep_data[lib2])

                results.append({
                    'lib1': lib1,
                    'lib2': lib2,
                    'embedding_similarity': float(emb_sim),
                    'dependency_overlap': float(dep_overlap),
                    'deps1_count': len(dep_data[lib1]),
                    'deps2_count': len(dep_data[lib2])
                })

    # Calculate Pearson correlation
    if results:
        emb_sims = np.array([r['embedding_similarity'] for r in results])
        dep_overlaps = np.array([r['dependency_overlap'] for r in results])

        correlation = np.corrcoef(emb_sims, dep_overlaps)[0, 1]

        print(f"\nPearson correlation: {correlation:.3f}")
        print(f"Sample size: {len(results)} library pairs")

        # Show top correlated pairs
        print(f"\nTop 10 pairs by embedding similarity:")
        sorted_results = sorted(results, key=lambda x: x['embedding_similarity'], reverse=True)
        for r in sorted_results[:10]:
            print(f"  {r['embedding_similarity']:.3f} emb, {r['dependency_overlap']:.3f} dep: "
                  f"{r['lib1']} ↔ {r['lib2']}")

        # Show pairs with high dep overlap but low emb similarity (anomalies)
        print(f"\nAnomalies (high dep overlap, low emb similarity):")
        anomalies = [r for r in results
                     if r['dependency_overlap'] > 0.5 and r['embedding_similarity'] < 0.9]
        for r in sorted(anomalies, key=lambda x: x['dependency_overlap'], reverse=True)[:5]:
            print(f"  {r['embedding_similarity']:.3f} emb, {r['dependency_overlap']:.3f} dep: "
                  f"{r['lib1']} ↔ {r['lib2']}")

        # Save results
        output_file = Path(__file__).parent / "librariesio_validation_results.json"
        with open(output_file, 'w') as f:
            json.dump({
                'correlation': float(correlation),
                'sample_size': len(results),
                'pairs': results,
                'summary': {
                    'mean_embedding_similarity': float(emb_sims.mean()),
                    'mean_dependency_overlap': float(dep_overlaps.mean()),
                    'std_embedding_similarity': float(emb_sims.std()),
                    'std_dependency_overlap': float(dep_overlaps.std())
                }
            }, f, indent=2)

        print(f"\n✓ Results saved to {output_file}")

    else:
        print("\nNo valid pairs to analyze")

    return results

def main():
    """Run validation."""
    api_key = get_api_key()
    if not api_key:
        print("\nTo run validation, set Libraries.io API key:")
        print("  export LIBRARIESIO_API_KEY=your_key_here")
        print("\nGet a key at: https://libraries.io/api")
        return

    embeddings_dir = Path(__file__).parent / "embeddings"
    if not embeddings_dir.exists():
        print(f"Error: {embeddings_dir} not found")
        print("Run train_embeddings.py first")
        return

    print("Loading embeddings...")
    model = load_embeddings(embeddings_dir)
    print(f"Loaded {len(model.wv)} library embeddings")

    # Run validation on sample
    validate_sample(model, api_key, sample_size=30)

    print(f"\n{'='*70}")
    print("Validation complete!")
    print(f"{'='*70}")

if __name__ == '__main__':
    main()
