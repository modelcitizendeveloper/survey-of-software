# Stanza - Technical Deep Dive

## Architecture

### Design Philosophy

**"Universal Dependencies-native neural NLP toolkit"**

Stanza is Stanford's **successor to CoreNLP** for Python, designed from the ground up for:
1. Universal Dependencies (UD) training and output
2. Neural architectures (replacing CoreNLP's statistical models)
3. Native Python (no Java dependency)
4. 80+ languages with consistent API

### Pipeline Architecture

**Modular processor design**:
```
Raw Text
 ↓
TokenizeProcessor (segmentation)
 ↓
MWTProcessor (multi-word token expansion, if needed)
 ↓
POSProcessor (POS tagging)
 ↓
LemmaProcessor (lemmatization)
 ↓
DepparseProcessor (dependency parsing) ← Our focus
 ↓
NERProcessor (named entity recognition)
 ↓
SentimentProcessor (sentiment, English only)
```

**Key design principle**: Each processor is independent module with clear input/output contracts.

## Dependency Parsing Architecture

### Algorithm: Transition-Based Parsing

**Core approach**: Build dependency tree through sequence of actions

**State representation**:
- **Stack**: Partially built dependencies
- **Buffer**: Remaining words to process
- **Actions**: SHIFT, LEFT-ARC, RIGHT-ARC

**Transition system**:
1. Start with root on stack, all words in buffer
2. Neural network predicts next action
3. Apply action (build arcs, move words)
4. Repeat until buffer empty
5. Result: Complete dependency tree

### Why Transition-Based (vs Graph-Based CoreNLP)?

**Advantages**:
- **Faster inference**: Linear time O(n) for projective trees
- **Rich feature history**: Can use entire transition history
- **Greedy decoding**: No expensive MST algorithm

**Disadvantages**:
- **Local decisions**: May miss globally optimal tree
- **Error propagation**: Early mistakes affect later decisions
- **Worse at long dependencies**: Compared to graph-based

**Stanford's rationale**: Speed-accuracy trade-off favors transition-based for production use.

### Neural Architecture

**Model components**:
```
Token embeddings (character + word + pretrained)
 ↓
BiLSTM encoder (multi-layer)
 ↓
Attention mechanism (optional)
 ↓
Classifier (action prediction)
 ↓
Transition sequence → Dependency tree
```

**Key technical details**:
- **Character-level encoding**: Handles OOV (out-of-vocabulary) words
- **Pretrained embeddings**: Optional (Word2Vec, FastText, GloVe)
- **BiLSTM**: Captures bidirectional context
- **Greedy decoding**: Argmax over action space (no beam search by default)

## Technical Specifications

### Language and Dependencies

**Core**: Python 3.6+
**Framework**: PyTorch 1.3+
**Hardware**:
- CPU: Fully supported
- GPU: Automatic detection and use
- Memory: 2-4 GB typical for Chinese

### Multilingual Coverage

**80+ languages** from Universal Dependencies v2.12
- **Chinese varieties**: Simplified (GSD treebank), Classical Chinese
- **Training data**: UD treebanks (consistent cross-linguistic)
- **Model availability**: Pretrained models for all UD languages

### UD-Native Design

**Critical insight**: Stanza is **designed for UD**, not adapted to it.

**Implications**:
- Tokenization aligns with UD standards (not CTB)
- POS tagset is Universal POS (17 tags, not CTB's 33)
- Dependency relations are UD (48 relations)
- Training data is UD treebanks exclusively

**Trade-off**: Optimal for UD benchmarks; domain-specific corpora may need retraining.

## Performance Analysis

### Accuracy

**Official benchmarks** (UD v2.12 test sets):
- Evaluated end-to-end (raw text → full CoNLL-U)
- Chinese-GSD results available on Stanza performance page
- Scores use CoNLL 2018 evaluation script (standard)

**Comparison context**:
- Stanza optimized for UD benchmarks
- HanLP/LTP use different standards (CTB, Stanford Deps)
- Direct accuracy comparison requires identical evaluation setup

**Typical range** (Chinese UD GSD):
- UAS: ~85-90% (depends on Stanza version, evaluation protocol)
- LAS: ~80-85%

### Speed

**Throughput** (approximate, hardware-dependent):
- **CPU**: 50-200 sentences/sec (single-core)
- **GPU**: 500-2000 sentences/sec (batch processing)

**Optimization factors**:
- Batch size (larger batches → higher GPU utilization)
- Sequence length (longer sentences → slower)
- Pretrained embeddings (if used, slight slowdown)

**Comparison to CoreNLP**:
- Stanza ~2-5x faster on CPU (transition-based + neural batching)
- With GPU: ~10-50x faster than CoreNLP

### Resource Requirements

**Memory**:
- **Chinese models**: ~300-500 MB
- **Peak during inference**: ~1-2 GB (batch processing)
- **Minimal**: ~500 MB (single sentence, CPU)

**Disk space**:
- Models downloaded to `~/stanza_resources/`
- Chinese full pipeline: ~400 MB

**GPU memory**:
- 1-2 GB VRAM typical (batch size 32)
- Scales with batch size and sequence length

## API Design

### Pythonic Interface

**Philosophy**: Simple, consistent, predictable

**Basic usage pattern** (conceptual):
```python
import stanza
stanza.download('zh')  # One-time setup
nlp = stanza.Pipeline('zh', processors='tokenize,pos,lemma,depparse')
doc = nlp("他爱北京")
for sentence in doc.sentences:
    for word in sentence.words:
        print(f"{word.text} -> {word.head} ({word.deprel})")
```

**Key features**:
- Automatic processor chaining (handles dependencies)
- Lazy model loading (first inference)
- GPU auto-detection (no manual device management)

### Document Model

**Structured output**:
```
Document
 ├─ Sentence 1
 │   ├─ Word 1 (id, text, lemma, upos, xpos, feats, head, deprel)
 │   ├─ Word 2
 │   └─ ...
 ├─ Sentence 2
 └─ ...
```

**Advantages**:
- Pythonic iteration (`for sent in doc.sentences`)
- Direct attribute access (`word.head`, `word.deprel`)
- JSON serialization built-in

### Processor Dependencies

**Critical**: Dependency parsing **requires** upstream processors.

**Required chain**:
1. `tokenize` (sentence + word segmentation)
2. `mwt` (multi-word token expansion, if language has MWTs)
3. `pos` (POS tagging)
4. `lemma` (lemmatization)
5. `depparse` (dependency parsing)

**Why?** Parser neural network uses POS tags as features.

**Shortcut**: `Pipeline('zh')` auto-includes all required processors.

## Chinese-Specific Considerations

### Tokenization

**UD vs CTB tokenization**:
- Stanza uses UD Chinese-GSD tokenization standard
- **Different from CTB** (more granular in some cases)
- Example: "中国人" → CTB: 1 token, UD: "中国" + "人" (2 tokens)

**Implication**: Scores on CTB test sets may differ from papers using CTB tokenization.

### POS Tagging

**Universal POS** (17 tags):
- NOUN, VERB, ADJ, ADV, PRON, DET, ADP, NUM, CONJ, PART, INTJ, X, etc.

**vs CTB tagset** (33 tags):
- NN, NR, NT, VV, VA, VC, AD, etc.

**Conversion**: UD provides mapping (many-to-one, lossy)

### Pretrained Embeddings

**Chinese models**:
- Character embeddings (built-in)
- Word embeddings (optional, if available)

**Training data**: UD Chinese-GSD (~4K sentences)

**Fine-tuning**: Possible with custom UD-format treebanks.

## Deployment Patterns

### Local/Script Use

**Best for**:
- Research experiments
- Data preprocessing pipelines
- Jupyter notebooks

**Advantages**:
- Simple pip install
- No server management
- Direct Python integration

### Server Deployment

**Options**:
1. **Custom Flask/FastAPI wrapper** (roll your own)
2. **Docker containerization** (reproducible)
3. **Cloud functions** (AWS Lambda, GCP Functions)

**Considerations**:
- Model loading time (~5 seconds, one-time per worker)
- Memory per worker (~2 GB)
- Concurrency (CPU: multi-process, GPU: batch accumulation)

### Production Best Practices

**Optimization**:
- Warm start (load models at startup, not per request)
- Batch processing (accumulate requests, process together)
- GPU utilization (larger batches for throughput)

**Monitoring**:
- Memory usage (models loaded)
- Inference latency (per-sentence)
- Error rate (rare but possible parsing failures)

## Integration Considerations

### Multilingual Pipelines

**Strength**: Unified API across 80+ languages

**Pattern**:
```python
zh_nlp = stanza.Pipeline('zh')
en_nlp = stanza.Pipeline('en')
# Same API, different languages
```

**Use case**: Cross-lingual applications (translation, alignment, comparison)

### Interoperability

**Output formats**:
- **Native**: Stanza Document object
- **JSON**: Built-in serialization
- **CoNLL-U**: Direct conversion (`doc.to_dict()` → format)

**Downstream tasks**:
- Semantic role labeling (external tools)
- Relation extraction (use dependency arcs)
- Knowledge graph construction

### Custom Models

**Supported**:
- Fine-tuning on custom UD treebanks
- Training from scratch (requires UD-format data)
- Transfer learning (start from pretrained, adapt to domain)

**Documentation**: Comprehensive training guides in official docs

**Skill requirement**: Understanding of UD annotation + PyTorch basics

## Comparison: Stanza vs CoreNLP

### When Stanza is Better

1. **Python projects**: Native integration, no Java
2. **Speed**: 2-5x faster CPU, 10-50x faster GPU
3. **Modern architecture**: Neural models, SOTA techniques
4. **Active development**: Regular updates, new languages
5. **UD-native**: Designed for UD from ground up

### When CoreNLP Might Be Preferred

1. **Java projects**: Native Java API
2. **Legacy systems**: Already integrated CoreNLP
3. **Exact reproduction**: Research requiring specific CoreNLP version
4. **Traditional Chinese**: Wrappers with auto-conversion (though Stanza can handle manually)

### Migration Path

**Stanford's recommendation**: New projects use Stanza.

**Breaking changes**:
- API completely different (Java → Python)
- Tokenization may differ (UD vs CTB)
- Outputs compatible (both UD format)

## Strengths Summary

1. **Python-native**: No Java dependency
2. **Fast**: Transition-based parsing, GPU support
3. **UD-optimized**: Native UD training/output
4. **Multilingual**: 80+ languages, consistent API
5. **Active development**: Stanford-backed, regular updates
6. **Clean API**: Pythonic, well-documented
7. **Research credibility**: Stanford NLP Group reputation

## Weaknesses Summary

1. **UD-only**: Not optimized for CTB or other formats
2. **Processor dependencies**: Must run tokenize→POS→lemma→depparse (no shortcuts)
3. **Training data size**: UD Chinese-GSD smaller than CTB
4. **Chinese-specific optimization**: Less than LTP/HanLP (general-purpose tool)
5. **No semantic dependencies**: Syntactic only (vs HanLP/LTP SDP)
6. **Cold start**: Model loading time on first use

## Use Case Fit

**Best for**:
- New Python projects requiring dependency parsing
- Multilingual applications (Chinese + others)
- UD-based research and benchmarking
- Production systems with GPU resources
- Projects prioritizing maintainability and documentation

**Not ideal for**:
- CTB-format output requirements (→ train custom model)
- Chinese-only projects needing maximum optimization (→ LTP)
- Semantic dependency parsing (→ HanLP, LTP)
- Minimal dependencies (→ lighter tools)
- Java ecosystems (→ CoreNLP)

## Further Reading

- Official docs: https://stanfordnlp.github.io/stanza/
- Dependency parsing: https://stanfordnlp.github.io/stanza/depparse.html
- Performance benchmarks: https://stanfordnlp.github.io/stanza/performance.html
- GitHub: https://github.com/stanfordnlp/stanza
- Stanza paper: Qi et al. (2020), ACL
