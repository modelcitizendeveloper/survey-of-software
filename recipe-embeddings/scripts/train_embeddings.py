#!/usr/bin/env python3
"""Train Word2Vec embeddings on recipe ingredients.

Uses skip-gram algorithm to learn ingredient relationships from co-occurrence
patterns in 2.2M recipes. Trains multiple embedding dimensions for comparison.

Based on food2vec (2016) but with:
- 23× more data (2.2M vs 96k recipes)
- Larger vocabulary (~50k vs 2k ingredients after filtering)
- Multiple dimensions (50d, 100d, 300d)
- Optimized for dietary substitution queries
"""

from gensim.models import Word2Vec
from pathlib import Path
import json
import time
import multiprocessing
from collections import Counter

# Training configuration
CONFIG = {
    'dimensions': [50, 100, 300],  # Train multiple sizes for comparison
    'window': 5,                   # ~Half of avg recipe length (8.5 ingredients)
    'min_count': 20,               # Filter rare ingredients/typos (0.001% threshold)
    'epochs': 10,                  # Standard for word embeddings
    'negative': 15,                # Higher for large datasets (vs default 5)
    'workers': multiprocessing.cpu_count() - 1,  # Parallel training
    'sample': 1e-3,                # Downsample frequent words (default)
    'sg': 1,                       # Skip-gram (better for rare ingredients)
    'hs': 0,                       # Use negative sampling (not hierarchical softmax)
}

# Test analogies for validation
TEST_ANALOGIES = [
    # Dairy substitutions
    ('butter', 'dairy', 'vegan', ['coconut oil', 'olive oil', 'vegetable oil', 'margarine']),
    ('milk', 'dairy', 'vegan', ['almond milk', 'soy milk', 'coconut milk']),

    # Gluten-free substitutions
    ('flour', 'wheat', 'gluten-free', ['almond flour', 'rice flour', 'coconut flour']),

    # Protein substitutions
    ('beef', 'meat', 'vegetarian', ['mushrooms', 'tofu', 'lentils', 'beans']),

    # Flavor pairings (like food2vec)
    ('egg', 'bacon', 'orange juice', ['coffee', 'milk']),
]


def load_ingredients(input_file):
    """Load tab-separated ingredient lists from file.

    Format: One recipe per line, ingredients separated by tabs.
    Multi-word ingredients (e.g., "cream of mushroom soup") preserved.
    """
    print(f"Loading ingredient lists from {input_file}...")

    sentences = []
    with open(input_file) as f:
        for i, line in enumerate(f):
            # Split on tabs to preserve multi-word ingredients
            ingredients = line.strip().split('\t')

            if ingredients and ingredients != ['']:
                sentences.append(ingredients)

            if (i + 1) % 100000 == 0:
                print(f"  Loaded {i + 1:,} recipes...")

    print(f"\n✓ Loaded {len(sentences):,} recipes")

    # Calculate statistics
    total_ingredients = sum(len(recipe) for recipe in sentences)
    avg_length = total_ingredients / len(sentences)

    print(f"  Average ingredients per recipe: {avg_length:.1f}")

    # Count vocabulary before min_count filtering
    all_ingredients = Counter()
    for recipe in sentences:
        all_ingredients.update(recipe)

    print(f"  Raw vocabulary: {len(all_ingredients):,} unique ingredients")

    # Show distribution
    thresholds = [1, 5, 10, 20, 50, 100]
    print(f"\n  Vocabulary at different min_count thresholds:")
    for threshold in thresholds:
        count = sum(1 for freq in all_ingredients.values() if freq >= threshold)
        print(f"    min_count={threshold:3d}: {count:6,} ingredients")

    return sentences


def train_model(sentences, vector_size, config):
    """Train a Word2Vec model with specified dimension."""

    print(f"\n{'='*60}")
    print(f"Training {vector_size}d model")
    print(f"{'='*60}")

    start_time = time.time()

    # Build model
    model = Word2Vec(
        sentences=sentences,
        vector_size=vector_size,
        window=config['window'],
        min_count=config['min_count'],
        workers=config['workers'],
        sg=config['sg'],
        hs=config['hs'],
        negative=config['negative'],
        sample=config['sample'],
        epochs=config['epochs'],
        seed=42,  # Reproducibility
    )

    elapsed = time.time() - start_time

    print(f"\n✓ Training complete in {elapsed:.1f}s ({elapsed/60:.1f} minutes)")
    print(f"  Vocabulary size: {len(model.wv):,} ingredients")
    print(f"  Total training samples: {model.corpus_total_words:,}")

    return model


def test_model(model, vector_size):
    """Test model with analogies and similarity queries."""

    print(f"\n{'='*60}")
    print(f"Testing {vector_size}d model")
    print(f"{'='*60}")

    # Test basic similarity
    print("\n1. Ingredient Similarity:")
    test_ingredients = ['butter', 'chicken', 'garlic', 'chocolate']

    for ing in test_ingredients:
        if ing in model.wv:
            similar = model.wv.most_similar(ing, topn=5)
            print(f"\n  '{ing}' is similar to:")
            for word, score in similar:
                print(f"    {score:.3f}  {word}")
        else:
            print(f"\n  '{ing}' not in vocabulary (filtered by min_count)")

    # Test analogies
    print("\n2. Analogies (X - A + B = ?):")

    successful = 0
    total = 0

    for x, a, b, expected_list in TEST_ANALOGIES:
        # Check if all words are in vocabulary
        if not all(word in model.wv for word in [x, a, b]):
            missing = [w for w in [x, a, b] if w not in model.wv]
            print(f"\n  {x} - {a} + {b} = ?")
            print(f"    SKIP: Words not in vocabulary: {missing}")
            continue

        try:
            # Perform analogy
            result = model.wv.most_similar(
                positive=[b, x],
                negative=[a],
                topn=10
            )

            print(f"\n  {x} - {a} + {b} = ?")
            print(f"    Top 5 results:")
            for word, score in result[:5]:
                marker = "✓" if word in expected_list else " "
                print(f"    {marker} {score:.3f}  {word}")

            # Check if any expected result is in top 10
            result_words = [word for word, _ in result]
            if any(expected in result_words for expected in expected_list):
                successful += 1
                print(f"    SUCCESS: Found expected result in top 10")
            else:
                print(f"    Expected one of: {expected_list}")

            total += 1

        except KeyError as e:
            print(f"\n  {x} - {a} + {b} = ?")
            print(f"    ERROR: {e}")

    if total > 0:
        accuracy = (successful / total) * 100
        print(f"\n  Analogy accuracy: {successful}/{total} ({accuracy:.1f}%)")

    # Test compound ingredients specifically
    print("\n3. Compound Ingredients (NER test):")
    compounds = ['cream of mushroom soup', 'cream of chicken soup',
                 'sour cream', 'brown sugar', 'olive oil']

    for compound in compounds:
        if compound in model.wv:
            similar = model.wv.most_similar(compound, topn=3)
            print(f"\n  '{compound}':")
            for word, score in similar:
                print(f"    {score:.3f}  {word}")
        else:
            print(f"\n  '{compound}': Not in vocabulary")


def save_model(model, vector_size, output_dir):
    """Save model and export vocabulary with vectors."""

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Save full model (for continued training)
    model_file = output_dir / f"recipe_embeddings_{vector_size}d.model"
    model.save(str(model_file))
    print(f"\n✓ Saved model to {model_file}")

    # Save word vectors only (smaller, faster loading)
    vectors_file = output_dir / f"recipe_embeddings_{vector_size}d.kv"
    model.wv.save(str(vectors_file))
    print(f"✓ Saved vectors to {vectors_file}")

    # Export to text format for inspection
    text_file = output_dir / f"recipe_embeddings_{vector_size}d.txt"
    model.wv.save_word2vec_format(str(text_file))
    print(f"✓ Saved text format to {text_file}")

    # Save metadata
    metadata = {
        'vector_size': vector_size,
        'vocabulary_size': len(model.wv),
        'config': CONFIG,
        'total_training_words': model.corpus_total_words,
        'total_training_examples': model.corpus_count,
    }

    metadata_file = output_dir / f"recipe_embeddings_{vector_size}d_metadata.json"
    with open(metadata_file, 'w') as f:
        json.dump(metadata, f, indent=2)
    print(f"✓ Saved metadata to {metadata_file}")

    # Export top ingredients with vectors (sample for inspection)
    sample_file = output_dir / f"recipe_embeddings_{vector_size}d_sample.json"
    sample_data = []

    for word in list(model.wv.index_to_key)[:100]:  # Top 100 most frequent
        vector = model.wv[word].tolist()
        sample_data.append({
            'ingredient': word,
            'vector': vector,
            'frequency': int(model.wv.get_vecattr(word, 'count'))  # Convert numpy int64 to Python int
        })

    with open(sample_file, 'w') as f:
        json.dump(sample_data, f, indent=2)
    print(f"✓ Saved sample vectors to {sample_file}")


def main():
    """Main training pipeline."""

    print("="*60)
    print("Recipe Ingredient Embeddings - Word2Vec Training")
    print("="*60)
    print(f"\nConfiguration:")
    for key, value in CONFIG.items():
        if key != 'dimensions':
            print(f"  {key:12s}: {value}")
    print(f"  dimensions  : {CONFIG['dimensions']}")

    # Load data
    data_dir = Path(__file__).parent.parent / "data" / "processed"
    input_file = data_dir / "ingredient_lists.txt"

    if not input_file.exists():
        print(f"\n❌ ERROR: Input file not found: {input_file}")
        print("Run extract_ingredients.py first to generate ingredient lists.")
        return

    sentences = load_ingredients(input_file)

    # Output directory
    output_dir = Path(__file__).parent.parent / "models"

    # Train models for each dimension
    models = {}

    for dim in CONFIG['dimensions']:
        model = train_model(sentences, dim, CONFIG)
        test_model(model, dim)
        save_model(model, dim, output_dir)
        models[dim] = model

    # Summary
    print("\n" + "="*60)
    print("Training Complete!")
    print("="*60)
    print(f"\nTrained {len(models)} models:")
    for dim, model in models.items():
        size_mb = (dim * len(model.wv) * 4) / (1024 * 1024)  # 4 bytes per float
        print(f"  {dim}d: {len(model.wv):,} ingredients, ~{size_mb:.1f}MB")

    print(f"\nModels saved to: {output_dir}/")
    print("\nNext steps:")
    print("  1. Evaluate embeddings with validation set")
    print("  2. Build CLI tool: recipe-emb substitute <ingredient> --diet <diet>")
    print("  3. Test with real recipes")
    print("  4. Compare with food2vec results (if available)")


if __name__ == "__main__":
    main()
