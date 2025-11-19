# S1 Rapid Discovery: Full-Text Search Libraries

**Goal**: Quick install, test, and benchmark top Python full-text search libraries

---

## How to Run Tests

All tests use **uv** for Python package management.

### Prerequisites

```bash
# Ensure you're in the research directory
cd /home/ivanadamin/spawn-solutions/research/1.003-full-text-search
```

### Test 1: Whoosh (Pure Python)

```bash
# Install
uv pip install whoosh

# Run test
uv run python 01-discovery/S1-rapid/01-whoosh-test.py
```

**What it tests:**
- Index 10,000 documents
- Keyword search performance
- Fuzzy search (typo correction)
- Phrase search
- Sorting by fields
- BM25 ranking

**Expected output:**
- Indexing speed: ~5,000-10,000 docs/second
- Query latency: <50ms
- Pure Python, no dependencies

---

### Test 2: Tantivy (Rust Bindings)

```bash
# Install (requires Rust toolchain)
uv pip install tantivy

# Run test
uv run python 01-discovery/S1-rapid/02-tantivy-test.py
```

**What it tests:**
- Index 10,000 documents
- Keyword search performance
- Phrase search
- Multi-field search
- BM25 ranking (default)

**Expected output:**
- Indexing speed: ~50,000+ docs/second (10× faster than Whoosh)
- Query latency: <10ms
- Rust backend, high performance

**Note**: If `pip install tantivy` fails with "Rust compiler not found":
```bash
# Install Rust toolchain (one-time setup)
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source $HOME/.cargo/env

# Then retry
uv pip install tantivy
```

---

### Test 3: Quick Comparison (Optional)

Run both tests and compare:

```bash
# Whoosh
time uv run python 01-discovery/S1-rapid/01-whoosh-test.py

# Tantivy
time uv run python 01-discovery/S1-rapid/02-tantivy-test.py
```

---

## What S1 Tests Measure

### 1. Indexing Performance
- **Metric**: Documents indexed per second
- **Target**: >10,000 docs/sec for interactive use
- **Why**: Determines if you can build index in reasonable time

### 2. Query Latency
- **Metric**: Milliseconds to return top 10 results
- **Target**: <50ms for good UX
- **Why**: User-facing search must feel instant

### 3. Features
- **Fuzzy search**: Typo tolerance ("Pythn" → "Python")
- **Phrase search**: Exact phrase matching
- **BM25 ranking**: Industry-standard relevance algorithm
- **Sorting**: Order by custom fields (views, date, etc.)

### 4. Developer Experience
- **Installation**: How easy to install? (pip install vs compilation)
- **API**: How many lines of code to get started?
- **Documentation**: Are there clear examples?

---

## Expected Results (Preview)

Based on typical benchmarks:

| Library | Indexing (docs/sec) | Query (ms) | Installation | Best For |
|---------|---------------------|------------|--------------|----------|
| **Whoosh** | 5,000-10,000 | 20-50ms | ✅ Easy (pure Python) | Small datasets, Python-only |
| **Tantivy** | 50,000-100,000 | 2-10ms | ⚠️ Requires Rust | Performance-critical |

---

## Next Steps After S1

Once you've run the tests:

1. **Review results** in terminal output
2. **Document findings** in `S1_RESULTS.md`
3. **Choose top 2** libraries for S2 deep-dive
4. **Proceed to S2** comprehensive benchmarks (100K, 1M documents)

---

## Troubleshooting

### Whoosh installation fails
```bash
# Should not happen (pure Python), but try:
uv pip install --upgrade whoosh
```

### Tantivy installation fails (no Rust)
```bash
# Install Rust (one-time)
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source $HOME/.cargo/env

# Verify Rust installed
rustc --version

# Retry Tantivy
uv pip install tantivy
```

### Tantivy installation fails (other errors)
```bash
# Try pre-built wheel (if available for your platform)
uv pip install tantivy --only-binary tantivy

# Or skip Tantivy for now, focus on Whoosh
```

---

## Time Estimate

- **Setup**: 5-10 minutes (install libraries)
- **Running tests**: 2-3 minutes each
- **Analysis**: 10-15 minutes (review output, document findings)
- **Total S1**: ~30 minutes hands-on time

---

**Status**: Ready to run
**Next**: Execute tests, document results in `S1_RESULTS.md`
