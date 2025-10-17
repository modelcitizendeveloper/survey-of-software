# S1 RAPID DISCOVERY: Python Advanced Collections Libraries

## Executive Summary

For developers needing immediate decisions on Python collections libraries in 2025, here are the **top 5 libraries** with clear use-case guidance:

1. **sortedcontainers** - Use for sorted collections (replaces bintrees)
2. **polars** - Use for large-scale data processing (outperforms pandas)
3. **pyrsistent** - Use for immutable/functional programming
4. **cytoolz** - Use for functional programming utilities (2-5x faster than toolz)
5. **more-itertools** - Use for extended iteration patterns (129M+ monthly downloads)

## Top 5 Advanced Collections Libraries

### 1. SortedContainers ⭐ **FASTEST SORTED COLLECTIONS**
- **Performance**: Outperforms C-extensions while being pure Python
- **Speed**: ~10x faster than bintrees for 100K insertions (332ms vs 3746ms)
- **Memory**: O(log n) operations, scales to billions of items
- **API**: Drop-in replacement for built-in list/set with sorted guarantees
- **Status**: Active maintenance, Apache2 licensed
- **Use when**: You need sorted collections with fast insertion/lookup

```python
from sortedcontainers import SortedList, SortedDict, SortedSet
```

### 2. Polars ⭐ **DATAFRAME REVOLUTION**
- **Performance**: 5-100x faster than pandas for common operations
- **Architecture**: Rust-based, multi-threaded, columnar processing
- **Memory**: Superior memory efficiency with lazy evaluation
- **API**: SQL-like syntax + pandas compatibility layer
- **Status**: Rapidly growing ecosystem, active development
- **Use when**: Working with datasets >10GB or need speed/memory efficiency

```python
import polars as pl  # The future of dataframes
```

### 3. Pyrsistent ⭐ **IMMUTABLE COLLECTIONS**
- **Performance**: O(log n) operations, C-extension available (2-20x speedup)
- **Types**: PVector, PMap, PSet, PRecord, PClass, PBag, PDeque
- **Memory**: Structural sharing for efficiency
- **API**: Immutable versions of list/dict/set with persistence
- **Status**: Actively maintained, PEP 561 type hints
- **Use when**: Functional programming or need immutable data structures

```python
from pyrsistent import pvector, pmap, pset
```

### 4. CyToolz ⭐ **FUNCTIONAL UTILITIES**
- **Performance**: 2-5x faster than pure Python toolz
- **Modules**: itertoolz, functoolz, dicttoolz for functional programming
- **Memory**: Iterator-based, low memory usage
- **API**: Functional programming primitives (curry, memoize, pipe)
- **Status**: Cython-based, Python 3.8+, active maintenance
- **Use when**: Building functional data pipelines or need performance-critical utils

```python
import cytoolz as toolz  # Always use cytoolz over toolz
```

### 5. More-Itertools ⭐ **ITERATION POWERHOUSE**
- **Performance**: Vectorized operations, memory-efficient processing
- **Downloads**: 129M+ monthly (most popular extension library)
- **Features**: 300+ recipes for advanced iteration patterns
- **API**: Extends itertools with practical utilities
- **Status**: Very active development, excellent maintenance
- **Use when**: Need advanced iteration patterns beyond stdlib itertools

```python
import more_itertools as mit
```

## Quick Decision Framework

### Performance vs Memory Trade-offs

| Library | Speed | Memory | Use Case |
|---------|-------|--------|----------|
| sortedcontainers | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | Sorted collections |
| polars | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Large datasets |
| pyrsistent | ⭐⭐⭐ | ⭐⭐⭐⭐ | Immutable data |
| cytoolz | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Functional programming |
| more-itertools | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Iterator extensions |

### When to Use Specialized Collections vs Built-ins

**Use Built-ins (dict/list/set) when:**
- Dataset < 100K items
- Simple CRUD operations
- Mutable data preferred
- Maximum compatibility needed

**Use Specialized Collections when:**
- Need sorted access patterns → **sortedcontainers**
- Processing large datasets → **polars**
- Immutability required → **pyrsistent**
- Functional programming style → **cytoolz**
- Advanced iteration patterns → **more-itertools**

## Key 2025 Insights

### Deprecated Libraries
- **bintrees**: Officially deprecated since 2017, use sortedcontainers instead
- **toolz**: Still maintained but cytoolz is 2-5x faster

### Performance Winners
1. **sortedcontainers** beat all tree-based implementations
2. **polars** emerged as pandas successor for large data
3. **cytoolz** provides significant speedup over pure Python

### Ecosystem Maturity
- sortedcontainers: Mature, stable, widely adopted
- polars: Rapidly growing, excellent pandas migration path
- pyrsistent: Stable, excellent type hints support
- cytoolz: Mature Cython implementation
- more-itertools: Most downloaded extension library

## Immediate Recommendations

### For New Projects
1. **Data Processing**: Start with polars for any dataset >1GB
2. **Sorted Collections**: Use sortedcontainers, forget bintrees
3. **Functional Programming**: Use cytoolz, not pure toolz
4. **Immutable Data**: Use pyrsistent for functional style
5. **Iterator Extensions**: Use more-itertools for advanced patterns

### Migration Priorities
1. **bintrees → sortedcontainers**: Immediate (10x performance gain)
2. **pandas → polars**: For large datasets (5-100x speedup)
3. **toolz → cytoolz**: Simple import change (2-5x speedup)

### Pure Python vs C Extensions
- **sortedcontainers**: Pure Python that beats C extensions
- **polars**: Rust-based, maximum performance
- **pyrsistent**: C extension optional but recommended
- **cytoolz**: Cython compilation required
- **more-itertools**: Pure Python, excellent optimization

## Bottom Line for Developers

**Use these libraries RIGHT NOW because:**

1. **sortedcontainers** - It's faster than C extensions while being pure Python
2. **polars** - Pandas is too slow for modern data volumes
3. **pyrsistent** - Immutability prevents entire classes of bugs
4. **cytoolz** - Functional programming shouldn't be slow
5. **more-itertools** - 129M downloads/month means battle-tested reliability

**Avoid these patterns:**
- Using bintrees (use sortedcontainers)
- Using toolz instead of cytoolz
- Using pandas for large datasets (use polars)
- Rolling your own sorted collections
- Using pure Python when Cython/Rust alternatives exist

---

**Date compiled**: 2025-09-28