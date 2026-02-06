# Tegaki: Open-Source Handwriting Framework

## Quick Assessment

| Factor | Score | Evidence |
|--------|-------|----------|
| **Popularity** | 6/10 | ~200 GitHub stars, active Python community |
| **Integration Ease** | 7/10 | Python-friendly, good documentation, multiple backends |
| **Production Readiness** | 7/10 | Stable API, used in several IME projects |
| **Cost/Licensing** | 10/10 | GPL/LGPL, completely free |
| **Overall Rapid Score** | **7.5/10** | Solid choice for Python-based projects |

## What It Is

Tegaki is a Python-based handwriting recognition framework that provides:
- Stroke capture and normalization
- Multiple recognition engines (HMM, neural networks)
- Training tools for custom models
- Multi-language support (CJK focus)

**Key strength:** Flexible architecture - can plug in different recognition backends.

## Speed Impression

**Pros:**
- Well-documented Python API
- Active community (Chinese/Japanese users)
- Modular design (swap recognition engines easily)
- Training tools included (can customize for specific domains)
- Works offline (no cloud dependency)

**Cons:**
- Python dependency may be heavy for embedded systems
- Slower than native C++ solutions (Zinnia)
- Model training requires ML expertise
- Less active development recently (mature = stable, but slow updates)

## Integration Snapshot

```python
# Example from docs (conceptual):
from tegaki import recognizer

# Load pre-trained model
rec = recognizer.Recognizer("models/japanese.model")

# Recognize stroke data
strokes = capture_handwriting()  # Your stroke capture code
results = rec.recognize(strokes, n=5)  # Top 5 candidates

print(results[0].character)  # Best match
```

**Integration time estimate:** 1-2 weeks (stroke capture + model integration)

## When to Use

**Good fit:**
- Python-based applications (web backends, desktop apps)
- Projects requiring custom model training
- Multi-language recognition (Chinese + Japanese + Korean)
- Educational applications (stroke-by-stroke feedback)

**Not ideal:**
- Resource-constrained embedded systems (use Zinnia instead)
- Need absolute fastest recognition (<50ms - use Zinnia)
- Commercial enterprise (may prefer supported cloud APIs)

## Rapid Verdict

✅ **Recommended** for Python projects requiring flexibility and customization.
⚠️ **Consider Zinnia** if speed is critical or deploying on resource-constrained devices.
⚠️ **Consider cloud ML** if accuracy is more important than offline capability.

**Differentiation:** Best balance of flexibility, ease of use, and open-source freedom.
