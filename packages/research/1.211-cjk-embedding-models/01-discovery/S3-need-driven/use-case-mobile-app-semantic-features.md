# Use Case 4: Mobile App Semantic Features

## Business Context

**Industry**: Mobile applications (note-taking, productivity, content apps)
**Application**: On-device semantic search, smart suggestions, content clustering
**Constraints**: 50-100MB model budget, offline capability, battery efficiency
**Languages**: Chinese-only or Chinese-English bilingual

## Technical Requirements

- **Model Size**: <100MB (ideally <50MB)
- **Offline**: Must run on-device (no API calls)
- **Battery**: Efficient inference (avoid GPU on mobile)
- **Latency**: <200ms for good UX
- **Platform**: iOS (CoreML) and Android (TFLite)

## Model Evaluation

**Winner: M3E-small (Chinese-only) or multilingual-e5-small (bilingual)**

| Model | Size (INT8) | Mobile Latency | Quality (Chinese STS) | CoreML/TFLite |
|-------|-------------|----------------|----------------------|---------------|
| M3E-small | 24 MB | ~180ms | 78.5 | ✓ (via ONNX) |
| multilingual-e5-small | 118 MB | ~250ms | 76.2 (multilingual) | ✓ (via ONNX) |
| M3E-base | 110 MB | ~400ms | 83.1 | ✗ (too slow) |

**Rationale**: M3E-small fits mobile constraints. 24MB INT8 model, acceptable quality (78.5 vs 83.1 for base), fast enough for mobile CPUs.

**Trade-off**: ~5 points lower quality than M3E-base, but mobile deployment possible.

## Deployment Architecture

```
[Mobile App]
  ├─ [M3E-small CoreML Model] (iOS)
  ├─ [M3E-small TFLite Model] (Android)
  ├─ [SQLite Vector Store] (on-device)
  │   └─ User's notes/content (up to 10K items)
  ├─ [Semantic Search Module]
  │   ├─ Embed query on-device
  │   ├─ ANN search (FAISS-lite or custom)
  │   └─ Return top-10 results
  └─ [Batch Embedding] (background)
      └─ Embed new content when charging + WiFi
```

## TCO Analysis

**Development Costs**:
- Model conversion (ONNX → CoreML/TFLite): 1 week, $5K
- Integration + testing: 2 weeks, $10K
- **Total one-time**: $15K

**Operational Costs**:
- **$0/month** (on-device, no servers)
- Model updates: $1K/year (new model versions)

**User Benefits**:
- Offline semantic search (no data usage)
- Privacy (data never leaves device)
- Fast (no network latency)

**Comparison to Cloud API**:
- Cloud API: $0.0001/query × 100 queries/user/month × 1M users = $10,000/month = **$120K/year**
- On-device: $15K (one-time) + $1K/year = **$16K total year 1**
- **Savings**: $104K/year starting year 2

## Implementation

**Phase 1** (2 weeks): Convert M3E-small to CoreML/TFLite
**Phase 2** (2 weeks): Integrate into app, implement on-device vector search
**Phase 3** (1 week): Optimize inference (quantization, caching, batching)
**Phase 4** (1 week): Beta test, measure battery impact

## Challenges & Solutions

**Challenge 1: Model Size (App Store limits)**
- **Solution**: On-demand download (download model on first use, not in app bundle)
- **Alternative**: Use even smaller distilled model (M3E-tiny, custom distillation)

**Challenge 2: Inference Speed on Low-End Devices**
- **Solution**: Feature flag (disable on devices older than 3 years)
- **Alternative**: Hybrid (on-device for high-end, cloud API for low-end)

**Challenge 3: Embedding Freshness (New Content)**
- **Solution**: Background embedding when charging + WiFi
- **Fallback**: Embed on-demand for immediate search (slight UX delay)

## Recommendation

**Model**: M3E-small (24MB INT8) for Chinese-only
**Alternative**: multilingual-e5-small (118MB INT8) if bilingual needed
**Deployment**: On-device (CoreML/TFLite)
**TCO**: $15K one-time, $1K/year (vs $120K/year cloud)
**ROI**: Massive (85% cost savings + privacy benefits)
**User Experience**: Offline search, 180ms latency, privacy-first
