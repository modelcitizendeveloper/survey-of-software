# Recipe Embeddings

**Find ingredient similarities and substitutes using AI trained on 2.2M recipes**

Recipe Embeddings uses Word2Vec embeddings trained on the RecipeNLG dataset (2.2 million recipes) to understand ingredient relationships and suggest substitutes for dietary restrictions.

## Features

- 🔍 **Find similar ingredients** - "What's similar to butter?"
- 🔄 **Smart substitutions** - "Vegan alternatives to butter?"
- 🧮 **Ingredient analogies** - "beef - meat + vegetarian = ?"
- 📖 **Vocabulary search** - "All ingredients with 'cream of'"
- 🎯 **Multiple models** - 50d (fast), 100d (balanced), 300d (quality)

## Installation

```bash
# Install with uv (recommended)
uv pip install -e .

# Or with pip
pip install -e .
```

## Quick Start

```bash
# Find similar ingredients
uv run recipe-emb similar butter

# Find vegan substitutes (exclude dairy)
uv run recipe-emb substitute butter --exclude dairy,milk

# Compute analogy
uv run recipe-emb analogy "beef - meat + vegetarian"

# Search vocabulary
uv run recipe-emb search "cream of"

# Show model info
uv run recipe-emb info
```

## Usage

### Similar Ingredients

Find ingredients similar to a given ingredient:

```bash
uv run recipe-emb similar butter
```

Output:
```
Similar to 'butter' (100d model, 12,767 ingredients):
============================================================
   1. 0.823  margarine
   2. 0.721  unsalted butter
   3. 0.715  butter +
   4. 0.644  buter
   5. 0.643  oleo
   ...
```

### Substitute Ingredients

Find substitutes with exclusions (e.g., for dietary restrictions):

```bash
# Vegan butter alternatives (exclude dairy)
uv run recipe-emb substitute butter --exclude dairy,milk

# Gluten-free flour alternatives
uv run recipe-emb substitute flour --exclude wheat,gluten

# Nut-free alternatives
uv run recipe-emb substitute "almond flour" --exclude nut,almond
```

### Ingredient Analogies

Compute vector arithmetic analogies:

```bash
# Vegetarian protein alternatives
uv run recipe-emb analogy "beef - meat + vegetarian"
# → tempeh, seitan, soy crumbles, veggie burgers

# Oil alternatives
uv run recipe-emb analogy "butter - butter + olive oil"
# → extra virgin olive oil, virgin olive oil

# Flavor pairings
uv run recipe-emb analogy "egg - bacon + orange juice"
# → coffee equivalents (breakfast beverages)
```

### Search Vocabulary

Find all ingredients matching a pattern:

```bash
uv run recipe-emb search "cream of"
# → cream of mushroom soup, cream of chicken soup, ...

uv run recipe-emb search chocolate
# → All chocolate varieties

uv run recipe-emb search -n 5 pepper
# → First 5 pepper types
```

### Model Selection

Choose between 50d (fast), 100d (balanced), or 300d (quality):

```bash
# Use 300d for highest quality
uv run recipe-emb -d 300 similar butter

# Use 50d for fastest queries
uv run recipe-emb -d 50 similar butter

# Default is 100d (best balance)
uv run recipe-emb similar butter
```

### Model Information

View model details and available models:

```bash
uv run recipe-emb info
```

Output:
```
Recipe Embeddings - Model Info
============================================================
  Dimension:    100d
  Vocabulary:   12,767 ingredients
  Model file:   models/recipe_embeddings_100d.kv
  Model size:   5.4MB

  Available models:
      50d   (  2.9MB)
    → 100d  (  5.4MB)
      300d  ( 15.1MB)

  Training data: 2.2M recipes (RecipeNLG dataset)
  Algorithm:     Word2Vec skip-gram
  ...
```

## Command Reference

| Command | Description | Example |
|---------|-------------|---------|
| `similar <ingredient>` | Find similar ingredients | `similar butter` |
| `substitute <ingredient>` | Find substitutes | `substitute butter --exclude dairy` |
| `analogy "<expression>"` | Compute analogy | `analogy "beef - meat + vegan"` |
| `search <pattern>` | Search vocabulary | `search "cream of"` |
| `info` | Show model info | `info` |

### Global Options

| Option | Description | Default |
|--------|-------------|---------|
| `-d, --dim {50,100,300}` | Model dimension | 100 |
| `-h, --help` | Show help | - |

### Command Options

| Command | Option | Description | Default |
|---------|--------|-------------|---------|
| `similar` | `-n, --top N` | Number of results | 10 |
| `substitute` | `-e, --exclude WORDS` | Comma-separated exclusions | None |
| `substitute` | `-n, --top N` | Number of results | 10 |
| `analogy` | `-n, --top N` | Number of results | 10 |
| `search` | `-n, --top N` | Max results | 20 |

## Interactive Explorer

For interactive exploration, use the explorer script:

```bash
uv run python scripts/explore_embeddings.py
```

Commands:
- `similar <ingredient>` - Find similar
- `sub <ingredient> --exclude word1,word2` - Find substitutes
- `analogy word1 - word2 + word3` - Compute analogy
- `compare <ing1> <ing2>` - Direct comparison
- `search <pattern>` - Search vocabulary
- `top [n]` - Most common ingredients
- `help` - Show help
- `quit` - Exit

## Training Your Own Models

```bash
# Extract ingredients from RecipeNLG dataset
uv run python scripts/extract_ingredients.py

# Train embeddings (50d, 100d, 300d)
uv run python scripts/train_embeddings.py

# Models saved to models/
```

See `docs/training-guide.md` for detailed training instructions.

## Dataset

**RecipeNLG** - 2.2M recipes with structured ingredient lists
- Paper: [RecipeNLG: A Cooking Recipes Dataset](https://www.aclweb.org/anthology/2020.inlg-1.4)
- License: Non-commercial research only
- Vocabulary: 198,899 raw ingredients → 12,767 after filtering (min_count=20)

## Model Architecture

- **Algorithm**: Word2Vec skip-gram
- **Window**: 5 (contextual co-occurrence)
- **Min count**: 20 (filters rare ingredients)
- **Dimensions**: 50d, 100d, 300d
- **Training epochs**: 10
- **Negative sampling**: 15

## Prior Art & Comparison

| Feature | food2vec (2016) | Recipe Embeddings (2026) |
|---------|----------------|--------------------------|
| Dataset | 96k recipes | 2.2M recipes (23× larger) |
| Vocabulary | 2,087 ingredients | 12,767 ingredients |
| Dimensions | 100d | 50d, 100d, 300d |
| Focus | Flavor pairing | Dietary substitution |
| Availability | Blog post | CLI tool + models |
| Multi-word ingredients | Unknown | ✅ Preserved ("cream of mushroom soup") |

## Use Cases

### Dietary Restrictions
```bash
# Vegan cooking
recipe-emb substitute butter --exclude dairy,milk,egg
recipe-emb substitute chicken --exclude meat,poultry

# Gluten-free
recipe-emb substitute flour --exclude wheat,gluten

# Allergy-safe
recipe-emb substitute "peanut butter" --exclude nut,peanut
```

### Recipe Adaptation
```bash
# Find flavor equivalents
recipe-emb similar "soy sauce"

# Seasonal substitutes
recipe-emb similar "fresh tomatoes"

# Budget alternatives
recipe-emb similar "ribeye steak"
```

### Culinary Exploration
```bash
# Discover ingredient families
recipe-emb search chocolate

# Compare ingredients
recipe-emb similar garlic

# Explore compound ingredients
recipe-emb search "cream of"
```

## Examples & Results

### Vegan Substitutions
```bash
$ uv run recipe-emb analogy "beef - meat + vegetarian"

Results:
  1. 0.554  vegan cheese
  2. 0.542  soy crumbles
  3. 0.531  tempeh
  4. 0.528  seitan
  5. 0.524  vegetarian ground beef
```

### Compound Ingredients
```bash
$ uv run recipe-emb similar "cream of mushroom soup"

Results:
  1. 0.889  mushroom soup
  2. 0.801  cream of mushroom
  3. 0.786  cream of mushroom soup or cream of chicken soup
```

### Chocolate Varieties
```bash
$ uv run recipe-emb similar chocolate

Results:
  1. 0.852  semisweet chocolate
  2. 0.848  milk chocolate
  3. 0.846  semi-sweet chocolate
  4. 0.833  bittersweet chocolate
  5. 0.823  dark chocolate
```

## Project Structure

```
recipe-embeddings/
├── recipe_emb/           # CLI tool package
│   ├── __init__.py
│   └── cli.py           # Main CLI logic
├── scripts/
│   ├── extract_ingredients.py    # Data extraction
│   ├── train_embeddings.py       # Model training
│   └── explore_embeddings.py     # Interactive explorer
├── models/              # Trained embeddings (not in git)
│   ├── recipe_embeddings_50d.kv
│   ├── recipe_embeddings_100d.kv
│   └── recipe_embeddings_300d.kv
├── data/                # Dataset (not in git)
│   ├── dataset/         # RecipeNLG CSV
│   └── processed/       # Extracted ingredients
├── docs/                # Documentation
│   ├── training-guide.md
│   ├── data-sources.md
│   └── recipe-embeddings-prior-art.md
├── pyproject.toml       # Package config
└── README.md           # This file
```

## Performance

| Model | Size | Load Time | Query Time | Quality |
|-------|------|-----------|------------|---------|
| 50d | 2.9MB | ~0.5s | ~0.01s | Good |
| 100d | 5.4MB | ~1s | ~0.02s | Better |
| 300d | 15.1MB | ~2s | ~0.05s | Best |

## Limitations

- **Vocabulary filtered**: min_count=20 removes rare ingredients (< 0.001%)
- **Abstract concepts not represented**: "dairy", "vegan", "gluten-free" aren't ingredients
- **Co-occurrence based**: Learns from recipes, not nutrition or chemistry
- **Cultural bias**: RecipeNLG is primarily English-language recipes
- **No temporal understanding**: Can't distinguish breakfast vs dinner context well

## Future Work

- [ ] Add diet/allergen metadata to ingredients
- [ ] Train on multilingual recipes
- [ ] Incorporate nutrition data
- [ ] Add recipe generation from ingredients
- [ ] Web API and demo site
- [ ] PyPI package release
- [ ] Research paper publication

## Citation

If you use this in research, please cite:

```bibtex
@software{recipe_embeddings_2026,
  title = {Recipe Embeddings: Ingredient Similarities for Dietary Substitutions},
  author = {Your Name},
  year = {2026},
  url = {https://github.com/yourusername/recipe-embeddings}
}

@inproceedings{bien-etal-2020-recipenlg,
  title = "{R}ecipe{NLG}: A Cooking Recipes Dataset for Semi-Structured Text Generation",
  author = "Bie{\'n}, Micha{\l} and Gilski, Micha{\l} and Maciejewska, Martyna and Taisner, Wojciech and Wisniewski, Dawid and Lawrynowicz, Agnieszka",
  booktitle = "Proceedings of the 13th International Conference on Natural Language Generation",
  year = "2020",
  url = "https://www.aclweb.org/anthology/2020.inlg-1.4"
}
```

## License

- **Code**: MIT License (or your choice)
- **RecipeNLG Dataset**: Non-commercial research and educational use only
- **Trained Models**: Inherits RecipeNLG license (non-commercial)

## Contributing

Contributions welcome! Areas for improvement:
- Better dietary substitution filtering
- Nutrition-aware recommendations
- Recipe generation features
- Web interface
- Additional languages

## Acknowledgments

- RecipeNLG dataset authors (Bien et al., 2020)
- food2vec by Jaan Li (2016) - inspiration
- gensim library - Word2Vec implementation
- Claude Code - development assistance

## Contact

- Issues: [GitHub Issues](https://github.com/yourusername/recipe-embeddings/issues)
- Email: your.email@example.com
