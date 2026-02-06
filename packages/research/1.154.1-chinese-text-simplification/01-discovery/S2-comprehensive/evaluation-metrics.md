# Evaluation Metrics for Chinese Text Simplification

## The Challenge

Unlike translation (compare to reference), simplification has:
- **Multiple valid outputs** (many ways to simplify)
- **No single ground truth** (HSK 3 can be expressed many ways)
- **Dual goals**: Simplicity AND meaning preservation

## Automatic Metrics

### 1. BLEU (Bilingual Evaluation Understudy)
**What it measures**: N-gram overlap with reference simplifications

```python
from sacrebleu import corpus_bleu

references = [["这是简单的句子。", "这个句子很简单。"]]  # Multiple refs
hypothesis = ["这是简单句子。"]

score = corpus_bleu(hypothesis, references)
print(score.score)  # 0-100, higher is better
```

**Pros**: Standard, widely used
**Cons**: Rewards exact matches, penalizes valid paraphrases
**Typical scores**: 30-45 for text simplification (lower than translation)

### 2. SARI (System output vs References and Input)
**What it measures**: How well you ADD simple words, KEEP important words, DELETE complex words

```python
from easse.sari import corpus_sari

sources = ["这是一个非常复杂的句子。"]
predictions = ["这是复杂句子。"]
references = [["这是难句子。", "这个句子很难。"]]

score = corpus_sari(sources, predictions, references)
print(score)  # 0-100, higher is better
```

**Install**: `pip install easse`

**Formula**:
```
SARI = (F1_add + F1_keep + F1_delete) / 3
```

**Pros**: Designed for simplification, better than BLEU
**Cons**: Requires multiple references for accuracy

**Typical scores**: 35-45 for good simplification

### 3. HSK Vocabulary Coverage
**What it measures**: Percentage of words within target HSK level

```python
def hsk_coverage(text, target_level=3):
    words = jieba.cut(text)
    hsk_vocab = load_hsk_vocab(levels=range(1, target_level+1))

    known_words = sum(1 for w in words if w in hsk_vocab)
    return known_words / len(list(words))

coverage = hsk_coverage("这是一个简单的句子", target_level=3)
# 0.95 = 95% of words are HSK 1-3
```

**Pros**: Directly measures learner comprehension
**Cons**: Doesn't measure sentence complexity

**Targets**:
- HSK 2: 90-95% coverage
- HSK 3: 95-98% coverage
- HSK 4: 98-99% coverage

### 4. Sentence Length
**What it measures**: Average characters per sentence (simpler = shorter)

```python
avg_length = sum(len(s) for s in sentences) / len(sentences)
```

**Targets**:
- HSK 2: 8-12 characters
- HSK 3: 12-18 characters
- HSK 4: 18-25 characters

### 5. Semantic Similarity
**What it measures**: Meaning preservation (does simplification keep same meaning?)

```python
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

original = "这是一个非常复杂的句子"
simplified = "这是难句子"

emb1 = model.encode(original)
emb2 = model.encode(simplified)

similarity = util.cos_sim(emb1, emb2)
print(similarity)  # 0-1, higher is better
```

**Thresholds**:
- < 0.7: Meaning changed too much
- 0.7-0.85: Acceptable paraphrase
- > 0.85: Very similar meaning

## Human Evaluation

### Dimensions to Measure

1. **Grammaticality**: Is the simplified text fluent?
   - Scale: 1-5 (1=broken, 5=perfect)

2. **Meaning Preservation**: Does it keep the original meaning?
   - Scale: 1-5 (1=completely different, 5=identical)

3. **Simplicity**: Is it simpler than the original?
   - Scale: 1-5 (1=same difficulty, 5=much simpler)

4. **Adequacy**: Would an HSK X learner understand this?
   - Binary: Yes/No

### Evaluation Protocol

**Annotators**: 3-5 native Chinese speakers (preferably with teaching experience)

**Sample size**: 100-200 sentence pairs (random sample)

**Agreement**: Calculate inter-annotator agreement (Fleiss' kappa)
- κ > 0.6: Good agreement
- κ < 0.4: Revise guidelines

**Cost**: $500-1000 for 200 evaluations (crowdsourcing) or $2K-5K (expert annotators)

## Composite Score

Combine metrics for overall quality:

```python
def evaluate_simplification(original, simplified, references, target_hsk=3):
    # Automatic metrics
    bleu = compute_bleu([simplified], [references])
    sari = compute_sari([original], [simplified], [references])
    hsk_cov = hsk_coverage(simplified, target_hsk)
    similarity = semantic_similarity(original, simplified)

    # Composite score
    score = {
        'bleu': bleu,
        'sari': sari,
        'hsk_coverage': hsk_cov,
        'semantic_sim': similarity,
        'composite': 0.2*bleu + 0.3*sari + 0.3*hsk_cov + 0.2*similarity
    }

    # Pass criteria
    passes = (
        hsk_cov >= 0.95 and  # 95%+ HSK coverage
        similarity >= 0.75 and  # Meaning preserved
        len(simplified) < len(original)  # Actually simpler
    )

    return score, passes
```

## Benchmarking Your System

### Baseline: No Simplification
- BLEU: 0 (no match with references)
- SARI: ~30 (keeps all words, doesn't simplify)
- HSK coverage: Depends on original

### Rule-Based Target
- SARI: 35-40
- HSK coverage: 90-95%
- Semantic similarity: 0.8-0.9

### Neural Target
- SARI: 40-45
- HSK coverage: 85-95% (less controllable)
- Semantic similarity: 0.75-0.85

### MCTS Paper Results
- Best models: ~40 BLEU, ~45 SARI
- Human upper bound: ~60 SARI (multi-reference)

## Practical Validation Workflow

**Week 1: Automated**
1. Run on 1K test sentences
2. Compute BLEU, SARI, HSK coverage
3. Filter failures (< thresholds)

**Week 2: Spot Check**
1. Manual review of 100 random samples
2. Identify error patterns (what's breaking?)

**Week 3: Human Eval**
1. Formal evaluation on 200 samples
2. Calculate inter-annotator agreement
3. Iterate if needed

**Week 4: Production**
1. Deploy with monitoring
2. Log edge cases for improvement
3. Periodic re-evaluation

## Monitoring in Production

Track these metrics over time:

```python
# Log per simplification
{
    'original_length': 45,
    'simplified_length': 28,
    'hsk_coverage': 0.94,
    'semantic_similarity': 0.82,
    'inference_time_ms': 250
}

# Alert if:
# - HSK coverage < 0.90 (too hard)
# - Semantic similarity < 0.70 (meaning drift)
# - Inference time > 500ms (too slow)
```

## Error Analysis

**Common failure modes**:

1. **Over-simplification**: "研究表明" → "说" loses academic tone
   - Fix: Be more conservative with replacements

2. **Under-simplification**: Didn't simplify hard words
   - Fix: Expand synonym dictionary

3. **Meaning drift**: "银行" (bank) → "河边" (riverbank) wrong context
   - Fix: Use POS tags or context-aware rules

4. **Unnatural output**: "非常的好" (ungrammatical)
   - Fix: Add grammar validation post-processing

## Tools

**Libraries**:
- `sacrebleu`: BLEU calculation
- `easse`: SARI and other simplification metrics (English-focused but adaptable)
- `sentence-transformers`: Semantic similarity
- `jieba`: Segmentation for HSK coverage

**MCTS eval scripts**: https://github.com/blcuicall/mcts (includes HSK evaluator)

## Verdict

**MVP evaluation** (fast):
- HSK coverage (must-have)
- Sentence length reduction
- Manual spot-checks (50 samples)

**Production evaluation** (rigorous):
- SARI (automatic)
- Semantic similarity (automatic)
- Human eval (200 samples, quarterly)

**Research evaluation** (comprehensive):
- All automatic metrics
- Human eval (500+ samples)
- Inter-annotator agreement
- Error analysis by category

## Sources
- [SARI Paper](https://aclanthology.org/Q16-1029/)
- [MCTS Paper](https://arxiv.org/abs/2306.02796)
- [easse Library](https://github.com/feralvam/easse)
- [SacreBLEU](https://github.com/mjpost/sacrebleu)
