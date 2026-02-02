# strsim (Rust)

**GitHub:** ~530 stars | **Ecosystem:** crates.io | **License:** MIT

## Positioning

Rust implementation of common string similarity metrics. Standard choice for Rust projects needing fuzzy matching with compile-time safety guarantees.

## Key Metrics

- **Performance:** Native Rust speed (comparable to C++)
- **Download stats:** ~6M downloads (crates.io all-time)
- **Maintenance:** Active, regular releases
- **Rust versions:** 1.56+ supported
- **Dependencies:** Zero external dependencies

## Algorithms Included

- Hamming distance
- Levenshtein distance
- Optimal String Alignment (OSA)
- Damerau-Levenshtein
- Jaro and Jaro-Winkler
- Sørensen-Dice coefficient
- Cosine similarity (needs additional ngram processing)

## Community Signals

**Reddit r/rust sentiment:**
- "strsim is the go-to for string metrics in Rust"
- "Use strsim for fuzzy matching, regex for exact patterns"
- "Performance on par with C++, easier to integrate than FFI"

**Common use cases:**
- CLI tools with typo-tolerant commands
- Log analysis and anomaly detection
- Fuzzy search in Rust-based databases
- Name matching in data pipelines

## Trade-offs

**Strengths:**
- Zero-cost abstractions (no runtime overhead)
- Memory safe (no buffer overflows)
- Compile-time guarantees
- Zero dependencies (easy to audit)
- Works in no_std environments (embedded systems)

**Limitations:**
- Rust-only ecosystem
- Smaller algorithm selection vs Python libraries (no phonetic, compression-based)
- No GUI-friendly bindings (command-line focused)

## Decision Context

**Choose strsim when:**
- Building Rust applications or CLI tools
- Memory safety is critical
- Need predictable performance (no GC pauses)
- Embedded or systems programming context

**Skip if:**
- Python/JavaScript ecosystem (use language-native libraries)
- Need 40+ algorithms (use textdistance)
- Rapid prototyping (Rust has steeper learning curve)
- GUI applications (consider language with richer UI bindings)
