#!/usr/bin/env python3
"""Command-line interface for recipe embeddings."""

import argparse
import sys
from pathlib import Path
from gensim.models import KeyedVectors
from .pantry import (RecipeDatabase, parse_pantry, load_pantry_from_file,
                     format_recipe_match)


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
  recipe-emb substitute butter --exclude dairy,milk
  recipe-emb analogy "beef - meat + vegetarian"
  recipe-emb pantry --ingredients "chicken,rice,onion,garlic,soy sauce"
  recipe-emb pantry --file pantry.txt --top 20
  recipe-emb search "cream of"
  recipe-emb info

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
    parser_pantry.add_argument('--details', action='store_true', default=True,
                              help='Show detailed ingredient matches')
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
