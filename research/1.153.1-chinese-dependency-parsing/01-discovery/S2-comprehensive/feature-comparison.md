# Feature Comparison Matrix

## Quick Reference Table

| Feature | UD | CoreNLP | HanLP | Stanza | LTP |
|---------|----|---------| ------|--------|-----|
| **Language** | Format | Java | Python | Python | Python |
| **Backend** | N/A | Statistical | PyTorch/TF | PyTorch | PyTorch |
| **Algorithm** | N/A | Graph-based | Biaffine | Transition-based | Biaffine |
| **Output Format** | CoNLL-U | UD, SD, XML | CoNLL-X | CoNLL-U | Python/JSON |
| **Multilingual** | 100+ langs | 8 langs | 130+ langs | 80+ langs | Chinese only |
| **GPU Support** | N/A | No | Yes | Yes | Yes |
| **Semantic Deps** | No | No | Yes | No | Yes |
| **Model Size** | N/A | ~500MB | 500MB-2GB | 300-500MB | ~300MB |
| **Maintenance** | Active | Stable | Active | Active | Active |

## Parsing Algorithm Comparison

### Algorithm Characteristics

| Algorithm | Used By | Strengths | Weaknesses |
|-----------|---------|-----------|------------|
| **Graph-based** (MST) | CoreNLP | Better long dependencies, global optimization | Slower (O(n³)), limited feature history |
| **Transition-based** | Stanza | Faster (O(n)), rich features, greedy | Local decisions, error propagation |
| **Biaffine** (neural) | HanLP, LTP | SOTA accuracy, efficient scoring | Requires GPU for speed, heavier models |

### Technical Details

**Graph-based (CoreNLP)**:
- Chu-Liu/Edmonds maximum spanning tree
- Scores all possible arcs, selects highest-scoring tree
- Non-projective (allows crossing dependencies)
- Pre-neural (maximum entropy features)

**Transition-based (Stanza)**:
- Stack-buffer state machine
- SHIFT, LEFT-ARC, RIGHT-ARC actions
- Neural classifier predicts next action
- Linear time for projective trees

**Biaffine (HanLP, LTP)**:
- BiLSTM/Transformer encoder
- Biaffine transformation scores (head, dependent) pairs
- Eisner algorithm decodes valid tree (projective)
- SOTA results (Dozat & Manning 2017: 95.7% UAS PTB)

## Output Format Comparison

### CoNLL-U (UD Standard)

**Used by**: UD (specification), Stanza (native), CoreNLP (since v3.5.2), HanLP (compatible)

**10-field format**:
1. ID, 2. FORM, 3. LEMMA, 4. UPOS, 5. XPOS, 6. FEATS, 7. HEAD, 8. DEPREL, 9. DEPS, 10. MISC

**Advantages**:
- Cross-linguistic consistency
- Extensive tooling (validators, visualizers)
- Academic standard (reproducibility)

**Limitations**:
- Fixed schema (may not capture language-specific nuances)
- Verbose (10 fields per token)

### CoNLL-X (Classic Format)

**Used by**: HanLP (for syntactic dependencies)

**Similar to CoNLL-U** but less standardized:
- 10 fields (slightly different conventions)
- No universal POS tags (language-specific only)
- Used in CoNLL-X 2006 shared task

### Stanford Dependencies

**Used by**: CoreNLP (pre-v3.5.2), HanLP (option)

**Relation set**:
- ~50 typed dependencies (nsubj, dobj, prep, etc.)
- English-centric (adapted for Chinese)
- Multiple versions (SD 1.x, 2.x, 3.3.0)

**Status**: Largely superseded by UD (Stanford developed UD as successor).

### Custom Formats

**LTP**: Python objects with task-specific structures
- Syntactic dep: Tree structure
- Semantic dep: DAG structure
- Requires conversion for standard formats

## Architecture Comparison

### Single-Task Models

**Approach**: Independent models per NLP task

**Used by**: CoreNLP, Stanza, HanLP (option)

**Workflow**:
```
Text → Tokenizer → POS Tagger → Parser
      (Model 1)   (Model 2)    (Model 3)
```

**Advantages**:
- Task-specific optimization (highest single-task accuracy)
- Modular (replace individual components)
- Clear error attribution (identify failing stage)

**Disadvantages**:
- Slower (multiple forward passes)
- Redundant computation (each model processes tokens)
- No shared learning (tasks don't inform each other)

### Multi-Task Learning (MTL)

**Approach**: One shared model, multiple task heads

**Used by**: HanLP (option), LTP (core design)

**Workflow**:
```
Text → Shared Encoder → Task Head 1 (segmentation)
                      → Task Head 2 (POS)
                      → Task Head 3 (parsing)
                      (All in one forward pass)
```

**Advantages**:
- Faster (single encoder forward pass)
- Shared representations (tasks benefit from each other)
- Smaller total footprint (one shared model vs many)

**Disadvantages**:
- Task interference (optimization conflicts)
- Less modular (can't easily replace one task)
- Heavier than single-task models (but lighter than pipeline)

### Knowledge Distillation (LTP)

**Approach**: Train MTL model to mimic single-task "teachers"

**Process**:
1. Train single-task teachers (maximize per-task accuracy)
2. Train MTL student to match teacher outputs
3. Student learns from teacher probability distributions (soft targets)

**Goal**: Achieve near-single-task accuracy with MTL efficiency.

**Results**: LTP reports MTL model approaching/surpassing teachers on benchmarks.

## Multilingual Capabilities

### Cross-Linguistic Coverage

**UD**: 100+ languages (format + treebanks)
**HanLP 2.1**: 130+ languages (widest coverage)
**Stanza**: 80+ languages (UD-trained)
**CoreNLP**: 8 languages (AR, ZH, EN, FR, DE, HU, IT, ES)
**LTP**: Chinese only (by design)

### Multilingual Architecture Approaches

**Stanza**:
- Language-specific models (80+ separate models)
- Shared architecture (same neural network design)
- UD-consistent (same annotation across languages)

**HanLP**:
- Some models language-specific (Chinese-optimized)
- Some models multilingual (trained on 130+ languages jointly)
- Flexible (choose monolingual or multilingual models)

**LTP**:
- Monolingual focus (Chinese-only)
- No multilingual compromise (maximum Chinese optimization)

### Cross-Lingual Transfer

**Supported by**: Stanza (via UD)

**Technique**: Train on high-resource languages, test on low-resource
- Example: Train on Chinese-GSD, test on Classical Chinese
- Results: 75-85% accuracy (vs 85-95% monolingual)

**Use case**: Parsing languages with limited training data.

## Deployment Considerations

### Installation Complexity

**Easiest**: Stanza, HanLP, LTP (all `pip install`)
**Moderate**: CoreNLP (requires Java, wrappers for Python)
**N/A**: UD (format only, not software)

### Runtime Dependencies

**Lightweight**: Stanza (PyTorch only)
**Moderate**: HanLP (PyTorch OR TensorFlow), LTP (PyTorch)
**Heavy**: CoreNLP (Java 8+, ~500MB JARs)

### Memory Footprint

**Comparison** (Chinese models, idle + peak):

| Tool | Model Size | Peak RAM |
|------|------------|----------|
| Stanza | 300-500MB | 1-2GB |
| HanLP | 500MB-2GB | 2-3GB |
| LTP | ~300MB | 1-2GB |
| CoreNLP | ~500MB | 2-4GB |

### GPU Requirements

**Supported**: HanLP, Stanza, LTP (all PyTorch-based)
**Not supported**: CoreNLP (pre-neural architecture)
**UD**: N/A

**Speedup**: 3-10x for single sentences, 10-50x for batches (GPU vs CPU)

## API Usability

### Pythonic API (Subjective Rating)

1. **Stanza**: ⭐⭐⭐⭐⭐ (Cleanest, most intuitive)
2. **HanLP**: ⭐⭐⭐⭐ (Powerful but complex for beginners)
3. **LTP**: ⭐⭐⭐⭐ (Simple, efficient)
4. **CoreNLP**: ⭐⭐ (Wrappers add friction, Java underneath)

### Documentation Quality

1. **Stanza**: ⭐⭐⭐⭐⭐ (Comprehensive, clear examples)
2. **CoreNLP**: ⭐⭐⭐⭐ (Extensive, academic focus)
3. **HanLP**: ⭐⭐⭐⭐ (Good for common tasks, Chinese for advanced)
4. **LTP**: ⭐⭐⭐ (Adequate, some English docs, primarily Chinese)

### Community and Support

**Largest**: Stanza (Stanford-backed, academic community)
**Growing**: HanLP (multilingual reach)
**Specialized**: LTP (Chinese NLP researchers)
**Stable**: CoreNLP (legacy user base, maintenance mode)

## Semantic Dependency Parsing

### Availability

**Supported**: HanLP, LTP
**Not supported**: Stanza, CoreNLP (syntactic only)
**UD**: Format doesn't include SDP (focused on syntactic)

### SDP Characteristics

**Syntactic vs Semantic**:

| Aspect | Syntactic (Tree) | Semantic (DAG) |
|--------|------------------|----------------|
| **Structure** | Tree (single head per word) | DAG (multiple heads possible) |
| **Relations** | Grammatical (nsubj, obj, obl) | Semantic roles (agent, patient, location) |
| **Goal** | Grammatical structure | Meaning representation |
| **Example** | 他 → 工作 (nsubj) | 他 → 工作 (agent), 北京 → 工作 (location) |

**Chinese motivation**:
- Topic-comment structure (syntax ≠ semantics)
- Pro-drop (implicit subjects/objects)
- Serial verbs (one syntactic head, multiple semantic roles)

### Use Cases for SDP

**When semantic dependencies matter**:
- Question answering (extract semantic roles)
- Information extraction (who did what to whom, where)
- Semantic similarity (meaning-based, not syntax-based)
- Knowledge graph construction

**When syntactic dependencies sufficient**:
- Grammar checking
- POS-based features (downstream ML)
- Simple relation extraction (surface syntax)

## Performance Trade-offs

### Accuracy vs Speed

**Highest accuracy** (typical): Biaffine parsers (HanLP, LTP) on their benchmark data
**Balanced**: Stanza (transition-based, optimized for UD)
**Legacy**: CoreNLP (graph-based, pre-neural)

**Speed ranking** (single-threaded CPU):
1. Stanza (transition-based, O(n))
2. LTP (MTL efficiency, Rust decoding)
3. HanLP (biaffine, PyTorch batching)
4. CoreNLP (graph-based, O(n³), pre-neural)

**With GPU**: HanLP, LTP, Stanza all benefit significantly (10-50x batched throughput).

### Accuracy vs Resource Usage

**Lightest**: Stanza (~300MB models, 1-2GB peak RAM)
**Moderate**: LTP (~300MB model, MTL efficiency)
**Heavier**: HanLP (500MB-2GB models, multiple tasks)
**Java overhead**: CoreNLP (~500MB + JVM ~1GB)

### Generality vs Specialization

**Most general**: HanLP (130+ languages, all NLP tasks)
**UD-optimized**: Stanza (80+ languages, UD-native)
**Chinese-optimized**: LTP (Chinese-only, no multilingual compromise)
**Legacy-optimized**: CoreNLP (Java ecosystems, research reproduction)

## Custom Model Training

### Training Support

| Tool | Custom Training | Documentation | Skill Required |
|------|----------------|---------------|----------------|
| **Stanza** | ✅ Excellent | Comprehensive | Moderate (UD annotation + PyTorch basics) |
| **HanLP** | ✅ Supported | Moderate (Chinese) | Advanced (MTL, transformers) |
| **LTP** | ✅ Supported | Limited (Chinese) | Advanced (MTL, knowledge distillation) |
| **CoreNLP** | ⚠️ Difficult | Academic papers | Expert (Java, old frameworks) |

### Data Requirements

**All tools require**:
- Annotated corpus (treebank)
- Train/dev/test splits
- Format-specific (CoNLL-U for Stanza, CoNLL-X for HanLP, etc.)

**Minimum corpus size**:
- Research: 500-1000 sentences (proof-of-concept)
- Production: 10K+ sentences (competitive accuracy)
- SOTA: 40K+ sentences (e.g., PTB English, CTB Chinese)

**Domain adaptation**:
- Fine-tune pretrained models on domain corpus
- Less data needed (1K sentences may suffice)
- Best results: In-domain training data

## Strategic Considerations

### Long-Term Maintenance

**Most likely to receive updates**:
1. **Stanza** (active Stanford research, UD evolution)
2. **HanLP** (active open-source, multilingual expansion)
3. **LTP** (active HIT research, Chinese NLP advances)
4. **CoreNLP** (maintenance mode, stable but not evolving)

### Ecosystem Momentum

**UD format**:
- Growing adoption (Stanza, HanLP, CoreNLP all support)
- Academic standard (reproducibility)
- Tooling ecosystem (validators, visualizers, converters)

**Trend**: Converging on UD as lingua franca for dependency parsing.

### Vendor Lock-In Risk

**Lowest risk**: Stanza, HanLP (both output UD → standard format → interchangeable)
**Moderate risk**: LTP (custom SDP format, but syntactic parsing uses standard)
**Legacy risk**: CoreNLP (old Stanford Deps format, though UD supported)

## Recommendation Summary

**Choose based on**:

1. **Project scope**:
   - Multilingual → Stanza or HanLP
   - Chinese-only → LTP or HanLP

2. **Task requirements**:
   - Syntactic only → Stanza (simplest)
   - Semantic needed → HanLP or LTP

3. **Infrastructure**:
   - Python → Stanza, HanLP, LTP
   - Java → CoreNLP

4. **Resources**:
   - GPU available → HanLP or LTP (best utilization)
   - CPU-only → Stanza (most efficient)

5. **Expertise**:
   - Standard benchmarks → Stanza (UD-native)
   - Chinese research → LTP (HIT standards)
   - General NLP → HanLP (broadest toolkit)

**See S2 recommendation.md for detailed decision guidance.**
