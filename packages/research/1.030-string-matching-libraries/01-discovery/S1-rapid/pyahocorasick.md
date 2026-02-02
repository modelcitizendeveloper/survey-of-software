# pyahocorasick

**Repository:** github.com/WojciechMula/pyahocorasick
**GitHub Stars:** 1,100
**Forks:** 141
**Last Updated:** December 17, 2025 (v2.3.0)
**License:** BSD-3-Clause

## Quick Assessment

- **Popularity:** Moderate (1.1k stars)
- **Maintenance:** Active (recent December 2025 release)
- **Documentation:** Excellent (comprehensive docs at pyahocorasick.readthedocs.io)
- **Production Adoption:** Moderate-High (specialized multi-pattern matching)

## Pros

- **Multi-pattern search**: Find thousands of patterns in single pass
- **Linear time**: O(n + m) performance regardless of pattern count
- **Memory efficient**: Trie-based automaton structure
- **C implementation**: Fast execution (52% C, 38% Python)
- **BSD license**: Very permissive
- **Mature**: Well-tested algorithm implementation

## Cons

- **Specialized use case**: Overkill for single-pattern matching
- **Learning curve**: Automaton API more complex than simple string methods
- **Build requirements**: C compiler needed for installation
- **Limited flexibility**: Best for exact matching (approximate matching limited)

## Quick Take

pyahocorasick excels at finding multiple keywords simultaneously (e.g., detecting 10,000 banned words in user input). Outperforms naive loops or regex for multi-pattern scenarios. Worst-case and best-case performance are similar - predictable linear time. Use when you need to search for many patterns at once; overkill for simple string.find() use cases.

## Alternative

**ahocorasick_rs**: Rust implementation claims 1.5× to 7× faster than pyahocorasick.

## Data Sources

- [GitHub - WojciechMula/pyahocorasick](https://github.com/WojciechMula/pyahocorasick)
- [pyahocorasick Documentation](https://pyahocorasick.readthedocs.io/)
- [GitHub - G-Research/ahocorasick_rs](https://github.com/G-Research/ahocorasick_rs)
