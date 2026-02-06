# bintrees - Traditional BST Implementations

## Overview

**WARNING: This library is DEPRECATED.** Last release was 2014. Included for historical context and algorithm reference only.

bintrees provided Python implementations of classic balanced binary search trees: AVL trees, Red-Black trees, and splay trees. It offered both pure Python and C-based implementations (FastAVLTree, FastRBTree).

**Why it matters**: While deprecated, understanding these implementations helps evaluate modern alternatives and understand classic BST algorithms.

## Status & Alternatives

- **Status**: Unmaintained since 2014 (10+ years)
- **Python 3 compatibility**: Limited, unofficial forks exist
- **Recommended alternative**: SortedContainers (faster, maintained)
- **Educational value**: Good reference for BST algorithms

## Algorithm Implementations

### AVL Tree
Self-balancing BST that maintains height balance:
- Balance factor: |height(left) - height(right)| ≤ 1
- Rotations: Single and double rotations to maintain balance
- Guarantees: Worst-case O(log n) for all operations

### Red-Black Tree
Self-balancing BST with color properties:
- Properties: Root is black, red nodes have black children, all paths have same black height
- Rotations: Color flips and structural rotations
- Guarantees: Worst-case O(log n), better constant factors than AVL for insertions

### Splay Tree
Self-adjusting BST (not strictly balanced):
- Properties: Recently accessed elements move toward root
- Rotations: Splay operation on access
- Guarantees: Amortized O(log n), good for locality of reference

## Complexity Analysis

All three implementations:

**Time Complexity**:
- Insert: O(log n) worst-case (AVL, RB), amortized (Splay)
- Delete: O(log n) worst-case
- Search: O(log n) worst-case
- Min/Max: O(log n) - tree traversal required
- Successor/Predecessor: O(log n)

**Space Complexity**: O(n) with significant overhead
- Each node stores: value, left/right pointers, height/color/parent
- Memory: ~3-4x more than SortedContainers

## Performance Characteristics (Historical Benchmarks)

From bintrees documentation (2014):
- **C-based FastAVLTree**: Competitive with C++ std::map
- **Pure Python**: 10-50x slower than FastAVLTree
- **vs SortedContainers**: 2-5x slower than SortedContainers (even C version)

Reasons for slower performance:
1. **Pointer chasing**: Tree traversal has poor cache locality
2. **Node allocation overhead**: Each insert creates a new object
3. **Balancing overhead**: Rotations require pointer updates

## Python Implementation Examples

**Note**: These examples are for educational purposes. Use SortedContainers in production.

### AVL Tree - Basic Operations

```python
# Historical API (bintrees - DO NOT USE IN PRODUCTION)
from bintrees import AVLTree  # DEPRECATED

# Create tree
tree = AVLTree()

# Insert
tree[5] = "five"
tree[3] = "three"
tree[7] = "seven"
tree[1] = "one"
tree[9] = "nine"

# Search
value = tree[5]  # "five"
if 5 in tree:
    print("Found")

# Delete
del tree[5]

# Min/Max
min_key = tree.min_key()  # 1
max_key = tree.max_key()  # 9

# Iteration (in-order traversal)
for key, value in tree.items():
    print(f"{key}: {value}")
# Output is sorted: 1, 3, 7, 9
```

### Modern Equivalent with SortedContainers

```python
from sortedcontainers import SortedDict

# Same operations, faster performance
tree = SortedDict()
tree[5] = "five"
tree[3] = "three"
tree[7] = "seven"

# All same operations work
value = tree[5]
del tree[5]
min_key = tree.iloc[0]   # First key
max_key = tree.iloc[-1]  # Last key

# Faster iteration
for key, value in tree.items():
    print(f"{key}: {value}")
```

### AVL Tree Properties (Educational)

```python
# Conceptual AVL tree implementation (simplified)
class AVLNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None
        self.height = 1  # AVL-specific: track height

def height(node):
    return node.height if node else 0

def balance_factor(node):
    return height(node.left) - height(node.right)

def update_height(node):
    node.height = 1 + max(height(node.left), height(node.right))

def rotate_right(y):
    """Right rotation for left-heavy tree"""
    x = y.left
    T2 = x.right

    x.right = y
    y.left = T2

    update_height(y)
    update_height(x)
    return x

def rotate_left(x):
    """Left rotation for right-heavy tree"""
    y = x.right
    T2 = y.left

    y.left = x
    x.right = T2

    update_height(x)
    update_height(y)
    return y

def insert_avl(node, key, value):
    """AVL insert with balancing"""
    # Standard BST insert
    if not node:
        return AVLNode(key, value)

    if key < node.key:
        node.left = insert_avl(node.left, key, value)
    elif key > node.key:
        node.right = insert_avl(node.right, key, value)
    else:
        node.value = value  # Update existing
        return node

    # Update height
    update_height(node)

    # Check balance and perform rotations
    balance = balance_factor(node)

    # Left-Left case
    if balance > 1 and key < node.left.key:
        return rotate_right(node)

    # Right-Right case
    if balance < -1 and key > node.right.key:
        return rotate_left(node)

    # Left-Right case
    if balance > 1 and key > node.left.key:
        node.left = rotate_left(node.left)
        return rotate_right(node)

    # Right-Left case
    if balance < -1 and key < node.right.key:
        node.right = rotate_right(node.right)
        return rotate_left(node)

    return node
```

### Red-Black Tree Properties (Educational)

```python
# Conceptual Red-Black tree (simplified)
class RBNode:
    def __init__(self, key, value, color="RED"):
        self.key = key
        self.value = value
        self.left = None
        self.right = None
        self.parent = None
        self.color = color  # "RED" or "BLACK"

# Red-Black tree properties:
# 1. Every node is RED or BLACK
# 2. Root is BLACK
# 3. All leaves (NIL) are BLACK
# 4. Red nodes have BLACK children (no consecutive reds)
# 5. All paths from node to descendant leaves have same # of BLACK nodes

def is_red(node):
    return node and node.color == "RED"

def rotate_left_rb(node):
    """Left rotation (similar to AVL but with color management)"""
    right_child = node.right
    node.right = right_child.left
    if right_child.left:
        right_child.left.parent = node

    right_child.parent = node.parent
    if not node.parent:
        # node was root
        root = right_child
    elif node == node.parent.left:
        node.parent.left = right_child
    else:
        node.parent.right = right_child

    right_child.left = node
    node.parent = right_child
    return right_child

def fix_insert_rb(node):
    """Fix Red-Black properties after insert"""
    while node.parent and is_red(node.parent):
        if node.parent == node.parent.parent.left:
            uncle = node.parent.parent.right
            if is_red(uncle):
                # Case 1: Uncle is red - recolor
                node.parent.color = "BLACK"
                uncle.color = "BLACK"
                node.parent.parent.color = "RED"
                node = node.parent.parent
            else:
                # Case 2/3: Uncle is black - rotate
                if node == node.parent.right:
                    node = node.parent
                    rotate_left_rb(node)
                node.parent.color = "BLACK"
                node.parent.parent.color = "RED"
                rotate_right_rb(node.parent.parent)
        else:
            # Mirror cases
            pass
    # Ensure root is black
    # root.color = "BLACK"
```

## AVL vs Red-Black Comparison

| Aspect | AVL Tree | Red-Black Tree |
|--------|----------|----------------|
| Balance | Strictly balanced (height diff ≤ 1) | Loosely balanced (height ≤ 2×log n) |
| Rotations (insert) | 1-2 rotations | 0-2 rotations + recoloring |
| Rotations (delete) | O(log n) rotations | O(1) rotations + recoloring |
| Search speed | Faster (better balanced) | Slightly slower |
| Insert/Delete speed | Slower (more rotations) | Faster (fewer rotations) |
| Use case | Read-heavy workloads | Write-heavy workloads |
| Memory | Stores height | Stores color (1 bit) |

**Historical usage**:
- AVL: Database indexes, lookup tables
- Red-Black: C++ std::map, Java TreeMap, Linux kernel

## Why Traditional BSTs Failed in Python

1. **Cache locality**: Trees have poor spatial locality
   - Random pointer chasing vs contiguous arrays
   - SortedContainers exploits CPU cache better

2. **Object overhead**: Each node is a Python object
   - 64 bytes overhead per node on 64-bit Python
   - SortedContainers uses lists (single allocation)

3. **GC pressure**: Frequent allocations stress garbage collector
   - Tree rotations don't help when every node is an object

4. **Python's strengths**: Optimized for list operations, not pointer manipulation
   - CPython has fast list ops but slow attribute access
   - Trees do many attribute accesses (node.left, node.right, etc.)

## Educational Value

**When to study these algorithms**:
- Learning data structures (classic CS education)
- Understanding self-balancing properties
- Implementing similar structures in systems languages (C++, Rust)
- Database internals (B-trees are cousins of BSTs)

**Don't implement in Python for production**: Use SortedContainers instead.

## Migration Guide

If you have legacy code using bintrees:

```python
# Old: bintrees (DEPRECATED)
from bintrees import AVLTree
tree = AVLTree()
tree[5] = "value"
min_key = tree.min_key()

# New: SortedContainers (RECOMMENDED)
from sortedcontainers import SortedDict
tree = SortedDict()
tree[5] = "value"
min_key = tree.iloc[0]  # First key

# Additional benefits:
# - 2-5x faster
# - Active maintenance
# - Better documentation
# - More Pythonic API
```

## Key Insights

1. **Algorithm beauty ≠ practical performance**: AVL/RB trees are elegant algorithms but SortedContainers' pragmatic approach wins in Python.

2. **Language matters**: Algorithms optimized for C/C++ (pointer-based) may not translate well to Python (object-based).

3. **Maintenance matters**: Unmaintained libraries accumulate technical debt faster than algorithmic superiority can compensate.

4. **Pure Python can win**: With the right algorithm for the language's strengths, pure Python beats C extensions.

## References

- bintrees GitHub: https://github.com/mozman/bintrees (archived)
- AVL tree paper: Adelson-Velsky & Landis (1962)
- Red-Black tree: Guibas & Sedgewick (1978)
- Modern alternative: SortedContainers (Grant Jenks, 2014-present)
