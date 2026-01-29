# S1 Recommendation: CJK Embedding Models Landscape

## Key Findings

The CJK embedding model landscape divides into two clear categories:

### 1. Chinese-Specialized Models
- **M3E** and **text2vec-chinese** focus exclusively on Chinese
- Optimized for Chinese-only applications
- Lighter weight, faster inference
- Strong performance on Chinese benchmarks

### 2. Multilingual Models
- **LaBSE**, **multilingual-e5**, and **sentence-transformers** (multilingual variants)
- Handle CJK + many other languages
- Essential for cross-lingual tasks
- Larger models with broader capabilities

## Performance Observations

**Chinese-Only Tasks:**
- M3E and text2vec-chinese excel at Chinese semantic similarity
- Purpose-built tokenization gives edge over general multilingual models
- Faster inference due to smaller model sizes

**Cross-Lingual Tasks:**
- multilingual-e5 shows strongest MTEB benchmark performance
- LaBSE specialized for translation-pair training (excellent for CJK ↔ English)
- sentence-transformers provides most flexibility (model hub ecosystem)

**Japanese/Korean:**
- Multilingual models (e5, LaBSE, sentence-transformers) required
- No Japanese/Korean-specific embedding models in survey
- Performance gap: multilingual models handle J/K better than Chinese-specific models handle beyond Chinese

## S2 Deep Dive Priorities

### High Priority (Full Technical Analysis)
1. **multilingual-e5** - State-of-the-art multilingual, recent release, strong benchmarks
2. **M3E** - Best Chinese-specific option, growing adoption
3. **LaBSE** - Unique translation-pair training, Google production quality

### Medium Priority (Focused Analysis)
4. **sentence-transformers** - Framework rather than single model, ecosystem analysis
5. **text2vec-chinese** - Practical library, but overlaps with M3E strengths

## Key Questions for S2
- Quantitative benchmark comparison on CJK semantic similarity tasks
- Memory and latency profiles for each model
- Fine-tuning capabilities and domain adaptation
- Handling of mixed CJK-English text (code-switching)
- Production deployment patterns (ONNX, quantization, API wrappers)

## Surprising Insights
- No dedicated Japanese or Korean embedding models found (gap in market)
- Chinese-specific models (M3E) surprisingly competitive with large multilingual models for Chinese-only tasks
- sentence-transformers as framework enables model mixing (e.g., use M3E via sentence-transformers API)
- multilingual-e5 relatively recent (2023) but already state-of-the-art on benchmarks

## Strategic Implications
- **If Chinese-only**: M3E or text2vec-chinese sufficient, lower TCO
- **If cross-lingual**: Must use multilingual model, multilingual-e5 emerging winner
- **If Japanese/Korean**: No choice but multilingual models (LaBSE, e5, sentence-transformers)
- **If uncertain about future languages**: Start with multilingual-e5 (headroom for expansion)
