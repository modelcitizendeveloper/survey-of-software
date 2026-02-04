# S1 RAPID DISCOVERY: Intent Classification Libraries

**Experiment**: 1.033.1 Intent Classification Libraries (subspecialization of 1.033 NLP Libraries)
**Date**: 2025-10-07
**Duration**: 20 minutes
**Context**: QRCards needs production-ready intent classification to replace slow Ollama prototype (2-5s latency)

## Executive Summary

Identified 5 production-ready solutions for intent classification with varying trade-offs between accuracy, speed, and ease of use:

1. **Hugging Face Zero-Shot Classification** (facebook/bart-large-mnli) - Best for quick deployment, no training required
2. **SetFit** (Sentence Transformers) - Best balance of accuracy, speed, and data efficiency
3. **DistilBERT Fine-tuned** - Best for production speed requirements (<50ms)
4. **Rasa NLU with DIET** - Best for conversational AI with entity extraction
5. **GPT-4 Turbo via API** - Best accuracy (96%) for simple use cases (<30 intents)

**Recommendation for QRCards**: Start with SetFit or DistilBERT for CLI/analytics use cases, consider Zero-Shot for support ticket triage with dynamic categories.

---

## Quick Comparison Table

| Solution | Speed (Latency) | Accuracy | Training Data Needed | Model Size | Production Ready | Best For |
|----------|----------------|----------|---------------------|------------|-----------------|----------|
| **BART Zero-Shot** | ~200-500ms | Good (85-90%) | None | 407M params | Yes | Dynamic categories, rapid prototyping |
| **SetFit** | ~50-100ms | Excellent (>95%) | 8-64 examples | 355M params | Yes | Few-shot learning, balanced performance |
| **DistilBERT Fine-tuned** | <50ms | Excellent (95%+) | 100-1000 examples | 66M params | Yes | High-throughput, low-latency production |
| **Rasa DIET** | ~100-200ms | Excellent (>BERT) | 500+ examples | Configurable | Yes | Conversational AI, entity extraction |
| **GPT-4 Turbo API** | ~500-2000ms | Best (96%) | None | N/A (API) | Yes | Simple bots, <30 intents, cloud-only |

---

## Detailed Findings

### 1. Hugging Face Zero-Shot Classification (facebook/bart-large-mnli)

**What it is**: Pre-trained BART model that classifies text into any candidate labels without training.

**Key Characteristics**:
- 407M parameters
- No training required - provide labels at inference time
- Works by treating labels as hypotheses in NLI framework
- Single model handles unlimited dynamic intent categories

**Speed**: ~200-500ms per inference (CPU), faster on GPU

**Accuracy**: 85-90% on diverse tasks, "surprisingly effective" per Hugging Face

**Implementation**:
```python
from transformers import pipeline
classifier = pipeline("zero-shot-classification",
                     model="facebook/bart-large-mnli")
result = classifier(text, candidate_labels=['intent1', 'intent2'])
```

**Pros**:
- Zero training required
- Dynamic intent categories
- Easy integration
- Well-documented and maintained

**Cons**:
- Slower inference than smaller models
- Large model size (407M params)
- May struggle with domain-specific terminology

**Best for**: Support ticket triage with evolving categories, rapid prototyping

---

### 2. SetFit (Sentence Transformers)

**What it is**: Efficient few-shot learning framework using sentence transformers, trained via contrastive learning.

**Key Characteristics**:
- 355M parameters (RoBERTa-based)
- Requires only 8-64 labeled examples per intent
- Outperforms GPT-3 on RAFT benchmark while being 1600x smaller
- Ranked 2nd after Human Baseline on few-shot classification

**Speed**:
- Training: 30 seconds on V100 GPU (8 examples)
- Inference: ~50-100ms
- Can run on CPU in "just a few minutes" for training
- Supports 123x speedup via model distillation

**Accuracy**: 95%+ on RAFT benchmark, outperformed GPT-3 in 7 of 11 tasks

**Implementation**:
```python
from setfit import SetFitModel
model = SetFitModel.from_pretrained("sentence-transformers/paraphrase-mpnet-base-v2")
model.fit(train_texts, train_labels)  # 8-64 examples
predictions = model.predict(test_texts)
```

**Pros**:
- Minimal training data required
- Fast training and inference
- Can run on modest hardware (Google Colab, even CPU)
- State-of-the-art accuracy with few examples
- Active development by Hugging Face

**Cons**:
- Still requires some labeled examples
- More complex setup than zero-shot
- Medium model size

**Best for**: CLI command understanding, analytics query classification with limited training data

---

### 3. DistilBERT Fine-tuned

**What it is**: Distilled version of BERT - 40% smaller, 60% faster, retains 95% of BERT's performance.

**Key Characteristics**:
- 66M parameters (smallest of the transformer options)
- Requires fine-tuning on domain data
- Optimized for production deployment
- Banking-intent-distilbert-classifier available on Hugging Face as reference

**Speed**:
- **<50ms inference time** with optimization
- **<10ms possible** with ONNX quantization
- 60% faster than BERT-base
- 71% faster on mobile devices
- Supports 100+ messages/second

**Accuracy**: 95%+ when properly fine-tuned, retains >95% of BERT performance

**Implementation**:
```python
from transformers import AutoModelForSequenceClassification, AutoTokenizer
model = AutoModelForSequenceClassification.from_pretrained("distilbert-base-uncased")
# Fine-tune on your data
# Or use pre-trained: "lxyuan/banking-intent-distilbert-classifier"
```

**Optimization**:
- ONNX quantization: <100MB memory
- TensorRT on NVIDIA GPUs
- INT8 quantization for edge deployment

**Pros**:
- Fastest transformer option
- Small model size (<100MB optimized)
- Production-proven
- Can run on edge devices
- Excellent throughput

**Cons**:
- Requires 100-1000 labeled examples
- Need to retrain for new intents
- Fine-tuning complexity

**Best for**: High-throughput production systems, edge deployment, latency-critical applications (<100ms requirement)

---

### 4. Rasa NLU with DIET Architecture

**What it is**: Complete conversational AI framework with Dual Intent and Entity Transformer architecture.

**Key Characteristics**:
- Multi-task architecture (intent + entity recognition)
- Integrates Hugging Face transformers as featurizers
- DIET architecture outperforms fine-tuned BERT
- 6x faster to train than BERT
- Full pipeline management (training, versioning, deployment)

**Speed**: ~100-200ms for intent + entity extraction

**Accuracy**: State-of-the-art, outperforms BERT fine-tuning on Rasa benchmarks

**Data Requirements**: 500+ examples recommended, 5000-50000 for complex bots

**Implementation**:
```yaml
# config.yml
pipeline:
  - name: LanguageModelFeaturizer
    model_name: "bert"
  - name: DIETClassifier
    epochs: 100
```

**Pros**:
- Complete conversational AI solution
- Intent + entity extraction in one pass
- Active development and community
- Production deployment tools included
- Supports custom Hugging Face models

**Cons**:
- Heavier framework (not just classification)
- Steeper learning curve
- Requires more training data
- More infrastructure complexity

**Best for**: Full conversational AI systems, chatbots needing entity extraction, teams wanting managed NLU pipeline

---

### 5. GPT-4 Turbo API (Cloud-based)

**What it is**: OpenAI's GPT-4 Turbo accessed via API for zero-shot intent classification.

**Key Characteristics**:
- No training required
- 96% accuracy in 2024 tests
- Best for <30 intent categories
- Cloud-only (API calls)

**Speed**: ~500-2000ms (network + inference)

**Accuracy**: 96% on common intents (2024 benchmark), outperforms smaller models

**Cost**: API pricing per token

**Implementation**:
```python
from openai import OpenAI
client = OpenAI()
response = client.chat.completions.create(
    model="gpt-4-turbo",
    messages=[{"role": "system", "content": "Classify the intent: {intents}"},
              {"role": "user", "content": user_message}]
)
```

**Pros**:
- Highest accuracy
- No infrastructure required
- No training needed
- Excellent for complex/ambiguous cases

**Cons**:
- Highest latency
- Ongoing API costs
- Cloud dependency
- May exceed 2-5s latency target
- Privacy/data concerns

**Best for**: Low-volume, high-accuracy needs; cloud-based applications; simple intent sets

---

## Production Readiness Assessment

### Ready for Production Now:
1. **DistilBERT** - Most production deployments, proven at scale
2. **SetFit** - Few-shot scenarios, balanced needs
3. **Zero-Shot BART** - Dynamic categories, no training time
4. **Rasa DIET** - Conversational AI platforms

### Requires More Setup:
5. **GPT-4 API** - Ready but may not meet latency requirements

---

## Key Insights

### Speed Benchmarks (2024 Production Standards):
- **Target latency**: <100ms for optimal UX
- **DistilBERT optimized**: <10-50ms
- **SetFit**: 50-100ms
- **Zero-Shot BART**: 200-500ms
- **Rasa DIET**: 100-200ms
- **GPT-4 API**: 500-2000ms

### Accuracy Hierarchy:
1. GPT-4 Turbo (96%)
2. SetFit (95%+, outperforms GPT-3)
3. DistilBERT fine-tuned (95%+)
4. Rasa DIET (>BERT)
5. Zero-Shot BART (85-90%)

### Data Efficiency:
- **Zero training**: Zero-Shot BART, GPT-4 API
- **8-64 examples**: SetFit
- **100-1000 examples**: DistilBERT
- **500+ examples**: Rasa DIET

---

## Initial Recommendations for QRCards Use Cases

### CLI Command Understanding
**Recommendation**: SetFit or DistilBERT
- **Rationale**:
  - Limited training data available initially
  - Need fast inference (<100ms)
  - Static intent set (help, search, create, update, etc.)
  - SetFit handles few-shot well, DistilBERT better for production scale

### Support Ticket Triage
**Recommendation**: Zero-Shot BART or SetFit
- **Rationale**:
  - Categories may evolve over time
  - Zero-Shot allows dynamic label addition
  - SetFit if categories stabilize
  - 200-500ms acceptable for async triage

### Analytics Query Classification
**Recommendation**: DistilBERT fine-tuned
- **Rationale**:
  - Need lowest latency (<50ms)
  - Well-defined query patterns
  - High volume expected
  - Worth investment in training data collection

### General Strategy
1. **Start**: Zero-Shot BART for all use cases (no training, validates approach)
2. **Collect**: Gather labeled examples from production usage
3. **Transition**: Move to SetFit (50-100 examples) or DistilBERT (500+ examples)
4. **Optimize**: Apply ONNX quantization and TensorRT for production deployment

---

## Questions for Deeper Investigation (S2)

### Technical Deep Dive:
1. What is the actual latency of each solution on our target hardware (CPU vs GPU)?
2. How much training data can we realistically collect for each use case?
3. What is the accuracy degradation on domain-specific terminology (QRCards-specific)?
4. Can we use hybrid approaches (rule-based for high-confidence, ML for ambiguous)?

### Implementation Details:
5. What is the deployment footprint for each solution (memory, CPU, GPU)?
6. How do we handle model versioning and A/B testing?
7. What are the retraining workflows for each approach?
8. How do confidence scores compare across solutions?

### Integration:
9. How do these integrate with existing Ollama infrastructure?
10. Can we run multiple models in parallel (fast first, accurate fallback)?
11. What monitoring/observability is needed for production?
12. How do we handle out-of-distribution intents (unknown/other)?

### Cost/Benefit:
13. What is the total cost of ownership (training, inference, maintenance)?
14. How much accuracy improvement justifies slower inference?
15. What is the expected ROI compared to current Ollama approach?

### Advanced Features:
16. Multi-intent classification (commands with multiple intents)?
17. Context-aware classification (conversation history)?
18. Multilingual support requirements?
19. Active learning for continuous improvement?

---

## Next Steps

### Immediate (S2 Comprehensive Discovery):
1. Benchmark all 5 solutions on QRCards sample data
2. Measure actual latency on target deployment hardware
3. Test accuracy on domain-specific examples
4. Evaluate integration complexity with existing systems

### Short-term (S3 Need-Driven Discovery):
5. Prototype top 2 solutions (likely SetFit + DistilBERT)
6. Collect baseline training data (100+ examples)
7. Set up evaluation framework with metrics
8. Plan A/B testing strategy

### Medium-term (S4 Strategic Discovery):
9. Production deployment architecture
10. Model monitoring and retraining pipeline
11. Cost analysis and optimization
12. Scale testing and performance tuning

---

## References

### Key Resources:
- **Hugging Face Zero-Shot**: https://huggingface.co/facebook/bart-large-mnli
- **SetFit**: https://huggingface.co/blog/setfit
- **DistilBERT**: https://huggingface.co/docs/transformers/model_doc/distilbert
- **Rasa DIET**: https://rasa.com/blog/introducing-diet/
- **Banking Intent Classifier**: https://huggingface.co/lxyuan/banking-intent-distilbert-classifier

### Benchmark Studies:
- SetFit RAFT benchmark (2023)
- Production latency requirements (<100ms, 2024 study)
- GPT-4 Turbo intent accuracy (96%, 2024)
- DistilBERT optimization guide (sub-10ms inference)

### Market Context:
- Conversational AI market: $13.2B (2024) to $49.9B (2030)
- Production latency target: <100ms for optimal UX
- LLM accuracy improving but latency remains challenge
- Hybrid approaches (edge + cloud) gaining traction

---

## Methodology Notes

**Search Strategy**:
- Focused on production-ready solutions (2024-2025)
- Prioritized speed benchmarks and latency data
- Cross-referenced accuracy claims across sources
- Validated with real-world implementations (Hugging Face models)

**Time Allocation**:
- Web research: 15 minutes
- Analysis and synthesis: 5 minutes
- Total: 20 minutes

**Limitations**:
- Did not benchmark on actual hardware
- Accuracy numbers from different datasets (not directly comparable)
- Pricing analysis deferred to S2
- No hands-on testing yet

**Confidence Level**: High for general findings, Medium for specific performance claims (need validation)
