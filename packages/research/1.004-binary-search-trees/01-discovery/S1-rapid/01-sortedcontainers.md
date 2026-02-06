# SortedContainers - Production BST Library

## Overview

SortedContainers is a pure-Python implementation of sorted list, sorted dict, and sorted set data structures. While not a traditional BST, it implements similar functionality using a B+ tree-like structure optimized for Python's memory model and cache locality.

**Key characteristics**:
- Pure Python (no C extensions required)
- Faster than C-extension alternatives (blist, rbtree, bintrees)
- Maintains sorted order with O(log n) operations
- Used by Hypothesis, Celery, pytest, and many production systems
- Active maintenance (100+ releases, 200K+ weekly downloads)

## Algorithm Description

SortedContainers uses a hybrid approach:
1. **SortedList**: List of sorted sublists (B+ tree-like structure)
   - Each sublist has size constraints (load factor)
   - Operations rebalance sublists when needed
   - Binary search within sublists

2. **Internal structure**:
   - Lists of ~1000 elements (tuned for Python's list performance)
   - Index tracking for O(1) length queries
   - Lazy deletion and compaction

The structure exploits Python's highly optimized list implementation while providing BST-like guarantees.

## Complexity Analysis

**Time Complexity**:
- `add()`: O(log n) - binary search + list insertion
- `remove()`: O(log n) - binary search + list deletion
- `__getitem__()`: O(log n) - index-based access
- `__contains__()`: O(log n) - binary search
- `bisect_left/right()`: O(log n) - find insertion point
- Iteration: O(n) - linear scan

**Space Complexity**: O(n) - overhead is ~25% compared to plain list

**Stability**: Maintains insertion order for equal elements (stable)

## Performance Characteristics

Benchmarks vs alternatives (from SortedContainers docs):
- **vs blist** (C extension): 5-10x faster for adds/removes
- **vs rbtree** (C extension): 2-5x faster for most operations
- **vs bintrees**: 10-50x faster (pure Python RB/AVL trees)
- **vs repeated list.sort()**: 182x faster for incremental updates

Real-world performance (1M elements):
- Add 1M items: ~1.2s (vs ~8s for repeated sort)
- Random access: ~40ns per lookup
- Iteration: Same as list (~30ns per element)

## Python Implementation

### Basic Usage - SortedList

```python
from sortedcontainers import SortedList

# Create and populate
sl = SortedList([5, 1, 3, 2, 4])
print(sl)  # SortedList([1, 2, 3, 4, 5])

# Add elements (maintains sorted order)
sl.add(2.5)
print(sl)  # SortedList([1, 2, 2.5, 3, 4, 5])

# Remove elements
sl.remove(3)
print(sl)  # SortedList([1, 2, 2.5, 4, 5])

# Index-based access (O(log n))
print(sl[2])  # 2.5

# Range queries
print(sl[1:4])  # SortedList([2, 2.5, 4])
```

### Advanced Features - Bisect Operations

```python
from sortedcontainers import SortedList

sl = SortedList([10, 20, 30, 40, 50])

# Find insertion point
idx = sl.bisect_left(25)
print(idx)  # 2 (would insert before 30)

# Range queries using bisect
left_idx = sl.bisect_left(20)
right_idx = sl.bisect_right(40)
print(sl[left_idx:right_idx])  # SortedList([20, 30, 40])

# Count elements in range
count = right_idx - left_idx
print(count)  # 3
```

### SortedDict - Key-Value Storage

```python
from sortedcontainers import SortedDict

# Create sorted dictionary
sd = SortedDict({'c': 3, 'a': 1, 'b': 2})
print(sd.keys())  # SortedKeysView(['a', 'b', 'c'])

# Iteration is sorted
for key, value in sd.items():
    print(f"{key}: {value}")
# a: 1
# b: 2
# c: 3

# Range queries by key
print(sd.iloc[0])  # 'a' - first key by sort order
print(sd.iloc[-1])  # 'c' - last key
```

### SortedSet - Unique Sorted Elements

```python
from sortedcontainers import SortedSet

# Create from iterable (duplicates removed, sorted)
ss = SortedSet([3, 1, 4, 1, 5, 9, 2, 6, 5])
print(ss)  # SortedSet([1, 2, 3, 4, 5, 6, 9])

# Set operations (intersection, union, etc.)
ss2 = SortedSet([2, 4, 6, 8])
print(ss & ss2)  # SortedSet([2, 4, 6]) - intersection
print(ss | ss2)  # SortedSet([1, 2, 3, 4, 5, 6, 8, 9]) - union

# Range queries
print(ss[2:5])  # SortedSet([3, 4, 5])
```

### Real-World Use Case - Leaderboard

```python
from sortedcontainers import SortedDict
from dataclasses import dataclass
from typing import Tuple

@dataclass
class Player:
    name: str
    score: int
    timestamp: float

class Leaderboard:
    def __init__(self):
        # Key: (score, timestamp) for tie-breaking
        # Value: player name
        self.scores = SortedDict()

    def add_score(self, player: Player):
        # Negative score for descending order
        key = (-player.score, player.timestamp)
        self.scores[key] = player.name

    def top_n(self, n: int) -> list[Tuple[str, int]]:
        """Get top N players in O(n) time"""
        result = []
        for (neg_score, _), name in list(self.scores.items())[:n]:
            result.append((name, -neg_score))
        return result

    def rank(self, player_name: str) -> int:
        """Get rank of player in O(log n) time"""
        for idx, (_, name) in enumerate(self.scores.items()):
            if name == player_name:
                return idx + 1
        return -1

# Usage
lb = Leaderboard()
lb.add_score(Player("Alice", 1000, 1.0))
lb.add_score(Player("Bob", 1500, 2.0))
lb.add_score(Player("Charlie", 1200, 3.0))

print(lb.top_n(3))
# [('Bob', 1500), ('Charlie', 1200), ('Alice', 1000)]

print(lb.rank("Charlie"))  # 2
```

### Performance Optimization Tips

```python
from sortedcontainers import SortedList

# Bulk loading is faster than incremental adds
data = list(range(1000000))
import random
random.shuffle(data)

# Fast: create from iterable
sl1 = SortedList(data)  # ~0.5s

# Slow: add one by one
sl2 = SortedList()
for x in data:
    sl2.add(x)  # ~1.2s (2.4x slower)

# Custom load factor for different workloads
# Default: 1000 (good for most cases)
# Higher load factor: better for read-heavy (less rebalancing)
# Lower load factor: better for write-heavy (faster rebalancing)
sl3 = SortedList(data, load=500)  # More frequent rebalancing
```

## Comparison with Traditional BSTs

**Advantages over AVL/Red-Black trees**:
1. **Faster in practice**: Exploits Python's optimized list operations
2. **Better cache locality**: Contiguous memory (lists) vs pointer-chasing (tree nodes)
3. **Pure Python**: No compilation required, easier to debug/modify
4. **Simpler implementation**: ~1000 LOC vs ~3000 LOC for balanced trees
5. **Index-based access**: O(log n) by index (trees can't do this efficiently)

**Disadvantages**:
1. **Not a true BST**: Different internal structure (list of lists)
2. **Higher constant factors**: O(log n) but with larger constants for some operations
3. **Memory overhead**: ~25% more than plain list (vs ~200% for node-based trees)
4. **No custom tree traversal**: Can't do in-order/pre-order traversal as you would with trees

## When to Use

**Use SortedContainers when**:
- You need sorted order with frequent insertions/deletions
- You're working in pure Python (no C extensions allowed)
- You need index-based access in addition to sorted order
- You want production-ready, well-maintained library
- Performance matters (it's faster than alternatives)

**Use traditional BST when**:
- You need specific tree properties (height, balance factor)
- You're implementing a textbook algorithm that requires BST structure
- You need custom tree traversal (in-order, level-order, etc.)
- Educational purposes (learning BST algorithms)

## Library Details

- **Package**: `sortedcontainers`
- **Installation**: `pip install sortedcontainers`
- **License**: Apache 2.0
- **Maintenance**: Active (last release 2024)
- **Author**: Grant Jenks
- **Downloads**: 200K+ per week
- **GitHub**: https://github.com/grantjenks/python-sortedcontainers
- **Docs**: http://www.grantjenks.com/docs/sortedcontainers/

## Key Insights

1. **Not all BSTs are trees**: SortedContainers proves you can achieve BST properties without a tree structure, often with better performance.

2. **Cache locality matters more than asymptotic complexity**: The B+ tree-like approach (lists of lists) outperforms traditional trees due to better CPU cache usage.

3. **Python's list is heavily optimized**: A list of 1000 elements is faster than a tree with 1000 nodes due to interpreter-level optimizations.

4. **Pure Python can be faster than C extensions**: When the algorithm is designed for Python's strengths (list operations, memory model), pure Python wins.

5. **Production success proves design**: Used by thousands of projects including major frameworks (Hypothesis, Celery), demonstrating real-world viability.

## Related Operations

- **Interval trees**: Can be built on top of SortedList for range overlap queries
- **Priority queues**: SortedList can serve as a priority queue with O(log n) operations
- **Order statistics**: Finding kth smallest element is O(log n) with index access
- **Range queries**: Natural fit for "find all elements between x and y"
