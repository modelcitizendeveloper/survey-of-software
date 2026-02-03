#!/usr/bin/env python3
"""
Train library embeddings using Word2Vec approach.

Treats research topics as "sentences" where libraries are "words".
Libraries appearing in the same research topic are treated as co-occurring
in a context window.
"""

import json
import numpy as np
from pathlib import Path
from typing import List, Dict
from gensim.models import Word2Vec

def load_research_topics(metadata_file: Path) -> List[List[str]]:
    """
    Load research topics as "sentences" for Word2Vec.

    Each research topic becomes a list of libraries (a sentence).
    """
    with open(metadata_file) as f:
        data = json.load(f)

    sentences = []
    for topic in data['research_topics']:
        libraries = topic.get('libraries', [])
        if len(libraries) >= 2:  # Need at least 2 for co-occurrence
            sentences.append(libraries)

    return sentences

def train_word2vec(sentences: List[List[str]], vector_size: int = 100,
                  window: int = 10, min_count: int = 2) -> Word2Vec:
    """
    Train Word2Vec model on library "sentences".

    Parameters:
        vector_size: Dimensionality of embeddings (50, 100, 300)
        window: Context window size (how many libraries around are context)
        min_count: Minimum occurrence count to include library
    """
    model = Word2Vec(
        sentences=sentences,
        vector_size=vector_size,
        window=window,
        min_count=min_count,
        workers=4,
        sg=1,  # Skip-gram (better for small datasets)
        epochs=100,
        seed=42
    )

    return model

def evaluate_model(model: Word2Vec):
    """Print evaluation metrics and examples."""
    vocab_size = len(model.wv)
    print(f"\nModel vocabulary: {vocab_size} libraries")

    # Test nearest neighbors
    print("\n=== Nearest Neighbors ===")
    test_libraries = ['numpy', 'pandas', 'torch', 'fastapi', 'requests']

    for lib in test_libraries:
        if lib in model.wv:
            print(f"\n{lib}:")
            similar = model.wv.most_similar(lib, topn=10)
            for similar_lib, score in similar:
                print(f"  {score:.3f}  {similar_lib}")
        else:
            print(f"\n{lib}: (not in vocabulary)")

    # Test analogies
    print("\n=== Library Analogies ===")
    analogies = [
        # requests - sync + async = ?
        ('requests', 'threading', 'asyncio'),
        # numpy - arrays + dataframes = ?
        ('numpy', 'array', 'pandas'),
        # torch - training + inference = ?
        ('torch', 'training', 'onnxruntime'),
    ]

    for positive1, negative, positive2 in analogies:
        try:
            if all(w in model.wv for w in [positive1, negative, positive2]):
                result = model.wv.most_similar(
                    positive=[positive1, positive2],
                    negative=[negative],
                    topn=5
                )
                print(f"\n{positive1} - {negative} + {positive2} = ?")
                for lib, score in result:
                    print(f"  {score:.3f}  {lib}")
        except Exception as e:
            print(f"\n{positive1} - {negative} + {positive2}: (error: {e})")

def save_embeddings(model: Word2Vec, output_dir: Path):
    """Save embeddings in multiple formats."""
    output_dir.mkdir(parents=True, exist_ok=True)

    # Format 1: NumPy arrays
    vocab = list(model.wv.index_to_key)
    vectors = np.array([model.wv[word] for word in vocab])

    np.save(output_dir / "embeddings.npy", vectors)
    with open(output_dir / "vocabulary.json", 'w') as f:
        json.dump(vocab, f, indent=2)

    print(f"  - embeddings.npy: {vectors.shape}")
    print(f"  - vocabulary.json: {len(vocab)} libraries")

    # Format 2: Gensim model
    model.save(str(output_dir / "word2vec.model"))
    print(f"  - word2vec.model (gensim format)")

    # Format 3: Word2Vec text format (for compatibility)
    model.wv.save_word2vec_format(str(output_dir / "embeddings.txt"))
    print(f"  - embeddings.txt (word2vec format)")

def train_multiple_dimensions(sentences: List[List[str]], output_base: Path):
    """Train models with different embedding dimensions."""
    dimensions = [50, 100, 300]

    results = {}

    for dim in dimensions:
        print(f"\n{'='*60}")
        print(f"Training {dim}-dimensional embeddings...")
        print(f"{'='*60}")

        model = train_word2vec(sentences, vector_size=dim)
        evaluate_model(model)

        output_dir = output_base / f"embeddings_{dim}d"
        print(f"\nSaving {dim}d embeddings to {output_dir}/...")
        save_embeddings(model, output_dir)

        results[dim] = {
            'vocab_size': len(model.wv),
            'vector_size': dim,
            'output_dir': str(output_dir)
        }

    return results

def main():
    """Train library embeddings."""
    metadata_file = Path(__file__).parent / "library-metadata-clean.json"
    output_base = Path(__file__).parent / "embeddings"

    if not metadata_file.exists():
        print(f"Error: {metadata_file} not found")
        return

    print("Loading research topics...")
    sentences = load_research_topics(metadata_file)
    print(f"  - {len(sentences)} research topics (sentences)")
    print(f"  - {sum(len(s) for s in sentences)} total library mentions")
    print(f"  - Avg {sum(len(s) for s in sentences) / len(sentences):.1f} libraries per topic")

    # Train models with different dimensions
    results = train_multiple_dimensions(sentences, output_base)

    # Save training summary
    summary_file = output_base / "training_summary.json"
    with open(summary_file, 'w') as f:
        json.dump({
            'num_topics': len(sentences),
            'models': results,
            'training_params': {
                'window': 10,
                'min_count': 2,
                'sg': 1,
                'epochs': 100
            }
        }, f, indent=2)

    print(f"\n✓ Training complete! Summary saved to {summary_file}")

if __name__ == '__main__':
    main()
