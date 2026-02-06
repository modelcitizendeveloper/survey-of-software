# BTrees - ZODB's B-tree Implementation

## Overview

BTrees is a production-grade B-tree implementation from the ZODB (Zope Object Database) project. Unlike traditional binary search trees, B-trees are multi-way trees optimized for systems that read and write large blocks of data (databases, filesystems).

**Key characteristics**:
- C implementation with Python bindings (fast)
- Designed for persistent storage (ZODB)
- Thread-safe with MVCC (Multi-Version Concurrency Control)
- Multiple key/value type specializations
- Active maintenance (part of ZODB ecosystem)

## Algorithm Description

**B-tree structure** (general, not specific to BTrees library):
1. Each node can have multiple keys (not just one like BST)
2. Keys within a node are sorted
3. Node capacity: minimum degree `t` means:
   - Each node has ≥ t-1 keys and ≤ 2t-1 keys
   - Each node has ≥ t children and ≤ 2t children (except root)
4. All leaves are at the same level (perfectly balanced height)

**Why B-trees for databases**:
- Minimize disk I/O: One node = one disk block
- Shallow trees: High branching factor means fewer levels
- Cache-friendly: Reading a node loads many keys at once

## Complexity Analysis

**Time Complexity** (for B-tree with minimum degree t):
- Search: O(log_t n) disk accesses, O(t log_t n) comparisons
- Insert: O(log_t n) disk accesses
- Delete: O(log_t n) disk accesses
- Min/Max: O(log_t n)
- Range scan: O(log_t n + k) where k is result size

**Space Complexity**: O(n) with ~50% utilization (due to minimum occupancy)

**Height**: If tree has n keys and minimum degree t:
- Height ≤ log_t((n+1)/2)
- For t=100, million keys → height ≤ 3

## ZODB BTrees Variants

BTrees provides specialized implementations for different key/value types:

| Class | Key Type | Value Type | Use Case |
|-------|----------|------------|----------|
| OOBTree | object | object | General Python objects |
| IOBTree | int | object | Integer keys, object values |
| OIBTree | object | int | Object keys, integer values |
| IIBTree | int | int | Integer keys and values |
| IFBTree | int | float | Integer to float mapping |
| OUBTree | object | int (unsigned) | Object to unsigned int |
| LLBTree | long | long | 64-bit integer keys/values |
| LOBTree | long | object | 64-bit int keys, object values |
| OLBTree | object | long | Object keys, 64-bit int values |

**Set variants** (keys only, no values):
- OOSet, IOSet, IISet, LLSet, etc.

## Performance Characteristics

**Strengths**:
- Persistent storage: Optimized for ZODB's object persistence
- MVCC: Multiple readers don't block each other
- Large datasets: Efficient for millions of keys
- Specialized types: Integer-keyed trees are very fast

**Weaknesses**:
- Overkill for in-memory: SortedContainers is faster for pure in-memory
- ZODB coupling: Full features require ZODB database
- Learning curve: MVCC semantics can be surprising

**Benchmarks** (in-memory usage, not ZODB):
- Slower than SortedContainers for in-memory workloads
- Competitive with C++ std::map for integer keys
- Excellent for persistent data (ZODB's main use case)

## Python Implementation

### Basic Operations - OOBTree

```python
from BTrees.OOBTree import OOBTree

# Create B-tree
tree = OOBTree()

# Insert key-value pairs
tree['apple'] = 1
tree['banana'] = 2
tree['cherry'] = 3

# Search
value = tree['apple']  # 1
if 'banana' in tree:
    print("Found banana")

# Delete
del tree['banana']

# Iteration (sorted by key)
for key, value in tree.items():
    print(f"{key}: {value}")
# Output: apple: 1, cherry: 3 (sorted)

# Min/Max
min_key = tree.minKey()  # 'apple'
max_key = tree.maxKey()  # 'cherry'
```

### Integer-Keyed Tree - IOBTree

```python
from BTrees.IOBTree import IOBTree

# Integer keys are much faster
tree = IOBTree()

# Insert
for i in range(1000):
    tree[i] = f"value_{i}"

# Search
value = tree[500]  # Fast integer comparison

# Range queries
keys_in_range = tree.keys(100, 200)  # Keys from 100 to 199
for key in keys_in_range:
    print(f"{key}: {tree[key]}")
```

### Set Operations - IOSet

```python
from BTrees.IOBTree import IOSet

# Create sets
set1 = IOSet([1, 2, 3, 4, 5])
set2 = IOSet([4, 5, 6, 7, 8])

# Set operations
union = set1.union(set2)  # IOSet([1, 2, 3, 4, 5, 6, 7, 8])
intersection = set1.intersection(set2)  # IOSet([4, 5])
difference = set1.difference(set2)  # IOSet([1, 2, 3])

# Membership
if 3 in set1:
    print("Found 3")

# Iteration (sorted)
for value in set1:
    print(value)  # 1, 2, 3, 4, 5
```

### Range Queries

```python
from BTrees.OOBTree import OOBTree

tree = OOBTree()
tree['apple'] = 1
tree['banana'] = 2
tree['cherry'] = 3
tree['date'] = 4
tree['elderberry'] = 5

# Range query: keys from 'b' to 'd' (inclusive start, exclusive end)
keys = tree.keys('banana', 'elderberry')
for key in keys:
    print(f"{key}: {tree[key]}")
# Output:
# banana: 2
# cherry: 3
# date: 4

# Values in range
values = tree.values('banana', 'elderberry')
print(list(values))  # [2, 3, 4]

# Items in range
items = tree.items('banana', 'elderberry')
for key, value in items:
    print(f"{key}: {value}")
```

### MVCC - Conflict Resolution

```python
from BTrees.OOBTree import OOBTree
import transaction

# MVCC example (requires ZODB)
# Multiple transactions can read simultaneously
# Writes create new versions

tree = OOBTree()
tree['key'] = 'value1'

# Transaction 1
try:
    tree['key'] = 'value2'
    transaction.commit()
except:
    transaction.abort()

# Transaction 2 (concurrent)
# Will see snapshot from its start time
# Modern databases use similar MVCC
```

### Real-World Use Case - Persistent Counter

```python
from BTrees.IOBTree import IOBTree
from persistent import Persistent
import transaction

class PageViewCounter(Persistent):
    """Track page views per user in ZODB"""

    def __init__(self):
        self.views = IOBTree()  # user_id -> view_count

    def record_view(self, user_id: int):
        """Increment view count for user"""
        current = self.views.get(user_id, 0)
        self.views[user_id] = current + 1

    def get_top_users(self, n: int) -> list:
        """Get top N users by view count"""
        # Convert to list and sort by value
        items = [(user_id, count) for user_id, count in self.views.items()]
        items.sort(key=lambda x: x[1], reverse=True)
        return items[:n]

    def users_with_views_in_range(self, min_views: int, max_views: int):
        """Find users with view count in range"""
        # Note: BTrees are sorted by KEY, not VALUE
        # For value-based queries, need to scan
        result = []
        for user_id, count in self.views.items():
            if min_views <= count <= max_views:
                result.append((user_id, count))
        return result

# Usage with ZODB (simplified)
counter = PageViewCounter()
counter.record_view(user_id=123)
counter.record_view(user_id=456)
counter.record_view(user_id=123)  # Second view

print(counter.views[123])  # 2
print(counter.get_top_users(10))
```

### Memory-Efficient Large Collections

```python
from BTrees.IIBTree import IIBTree
import sys

# BTrees are more memory-efficient than dict for large collections
# Create large mapping
tree = IIBTree()
regular_dict = {}

# Insert 1M integers
for i in range(1_000_000):
    tree[i] = i * 2
    regular_dict[i] = i * 2

# Memory comparison (approximate)
# dict: ~200 MB (Python dict overhead)
# IIBTree: ~70 MB (C implementation, no Python object overhead)

print(f"Dict size: {sys.getsizeof(regular_dict) / 1e6:.1f} MB")
# Note: sys.getsizeof doesn't include referenced objects
# Real memory usage is much higher for dict
```

## When to Use BTrees

**Use BTrees when**:
- Using ZODB for object persistence
- Need MVCC (multi-version concurrency)
- Working with very large datasets (millions of keys)
- Integer keys (IOBTree, IIBTree are very fast)
- Need thread-safe data structures

**Use SortedContainers when**:
- Pure in-memory data structures
- Don't need persistence
- Want simpler API
- Faster for general-purpose use

**Use regular dict when**:
- Don't need sorted order
- < 100K items (dict is faster for lookups)

## B-tree vs BST Comparison

| Aspect | B-tree | Binary Search Tree |
|--------|--------|-------------------|
| Node capacity | Multiple keys (2t-1 max) | One key |
| Children per node | Multiple (2t max) | Two (left, right) |
| Height | log_t(n) (shallow) | log_2(n) (deeper) |
| Disk I/O | Optimized (1 node = 1 block) | Poor (1 key = 1 block) |
| Cache locality | Good (many keys per node) | Poor (pointer chasing) |
| Use case | Databases, filesystems | In-memory structures |
| Rebalancing | Split/merge nodes | Rotations |

**Why databases use B-trees**:
1. Shallow trees: Height 3-4 for billions of keys
2. Each node = one disk page (4KB typically)
3. Reading one node gets many keys → fewer disk reads

## Implementation Details

BTrees uses several optimizations:

1. **Bucket/Tree hybrid**:
   - Small collections: Use simple sorted list (bucket)
   - Large collections: Split into B-tree
   - Threshold: ~128 items

2. **Persistent references**:
   - In ZODB, nodes can be swapped to/from disk
   - Only active nodes kept in memory
   - Enables handling datasets larger than RAM

3. **Integer optimization**:
   - Integer keys stored as C arrays, not Python objects
   - No Python object overhead → 10x memory savings

4. **MVCC implementation**:
   - Copy-on-write for modified nodes
   - Multiple versions can coexist
   - Old versions garbage collected when no longer referenced

## Key Insights

1. **B-trees optimize for block I/O**: Designed when "disk seek is expensive, sequential read is cheap." Still relevant for modern SSDs and CPU cache.

2. **Multi-way > binary for external storage**: Binary search trees require more levels (more disk seeks). B-trees are shallower.

3. **Type specialization matters**: IOBTree's integer keys are 10x more memory-efficient than OOBTree's Python object keys.

4. **MVCC is powerful but complex**: Multiple concurrent readers without locking, but conflict resolution requires careful design.

5. **In-memory vs persistent**: BTrees excel at persistent storage. For pure in-memory, SortedContainers is simpler and often faster.

## Library Details

- **Package**: `BTrees`
- **Installation**: `pip install BTrees`
- **License**: Zope Public License (ZPL)
- **Maintenance**: Active (part of ZODB project)
- **Organization**: Zope Foundation
- **C Extension**: Yes (fast)
- **Python 3**: Supported
- **GitHub**: https://github.com/zopefoundation/BTrees
- **Docs**: https://btrees.readthedocs.io/

## Related Technologies

- **ZODB**: Object database that uses BTrees internally
- **SQLite B-trees**: Similar design, used for indexes
- **PostgreSQL**: Uses B+ trees (variant with all data in leaves)
- **MongoDB**: Uses B-trees for indexes
- **Filesystems**: ext4, XFS use B-trees for directory indexing

## References

- B-tree paper: Bayer & McCreight (1972)
- ZODB documentation: http://www.zodb.org/
- BTrees implementation: https://github.com/zopefoundation/BTrees
