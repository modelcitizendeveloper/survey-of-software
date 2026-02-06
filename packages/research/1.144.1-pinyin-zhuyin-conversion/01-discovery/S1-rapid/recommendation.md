# S1-Rapid Recommendation

## Summary of Findings

| Library | Pinyin | Zhuyin | Standout Feature | Maintenance |
|---------|--------|--------|------------------|-------------|
| **pypinyin** | ✅ | ✅ | Context-aware heteronym handling | Active (v0.55.0) |
| **dragonmapper** | ✅ | ✅ | Bidirectional transcription conversion | Stable (v0.2.6) |
| **xpinyin** | ✅ | ❌ | Simple API, Pinyin-only | Active (v0.7.7) |

## Key Discovery: "python-pinyin" Clarification
The bead specification lists "python-pinyin" as a separate library, but this is actually the **same library as pypinyin**. The repository is named "python-pinyin," but the package is installed and imported as "pypinyin." There is a different library called "pinyin" (without "py"), but it's not relevant to this research scope.

## Libraries for S2-Comprehensive

### RECOMMENDED: pypinyin
**Rationale**: Most feature-rich, active maintenance, sophisticated heteronym handling, native Zhuyin support.

**Proceed to S2**: ✅

### RECOMMENDED: dragonmapper
**Rationale**: Unique transcription conversion capabilities (Pinyin ↔ Zhuyin), text identification features, bidirectional support.

**Proceed to S2**: ✅

### NOT RECOMMENDED: xpinyin
**Rationale**: Lacks Zhuyin support entirely. While it has a clean API and good Pinyin capabilities, it doesn't meet the core requirement of Zhuyin conversion.

**Proceed to S2**: ❌

## Initial Positioning

### pypinyin: "The Comprehensive Converter"
Best for applications that need rich formatting options, context-aware pronunciation, and multiple output styles including Zhuyin.

### dragonmapper: "The Transcription Swiss Army Knife"
Best for applications that need to work with multiple transcription systems, convert between them, or identify which system is in use.

## Open Questions for S2
1. How do pypinyin and dragonmapper compare on accuracy for polyphone/heteronym characters?
2. What are the performance characteristics of each library?
3. Does dragonmapper's Zhuyin support include tone marks?
4. How up-to-date are the pronunciation databases in each library?
5. What are the dependencies for each library?
6. Can they handle Traditional vs. Simplified Chinese differently?

## S2-Comprehensive Focus Areas
- API deep dive with code examples
- Feature comparison matrix
- Performance benchmarking
- Accuracy testing on edge cases (polyphones, rare characters)
- Dependency analysis
- Community health and maintenance trends
