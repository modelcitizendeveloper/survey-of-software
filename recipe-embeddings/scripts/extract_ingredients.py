#!/usr/bin/env python3
"""Extract ingredient entities from RecipeNLG dataset.

Reads full_dataset.csv and extracts NER (Named Entity Recognition) field
to create ingredient vocabulary and co-occurrence matrix for Word2Vec training.
"""

import pandas as pd
import json
from pathlib import Path
from collections import Counter, defaultdict

def extract_ingredients():
    """Extract ingredients from RecipeNLG CSV."""

    data_dir = Path(__file__).parent.parent / "data"
    dataset_path = data_dir / "dataset" / "full_dataset.csv"

    print(f"Loading RecipeNLG dataset from {dataset_path}...")
    print("This may take a few minutes (2.2M recipes, 2.2GB CSV)...")

    # Read CSV
    df = pd.read_csv(dataset_path)

    print(f"\n✓ Loaded {len(df):,} recipes")
    print(f"Columns: {list(df.columns)}")

    # Extract ingredient lists (NER column)
    print("\nExtracting ingredients from NER column...")

    ingredient_lists = []
    all_ingredients = Counter()
    recipe_count_by_source = Counter()

    for idx, row in df.iterrows():
        if (idx + 1) % 100000 == 0:
            print(f"  Processed {idx + 1:,} recipes...")

        # Parse NER field (JSON array)
        try:
            ner = json.loads(row['NER']) if isinstance(row['NER'], str) else row['NER']

            if ner and isinstance(ner, list):
                # Clean ingredients (lowercase, strip whitespace)
                ingredients = [ing.lower().strip() for ing in ner if ing]

                if ingredients:
                    ingredient_lists.append(ingredients)
                    all_ingredients.update(ingredients)
                    recipe_count_by_source[row['source']] += 1

        except (json.JSONDecodeError, TypeError):
            # Skip recipes with malformed NER
            continue

    print(f"\n✓ Extracted {len(ingredient_lists):,} valid ingredient lists")
    print(f"✓ Found {len(all_ingredients):,} unique ingredients")

    # Source breakdown
    print("\nRecipe sources:")
    for source, count in sorted(recipe_count_by_source.items()):
        source_name = "Gathered (high quality)" if source == 0 else "Recipes1M"
        print(f"  {source_name}: {count:,} recipes")

    # Save ingredient vocabulary
    output_dir = data_dir / "processed"
    output_dir.mkdir(exist_ok=True)

    vocab_file = output_dir / "ingredient_vocabulary.json"
    vocab = {
        'total_ingredients': len(all_ingredients),
        'total_recipes': len(ingredient_lists),
        'ingredients': [
            {
                'name': ing,
                'frequency': count
            }
            for ing, count in all_ingredients.most_common()
        ]
    }

    with open(vocab_file, 'w') as f:
        json.dump(vocab, f, indent=2)

    print(f"\n✓ Saved vocabulary to {vocab_file}")

    # Save ingredient lists for Word2Vec training
    # Use TAB delimiter to preserve multi-word ingredients
    lists_file = output_dir / "ingredient_lists.txt"

    with open(lists_file, 'w') as f:
        for ingredients in ingredient_lists:
            f.write('\t'.join(ingredients) + '\n')

    print(f"✓ Saved ingredient lists to {lists_file}")

    # Statistics
    print("\n" + "="*60)
    print("Dataset Statistics:")
    print("="*60)
    print(f"Total recipes: {len(df):,}")
    print(f"Valid ingredient lists: {len(ingredient_lists):,}")
    print(f"Unique ingredients: {len(all_ingredients):,}")

    avg_ingredients = sum(len(lst) for lst in ingredient_lists) / len(ingredient_lists)
    print(f"Avg ingredients per recipe: {avg_ingredients:.1f}")

    # Top ingredients
    print("\nTop 30 ingredients:")
    for ing, count in all_ingredients.most_common(30):
        print(f"  {count:6,}  {ing}")

    # Co-occurrence analysis
    print("\n" + "="*60)
    print("Co-occurrence Analysis:")
    print("="*60)

    co_occur = defaultdict(lambda: defaultdict(int))

    print("Computing co-occurrences (this may take a minute)...")
    for idx, ingredients in enumerate(ingredient_lists[:100000]):  # Sample 100k for speed
        if (idx + 1) % 10000 == 0:
            print(f"  Processed {idx + 1:,} recipes...")

        for i, ing1 in enumerate(ingredients):
            for ing2 in ingredients[i+1:]:
                co_occur[ing1][ing2] += 1
                co_occur[ing2][ing1] += 1

    # Find most common pairs
    pairs = []
    for ing1, ing2_counts in co_occur.items():
        for ing2, count in ing2_counts.items():
            if ing1 < ing2:  # Avoid duplicates
                pairs.append((count, ing1, ing2))

    pairs.sort(reverse=True)

    print("\nTop 20 ingredient pairs (from 100k sample):")
    for count, ing1, ing2 in pairs[:20]:
        print(f"  {count:5,}  {ing1} + {ing2}")

    print("\n" + "="*60)
    print("Ready for Word2Vec training!")
    print("="*60)
    print(f"Input file: {lists_file}")
    print(f"Format: One recipe per line, TAB-separated ingredients")
    print(f"Read with: [line.strip().split('\\t') for line in f]")
    print(f"Total: {len(ingredient_lists):,} sentences (recipes)")
    print(f"Vocab: {len(all_ingredients):,} words (ingredients)")

if __name__ == "__main__":
    extract_ingredients()
