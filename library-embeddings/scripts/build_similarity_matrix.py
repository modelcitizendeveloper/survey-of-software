#!/usr/bin/env python3
"""
Build library similarity matrices from Survey of Software metadata.

Computes pairwise similarity using multiple signals:
1. Co-occurrence in research topics
2. Tag/category overlap (for structured metadata)
3. Algorithm support overlap

Outputs similarity matrices and co-occurrence pairs for embeddings training.
"""

import json
import numpy as np
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Tuple, Set
from itertools import combinations

def load_library_data(file_path: Path) -> Tuple[Dict, List]:
    """Load library metadata and research topics."""
    with open(file_path) as f:
        data = json.load(f)

    return data['libraries'], data['research_topics']

def build_co_occurrence_matrix(libraries: Dict, research_topics: List) -> Tuple[np.ndarray, List[str], List[Tuple]]:
    """
    Build co-occurrence matrix: how often libraries appear together in research.

    Returns:
        - matrix: NxN matrix of co-occurrence counts
        - lib_names: ordered list of library names
        - pairs: list of (lib1, lib2, count) tuples for embeddings training
    """
    # Get library names sorted
    lib_names = sorted(libraries.keys())
    n = len(lib_names)
    lib_to_idx = {name: i for i, name in enumerate(lib_names)}

    # Initialize matrix
    cooccurrence = np.zeros((n, n), dtype=int)

    # Count co-occurrences
    pairs_count = defaultdict(int)

    for topic in research_topics:
        topic_libs = topic.get('libraries', [])

        # All pairs in this topic co-occur
        for lib1, lib2 in combinations(topic_libs, 2):
            if lib1 in lib_to_idx and lib2 in lib_to_idx:
                i, j = lib_to_idx[lib1], lib_to_idx[lib2]
                cooccurrence[i, j] += 1
                cooccurrence[j, i] += 1  # Symmetric

                # Track pairs for embeddings
                pair = tuple(sorted([lib1, lib2]))
                pairs_count[pair] += 1

    # Convert pairs to list
    pairs = [(lib1, lib2, count) for (lib1, lib2), count in pairs_count.items()]
    pairs.sort(key=lambda x: x[2], reverse=True)

    return cooccurrence, lib_names, pairs

def compute_jaccard_similarity(set1: Set, set2: Set) -> float:
    """Jaccard similarity: |A ∩ B| / |A ∪ B|"""
    if not set1 and not set2:
        return 0.0
    intersection = len(set1 & set2)
    union = len(set1 | set2)
    return intersection / union if union > 0 else 0.0

def build_tag_similarity_matrix(libraries: Dict, lib_names: List[str]) -> np.ndarray:
    """Build similarity matrix based on tag/category overlap."""
    n = len(lib_names)
    tag_similarity = np.zeros((n, n), dtype=float)

    for i, lib1 in enumerate(lib_names):
        tags1 = set(libraries[lib1].get('tags', []))
        cats1 = set(libraries[lib1].get('categories', []))
        features1 = tags1 | cats1

        for j, lib2 in enumerate(lib_names):
            if i == j:
                tag_similarity[i, j] = 1.0
                continue

            tags2 = set(libraries[lib2].get('tags', []))
            cats2 = set(libraries[lib2].get('categories', []))
            features2 = tags2 | cats2

            similarity = compute_jaccard_similarity(features1, features2)
            tag_similarity[i, j] = similarity

    return tag_similarity

def build_algorithm_similarity_matrix(libraries: Dict, lib_names: List[str]) -> np.ndarray:
    """Build similarity matrix based on algorithm support overlap."""
    n = len(lib_names)
    algo_similarity = np.zeros((n, n), dtype=float)

    for i, lib1 in enumerate(lib_names):
        algos1 = set(libraries[lib1].get('algorithms', []))

        for j, lib2 in enumerate(lib_names):
            if i == j:
                algo_similarity[i, j] = 1.0
                continue

            algos2 = set(libraries[lib2].get('algorithms', []))
            similarity = compute_jaccard_similarity(algos1, algos2)
            algo_similarity[i, j] = similarity

    return algo_similarity

def normalize_matrix(matrix: np.ndarray) -> np.ndarray:
    """Normalize matrix to [0, 1] range."""
    max_val = matrix.max()
    if max_val > 0:
        return matrix / max_val
    return matrix

def save_matrices(output_dir: Path, lib_names: List[str], **matrices):
    """Save matrices and library names."""
    output_dir.mkdir(exist_ok=True)

    # Save library names
    with open(output_dir / "library_names.json", 'w') as f:
        json.dump(lib_names, f, indent=2)

    # Save each matrix
    for name, matrix in matrices.items():
        np.save(output_dir / f"{name}.npy", matrix)
        print(f"  - Saved {name}.npy ({matrix.shape})")

def print_top_pairs(pairs: List[Tuple], n: int = 20):
    """Print top co-occurring library pairs."""
    print(f"\nTop {n} co-occurring library pairs:")
    for lib1, lib2, count in pairs[:n]:
        print(f"  {count:2}x  {lib1:20} + {lib2}")

def print_similar_libraries(lib_names: List[str], similarity_matrix: np.ndarray,
                           target_lib: str, n: int = 10):
    """Print most similar libraries to target."""
    if target_lib not in lib_names:
        print(f"Library '{target_lib}' not found")
        return

    idx = lib_names.index(target_lib)
    similarities = similarity_matrix[idx]

    # Sort by similarity (excluding self)
    similar_indices = np.argsort(similarities)[::-1]
    similar_indices = [i for i in similar_indices if i != idx][:n]

    print(f"\nMost similar to '{target_lib}':")
    for i in similar_indices:
        sim_score = similarities[i]
        if sim_score > 0:
            print(f"  {sim_score:.3f}  {lib_names[i]}")

def main():
    """Build and save similarity matrices."""
    input_file = Path(__file__).parent / "library-metadata-clean.json"
    output_dir = Path(__file__).parent / "similarity_matrices"

    if not input_file.exists():
        print(f"Error: {input_file} not found")
        return

    print("Loading library data...")
    libraries, research_topics = load_library_data(input_file)
    print(f"  - {len(libraries)} libraries")
    print(f"  - {len(research_topics)} research topics")

    print("\nBuilding co-occurrence matrix...")
    cooccurrence, lib_names, pairs = build_co_occurrence_matrix(libraries, research_topics)
    cooccurrence_norm = normalize_matrix(cooccurrence)
    print(f"  - Found {len(pairs)} library pairs")
    print(f"  - Max co-occurrence: {cooccurrence.max()}")

    print("\nBuilding tag similarity matrix...")
    tag_similarity = build_tag_similarity_matrix(libraries, lib_names)
    non_zero_tags = (tag_similarity > 0).sum() - len(lib_names)  # Exclude diagonal
    print(f"  - {non_zero_tags} non-zero similarities")

    print("\nBuilding algorithm similarity matrix...")
    algo_similarity = build_algorithm_similarity_matrix(libraries, lib_names)
    non_zero_algos = (algo_similarity > 0).sum() - len(lib_names)
    print(f"  - {non_zero_algos} non-zero similarities")

    # Save all matrices
    print(f"\nSaving matrices to {output_dir}/...")
    save_matrices(
        output_dir,
        lib_names,
        cooccurrence=cooccurrence,
        cooccurrence_normalized=cooccurrence_norm,
        tag_similarity=tag_similarity,
        algorithm_similarity=algo_similarity
    )

    # Save co-occurrence pairs (for embeddings training)
    pairs_file = output_dir / "cooccurrence_pairs.json"
    with open(pairs_file, 'w') as f:
        json.dump([
            {'library1': lib1, 'library2': lib2, 'count': count}
            for lib1, lib2, count in pairs
        ], f, indent=2)
    print(f"  - Saved cooccurrence_pairs.json ({len(pairs)} pairs)")

    # Print interesting results
    print_top_pairs(pairs, n=20)

    # Example similarity queries
    for lib in ['numpy', 'pandas', 'torch', 'requests', 'fastapi']:
        if lib in lib_names:
            print_similar_libraries(lib_names, cooccurrence_norm, lib, n=10)

    print(f"\n✓ Done! Matrices saved to {output_dir}/")

if __name__ == '__main__':
    main()
