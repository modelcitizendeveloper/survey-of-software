#!/usr/bin/env python3
"""Command-line interface for recipe embeddings."""

import argparse
import sys
from pathlib import Path
from gensim.models import KeyedVectors
from .pantry import (RecipeDatabase, parse_pantry, load_pantry_from_file,
                     format_recipe_match, format_recipe_full)


class RecipeEmbeddings:
    """Recipe ingredient embeddings interface."""

    _models_cache = {}  # Cache loaded models

    def __init__(self, dimension=100, models_dir=None):
        """Load embeddings for specified dimension."""
        if models_dir is None:
            # Default to models/ in package parent directory
            package_dir = Path(__file__).parent.parent
            models_dir = package_dir / "models"

        self.models_dir = Path(models_dir)
        self.dimension = dimension

        # Check if model exists
        self.model_path = self.models_dir / f"recipe_embeddings_{dimension}d.kv"
        if not self.model_path.exists():
            available = list(self.models_dir.glob("recipe_embeddings_*d.kv"))
            if available:
                dims = [m.stem.split('_')[-1] for m in available]
                raise FileNotFoundError(
                    f"Model {dimension}d not found. Available: {', '.join(dims)}"
                )
            else:
                raise FileNotFoundError(
                    f"No models found in {self.models_dir}. "
                    "Run train_embeddings.py first."
                )

        # Load model (with caching)
        cache_key = str(self.model_path)
        if cache_key not in self._models_cache:
            self._models_cache[cache_key] = KeyedVectors.load(str(self.model_path))

        self.wv = self._models_cache[cache_key]

    def similar(self, ingredient, topn=10):
        """Find similar ingredients."""
        if ingredient not in self.wv:
            # Try case-insensitive
            matches = [w for w in self.wv.index_to_key if w.lower() == ingredient.lower()]
            if matches:
                ingredient = matches[0]
            else:
                return None, self._suggest_alternatives(ingredient)

        similar = self.wv.most_similar(ingredient, topn=topn + 1)
        # Exclude the ingredient itself
        similar = [(w, s) for w, s in similar if w != ingredient][:topn]

        return similar, None

    def substitute(self, ingredient, exclude=None, topn=10):
        """Find substitutes, excluding certain words."""
        similar, error = self.similar(ingredient, topn=topn * 3)

        if error:
            return None, error

        if exclude:
            exclude_lower = [w.lower() for w in exclude]
            filtered = []

            for word, score in similar:
                if not any(exc in word.lower() for exc in exclude_lower):
                    filtered.append((word, score))
                if len(filtered) >= topn:
                    break

            return filtered, None

        return similar[:topn], None

    def analogy(self, positive, negative, topn=10):
        """Compute analogy: positive[0] - negative[0] + positive[1]."""
        all_words = positive + negative
        missing = [w for w in all_words if w not in self.wv]

        if missing:
            suggestions = []
            for word in missing:
                sugg = self._suggest_alternatives(word, max_suggestions=3)
                if sugg:
                    suggestions.append(f"  '{word}' → try: {', '.join(sugg)}")
            return None, f"Not in vocabulary: {', '.join(missing)}\n" + "\n".join(suggestions)

        try:
            result = self.wv.most_similar(positive=positive, negative=negative, topn=topn)
            return result, None
        except KeyError as e:
            return None, str(e)

    def _suggest_alternatives(self, word, max_suggestions=5):
        """Suggest similar vocabulary words."""
        word_lower = word.lower()

        # Exact substring matches
        matches = [w for w in self.wv.index_to_key if word_lower in w.lower()]

        if not matches:
            # Prefix matches
            prefix = word_lower[:3] if len(word_lower) >= 3 else word_lower
            matches = [w for w in self.wv.index_to_key if w.lower().startswith(prefix)]

        return matches[:max_suggestions]

    def search(self, pattern, max_results=20):
        """Search vocabulary for pattern."""
        pattern_lower = pattern.lower()
        matches = [w for w in self.wv.index_to_key if pattern_lower in w.lower()]
        return matches[:max_results]

    @property
    def vocab_size(self):
        """Get vocabulary size."""
        return len(self.wv)


def cmd_similar(args):
    """Handle 'similar' command."""
    emb = RecipeEmbeddings(dimension=args.dim)

    results, error = emb.similar(args.ingredient, topn=args.top)

    if error:
        print(f"❌ '{args.ingredient}' not in vocabulary")
        if error:
            print(f"\n💡 Did you mean:")
            for word in error:
                print(f"   - {word}")
        return 1

    print(f"\nSimilar to '{args.ingredient}' ({args.dim}d model, {emb.vocab_size:,} ingredients):")
    print("=" * 60)
    for i, (word, score) in enumerate(results, 1):
        print(f"  {i:2d}. {score:.3f}  {word}")

    return 0


def cmd_substitute(args):
    """Handle 'substitute' command."""
    emb = RecipeEmbeddings(dimension=args.dim)

    exclude = args.exclude.split(',') if args.exclude else None

    results, error = emb.substitute(args.ingredient, exclude=exclude, topn=args.top)

    if error:
        print(f"❌ '{args.ingredient}' not in vocabulary")
        if error:
            print(f"\n💡 Did you mean:")
            for word in error:
                print(f"   - {word}")
        return 1

    title = f"Substitutes for '{args.ingredient}'"
    if exclude:
        title += f" (excluding: {', '.join(exclude)})"

    print(f"\n{title}")
    print("=" * 60)
    for i, (word, score) in enumerate(results, 1):
        print(f"  {i:2d}. {score:.3f}  {word}")

    return 0


def cmd_analogy(args):
    """Handle 'analogy' command."""
    emb = RecipeEmbeddings(dimension=args.dim)

    # Parse analogy: "word1 - word2 + word3"
    parts = args.expression.split()

    if '-' not in parts or '+' not in parts:
        print("❌ Invalid format. Use: <word1> - <word2> + <word3>")
        print("   Example: beef - meat + vegetarian")
        return 1

    try:
        minus_idx = parts.index('-')
        plus_idx = parts.index('+')

        word1 = ' '.join(parts[:minus_idx])
        word2 = ' '.join(parts[minus_idx + 1:plus_idx])
        word3 = ' '.join(parts[plus_idx + 1:])

        positive = [word1, word3]
        negative = [word2]

    except (ValueError, IndexError):
        print("❌ Invalid format. Use: <word1> - <word2> + <word3>")
        return 1

    results, error = emb.analogy(positive, negative, topn=args.top)

    if error:
        print(f"❌ {error}")
        return 1

    print(f"\n{word1} - {word2} + {word3} = ?")
    print("=" * 60)
    for i, (word, score) in enumerate(results, 1):
        print(f"  {i:2d}. {score:.3f}  {word}")

    return 0


def cmd_search(args):
    """Handle 'search' command."""
    emb = RecipeEmbeddings(dimension=args.dim)

    results = emb.search(args.pattern, max_results=args.top)

    if not results:
        print(f"❌ No matches found for '{args.pattern}'")
        return 1

    print(f"\nMatches for '{args.pattern}' ({len(results)} results):")
    print("=" * 60)
    for i, word in enumerate(results, 1):
        print(f"  {i:2d}. {word}")

    return 0


def categorize_ingredient(ingredient):
    """Categorize an ingredient into food groups."""
    ing_lower = ingredient.lower()

    # Expanded category definitions
    categories = []

    # Proteins
    protein_words = [
        'chicken', 'beef', 'pork', 'fish', 'shrimp', 'turkey', 'bacon', 'sausage',
        'tofu', 'egg', 'salmon', 'tuna', 'cod', 'ham', 'lamb', 'duck', 'venison',
        'crab', 'lobster', 'scallop', 'anchovy', 'sardine', 'tempeh', 'seitan'
    ]
    if any(p in ing_lower for p in protein_words):
        categories.append('protein')

    # Vegetables
    veggie_words = [
        'onion', 'tomato', 'pepper', 'carrot', 'celery', 'mushroom', 'broccoli',
        'spinach', 'potato', 'zucchini', 'eggplant', 'cabbage', 'lettuce', 'kale',
        'chard', 'beet', 'radish', 'turnip', 'squash', 'pumpkin', 'cucumber',
        'asparagus', 'artichoke', 'brussels', 'cauliflower', 'pea', 'bean',
        'corn', 'avocado', 'leek', 'fennel', 'arugula', 'bok choy', 'collard'
    ]
    if any(v in ing_lower for v in veggie_words):
        categories.append('vegetables')

    # Aromatics (subset of vegetables, but more specific)
    aromatic_words = ['garlic', 'ginger', 'shallot', 'scallion', 'leek', 'onion']
    if any(a in ing_lower for a in aromatic_words):
        categories.append('aromatics')

    # Herbs
    herb_words = [
        'basil', 'parsley', 'cilantro', 'thyme', 'rosemary', 'oregano', 'sage',
        'mint', 'dill', 'tarragon', 'chive', 'bay', 'marjoram', 'savory'
    ]
    if any(h in ing_lower for h in herb_words):
        categories.append('herbs')

    # Spices
    spice_words = [
        'pepper', 'cumin', 'paprika', 'cinnamon', 'nutmeg', 'clove', 'cardamom',
        'coriander', 'turmeric', 'curry', 'chili', 'cayenne', 'garam', 'masala',
        'saffron', 'star anise', 'fennel seed', 'mustard seed', 'sesame seed',
        'poppy', 'caraway', 'allspice', 'mace', 'za\'atar', 'sumac'
    ]
    if any(s in ing_lower for s in spice_words):
        categories.append('spices')

    # Dairy
    dairy_words = [
        'butter', 'cream', 'cheese', 'milk', 'yogurt', 'sour cream', 'cream cheese',
        'mozzarella', 'parmesan', 'cheddar', 'ricotta', 'feta', 'goat cheese',
        'mascarpone', 'cottage cheese', 'whey', 'buttermilk', 'ghee'
    ]
    if any(d in ing_lower for d in dairy_words):
        categories.append('dairy')

    # Fruits
    fruit_words = [
        'apple', 'banana', 'orange', 'lemon', 'lime', 'berry', 'grape', 'melon',
        'peach', 'pear', 'plum', 'cherry', 'mango', 'pineapple', 'strawberry',
        'blueberry', 'raspberry', 'blackberry', 'cranberry', 'date', 'fig',
        'apricot', 'nectarine', 'kiwi', 'papaya', 'guava', 'passion fruit'
    ]
    if any(f in ing_lower for f in fruit_words):
        categories.append('fruits')

    # Grains & Starches
    grain_words = [
        'rice', 'pasta', 'flour', 'bread', 'quinoa', 'couscous', 'oat', 'barley',
        'wheat', 'rye', 'corn', 'tortilla', 'noodle', 'macaroni', 'spaghetti'
    ]
    if any(g in ing_lower for g in grain_words):
        categories.append('grains')

    # Oils & Fats
    oil_words = [
        'oil', 'fat', 'lard', 'shortening', 'ghee', 'schmaltz'
    ]
    if any(o in ing_lower for o in oil_words) and 'olive' not in ing_lower:
        categories.append('oils')

    if not categories:
        categories.append('other')

    return categories


def cmd_pair(args):
    """Handle 'pair' command - ingredient pairing suggestions."""
    emb = RecipeEmbeddings(dimension=args.dim)

    # Get more results for filtering (need to search deep for category filtering)
    search_multiplier = 20 if args.category else 2
    results, error = emb.similar(args.ingredient, topn=min(args.top * search_multiplier, 200))

    if error:
        print(f"❌ '{args.ingredient}' not in vocabulary")
        if error:
            print(f"\n💡 Did you mean:")
            for word in error:
                print(f"   - {word}")
        return 1

    # Parse requested categories
    requested_categories = []
    if args.category:
        requested_categories = [c.strip().lower() for c in args.category.split(',')]

    # Filter results
    base_ingredient = args.ingredient.lower()
    filtered = []

    for word, score in results:
        word_lower = word.lower()

        # Skip if it's the same ingredient
        if args.exclude_self and word_lower == base_ingredient:
            continue

        # Skip close variations of the same ingredient (unless it's a useful form)
        if args.exclude_self and (base_ingredient in word_lower or word_lower in base_ingredient):
            # Allow useful variations
            if not any(prefix in word_lower for prefix in ['fresh', 'dried', 'ground', 'chopped', 'minced']):
                continue

        # Category filtering
        if requested_categories:
            ing_categories = categorize_ingredient(word)
            if not any(cat in ing_categories for cat in requested_categories):
                continue

        filtered.append((word, score))

        if len(filtered) >= args.top:
            break

    print(f"\nCooking with '{args.ingredient}'? Consider adding:")
    print("=" * 60)

    if args.group:
        # Group by category (simple heuristic)
        proteins = []
        vegetables = []
        aromatics = []
        herbs_spices = []
        dairy = []
        other = []

        protein_words = ['chicken', 'beef', 'pork', 'fish', 'shrimp', 'turkey', 'bacon', 'sausage', 'tofu', 'egg']
        veggie_words = ['onion', 'tomato', 'pepper', 'carrot', 'celery', 'mushroom', 'broccoli', 'spinach', 'potato']
        aromatic_words = ['garlic', 'ginger', 'shallot', 'scallion', 'leek']
        herb_spice_words = ['basil', 'parsley', 'thyme', 'rosemary', 'oregano', 'cilantro', 'cumin', 'paprika', 'pepper', 'cinnamon']
        dairy_words = ['butter', 'cream', 'cheese', 'milk', 'yogurt']

        for word, score in filtered:
            word_lower = word.lower()
            if any(p in word_lower for p in protein_words):
                proteins.append((word, score))
            elif any(v in word_lower for v in veggie_words):
                vegetables.append((word, score))
            elif any(a in word_lower for a in aromatic_words):
                aromatics.append((word, score))
            elif any(h in word_lower for h in herb_spice_words):
                herbs_spices.append((word, score))
            elif any(d in word_lower for d in dairy_words):
                dairy.append((word, score))
            else:
                other.append((word, score))

        # Print grouped results
        categories = [
            ("Aromatics", aromatics),
            ("Herbs & Spices", herbs_spices),
            ("Vegetables", vegetables),
            ("Proteins", proteins),
            ("Dairy & Fats", dairy),
            ("Other", other)
        ]

        for category, items in categories:
            if items:
                print(f"\n{category}:")
                for word, score in items[:5]:
                    print(f"  • {word} (pairs well, {score:.2f} similarity)")
    else:
        # Simple list
        for i, (word, score) in enumerate(filtered, 1):
            print(f"  {i:2d}. {word} (similarity: {score:.2f})")

    return 0


def cmd_info(args):
    """Handle 'info' command."""
    emb = RecipeEmbeddings(dimension=args.dim)

    print(f"\nRecipe Embeddings - Model Info")
    print("=" * 60)
    print(f"  Dimension:    {emb.dimension}d")
    print(f"  Vocabulary:   {emb.vocab_size:,} ingredients")
    print(f"  Model file:   {emb.model_path}")
    print(f"  Model size:   {emb.model_path.stat().st_size / (1024*1024):.1f}MB")

    # Show available models
    available = sorted(emb.models_dir.glob("recipe_embeddings_*d.kv"),
                      key=lambda x: x.stat().st_size)

    if len(available) > 1:
        print(f"\n  Available models:")
        for model_file in available:
            dim = model_file.stem.split('_')[-1]
            size_mb = model_file.stat().st_size / (1024 * 1024)
            marker = "→" if dim == f"{emb.dimension}d" else " "
            print(f"    {marker} {dim:5s} ({size_mb:5.1f}MB)")

    print(f"\n  Training data: 2.2M recipes (RecipeNLG dataset)")
    print(f"  Algorithm:     Word2Vec skip-gram")
    print(f"  Window:        5")
    print(f"  Min count:     20")

    # Show top 10 ingredients
    print(f"\n  Top 10 ingredients:")
    for i, word in enumerate(emb.wv.index_to_key[:10], 1):
        print(f"    {i:2d}. {word}")

    return 0


def cmd_show(args):
    """Handle 'show' command - display full recipe details."""
    import subprocess
    import csv
    import json
    from io import StringIO

    # Find dataset
    package_dir = Path(__file__).parent.parent
    dataset_path = package_dir / "data" / "dataset" / "full_dataset.csv"

    if not dataset_path.exists():
        print(f"❌ Dataset not found: {dataset_path}")
        print("Run extract_ingredients.py first to download and process the dataset.")
        return 1

    # Fast lookup using grep (much faster than loading entire database)
    print(f"Looking up recipe {args.recipe_id}...")

    try:
        # Grep for the recipe ID in the first column
        # Format: ^<id>,  (start of line, ID, comma)
        result = subprocess.run(
            ['grep', '-m', '1', f'^{args.recipe_id},', str(dataset_path)],
            capture_output=True,
            text=True,
            check=False
        )

        if result.returncode != 0 or not result.stdout.strip():
            print(f"❌ Recipe ID {args.recipe_id} not found")
            return 1

        # Parse the CSV line (format: id,title,ingredients,directions,link,source,NER)
        csv_reader = csv.reader(StringIO(result.stdout))
        row = next(csv_reader)

        if len(row) < 7:
            print(f"❌ Invalid recipe data")
            return 1

        recipe_id, title, ingredients_json, directions_json, link, source_str, ner_json = row

        # Parse JSON fields
        try:
            raw_ingredients = json.loads(ingredients_json) if ingredients_json else []
            directions = json.loads(directions_json) if directions_json else []
            ner = json.loads(ner_json) if ner_json else []
        except json.JSONDecodeError:
            raw_ingredients = []
            directions = []
            ner = []

        # Map source string to int (Gathered=0, Recipes1M=1)
        source = 0 if source_str == "Gathered" else 1

        # Create Recipe object
        from .pantry import Recipe
        recipe = Recipe(
            id=int(recipe_id),
            title=title,
            ingredients=ner,
            source=source,
            raw_ingredients=raw_ingredients,
            directions=directions,
            link=link if link else None
        )

        # Display full recipe
        print()
        print(format_recipe_full(recipe))

        return 0

    except Exception as e:
        print(f"❌ Error reading recipe: {e}")
        return 1


def cmd_pantry(args):
    """Handle 'pantry' command."""
    emb = RecipeEmbeddings(dimension=args.dim)

    # Get pantry ingredients
    if args.file:
        pantry = load_pantry_from_file(args.file)
        print(f"Loaded {len(pantry)} ingredients from {args.file}")
    elif args.ingredients:
        pantry = parse_pantry(args.ingredients)
    else:
        print("❌ Must provide either --ingredients or --file")
        return 1

    if not pantry:
        print("❌ No ingredients provided")
        return 1

    print(f"\nYour pantry ({len(pantry)} ingredients):")
    print(f"  {', '.join(pantry)}")

    # Find dataset
    package_dir = Path(__file__).parent.parent
    dataset_path = package_dir / "data" / "dataset" / "full_dataset.csv"

    if not dataset_path.exists():
        print(f"\n❌ Dataset not found: {dataset_path}")
        print("Run extract_ingredients.py first to download and process the dataset.")
        return 1

    # Load database
    print(f"\nSearching recipe database...")
    db = RecipeDatabase(str(dataset_path))

    # Load recipes (limit for performance)
    max_recipes = args.max_recipes if hasattr(args, 'max_recipes') else None
    high_quality = args.high_quality_only

    db.load(max_recipes=max_recipes, high_quality_only=high_quality)

    # Search
    matches = db.search_by_pantry(
        pantry=pantry,
        embeddings=emb.wv,
        min_match=args.min_match,
        similarity_threshold=args.similarity_threshold,
        use_similarity=not args.no_similarity,
        min_ingredients=args.min_ingredients,
        topn=args.top
    )

    if not matches:
        print(f"\n❌ No recipes found with >={args.min_match * 100:.0f}% match")
        print("Try lowering --min-match threshold")
        return 0

    # Display results
    print(f"\n{'='*60}")
    print(f"Found {len(matches)} recipes you can make")
    print(f"{'='*60}\n")

    for i, match in enumerate(matches, 1):
        print(f"{i}. {format_recipe_match(match, show_details=args.details, show_similar=not args.no_similarity)}")
        print()

    # Interactive mode
    if args.interactive:
        print("=" * 60)
        print("Enter a recipe number to view full details, or 'q' to quit")
        print("=" * 60)

        while True:
            try:
                choice = input("\nSelect recipe (1-{}, q to quit): ".format(len(matches))).strip().lower()

                if choice == 'q' or choice == 'quit':
                    break

                try:
                    idx = int(choice) - 1
                    if 0 <= idx < len(matches):
                        selected_match = matches[idx]
                        print()
                        print(format_recipe_full(selected_match.recipe))
                        print()
                    else:
                        print(f"❌ Please enter a number between 1 and {len(matches)}")
                except ValueError:
                    print("❌ Please enter a number or 'q' to quit")

            except (EOFError, KeyboardInterrupt):
                print("\n")
                break

    return 0


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        prog='recipe-emb',
        description='Recipe ingredient embeddings - find similarities and substitutes',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  recipe-emb similar butter
  recipe-emb pair salmon --category herbs
  recipe-emb pair chicken --category vegetables,spices --group
  recipe-emb substitute butter --exclude dairy,milk
  recipe-emb analogy "beef - meat + vegetarian"
  recipe-emb pantry --ingredients "chicken,rice,onion,garlic,soy sauce"
  recipe-emb pantry --file pantry.txt --interactive
  recipe-emb show 12345
  recipe-emb search "cream of"
  recipe-emb info

Available categories for --category flag:
  aromatics, dairy, fruits, grains, herbs, oils, protein, spices, vegetables, other

For more information: https://github.com/yourusername/recipe-embeddings
        """
    )

    parser.add_argument(
        '-d', '--dim',
        type=int,
        default=100,
        choices=[50, 100, 300],
        help='Embedding dimension (default: 100)'
    )

    subparsers = parser.add_subparsers(dest='command', help='Command to run')

    # Similar command
    parser_similar = subparsers.add_parser(
        'similar',
        help='Find similar ingredients',
        description='Find ingredients similar to the given ingredient'
    )
    parser_similar.add_argument('ingredient', help='Ingredient to query')
    parser_similar.add_argument('-n', '--top', type=int, default=10,
                               help='Number of results (default: 10)')
    parser_similar.set_defaults(func=cmd_similar)

    # Pair command
    parser_pair = subparsers.add_parser(
        'pair',
        aliases=['complement', 'with'],
        help='Suggest ingredient pairings',
        description='Find ingredients that pair well with the given ingredient',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Categories:
  aromatics    - garlic, ginger, shallot, scallion, leek, onion
  dairy        - butter, cream, cheese, milk, yogurt, ghee
  fruits       - apple, banana, lemon, lime, berries, mango
  grains       - rice, pasta, flour, bread, quinoa, couscous
  herbs        - basil, parsley, cilantro, thyme, rosemary, dill
  oils         - olive oil, vegetable oil, sesame oil, coconut oil
  protein      - chicken, beef, pork, fish, shrimp, tofu, eggs
  spices       - pepper, cumin, paprika, cinnamon, nutmeg, curry
  vegetables   - onion, tomato, pepper, carrot, celery, mushroom
  other        - everything else

Examples:
  recipe-emb pair salmon --category herbs
    → dill, chives, tarragon (herbs that pair with salmon)

  recipe-emb pair chicken --category vegetables,spices
    → onion, peppers, paprika, cumin (veggies and spices for chicken)

  recipe-emb pair pasta --category dairy --group
    → cheese varieties (grouped output)
        """
    )
    parser_pair.add_argument('ingredient', help='Ingredient to find pairings for')
    parser_pair.add_argument('-n', '--top', type=int, default=10,
                            help='Number of results (default: 10)')
    parser_pair.add_argument('-g', '--group', action='store_true',
                            help='Group results by category')
    parser_pair.add_argument('-c', '--category',
                            help='Filter by category (comma-separated): aromatics, dairy, fruits, grains, herbs, oils, protein, spices, vegetables, other')
    parser_pair.add_argument('--exclude-self', action='store_true', default=True,
                            help='Exclude variations of the same ingredient (default: True)')
    parser_pair.set_defaults(func=cmd_pair)

    # Substitute command
    parser_sub = subparsers.add_parser(
        'substitute',
        aliases=['sub'],
        help='Find ingredient substitutes',
        description='Find substitute ingredients with optional exclusions'
    )
    parser_sub.add_argument('ingredient', help='Ingredient to substitute')
    parser_sub.add_argument('-e', '--exclude',
                           help='Comma-separated words to exclude (e.g., dairy,milk)')
    parser_sub.add_argument('-n', '--top', type=int, default=10,
                           help='Number of results (default: 10)')
    parser_sub.set_defaults(func=cmd_substitute)

    # Analogy command
    parser_analogy = subparsers.add_parser(
        'analogy',
        help='Compute ingredient analogy',
        description='Compute analogy using vector arithmetic'
    )
    parser_analogy.add_argument('expression',
                               help='Analogy expression: "word1 - word2 + word3"')
    parser_analogy.add_argument('-n', '--top', type=int, default=10,
                               help='Number of results (default: 10)')
    parser_analogy.set_defaults(func=cmd_analogy)

    # Search command
    parser_search = subparsers.add_parser(
        'search',
        help='Search ingredient vocabulary',
        description='Search for ingredients matching a pattern'
    )
    parser_search.add_argument('pattern', help='Search pattern')
    parser_search.add_argument('-n', '--top', type=int, default=20,
                              help='Max results (default: 20)')
    parser_search.set_defaults(func=cmd_search)

    # Info command
    parser_info = subparsers.add_parser(
        'info',
        help='Show model information',
        description='Display information about the loaded model'
    )
    parser_info.set_defaults(func=cmd_info)

    # Show command
    parser_show = subparsers.add_parser(
        'show',
        help='Display full recipe details',
        description='Show complete recipe with ingredients and directions'
    )
    parser_show.add_argument('recipe_id', type=int, help='Recipe ID to display')
    parser_show.set_defaults(func=cmd_show)

    # Pantry command
    parser_pantry = subparsers.add_parser(
        'pantry',
        help='Find recipes from pantry contents',
        description='Search for recipes you can make with ingredients in your pantry'
    )
    parser_pantry.add_argument('-i', '--ingredients',
                              help='Comma-separated list of ingredients')
    parser_pantry.add_argument('-f', '--file',
                              help='File with ingredients (one per line)')
    parser_pantry.add_argument('-n', '--top', type=int, default=10,
                              help='Number of results (default: 10)')
    parser_pantry.add_argument('--min-match', type=float, default=0.5,
                              help='Minimum match ratio 0.0-1.0 (default: 0.5)')
    parser_pantry.add_argument('--similarity-threshold', type=float, default=0.6,
                              help='Similarity threshold for partial matches (default: 0.6)')
    parser_pantry.add_argument('--no-similarity', action='store_true',
                              help='Disable similarity-based matching')
    parser_pantry.add_argument('--high-quality-only', action='store_true',
                              help='Only use high-quality recipes (default: all sources)')
    parser_pantry.add_argument('--max-recipes', type=int,
                              help='Limit recipes to search (for testing)')
    parser_pantry.add_argument('--min-ingredients', type=int, default=3,
                              help='Minimum ingredients per recipe (default: 3, filters incomplete recipes)')
    parser_pantry.add_argument('--details', action='store_true', default=True,
                              help='Show detailed ingredient matches')
    parser_pantry.add_argument('--interactive', '-I', action='store_true',
                              help='Interactive mode: select a recipe to view full details')
    parser_pantry.set_defaults(func=cmd_pantry)

    # Parse arguments
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 0

    # Run command
    try:
        return args.func(args)
    except FileNotFoundError as e:
        print(f"❌ {e}")
        return 1
    except KeyboardInterrupt:
        print("\n\nInterrupted")
        return 130
    except Exception as e:
        print(f"❌ Error: {e}")
        if '--debug' in sys.argv:
            raise
        return 1


if __name__ == '__main__':
    sys.exit(main())
