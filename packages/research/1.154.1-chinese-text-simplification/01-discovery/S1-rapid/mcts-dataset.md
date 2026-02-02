# MCTS: Multi-Reference Chinese Text Simplification Dataset

## Overview

**MCTS** is the first published multi-reference Chinese text simplification evaluation dataset, released in 2024 for the LREC-COLING conference.

**Paper**: [MCTS: A Multi-Reference Chinese Text Simplification Dataset](https://arxiv.org/abs/2306.02796)
**GitHub**: https://github.com/blcuicall/mcts
**Authors**: Ruining Chong, Luming Lu, Liner Yang, Jinran Nie, Zhenghao Liu, Shuo Wang, Shuhan Zhou, Yaoxin Li, Erhong Yang (2024)

## What It Provides

### 1. Evaluation Dataset
- **3,615 human simplifications** across **723 original sentences**
- **5 simplifications per original sentence** (multi-reference)
- Source: Penn Chinese Treebank (CTB) - news, government docs, broadcasts

### 2. Training Corpus
- **691,474 high-quality parallel training pairs** (complex ↔ simple)
- Largest scale training data in Chinese Text Simplification field (as of 2024)
- Generated via rigorous automatic screening
- Built using combination of Machine Translation + English Text Simplification

### 3. Evaluation Scripts
- `hsk_evaluate.py` - HSK-based evaluation metrics
- Benchmarking tools for comparing simplification models

## Dataset Composition

**Original sentences source**: Penn Chinese Treebank (CTB)
- Xinhua news agency reports
- Government documents
- News magazines
- Broadcasts and interviews
- Online news and web logs

**Human simplifications**:
- Professional annotators
- Multiple references per sentence (captures variation)
- Quality controlled

## What It's NOT

❌ **Not a pip-installable library** - It's a dataset, not production code
❌ **Not a pre-trained model** - No ready-to-use simplification models included
❌ **Not turnkey** - Requires ML expertise to train models from the data

## How to Use

### 1. Download the Dataset
```bash
git clone https://github.com/blcuicall/mcts
cd mcts
```

### 2. Access the Data
- `data/evaluation/` - Multi-reference evaluation set (723 sentences × 5 simplifications)
- `data/training/` - Parallel corpus (691K pairs)

### 3. Train a Model
- Use training corpus with seq2seq models (T5, BART, mBART)
- Fine-tune on Chinese text simplification task
- Evaluate on multi-reference test set

### 4. Evaluate with HSK Metrics
```bash
python hsk_evaluate.py --input your_simplifications.txt
```

## Use Cases

**For researchers**:
- Train and evaluate neural text simplification models
- Compare against multi-reference gold standard
- Publish papers on Chinese text simplification

**For product teams** (with ML resources):
- Train custom simplification models for your domain
- Fine-tune on domain-specific data after pre-training on MCTS
- Requires: ML engineers, GPU resources, 2-4 months development

**Not suitable for**:
- Quick prototypes (dataset, not library)
- Teams without ML expertise
- Production deployment without training pipeline

## Significance

**Why it matters**:
1. **First multi-reference dataset** - Previous work had single reference translations
2. **Largest training corpus** - 691K pairs vs. previous datasets with < 100K
3. **HSK-aware evaluation** - Specifically designed for learner-focused simplification

**Research impact**:
- Enables neural model development
- Standardizes evaluation (multi-reference BLEU, HSK metrics)
- Provides benchmark for comparing approaches

## Limitations

1. **Domain bias**: News/formal text (CTB source)
   - May not generalize to casual, social media, or technical text
2. **Mainland Chinese**: Simplified Chinese from mainland sources
   - Not optimized for Traditional Chinese or Taiwan/HK variants
3. **No model included**: Data only, you must build the model
4. **Static dataset**: As of 2024, no updates since publication

## Practical Path Forward

**If you want to use MCTS**:

**Option A: Train a neural model**
- Download dataset
- Set up training pipeline (T5/BART + seq2seq)
- Train on 691K corpus (requires GPU, ~$100-500 cloud cost)
- Evaluate on multi-reference test set
- Deploy model for inference
- **Timeline**: 2-4 months (with ML expertise)

**Option B: Use as inspiration**
- Study human simplifications to understand patterns
- Extract simplification rules (what words get replaced, how sentences split)
- Implement rules in code (rule-based approach)
- Use MCTS as validation (compare your output to human references)
- **Timeline**: 1-2 months (less ML-heavy)

**Option C: Hybrid**
- Use MCTS for hard cases (train small specialized model)
- Use rule-based for easy cases (word replacements)
- Combine for production system
- **Timeline**: 2-3 months

## Integration with Other Tools

MCTS pairs well with:
- **jieba**: Segment text before feeding to trained model
- **HSK-Character-Profiler**: Validate output difficulty
- **OpenCC**: Handle Traditional/Simplified conversion
- **HanLP**: Extract linguistic features for model training

## Example Workflow

```python
# 1. Segment input text
import jieba
text = "这是一段复杂的中文文本"
words = jieba.cut(text)

# 2. Simplify with MCTS-trained model
# (You must train this model first using MCTS dataset)
simplified = your_trained_model.simplify(text)

# 3. Validate output difficulty
from hsk_profiler import analyze
hsk_level = analyze(simplified)
print(f"Output difficulty: HSK {hsk_level}")
```

## Verdict

**MCTS is essential infrastructure** for research and large-scale production systems, but it's **not a quick solution** for MVPs or small teams.

**Best for**:
- Research teams publishing on Chinese NLP
- Large platforms with ML resources (> 10K texts/month to simplify)

**Not for**:
- Rapid prototypes (use rule-based instead)
- Small teams without ML expertise
- Projects with < 3 month timeline

## Sources

- [MCTS Paper (arXiv)](https://arxiv.org/abs/2306.02796)
- [MCTS ACL Anthology](https://aclanthology.org/2024.lrec-main.969/)
- [MCTS GitHub](https://github.com/blcuicall/mcts)
