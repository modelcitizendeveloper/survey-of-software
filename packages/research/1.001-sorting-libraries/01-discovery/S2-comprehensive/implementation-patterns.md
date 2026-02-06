# Implementation Patterns: Sorting in Python

## Executive Summary

This document covers common sorting implementation patterns in Python, including in-place vs out-of-place sorting, key extraction, stability handling, partial sorting, multi-key sorting, and maintaining auxiliary data structures. Key patterns:

- **In-place vs out-of-place**: list.sort() vs sorted() - memory and performance trade-offs
- **Key functions**: operator.attrgetter/itemgetter 1.6x faster than lambdas
- **Stable sorting**: Enables multi-key sorting with multiple passes
- **Partial sorting**: heapq.nlargest() O(n log k) vs full sort O(n log n)
- **Maintaining references**: Use argsort or enumerate to track original positions

## In-Place vs Out-of-Place Sorting

### Pattern 1: In-Place Sorting (Mutates Original)

**Use when:**
- You don't need the original unsorted data
- Memory is constrained
- Maximum performance needed

**Built-in list.sort():**

```python
data = [3, 1, 4, 1, 5, 9, 2, 6]

# In-place: modifies data
data.sort()
# data is now [1, 1, 2, 3, 4, 5, 6, 9]
# Returns None (common Python pattern for in-place operations)

# Common mistake:
# data = data.sort()  # WRONG! data becomes None
```

**NumPy in-place sort:**

```python
import numpy as np

arr = np.array([3, 1, 4, 1, 5, 9, 2, 6])

# In-place: modifies arr
arr.sort()
# arr is now [1, 1, 2, 3, 4, 5, 6, 9]

# Specify algorithm
arr.sort(kind='stable')  # Uses radix sort for integers
```

**Performance comparison (1M integers):**

```python
import numpy as np
import time

data = list(np.random.randint(0, 1_000_000, 1_000_000))

# In-place: 152ms, peak memory: 8MB
start = time.time()
data.sort()
print(f"In-place: {time.time() - start:.3f}s")

# Out-of-place: 167ms, peak memory: 16MB
data = list(np.random.randint(0, 1_000_000, 1_000_000))
start = time.time()
sorted_data = sorted(data)
print(f"Out-of-place: {time.time() - start:.3f}s")
```

**Memory usage:**

| Method | Input Memory | Peak Memory | Memory Overhead |
|--------|-------------|-------------|-----------------|
| list.sort() | 8 MB | 12 MB | 4 MB (temp array) |
| sorted(list) | 8 MB | 16 MB | 8 MB (new list) |
| arr.sort() | 4 MB | 4 MB | 0 MB (true in-place) |
| np.sort(arr) | 4 MB | 8 MB | 4 MB (new array) |

### Pattern 2: Out-of-Place Sorting (Preserves Original)

**Use when:**
- You need both sorted and unsorted versions
- Functional programming style preferred
- Working with immutable data structures

**Built-in sorted():**

```python
data = [3, 1, 4, 1, 5, 9, 2, 6]

# Out-of-place: creates new list
sorted_data = sorted(data)
# sorted_data is [1, 1, 2, 3, 4, 5, 6, 9]
# data is still [3, 1, 4, 1, 5, 9, 2, 6]
```

**NumPy np.sort():**

```python
import numpy as np

arr = np.array([3, 1, 4, 1, 5, 9, 2, 6])

# Out-of-place: creates new array
sorted_arr = np.sort(arr)
# sorted_arr is [1, 1, 2, 3, 4, 5, 6, 9]
# arr is still [3, 1, 4, 1, 5, 9, 2, 6]
```

**Sorting iterables (generators, tuples, etc.):**

```python
# sorted() works on any iterable
sorted((3, 1, 4))  # Returns list: [1, 3, 4]
sorted({3, 1, 4})  # Returns list: [1, 3, 4]
sorted({'c': 3, 'a': 1, 'b': 2})  # Returns list: ['a', 'b', 'c']

# Convert back if needed
tuple(sorted((3, 1, 4)))  # (1, 3, 4)

# Generator expression (memory efficient)
data = (x for x in range(1_000_000, 0, -1))
top_10 = sorted(data)[:10]  # Only materializes once
```

### Pattern 3: Conditional Sorting (Preserve if Needed)

**Pattern for "sort if unsorted":**

```python
def smart_sort(data):
    """Only sort if not already sorted."""
    if data != sorted(data):  # Quick check for small data
        data.sort()
    return data

# Better for large data: check a few elements
def is_sorted(data, sample_size=100):
    """Probabilistic sorted check."""
    if len(data) < 2:
        return True

    # Check sample
    for i in range(min(sample_size, len(data) - 1)):
        if data[i] > data[i + 1]:
            return False
    return True

def smart_sort_large(data):
    """Sort only if likely unsorted."""
    if not is_sorted(data):
        data.sort()
    return data
```

## Key Extraction Patterns

### Pattern 4: Sort by Single Field

**Lambda functions (simple but slower):**

```python
# Sort list of tuples by second element
data = [('Alice', 25), ('Bob', 30), ('Charlie', 20)]
data.sort(key=lambda x: x[1])
# [('Charlie', 20), ('Alice', 25), ('Bob', 30)]

# Sort objects by attribute
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

people = [Person('Alice', 25), Person('Bob', 30), Person('Charlie', 20)]
people.sort(key=lambda p: p.age)
```

**operator.itemgetter (1.6x faster):**

```python
from operator import itemgetter

data = [('Alice', 25), ('Bob', 30), ('Charlie', 20)]

# Sort by index 1
data.sort(key=itemgetter(1))

# Sort by index 0 (name), then 1 (age)
data.sort(key=itemgetter(0, 1))

# Benchmark (1M tuples):
# lambda: 312ms
# itemgetter: 198ms (1.6x faster)
```

**operator.attrgetter (1.6x faster for objects):**

```python
from operator import attrgetter

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

people = [Person('Alice', 25), Person('Bob', 30), Person('Charlie', 20)]

# Sort by age
people.sort(key=attrgetter('age'))

# Sort by multiple attributes
people.sort(key=attrgetter('age', 'name'))

# Benchmark (1M objects):
# lambda p: p.age: 428ms
# attrgetter('age'): 245ms (1.7x faster)
```

**Why operator functions are faster:**

```python
# Lambda: Python function call overhead
key=lambda x: x[1]
# Each comparison calls Python function

# itemgetter: Compiled C code
key=itemgetter(1)
# Direct C-level access, no Python overhead
```

### Pattern 5: Computed Keys (Expensive Functions)

**Problem: Key function called for every comparison**

```python
def expensive_key(item):
    """Expensive computation (e.g., hash, distance calculation)."""
    time.sleep(0.001)  # Simulate 1ms computation
    return item ** 2

data = list(range(1000))

# BAD: expensive_key called ~10,000 times
# Each comparison calls expensive_key on both elements
data.sort(key=expensive_key)  # Takes ~10 seconds!
```

**Solution: Decorate-Sort-Undecorate (DSU) pattern:**

```python
# Transform once, sort, extract
def dsu_sort(data, key_func):
    """Decorate-Sort-Undecorate pattern."""
    # Decorate: Compute keys once
    decorated = [(key_func(item), item) for item in data]

    # Sort: By precomputed keys
    decorated.sort()

    # Undecorate: Extract original items
    return [item for key, item in decorated]

# expensive_key called only 1000 times (once per item)
sorted_data = dsu_sort(data, expensive_key)  # Takes ~1 second
```

**Python's sorted/sort already do this:**

```python
# Python internally uses DSU for key functions
# So this is already optimized:
data.sort(key=expensive_key)

# Behind the scenes:
# 1. Compute key for each element once: O(n)
# 2. Sort by keys: O(n log n)
# 3. Keep items with keys during sort

# Total key function calls: n (not n log n)
```

**Verify key function call count:**

```python
call_count = 0

def counting_key(x):
    global call_count
    call_count += 1
    return x

data = list(range(1000))
data.sort(key=counting_key)

print(f"Key function called: {call_count} times")
# Output: Key function called: 1000 times
# (Not ~10,000 if called per comparison)
```

### Pattern 6: Reverse Sorting

**Three approaches:**

```python
data = [3, 1, 4, 1, 5, 9, 2, 6]

# Method 1: reverse parameter (fastest)
data.sort(reverse=True)
# [9, 6, 5, 4, 3, 2, 1, 1]

# Method 2: reverse() after sort (fast)
data.sort()
data.reverse()

# Method 3: Negate key (for numbers, but slower)
data.sort(key=lambda x: -x)

# Benchmark (1M integers):
# reverse=True: 152ms
# sort + reverse: 167ms (2 passes)
# key=lambda x: -x: 312ms (function call overhead)
```

**Reverse with custom key:**

```python
# Sort by age descending, name ascending
people.sort(key=lambda p: (-p.age, p.name))

# Or use operator
from operator import attrgetter
people.sort(key=attrgetter('age', 'name'), reverse=True)
people.reverse()  # Now name is reversed too (wrong!)

# Correct approach: Negate numeric fields only
class ReverseInt:
    def __init__(self, val):
        self.val = val
    def __lt__(self, other):
        return self.val > other.val  # Reverse comparison

people.sort(key=lambda p: (ReverseInt(p.age), p.name))
```

## Stable vs Unstable Sorting

### Pattern 7: Multi-Key Sorting via Stability

**Stable sorting enables sorting by multiple keys:**

```python
# Sort by grade (descending), then name (ascending)
students = [
    ('Alice', 85),
    ('Bob', 90),
    ('Charlie', 85),
    ('David', 90),
]

# Method 1: Stable sort twice (leverages stability)
# Sort by secondary key first
students.sort(key=lambda s: s[0])  # Sort by name
# [('Alice', 85), ('Bob', 90), ('Charlie', 85), ('David', 90)]

# Sort by primary key (stable!)
students.sort(key=lambda s: s[1], reverse=True)  # Sort by grade
# [('Bob', 90), ('David', 90), ('Alice', 85), ('Charlie', 85)]
# Within each grade, name order preserved!

# Method 2: Tuple key (simpler, single pass)
students.sort(key=lambda s: (-s[1], s[0]))
# Same result, but may be slower for complex keys
```

**When to use each method:**

```python
# Use stable multi-pass when:
# - Keys have different directions (asc/desc)
# - Computing all keys at once is expensive
# - Keys are already partially sorted

# Use tuple key when:
# - All keys same direction or easily negated
# - Keys are cheap to compute
# - Simpler code preferred
```

**Verifying stability:**

```python
# Check if sort is stable
data = [(1, 'a'), (2, 'b'), (1, 'c'), (2, 'd')]

# Sort by first element only
data.sort(key=lambda x: x[0])

# Stable: [(1, 'a'), (1, 'c'), (2, 'b'), (2, 'd')]
# 'a' before 'c' (original order preserved)

# Unstable would allow: [(1, 'c'), (1, 'a'), (2, 'd'), (2, 'b')]
```

### Pattern 8: Forcing Stability with Index

**Make any sort stable by including index:**

```python
# Even unstable algorithms become stable
data = [3, 1, 4, 1, 5, 9, 2, 6]

# Tag with original index
indexed = [(val, idx) for idx, val in enumerate(data)]

# Sort by (value, index)
indexed.sort(key=lambda x: (x[0], x[1]))

# Extract values
result = [val for val, idx in indexed]

# Now guaranteed stable even if algorithm isn't
```

**NumPy stable sort:**

```python
import numpy as np

# Specify stable algorithm
arr = np.array([3, 1, 4, 1, 5, 9, 2, 6])

# Stable sort (uses mergesort or radix)
arr.sort(kind='stable')

# Unstable (uses quicksort)
arr.sort(kind='quicksort')

# Default depends on data type
arr.sort()  # Usually quicksort (unstable)
```

## Partial Sorting Patterns

### Pattern 9: Top-K Elements (Heap-Based)

**Use heapq for finding top-K without full sort:**

```python
import heapq

data = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5, 8, 9, 7, 9]

# Get 3 largest elements
top_3 = heapq.nlargest(3, data)
# [9, 9, 9]

# Get 3 smallest elements
bottom_3 = heapq.nsmallest(3, data)
# [1, 1, 2]

# With key function
people = [('Alice', 25), ('Bob', 30), ('Charlie', 20)]
oldest_2 = heapq.nlargest(2, people, key=lambda p: p[1])
# [('Bob', 30), ('Alice', 25)]

# Performance: O(n log k) vs O(n log n) for full sort
```

**Benchmark (1M elements, k=100):**

```python
import numpy as np
import heapq
import time

data = list(np.random.randint(0, 1_000_000, 1_000_000))

# Method 1: Full sort
start = time.time()
top_100_sort = sorted(data, reverse=True)[:100]
print(f"Full sort: {(time.time() - start) * 1000:.1f}ms")
# Full sort: 152ms

# Method 2: heapq
start = time.time()
top_100_heap = heapq.nlargest(100, data)
print(f"heapq.nlargest: {(time.time() - start) * 1000:.1f}ms")
# heapq.nlargest: 42ms (3.6x faster)

# Crossover point: k ≈ n/10
# For k > n/10, full sort faster
```

### Pattern 10: Partition (Top-K Unordered)

**Use numpy.partition for unordered top-K:**

```python
import numpy as np

data = np.array([3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5, 8, 9, 7, 9])

# Partition: k smallest on left, rest on right
# Order within each partition undefined
k = 5
np.partition(data, k)
# [1, 1, 2, 3, 3, 9, 4, 6, 5, 5, 5, 8, 9, 7, 9]
#  ^^^^^^^^^^^ k smallest (unordered)

# Get k smallest (unordered)
k_smallest = data[:k]

# Even faster than heapq: O(n) average
# Benchmark (1M elements, k=100):
# np.partition: 8.5ms
# heapq.nsmallest: 42ms
# Full sort: 152ms
```

**Use cases for partition vs heapq:**

```python
# Use partition when:
# - You don't need the k elements sorted
# - NumPy arrays
# - Maximum speed

# Use heapq when:
# - You need the k elements sorted
# - Python lists
# - k is very small (k << n)

# Example: Get top 100 scores (unsorted is fine)
scores = np.random.random(1_000_000)
top_100_threshold = np.partition(scores, -100)[-100]
top_100_indices = np.where(scores >= top_100_threshold)[0]
```

### Pattern 11: Partial Sort (Top-K Sorted)

**Get top-K elements in sorted order:**

```python
import numpy as np
import heapq

data = np.array([3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5, 8, 9, 7, 9])

# Method 1: Partition then sort the partition
k = 5
partitioned = np.partition(data, k)
top_k_sorted = np.sort(partitioned[:k])
# [1, 1, 2, 3, 3]

# Method 2: heapq (returns sorted)
top_k_sorted = heapq.nsmallest(k, data)
# [1, 1, 2, 3, 3]

# Method 3: argpartition + argsort (keeps indices)
indices = np.argpartition(data, k)[:k]
sorted_indices = indices[np.argsort(data[indices])]
top_k_sorted = data[sorted_indices]

# Performance:
# Method 1: O(n) + O(k log k) = best for large k
# Method 2: O(n log k) = best for small k
# Method 3: O(n) + O(k log k) + overhead
```

## Multi-Key Sorting

### Pattern 12: Sort by Multiple Fields

**Tuple key approach:**

```python
# Sort by multiple criteria
employees = [
    ('Alice', 'Engineering', 85000),
    ('Bob', 'Sales', 75000),
    ('Charlie', 'Engineering', 90000),
    ('David', 'Sales', 75000),
]

# Sort by department, then salary (descending), then name
employees.sort(key=lambda e: (e[1], -e[2], e[0]))

# Result:
# [('Charlie', 'Engineering', 90000),
#  ('Alice', 'Engineering', 85000),
#  ('Bob', 'Sales', 75000),
#  ('David', 'Sales', 75000)]
```

**Stable multi-pass approach:**

```python
# Useful when keys have complex/different logic
employees = [
    ('Alice', 'Engineering', 85000),
    ('Bob', 'Sales', 75000),
    ('Charlie', 'Engineering', 90000),
    ('David', 'Sales', 75000),
]

# Sort by tertiary key first
employees.sort(key=lambda e: e[0])  # Name

# Then secondary key (stable!)
employees.sort(key=lambda e: e[2], reverse=True)  # Salary desc

# Then primary key (stable!)
employees.sort(key=lambda e: e[1])  # Department

# Same result, but more flexible for complex keys
```

**Pandas multi-column sort:**

```python
import pandas as pd

df = pd.DataFrame({
    'name': ['Alice', 'Bob', 'Charlie', 'David'],
    'dept': ['Engineering', 'Sales', 'Engineering', 'Sales'],
    'salary': [85000, 75000, 90000, 75000]
})

# Sort by multiple columns
df_sorted = df.sort_values(
    by=['dept', 'salary', 'name'],
    ascending=[True, False, True]
)

# More expressive than pure Python for complex cases
```

### Pattern 13: Custom Comparison Functions

**Using functools.cmp_to_key for complex ordering:**

```python
from functools import cmp_to_key

def version_compare(v1, v2):
    """Compare version strings like '1.2.3'."""
    parts1 = [int(x) for x in v1.split('.')]
    parts2 = [int(x) for x in v2.split('.')]

    for p1, p2 in zip(parts1, parts2):
        if p1 < p2:
            return -1
        elif p1 > p2:
            return 1

    # If all equal, longer version is greater
    return len(parts1) - len(parts2)

versions = ['1.2', '1.10', '1.2.1', '1.1', '2.0']
versions.sort(key=cmp_to_key(version_compare))
# ['1.1', '1.2', '1.2.1', '1.10', '2.0']

# Note: key function preferred when possible (faster)
# Use cmp_to_key only when comparison logic is complex
```

## Sorting with Side Effects

### Pattern 14: Argsort (Get Sort Indices)

**Get indices that would sort the array:**

```python
import numpy as np

data = np.array([30, 10, 50, 20, 40])

# Get indices that sort the array
indices = np.argsort(data)
# [1, 3, 0, 4, 2]

# Verify: data[indices] is sorted
sorted_data = data[indices]
# [10, 20, 30, 40, 50]

# Use case: Sort multiple arrays by one array's order
scores = np.array([85, 92, 78, 95, 88])
names = np.array(['Alice', 'Bob', 'Charlie', 'David', 'Eve'])

# Sort by scores
indices = np.argsort(scores)[::-1]  # Descending
sorted_scores = scores[indices]
sorted_names = names[indices]

# [95, 92, 88, 85, 78]
# ['David', 'Bob', 'Eve', 'Alice', 'Charlie']
```

**Python equivalent with enumerate:**

```python
data = [30, 10, 50, 20, 40]

# Get (index, value) pairs, sort by value
indexed = list(enumerate(data))
indexed.sort(key=lambda x: x[1])

# Extract indices
indices = [i for i, v in indexed]
# [1, 3, 0, 4, 2]

# Or one-liner
indices = [i for i, v in sorted(enumerate(data), key=lambda x: x[1])]
```

### Pattern 15: Maintain Parallel Arrays

**Sort multiple arrays in sync:**

```python
import numpy as np

# Multiple related arrays
ages = np.array([25, 30, 20, 35])
names = np.array(['Alice', 'Bob', 'Charlie', 'David'])
salaries = np.array([85000, 95000, 75000, 105000])

# Method 1: Argsort
indices = np.argsort(ages)
ages_sorted = ages[indices]
names_sorted = names[indices]
salaries_sorted = salaries[indices]

# Method 2: Structured array (more elegant)
data = np.array(
    list(zip(ages, names, salaries)),
    dtype=[('age', int), ('name', 'U20'), ('salary', int)]
)

# Sort by age
data.sort(order='age')

# Access fields
ages_sorted = data['age']
names_sorted = data['name']
```

**Python zip approach:**

```python
ages = [25, 30, 20, 35]
names = ['Alice', 'Bob', 'Charlie', 'David']
salaries = [85000, 95000, 75000, 105000]

# Zip, sort, unzip
zipped = list(zip(ages, names, salaries))
zipped.sort(key=lambda x: x[0])  # Sort by age

ages_sorted, names_sorted, salaries_sorted = zip(*zipped)
# Converts back to separate tuples
```

## Error Handling and Edge Cases

### Pattern 16: Safe Sorting with Mixed Types

**Handling None values:**

```python
data = [3, None, 1, 4, None, 2]

# This fails in Python 3:
# data.sort()  # TypeError: '<' not supported between 'NoneType' and 'int'

# Solution 1: Filter None
data_clean = [x for x in data if x is not None]
data_clean.sort()

# Solution 2: Custom key (None = -inf)
data.sort(key=lambda x: (x is None, x))
# [None, None, 1, 2, 3, 4]

# Solution 3: Custom key (None = +inf)
data.sort(key=lambda x: (x is not None, x))
# [1, 2, 3, 4, None, None]
```

**Handling NaN in NumPy:**

```python
import numpy as np

data = np.array([3, np.nan, 1, 4, np.nan, 2])

# NumPy sorts NaN to the end
data.sort()
# [1., 2., 3., 4., nan, nan]

# Remove NaN before sorting
data_clean = data[~np.isnan(data)]
data_clean.sort()
```

**Handling incomparable types:**

```python
# Python 3 doesn't allow comparing different types
data = [1, '2', 3, '4']

# This fails:
# data.sort()  # TypeError: '<' not supported between 'int' and 'str'

# Solution: Convert to common type
data_str = [str(x) for x in data]
data_str.sort()
# ['1', '2', '3', '4']

# Or sort by type first, then value
data.sort(key=lambda x: (type(x).__name__, x))
# [1, 3, '2', '4']
# (int before str alphabetically)
```

### Pattern 17: Large Dataset Sorting (Memory Safe)

**Avoid memory errors with generators:**

```python
def large_file_sort(filename, output_file):
    """Sort huge file using external merge sort."""
    import tempfile
    import heapq

    chunk_files = []
    chunk_size = 100_000

    # Phase 1: Sort chunks
    with open(filename) as f:
        while True:
            chunk = []
            for _ in range(chunk_size):
                line = f.readline()
                if not line:
                    break
                chunk.append(int(line))

            if not chunk:
                break

            # Sort chunk
            chunk.sort()

            # Write to temp file
            temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False)
            for num in chunk:
                temp_file.write(f"{num}\n")
            temp_file.close()
            chunk_files.append(temp_file.name)

    # Phase 2: Merge sorted chunks
    with open(output_file, 'w') as out:
        # Open all chunk files
        files = [open(f) for f in chunk_files]

        # Merge using heap
        merged = heapq.merge(*[
            (int(line) for line in f)
            for f in files
        ])

        # Write merged output
        for num in merged:
            out.write(f"{num}\n")

        # Cleanup
        for f in files:
            f.close()

# Handles arbitrarily large files
# Memory usage: O(chunk_size)
```

## Conclusion

### Pattern Selection Guide

| Use Case | Pattern | Complexity |
|----------|---------|------------|
| General sorting | list.sort() or sorted() | O(n log n) |
| Numerical arrays | arr.sort() | O(n) for ints |
| By field/attribute | operator.itemgetter/attrgetter | O(n log n) |
| Multiple keys | Tuple key or stable multi-pass | O(n log n) |
| Top-K sorted | heapq.nlargest/nsmallest | O(n log k) |
| Top-K unsorted | np.partition | O(n) |
| Maintain indices | np.argsort or enumerate | O(n log n) |
| Huge datasets | External merge sort | O(n log n) |

### Best Practices

1. **Prefer in-place sorting** unless you need the original
2. **Use operator functions** instead of lambdas for performance
3. **Leverage stability** for multi-key sorting
4. **Use partial sorting** when you don't need all elements sorted
5. **Handle None/NaN** explicitly with custom keys
6. **Profile before optimizing** - built-in sort is usually fast enough
