# Java/JVM String Algorithm Libraries

## Built-in: `java.util.regex` and `String`
- **Standard library**: JDK
- **Capabilities**: Regex via `Pattern`/`Matcher`, basic string operations
- **Performance**: JIT-compiled, mature implementations
- **Unicode**: Full Unicode support in modern JDK versions

## Apache Commons Lang - `StringUtils`
- **Maven**: `org.apache.commons:commons-lang3`
- **Purpose**: Enhanced string utilities
- **Features**: isEmpty, isBlank, abbreviate, difference, fuzzy matching
- **Use case**: Common string operations, null-safe handling

## Apache Commons Text
- **Maven**: `org.apache.commons:commons-text`
- **Purpose**: Advanced text processing
- **Features**: String similarity (Levenshtein, Jaro-Winkler), diff, escaping
- **Use case**: Text analysis, similarity computation, safe string handling

## Google Guava - `Strings`, `Splitter`
- **Maven**: `com.google.guava:guava`
- **Purpose**: Core utilities including string processing
- **Features**: Splitter, Joiner, CharMatcher, string utilities
- **Use case**: Idiomatic string manipulation, parsing

## `java-string-similarity` (tdebatty)
- **Maven**: `info.debatty:java-string-similarity`
- **Purpose**: String distance and similarity algorithms
- **Algorithms**: 15+ algorithms (Levenshtein, Jaro-Winkler, Cosine, N-Gram)
- **Use case**: Fuzzy matching, deduplication, clustering

## ANTLR - Parser Generator
- **Maven**: `org.antlr:antlr4-runtime`
- **Purpose**: Parser and lexer generation
- **Features**: Generates parsers from grammar files, tree walkers
- **Use case**: Building compilers, DSL parsers, structured text processing

## Aho-Corasick (hankcs)
- **Maven**: `com.hankcs:aho-corasick-double-array-trie`
- **Purpose**: Multi-pattern string matching
- **Algorithm**: Aho-Corasick with double-array trie
- **Performance**: Optimized for memory efficiency
- **Use case**: Dictionary-based tagging, content filtering

## ICU4J - Unicode & Internationalization
- **Maven**: `com.ibm.icu:icu4j`
- **Purpose**: Comprehensive Unicode and i18n support
- **Features**: Collation, normalization, transliteration, boundary analysis
- **Use case**: Complex Unicode handling, internationalization
