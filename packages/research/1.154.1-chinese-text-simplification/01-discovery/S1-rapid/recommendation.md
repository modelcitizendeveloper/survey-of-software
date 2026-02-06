# S1-rapid Recommendations

## Executive Summary

**Finding**: No pip-installable libraries exist specifically for Chinese text simplification as of 2026. This is a **BUILD, not BUY** problem.

**Recommended approach**: Hybrid stack combining existing NLP libraries (jieba, OpenCC, HSK-Character-Profiler) with custom simplification logic.

**Timeline**: 2-4 weeks for MVP (rule-based), 2-4 months for production system

**Cost**: $5K-$35K Year 1 depending on complexity

---

## Key Findings from S1-rapid

### 1. Library Landscape (Reality Check)

**What EXISTS**:
✅ Text segmentation (jieba, HanLP)
✅ Traditional/Simplified conversion (OpenCC, hanziconv)
✅ Readability analysis (HSK-Character-Profiler)
✅ NLP foundations (HanLP, LTP)
✅ Training datasets (MCTS - 691K parallel sentences)

**What DOESN'T exist**:
❌ Production-ready text simplification libraries (pip-installable)
❌ Pre-trained simplification models (load-and-use)
❌ Turnkey solutions (like English has Rewordify)

**Gap**: Chinese text simplification is 3-5 years behind English in terms of library maturity.

### 2. Three Viable Approaches

#### Option A: Rule-Based (Recommended for MVP)
**Stack**: jieba + OpenCC + HSK vocabulary + custom rules
**Timeline**: 2-4 weeks
**Cost**: $5K-$15K
**Pros**:
- Fast to implement
- Predictable results
- Easy to debug and maintain
- No ML expertise required

**Cons**:
- Limited to word replacement (can't restructure sentences well)
- Needs manual synonym dictionary curation
- Struggles with idioms and context

**Success rate**: 70-80% of sentences

#### Option B: Neural (Research-Grade)
**Stack**: MCTS dataset + transformer model (T5/BART) + GPU training
**Timeline**: 2-4 months
**Cost**: $20K-$60K (development + GPU)
**Pros**:
- Can handle complex restructuring
- Improves with more data
- Handles idioms better

**Cons**:
- Requires ML expertise
- Unpredictable output (may generate fluent but incorrect text)
- Slower inference
- Hard to control exact output level

**Success rate**: 80-90% (but 10-20% errors can be severe)

#### Option C: Hybrid (Production-Ready)
**Stack**: Rule-based for common cases + neural for complex cases
**Timeline**: 2-3 months
**Cost**: $15K-$35K
**Pros**:
- Best of both worlds
- Rules handle 70%, neural handles remaining 30%
- Fallback logic (if neural fails, use rule output)

**Cons**:
- More complex architecture
- Requires both rule curation AND model training

**Success rate**: 85-95%

---

## Decision Matrix

| Scenario | Recommended Approach | Rationale |
|----------|---------------------|-----------|
| MVP / Prototype (< 1 month) | **Rule-based** | Fastest time to value |
| Language learning app (1K-10K texts/month) | **Rule-based → Hybrid** | Start simple, upgrade if needed |
| Large platform (> 10K texts/month) | **Hybrid** | ROI justifies complexity |
| Research / Publishing | **Neural** | Accuracy matters more than speed |
| Accessibility (government docs) | **Rule-based** | Predictability matters |

---

## Recommended MVP Stack

**Goal**: Working text simplification in 2-4 weeks

### Components

1. **jieba** - Text segmentation
   ```bash
   pip install jieba
   ```

2. **OpenCC** - Traditional/Simplified normalization
   ```bash
   pip install opencc-python-reimplemented
   ```

3. **HSK-Character-Profiler** - Difficulty validation
   ```bash
   git clone https://github.com/Ancastal/HSK-Character-Profiler
   ```

4. **HSK Vocabulary Lists**
   ```bash
   git clone https://github.com/krmanik/HSK-3.0
   ```

5. **Custom logic** (you build):
   - Synonym dictionary (HSK 6→3 word mappings)
   - Sentence splitting rules
   - Idiom handling

### Implementation Steps

**Week 1**: Infrastructure
- Set up jieba segmentation pipeline
- Integrate OpenCC for normalization
- Load HSK vocabulary lists
- Set up HSK-Character-Profiler for validation

**Week 2**: Simplification logic
- Build synonym dictionary (map 500 common HSK 4-6 words to HSK 2-3 equivalents)
- Implement word replacement logic
- Add sentence splitting (sentences > 20 chars)

**Week 3**: Quality assurance
- Test on sample texts
- Native speaker validation
- Fix edge cases (names, numbers, idioms)

**Week 4**: Deployment
- Build API endpoint
- Add caching
- Performance optimization

---

## What to Build Yourself

### 1. Synonym Dictionary (Critical)

**Format**:
```json
{
  "复杂": {
    "hsk_level": 4,
    "synonyms": {
      "3": ["难"],
      "2": ["难"]
    }
  },
  "研究": {
    "hsk_level": 4,
    "synonyms": {
      "3": ["学习"],
      "2": ["学"]
    }
  }
}
```

**Sources for building**:
- HSK vocabulary lists (levels 1-6 or 1-9)
- Chinese learner dictionaries
- Manual curation by native speakers

**Effort**: 1-2 weeks for 500-1000 words

### 2. Simplification Rules

**Word replacement**:
```python
def simplify_word(word, target_hsk=3):
    if word_hsk_level(word) <= target_hsk:
        return word  # Already simple enough

    synonym = synonym_dict[word]['synonyms'].get(str(target_hsk))
    return synonym if synonym else word
```

**Sentence splitting**:
```python
def split_long_sentence(sentence, max_length=15):
    if len(sentence) <= max_length:
        return [sentence]

    # Find split points (commas, conjunctions)
    # Split and return list of shorter sentences
```

**Idiom handling**:
```python
def simplify_idiom(text):
    # Replace 4-character idioms with plain explanations
    idiom_map = {
        "一举两得": "一次做两件事",
        "画蛇添足": "做多余的事"
    }
    # Replace in text
```

### 3. Quality Validation

```python
from hsk_profiler import analyze

def validate_simplification(original, simplified, target_hsk=3):
    # 1. Check difficulty
    difficulty = analyze(simplified)
    if difficulty > target_hsk:
        return False, "Still too difficult"

    # 2. Check meaning preservation
    # (You need semantic similarity metric)
    similarity = compute_similarity(original, simplified)
    if similarity < 0.7:
        return False, "Meaning changed too much"

    return True, "OK"
```

---

## Common Pitfalls to Avoid

1. **Over-simplification**
   - Don't replace every word blindly
   - Keep domain-specific terms (if learner needs them)
   - Maintain natural flow

2. **Segmentation errors compound**
   - Jieba mistakes → wrong word boundaries → wrong replacements
   - Add custom dictionary for your domain

3. **Context blindness**
   - "银行" = bank (financial) or riverbank
   - Rule-based can't distinguish without context
   - Solution: Use POS tagging (HanLP) or accept limitation

4. **No ground truth**
   - Unlike translation (many parallel corpora), simplification has limited references
   - Solution: Human validation, iterative testing

---

## Next Steps in 4PS Research

### S2-comprehensive (Technical Depth)
- Deep dive into MCTS dataset structure
- Neural model architectures (T5, BART, mBART)
- Feature engineering for ML approaches
- Evaluation metrics (BLEU, SARI, HSK-aware metrics)

**Questions to answer**:
- How do you train a neural simplification model?
- What linguistic features correlate with simplification quality?
- How do you evaluate simplification (beyond human judgment)?

### S3-need-driven (Use Case Mapping)
- Language learning apps: Requirements and implementation
- Accessibility services: Government doc simplification
- Publishers: Educational content adaptation

**Questions to answer**:
- What accuracy threshold is "good enough" for each use case?
- What's the TCO over 3 years for each approach?
- Build vs buy decision tree

### S4-strategic (Viability & ROI)
- 3-year TCO analysis (rule-based vs neural vs hybrid)
- Break-even volume (when does automation pay off?)
- Risk assessment (what can go wrong?)

**Questions to answer**:
- At what scale does neural approach become cost-effective?
- What's the risk of meaning drift in automated simplification?
- When should you hire editors instead of building tech?

---

## S1-rapid Conclusion

**For most teams**: Start with **rule-based MVP** using jieba + OpenCC + custom logic.

**Timeline**: 2-4 weeks to working prototype
**Cost**: $5K-$15K
**Success rate**: 70-80% (good enough for MVP)

**Upgrade path**: If you hit limitations (complex sentences not simplifying well), add neural model for those cases (hybrid approach).

**Reality**: Chinese text simplification is immature compared to English. You will build custom solutions, not pip install magic.

## Sources

- [MCTS Dataset](https://github.com/blcuicall/mcts)
- [HSK-Character-Profiler](https://github.com/Ancastal/HSK-Character-Profiler)
- [jieba](https://github.com/fxsjy/jieba)
- [OpenCC](https://github.com/BYVoid/OpenCC)
- [HanLP](https://hanlp.hankcs.com/)
- [HSK 3.0 Lists](https://github.com/krmanik/HSK-3.0)
