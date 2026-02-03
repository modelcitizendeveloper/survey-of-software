#!/usr/bin/env python3
"""Interactive tool to explore recipe ingredient embeddings.

Load trained Word2Vec models and interactively query:
- Ingredient similarity
- Analogies and substitutions
- Vocabulary exploration
- Multi-model comparison
"""

from gensim.models import KeyedVectors
from pathlib import Path
import sys


class EmbeddingExplorer:
    """Interactive exploration of ingredient embeddings."""

    def __init__(self, model_path):
        """Load embeddings from file."""
        print(f"\nLoading embeddings from {model_path}...")
        self.wv = KeyedVectors.load(str(model_path))
        print(f"✓ Loaded {len(self.wv):,} ingredients")

        # Extract dimension from filename
        self.dimension = int(model_path.stem.split('_')[-1].replace('d', ''))

    def similar(self, ingredient, topn=10, exclude_self=True):
        """Find similar ingredients."""
        if ingredient not in self.wv:
            # Try case-insensitive search
            matches = [w for w in self.wv.index_to_key if w.lower() == ingredient.lower()]
            if matches:
                ingredient = matches[0]
                print(f"(Using '{ingredient}' from vocabulary)")
            else:
                print(f"❌ '{ingredient}' not in vocabulary")
                self.suggest_alternatives(ingredient)
                return []

        similar = self.wv.most_similar(ingredient, topn=topn + 1)

        # Optionally exclude the ingredient itself
        if exclude_self:
            similar = [(w, s) for w, s in similar if w != ingredient][:topn]

        return similar

    def analogy(self, positive, negative, topn=10):
        """Compute analogy: positive[0] - negative[0] + positive[1] = ?

        Example: butter - dairy + vegan = ?
        positive = ['butter', 'vegan']
        negative = ['dairy']
        """
        # Check all words are in vocabulary
        all_words = positive + negative
        missing = [w for w in all_words if w not in self.wv]

        if missing:
            print(f"❌ Words not in vocabulary: {missing}")
            for word in missing:
                self.suggest_alternatives(word)
            return []

        try:
            result = self.wv.most_similar(positive=positive, negative=negative, topn=topn)
            return result
        except KeyError as e:
            print(f"❌ Error: {e}")
            return []

    def substitute(self, ingredient, exclude_words=None, topn=10):
        """Find substitutes, optionally excluding certain words/patterns.

        Example: Find vegan butter substitutes
        substitute('butter', exclude_words=['butter', 'dairy', 'milk'])
        """
        similar = self.similar(ingredient, topn=topn * 3, exclude_self=True)

        if exclude_words:
            exclude_lower = [w.lower() for w in exclude_words]
            filtered = []

            for word, score in similar:
                # Check if any excluded word is in the ingredient name
                if not any(exc in word.lower() for exc in exclude_lower):
                    filtered.append((word, score))

                if len(filtered) >= topn:
                    break

            return filtered

        return similar[:topn]

    def suggest_alternatives(self, word, max_suggestions=5):
        """Suggest similar vocabulary words."""
        # Find words that contain the query word
        word_lower = word.lower()
        matches = [w for w in self.wv.index_to_key if word_lower in w.lower()]

        if matches:
            print(f"\n💡 Did you mean one of these?")
            for match in matches[:max_suggestions]:
                print(f"   - {match}")
        else:
            # Find words with similar starting letters
            prefix = word_lower[:3] if len(word_lower) >= 3 else word_lower
            matches = [w for w in self.wv.index_to_key if w.lower().startswith(prefix)]

            if matches:
                print(f"\n💡 Similar words starting with '{prefix}':")
                for match in matches[:max_suggestions]:
                    print(f"   - {match}")

    def search_vocab(self, pattern, max_results=20):
        """Search vocabulary for pattern."""
        pattern_lower = pattern.lower()
        matches = [w for w in self.wv.index_to_key if pattern_lower in w.lower()]

        if matches:
            print(f"\n✓ Found {len(matches)} matches for '{pattern}':")
            for match in matches[:max_results]:
                print(f"   - {match}")

            if len(matches) > max_results:
                print(f"   ... and {len(matches) - max_results} more")
        else:
            print(f"❌ No matches found for '{pattern}'")

        return matches

    def compare_ingredients(self, ing1, ing2):
        """Compare two ingredients directly."""
        if ing1 not in self.wv:
            print(f"❌ '{ing1}' not in vocabulary")
            return None

        if ing2 not in self.wv:
            print(f"❌ '{ing2}' not in vocabulary")
            return None

        similarity = self.wv.similarity(ing1, ing2)
        return similarity

    def most_common(self, n=20):
        """Show most common ingredients (by frequency in training)."""
        print(f"\nTop {n} most frequent ingredients:")
        for i, word in enumerate(self.wv.index_to_key[:n], 1):
            print(f"  {i:2d}. {word}")


def print_results(title, results, show_scores=True):
    """Pretty print results."""
    print(f"\n{title}")
    print("=" * len(title))

    if not results:
        print("  (no results)")
        return

    for i, item in enumerate(results, 1):
        if show_scores and isinstance(item, tuple):
            word, score = item
            print(f"  {i:2d}. {score:.3f}  {word}")
        else:
            print(f"  {i:2d}. {item}")


def interactive_mode(explorer):
    """Interactive REPL for exploring embeddings."""

    def show_help():
        """Display help message."""
        print("\n" + "=" * 60)
        print(f"Recipe Embeddings Explorer ({explorer.dimension}d)")
        print("=" * 60)
        print("\nCommands:")
        print("  similar <ingredient>           - Find similar ingredients")
        print("  sub <ingredient> [--exclude]   - Find substitutes")
        print("  analogy <ing1> - <ing2> + <ing3>  - Compute analogy")
        print("  compare <ing1> <ing2>          - Compare two ingredients")
        print("  search <pattern>               - Search vocabulary")
        print("  top [n]                        - Show most common ingredients")
        print("  help                           - Show this help message")
        print("  quit / exit                    - Exit")
        print("\nExamples:")
        print("  similar butter")
        print("  sub butter --exclude dairy,milk")
        print("  analogy beef - meat + vegetarian")
        print("  compare butter margarine")
        print("  search cream of")
        print()

    show_help()

    while True:
        try:
            command = input(f"\n[{explorer.dimension}d] > ").strip()

            if not command:
                continue

            if command in ['quit', 'exit', 'q']:
                print("\nGoodbye!")
                break

            parts = command.split()
            cmd = parts[0].lower()

            if cmd == 'similar' and len(parts) >= 2:
                ingredient = ' '.join(parts[1:])
                results = explorer.similar(ingredient, topn=10)
                print_results(f"Similar to '{ingredient}':", results)

            elif cmd == 'sub' and len(parts) >= 2:
                # Parse: sub butter --exclude dairy,milk
                exclude = None
                if '--exclude' in parts:
                    idx = parts.index('--exclude')
                    ingredient = ' '.join(parts[1:idx])
                    if idx + 1 < len(parts):
                        exclude = parts[idx + 1].split(',')
                else:
                    ingredient = ' '.join(parts[1:])

                results = explorer.substitute(ingredient, exclude_words=exclude, topn=10)
                title = f"Substitutes for '{ingredient}'"
                if exclude:
                    title += f" (excluding: {', '.join(exclude)})"
                print_results(title + ":", results)

            elif cmd == 'analogy' and len(parts) >= 5:
                # Parse: analogy beef - meat + vegetarian
                # Find - and + positions
                if '-' not in parts or '+' not in parts:
                    print("❌ Format: analogy <word1> - <word2> + <word3>")
                    continue

                minus_idx = parts.index('-')
                plus_idx = parts.index('+')

                word1 = ' '.join(parts[1:minus_idx])
                word2 = ' '.join(parts[minus_idx + 1:plus_idx])
                word3 = ' '.join(parts[plus_idx + 1:])

                positive = [word1, word3]
                negative = [word2]

                print(f"\nComputing: {word1} - {word2} + {word3} = ?")
                results = explorer.analogy(positive, negative, topn=10)
                print_results("Results:", results)

            elif cmd == 'compare' and len(parts) >= 3:
                ing1 = parts[1]
                ing2 = ' '.join(parts[2:])
                similarity = explorer.compare_ingredients(ing1, ing2)
                if similarity is not None:
                    print(f"\nSimilarity: {similarity:.3f}")
                    if similarity > 0.7:
                        print("  → Very similar!")
                    elif similarity > 0.5:
                        print("  → Moderately similar")
                    elif similarity > 0.3:
                        print("  → Somewhat similar")
                    else:
                        print("  → Not very similar")

            elif cmd == 'search' and len(parts) >= 2:
                pattern = ' '.join(parts[1:])
                explorer.search_vocab(pattern)

            elif cmd == 'top':
                n = int(parts[1]) if len(parts) > 1 else 20
                explorer.most_common(n)

            elif cmd == 'help' or cmd == 'h' or cmd == '?':
                show_help()

            else:
                print("❌ Unknown command. Type 'help' for available commands.")

        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")


def quick_test(explorer):
    """Run quick tests to demonstrate functionality."""

    print("\n" + "=" * 60)
    print("Quick Test - Exploring Embeddings")
    print("=" * 60)

    # Test 1: Similarity
    test_ingredients = ['butter', 'chicken breast', 'garlic', 'chocolate']
    for ing in test_ingredients:
        if ing in explorer.wv:
            results = explorer.similar(ing, topn=5)
            print_results(f"\nSimilar to '{ing}':", results)

    # Test 2: Substitutions
    print("\n" + "-" * 60)
    print("Substitution Tests")
    print("-" * 60)

    if 'butter' in explorer.wv:
        # Vegan butter substitutes
        results = explorer.substitute('butter', exclude_words=['butter', 'milk', 'dairy'], topn=5)
        print_results("\nVegan butter substitutes (exclude dairy):", results)

    if 'chicken breast' in explorer.wv:
        # Vegetarian protein alternatives
        results = explorer.substitute('chicken breast', exclude_words=['chicken', 'meat'], topn=5)
        print_results("\nVegetarian chicken alternatives:", results)

    # Test 3: Analogies
    print("\n" + "-" * 60)
    print("Analogy Tests")
    print("-" * 60)

    analogy_tests = [
        (['beef', 'vegetarian'], ['meat'], "beef - meat + vegetarian = ?"),
        (['butter', 'olive oil'], ['butter'], "butter - butter + olive oil = ? (oils)"),
    ]

    for positive, negative, description in analogy_tests:
        print(f"\n{description}")
        results = explorer.analogy(positive, negative, topn=5)
        if results:
            print_results("Results:", results)

    # Test 4: Compound ingredients
    print("\n" + "-" * 60)
    print("Compound Ingredient Tests")
    print("-" * 60)

    compounds = ['cream of mushroom soup', 'sour cream', 'brown sugar', 'olive oil']
    for compound in compounds:
        if compound in explorer.wv:
            results = explorer.similar(compound, topn=3)
            print_results(f"\nSimilar to '{compound}':", results)


def main():
    """Main entry point."""

    models_dir = Path(__file__).parent.parent / "models"

    # Check available models (sort by file size)
    available_models = sorted(models_dir.glob("recipe_embeddings_*d.kv"),
                             key=lambda x: x.stat().st_size)

    if not available_models:
        print(f"❌ No models found in {models_dir}")
        print("Run train_embeddings.py first to train models.")
        return

    # Parse command line
    if len(sys.argv) > 1:
        # Model specified on command line
        dim = sys.argv[1].replace('d', '')
        model_file = models_dir / f"recipe_embeddings_{dim}d.kv"

        if not model_file.exists():
            print(f"❌ Model not found: {model_file}")
            print(f"\nAvailable models:")
            for model in available_models:
                print(f"  - {model.stem}")
            return

    else:
        # Show menu
        print("\nAvailable models:")
        for i, model in enumerate(available_models, 1):
            dim = model.stem.split('_')[-1]
            size_mb = model.stat().st_size / (1024 * 1024)
            print(f"  {i}. {dim} ({size_mb:.1f}MB)")

        choice = input("\nSelect model (1-3) or press Enter for 100d: ").strip()

        if not choice:
            model_file = models_dir / "recipe_embeddings_100d.kv"
        else:
            try:
                idx = int(choice) - 1
                model_file = available_models[idx]
            except (ValueError, IndexError):
                print("❌ Invalid choice")
                return

    # Load model
    explorer = EmbeddingExplorer(model_file)

    # Check mode
    mode = sys.argv[2] if len(sys.argv) > 2 else 'interactive'

    if mode == 'test':
        quick_test(explorer)
    else:
        quick_test(explorer)
        interactive_mode(explorer)


if __name__ == "__main__":
    main()
