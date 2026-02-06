# S1 Rapid Decision Guide

## Quick Selection Matrix

| If you need... | Choose | Why |
|----------------|--------|-----|
| **Python, production speed** | rapidfuzz | 5-50x faster, C++ core, maintained |
| **Python, prototyping/research** | textdistance | 40+ algorithms, easy debugging |
| **JavaScript, lightweight** | string-similarity | <5KB, zero deps, browser-friendly |
| **Rust projects** | strsim | Native performance, memory safety |
| **Enterprise Java/Spring** | Apache Commons Text | Battle-tested, enterprise support |

## Common Patterns from Community

### Python Ecosystem Consensus
- **Production:** rapidfuzz dominates (12M downloads/mo)
- **Research:** textdistance for algorithm exploration
- **Pattern:** "Prototype with textdistance, optimize with rapidfuzz"

### JavaScript/TypeScript
- **Browser:** string-similarity (lightweight, zero deps)
- **Node.js server:** natural or talisman (more algorithms)
- **Pattern:** Client uses Dice coefficient, server uses Levenshtein

### Systems Programming
- **Rust:** strsim (zero-cost abstractions, memory safe)
- **Go:** go-levenshtein or agnivade/levenshtein
- **Pattern:** CLI tools prefer single-metric libraries for minimal binaries

### Enterprise Java
- **Default:** Apache Commons Text (stability first)
- **Performance-critical:** JNI wrappers to C++ (rare)
- **Pattern:** Trade raw speed for backwards compatibility

## Decision Flowchart

```
Need string similarity?
│
├─ Python?
│  ├─ Production performance critical? → rapidfuzz
│  └─ Exploring algorithms? → textdistance
│
├─ JavaScript/TypeScript?
│  ├─ Browser/frontend? → string-similarity
│  └─ Node.js backend with load? → natural, talisman
│
├─ Rust?
│  └─ → strsim
│
├─ Java/JVM?
│  ├─ Enterprise/Spring? → Apache Commons Text
│  └─ Kotlin? → kotlin-string-similarity
│
└─ Other?
   └─ Check ecosystem-specific recommendations in S2
```

## Red Flags

**Avoid these anti-patterns:**

❌ Using pure Python implementations in production hot paths (10-100x slower)
❌ Bundling 40-algorithm libraries when you only need Levenshtein
❌ Implementing your own edit distance (bug-prone, slower than optimized libs)
❌ Choosing unmaintained libraries (python-Levenshtein → use rapidfuzz instead)
❌ Using heavy JVM libraries in size-constrained microservices

## Ecosystem-Specific Gotchas

**Python:**
- `python-Levenshtein` is deprecated → use `rapidfuzz` or `Levenshtein` (maintained fork)
- `fuzzywuzzy` → use `rapidfuzz` (10x faster, drop-in replacement)

**JavaScript:**
- Many libraries have TypeScript declaration issues → check @types packages
- Pure JS is often fast enough for UI; use WASM only if profiling shows bottleneck

**Java:**
- Avoid rolling your own with Apache Commons Lang (use Commons Text successor)
- Thread safety matters more in Java than Python/JS (Commons Text is thread-safe)

## When to Deep-Dive

Move to S2 (Comprehensive Analysis) if:
- Performance is critical (need algorithm-specific benchmarks)
- Choosing between Levenshtein variants (OSA vs Damerau-Levenshtein)
- Integrating with specific frameworks (Spring, Django, React)
- Need rare metrics (compression-based, phonetic)

Move to S3 (Need-Driven) if:
- Specific domain (genomics, name matching, fuzzy search UX)
- Compliance requirements (GDPR, HIPAA affect library choice)
- Multi-language projects (need consistent behavior across ecosystems)

Move to S4 (Strategic) if:
- Long-term maintenance burden matters
- Vendor/ecosystem lock-in concerns
- Team expertise and hiring considerations
- Evaluating build vs integrate vs buy
