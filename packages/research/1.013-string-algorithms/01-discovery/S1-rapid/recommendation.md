# S1: Rapid Discovery - Recommendations

## Quick-Win Libraries (Go-To Choices)

### Python
- **Regex**: `re` (stdlib) for basic needs, `regex` for advanced features
- **Fuzzy matching**: `thefuzz` + `python-Levenshtein` (de facto standard)
- **Multi-pattern**: `pyahocorasick` for content filtering

### JavaScript/TypeScript
- **Fuzzy search**: `fuse.js` (lightweight, client-friendly)
- **String similarity**: `string-similarity` (simple, effective)
- **Glob matching**: `minimatch` (npm's choice)

### Rust
- **Regex**: `regex` (safe, fast, production-ready)
- **Multi-pattern**: `aho-corasick` (ripgrep-proven performance)
- **Parsing**: `pest` (elegant PEG grammars)

### Go
- **Regex**: `regexp` (stdlib, safe by default)
- **String ops**: `strings` (stdlib, sufficient for most needs)
- **Fuzzy search**: `github.com/lithammer/fuzzysearch`

### Java/JVM
- **Utilities**: Apache Commons Text or Guava
- **Similarity**: `java-string-similarity` (comprehensive algorithms)
- **Parsing**: ANTLR (industry standard)

### C/C++
- **Regex**: RE2 (safety-first) or PCRE2 (feature-rich)
- **Unicode**: ICU (comprehensive i18n)
- **String formatting**: `fmt` (modern C++)

## Common Patterns

1. **Standard library first**: Most languages provide adequate string operations and regex in stdlib
2. **Specialize when needed**: Fuzzy matching, multi-pattern search, parsing require external libraries
3. **Safety matters**: Prefer DoS-resistant regex (RE2, Rust `regex`, Go `regexp`) for untrusted input
4. **Unicode is hard**: Use ICU or language-specific Unicode libraries for complex internationalization

## S1 Conclusion

The string algorithm landscape is mature and well-served by open-source libraries. Most common needs (regex, basic string ops, fuzzy matching) have clear "obvious choice" libraries with strong community support and proven production use.

**Next**: S2 will dive deeper into specialized use cases and performance characteristics.
