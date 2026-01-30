# LTP (Language Technology Platform) - Technical Deep Dive

## Evolution and Positioning

### LTP History

**Original LTP** (pre-2020):
- Statistical + rule-based Chinese NLP
- CRF, SVM, maximum entropy models
- Developed by Harbin Institute of Technology (HIT-SCIR)
- Windows + Linux tools

### N-LTP (Neural LTP, 2020+)

**Complete reimplementation** in PyTorch with:
- Neural architectures (transformers, biaffine)
- Multi-task learning framework
- Knowledge distillation from single-task teachers
- Open-source Python library

**Key insight**: N-LTP is **not an upgrade** but a **redesign** for the neural era.

## Architecture: Multi-Task Learning with Knowledge Distillation

### Core Design Philosophy

**"One shared model, six Chinese NLP tasks"**

**Contrast with competitors**:
- **Stanza/CoreNLP**: Independent models per task (pipeline)
- **HanLP**: Optional MTL (offers single-task + MTL models)
- **LTP**: MTL is **core design** (no single-task option)

### Six Fundamental Chinese NLP Tasks

1. **Lexical Analysis**:
   - Chinese word segmentation (CWS)
   - Part-of-speech (POS) tagging
   - Named entity recognition (NER)

2. **Syntactic Parsing**:
   - **Dependency parsing** (syntactic) ← Our focus

3. **Semantic Parsing**:
   - **Semantic dependency parsing** (SDP)
   - Semantic role labeling (SRL)

**Unique**: First toolkit supporting all six for Chinese.

## Multi-Task Learning Architecture

### Shared Encoder Design

```
Chinese Text
 ↓
Pretrained Transformer (shared)
 │
 ├─→ CWS decoder
 ├─→ POS decoder
 ├─→ NER decoder
 ├─→ Dependency Parsing decoder (biaffine)
 ├─→ SDP decoder
 └─→ SRL decoder
```

**Key advantage**: Shared encoder learns **general Chinese representations**.
- Word segmentation informs POS tagging
- POS tagging informs parsing
- Syntactic structure informs semantic parsing

### Knowledge Distillation

**Problem**: Multi-task models often underperform single-task specialists.

**LTP's solution**: Train single-task "teacher" models, then distill knowledge to multi-task "student".

**Process**:
1. Train six single-task models independently (teachers)
2. Train multi-task model (student) to mimic teachers' outputs
3. **Goal**: Student surpasses teachers through shared representations

**Mechanism**:
- Loss function includes task loss + distillation loss
- Student learns from teacher's soft predictions (probability distributions)
- Regularization prevents overfitting to any single task

**Result**: Multi-task model with near-single-task accuracy, significantly faster inference.

## Dependency Parsing Technical Details

### Algorithm: Biaffine Parser

**Same architecture** as HanLP (Dozat & Manning 2017):

```
Input: Token sequence (from CWS) + POS tags
 ↓
Shared transformer encoder (ELECTRA-small for LTP)
 ↓
Task-specific MLP (dimensionality reduction)
 ↓
Biaffine attention (scores all possible arcs)
 ↓
Eisner algorithm (decode MST, guarantee valid tree)
 ↓
Output: Dependency tree
```

**Eisner algorithm**:
- Guarantees **projective** dependency tree
- O(n³) time complexity
- **LTP optimization**: Rust implementation (faster than pure Python)

**Non-projective handling**:
- Eisner enforces projectivity (crossing arcs disallowed)
- Chinese dependencies are mostly projective (this is acceptable)
- Alternative: Chu-Liu/Edmonds for non-projective (not used in LTP)

### Semantic Dependency Parsing (SDP)

**Unique to LTP and HanLP** (not in Stanza/CoreNLP).

**Motivation**: Chinese semantic roles don't align with syntactic structure.
- Topic-comment structure
- Pro-drop (implicit subjects)
- Serial verb constructions

**Output**: **Directed acyclic graph (DAG)**, not tree.
- Words can have multiple semantic heads
- Represents semantic roles (agent, patient, location, etc.)

**Use case**: Semantic role labeling, question answering, information extraction.

## Technical Specifications

### Language and Framework

**Core**: Python 3.6+
**Framework**: PyTorch 1.6+
**Pretrained model**: ELECTRA-small (Chinese)
**Hardware**:
- CPU: Supported
- GPU: Recommended (3-5x speedup)
- Memory: 1-2 GB typical

### Chinese-Only Focus

**Deliberate design choice**:
- Optimize for Chinese linguistic phenomena
- No multilingual compromise (vs Stanza/HanLP 130+ languages)
- Deep Chinese-specific features (classifiers, aspectual markers, etc.)

**Implication**: Cannot use LTP for English, Japanese, etc. (Chinese-only pipeline).

### Model Size and Variants

**Base model**: ELECTRA-small-based (~300MB)
- Balance of speed and accuracy
- Suitable for most applications

**Alternative backbones**: Can fine-tune with other Chinese pretrained models (BERT, RoBERTa).

## Performance Analysis

### Accuracy

**MTL knowledge distillation results** (N-LTP paper):
- Multi-task model **approaches or surpasses** single-task teachers
- Dependency parsing LAS: Competitive with single-task biaffine parser

**Specific scores**: Paper reports benchmarks on CTB5/7/8 (exact scores depend on test set).

**Comparison challenge**:
- LTP, HanLP, Stanza use different benchmarks (CTB variants, UD-GSD, splits)
- Direct comparison requires controlled evaluation

### Speed

**Throughput** (approximate):
- **CPU**: 30-100 sentences/sec (multi-task inference)
- **GPU**: 300-800 sentences/sec (batch processing)

**Key advantage**: **One forward pass, six tasks**.
- Competitors: Six separate forward passes (pipeline)
- LTP: Shared encoder amortizes cost

**Trade-off**: MTL model slightly heavier (~300MB), but single inference.

### Resource Requirements

**Memory**:
- **Model**: ~300 MB (ELECTRA-small base)
- **Peak inference**: ~1-2 GB (batch processing)

**Disk space**:
- Models auto-downloaded to cache
- Full installation: ~500 MB

**GPU memory**:
- 1-2 GB VRAM typical (batch size 16)

## API Design

### Native Python API

**Philosophy**: Simple, efficient, task-oriented

**Example pattern** (conceptual):
```python
from ltp import LTP
ltp = LTP()  # Load pretrained Chinese model
result = ltp.pipeline(["他爱北京"], tasks=["dep"])
# result.dep = dependency parsing output
```

**Features**:
- Single object for all tasks (`LTP()`)
- Task selection (run only what you need)
- Automatic batching

### Multi-Task Invocation

**Efficiency**:
```python
# Run multiple tasks in one call
result = ltp.pipeline(texts, tasks=["cws", "pos", "dep", "sdp"])
# Shared encoder runs once, all tasks computed
```

**Advantage over pipelines**:
- Stanza: `tokenize → pos → lemma → depparse` (4 forward passes)
- LTP: `cws,pos,dep` (1 forward pass, shared encoder)

### LTP-Cloud Service

**Cloud API**:
- REST API (https://www.ltp-cloud.com)
- No local installation required
- Commercial offering with free tier

**Use case**: Quick prototyping, mobile apps, lightweight clients.

## Chinese-Specific Optimizations

### Integrated Word Segmentation

**Critical**: Chinese lacks word boundaries.

**LTP advantage**:
- Segmentation (CWS) is **first task** in MTL model
- Parser directly uses segmenter output (shared representations)
- Joint training improves segmentation-parsing consistency

**Contrast**:
- Stanza: UD tokenization (fixed standard, may mismatch domain)
- LTP: Trainable segmentation (adaptable to domain)

### Semantic Dependencies

**Chinese SDP scheme**:
- HIT-developed annotation standard
- Covers topic-comment structures
- Handles pro-drop and implicit roles

**Output example** (conceptual):
```
他 在 北京 工作
Syntactic (tree):
  工作 (root)
  ├── 他 (nsubj)
  └── 在 (obl)
      └── 北京 (obj)

Semantic (DAG):
  工作 (root)
  ├── 他 (Agt - agent)
  ├── 北京 (Loc - location, multi-head from 在 too)
  └── 在 (mPrep - marking preposition)
```

**Use case**: QA systems ("Where does he work?" → extract location from SDP).

### Knowledge from Academic Research

**Backing institution**: Harbin Institute of Technology (HIT-SCIR)
- Leading Chinese NLP research group
- Deep expertise in Chinese linguistics
- Academic rigor in annotation standards

**Implication**: LTP reflects state-of-the-art Chinese NLP research (2020-2021 era).

## Deployment Patterns

### Local Python Usage

**Best for**:
- Research projects
- Data preprocessing
- Full control over models

**Requirements**:
- Python 3.6+
- PyTorch 1.6+
- ~2 GB RAM

### LTP-Cloud (REST API)

**Best for**:
- Mobile app backends
- Quick prototyping (no setup)
- Outsourcing computation (free tier)

**Limitations**:
- Network latency
- Data privacy (text sent to cloud)
- Rate limits (free tier)

### Docker/Containerized

**Recommendation**: Package LTP + dependencies in Docker for reproducible deployments.

## Integration Considerations

### Chinese-Only Constraint

**Implication**: Cannot use LTP for multilingual projects.

**Workaround**: Combine LTP (Chinese) + Stanza (other languages) in polyglot system.

**Trade-off**: Complexity (two libraries) vs optimization (best-in-class per language).

### Custom Model Training

**Supported**: Fine-tune on custom Chinese corpora.

**Requirements**:
- Annotated data in LTP format (CWS, POS, dependency relations)
- PyTorch training infrastructure
- Expertise in multi-task learning

**Documentation**: Available (primarily Chinese).

### Interoperability

**Output format**: Python objects (convert to JSON, CoNLL-X as needed).

**Challenge**: SDP output format non-standard (LTP-specific, not CoNLL-U).

**Recommendation**: Write converters if integrating with non-LTP systems.

## Strengths Summary

1. **Multi-task efficiency**: One model, six tasks, shared encoder
2. **Knowledge distillation**: MTL model rivals single-task accuracy
3. **Chinese-optimized**: Purpose-built for Chinese, no multilingual compromise
4. **Semantic dependencies**: DAG-based semantic parsing (vs syntactic tree only)
5. **Academic rigor**: HIT-SCIR research backing
6. **Rust-optimized decoding**: Faster Eisner algorithm for parsing

## Weaknesses Summary

1. **Chinese-only**: Cannot use for other languages
2. **MTL constraint**: Cannot train single-task models (design choice)
3. **Smaller community**: Compared to Stanza (Stanford) or HanLP (multilingual)
4. **Documentation**: Advanced features documented primarily in Chinese
5. **Benchmark opacity**: Non-standard evaluation makes comparison difficult
6. **SDP format**: Non-standard semantic dependency output (integration challenge)

## Comparison: LTP vs HanLP

Both offer syntactic + semantic dependency parsing for Chinese, but differ in scope:

| Aspect | LTP | HanLP |
|--------|-----|-------|
| **Language scope** | Chinese-only | 130+ languages |
| **Architecture** | MTL (mandatory) | MTL optional |
| **Knowledge distillation** | Yes (core design) | No |
| **Community** | Academic (HIT) | Broader (multilingual users) |
| **Semantic dependencies** | HIT SDP scheme | Multiple schemes |
| **Optimization** | Chinese-specific | Multilingual generality |

**Choose LTP over HanLP when**:
- Chinese-only project (no multilingual requirement)
- Want MTL efficiency (one model, multiple tasks)
- Prefer HIT academic standards

**Choose HanLP over LTP when**:
- Need multilingual support (Chinese + others)
- Want single-task models (not just MTL)
- Prefer larger community/documentation

## Use Case Fit

**Best for**:
- Chinese-only NLP applications
- Projects requiring syntactic + semantic parsing
- Efficiency-critical deployments (MTL reduces inference cost)
- Academic research on Chinese (HIT standards)
- Systems with GPU resources

**Not ideal for**:
- Multilingual projects (→ Stanza or HanLP)
- Minimal dependencies (MTL model is heavier)
- Non-Chinese languages (by design)
- Projects requiring extensive English documentation (→ Stanza)

## Further Reading

- GitHub: https://github.com/HIT-SCIR/ltp
- N-LTP paper: https://arxiv.org/abs/2009.11616 (Che et al., EMNLP 2021)
- LTP-Cloud: https://www.ltp-cloud.com/intro_en
- ACL Anthology: https://aclanthology.org/2021.emnlp-demo.6/
- Knowledge distillation paper: Hinton et al. (2015)
