# Apache Commons Text (Java)

**GitHub:** ~400 stars (apache/commons-text) | **Ecosystem:** Maven | **License:** Apache 2.0

## Positioning

Enterprise Java library for text algorithms including string similarity metrics. Part of Apache Commons family with strong backwards compatibility guarantees.

## Key Metrics

- **Maturity:** Successor to Apache Commons Lang's string utilities
- **Download stats:** ~100M downloads/month (Maven Central, Jan 2025)
- **Maintenance:** Active Apache project with monthly releases
- **Java versions:** Java 8+ required
- **Enterprise adoption:** Used by Fortune 500 Java shops

## Algorithms Included

**Similarity metrics:**
- Levenshtein distance (with threshold optimization)
- Jaro-Winkler similarity
- Cosine similarity
- Hamming distance
- Longest Common Subsequence (LCS)

**Utility classes:**
- `LevenshteinDistance` - configurable threshold for early termination
- `JaroWinklerSimilarity` - normalized scores (0-1)
- `CosineSimilarity` - vector-based text similarity
- `SimilarityScore` interface - common API for all metrics

## Community Signals

**Stack Overflow sentiment:**
- "Use Apache Commons for enterprise Java - well-tested and stable"
- "Spring Boot projects: Commons Text over rolling your own"
- "Thread-safe and battle-tested in production for years"

**Common use cases:**
- Data deduplication in Spring Boot applications
- Fuzzy search in enterprise CRM/ERP systems
- Name matching in banking and healthcare (high-reliability domains)
- Log analysis in Java microservices

## Trade-offs

**Strengths:**
- Enterprise-grade stability and testing
- Backwards compatibility guarantees
- Thread-safe implementations
- Apache license (enterprise-friendly)
- Integrates seamlessly with Spring ecosystem
- Extensive Javadocs and examples

**Limitations:**
- Slower than specialized JNI-based implementations
- Limited algorithm selection vs Python equivalents
- Heavier dependency (pulls in entire commons-text JAR)
- Java-only (no native cross-language bindings)

## Decision Context

**Choose Apache Commons Text when:**
- Building enterprise Java applications
- Spring Boot or Jakarta EE ecosystem
- Stability and support matter more than raw speed
- Backwards compatibility is critical
- Compliance requires Apache-licensed dependencies

**Skip if:**
- Kotlin-first projects (use kotlin-string-similarity)
- Need maximum performance (consider JNI wrappers to C++)
- Microservices with tight size constraints (use leaner alternatives)
- Non-JVM ecosystems (Python, JavaScript, Rust)
