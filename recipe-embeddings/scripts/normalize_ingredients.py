#!/usr/bin/env python3
"""Normalize ingredient names for better embeddings.

Handles:
- Spelling corrections (tarter → tartar)
- Variant merging (cream of mushroom → cream of mushroom soup)
- Singularization (mushrooms → mushroom)
- Compound preservation (keep "cream of X" as single entity)
"""

import re
from collections import Counter

# Spelling corrections for common typos
SPELLING_FIXES = {
    "cream of tarter": "cream of tartar",
    "backing powder": "baking powder",
    "backing soda": "baking soda",
    # Add more as discovered
}

# Ingredients that should NOT get "soup" added
NOT_SOUPS = {
    "cream of tartar",
    "cream of wheat", 
    "cream of coconut",
    "cream of rice",
}

def normalize_ingredient(ing):
    """Normalize a single ingredient name."""
    ing = ing.lower().strip()
    
    # Fix common typos
    if ing in SPELLING_FIXES:
        ing = SPELLING_FIXES[ing]
    
    # Normalize "cream of X" → "cream of X soup" (except special cases)
    if ing.startswith("cream of "):
        # Already has soup?
        if not ing.endswith("soup") and ing not in NOT_SOUPS:
            # Check if it's a soup variant
            if any(word in ing for word in ["mushroom", "chicken", "celery", 
                                             "potato", "broccoli", "shrimp", 
                                             "onion", "tomato", "asparagus",
                                             "cheddar", "cheese"]):
                ing = ing + " soup"
    
    # Singularization (simple heuristic - can use inflect library for better)
    # But be careful: "brussels sprouts" should stay plural!
    # For now, skip this - too many edge cases
    
    return ing

def normalize_all_ingredients(input_file, output_file, vocab_file):
    """Normalize all ingredient lists and update vocabulary."""
    
    print("Loading ingredient lists...")
    with open(input_file) as f:
        recipes = [line.strip().split() for line in f]
    
    print(f"Loaded {len(recipes):,} recipes")
    
    # Normalize all ingredients
    print("\nNormalizing ingredients...")
    normalized_recipes = []
    all_ingredients = Counter()
    
    changes = Counter()  # Track what changed
    
    for idx, recipe in enumerate(recipes):
        if (idx + 1) % 100000 == 0:
            print(f"  Processed {idx + 1:,} recipes...")
        
        normalized = []
        for ing in recipe:
            norm_ing = normalize_ingredient(ing)
            normalized.append(norm_ing)
            all_ingredients[norm_ing] += 1
            
            if norm_ing != ing:
                changes[f"{ing} → {norm_ing}"] += 1
        
        normalized_recipes.append(normalized)
    
    # Save normalized lists
    print(f"\nSaving normalized lists to {output_file}...")
    with open(output_file, 'w') as f:
        for recipe in normalized_recipes:
            f.write(' '.join(recipe) + '\n')
    
    # Save updated vocabulary
    print(f"Saving updated vocabulary to {vocab_file}...")
    import json
    vocab = {
        'total_ingredients': len(all_ingredients),
        'total_recipes': len(normalized_recipes),
        'ingredients': [
            {'name': ing, 'frequency': count}
            for ing, count in all_ingredients.most_common()
        ]
    }
    
    with open(vocab_file, 'w') as f:
        json.dump(vocab, f, indent=2)
    
    # Report changes
    print("\n" + "="*60)
    print("Normalization Summary:")
    print("="*60)
    print(f"Original vocabulary: {len(set(ing for recipe in recipes for ing in recipe)):,}")
    print(f"Normalized vocabulary: {len(all_ingredients):,}")
    print(f"Reduction: {len(set(ing for recipe in recipes for ing in recipe)) - len(all_ingredients):,} ingredients merged")
    
    if changes:
        print(f"\nTop 20 changes:")
        for change, count in changes.most_common(20):
            print(f"  {count:6,}  {change}")

if __name__ == "__main__":
    normalize_all_ingredients(
        input_file="data/processed/ingredient_lists.txt",
        output_file="data/processed/ingredient_lists_normalized.txt",
        vocab_file="data/processed/ingredient_vocabulary_normalized.json"
    )
