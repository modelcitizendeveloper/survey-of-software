# Stanza - Comprehensive Assessment

## Universal Dependencies Framework

### What Stanza Provides
From [Stanza documentation](https://stanfordnlp.github.io/stanza/available_models.html):
- Tokenization & sentence segmentation
- Lemmatization
- POS tagging
- Morphological features (UD framework)
- Dependency parsing

### Chinese Models
- Trained on Universal Dependencies v2.12
- Models available for simplified and traditional Chinese
- [Performance metrics](https://stanfordnlp.github.io/stanza/performance.html) show 94%+ token accuracy

## Morphological Features in UD

### What "Morphological" Means in UD Context
UD morphological features capture grammatical properties:
- Tense, aspect, mood (for languages that have them)
- Number, gender, case
- Transitivity, politeness markers

### Chinese in UD Framework
Research findings ([Computational Linguistics](https://direct.mit.edu/coli/article/42/3/391/1538/Towards-Accurate-and-Efficient-Chinese-Part-of)):
- Chinese is an analytic language
- Lacks formal morphological devices (no tense inflections, number markers)
- "Weak morphology" compared to agglutinative or fusional languages
- UD features limited to aspect markers, classifiers, etc.

**Example UD tags for Chinese:**
- Aspect markers: 了 (le), 着 (zhe), 过 (guo)
- Classifiers: 个, 只, 本
- NOT character decomposition or internal word structure

## Character Decomposition

**None** - Stanza operates at token/word level, not character component level. UD framework doesn't model sub-character structure.

## Compound Word Analysis

**Word-level tokenization only:**
- Segments text into tokens
- Assigns grammatical tags
- Does NOT analyze morpheme composition of compounds
- Example: "电脑" (computer) = single token "电脑", not analyzed as "电" (electricity) + "脑" (brain)

### Research Context
[ACL 2020 paper](https://aclanthology.org/2020.acl-demos.14.pdf) notes:
- Stanza focuses on cross-lingual consistency
- Same annotation framework for all languages
- Chinese processing adapted to UD conventions
- Morphological analysis limited to what UD framework supports

## Production Readiness

**High:**
- ✅ Python 3 support
- ✅ pip installable: `pip install stanza`
- ✅ Stanford NLP backing
- ✅ Excellent documentation
- ✅ 80 languages supported
- ✅ Regular updates with new UD versions

## Integration with Character Analysis

**Preprocessing role only:**
- Stanza segments text into tokens
- Provides grammatical structure
- Separate tool needed for character decomposition
- UD parse trees useful for understanding word relationships

### Workflow Example
1. Input: "学习汉字很有趣"
2. Stanza tokenizes: ["学习", "汉字", "很", "有趣"]
3. POS tags: [VERB, NOUN, ADV, ADJ]
4. Dependency parse: shows "学习" as root, "汉字" as object
5. Separate tool decomposes characters: "汉" = ⿰氵又

## Verdict for Our Needs

**Grammatical morphology (UD sense): Yes**
**Character decomposition: No**
**Compound analysis (morphemes): No**

Stanza provides morphological tagging in the UD sense (grammatical features), not character decomposition or morpheme analysis. Useful for NLP pipelines but doesn't address core requirement of analyzing character structure.

### Clarification Needed

The term "morphological analysis" is ambiguous:
- **UD morphology:** Grammatical features (what Stanza does)
- **Character morphology:** Component structure (what we need)
- **Word morphology:** Compound word decomposition (unclear if needed)

Stanza addresses the first definition only.

---

Sources:
- [Stanza Available Models](https://stanfordnlp.github.io/stanza/available_models.html)
- [Stanza ACL 2020 Paper](https://aclanthology.org/2020.acl-demos.14.pdf)
- [Towards Accurate Chinese POS Tagging](https://direct.mit.edu/coli/article/42/3/391/1538/Towards-Accurate-and-Efficient-Chinese-Part-of)
