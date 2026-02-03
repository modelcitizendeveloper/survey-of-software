"""Pantry-based recipe search using ingredient embeddings."""

import json
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from collections import defaultdict


@dataclass
class Recipe:
    """Recipe data structure."""
    id: int
    title: str
    ingredients: List[str]  # NER-parsed ingredient list
    source: int  # 0=Gathered, 1=Recipes1M
    raw_ingredients: Optional[List[str]] = None  # Full ingredients with quantities
    directions: Optional[List[str]] = None  # Cooking instructions
    link: Optional[str] = None  # Source URL

    def __repr__(self):
        return f"Recipe({self.id}, {self.title!r}, {len(self.ingredients)} ingredients)"


@dataclass
class RecipeMatch:
    """Recipe match result with scoring."""
    recipe: Recipe
    exact_matches: List[str]
    missing: List[str]
    similar_matches: List[Tuple[str, str, float]]  # (pantry_item, recipe_item, similarity)
    exact_score: float  # 0.0-1.0
    similarity_score: float  # 0.0-1.0
    total_score: float  # weighted combination

    def __repr__(self):
        return (f"RecipeMatch({self.recipe.title!r}, "
                f"exact={self.exact_score:.2f}, "
                f"total={self.total_score:.2f}, "
                f"missing={len(self.missing)})")


class RecipeDatabase:
    """Loads and searches recipe database."""

    def __init__(self, dataset_path: str):
        """Load recipe database from RecipeNLG CSV."""
        self.dataset_path = Path(dataset_path)
        self.recipes = []
        self._loaded = False

    def load(self, max_recipes: Optional[int] = None, high_quality_only: bool = True, force_reload: bool = False):
        """Load recipes from CSV.

        Args:
            max_recipes: Limit number of recipes (for testing)
            high_quality_only: Only load source=0 (Gathered) recipes
            force_reload: Force reload even if already loaded
        """
        if self._loaded and not force_reload:
            return

        # Reset if force reloading
        if force_reload:
            self.recipes = []
            self._loaded = False

        print(f"Loading recipes from {self.dataset_path}...")

        import pandas as pd

        # Read CSV in chunks to save memory
        chunk_size = 100000
        recipe_count = 0

        for chunk in pd.read_csv(self.dataset_path, chunksize=chunk_size):
            for idx, row in chunk.iterrows():
                # Filter by quality if requested
                if high_quality_only and row['source'] != 0:
                    continue

                # Parse NER field
                try:
                    ner = json.loads(row['NER']) if isinstance(row['NER'], str) else row['NER']

                    if ner and isinstance(ner, list):
                        # Lowercase and clean
                        ingredients = [ing.lower().strip() for ing in ner if ing]

                        if ingredients:
                            # Parse full ingredients and directions
                            raw_ingredients = None
                            directions = None
                            link = None

                            try:
                                raw_ingredients = json.loads(row['ingredients']) if isinstance(row['ingredients'], str) else row['ingredients']
                            except (json.JSONDecodeError, TypeError, KeyError):
                                pass

                            try:
                                directions = json.loads(row['directions']) if isinstance(row['directions'], str) else row['directions']
                            except (json.JSONDecodeError, TypeError, KeyError):
                                pass

                            try:
                                link = row['link'] if 'link' in row and pd.notna(row['link']) else None
                            except (KeyError, TypeError):
                                pass

                            self.recipes.append(Recipe(
                                id=row['Unnamed: 0'],
                                title=row['title'],
                                ingredients=ingredients,
                                source=row['source'],
                                raw_ingredients=raw_ingredients,
                                directions=directions,
                                link=link
                            ))
                            recipe_count += 1

                            if max_recipes and recipe_count >= max_recipes:
                                break

                except (json.JSONDecodeError, TypeError):
                    continue

            if max_recipes and recipe_count >= max_recipes:
                break

            if recipe_count % 100000 == 0:
                print(f"  Loaded {recipe_count:,} recipes...")

        self._loaded = True
        print(f"✓ Loaded {len(self.recipes):,} recipes")

    def search_by_pantry(self, pantry: List[str], embeddings,
                        min_match: float = 0.5,
                        similarity_threshold: float = 0.6,
                        use_similarity: bool = True,
                        min_ingredients: int = 3,
                        topn: int = 20) -> List[RecipeMatch]:
        """Search for recipes matching pantry contents.

        Args:
            pantry: List of ingredients in user's pantry (lowercase)
            embeddings: KeyedVectors instance (gensim word vectors)
            min_match: Minimum exact match ratio (0.0-1.0)
            similarity_threshold: Minimum similarity to count as match
            use_similarity: Use embedding similarity for partial matches
            topn: Number of results to return

        Returns:
            List of RecipeMatch objects, sorted by total_score descending
        """
        if not self._loaded:
            raise RuntimeError("Call load() first")

        matches = []
        pantry_set = set(pantry)

        for recipe in self.recipes:
            # Filter recipes with too few ingredients (incomplete NER)
            if len(recipe.ingredients) < min_ingredients:
                continue

            recipe_set = set(recipe.ingredients)

            # Exact matches
            exact_matches = list(pantry_set & recipe_set)
            exact_score = len(exact_matches) / len(recipe.ingredients)

            # Skip if below threshold
            if exact_score < min_match:
                continue

            missing = list(recipe_set - pantry_set)

            # Compute similarity matches if enabled
            similar_matches = []
            similarity_bonus = 0.0

            if use_similarity and missing and embeddings:
                for missing_ing in missing:
                    # Find best match in pantry
                    best_match = None
                    best_score = 0.0

                    for pantry_ing in pantry:
                        if pantry_ing not in exact_matches:  # Don't double count
                            sim = embeddings.similarity(pantry_ing, missing_ing) \
                                  if pantry_ing in embeddings and missing_ing in embeddings \
                                  else 0.0

                            if sim > best_score:
                                best_score = sim
                                best_match = pantry_ing

                    if best_match and best_score >= similarity_threshold:
                        similar_matches.append((best_match, missing_ing, best_score))
                        similarity_bonus += best_score

                # Normalize similarity bonus
                if len(recipe.ingredients) > 0:
                    similarity_bonus /= len(recipe.ingredients)

            # Total score: 70% exact, 30% similarity
            total_score = (exact_score * 0.7) + (similarity_bonus * 0.3)

            matches.append(RecipeMatch(
                recipe=recipe,
                exact_matches=exact_matches,
                missing=missing,
                similar_matches=similar_matches,
                exact_score=exact_score,
                similarity_score=similarity_bonus,
                total_score=total_score
            ))

        # Sort by total score
        matches.sort(key=lambda m: m.total_score, reverse=True)

        return matches[:topn]

    def get_recipe_by_id(self, recipe_id: int) -> Optional[Recipe]:
        """Get recipe by ID."""
        for recipe in self.recipes:
            if recipe.id == recipe_id:
                return recipe
        return None


def parse_pantry(pantry_input: str) -> List[str]:
    """Parse pantry input (comma-separated or newline-separated).

    Args:
        pantry_input: String of ingredients

    Returns:
        List of lowercase ingredient names
    """
    # Try comma-separated first
    if ',' in pantry_input:
        ingredients = [ing.strip().lower() for ing in pantry_input.split(',')]
    else:
        # Try newline-separated
        ingredients = [ing.strip().lower() for ing in pantry_input.split('\n')]

    # Filter empty
    return [ing for ing in ingredients if ing]


def load_pantry_from_file(file_path: str) -> List[str]:
    """Load pantry from file (one ingredient per line or comma-separated)."""
    with open(file_path) as f:
        content = f.read()

    return parse_pantry(content)


def format_recipe_full(recipe: Recipe) -> str:
    """Format full recipe details for display."""
    lines = []

    # Header
    lines.append("=" * 70)
    lines.append(f"{recipe.title}")
    lines.append(f"Recipe ID: {recipe.id}")
    lines.append("=" * 70)

    # Ingredients
    lines.append("\nINGREDIENTS:")
    if recipe.raw_ingredients:
        for i, ing in enumerate(recipe.raw_ingredients, 1):
            lines.append(f"  {i}. {ing}")
    else:
        lines.append("  (ingredients not available)")

    # Directions
    lines.append("\nDIRECTIONS:")
    if recipe.directions:
        for i, step in enumerate(recipe.directions, 1):
            # Wrap long steps
            step_lines = []
            words = step.split()
            current_line = f"  {i}. "
            indent = " " * len(current_line)

            for word in words:
                if len(current_line) + len(word) + 1 > 70:
                    step_lines.append(current_line)
                    current_line = indent + word
                else:
                    if current_line.endswith(". "):
                        current_line += word
                    else:
                        current_line += " " + word

            if current_line.strip():
                step_lines.append(current_line)

            lines.extend(step_lines)
    else:
        lines.append("  (directions not available)")

    # Source
    if recipe.link:
        lines.append(f"\nSource: {recipe.link}")

    lines.append("=" * 70)

    return '\n'.join(lines)


def format_recipe_match(match: RecipeMatch, show_details: bool = True,
                       show_similar: bool = True) -> str:
    """Format recipe match for display."""
    lines = []

    # Title and score
    score_pct = match.total_score * 100
    lines.append(f"{match.recipe.title} [ID: {match.recipe.id}]")
    lines.append(f"  Match: {score_pct:.0f}% "
                f"({len(match.exact_matches)}/{len(match.recipe.ingredients)} ingredients)")

    if show_details:
        # Exact matches
        if match.exact_matches:
            lines.append(f"  ✓ Have: {', '.join(match.exact_matches[:5])}")
            if len(match.exact_matches) > 5:
                lines.append(f"         ... and {len(match.exact_matches) - 5} more")

        # Similar matches
        if show_similar and match.similar_matches:
            similar_strs = []
            for pantry_ing, recipe_ing, sim in match.similar_matches[:3]:
                similar_strs.append(f"{pantry_ing}→{recipe_ing} ({sim:.2f})")
            lines.append(f"  ≈ Close: {', '.join(similar_strs)}")
            if len(match.similar_matches) > 3:
                lines.append(f"          ... and {len(match.similar_matches) - 3} more")

        # Missing
        if match.missing:
            missing_show = [ing for ing in match.missing
                          if ing not in [m[1] for m in match.similar_matches]]
            if missing_show:
                lines.append(f"  ✗ Need: {', '.join(missing_show[:5])}")
                if len(missing_show) > 5:
                    lines.append(f"         ... and {len(missing_show) - 5} more")

    return '\n'.join(lines)
