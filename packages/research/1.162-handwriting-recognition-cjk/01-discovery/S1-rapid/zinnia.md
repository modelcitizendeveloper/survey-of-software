# Zinnia: Lightweight Stroke-Based Recognition

## Quick Assessment

| Factor | Score | Evidence |
|--------|-------|----------|
| **Popularity** | 8/10 | Used in multiple production IME systems, active adoption |
| **Integration Ease** | 9/10 | Simple C++ API, bindings for Python/Ruby/Perl/Java |
| **Production Readiness** | 9/10 | Battle-tested in IME applications, stable for 15+ years |
| **Cost/Licensing** | 10/10 | BSD license (very permissive), completely free |
| **Overall Rapid Score** | **9.0/10** | Gold standard for fast, lightweight recognition |

## What It Is

Zinnia is a C++ stroke-based handwriting recognition engine optimized for:
- Real-time input method editors (IME)
- Minimal memory footprint (<5MB with models)
- Fast recognition (<50ms typical)
- Japanese focus (but extensible to Chinese/Korean)

**Key strength:** Speed and efficiency - designed for embedded/mobile environments.

## Speed Impression

**Pros:**
- Extremely fast (20-50ms recognition, <5ms with optimized models)
- Tiny memory footprint (2-5MB depending on model size)
- Native C++ performance (no interpreter overhead)
- Simple, clean API (5-10 lines of code for basic use)
- Language bindings available (Python, Ruby, Perl, Java)
- Proven in production (used by major IME vendors)
- Permissive BSD license (no copyleft restrictions)

**Cons:**
- Japanese-optimized (Chinese/Korean models less mature)
- Requires C++ build toolchain (not pure-Python like Tegaki)
- Model training less flexible than neural network approaches
- Less active community than cloud ML solutions

## Integration Snapshot

```cpp
// Example from docs (C++):
#include <zinnia.h>

zinnia::Recognizer *recognizer = zinnia::Recognizer::create();
recognizer->open("models/handwriting-ja.model");

zinnia::Character *character = zinnia::Character::create();
character->set_width(300);
character->set_height(300);

// Add stroke data (x, y coordinates)
character->add(0, 51, 29);
character->add(0, 117, 41);
// ... more points ...

zinnia::Result *result = recognizer->classify(character, 10);
std::cout << result->value(0) << std::endl;  // Best match

character->destroy();
result->destroy();
recognizer->destroy();
```

```python
# Python binding (via zinnia-python):
import zinnia

recognizer = zinnia.Recognizer()
recognizer.open('/path/to/model')

character = zinnia.Character()
character.set_width(300)
character.set_height(300)
character.add(0, 51, 29)
# ... add stroke points ...

result = recognizer.classify(character, 10)
print(result.value(0))  # Best match
```

**Integration time estimate:** 3-5 days (C++), 1-2 days (Python binding)

## When to Use

**Perfect fit:**
- Input method editors (IME) - Zinnia's original use case
- Mobile/embedded applications (resource constraints)
- Real-time recognition (<100ms latency requirement)
- Offline-first applications (no internet dependency)
- Performance-critical systems

**Not ideal:**
- Need highest accuracy (95%+ - use cloud ML)
- Pure Python projects with complex needs (Tegaki more flexible)
- Document batch processing (cloud APIs more accurate)

## Rapid Verdict

✅ **Highly recommended** for performance-critical applications (IME, mobile, embedded).
✅ **First choice** for offline handwriting input methods.
⚠️ **Consider cloud ML** if accuracy more important than speed/offline capability.

**Differentiation:** Fastest, lightest, most proven for real-time input. The reference implementation for stroke-based recognition.

## Notable Deployments

- Anthy (Japanese IME)
- Various Android/iOS handwriting keyboards
- Embedded Linux systems (e-readers, tablets)

**Production evidence:** Zinnia's deployment in commercial IME products demonstrates production-grade stability and performance.
