# Recipe Embeddings: Data Sources

**Goal**: Document available recipe datasets for training ingredient embeddings.

**Recommendation**: RecipeNLG (2.2M recipes) - requires manual download from official website.

---

## Primary Source: RecipeNLG

### Overview
- **Name**: RecipeNLG: A Cooking Recipes Dataset for Semi-Structured Text Generation
- **Size**: 2,231,142 recipes (2.2M)
- **Quality Subset**: 1.6M "Gathered" recipes (filter: `source=0`)
- **Language**: English
- **Year**: 2020
- **License**: Non-commercial research and educational use only

### Data Structure
```json
{
  "id": 0,
  "title": "No-Bake Nut Cookies",
  "ingredients": [
    "1 c. firmly packed brown sugar",
    "1/2 c. evaporated milk",
    "1/2 tsp. vanilla",
    "1/2 c. broken nuts (pecans)",
    "2 Tbsp. butter or margarine",
    "3 1/2 c. bite size shredded rice biscuits"
  ],
  "directions": [...],
  "link": "www.cookbooks.com/Recipe-Details.aspx?id=44874",
  "source": 0,  // 0=Gathered (high quality), 1=Recipes1M
  "ner": ["brown sugar", "milk", "vanilla", "nuts", "butter", "rice biscuits"]
}
```

### Why This Field is Perfect
The `ner` (Named Entity Recognition) field contains **pre-parsed ingredient entities**:
- Removes quantities: "1 c. brown sugar" → "brown sugar"
- Removes modifiers: "1/2 tsp. vanilla" → "vanilla"
- Clean tokenization ready for Word2Vec

### Download Methods

**Option 1: Official Website** (Recommended but currently inaccessible)
- URL: recipenlg.cs.put.poznan.pl
- Direct download of full dataset
- Status: Website appears down/minimal as of 2026-02-02

**Option 2: Hugging Face** (Issue: Old script format)
- URL: https://huggingface.co/datasets/mbien/recipe_nlg
- Issue: Uses deprecated loading script (not Parquet)
- Error: `RuntimeError: Dataset scripts are no longer supported`
- Workaround needed: Manual parquet conversion or wait for dataset update

**Option 3: Kaggle**
- URL: https://www.kaggle.com/datasets/paultimothymooney/recipenlg
- Requires Kaggle account and API setup
- May have older version

**Option 4: GitHub (Scripts only)**
- URL: https://github.com/Glorf/recipenlg
- Contains processing scripts, not full dataset
- Points back to official website for data

### Current Status (2026-02-02)
- **Attempted**: Hugging Face download via `datasets` library
- **Result**: Failed due to deprecated script format
- **Workaround**: Need manual download or dataset format update
- **Alternative**: Using lite version (7k recipes) for pipeline testing

### Next Steps
1. Contact dataset authors for updated download link
2. Try Kaggle API download
3. Use lite version for initial development
4. Request Hugging Face parquet conversion

---

## Alternative Sources

### RecipeNLG Lite (Testing Only)

- **URL**: https://huggingface.co/datasets/m3hrdadfi/recipe_nlg_lite
- **Size**: 7,198 recipes
- **Use**: Pipeline testing, proof of concept
- **Limitation**: Too small for production embeddings (need 100k+ minimum)
- **Status**: Also has deprecated script format issue

### Spoonacular API

- **URL**: https://spoonacular.com/food-api
- **Size**: 365,000+ recipes
- **Structure**: JSON with nutrition data, diet tags, cuisine types
- **License**: Freemium (free tier available, limited calls)
- **Pros**:
  - Active maintenance
  - Rich metadata (nutrition, diets, cuisines)
  - API access (no download needed)
- **Cons**:
  - Rate limits on free tier
  - Smaller than RecipeNLG
  - Requires API key management

**Sample API call**:
```bash
curl "https://api.spoonacular.com/recipes/complexSearch?apiKey=YOUR_KEY&number=100"
```

### TheMealDB

- **URL**: https://www.themealdb.com/api.php
- **Size**: 283 meals (as of 2026)
- **License**: Free, open, crowd-sourced
- **Pros**: Completely free, simple API
- **Cons**: Too small for embeddings training
- **Use**: Validation set, manual testing

### Recipe1M+

- **Size**: 1,000,000 recipes
- **Year**: 2017
- **Status**: Subset of RecipeNLG (RecipeNLG extends this)
- **Use**: Historical comparison, baseline
- **Recommendation**: Use RecipeNLG instead (superset)

---

## Dataset Comparison

| Dataset | Recipes | Ingredients Est. | License | Download | Our Use |
|---------|---------|------------------|---------|----------|---------|
| **RecipeNLG** | 2.2M | ~5,000+ | Research only | Manual | ✅ Primary (when available) |
| RecipeNLG Lite | 7k | ~500 | Research only | Difficult | ⚠️ Testing only |
| Spoonacular | 365k | ~3,000 | Freemium | API | ⚠️ Backup option |
| TheMealDB | 283 | ~600 | Free | API | ❌ Too small |
| Recipe1M+ | 1M | ~3,000 | Research | Manual | ⚠️ Subset of RecipeNLG |

---

## Recommended Approach

### Phase 1: Pipeline Development (Now)
Use **Spoonacular API** with free tier:
- Download 10-20k recipes for pipeline testing
- Extract ingredients, train small embeddings
- Validate extraction and training pipeline
- Test CLI commands

### Phase 2: Full Scale Training (When RecipeNLG available)
Use **RecipeNLG 2.2M** for production:
- Train on full 2.2M dataset
- 5,000+ ingredient vocabulary
- Multiple dimensions (50d, 100d, 300d)
- High-quality embeddings for deployment

### Phase 3: Validation
Use **TheMealDB** for human validation:
- Small, manually curated set
- Test substitution quality
- Known-good recipes for evaluation

---

## Extraction Challenges

### Ingredient Parsing

**Raw format** (from recipes):
```
"1 c. firmly packed brown sugar"
"1/2 c. evaporated milk"
"2 Tbsp. butter or margarine"
```

**Need to extract**:
```
"brown sugar"
"milk"
"butter"
```

**Approaches**:

1. **Use RecipeNLG NER field** (best):
   - Pre-parsed ingredient entities
   - Already cleaned: "brown sugar", "milk", "vanilla"
   - Just use directly!

2. **ingredient-parser-nlp library**:
   ```python
   from ingredient_parser_nlp import parse
   result = parse("1 c. brown sugar")
   # → {name: "brown sugar", quantity: 1, unit: "cup"}
   ```

3. **Regex + Manual rules**:
   - Strip quantities: `\d+[\s\/]*(c\.|cup|tbsp|tsp|lb|oz)`
   - Remove modifiers: `(fresh|dried|chopped|minced|optional)`
   - Normalize: plurals, variants ("tomato" / "tomatoes")

**Recommendation**: Use RecipeNLG's `ner` field → already done!

---

## License Compliance

### RecipeNLG Terms

**Non-Commercial Research License**:
- ✅ Academic research
- ✅ Educational purposes
- ✅ Open-source tools (non-commercial)
- ❌ Commercial applications (without permission)
- ⚠️ Attribution required (cite paper)

**Our use case**:
- Research project exploring embeddings methodology ✅
- Open-source CLI tool ✅
- Potential future commercialization: Need to contact authors

**Citation required**:
```bibtex
@inproceedings{bien-etal-2020-recipenlg,
    title = "{R}ecipe{NLG}: A Cooking Recipes Dataset for Semi-Structured Text Generation",
    author = "Bie{\'n}, Micha{\l} and Gilski, Micha{\l} and Maciejewska, Martyna and Taisner, Wojciech and Wisniewski, Dawid and Lawrynowicz, Agnieszka",
    booktitle = "Proceedings of the 13th International Conference on Natural Language Generation",
    year = "2020",
    url = "https://www.aclweb.org/anthology/2020.inlg-1.4",
    pages = "22--28",
}
```

---

## Download Script

Located at: `recipe-embeddings/scripts/download_recipenlg.py`

**Current status**: Configured for RecipeNLG lite (7k recipes) due to download issues.

**To use full dataset** (when available):
```python
# Update download_recipenlg.py line 25:
dataset = load_dataset("mbien/recipe_nlg")  # When script format fixed
# OR
dataset = load_dataset("parquet", data_files="recipenlg.parquet")  # Manual download
```

---

## Next Steps

1. ✅ Document data sources (this file)
2. ⏳ Attempt Kaggle download or contact dataset authors
3. ⏳ Use Spoonacular API for initial pipeline (10-20k recipes)
4. ⏳ Build extraction pipeline with NER field
5. ⏳ Train test embeddings (50d, 100 ingredients)
6. ⏳ Validate with small set before full-scale training

---

## References

- RecipeNLG Paper: https://www.aclweb.org/anthology/2020.inlg-1.4
- Hugging Face: https://huggingface.co/datasets/mbien/recipe_nlg
- GitHub: https://github.com/Glorf/recipenlg
- Spoonacular API: https://spoonacular.com/food-api
- TheMealDB: https://www.themealdb.com/api.php
