# Neural Architectures for Chinese Text Simplification

## Models That Work

### 1. mBART (Multilingual BART)
**Best for**: Chinese text simplification (multilingual pre-training helps)

```python
from transformers import MBartForConditionalGeneration, MBart50TokenizerFast

model = MBartForConditionalGeneration.from_pretrained("facebook/mbart-large-50")
tokenizer = MBart50TokenizerFast.from_pretrained("facebook/mbart-large-50", src_lang="zh_CN", tgt_lang="zh_CN")

# Fine-tune on MCTS dataset
```

**Pros**: Pre-trained on Chinese, handles seq2seq well
**Cons**: Large (600M params), slow inference
**MCTS paper results**: Not specifically tested, but BART-style models work well

### 2. mT5 (Multilingual T5)
**Best for**: Chinese when you need smaller models

```python
from transformers import MT5ForConditionalGeneration, MT5Tokenizer

model = MT5ForConditionalGeneration.from_pretrained("google/mt5-base")
tokenizer = MT5Tokenizer.from_pretrained("google/mt5-base")
```

**Sizes**: Small (300M), Base (580M), Large (1.2B)
**Pros**: Good Chinese support, multiple sizes
**Cons**: Requires more training data than BART

### 3. CPT (Chinese Pre-Trained Transformer)
**Best for**: Chinese-only tasks (no multilingual overhead)

**GitHub**: https://github.com/fastnlp/CPT
**Pros**: Optimized for Chinese, faster than mBART
**Cons**: Less widely adopted, fewer resources

## Training Setup

### Hardware Requirements

| Model Size | GPU Memory | Training Time (MCTS 691K) | Inference Speed |
|------------|------------|---------------------------|-----------------|
| mT5-small  | 16GB       | 2-3 days                  | 0.5s/sentence   |
| mT5-base   | 24GB       | 4-5 days                  | 1s/sentence     |
| mBART      | 32GB+      | 5-7 days                  | 1.5s/sentence   |

**Cloud costs**: ~$100-500 (AWS p3.2xlarge or equivalent)

### Training Pipeline

```python
# 1. Load MCTS dataset
from datasets import load_dataset
dataset = load_dataset('json', data_files={'train': 'mcts/train.jsonl'})

# 2. Tokenize
def tokenize(examples):
    inputs = tokenizer(examples['source'], max_length=128, truncation=True)
    targets = tokenizer(examples['target'], max_length=128, truncation=True)
    inputs['labels'] = targets['input_ids']
    return inputs

dataset = dataset.map(tokenize, batched=True)

# 3. Train
from transformers import Seq2SeqTrainer, Seq2SeqTrainingArguments

training_args = Seq2SeqTrainingArguments(
    output_dir="./results",
    num_train_epochs=3,
    per_device_train_batch_size=8,
    learning_rate=5e-5,
    save_steps=10000,
)

trainer = Seq2SeqTrainer(
    model=model,
    args=training_args,
    train_dataset=dataset['train'],
)

trainer.train()
```

## Fine-Tuning Strategies

### 1. Full Fine-Tuning
- Update all model weights
- Best accuracy
- Requires most GPU memory
- 3-5 epochs on MCTS: ~$200-500

### 2. LoRA (Low-Rank Adaptation)
- Update only small adapter layers
- 90% of full fine-tuning accuracy
- 1/4 the memory usage
- **Recommended for smaller teams**

```python
from peft import LoraConfig, get_peft_model

lora_config = LoraConfig(
    r=16,  # rank
    lora_alpha=32,
    target_modules=["q_proj", "v_proj"],
    lora_dropout=0.1,
)

model = get_peft_model(model, lora_config)
# Train as normal, much less memory
```

### 3. Prefix Tuning
- Add learnable prefix tokens
- Even smaller than LoRA
- Slightly lower accuracy

## Controlling Output Difficulty

**Challenge**: Neural models don't respect HSK levels by default.

**Solution 1**: Prompt engineering
```python
input_text = f"[HSK 3] {source_text}"
# Model learns to simplify to HSK 3 level
```

**Solution 2**: Separate models per level
- Train mT5-small for HSK 3
- Train mT5-small for HSK 4
- Route at inference time

**Solution 3**: Post-process with HSK validator
```python
simplified = model.generate(input)
if hsk_level(simplified) > target_level:
    # Reject and regenerate with different decoding params
```

## Decoding Strategies

### Beam Search (Standard)
```python
output = model.generate(
    input_ids,
    max_length=128,
    num_beams=5,
    early_stopping=True
)
```
**Best for**: Quality (default choice)

### Sampling
```python
output = model.generate(
    input_ids,
    max_length=128,
    do_sample=True,
    top_k=50,
    top_p=0.95,
    temperature=0.7
)
```
**Best for**: Variety (multiple simplification candidates)

### Constrained Decoding
Force output to use only HSK 1-3 vocabulary (advanced).

## Benchmarks from Literature

**MCTS paper** (2024):
- BART-based models: ~40 BLEU score
- mT5-base: ~38 BLEU score
- Human references: 100 BLEU (by definition)

**Reality check**: BLEU scores are low because simplification has multiple valid outputs. Multi-reference BLEU is more meaningful.

## Production Considerations

### Inference Optimization
- **TorchScript**: 20-30% faster
- **ONNX Runtime**: 30-50% faster
- **Model quantization**: 2-4x faster, slight quality loss
- **Batching**: 5-10x throughput improvement

### Cost at Scale
1K simplifications/day:
- **GPU inference** (T4): $50-100/month
- **CPU inference** (optimized): $20-50/month
- **Serverless** (AWS Lambda + GPU): $100-200/month

10K simplifications/day:
- Dedicated GPU server becomes cost-effective

## Verdict

**For most teams**: Start with **mT5-base + LoRA** on MCTS
- Good balance of quality and resources
- 2-3 days training on single GPU
- Deploy with ONNX for fast inference

**For research**: mBART-large (best quality)
**For production at scale**: mT5-small (fast, good enough)

## Sources
- [MCTS Paper](https://arxiv.org/abs/2306.02796)
- [mBART](https://huggingface.co/facebook/mbart-large-50)
- [mT5](https://huggingface.co/google/mt5-base)
- [LoRA](https://arxiv.org/abs/2106.09685)
