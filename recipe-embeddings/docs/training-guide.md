# Word2Vec Training Guide

## Overview

The training script (`scripts/train_embeddings.py`) trains ingredient embeddings using the Word2Vec skip-gram algorithm on 2.2M recipes.

## Quick Start

```bash
# Train all models (50d, 100d, 300d)
uv run python scripts/train_embeddings.py

# Expected runtime: 10-20 minutes for all three models
```

## Output

Models will be saved to `models/`:

```
models/
├── recipe_embeddings_50d.model          # Full model (retrainable)
├── recipe_embeddings_50d.kv             # Vectors only (faster loading)
├── recipe_embeddings_50d.txt            # Text format (human-readable)
├── recipe_embeddings_50d_metadata.json  # Training config & stats
├── recipe_embeddings_50d_sample.json    # Top 100 ingredients with vectors
├── recipe_embeddings_100d.*             # Same for 100d
└── recipe_embeddings_300d.*             # Same for 300d
```

## Configuration Choices

### Algorithm: Skip-gram
- **Why**: Better for rare ingredients (long-tail distribution)
- **Alternative**: CBOW (faster, but worse for rare words)
- **Setting**: `sg=1`

### Dimensions: 50d, 100d, 300d
- **50d**: Fast queries, lower quality, good for mobile/web
- **100d**: Best balance (food2vec used this), production default
- **300d**: Maximum quality, research/comparison
- **Why multiple**: Compare quality vs performance trade-offs

### Window Size: 5
- **Meaning**: Consider 5 ingredients to the left and right as context
- **Rationale**: Average recipe has 8.5 ingredients, window=5 captures most
- **Note**: Recipes are unordered sets (unlike sentences)

### Min Count: 20
- **Meaning**: Ingredient must appear in ≥20 recipes to be included
- **Rationale**: Filters typos while keeping rare dietary alternatives
- **Effect**: Reduces vocab from 198k → ~50k ingredients
- **Threshold**: 0.001% of 2.2M recipes

### Epochs: 10
- **Meaning**: Iterate over full dataset 10 times
- **Rationale**: Standard for word embeddings (BERT, Word2Vec papers)
- **Alternative**: Monitor loss, add more if needed

### Negative Sampling: 15
- **Meaning**: Use 15 negative examples per positive example
- **Rationale**: Higher for large datasets (default is 5)
- **Effect**: Better quality distinctions with more data

### Workers: CPU count - 1
- **Meaning**: Parallel training across all cores
- **Rationale**: Faster training, no downside
- **Effect**: 10-30 minute training time for 2.2M recipes

### Sampling: 1e-3
- **Meaning**: Downsample frequent words like "salt"
- **Rationale**: Default works well, prevents overfitting to common words
- **Effect**: "salt" appears in 1M recipes but not every occurrence needed

## Test Analogies

The script tests these analogies automatically:

### Dietary Substitutions
```
butter - dairy + vegan = ?
→ Expected: coconut oil, olive oil, margarine

milk - dairy + vegan = ?
→ Expected: almond milk, soy milk, coconut milk

flour - wheat + gluten-free = ?
→ Expected: almond flour, rice flour, coconut flour
```

### Protein Alternatives
```
beef - meat + vegetarian = ?
→ Expected: mushrooms, tofu, lentils, beans
```

### Flavor Pairings (like food2vec)
```
egg - bacon + orange juice = ?
→ Expected: coffee, milk
```

## Expected Results

### Vocabulary Size
- Raw: 198,899 ingredients
- After min_count=20: ~30-50k ingredients
- Quality ingredients retained, typos filtered

### Training Time
- **50d**: ~3-5 minutes
- **100d**: ~5-10 minutes
- **300d**: ~10-15 minutes
- **Total**: ~20-30 minutes for all three

### Model Sizes
- **50d**: ~10MB (50 floats × 50k ingredients)
- **100d**: ~20MB
- **300d**: ~60MB

### Quality Indicators
- Similar ingredients cluster together (butter → margarine, oil, ghee)
- Analogies work (butter - dairy + vegan → coconut oil)
- Compound ingredients preserved (cream of mushroom soup)

## Comparison with food2vec (2016)

| Feature | food2vec | Our Models |
|---------|----------|------------|
| Dataset | 96k recipes | 2.2M recipes (23× larger) |
| Vocabulary | 2,087 ingredients | ~50k ingredients |
| Dimensions | 100d | 50d, 100d, 300d |
| Algorithm | Skip-gram | Skip-gram ✓ |
| Focus | Flavor pairing | Dietary substitution |
| Output | Blog post | CLI tool + API |

## Troubleshooting

### Memory Issues
- Reduce dimensions (try 50d only)
- Increase min_count to 50 or 100
- Process fewer recipes (sample first 1M)

### Training Too Slow
- Reduce workers if system becomes unresponsive
- Reduce epochs to 5 for testing
- Train only 100d first

### Poor Analogy Results
- Expected with 50d (too small)
- Try 300d for better quality
- Check if words are in vocabulary (may be filtered by min_count)
- Some analogies require cultural knowledge not in co-occurrence

## Next Steps

After training:

1. **Evaluate**: Test with known substitutions
2. **Validate**: Ask domain expert (chef, nutritionist)
3. **Build CLI**: `recipe-emb substitute butter --diet vegan`
4. **A/B Test**: Compare with food2vec results
5. **Publish**: Research paper + PyPI package

## References

- Mikolov et al. (2013): "Efficient Estimation of Word Representations in Vector Space"
- Jaan Li (2016): food2vec blog post
- RecipeNLG dataset (2020): 2.2M recipes
