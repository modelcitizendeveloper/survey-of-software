# Java & JVM Pattern Matching Libraries

## Java Standard Library

### String.indexOf()
- **Maturity**: Java standard library (universal)
- **Performance**: ~500 MB/s to 2 GB/s (JIT-optimized)
- **Algorithms**: Boyer-Moore variant in HotSpot JVM
- **Ease**: Trivial (one method call)
- **Best for**: Single-pattern search in Java

### Pattern/Matcher (java.util.regex)
- **Maturity**: Java standard library
- **Performance**: ~100-500 MB/s
- **Algorithms**: Backtracking NFA for regex
- **Ease**: Verbose API but standard
- **Best for**: Regex patterns in Java
- **Warning**: Can have catastrophic backtracking

## Aho-Corasick Implementations

### aho-corasick (robert-bor)
- **Maturity**: 1.1K GitHub stars, widely used
- **Performance**: ~500 MB/s to 1.5 GB/s
- **Algorithms**: Aho-Corasick automaton
- **Ease**: Clean Java API
- **Best for**: Multi-pattern matching in Java
- **Production use**: Text analysis, security tools

### text-processing (Apache Commons)
- **Maturity**: Apache Commons library
- **Performance**: Moderate
- **Algorithms**: Various (including Aho-Corasick)
- **Ease**: Apache Commons style API
- **Best for**: Java projects already using Commons

## AC-Library (ahocorasick-java)

- **Maturity**: ~600 stars
- **Performance**: ~1-2 GB/s
- **Algorithms**: Aho-Corasick with optimizations
- **Ease**: Simple builder pattern API
- **Best for**: Performance-critical multi-pattern matching

## Kotlin/Scala

### Kotlin String methods
- **Maturity**: Kotlin stdlib (JVM-based)
- **Performance**: Same as Java (JVM-optimized)
- **Algorithms**: Same as Java String.indexOf()
- **Ease**: More concise syntax than Java
- **Best for**: Kotlin projects

### Scala collections
- **Maturity**: Scala stdlib
- **Performance**: Comparable to Java
- **Algorithms**: Uses Java implementations underneath
- **Ease**: Functional API
- **Best for**: Scala projects with functional style
