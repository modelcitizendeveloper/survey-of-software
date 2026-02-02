# S2-comprehensive Recommendations

## Neural Approach: Go/No-Go

### GO if:
- Volume > 5K texts/month (justify training cost)
- Accuracy needs > 80% (rule-based plateaus at 70-80%)
- Have ML engineer or budget for consulting
- Can tolerate 3-5% meaning drift

### NO-GO if:
- Volume < 1K texts/month (not worth complexity)
- Need 100% predictable output (use rules)
- No ML expertise and < $20K budget
- Can't accept any meaning errors

## Recommended Neural Stack

**mT5-base + LoRA** on MCTS dataset:
- 2-3 days training (single GPU, ~$150)
- Deploy with ONNX (1s/sentence CPU)
- 40-45 SARI, 85-95% HSK coverage
- LoRA = 1/4 memory of full fine-tuning

**Implementation**:
```bash
# 1. Setup
pip install transformers datasets peft onnx

# 2. Train
python train.py \
  --model google/mt5-base \
  --dataset mcts/train.jsonl \
  --epochs 3 \
  --lora_r 16 \
  --output models/mt5-lora-hsk3

# 3. Evaluate
python eval.py \
  --model models/mt5-lora-hsk3 \
  --test mcts/test.jsonl \
  --metrics sari,bleu,hsk_coverage

# 4. Deploy
python convert_to_onnx.py \
  --model models/mt5-lora-hsk3 \
  --output models/mt5-lora-hsk3.onnx
```

**Timeline**: 1 week (setup + train + eval)
**Cost**: $200-500 (cloud GPU + storage)

## Evaluation Strategy

**MVP**: HSK coverage + spot checks
- 100 test sentences
- Must achieve 95%+ HSK coverage
- Manual review of 20 samples

**Production**: SARI + semantic similarity + human eval
- Run SARI on full test set (target: 40+)
- Semantic similarity > 0.75 (meaning preserved)
- Human eval on 200 samples quarterly

**Monitoring**: Log these per-simplification
```python
{
  'hsk_coverage': 0.94,
  'semantic_similarity': 0.82,
  'inference_time_ms': 250
}
# Alert if coverage < 0.90 or similarity < 0.70
```

## Hybrid Architecture (Best of Both)

**Route by sentence complexity**:
```python
def simplify(text):
    complexity = measure_complexity(text)

    if complexity < 15:  # Simple sentence
        return rule_based_simplify(text)  # Fast, predictable

    else:  # Complex sentence
        result = neural_simplify(text)
        if validate(result):
            return result
        else:
            return rule_based_simplify(text)  # Fallback
```

**Result**: 85-90% success rate (neural handles hard cases, rules are fallback)

## S2 Key Takeaways

1. **Neural is viable** but not trivial (1 week + $500, requires ML skills)
2. **mT5-base + LoRA** = best balance (quality vs resources)
3. **SARI + HSK coverage** = must-have metrics
4. **Hybrid architecture** = production-grade (rules + neural)
5. **3-5% meaning drift** is unavoidable with neural (need human review)

**Next**: S3 maps these technical options to specific use cases with TCO models.
