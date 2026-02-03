# Rust & Go Pattern Matching Libraries

## Rust Libraries

### memchr crate
- **Maturity**: 1.1K GitHub stars, widely used (148M downloads)
- **Performance**: 5-10 GB/s (SIMD-optimized single-byte search)
- **Algorithms**: SIMD-accelerated Boyer-Moore variant
- **Ease**: Simple API for byte search
- **Best for**: Single-byte/multi-byte search in byte slices
- **Production use**: Used by ripgrep, many parsing libraries

### aho-corasick crate
- **Maturity**: Same author as ripgrep, 1K+ stars
- **Performance**: 1-5 GB/s (optimized implementation)
- **Algorithms**: Aho-Corasick with DFA/NFA variants
- **Ease**: Clean Rust API
- **Best for**: Multi-pattern matching in Rust
- **Production use**: ripgrep, tokenizers, log parsers

### regex crate
- **Maturity**: 3.5K GitHub stars, de facto standard
- **Performance**: 1-2 GB/s (DFA-based, linear time guarantee)
- **Algorithms**: Thompson NFA + DFA + bounded backtracking hybrid
- **Ease**: Ergonomic Rust API
- **Best for**: Regex in Rust (no catastrophic backtracking)
- **Production use**: ripgrep, Rust stdlib uses it

### bstr crate
- **Maturity**: 228 stars, byte string utilities
- **Performance**: Varies by algorithm (provides multiple)
- **Algorithms**: Two-Way, Rabin-Karp, naive
- **Ease**: Simple API, byte-oriented
- **Best for**: Working with byte strings (not UTF-8)

### twoway crate
- **Maturity**: 97 stars
- **Performance**: 2-4 GB/s
- **Algorithms**: Two-Way algorithm (Crochemore-Perrin)
- **Ease**: Simple API
- **Best for**: Alternative to Boyer-Moore with consistent performance

## Go Libraries

### strings.Index() (stdlib)
- **Maturity**: Go standard library
- **Performance**: ~500 MB/s to 2 GB/s
- **Algorithms**: Rabin-Karp for short strings, optimized for SSE4.2
- **Ease**: Trivial (one function call)
- **Best for**: Single-pattern search in Go

### regexp package (stdlib)
- **Maturity**: Go standard library
- **Performance**: ~100-500 MB/s
- **Algorithms**: RE2-based (linear time guarantees)
- **Ease**: Simple API, familiar syntax
- **Best for**: Regex in Go (safe, no catastrophic backtracking)

### aho-corasick-go
- **Maturity**: ~500 stars (multiple implementations)
- **Performance**: ~500 MB/s to 2 GB/s
- **Algorithms**: Aho-Corasick
- **Ease**: Simple API
- **Best for**: Multi-pattern matching in Go
- **Note**: Multiple packages available, varying quality

### cloudflare/ahocorasick
- **Maturity**: Cloudflare-maintained, 340 stars
- **Performance**: ~1-3 GB/s (optimized)
- **Algorithms**: Aho-Corasick with optimizations
- **Ease**: Clean API
- **Best for**: Production multi-pattern matching in Go
- **Production use**: Cloudflare infrastructure

### bmh (Boyer-Moore-Horspool)
- **Maturity**: ~50 stars, academic implementations
- **Performance**: ~1-2 GB/s
- **Algorithms**: Boyer-Moore-Horspool
- **Ease**: Simple
- **Best for**: Single-pattern matching when strings.Index() isn't enough
