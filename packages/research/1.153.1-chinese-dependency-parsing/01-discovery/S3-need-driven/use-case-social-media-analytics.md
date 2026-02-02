# Use Case: Chinese Social Media Analytics and Sentiment Analysis

## Who Needs This

**User Persona**: Data scientists and ML engineers at social media monitoring companies or brand management agencies analyzing Chinese social platforms (Weibo, Douyin, WeChat).

**Organization Context**:
- Social media monitoring platforms
- Brand reputation management agencies
- Market research firms
- Government/academic social science research

**Technical Background**:
- Data science background (Python, pandas, scikit-learn)
- ML experience (classification, clustering, topic modeling)
- Basic NLP (sentiment analysis, entity extraction)

**Scale**: Analyzing millions of posts per day from Weibo, Douyin, Xiaohongshu, etc.

## Why They Need Dependency Parsing

### Primary Goals

**Aspect-Based Sentiment Analysis (ABSA)**:
- Extract opinions about specific product features
- Example: "屏幕很清晰但电池不耐用" (screen is clear, but battery doesn't last)
- Identify syntactic relations to map sentiment to aspects

**Opinion Holder Extraction**:
- Determine who holds which opinion
- Example: "他说服务很好" (He says service is good) → "他" is opinion holder
- Use dependency relations (nsubj) to find subjects

**Event Detection and Extraction**:
- Identify events mentioned in posts (protests, scandals, product launches)
- Extract event participants and their roles (agent, patient, location)
- Build timelines of event mentions

**Fake News and Rumor Detection**:
- Analyze syntactic complexity (simple claims vs nuanced reporting)
- Detect hedging and attribution patterns ("据说", "有人说")
- Compare syntactic structures across sources

### Success Criteria

- **Accuracy**: Better sentiment classification (F1 improvement vs bag-of-words)
- **Actionability**: Identify specific issues (not just "negative sentiment")
- **Speed**: Near real-time processing (seconds to minutes, not hours)
- **Scalability**: Handle spikes (viral posts, breaking news)
- **Cost-effective**: Reasonable compute costs for high volume

## Requirements and Constraints

### Technical Requirements

**Must-have**:
- High throughput (millions of posts per day)
- Chinese-specific handling (informal text, emojis, abbreviations)
- Semantic role understanding (who did what to whom)
- Integration with existing ML pipelines (scikit-learn, PyTorch)

**Nice-to-have**:
- Domain adaptation (social media text differs from news)
- Robust to noise (typos, netspeak, mixed script)
- Emoji and punctuation handling

### Resource Constraints

**Compute**:
- Cloud-based (AWS, Alibaba Cloud)
- GPU budget available (justified by business value)
- Real-time constraints (process within minutes of posting)

**Budget**:
- Open-source preferred (avoid per-API costs)
- Can invest in infrastructure (ROI from insights)

**Skills**:
- Data science team (not NLP researchers)
- Need practical tools (not academic experiments)
- Prefer Python ecosystem (pandas, sklearn, PyTorch)

## Library Recommendation

### Primary Choice: **HanLP (with semantic dependencies)**

**Why HanLP**:

1. **Semantic dependency parsing**: Critical for ABSA and opinion extraction
   - DAG structure (multiple semantic heads) captures Chinese patterns
   - Semantic roles (agent, patient, location) map directly to analysis needs
   - Example: "我觉得屏幕很清晰" → "我" is experiencer, "屏幕" is theme, "清晰" is attribute

2. **Chinese-optimized**: Handles social media challenges
   - Better segmentation for informal text (vs UD-based Stanza)
   - Trained on broader Chinese corpora (not just news/Wikipedia)
   - Handles mixed script (Chinese + English + emojis)

3. **Multi-task efficiency**: Extract multiple features in one pass
   - Segmentation + POS + NER + dep parsing + SRL
   - Single API call for all features (reduces latency)
   - Shared encoder amortizes compute cost

4. **Flexible deployment**: REST API or native Python
   - REST for microservices (social media ingestion pipeline)
   - Native Python for batch analytics (nightly sentiment reports)
   - GPU support (throughput for high-volume processing)

**Implementation Pattern**:

```
Social Media Stream (Weibo API, etc.)
 ↓
Preprocessing (clean, normalize)
 ↓
HanLP REST API
 ├─ Semantic dependency parsing (opinion→aspect linking)
 ├─ NER (brand names, products, people)
 ├─ POS (identify adjectives, verbs for sentiment)
 ↓
Feature Extraction
 ├─ Aspect-sentiment pairs (from semantic deps)
 ├─ Opinion holder (from nsubj, agent roles)
 ├─ Event tuples (agent-verb-patient from semantic graph)
 ↓
ML Models (sentiment classifiers, event detectors)
 ↓
Analytics Dashboard (brand reputation, trending issues)
```

**Domain Adaptation**:
- Fine-tune HanLP on annotated social media corpus
- Example: 5K Weibo posts manually labeled for aspects + sentiments
- Improves segmentation (netspeak) and parsing (informal syntax)

### Alternative: **LTP (for Chinese-only with MTL efficiency)**

**When to choose LTP instead**:

**Chinese-only focus**:
- Not monitoring other languages (English Twitter, Japanese Twitter)
- LTP's Chinese-only design is acceptable

**Knowledge distillation advantage**:
- LTP's MTL model rivals single-task accuracy
- Faster than HanLP's single-task pipeline (if not using HanLP MTL)

**HIT annotation standards**:
- Prefer HIT's semantic dependency scheme
- Integration with HIT research tools

**Trade-offs**:
- Smaller community (less Stack Overflow support)
- Cannot extend to multilingual (if future requirement)
- Documentation primarily Chinese (team must read Chinese)

### Why Not Stanza

**Reasons to avoid**:

1. **No semantic dependencies**: Only syntactic parsing
   - Harder to extract aspect-sentiment pairs
   - Misses semantic roles (agent, patient) critical for opinion analysis

2. **UD tokenization**: Optimized for news, not social media
   - Lower accuracy on informal text (netspeak, abbreviations)
   - Less robust to noise (typos, emoji usage)

3. **No sentiment/opinion features**: Pure syntactic tool
   - Requires separate models for sentiment, NER, etc.
   - More pipeline complexity (multiple tools)

**Exception**: If only syntactic features needed (rare for social media analytics).

### Why Not CoreNLP

**Reasons to avoid**:
- Pre-neural (lower accuracy on noisy social media text)
- No semantic dependencies
- Java (Python dominates data science workflows)
- Slow (can't handle real-time social media volumes)

## Risk Factors and Mitigations

### Risk: Social Media Text Differs from Training Data

**Problem**: HanLP trained on news/formal text, but social media is informal.
- Netspeak ("666", "yyds"), abbreviations, typos
- Emoji usage, mixed script (Chinese + pinyin + English)
- Lower parsing accuracy → worse sentiment analysis

**Mitigation**:
- Fine-tune on social media corpus (1K-5K annotated posts)
- Preprocessing normalization (expand abbreviations, remove emojis)
- Ensemble with rule-based patterns (complement parser errors)
- Human-in-the-loop validation (review parser errors on key brands)

### Risk: Real-Time Latency Requirements

**Problem**: Viral posts require immediate analysis (minutes, not hours).
- Single HanLP instance too slow (hundreds of posts/second during spikes)
- GPU costs add up at high volume

**Mitigation**:
- Auto-scaling (spin up GPU instances during traffic spikes)
- Priority queue (brand mentions first, general posts later)
- Streaming architecture (Kafka, process incrementally)
- Approximations (parse sample of posts, extrapolate trends)

### Risk: Semantic Dependencies May Be Overkill

**Problem**: Syntactic parsing + simple rules might suffice for basic sentiment.
- Semantic parsing adds compute cost
- Returns diminish if downstream models don't use semantic features

**Mitigation**:
- A/B test (syntactic-only Stanza vs semantic HanLP)
- Measure F1 improvement (is semantic parsing worth cost?)
- Start simple (Stanza), upgrade to HanLP if accuracy insufficient
- Profile pipeline (identify bottlenecks, optimize)

### Risk: Handling Multiple Chinese Variants

**Problem**: Social media uses Simplified (Mainland), Traditional (Taiwan/HK), and mixed.
- Parser trained on Simplified (lower accuracy on Traditional)
- Code-switching (Chinese + English in same sentence)

**Mitigation**:
- Preprocessing conversion (Traditional → Simplified via OpenCC)
- Language detection (route Chinese vs English to different parsers)
- Fine-tuning on mixed-script data (if available)

## Expected Outcomes

**Timeline**: 2-4 months for production deployment
- Week 1-2: Prototype (HanLP + sentiment classifier on sample data)
- Week 3-6: Integration (connect to social media ingestion pipeline)
- Week 7-12: Fine-tuning (annotate social media corpus, retrain models)
- Week 13-16: Scaling (GPU infrastructure, auto-scaling, monitoring)

**Deliverables**:
- Aspect-based sentiment analysis (F1 improvement over baseline)
- Opinion holder extraction (who said what about what)
- Event detection (trending topics, crisis identification)
- Real-time dashboard (brand reputation, competitor analysis)

**Business Impact**:
- Faster crisis response (detect negative sentiment spikes in minutes)
- Granular insights (specific product issues, not just "negative")
- Competitive intelligence (what are customers saying about competitors)

## Summary

**For social media analytics, HanLP is the recommended choice** due to semantic dependency support, Chinese optimization, and multi-task efficiency. LTP is a viable alternative for Chinese-only projects. Stanza and CoreNLP lack the semantic features critical for opinion analysis and aren't optimized for informal Chinese text.

**Key success factors**:
- Domain adaptation (fine-tune on social media corpus)
- Semantic dependencies (extract aspect-sentiment pairs accurately)
- Scalable infrastructure (auto-scaling for traffic spikes)
- Validation (A/B test, measure F1 improvement vs baseline)
