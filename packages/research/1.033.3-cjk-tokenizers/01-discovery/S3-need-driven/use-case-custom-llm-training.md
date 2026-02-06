# Use Case: Training Domain-Specific Chinese LLM

## Scenario
Training a specialized LLM for Chinese medical literature. Corpus includes medical terminology, pharmaceutical names, and traditional Chinese medicine concepts not well-represented in general vocabularies.

## Requirements

### Must-Have
- ✅ Full control over vocabulary (domain terms)
- ✅ Optimized for medical Chinese (not general Chinese)
- ✅ Training from custom corpus
- ✅ Reproducible tokenization
- ✅ Academic/research-friendly license

### Nice-to-Have
- Fast training process
- Easy experimentation with different vocab sizes
- Compatible with major training frameworks (PyTorch, JAX)
- Published methodology (for papers)

### Constraints
- **Corpus:** 500M tokens of medical Chinese
- **Timeline:** 6 months research project
- **Team:** 2 researchers + compute cluster
- **Output:** Model + paper publication

## Candidate Evaluation

### tiktoken
- ❌ **No training capability**
- ❌ Cannot customize vocabulary
- N/A Not applicable to this use case

**Fit:** 0% - Fundamentally wrong tool

### SentencePiece
- ✅ Full training control
- ✅ Optimize for domain corpus
- ✅ Multiple algorithms (BPE, unigram, char)
- ✅ Reproducible (fixed seed)
- ✅ Apache 2.0 license
- ✅ Well-documented for research
- ✅ PyTorch integration via `tokenizers`
- ⚠️ Slower training (hours on CPU)

**Fit:** **95% - Purpose-built for this**

**Training example:**
```python
import sentencepiece as spm

spm.SentencePieceTrainer.train(
    input='medical_chinese_corpus.txt',
    model_prefix='medical_zh',
    vocab_size=64000,  # Larger for medical terms
    character_coverage=0.9995,
    split_by_whitespace=False,
    model_type='unigram',
    user_defined_symbols=['<DRUG>', '<DISEASE>', '<SYMPTOM>']  # Special tokens
)
```

### HuggingFace Tokenizers
- ✅ Training capability
- ✅ Fast training (Rust backend)
- ✅ Custom vocabulary
- ✅ Framework integration
- ✅ Reproducible
- ⚠️ **Less documentation for custom training**
- ⚠️ **Fewer algorithm choices than SentencePiece**

**Fit:** 80% - Capable but less established for research

## Gap Analysis

**Primary consideration:** Research reproducibility and documentation.

**SentencePiece advantages:**
- Extensive academic citations (can reference in papers)
- Clear methodology documentation
- Known behavior across different corpora
- Multiple published papers using SentencePiece for domain-specific tokenization

**HF Tokenizers advantages:**
- Faster iteration (train in minutes vs hours)
- Native integration with `transformers` library
- Modern Rust codebase

## Trade-off Decision

| Factor | SentencePiece | HF Tokenizers |
|--------|---------------|---------------|
| Research legitimacy | ✅✅✅ Established | ✅✅ Growing |
| Training speed | ❌ Hours | ✅ Minutes |
| Documentation | ✅✅✅ Excellent | ✅✅ Good |
| Flexibility | ✅✅✅ Maximum | ✅✅ High |
| Publication track record | ✅✅✅ Many papers | ✅ Some papers |

## Domain-Specific Considerations

Medical terminology examples:
- 阿司匹林 (aspirin) - Should be single token
- 糖尿病 (diabetes) - Should be single token
- 中医 (TCM) - Common bigram, should merge

**SentencePiece's unigram model** excels here because:
1. Probabilistic segmentation adapts to domain frequency
2. Can explicitly add domain terms as user-defined symbols
3. Handles both modern medical terms and classical Chinese medical texts

## Experimental Workflow

**With SentencePiece:**
```bash
# Experiment 1: 32k vocab
spm_train --vocab_size=32000 ...

# Experiment 2: 64k vocab
spm_train --vocab_size=64000 ...

# Experiment 3: BPE vs unigram
spm_train --model_type=bpe ...
```

Easy to run multiple experiments, compare results, cite methodology.

**With HF Tokenizers:**
Faster iteration but less established methodology for reporting.

## Recommendation

**SentencePiece** - The research-grade choice for custom vocabulary training.

**Confidence:** Very High (95%)

**Rationale:**
1. Established methodology for academic publication
2. Explicit support for domain-specific training
3. Flexible algorithm choices (unigram particularly good for medical text)
4. Reproducible results well-documented in literature

**When to use HF Tokenizers instead:**
- If speed of experimentation is critical (training 10+ models/day)
- If already deeply integrated into HuggingFace ecosystem
- If publication is less important than production deployment

**Best practice:** Use SentencePiece for research phase, optionally convert to HF Tokenizers format for production deployment (best of both worlds).
