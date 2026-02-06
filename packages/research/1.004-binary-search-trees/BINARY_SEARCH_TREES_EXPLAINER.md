# What are Binary Search Trees?

> Efficient data structures for maintaining sorted data with fast insertion, deletion, and lookup

## Core Concepts

**Binary Search Tree (BST)** is a tree data structure where each node has at most two children (left and right), and values are organized so that:
- Left subtree contains values less than the node
- Right subtree contains values greater than the node
- This property holds recursively for all nodes

**Why this matters:**
- Finding an element: O(log n) average time (vs O(n) for unsorted lists)
- Inserting while maintaining sort order: O(log n)
- Range queries (all values between X and Y): Very efficient

**Real-world analogy:** Like a decision tree for guessing a number between 1-100. Each guess eliminates half the remaining possibilities. With 7 guesses, you can find any number.

## When You Need This

Use BSTs when you need **sorted data with frequent modifications**:

### Typical Use Cases
1. **Leaderboards** - Track top scores that change frequently
2. **Priority queues** - Process items by priority (medical triage, task schedulers)
3. **Range queries** - Find all users between ages 25-35
4. **Autocomplete** - Find all words starting with "pro..."
5. **Event scheduling** - Find next event after timestamp X

### When NOT to use BSTs
- **Static sorted data** → Use sorted list + binary search (simpler, faster)
- **Unsorted data** → Use hash table (O(1) lookup vs O(log n))
- **Mostly sequential access** → Use array/list (better cache locality)

## Common Approaches

### 1. Classic BSTs (AVL, Red-Black Trees)
**What:** Self-balancing trees that guarantee O(log n) operations
**Languages:** C++, Java standard libraries use Red-Black trees
**Trade-off:** Complex implementation, pointer overhead

**Example (C++ std::map):**
```cpp
std::map<int, string> leaderboard;  // Red-Black tree
leaderboard[100] = "Alice";          // O(log n) insert
leaderboard[95] = "Bob";
```

### 2. B-trees (Multiway Trees)
**What:** Trees with many children per node (not just 2)
**Use case:** Databases (PostgreSQL, MySQL indexes)
**Why:** Matches disk page size - fewer disk seeks

**Key insight:** Database pages are 4KB-16KB. B-tree fits hundreds of keys per node, so tree height is very shallow (3-4 levels for billions of keys).

### 3. Python: Pragmatic Alternatives
**What:** Python libraries abandon traditional trees for cache-friendly structures
**Winner:** SortedContainers (list-of-sorted-lists, not a tree)
**Why:** Python object overhead makes traditional trees slow

**Example:**
```python
from sortedcontainers import SortedList

scores = SortedList()  # Not a tree! List-of-lists
scores.add(100)        # O(log n), stays sorted
scores.add(95)
top_5 = scores[-5:]    # Efficient slicing
```

## The Modern Reality

**Classic computer science:** "Use balanced BSTs for sorted data"
**Modern practice:** Depends heavily on context:

- **C/C++:** Red-Black trees still optimal (low overhead)
- **Python:** List-based structures often faster (SortedContainers)
- **Databases:** B-trees dominate (disk-aware design)
- **Go/Rust:** Skip lists emerging (simpler than RB trees)

**Why the divergence?**
1. **Cache locality matters** - Modern CPUs fetch 64-byte cache lines. Sequential list access is 10x+ faster than pointer-chasing
2. **Language overhead** - Python objects have 40+ bytes overhead. Tree node = 100+ bytes. List element = 8 bytes.
3. **Hardware evolution** - RAM latency hasn't scaled with CPU speed. Cache misses cost 100+ cycles.

## Key Takeaway

Binary search trees are a **concept**, not a specific implementation. The best data structure for sorted data depends on:
- Your programming language (overhead characteristics)
- Your hardware (CPU cache size, RAM speed)
- Your access patterns (reads vs writes, range queries vs point lookups)

**Modern best practice:** Use your language's standard library sorted container (C++ `std::map`, Python `sortedcontainers`, Java `TreeMap`) unless you have measured performance issues.

## Further Reading

**Foundational:**
- [Introduction to Algorithms (CLRS)](https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/) - Chapter 12 (Binary Search Trees), Chapter 13 (Red-Black Trees)
- [AVL Trees](https://en.wikipedia.org/wiki/AVL_tree) - Original self-balancing BST

**Modern perspectives:**
- [SortedContainers Documentation](http://www.grantjenks.com/docs/sortedcontainers/) - Why lists beat trees in Python
- [B-Trees: More Than I Thought I'd Want to Know](https://benjamincongdon.me/blog/2021/08/17/B-Trees-More-Than-I-Thought-Id-Want-to-Know/) - Database perspective

**Performance deep-dives:**
- [What Every Programmer Should Know About Memory](https://people.freebsd.org/~lstewart/articles/cpumemory.pdf) - Why cache locality matters
- [Are You Sure You Want to Use MMAP in Your Database?](https://db.cs.cmu.edu/mmap-cidr2022/) - Hardware realities affect algorithm choices
