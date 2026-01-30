# HanLP - Technical Deep Dive

## Architecture Evolution

### HanLP 1.x (Java, Dictionary-Based)
- Traditional rule-based + statistical NLP
- CRF, HMM, Viterbi algorithms
- Large hand-crafted dictionaries
- **Legacy**: Still used in production systems

### HanLP 2.x (Python, Neural)
**Complete rewrite** on PyTorch/TensorFlow 2.x

**Philosophy**: "One model, multiple tasks"
- Joint training across related NLP tasks
- Shared pretrained embeddings (BERT, RoBERTa)
- Modular architecture (mix-and-match components)

## Dependency Parsing Architecture

### Dual Parsing Capabilities

**1. Syntactic Dependency Parsing**
- **Algorithm**: Biaffine parser (Dozat & Manning 2017)
- **Architecture**: BiLSTM + biaffine attention
- **Output**: Traditional head-dependent relations
- **Format**: CoNLL-X
- **Use case**: Grammatical structure analysis

**2. Semantic Dependency Parsing (SDP)**
- **Framework**: Task-oriented semantic graphs
- **Output**: Multi-head dependencies (DAG, not tree)
- **Use case**: Semantic role labeling, meaning extraction
- **Unique to**: HanLP and LTP (not in Stanza/CoreNLP)

### Biaffine Parser Technical Details

**Architecture**:
```
Input: Token sequence + POS tags
↓
Word + POS embeddings
↓
BiLSTM (multi-layer, bidirectional)
↓
MLP dimensionality reduction
↓
Biaffine attention (scores all possible arcs)
↓
Arc prediction + Relation labeling
↓
Output: Dependency tree (CoNLL-X format)
```

**Key innovation** (Dozat & Manning):
- **Biaffine transformation**: Computes score for every (head, dependent) pair
- **Efficiency**: O(n²) arc scoring, Eisner MST decoding O(n³)
- **Accuracy**: SOTA results on PTB English (95.7% UAS, 94.1% LAS)

**HanLP's implementation**:
- Pretrained Chinese models on CTB7
- Example: `CTB7_BIAFFINE_DEP_ZH`
- Uses UD relations (recent versions)

## Technical Specifications

### Language and Framework

**Core**: Python 3.6+
**Backends**: PyTorch 1.6+ OR TensorFlow 2.3+
**Hardware**:
- CPU: Supported (slower)
- GPU: Recommended (3-10x speedup)
- TPU: Supported (TensorFlow backend only)

### Multi-Task Learning (MTL) Models

**HanLP 2.1 MTL architecture**:
- **Shared encoder**: Pretrained transformer (e.g., BERT for Chinese)
- **Task-specific heads**: Separate decoders for each task
- **Joint training**: Backprop through shared encoder improves all tasks

**Supported tasks** (10 joint tasks):
1. Tokenization (word segmentation)
2. Lemmatization
3. POS tagging
4. Token feature extraction
5. **Dependency parsing** (syntactic)
6. Constituency parsing
7. Semantic role labeling
8. **Semantic dependency parsing**
9. AMR parsing (English)
10. Named entity recognition

**Advantage**: Single model inference (faster than pipeline)
**Disadvantage**: Heavier memory footprint (~1-2GB for Chinese MTL model)

## Performance Analysis

### Accuracy

**Syntactic dependency parsing** (Ancient Chinese example from docs):
- UAS: 88.70%
- LAS: 83.89%

**Note**: HanLP uses **Stanford Dependencies 3.3.0** standard (not Zhang & Clark 2008), making literature comparisons difficult.

**CTB splits**: HanLP proposes uniform splitting, different from common academic practice.

**Implication**: Published HanLP scores may not directly compare to papers using different standards/splits.

### Speed

**Throughput** (approximate, GPU-dependent):
- **Single-task models**: ~500-1000 sentences/sec (GPU)
- **MTL models**: ~200-500 sentences/sec (GPU, 10 tasks)
- **CPU**: 10-50 sentences/sec (varies by model)

**Optimization**:
- Batching critical for GPU utilization
- Lightweight models available (KBs for mobile, lower accuracy)

**Bottleneck**: Transformer encoder (BERT) dominates inference time.

### Resource Requirements

**Memory**:
- **Lightweight models**: 10-50 MB
- **Standard models**: 500 MB - 1 GB
- **MTL models**: 1-2 GB
- **Peak during inference**: +500 MB (batch processing)

**Disk space**:
- Models auto-downloaded on first use
- Cache: `~/.hanlp/` (multi-GB for all models)

**GPU memory**:
- 2-4 GB typical (batch size dependent)
- Larger batches require more VRAM

## API Design

### Native Python API

**Philosophy**: Pythonic, minimal boilerplate

**Example pattern** (conceptual):
```python
import hanlp
parser = hanlp.load(hanlp.pretrained.dep.CTB7_BIAFFINE_DEP_ZH)
result = parser(["他", "爱", "北京"])
# Output: CoNLL-X format with HEAD, DEPREL fields
```

**Features**:
- Lazy loading (models loaded on first inference)
- Automatic device selection (GPU if available)
- Batch processing support

### RESTful API

**Deployment**:
```bash
hanlp serve  # Starts HTTP server
```

**Advantages**:
- Language-agnostic clients
- Horizontal scaling (multiple servers)
- Cloud deployment patterns

**Use case**: Production services (mobile apps, web backends)

### Shared Interface Philosophy

**Design goal**: Native and REST APIs share similar structure
- Same input formats (text, pretokenized lists)
- Same output formats (JSON, CoNLL-X)
- Easy transition (development → production)

## Chinese-Specific Optimizations

### Multi-Granularity Word Segmentation

**Challenge**: Chinese lacks spaces; segmentation ambiguous
**HanLP approach**:
- Joint tokenization + parsing models
- Character-level and word-level features
- Lattice-based decoding

### Semantic Dependencies (Chinese-Specific)

**Motivation**: Chinese syntax-semantics mismatch
- Topic-prominent structure
- Implicit subjects/objects
- Semantic roles don't align with syntactic heads

**SDP output**:
- Multi-head dependencies (words can have multiple semantic heads)
- DAG structure (not tree)
- Task-oriented relations (agent, patient, location, etc.)

**Example**:
```
他 在 北京 工作
- Syntactic: 工作 is root, 他 is nsubj, 北京 is obl
- Semantic: 他 is agent of 工作, 北京 is location of 工作 (multi-head)
```

### Pretrained Models for Chinese

**Available models**:
- `CTB5_BIAFFINE_DEP_ZH`: Trained on CTB5
- `CTB7_BIAFFINE_DEP_ZH`: Trained on CTB7 (more data)
- `CTB9_DEP_ELECTRA_SMALL`: ELECTRA-based (faster)
- MTL models: Combined segmentation + POS + parsing

**Recommendation**: Use latest CTB9 or MTL models for best accuracy.

## Deployment Patterns

### Local Development

**Advantages**:
- Direct Python import
- No network latency
- GPU acceleration (if available)

**Best for**: Notebooks, scripts, experiments

### REST Service

**Advantages**:
- Horizontal scaling
- Language-agnostic
- Centralized model management

**Best for**: Production web services, mobile backends

### Mobile/Edge

**Special models**:
- HanLP provides "tiny" models (KBs size)
- Lower accuracy, drastically smaller
- Suitable for on-device inference (Android, iOS)

**Trade-off**: 5-10% accuracy drop for 100x size reduction

## Integration Considerations

### PyTorch vs TensorFlow

**Choice**: Depends on existing infrastructure
- Both backends supported
- Model availability varies (PyTorch more common)
- Performance parity for most tasks

**Installation**:
- `pip install hanlp[torch]` (PyTorch)
- `pip install hanlp[tf]` (TensorFlow)

### Multilingual Projects

**HanLP 2.1 supports 130+ languages**
- Trained on UD treebanks (multilingual)
- Chinese models often Chinese-only (better optimization)
- Use multilingual MTL models for cross-language consistency

**Use case**: Unified API for English + Chinese + Japanese projects

### Custom Model Training

**Supported**:
- Fine-tuning pretrained models on domain data
- Training from scratch (requires treebank)
- Transfer learning (leverage BERT embeddings)

**Documentation**: Available but primarily Chinese
**Skill requirement**: Deep learning + NLP expertise

## Strengths Summary

1. **Dual parsing**: Syntactic + semantic dependencies (unique)
2. **Modern architecture**: SOTA neural models (biaffine, transformers)
3. **Multilingual**: 130+ languages in HanLP 2.1
4. **Flexible deployment**: Native, REST, mobile
5. **Active development**: Regular updates, new models
6. **Chinese-optimized**: Purpose-built for Chinese NLP

## Weaknesses Summary

1. **Memory footprint**: Neural models require 500MB-2GB
2. **GPU preferred**: CPU inference significantly slower
3. **Documentation**: Advanced features documented in Chinese
4. **Dependency heaviness**: PyTorch/TensorFlow adds overhead
5. **Benchmark opacity**: Non-standard evaluation splits
6. **Segmentation gap**: Some benchmarks show lower segmentation accuracy vs competitors (THULAC)

## Technical Comparison: HanLP vs LTP

**Similarities**:
- Both Chinese-focused
- Both offer semantic dependency parsing
- Both use modern neural architectures

**Key differences**:

| Aspect | HanLP | LTP |
|--------|-------|-----|
| **Language scope** | 130+ languages | Chinese-only |
| **Architecture** | PyTorch/TensorFlow | PyTorch |
| **MTL approach** | Optional (single + MTL models) | Core design (always MTL) |
| **Knowledge distillation** | No | Yes (teacher-student) |
| **Community** | Larger, international | Smaller, Chinese academic |
| **Java version** | Yes (HanLP 1.x) | No |

## Use Case Fit

**Best for**:
- Modern Python projects requiring syntactic + semantic parsing
- Multilingual applications (Chinese + others)
- Production services with REST API requirements
- Research leveraging semantic dependencies
- Projects with GPU resources

**Not ideal for**:
- CPU-only, resource-constrained environments (→ Stanza lighter)
- Chinese-only speed optimization (→ LTP knowledge distillation)
- Minimal dependencies (→ simpler tools)
- Windows + TensorFlow (installation issues reported)

## Further Reading

- Official docs: https://hanlp.hankcs.com/docs/
- GitHub: https://github.com/hankcs/HanLP
- Dependency parsing demo: https://hanlp.hankcs.com/en/demos/dep.html
- Biaffine parser paper: Dozat & Manning (2017)
- HanLP 2.1 paper: He & Choi (2021)
