# Stanford CoreNLP - Technical Deep Dive

## Architecture

### System Design
CoreNLP is a **monolithic Java application** providing end-to-end NLP pipelines through annotator composition.

**Core architecture**:
```
Raw Text → Tokenizer → Sentence Splitter → POS Tagger → Parser → Output
                                           ↓
                                    Named Entity Recognition
                                           ↓
                                    Coreference Resolution
```

### Dependency Parser Implementation

**Algorithm**: **Graph-based, non-projective dependency parsing**

**How it works**:
1. **Global optimization**: Considers all possible arcs simultaneously
2. **Scoring function**: Assigns scores to potential dependency arcs
3. **Maximum spanning tree**: Finds highest-scoring tree using Chu-Liu/Edmonds algorithm
4. **Non-projective**: Can handle crossing dependencies (important for Chinese)

**Comparison to transition-based** (used by Stanza):
- Graph-based: Better at long-distance dependencies, slower inference
- Transition-based: Faster, richer feature history, local decisions

### Chinese-Specific Components

**Segmenter**:
- CRF-based word segmentation
- Trained on CTB (Chinese Treebank)
- Handles both Simplified and Traditional Chinese

**POS Tagger**:
- Maximum entropy model
- CTB tagset (33 tags)

**Parser**:
- Dependency relations developed by Huihsin Tseng and Pi-Chuan Chang
- Originally used Stanford Dependencies format
- Since v3.5.2: Outputs Universal Dependencies by default

## Technical Specifications

### Language and Runtime

**Language**: Java
**Requirements**: Java 8+ (JRE 1.8.0 or higher)
**Distribution**: JAR file (~500MB with all models)
**Memory**: 2-4GB RAM typical for Chinese processing

### API Patterns

**Native Java**:
```java
// Conceptual (not executable code)
Properties props = new Properties();
props.setProperty("annotators", "tokenize,ssplit,pos,depparse");
props.setProperty("tokenize.language", "zh");
StanfordCoreNLP pipeline = new StanfordCoreNLP(props);
Annotation document = new Annotation(text);
pipeline.annotate(document);
```

**Python Wrappers**:
- `stanfordcorenlp` (unofficial, Stanza recommended)
- `chinese_corenlp` (Simplified/Traditional conversion)
- Server mode: CoreNLP as HTTP server, Python as client

### Input/Output Formats

**Input**:
- Raw text (UTF-8)
- Pre-segmented text (space-delimited)

**Output formats**:
- JSON
- XML
- CoNLL-X / CoNLL-U
- Serialized Java objects

**UD output** (since v3.5.2):
- Universal Relations (48 types)
- Universal POS tags (17 types)
- Enhanced dependencies (optional)

## Performance Analysis

### Accuracy

**Historical context**: CoreNLP's Chinese parser achieved state-of-the-art in 2012-2015 era.

**Modern comparison**:
- Pre-neural architecture (maximum entropy, graph-based)
- Surpassed by neural parsers (Stanza, HanLP) on standard benchmarks
- Still competitive on some evaluation metrics

**Note**: Direct comparison requires same evaluation setup (treebank, train/test split, preprocessing).

### Speed

**Throughput** (approximate, hardware-dependent):
- ~10-30 sentences/second on CPU (single-threaded)
- Slower than neural parsers optimized for batch processing
- Parser is bottleneck (segmentation/POS are fast)

**Latency considerations**:
- JVM startup overhead (~2-3 seconds)
- Model loading (~5-10 seconds)
- Mitigation: Server mode (persistent JVM)

### Resource Requirements

**Memory footprint**:
- Base: ~1GB (JVM + core models)
- Chinese models: +500MB
- Peak during parsing: 2-4GB typical

**Disk space**:
- Full CoreNLP: ~500MB
- Chinese-only minimal: ~200MB

**GPU support**: None (pre-neural architecture)

## Deployment Patterns

### Server Mode (Recommended for Python)

**Advantages**:
- Amortize JVM startup cost
- RESTful API (language-agnostic)
- Concurrent request handling

**Disadvantages**:
- Additional complexity (server management)
- Network overhead (localhost)
- Resource contention (shared JVM)

### Embedded Mode

**Advantages**:
- No network overhead
- Simpler deployment (single JAR)

**Disadvantages**:
- Java dependency in application
- JVM lifecycle management
- Memory overhead

### Docker/Containerized

**Options**:
- Official Stanford Docker images available
- Simplifies Java dependency management
- Production-ready deployment pattern

## Integration Considerations

### Python Projects

**Recommendation**: **Use Stanza instead** (per Stanford NLP Group FAQ)

**Rationale**:
- Stanza is native Python (no Java)
- Better performance (neural models)
- Same research group, modern successor
- Easier deployment

**When to use CoreNLP**:
- Maintaining legacy systems
- Exact reproducibility requirements
- Specific CoreNLP-only features needed

### Java Projects

**Good fit**:
- Native Java integration (no wrappers)
- Mature, stable API
- Extensive documentation

**Consider Stanza via JNI** if:
- Need latest performance
- Want UD-native output
- Can tolerate Python bridge

### Traditional Chinese Handling

**Special feature**: Python wrappers auto-convert Traditional → Simplified for processing, restore in output.

**Why this matters**:
- CoreNLP Chinese models trained on Simplified Chinese (CTB)
- Traditional Chinese requires conversion for optimal accuracy
- Wrappers handle this transparently

## Technical Limitations

### Architecture Age

**Pre-neural design** (2005-2015 era):
- Maximum entropy models (not transformers)
- Hand-crafted features (not learned representations)
- Slower inference than batched neural models

**Implications**:
- Lower accuracy ceiling than SOTA neural parsers
- Cannot leverage pretrained embeddings (BERT, etc.)
- Limited transfer learning capabilities

### Maintenance Status

**Development focus**:
- Stanza is now primary Python NLP toolkit from Stanford
- CoreNLP receives maintenance updates (bug fixes, UD format compliance)
- New features unlikely (focus shifted to Stanza)

**Community**:
- Large installed base (many legacy systems)
- Active but declining (users migrate to Stanza)

### Format Lock-in

**Stanford Dependencies → UD transition**:
- Old code may expect Stanford Dependencies format
- UD output since v3.5.2 (good for new projects)
- Conversion between formats possible but lossy

## Strengths Summary

1. **Battle-tested reliability**: Decade+ of production use
2. **Complete pipeline**: Full NLP stack, not just parsing
3. **Strong documentation**: Academic papers + user guides
4. **Traditional Chinese support**: Via wrappers with auto-conversion
5. **Java ecosystem fit**: Native integration for Java projects

## Weaknesses Summary

1. **Java dependency**: Complicates Python deployments
2. **Pre-neural architecture**: Lower accuracy than modern parsers
3. **Speed**: Slower than optimized neural models
4. **Maintenance**: Superseded by Stanza for new projects
5. **Complexity**: Server mode or wrappers add operational overhead

## Migration Path

### From CoreNLP to Stanza

**Compatibility**:
- Both output UD format (compatible downstream)
- API differences require code changes
- Performance improvements (speed + accuracy)

**Breaking changes**:
- Java → Python (language shift)
- Different tokenization (Stanza uses UD-trained)
- Model architectures differ (output may vary slightly)

**Recommendation**: New projects start with Stanza; existing systems migrate opportunistically.

## Use Case Fit

**Best for**:
- Legacy Java systems with existing CoreNLP integration
- Research reproduction (exact CoreNLP versions)
- Specific Traditional Chinese conversion needs (via wrappers)

**Not ideal for**:
- New Python projects (→ Stanza)
- Performance-critical applications (→ neural parsers)
- Minimal dependencies (→ lighter tools)
- Latest SOTA accuracy (→ HanLP, Stanza with recent models)

## Further Reading

- Official docs: https://stanfordnlp.github.io/CoreNLP/
- Dependency parsing: https://stanfordnlp.github.io/CoreNLP/depparse.html
- Chinese processing: https://stanfordnlp.github.io/CoreNLP/chinese.html
- Stanford Dependencies paper: de Marneffe et al. (2014)
- FAQ (Stanza recommendation): https://stanfordnlp.github.io/stanza/faq.html
