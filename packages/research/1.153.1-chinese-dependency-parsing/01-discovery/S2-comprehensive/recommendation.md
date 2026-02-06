# S2-Comprehensive: Recommendation

## Technical Decision Framework

After deep analysis, library choice depends on **constraints** and **requirements** more than absolute "best" ranking.

## Decision Matrix

### By Primary Constraint

#### If Multilingual Required

**Recommended: Stanza**
- 80+ languages with consistent API
- UD-native (cross-linguistic compatibility)
- Clean Python, well-documented
- Stanford-backed reliability

**Alternative: HanLP**
- 130+ languages (wider coverage)
- More NLP tasks beyond parsing
- Heavier footprint, steeper learning curve

**Not suitable: LTP** (Chinese-only by design)

#### If Chinese-Only

**Recommended: LTP** (if need semantic dependencies)
- Multi-task efficiency (one model, six tasks)
- Semantic + syntactic parsing
- Chinese-optimized (HIT research)
- Knowledge distillation (MTL rivals single-task accuracy)

**Alternative: HanLP**
- Semantic + syntactic parsing
- More flexible (single-task or MTL models)
- Larger community
- Also supports other languages (future-proof)

**Also viable: Stanza**
- Simpler if only syntactic parsing needed
- Lighter models (~300MB vs 500MB+)
- Best documentation
- UD-standard output

#### If Semantic Dependencies Required

**Only options: HanLP or LTP**

**Choose HanLP if**:
- Need multilingual (Chinese + others)
- Want PyTorch OR TensorFlow backends
- Prefer larger community
- Building diverse NLP pipelines (sentiment, classification, etc.)

**Choose LTP if**:
- Chinese-only project
- Want MTL efficiency (one forward pass, multiple tasks)
- Prefer HIT academic standards
- Trust knowledge distillation approach

**Note**: Stanza and CoreNLP provide **syntactic dependencies only** (no semantic).

#### If Java Ecosystem

**Only option: CoreNLP**
- Native Java integration
- Mature API
- Proven reliability

**But consider**:
- Slower than neural parsers
- Pre-neural architecture (lower accuracy ceiling)
- Maintenance mode (Stanza is Stanford's new focus)

**Alternative**: Stanza with JNI bridge (if Python acceptable)

### By Performance Priority

#### Maximize Accuracy

**For UD benchmarks**: Stanza (optimized for UD from ground up)
**For CTB benchmarks**: HanLP or LTP (trained on CTB, use CTB standards)
**For semantic accuracy**: HanLP or LTP (SDP support)

**Note**: "Accuracy" is benchmark-dependent. Tools use different test sets, making direct comparison difficult.

#### Maximize Speed (CPU)

1. **Stanza**: Transition-based O(n), optimized single-task inference
2. **LTP**: MTL efficiency (one model, multiple tasks)
3. **HanLP**: Biaffine O(n²) scoring, batched inference
4. **CoreNLP**: Graph-based O(n³), pre-neural (slowest)

**With GPU**: All neural parsers (HanLP, LTP, Stanza) benefit similarly (~10-50x batched throughput).

#### Minimize Resource Usage

**Lightest models**: Stanza (~300MB Chinese models)
**Moderate**: LTP (~300MB MTL model, but includes 6 tasks)
**Heavier**: HanLP (500MB-2GB depending on model choice)
**Java overhead**: CoreNLP (~500MB models + ~1GB JVM)

**Memory-constrained environments** (mobile, edge):
- HanLP offers "tiny" models (KBs, significant accuracy drop)
- Otherwise, Stanza is lightest full-featured option

### By Deployment Context

#### Research/Academic

**Recommended: Stanza**
- UD-native (standard benchmarks)
- Reproducible (clear versioning, model provenance)
- Stanford-backed (academic credibility)
- Extensive citation history

**Also strong**: LTP (if Chinese-focused research, HIT standards)

#### Production Services

**For scale**: HanLP or LTP (GPU batch processing)
**For simplicity**: Stanza (cleanest API, best docs)
**For REST API**: HanLP or LTP-Cloud (native REST support)

**Consider**:
- Model loading time (5-10 seconds one-time cost)
- Memory per worker (1-2GB typical)
- GPU utilization (batching critical for throughput)

#### Embedded/Mobile

**Only option**: HanLP "tiny" models
- Drastically reduced size (KBs vs MB)
- ~5-10% accuracy drop
- On-device inference feasible

**Otherwise**: Server-side parsing (client sends text, receives parse)

#### Legacy System Integration

**Java systems**: CoreNLP (native) or Stanza (via bridge)
**Python systems**: Stanza, HanLP, or LTP
**Polyglot**: All support JSON I/O (language-agnostic interface)

## Architecture-Specific Recommendations

### Parsing Algorithm Trade-offs

**Transition-based (Stanza)**:
- **Pro**: Fast (linear time), rich features
- **Con**: Greedy (local decisions), error propagation
- **Best for**: Speed-critical, large-scale processing

**Graph-based (CoreNLP)**:
- **Pro**: Global optimization, better long dependencies
- **Con**: Slower (cubic time), pre-neural (dated)
- **Best for**: Legacy systems, exact reproduction

**Biaffine (HanLP, LTP)**:
- **Pro**: SOTA accuracy, efficient neural scoring
- **Con**: Requires GPU for speed, heavier models
- **Best for**: Accuracy-critical, GPU-available environments

### Single-Task vs Multi-Task

**Single-task (Stanza, HanLP option)**:
- **Pro**: Highest per-task accuracy, modular
- **Con**: Slower (multiple forward passes)
- **Best for**: Task-specific optimization, clear error attribution

**Multi-task (LTP, HanLP option)**:
- **Pro**: Faster (shared encoder), captures task synergies
- **Con**: Task interference, less modular
- **Best for**: Multiple NLP tasks needed, efficiency-critical

**LTP's knowledge distillation**: Attempts to get single-task accuracy with MTL efficiency.

## Technical Risk Assessment

### Lowest Risk (Conservative Choice)

**Stanza**:
- Stanford-backed (institutional stability)
- UD-native (standard format)
- Active development (regular updates)
- Extensive documentation (low learning curve)
- Large community (Stack Overflow, GitHub issues)

**Risk**: Minimal. Safe bet for most projects.

### Moderate Risk (Specialized Choice)

**HanLP**:
- Active development (regular releases)
- Broad feature set (future-proof)
- Multilingual (scales to new languages)
- **Risk**: Complexity (many options), heavier dependencies

**LTP**:
- Academic backing (HIT research)
- Chinese-optimized (best for domain)
- **Risk**: Smaller community, Chinese-only (not future-proof for multilingual)

### Higher Risk (Legacy/Niche)

**CoreNLP**:
- Maintenance mode (minimal new features)
- Pre-neural (accuracy ceiling)
- Java dependency (friction in Python projects)
- **Risk**: Technical debt, migration pressure to Stanza

**Recommendation**: Use CoreNLP only if:
- Maintaining existing system
- Java requirement non-negotiable
- Exact reproduction of old research needed

## Custom Training Considerations

### Easiest to Train

**Stanza**:
- Comprehensive training documentation
- UD-format data (standard, well-documented)
- Clear examples (official tutorials)
- Moderate skill requirement (PyTorch basics + UD annotation)

### Advanced Training

**HanLP**:
- MTL training more complex
- Documentation primarily Chinese for advanced features
- Requires deep learning expertise

**LTP**:
- Knowledge distillation adds complexity
- Requires training teachers + student
- Academic research-level expertise

**CoreNLP**:
- Old frameworks (MaxEnt, pre-neural)
- Java expertise required
- Minimal recent documentation

## Integration Pattern Recommendations

### Microservice Architecture

**Recommended**: HanLP or LTP via REST
- Native REST API support
- Stateless (horizontal scaling)
- Language-agnostic clients

**Pattern**:
```
Client (any language) → HTTP → Parsing Service (HanLP/LTP) → JSON response
```

### Monolithic Application

**Recommended**: Stanza (if Python) or CoreNLP (if Java)
- Direct library import
- No network overhead
- Simpler deployment (single process)

### Serverless / Cloud Functions

**Challenges**: Cold start (model loading 5-10s)
**Mitigation**: Keep workers warm, pre-load models

**Best fit**: Stanza or LTP (lighter models, faster loading)
**Less suitable**: HanLP MTL models (heavier, longer cold start)

## Budget/Resource Considerations

### Free/Open Source Only

**All tools are open source**:
- Stanza, HanLP, LTP: Apache/MIT-style licenses
- CoreNLP: GPL v3+ (note: GPL more restrictive)

**Cloud services**:
- LTP-Cloud: Free tier available
- HanLP: Self-host or use commercial offering

### Compute Budget

**CPU-only**: Stanza (most efficient)
**GPU available**: HanLP or LTP (best utilization)
**Cloud**: All tools can run on AWS, GCP, Azure (Docker recommended)

### Development Time Budget

**Fastest to prototype**:
1. Stanza (pip install, 3 lines of code)
2. LTP (similar simplicity)
3. HanLP (more options, steeper learning curve)
4. CoreNLP (Java setup, wrappers)

## Summary Recommendations

### Default Recommendation

**For most projects: Stanza**
- Balanced accuracy, speed, usability
- Best documentation and community
- Future-proof (UD standard, Stanford-backed)
- Works for Chinese + potential future languages

### When to Choose Alternatives

**Choose HanLP if**:
- Need semantic dependencies
- Building comprehensive NLP pipeline (classification, sentiment, etc.)
- 130+ languages required
- Comfortable with heavier dependencies

**Choose LTP if**:
- Chinese-only project (confirmed)
- Need semantic dependencies
- Want MTL efficiency (multiple tasks at once)
- Prefer HIT academic standards

**Choose CoreNLP if**:
- Java ecosystem requirement
- Legacy system maintenance
- Research reproduction (specific old versions)

**Choose UD framework if**:
- Building custom parser from scratch
- Cross-linguistic research (annotation consistency)
- Training on new languages (use UD treebanks)

## Confidence Level

**80-90% confidence** - Recommendations based on:
- Published research (architecture descriptions)
- Official documentation (API patterns, performance)
- Community evidence (GitHub issues, papers)

**Validation recommended**:
- Benchmark on your domain data (news, legal, medical, etc.)
- Test with your typical sentence lengths and complexity
- Measure actual throughput in your infrastructure

## Next Steps

1. **S3 Need-Driven**: Match your specific use case to library strengths
2. **S4 Strategic**: Consider long-term maintenance and ecosystem trends
3. **Hands-on validation**: Download Stanza + HanLP + LTP, test on sample data
4. **Domain benchmarking**: Evaluate accuracy on your specific domain (if critical)
