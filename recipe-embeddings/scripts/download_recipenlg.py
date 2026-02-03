#!/usr/bin/env python3
"""Download RecipeNLG dataset from Hugging Face.

RecipeNLG: 2.2M cooking recipes with structured ingredient lists.
Source: https://huggingface.co/datasets/mbien/recipe_nlg
License: Non-commercial research and educational use only
"""

from datasets import load_dataset
import json
from pathlib import Path

def download_recipenlg():
    """Download RecipeNLG dataset and save to local JSON."""

    print("Downloading RecipeNLG dataset from Hugging Face...")
    print("This may take several minutes (2.2M recipes)...")

    # Try lite version first (7k recipes) to test pipeline
    # Full dataset: mbien/recipe_nlg (2.2M recipes) - requires manual download
    print("NOTE: Using lite version (7k recipes) for testing")
    print("Full dataset (2.2M) available at: recipenlg.cs.put.poznan.pl")
    print()

    dataset = load_dataset("m3hrdadfi/recipe_nlg_lite")

    # Get train split (only split available)
    recipes = dataset['train']

    print(f"\nDataset loaded: {len(recipes):,} recipes")

    # Save full dataset to JSON
    output_dir = Path(__file__).parent.parent / "data"
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / "recipenlg_full.json"

    print(f"\nSaving to {output_file}...")

    # Convert to list of dicts for easier processing
    recipes_list = []
    for i, recipe in enumerate(recipes):
        recipes_list.append({
            'id': recipe['id'],
            'title': recipe['title'],
            'ingredients': recipe['ingredients'],
            'directions': recipe['directions'],
            'link': recipe['link'],
            'source': recipe['source'],  # 0=Gathered, 1=Recipes1M
            'ner': recipe['ner']  # Pre-parsed ingredient entities
        })

        if (i + 1) % 100000 == 0:
            print(f"  Processed {i + 1:,} recipes...")

    with open(output_file, 'w') as f:
        json.dump(recipes_list, f, indent=2)

    print(f"\n✓ Saved {len(recipes_list):,} recipes to {output_file}")

    # Also save high-quality subset (source=Gathered)
    gathered = [r for r in recipes_list if r['source'] == 0]
    gathered_file = output_dir / "recipenlg_gathered.json"

    with open(gathered_file, 'w') as f:
        json.dump(gathered, f, indent=2)

    print(f"✓ Saved {len(gathered):,} high-quality recipes to {gathered_file}")

    # Print sample recipe
    sample = recipes_list[0]
    print("\n" + "="*60)
    print("Sample Recipe:")
    print("="*60)
    print(f"Title: {sample['title']}")
    print(f"\nIngredients ({len(sample['ingredients'])}):")
    for ing in sample['ingredients'][:5]:
        print(f"  - {ing}")
    if len(sample['ingredients']) > 5:
        print(f"  ... and {len(sample['ingredients']) - 5} more")

    print(f"\nParsed entities (NER): {sample['ner'][:5]}")

    print("\n" + "="*60)
    print("Dataset Statistics:")
    print("="*60)
    print(f"Total recipes: {len(recipes_list):,}")
    print(f"Gathered (high quality): {len(gathered):,}")
    print(f"Recipe1M (original): {len(recipes_list) - len(gathered):,}")

    # Count unique ingredients from NER
    all_ingredients = set()
    for recipe in recipes_list[:10000]:  # Sample for speed
        all_ingredients.update(recipe['ner'])

    print(f"\nUnique ingredients (from 10k sample): {len(all_ingredients):,}")
    print(f"Sample ingredients: {sorted(list(all_ingredients))[:20]}")

if __name__ == "__main__":
    download_recipenlg()
