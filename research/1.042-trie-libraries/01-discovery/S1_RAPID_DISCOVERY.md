# S1: Rapid Discovery - Trie Libraries Ecosystem

**Experiment**: 1.042 - Trie Libraries (Prefix Trees, Suffix Trees, Radix Trees)
**Stage**: S1 - Rapid Discovery (Ecosystem Landscape)
**Date**: 2025-10-10
**Methodology**: MPSE Stage 1 - Quick ecosystem scan, no application-specific analysis

---

## What Are Tries?

**Trie** (from "retrieval") is a tree-based data structure optimized for **prefix-based operations** on strings. Unlike hash tables or binary search trees, tries exploit the hierarchical structure of strings to enable:

- **Prefix search**: Find all strings starting with "cat"
- **Autocomplete**: Suggest completions as user types
- **Longest prefix matching**: Route `/api/users/123` to handler
- **String deduplication**: Share common prefixes in memory
- **Dictionary operations**: Spell checking, word validation

### Trie Variants

1. **Standard Trie**: One node per character, simple but space-intensive
2. **Compressed Trie (Patricia)**: Merge single-child chains into edges
3. **Radix Tree**: Generalization of Patricia, arbitrary radix
4. **Suffix Tree**: All suffixes of a string, powerful for pattern matching
5. **Ternary Search Tree**: Binary tree hybrid, balances space and speed

---

## Python Trie Library Ecosystem

### 🏆 **Tier 1: Production-Grade Libraries**

#### **1. `pygtrie` (Google)**
- **PyPI**: `pygtrie` (3.5k+ stars on GitHub)
- **Maturity**: Google open source, actively maintained since 2014
- **Variants**: CharTrie, StringTrie, PrefixSet
- **Use Cases**: Autocomplete, IP routing, prefix search
- **Strengths**: Pure Python, clean API, well-tested
- **Weaknesses**: Pure Python performance limits

```python
from pygtrie import CharTrie
trie = CharTrie()
trie['cat'] = 1
trie['cats'] = 2
trie['dog'] = 3
trie.has_key('cat')  # True
list(trie.items(prefix='cat'))  # [('cat', 1), ('cats', 2)]
```

#### **2. `datrie` (LibDATRIE bindings)**
- **PyPI**: `datrie` (500+ stars)
- **Maturity**: Wraps C library (libdatrie), stable since 2012
- **Algorithm**: Double-Array Trie (memory-efficient)
- **Use Cases**: Large dictionaries, NLP, spell checking
- **Strengths**: Fast lookups (C speed), memory efficient
- **Weaknesses**: Requires alphabet declaration, immutable after creation

```python
import datrie
trie = datrie.Trie('abcdefghijklmnopqrstuvwxyz')
trie['cat'] = 1
trie['cats'] = 2
trie.keys(prefix='cat')  # ['cat', 'cats']
```

#### **3. `marisa-trie`**
- **PyPI**: `marisa-trie` (1k+ stars)
- **Maturity**: Wraps C++ MARISA library, stable
- **Algorithm**: Memory-efficient MARISA trie (succinct data structure)
- **Use Cases**: Static dictionaries, text mining, large-scale NLP
- **Strengths**: Extremely memory efficient, supports record trie
- **Weaknesses**: Immutable (build once, query many), C++ dependency

```python
import marisa_trie
trie = marisa_trie.Trie(['cat', 'cats', 'dog'])
'cat' in trie  # True
trie.prefixes('catastrophe')  # ['cat']
```

#### **4. `hat-trie` (C++ bindings)**
- **PyPI**: `hat-trie` (200+ stars)
- **Maturity**: Wraps tessil/hat-trie C++ library
- **Algorithm**: HAT-trie (hybrid array/trie)
- **Use Cases**: Dynamic dictionaries, high-performance routing
- **Strengths**: Fast mutations, cache-friendly
- **Weaknesses**: Less mature Python bindings

---

### 🔧 **Tier 2: Specialized/Academic Libraries**

#### **5. `ahocorasick` (Aho-Corasick Algorithm)**
- **PyPI**: `pyahocorasick` (900+ stars)
- **Purpose**: Multi-pattern string search (not pure trie)
- **Use Cases**: Log parsing, intrusion detection, text search
- **Strengths**: Searches multiple patterns simultaneously

#### **6. `pytrie`**
- **PyPI**: `pytrie` (older, less maintained)
- **Status**: Pure Python, educational quality
- **Use Cases**: Learning, small datasets
- **Weaknesses**: Performance, limited features

#### **7. `Radix` (from `radix` package)**
- **PyPI**: `radix` (networking-focused)
- **Purpose**: IP address prefix matching
- **Use Cases**: BGP routing tables, IP lookups
- **Strengths**: Optimized for CIDR notation

---

### 🛠️ **DIY Solutions**

#### **8. Redis with Sorted Sets (for routing)**
- **Approach**: Store paths as sorted set members, use `ZRANGEBYLEX`
- **Use Cases**: HTTP routing, dynamic path matching
- **Strengths**: Distributed, real-time updates
- **Weaknesses**: Not a true trie, network overhead

#### **9. Custom Python Trie**
- **Approach**: Dict-of-dicts structure
- **Use Cases**: Learning, application-specific optimizations
- **Example**:

```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False
        self.value = None
```

---

## Language Ecosystem Comparison

### **Python vs Other Languages**

| Language | Notable Libraries | Strengths |
|----------|-------------------|-----------|
| **Python** | pygtrie, datrie, marisa-trie | Good bindings, pure Python options |
| **JavaScript** | trie-search, mnemonist | Browser + Node.js, lightweight |
| **Go** | go-radix, iradix | Built-in, high concurrency |
| **Rust** | radix_trie, qp-trie | Zero-cost abstractions, safety |
| **C/C++** | libdatrie, MARISA, HAT-trie | Maximum performance |
| **Java** | Apache Commons Collections | Enterprise tooling |

---

## Quick Selection Guide

### **Choose `pygtrie` if:**
- Pure Python preferred (no C dependencies)
- Need simple, readable code
- Moderate dataset sizes (<100k keys)
- Mutable trie required

### **Choose `datrie` if:**
- Large dictionaries (100k-10M keys)
- Fast lookups critical
- Static or semi-static data
- Known alphabet (Latin, Thai, etc.)

### **Choose `marisa-trie` if:**
- Extreme memory constraints
- Static dictionary (build once, query many)
- Need compressed storage
- Multi-value associations (RecordTrie)

### **Choose `hat-trie` if:**
- High mutation frequency
- Cache performance matters
- Dynamic routing tables

### **Choose Redis/Custom if:**
- Distributed system requirements
- Real-time path updates
- Integration with existing Redis infrastructure

---

## Performance Intuitions (Rough Order of Magnitude)

**Lookup Speed** (million ops/sec):
- C-based tries (`datrie`, `marisa-trie`, `hat-trie`): **1-5M ops/sec**
- Pure Python (`pygtrie`): **100k-500k ops/sec**
- Dict-based custom: **50k-200k ops/sec**

**Memory Efficiency** (bytes per key):
- `marisa-trie`: **5-15 bytes/key** (succinct)
- `datrie`: **20-50 bytes/key** (double-array)
- `pygtrie`: **100-300 bytes/key** (Python objects)
- Python dict: **200-500 bytes/key** (hash table)

---

## Common Use Case Patterns

### **1. Autocomplete / Type-ahead**
- **Best**: `pygtrie` (simple), `datrie` (fast)
- **Pattern**: Prefix search with ranking

### **2. HTTP Routing**
- **Best**: `pygtrie`, custom radix tree
- **Pattern**: Longest prefix match with wildcards

### **3. IP Routing Tables**
- **Best**: `radix` (specialized), `pygtrie`
- **Pattern**: CIDR prefix matching

### **4. Spell Checking**
- **Best**: `datrie`, `marisa-trie`
- **Pattern**: Large static dictionary

### **5. Text Compression**
- **Best**: Suffix trees (`suffix-tree` library)
- **Pattern**: Repeated substring detection

### **6. String Deduplication**
- **Best**: `marisa-trie` (memory), `datrie`
- **Pattern**: Shared prefix compression

---

## Ecosystem Maturity Assessment

### **Strengths**
✅ Multiple mature C-binding options (`datrie`, `marisa-trie`)
✅ Pure Python alternative exists (`pygtrie`)
✅ Specialized variants for specific use cases
✅ Active maintenance in top libraries

### **Gaps**
❌ No dominant "obvious choice" (fragmented ecosystem)
❌ Limited native Python performance
❌ Suffix tree support underdeveloped
❌ Ternary search trees not well represented

### **Trends**
📈 Growing interest in routing/autocomplete use cases
📈 Memory efficiency increasingly valued (succinct structures)
📉 Pure Python tries declining (C bindings preferred)

---

## Red Flags & Considerations

### **Alphabet Constraints** (`datrie`)
- Must declare character set upfront
- Non-Latin scripts need special handling
- Binary data requires workarounds

### **Immutability** (`marisa-trie`)
- Cannot modify after build
- Rebuild required for updates
- Not suitable for dynamic data

### **C Dependencies**
- Build complexity on some platforms
- Binary wheel availability varies
- Debugging more difficult

### **Memory Patterns**
- Tries can be memory-intensive for sparse datasets
- Python object overhead compounds the issue
- Consider hash tables for random access patterns

---

## Next Steps for Deep Dive (S2)

1. **Benchmark suite**: Compare lookup, insert, memory across libraries
2. **API ergonomics**: Evaluate developer experience
3. **Edge cases**: Unicode, binary data, massive datasets
4. **Mutation patterns**: Dynamic vs static workloads
5. **Integration patterns**: Redis, SQLite, file-backed tries
6. **Algorithmic trade-offs**: Space vs time, immutability costs

---

## Research Questions

1. When does trie overhead beat hash table simplicity?
2. How do compressed tries (MARISA, HAT) affect performance?
3. Can Redis sorted sets match native trie performance?
4. What's the crossover point for pure Python vs C bindings?
5. How do tries perform with non-ASCII Unicode data?

---

**Status**: ✅ S1 Complete - Ecosystem landscape mapped
**Next Stage**: S2 Comprehensive Discovery (technical deep-dive)
**Confidence**: High - mature ecosystem with clear trade-offs
