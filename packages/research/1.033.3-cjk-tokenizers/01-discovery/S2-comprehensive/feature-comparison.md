# Feature Comparison: CJK Tokenization

## Performance Benchmarks

| Metric | tiktoken | SentencePiece | HF Tokenizers (Qwen) |
|--------|----------|---------------|----------------------|
| **Inference Speed** | 3-6× faster | Baseline | 2-4× faster |
| **Training Speed** | N/A (pre-built) | Slow (hours) | Fast (Rust) |
| **CJK Token Ratio** | 2.0-3.0× | 1.0-1.2× | 1.0-1.2× |
| **Memory (Runtime)** | Low | Medium | Low |
| **Model Size** | ~1MB | 1-10MB | 1-5MB |

## CJK Efficiency Metrics

### Character-to-Token Ratios (Lower is Better)

| Language | tiktoken (GPT-4) | SentencePiece (T5) | HF (Qwen) |
|----------|------------------|-------------------|-----------|
| **Mandarin** | 1.76× | 1.1× | 1.0× |
| **Cantonese** | 2.10× | 1.2× | 1.1× |
| **Japanese** | 2.12× | 1.3× | 1.2× |
| **Korean** | 2.36× | 1.4× | 1.3× |
| **English** | 1.0× (baseline) | 1.0× | 1.0× |

**Interpretation:** tiktoken requires 2× more tokens for same CJK content. API costs double, context windows halve.

## Feature Matrix

| Feature | tiktoken | SentencePiece | HF Tokenizers |
|---------|----------|---------------|---------------|
| **Pre-built CJK Model** | ✅ (but inefficient) | ❌ (train your own) | ✅ (Qwen, BERT-CN) |
| **Custom Training** | ❌ | ✅ | ✅ |
| **Byte-level BPE** | ✅ | ✅ (option) | ✅ |
| **Character-level** | ❌ | ✅ (option) | ✅ |
| **Unigram LM** | ❌ | ✅ | ✅ |
| **Zero-config CJK** | ❌ | ❌ | ✅ (use Qwen) |
| **Language-independent** | ✅ | ✅ | ✅ |
| **No OOV** | ✅ | ✅ (with byte fallback) | ✅ |
| **Fast Inference** | ✅✅✅ | ❌ | ✅✅ |
| **Streaming Support** | ✅ | ✅ | ✅ |
| **Normalization** | ❌ | ✅ | ✅ |

## Architecture Trade-offs

### Speed vs Efficiency

```
                    tiktoken
                       ▲
                       │ (fast, wasteful)
      Inference Speed  │
                       │
                       │           HF Tokenizers (Qwen)
                       │              ●
                       │          (fast, efficient)
                       │
                       │
                       │    SentencePiece (trained)
                       │         ●
                       │    (moderate, efficient)
                       │
                       └──────────────────────────►
                          CJK Token Efficiency
```

**Key insight:** You don't have to choose. HuggingFace Tokenizers with CJK-optimized models (Qwen) achieve both speed AND efficiency.

## Unicode Handling

| Issue | tiktoken | SentencePiece | HF Tokenizers |
|-------|----------|---------------|---------------|
| **Rare Characters** | ✅ (bytes) | ✅ (byte fallback) | ✅ |
| **Normalization** | ❌ | ✅ (NFKC options) | ✅ |
| **Traditional/Simplified** | Treated separately | Can normalize | Can normalize |
| **Emoji** | ✅ (bytes) | ✅ | ✅ |
| **Mixed Scripts** | ✅ | ✅ | ✅ |

## Training Requirements

| Aspect | tiktoken | SentencePiece | HF Tokenizers |
|--------|----------|---------------|---------------|
| **Corpus Size** | N/A | 1M-10M+ sentences | 1M-10M+ sentences |
| **Training Time** | N/A | Hours | Minutes-Hours |
| **Hardware** | N/A | CPU sufficient | GPU helpful |
| **Expertise** | None (use pre-built) | Medium | Medium |
| **Iteration Speed** | Instant | Slow | Fast |

## API Complexity

### tiktoken (Simplest)
```python
import tiktoken
enc = tiktoken.get_encoding("cl100k_base")
tokens = enc.encode("你好世界")  # [102, 23957, 99834]
```
**Lines of code:** 3
**Complexity:** Trivial

### SentencePiece (Moderate)
```python
import sentencepiece as spm
sp = spm.SentencePieceProcessor()
sp.load('cjk_model.model')
tokens = sp.encode("你好世界", out_type=int)
```
**Lines of code:** 4 (+ training pipeline)
**Complexity:** Medium

### HuggingFace (Moderate, but pre-built option)
```python
from transformers import AutoTokenizer
tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen-7B")
tokens = tokenizer.encode("你好世界")
```
**Lines of code:** 3
**Complexity:** Trivial (if using pre-built), Medium (if training custom)

## Cost Analysis (API Services)

**Scenario:** 1M characters of Chinese text

| Tokenizer | Tokens | Cost @ $0.01/1k tokens |
|-----------|--------|------------------------|
| **tiktoken (GPT-4)** | 2.1M tokens | $21.00 |
| **SentencePiece (Custom)** | 1.1M tokens | $11.00 |
| **Qwen tokenizer** | 1.0M tokens | $10.00 |

**Savings:** 50% cost reduction by using CJK-optimized tokenizer.

## Ecosystem Integration

| Ecosystem | tiktoken | SentencePiece | HF Tokenizers |
|-----------|----------|---------------|---------------|
| **OpenAI API** | ✅ Native | ❌ | ❌ |
| **HuggingFace** | Manual | ✅ | ✅✅ Native |
| **LangChain** | ✅ | ✅ | ✅ |
| **LlamaIndex** | ✅ | ✅ | ✅ |
| **Custom Models** | ✅ | ✅✅ | ✅ |

## Recommendation Matrix

| Your Situation | Best Choice |
|----------------|-------------|
| **Using OpenAI API** | tiktoken (no choice) |
| **Training custom LLM** | SentencePiece |
| **Using HuggingFace models** | HF Tokenizers (Qwen for Chinese) |
| **Speed-critical + CJK** | HF Tokenizers (Qwen) |
| **English-primary + some CJK** | tiktoken (acceptable) |
| **Multilingual balanced** | SentencePiece (custom training) |
| **Quick prototype** | HF Tokenizers (pre-built) |
| **Research/experimentation** | SentencePiece (most flexible) |

## Convergence Points

**All three agree:**
- Byte-level fallback prevents OOV
- Training data distribution matters more than algorithm choice
- English-optimized vocabularies hurt CJK
- 32k+ vocab size needed for good CJK support

**Key divergence:**
- **Speed:** tiktoken wins by 3-6×
- **Efficiency:** SentencePiece/HF-Qwen win by 2×
- **Flexibility:** SentencePiece wins (most training options)
- **Ease of use:** tiktoken/HF wins (pre-built models)

## Verdict

**No universal winner.** Choice depends on constraints:
- Speed-bound → tiktoken or HF-Qwen
- Cost-bound → SentencePiece or HF-Qwen
- Flexibility-bound → SentencePiece
- Time-bound → HF-Qwen (best balance)
