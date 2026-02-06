# google-re2 (pyre2)

**Repository:** github.com/google/re2 (C++ library)
**Python Wrappers:** github.com/facebook/pyre2, github.com/axiak/pyre2
**License:** BSD-3-Clause

## Quick Assessment

- **Popularity:** Moderate (specialized use case)
- **Maintenance:** Active (Google maintains RE2 core)
- **Documentation:** Good (RE2 docs, wrapper docs)
- **Production Adoption:** High (Google, Facebook usage)

## Pros

- **Linear time guarantee**: No catastrophic backtracking
- **Predictable performance**: Worst-case = best-case asymptotically
- **Thread-safe**: Can be used from multiple threads
- **Security**: Safe against regex DoS attacks
- **Google pedigree**: Proven at massive scale

## Cons

- **Limited features**: No backreferences, lookahead/lookbehind
- **Multiple wrappers**: Several competing Python bindings (confusing)
- **Sometimes slower**: For simple patterns, re module can be faster
- **UTF-8 focused**: Best performance with UTF-8 encoded bytes
- **Setup complexity**: C++ dependency, build requirements

## Quick Take

RE2 trades regex power for guaranteed linear-time performance. Use when processing untrusted user input (prevents regex DoS) or when you need predictable performance at scale. Not suitable if you need advanced regex features (backreferences, lookahead). Python's re module is fine for most use cases; switch to RE2 when security or performance guarantees matter more than features.

## Data Sources

- [GitHub - google/re2](https://github.com/google/re2)
- [GitHub - facebook/pyre2](https://github.com/facebook/pyre2/)
- [pyre2 Documentation](https://sarnold.github.io/pyre2/README.html)
