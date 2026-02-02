# Feature Comparison Matrix

## Algorithm Coverage

| Algorithm | rapidfuzz | textdistance | string-similarity | strsim | Apache Commons Text |
|-----------|-----------|--------------|-------------------|--------|---------------------|
| **Levenshtein** | ✅ Optimized | ✅ Pure + C backend | ❌ | ✅ | ✅ |
| **Damerau-Levenshtein** | ✅ | ✅ | ❌ | ✅ | ❌ |
| **Hamming** | ✅ | ✅ | ❌ | ✅ | ✅ |
| **Jaro** | ✅ | ✅ | ❌ | ✅ | ❌ |
| **Jaro-Winkler** | ✅ | ✅ | ❌ | ✅ | ✅ |
| **LCS** | ✅ (partial) | ✅ (Str + Seq) | ❌ | ❌ | ✅ |
| **Jaccard** | ❌ | ✅ | ❌ | ❌ | ❌ |
| **Cosine** | ❌ | ✅ | ❌ | ✅ (limited) | ✅ |
| **Dice Coefficient** | ❌ | ✅ | ✅ (primary) | ✅ | ❌ |
| **Soundex** | ✅ | ❌ | ❌ | ❌ | ✅ (via codec) |
| **Metaphone** | ✅ | ❌ | ❌ | ❌ | ✅ (via codec) |
| **Phonetic (MRA, Editex)** | ❌ | ✅ | ❌ | ❌ | ❌ |
| **Compression-based** | ❌ | ✅ (4 variants) | ❌ | ❌ | ❌ |
| **Q-gram variants** | ❌ | ✅ (5 variants) | ❌ | ❌ | ❌ |
| **Token-based (set ops)** | ✅ (3 variants) | ✅ (8 variants) | ❌ | ❌ | ❌ |

**Summary:**
- **Most comprehensive:** textdistance (40+ algorithms)
- **Production-optimized:** rapidfuzz (20+ algorithms, all optimized)
- **Minimal/focused:** string-similarity (1 algorithm), strsim (7 algorithms)
- **Enterprise Java:** Apache Commons Text (5 core algorithms)

## Performance Comparison

**Levenshtein distance (100-character strings, ops/sec):**

| Library | Implementation | Performance | Notes |
|---------|---------------|-------------|-------|
| rapidfuzz | C++ (SIMD) | 400K ops/sec | Threshold optimization, vectorized |
| python-Levenshtein | C | 120K ops/sec | Standard DP with row reuse |
| textdistance + C backend | C | 100K ops/sec | Via python-Levenshtein |
| strsim (Rust) | Rust | 350K ops/sec | Zero-cost abstractions |
| Apache Commons Text | Java | 80K ops/sec | JVM optimized, GC overhead |
| textdistance (pure Python) | Python | 8K ops/sec | Readable but slow |
| string-similarity (Dice) | JavaScript | 250K ops/sec | Different algorithm (faster) |

**Jaro-Winkler similarity (50-character strings):**

| Library | Performance | Memory | Notes |
|---------|-------------|--------|-------|
| rapidfuzz | 900K ops/sec | O(1) | C++ optimized |
| strsim | 800K ops/sec | O(1) | Rust native |
| textdistance (pure) | 60K ops/sec | O(1) | Python overhead |
| Apache Commons Text | 150K ops/sec | O(1) | JVM |

**Memory efficiency (1000-char strings, Levenshtein):**

| Library | Memory usage | Strategy |
|---------|-------------|----------|
| rapidfuzz | ~4KB | Single-row DP |
| textdistance | ~4MB | Full matrix (pure Python) |
| strsim | ~4KB | Optimized DP |
| Apache Commons Text | ~4KB + JVM overhead | Row reuse |

## API Ergonomics

### Type Safety

| Library | Type Hints | Null Safety | Compile-time Checks |
|---------|-----------|-------------|---------------------|
| rapidfuzz | ✅ Full | Runtime checks | Python 3.8+ |
| textdistance | ⚠️ Partial | Runtime checks | Limited |
| string-similarity | ❌ (use @types) | Runtime | TypeScript defs available |
| strsim | ✅ Full | Compile-time | Rust type system |
| Apache Commons Text | ✅ Generics | Compile-time | Java type system |

### Error Handling

**rapidfuzz:**
```
# Clear error messages
levenshtein(123, "abc")  # TypeError: expected str, not int
levenshtein("", "abc", score_cutoff=-1)  # ValueError: score_cutoff must be >= 0
```

**textdistance:**
```
# Some algorithms raise on invalid input
hamming("ab", "abc")  # ValueError: Lengths must be equal
jaccard("", "")       # Returns 0.0 (graceful handling)
```

**strsim:**
```
// Compile-time type safety
levenshtein("hello", "world")  // OK
levenshtein(123, "world")       // Compile error
```

### API Consistency

**rapidfuzz:** Consistent `(s1, s2, **kwargs)` signature across all scorers
**textdistance:** Consistent `.distance()`, `.similarity()`, `.normalized_*()` methods
**string-similarity:** Simple functions `compareTwoStrings()`, `findBestMatch()`
**strsim:** Rust-style functions: `levenshtein(&str, &str) -> usize`
**Apache Commons:** Java-style classes: `new LevenshteinDistance().apply(s1, s2)`

## Unicode Support

| Library | Normalization | Grapheme Clusters | Locale Awareness |
|---------|--------------|-------------------|------------------|
| rapidfuzz | NFD auto | ✅ Correct | No (user-preprocessed) |
| textdistance | None (user) | ⚠️ Code points | No |
| string-similarity | None | ⚠️ UTF-16 code units | No |
| strsim | None | ⚠️ Chars (not graphemes) | No |
| Apache Commons | None | ⚠️ Java chars | Locale via Collator |

**Best practice:** Pre-normalize with `unicodedata.normalize()` (Python) or equivalent

## Concurrency Support

| Library | Thread Safety | Parallel Processing | GIL Behavior |
|---------|--------------|---------------------|--------------|
| rapidfuzz | ✅ Thread-safe | ProcessPoolExecutor scales | Releases GIL |
| textdistance | ✅ Pure Python | GIL-bound | Holds GIL |
| string-similarity | ✅ Pure JS | Web Workers | N/A (single-threaded) |
| strsim | ✅ Thread-safe | rayon for parallelism | N/A (no GIL) |
| Apache Commons | ✅ Thread-safe | ExecutorService scales | N/A (JVM) |

## Integration Ecosystem

### Framework Support

| Library | Web Frameworks | ORMs | Data Processing |
|---------|---------------|------|-----------------|
| rapidfuzz | FastAPI, Flask, Django | SQLAlchemy, Django ORM | Pandas, Dask |
| textdistance | Flask, Django | Limited | Pandas |
| string-similarity | Express, React, Vue | - | Lodash chains |
| strsim | Actix, Axum (Rust) | Diesel | Polars |
| Apache Commons | Spring, Jakarta EE | Hibernate, JPA | Spark |

### Cloud Deployment

**rapidfuzz:**
- Pre-built wheels for Lambda, Cloud Run, ECS
- No compilation needed
- ~2MB binary footprint

**textdistance:**
- Pure Python: Minimal footprint
- C backends: Requires compilation layer (use docker with build tools)

**string-similarity:**
- Node.js: Deploy as npm package
- Serverless: Fast cold starts (<100ms)

**strsim:**
- Compile to static binary
- Tiny footprint (~500KB stripped)
- No runtime dependencies

**Apache Commons Text:**
- JVM required (~50-100MB base image)
- JAR size: ~200KB (+ dependencies)

## Extensibility

| Feature | rapidfuzz | textdistance | string-similarity | strsim | Apache Commons |
|---------|-----------|--------------|-------------------|--------|----------------|
| **Custom metrics** | C++ plugin | Python subclass | Fork/modify | Rust trait | Java interface |
| **Preprocessing hooks** | ✅ | ✅ | Manual | Manual | Manual |
| **Custom tokenizers** | ✅ | ✅ | Manual | Manual | Manual |
| **Batch optimization** | ✅ Built-in | Manual | Manual | Manual | Manual |

## Production Maturity

| Criterion | rapidfuzz | textdistance | string-similarity | strsim | Apache Commons |
|-----------|-----------|--------------|-------------------|--------|----------------|
| **Versioning** | SemVer | SemVer | SemVer | SemVer | SemVer |
| **Breaking changes** | Rare | Occasional | Rare | Rare | Very rare |
| **Backwards compat** | 1-2 years | Limited | Good | Rust editions | Years (Apache policy) |
| **Security patches** | Active | Moderate | Slow | Active | Active (Apache) |
| **CVE history** | None | None | None | None | Tracked by Apache |
| **Release cadence** | Monthly | Quarterly | Yearly | As needed | Monthly |

## Dependency Footprint

**Install size (including dependencies):**

| Library | Minimal Install | With Backends | Notes |
|---------|----------------|---------------|-------|
| rapidfuzz | 2.1MB (wheel) | 2.1MB | Self-contained C++ |
| textdistance | 80KB (pure) | +1.5MB (C backends) | Modular dependencies |
| string-similarity | 12KB | 12KB | Zero deps |
| strsim | 500KB (binary) | 500KB | Rust static binary |
| Apache Commons Text | 200KB (JAR) | +50MB (JVM) | Requires JVM |

## Decision Matrix

**Choose rapidfuzz if:**
- Production Python application
- Performance critical (>10K ops/sec)
- Need Levenshtein, Jaro-Winkler, token-based
- Multi-core parallelism important

**Choose textdistance if:**
- Research/prototyping phase
- Need rare metrics (compression, phonetic, Tversky)
- Exploring which algorithm works best
- Educational/learning context

**Choose string-similarity if:**
- Browser/frontend use case
- Dice coefficient fits your needs
- Minimal bundle size critical
- Zero-dependency requirement

**Choose strsim if:**
- Rust ecosystem
- CLI tools or systems programming
- Memory safety critical
- Predictable performance required

**Choose Apache Commons Text if:**
- Enterprise Java/Spring application
- Backwards compatibility critical
- Apache license required
- Existing Commons infrastructure
