#!/usr/bin/env python3
"""
Explore library embeddings - analogies, nearest neighbors, visualizations.

Answer the question: what's the king-man+woman=queen of Python libraries?
"""

import json
import numpy as np
from pathlib import Path
from gensim.models import Word2Vec

def load_model(model_dir: Path) -> Word2Vec:
    """Load trained Word2Vec model."""
    model_file = model_dir / "word2vec.model"
    return Word2Vec.load(str(model_file))

def test_analogies(model: Word2Vec):
    """Test interesting library analogies."""
    print("=" * 70)
    print("LIBRARY ANALOGIES (king - man + woman = queen style)")
    print("=" * 70)

    analogies = [
        # Sync to async
        {
            'name': 'Sync → Async Web Framework',
            'formula': 'requests - sync + async',
            'positive': ['requests', 'asyncio'],
            'negative': ['threading'],
            'expected': 'httpx or aiohttp'
        },
        {
            'name': 'Sync → Async HTTP',
            'formula': 'requests - urllib + asyncio',
            'positive': ['requests', 'asyncio'],
            'negative': ['urllib'],
            'expected': 'httpx or aiohttp'
        },
        # Array → DataFrame
        {
            'name': 'Arrays → DataFrames',
            'formula': 'numpy - arrays + dataframes',
            'positive': ['numpy', 'pandas'],
            'negative': ['array'],
            'expected': 'pandas'
        },
        # Training → Inference
        {
            'name': 'Training → Inference',
            'formula': 'torch - training + inference',
            'positive': ['torch', 'onnxruntime'],
            'negative': ['transformers'],
            'expected': 'onnx or onnxruntime'
        },
        # Web framework variations
        {
            'name': 'Flask → FastAPI (modern async)',
            'formula': 'flask - sync + async',
            'positive': ['flask', 'asyncio'],
            'negative': ['threading'],
            'expected': 'fastapi'
        },
        # Data viz
        {
            'name': 'Basic → Interactive Plots',
            'formula': 'matplotlib - static + interactive',
            'positive': ['matplotlib', 'plotly'],
            'negative': ['scipy'],
            'expected': 'plotly or dash'
        },
        # NLP domain
        {
            'name': 'General NLP → Transformers',
            'formula': 'spacy - rules + transformers',
            'positive': ['spacy', 'transformers'],
            'negative': ['regex'],
            'expected': 'transformers-based'
        },
    ]

    for i, analogy in enumerate(analogies, 1):
        print(f"\n{i}. {analogy['name']}")
        print(f"   Formula: {analogy['formula']}")
        print(f"   Expected: {analogy['expected']}")

        positive = analogy['positive']
        negative = analogy['negative']

        # Check if all terms exist
        missing = [w for w in positive + negative if w not in model.wv]
        if missing:
            print(f"   Result: ❌ Missing terms: {missing}")
            continue

        try:
            results = model.wv.most_similar(
                positive=positive,
                negative=negative,
                topn=5
            )
            print(f"   Result:")
            for lib, score in results:
                print(f"     {score:.3f}  {lib}")

        except Exception as e:
            print(f"   Result: ❌ Error: {e}")

def nearest_neighbors_exploration(model: Word2Vec):
    """Explore nearest neighbors for interesting libraries."""
    print("\n" + "=" * 70)
    print("NEAREST NEIGHBORS - Library Similarity")
    print("=" * 70)

    categories = {
        'Popular general libs': ['numpy', 'pandas', 'requests'],
        'ML/DL frameworks': ['torch', 'tensorflow', 'transformers'],
        'Web frameworks': ['fastapi', 'flask', 'django'],
        'Data viz': ['matplotlib', 'plotly', 'dash'],
        'NLP': ['spacy', 'nltk', 'transformers'],
        'Async': ['asyncio', 'aiohttp', 'trio'],
    }

    for category, libs in categories.items():
        print(f"\n{category}:")
        for lib in libs:
            if lib in model.wv:
                similar = model.wv.most_similar(lib, topn=5)
                similar_str = ', '.join([f"{s[0]}({s[1]:.2f})" for s in similar[:3]])
                print(f"  {lib:15} → {similar_str}")
            else:
                print(f"  {lib:15} → (not in vocabulary)")

def cluster_analysis(model: Word2Vec):
    """Identify library clusters."""
    print("\n" + "=" * 70)
    print("CLUSTER ANALYSIS")
    print("=" * 70)

    # High-level seeds for different ecosystems
    seeds = {
        'Data Science': ['pandas', 'numpy', 'scipy'],
        'Machine Learning': ['torch', 'tensorflow', 'transformers'],
        'Web Development': ['fastapi', 'flask', 'requests'],
        'NLP': ['spacy', 'nltk', 'jieba'],
        'Async/Concurrent': ['asyncio', 'celery', 'redis'],
    }

    print("\nLibraries closest to each ecosystem:")
    for ecosystem, seed_libs in seeds.items():
        # Find libraries in vocabulary
        valid_seeds = [lib for lib in seed_libs if lib in model.wv]
        if not valid_seeds:
            continue

        print(f"\n{ecosystem} (seeds: {', '.join(valid_seeds)}):")

        # Get average vector of seeds
        seed_vectors = [model.wv[lib] for lib in valid_seeds]
        avg_vector = np.mean(seed_vectors, axis=0)

        # Find closest libraries to this centroid
        similarities = []
        for lib in model.wv.index_to_key:
            if lib not in valid_seeds:
                sim = np.dot(avg_vector, model.wv[lib]) / (
                    np.linalg.norm(avg_vector) * np.linalg.norm(model.wv[lib])
                )
                similarities.append((lib, sim))

        similarities.sort(key=lambda x: x[1], reverse=True)
        top_10 = similarities[:10]
        for lib, sim in top_10:
            print(f"  {sim:.3f}  {lib}")

def interesting_distances(model: Word2Vec):
    """Calculate interesting library distances."""
    print("\n" + "=" * 70)
    print("INTERESTING COMPARISONS")
    print("=" * 70)

    comparisons = [
        ('numpy', 'pandas', 'Array lib vs DataFrame lib'),
        ('torch', 'tensorflow', 'PyTorch vs TensorFlow'),
        ('fastapi', 'flask', 'Modern vs Classic web framework'),
        ('spacy', 'nltk', 'Modern vs Classic NLP'),
        ('asyncio', 'threading', 'Async vs Threading'),
        ('requests', 'aiohttp', 'Sync vs Async HTTP'),
    ]

    print("\nLibrary pair similarities:")
    for lib1, lib2, description in comparisons:
        if lib1 in model.wv and lib2 in model.wv:
            similarity = model.wv.similarity(lib1, lib2)
            print(f"  {similarity:.3f}  {lib1:15} ↔ {lib2:15}  ({description})")
        else:
            missing = [l for l in [lib1, lib2] if l not in model.wv]
            print(f"  ---   {lib1:15} ↔ {lib2:15}  (missing: {missing})")

def summarize_vocabulary(model: Word2Vec):
    """Summarize the learned vocabulary."""
    print("\n" + "=" * 70)
    print("VOCABULARY SUMMARY")
    print("=" * 70)

    vocab = model.wv.index_to_key
    print(f"\nTotal libraries learned: {len(vocab)}")
    print(f"\nAll libraries:")

    # Print in columns
    cols = 4
    for i in range(0, len(vocab), cols):
        chunk = vocab[i:i+cols]
        print("  " + "  ".join(f"{lib:20}" for lib in chunk))

def main():
    """Explore library embeddings."""
    embeddings_base = Path(__file__).parent / "embeddings"

    # Use 100d model (good balance of expressiveness and interpretability)
    model_dir = embeddings_base / "embeddings_100d"

    if not model_dir.exists():
        print(f"Error: {model_dir} not found")
        print("Run train_embeddings.py first")
        return

    print("Loading 100-dimensional embeddings...")
    model = Word2Vec.load(str(model_dir / "word2vec.model"))
    print(f"Loaded model with {len(model.wv)} libraries")

    # Run explorations
    summarize_vocabulary(model)
    test_analogies(model)
    nearest_neighbors_exploration(model)
    cluster_analysis(model)
    interesting_distances(model)

    print("\n" + "=" * 70)
    print("✓ Exploration complete!")
    print("=" * 70)

if __name__ == '__main__':
    main()
