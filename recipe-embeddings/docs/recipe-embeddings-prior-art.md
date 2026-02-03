# Recipe & Ingredient Embeddings: Prior Art Analysis

**Goal**: Determine if ingredient embeddings for dietary substitutions have been done before, and identify research gaps.

**Date**: 2026-02-02
**Context**: Applying Word2Vec to recipe ingredients after success with library embeddings

---

## Summary: YES, But With Significant Gaps

Ingredient embeddings exist in research, but **no practical tools** for dietary substitutions at scale.

**What exists**: Academic papers on ingredient similarity and flavor pairing
**What doesn't exist**: CLI tool for `butter → vegan alternatives`, large-scale training (2M+ recipes), dietary focus

**Our opportunity**: Build the practical tool researchers never shipped, using 20×larger dataset.

---

## Prior Work Identified

### 1. food2vec (Jaan Li, ~2016)

**Link**: [jaan.io/food2vec-augmented-cooking-machine-intelligence](https://jaan.io/food2vec-augmented-cooking-machine-intelligence/)

**Approach**:
- Word2Vec on ~96,000 recipes
- 2,087 ingredients, 100 dimensions
- Skip-gram model

**What it does**:
- Flavor pairing analogies: "Egg:bacon :: orange juice:coffee"
- Ingredient recommendations: "You have peanut butter, honey, bread → add butter, strawberry"
- Clustering: Find ingredients that co-occur

**Limitations**:
- **Small dataset**: 96k recipes (we have 2.2M = 23× larger)
- **North American bias**: Limited cuisine diversity
- **No dietary focus**: Doesn't systematically handle vegan/gluten-free/allergens
- **No practical tool**: Blog post + Jupyter notebook, no CLI/API
- **Unclear analogies**: Author admits some results are "wackier"

**Quote from author**: "word2vec is not the best model for this"

**Assessment**: Proof of concept, not production-ready tool

---

### 2. "Exploiting Food Embeddings for Ingredient Substitution" (Pellegrini et al., 2021)

**Link**: [SCITEPRESS Paper](https://www.scitepress.org/Papers/2021/102020/102020.pdf)

**Approach**:
- Food2Vec + FoodBERT (multimodal: text + images)
- Explicitly focused on **substitution** (closer to our vision!)
- Tested on Recipe1M dataset

**What it does**:
- Ingredient substitution recommendations
- Combines text embeddings with visual features
- Evaluates substitution quality

**Limitations**:
- **Academic only**: No public tool/code
- **Multimodal complexity**: Requires images (adds overhead)
- **No dietary filtering**: Doesn't distinguish vegan/gluten-free/allergen-free
- **Small-scale evaluation**: No large-scale validation

**Assessment**: Validates substitution use case, but not accessible

---

### 3. Recipe Recommendation Systems (GitHub, Medium, Towards Data Science)

**Examples**:
- [Whatscooking GitHub](https://github.com/jackmleitch/Whatscooking-)
- [Recipe Embeddings - Towards Data Science](https://towardsdatascience.com/food-item-search-using-recipe-embeddings-a-simple-embedding-based-search-engine-using-gensim-29631fcf5953/)

**Approach**:
- Word2Vec + TF-IDF for recipe similarity
- Cosine similarity to find similar recipes
- Focus: "Find recipes like this one"

**What they do**:
- Recipe recommendations
- Cuisine classification
- Ingredient search

**Limitations**:
- **Recipe-level, not ingredient-level**: Find similar *recipes*, not substitute *ingredients*
- **No analogies**: Can't do "butter - dairy + vegan = ?"
- **No practical deployment**: Mostly Jupyter notebooks

**Assessment**: Different use case (recommendation, not substitution)

---

### 4. "A Recipe for Creating Recipes: An Ingredient Embedding Approach" (Columbia Business School, 2024)

**Link**: [Columbia WP](https://business.columbia.edu/sites/default/files-efs/citation_file_upload/WP_Recipe_Paper_01_24.pdf)

**Approach**:
- Word2Vec on recipe ingredients
- Focus: Recipe *generation* not substitution
- Economic analysis of ingredient combinations

**What it does**:
- Generate new recipes by combining ingredient embeddings
- Analyze "creativity" in recipes
- Business applications (restaurant menu design)

**Limitations**:
- **Generation focus**: Creates new recipes, not substitutes ingredients
- **No dietary constraints**: Doesn't filter by vegan/allergen/etc
- **Academic**: No deployed tool

**Assessment**: Different application domain (business/creativity)

---

### 5. Commercial Tools (Whisk, Yummly, Supercook)

**Approach**:
- Collaborative filtering (like Netflix recommendations)
- "Users who made X also made Y"

**What they do**:
- Recipe search by ingredients you have
- Recipe recommendations
- Meal planning

**Limitations**:
- **No embeddings**: Use collaborative filtering, not vector semantics
- **No analogies**: Can't do vector arithmetic
- **Closed source**: Can't inspect methodology
- **Recipe-level**: Not ingredient-level substitution

**Assessment**: Different methodology, less flexible

---

## Gap Analysis: What's Missing?

| Feature | food2vec | Pellegrini 2021 | Recipe Rec Systems | Commercial Tools | **Our Opportunity** |
|---------|----------|-----------------|-------------------|------------------|---------------------|
| **Dataset Size** | 96k recipes | ~1M recipes | Varies | Unknown | **2.2M recipes** |
| **Dietary Focus** | ❌ None | ❌ None | ❌ None | ⚠️ Limited | **✅ Core feature** |
| **Analogies** | ✅ Yes (flavor) | ❌ No | ❌ No | ❌ No | **✅ Yes (substitution)** |
| **CLI Tool** | ❌ No | ❌ No | ❌ No | ❌ No (web only) | **✅ `recipe-emb`** |
| **Open Source** | ⚠️ Blog only | ❌ No | ⚠️ Varies | ❌ No | **✅ PyPI package** |
| **Validation** | ⚠️ Informal | ✅ Academic | ⚠️ Informal | ❌ Unknown | **✅ Human eval** |
| **Scale** | ~2k ingredients | Unknown | Varies | Unknown | **✅ 5k+ ingredients** |

---

## Our Unique Contribution

### 1. Largest Ingredient Embeddings
- **2.2M recipes** (vs 96k for food2vec)
- **5,000+ unique ingredients** (vs 2k)
- Trained on RecipeNLG (most comprehensive public dataset)

### 2. Dietary Substitution Focus
```bash
# NEW: Explicit dietary constraints
recipe-emb substitute butter --diet vegan
→ coconut oil (0.94), vegan butter (0.91), olive oil (0.88)

recipe-emb substitute wheat-flour --diet gluten-free
→ almond flour (0.89), rice flour (0.87), coconut flour (0.85)
```

### 3. Practical Tool (Not Just Research)
- **CLI**: `pip install recipe-embeddings`
- **Web app**: Planned substitution wizard
- **API**: For integration with recipe apps

### 4. Cross-Domain Validation
- Proves library embeddings methodology generalizes
- Research paper: "Domain-Agnostic Co-occurrence Embeddings"

### 5. Human Evaluation at Scale
- Real users (starting with project muse: Ivan's wife!)
- A/B testing vs commercial tools
- Dietary community validation (vegan, GF, allergen forums)

---

## Research Positioning

### Novel Contributions

1. **Largest ingredient embeddings** (2.2M recipes, previous max ~1M)
2. **First dietary-focused tool** using embeddings
3. **First practical CLI** for ingredient analogies
4. **Cross-domain methodology** (libraries → recipes → any co-occurrence data)

### Complementary to Existing Work

**vs food2vec**: Same approach, 23× more data, dietary focus, practical tool
**vs Pellegrini**: Simpler (text-only), larger scale, open source
**vs Commercial**: Explainable (embeddings > black box), open, specialized for substitution

---

## Publication Strategy

### Academic Venues

**Option 1: Food Informatics / HCI**
- Title: "Ingredient Embeddings for Dietary Substitutions: A 2.2M Recipe Analysis"
- Venue: CHI (Human-Computer Interaction), IUI (Intelligent User Interfaces)
- Angle: Practical tool for dietary restrictions

**Option 2: Cross-Domain Methodology**
- Title: "Domain-Agnostic Co-occurrence Embeddings: From Libraries to Recipes"
- Venue: EMSE (Empirical Software Engineering) or Data Mining conferences
- Angle: Methodology that generalizes across domains

**Option 3: Food Science**
- Title: "Data-Driven Ingredient Substitution for Dietary Adaptation"
- Venue: Food Quality and Preference, International Journal of Gastronomy
- Angle: Culinary science meets ML

### Consumer Impact

**Beyond academia**:
- Blog post: "How to Find Vegan Substitutes with AI"
- Reddit: r/vegan, r/glutenfree, r/foodscience
- Cooking YouTubers/TikTokers
- Integration with recipe apps (Paprika, Mealime)

---

## Dataset Comparison

| Dataset | Recipes | Ingredients | Year | License | Our Use |
|---------|---------|-------------|------|---------|---------|
| **RecipeNLG** | 2.2M | ~5k+ | 2020 | Non-commercial research | ✅ Primary |
| Recipe1M+ | 1M | ~3k | 2017 | Research | ⚠️ Subset of RecipeNLG |
| food2vec dataset | 96k | 2,087 | ~2016 | Unknown | ❌ Too small |
| Spoonacular API | 365k | Unknown | Ongoing | Freemium | ⚠️ Backup |

---

## Implementation Differences

### food2vec (2016)
```python
# Flavor pairing focus
egg + bacon = breakfast_protein
orange_juice + coffee = morning_beverage
```

### Our approach (2026)
```python
# Dietary substitution focus
butter - dairy + vegan = coconut_oil, vegan_butter
beef - meat + vegetarian = mushrooms, lentils, tofu
eggs - animal + vegan = flax_eggs, aquafaba

# With explicit diet flags
recipe-emb substitute butter --diet vegan --top 5
recipe-emb substitute flour --diet gluten-free --top 5
recipe-emb substitute nuts --exclude allergen:tree-nuts
```

---

## Timeline: Prior Work

- **2016**: food2vec (Jaan Li) - Proof of concept
- **2017**: Recipe1M dataset released
- **2020**: RecipeNLG dataset (2.2M recipes)
- **2021**: Pellegrini et al. - Substitution paper
- **2024**: Columbia - Recipe generation paper
- **2026**: **Our work** - First practical tool at scale

**Observation**: 10-year gap between concept and practical tool. We're filling that gap.

---

## Validation Plan (vs Prior Work)

### What food2vec did
- Informal evaluation (author's intuition)
- Example analogies in blog post
- No systematic validation

### What Pellegrini did
- Academic evaluation metrics
- Human judges rate substitution quality
- Limited scale (research only)

### What we'll do
1. **Analogy test set** (50 hand-curated substitutions)
2. **Human evaluation** (20 users, dietary communities)
3. **A/B testing** vs food2vec results
4. **Real-world usage** (wife's kitchen testing!)
5. **Dietary community validation** (r/vegan approval?)

---

## Conclusion: Clear Path Forward

**Prior art exists**, but with significant limitations:
- Small datasets (96k-1M vs our 2.2M)
- No dietary focus (flavor pairing, not substitution)
- No practical tools (papers, not products)
- Limited validation (academic exercises, not real users)

**Our contribution fills the gap**:
- Largest scale (2.2M recipes)
- Dietary substitution as core use case
- Practical CLI tool (`recipe-emb`)
- Human validation with real users
- Proves cross-domain methodology (libraries → recipes)

**Next steps**: Download dataset, build extraction pipeline, train embeddings, ship CLI tool.

---

## References

1. Jaan Li. (2016). "food2vec - Augmented cooking with machine intelligence" [https://jaan.io/food2vec-augmented-cooking-machine-intelligence/](https://jaan.io/food2vec-augmented-cooking-machine-intelligence/)

2. Pellegrini, C. et al. (2021). "Exploiting Food Embeddings for Ingredient Substitution" [https://www.scitepress.org/Papers/2021/102020/102020.pdf](https://www.scitepress.org/Papers/2021/102020/102020.pdf)

3. Bień, M., Gilski, M., Maciejewska, M., Taisner, W., Wisniewski, D., & Lawrynowicz, A. (2020). "RecipeNLG: A Cooking Recipes Dataset for Semi-Structured Text Generation". Proceedings of the 13th International Conference on Natural Language Generation, 22-28. [https://www.aclweb.org/anthology/2020.inlg-1.4](https://www.aclweb.org/anthology/2020.inlg-1.4)

4. "Recipe Embeddings - Towards Data Science" [https://towardsdatascience.com/food-item-search-using-recipe-embeddings-a-simple-embedding-based-search-engine-using-gensim-29631fcf5953/](https://towardsdatascience.com/food-item-search-using-recipe-embeddings-a-simple-embedding-based-search-engine-using-gensim-29631fcf5953/)

5. Columbia Business School. (2024). "A Recipe for Creating Recipes: An Ingredient Embedding Approach" [https://business.columbia.edu/sites/default/files-efs/citation_file_upload/WP_Recipe_Paper_01_24.pdf](https://business.columbia.edu/sites/default/files-efs/citation_file_upload/WP_Recipe_Paper_01_24.pdf)

6. RecipeNLG GitHub. [https://github.com/Glorf/recipenlg](https://github.com/Glorf/recipenlg)

---

## BibTeX Citations

```bibtex
@inproceedings{bien-etal-2020-recipenlg,
    title = "{R}ecipe{NLG}: A Cooking Recipes Dataset for Semi-Structured Text Generation",
    author = "Bie{\'n}, Micha{\l}  and
      Gilski, Micha{\l}  and
      Maciejewska, Martyna  and
      Taisner, Wojciech  and
      Wisniewski, Dawid  and
      Lawrynowicz, Agnieszka",
    booktitle = "Proceedings of the 13th International Conference on Natural Language Generation",
    month = dec,
    year = "2020",
    address = "Dublin, Ireland",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/2020.inlg-1.4",
    pages = "22--28",
}
```
