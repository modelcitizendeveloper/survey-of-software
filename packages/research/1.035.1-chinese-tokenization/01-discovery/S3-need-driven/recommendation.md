# S3 Recommendation: Scenario-Based Selection

## Quick Use Case Lookup

### E-commerce / Search
**Need**: High recall product search, real-time queries, custom brands
→ **Use: Jieba (search mode) + custom dictionary**

Why: Fine-grained segmentation, fast indexing, easy brand name addition

### Academic Research
**Need**: Maximum accuracy, reproducible results, citable methodology
→ **Use: PKUSEG (domain model) or bert-base-chinese**

Why: Highest accuracy (F1 ~96%), well-documented, standard in publications

### Real-Time Chatbots
**Need**: <50ms latency, handles informal text, robust at scale
→ **Use: LAC (joint seg + NER mode)**

Why: Fast (800 QPS), extracts entities for intent recognition, production-tested

### Multilingual SaaS
**Need**: Unified tokenizer, no language detection, token efficiency
→ **Use: SentencePiece or Qwen/mT5 tokenizer**

Why: Language-agnostic, efficient for CJK, single codebase

## Requirement-to-Library Matrix

| Primary Need | Recommended Library | Alternative |
|--------------|---------------------|-------------|
| **Speed >500 KB/s** | Jieba (full mode) | LAC |
| **Accuracy >95%** | PKUSEG | transformers (BERT) |
| **Low latency (<50ms)** | LAC | Jieba |
| **Custom domains** | PKUSEG + domain model | Jieba + custom dict |
| **Multilingual** | SentencePiece | Qwen tokenizer |
| **Simple integration** | Jieba | LAC |
| **Production scale** | LAC | PKUSEG |
| **Research/academic** | PKUSEG | BERT |
| **Search/IR** | Jieba (search mode) | Character n-grams |
| **NER extraction** | LAC (joint mode) | Separate NER model |

## Persona-Driven Recommendations

### Startup Engineer (Speed to Market)
**Constraints**: Small team, fast iteration, "good enough" quality
**Choose**: Jieba
**Why**: 2 lines of code, works immediately, 80% use cases covered

### Data Scientist (Model Training)
**Constraints**: GPU available, accuracy matters, building custom models
**Choose**: transformers (BERT or Qwen)
**Why**: Integrates with PyTorch/HuggingFace, state-of-the-art accuracy

### Enterprise Architect (Production Scale)
**Constraints**: 10K+ QPS, stability, proven at scale
**Choose**: LAC
**Why**: Baidu production-tested, fast + accurate, joint seg+POS+NER

### Academic Researcher (Publications)
**Constraints**: Reproducibility, standard benchmarks, citations
**Choose**: PKUSEG
**Why**: Published methodology, domain models, highest benchmark accuracy

### Product Manager (Global Expansion)
**Constraints**: Multilingual support, unified UX, cost control
**Choose**: SentencePiece
**Why**: Language-agnostic, efficient for CJK, proven in mT5

## Decision Framework

```
What's your PRIMARY constraint?

SPEED (>400 KB/s needed)
  ├─ Need search recall?
  │  └─ Jieba search mode
  └─ Need accuracy too?
     └─ LAC

ACCURACY (>95% F1 needed)
  ├─ Have domain corpus?
  │  └─ PKUSEG with domain model
  └─ Using transformers?
     └─ BERT-base-chinese

LATENCY (<50ms per request)
  ├─ Need NER too?
  │  └─ LAC (joint mode)
  └─ Just segmentation?
     └─ Jieba

MULTILINGUAL (Chinese + others)
  ├─ Have training corpus?
  │  └─ SentencePiece
  └─ Need pre-trained?
     └─ Qwen or mT5 tokenizer
```

## Common Anti-Patterns to Avoid

❌ **Using BERT for high-volume processing**: Too slow
✅ **Use Jieba or LAC instead**

❌ **Using Jieba for research**: Not reproducible
✅ **Use PKUSEG or BERT instead**

❌ **Separate tokenizers per language**: Maintenance nightmare
✅ **Use SentencePiece for unified approach**

❌ **Byte-level BPE for Chinese-heavy apps**: 2-3x cost
✅ **Use SentencePiece or Qwen instead**

## Validation Strategy

After selecting based on use case:

1. **Prototype** with recommended library
2. **Test on real data** (not benchmarks)
3. **Measure**: Accuracy, latency, cost
4. **Iterate**: Add custom dictionary, tune parameters
5. **Fallback**: Plan B if constraints change

## Next Steps

- **From S3 to S1**: Quick spec sheets for each library
- **From S3 to S2**: Deep technical implementation details
- **From S3 to S4**: Long-term strategic considerations

## Bottom Line

**Match library to YOUR constraints, not theoretical "best"**:
- Jieba: Speed + simplicity
- PKUSEG: Accuracy + domain
- LAC: Balance + production
- SentencePiece: Multilingual + flexibility
- transformers: State-of-art + GPU
