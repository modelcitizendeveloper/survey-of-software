# NumPy Sorting Functions

## Overview

NumPy provides high-performance sorting functions optimized for numerical arrays. These functions
leverage compiled C code and vectorized operations, offering significant speed advantages over
Python's built-in sort for numerical data, especially large arrays.

## Core Functions

### np.sort() - Returns sorted copy
### np.argsort() - Returns indices that would sort the array
### np.partition() / np.argpartition() - Partial sorting for k-th element problems
### ndarray.sort() - In-place sorting

## Algorithm Selection

NumPy automatically selects algorithms based on data type and parameters:

**Default algorithms**:
- **Quicksort**: Default for general sorting (unstable, O(n log n) average)
- **Mergesort**: Available for stable sorting (O(n log n) worst case)
- **Heapsort**: Available as alternative (O(n log n) worst case, in-place)
- **Timsort**: Added for better performance on partially sorted data
- **Radix sort**: Automatically used for integer types when stable sort requested (O(n) complexity!)

## Complexity Analysis

**Time Complexity**:
- Quicksort (default): O(n log n) average, O(n²) worst case (rare)
- Mergesort/Stable: O(n log n) all cases
- Radix sort (integers): O(n) - linear time!
- Partition: O(n) - linear partial sort

**Space Complexity**:
- In-place sort: O(1) additional space
- np.sort(): O(n) for returned copy
- Mergesort: O(n) temporary storage
- Radix sort: O(n) additional space

## Performance Characteristics

**Speed advantages**:
- 10-100x faster than Python list.sort() for large numerical arrays
- Radix sort for integers provides O(n) performance
- Contiguous memory layout enables cache-friendly operations
- SIMD vectorization on modern CPUs

**Memory efficiency**:
- Use in-place sort (ndarray.sort()) when possible
- Ensure arrays are C-contiguous for best performance
- argpartition uses O(n) vs O(n log n) for argsort

## Python Implementation

### Basic Sorting

```python
import numpy as np

# np.sort() - returns sorted copy
arr = np.array([64, 34, 25, 12, 22, 11, 90])
sorted_arr = np.sort(arr)
print(sorted_arr)  # [11 12 22 25 34 64 90]
print(arr)  # [64 34 25 12 22 11 90] - original unchanged

# In-place sorting
arr.sort()  # Modifies arr directly
print(arr)  # [11 12 22 25 34 64 90]

# Specify algorithm
arr = np.array([3, 1, 4, 1, 5, 9, 2, 6])
sorted_stable = np.sort(arr, kind='stable')  # Uses radix sort for integers!
sorted_merge = np.sort(arr, kind='mergesort')
sorted_heap = np.sort(arr, kind='heapsort')
```

### Multi-dimensional Sorting

```python
# 2D array sorting
matrix = np.array([[3, 1, 4],
                   [1, 5, 9],
                   [2, 6, 5]])

# Sort along different axes
sorted_rows = np.sort(matrix, axis=1)  # Sort each row
print(sorted_rows)
# [[1 3 4]
#  [1 5 9]
#  [2 5 6]]

sorted_cols = np.sort(matrix, axis=0)  # Sort each column
print(sorted_cols)
# [[1 1 4]
#  [2 5 5]
#  [3 6 9]]

# Flatten and sort
flat_sorted = np.sort(matrix, axis=None)
print(flat_sorted)  # [1 1 2 3 4 5 5 6 9]
```

### Argsort - Sorting by Indices

```python
# Get indices that would sort the array
arr = np.array([64, 34, 25, 12, 22, 11, 90])
indices = np.argsort(arr)
print(indices)  # [5 3 4 2 1 0 6]
print(arr[indices])  # [11 12 22 25 34 64 90] - sorted

# Sort multiple arrays based on one array's order
names = np.array(['Alice', 'Bob', 'Charlie', 'David'])
scores = np.array([85, 92, 78, 95])
indices = np.argsort(scores)[::-1]  # Descending order
print(names[indices])  # ['David' 'Bob' 'Alice' 'Charlie']
print(scores[indices])  # [95 92 85 78]

# Multi-level sorting (lexicographic)
data = np.array([(1, 3), (2, 2), (1, 1), (2, 1)],
                dtype=[('x', int), ('y', int)])
indices = np.lexsort((data['y'], data['x']))  # Sort by x, then y
print(data[indices])
```

### Partition - Partial Sorting for Top-K Problems

```python
# Find k smallest/largest elements efficiently
arr = np.array([64, 34, 25, 12, 22, 11, 90, 45, 33])

# Get 3 smallest elements (not fully sorted)
k = 3
partitioned = np.partition(arr, k-1)
print(partitioned[:k])  # [11 12 22] - three smallest (may not be sorted)

# Get indices of k smallest
indices = np.argpartition(arr, k-1)[:k]
top_k = arr[indices]
top_k.sort()  # Sort just the k elements
print(top_k)  # [11 12 22] - sorted

# Top 3 largest elements
k_largest_indices = np.argpartition(arr, -3)[-3:]
top_3 = arr[k_largest_indices]
top_3.sort()
print(top_3[::-1])  # [90 64 45] - descending

# Performance advantage: O(n + k log k) vs O(n log n)
# For k << n, this is much faster
```

### Performance Comparison

```python
import numpy as np
import time

# Large array benchmark
n = 1_000_000
arr = np.random.randint(0, 1000000, n)

# Full sort with argsort: O(n log n)
start = time.time()
indices = np.argsort(arr)[:100]  # Want 100 smallest
elapsed_argsort = time.time() - start

# Partition then sort: O(n + k log k)
start = time.time()
indices = np.argpartition(arr, 100)[:100]
smallest = arr[indices]
smallest.sort()
elapsed_partition = time.time() - start

print(f"argsort: {elapsed_argsort:.4f}s")
print(f"partition: {elapsed_partition:.4f}s")
# Partition is typically 5-10x faster for small k
```

### Structured Array Sorting

```python
# Sort complex records
employees = np.array([
    ('Alice', 25, 50000),
    ('Bob', 30, 60000),
    ('Charlie', 25, 55000),
    ('David', 30, 58000)
], dtype=[('name', 'U10'), ('age', int), ('salary', int)])

# Sort by single field
sorted_by_age = np.sort(employees, order='age')

# Multi-field sorting
sorted_emp = np.sort(employees, order=['age', 'salary'])
print(sorted_emp)
# Age 25: Alice ($50k), Charlie ($55k)
# Age 30: David ($58k), Bob ($60k)
```

## Best Use Cases

1. **Large numerical arrays**: NumPy excels with arrays of 10,000+ elements
2. **Integer arrays**: Automatic radix sort provides O(n) performance
3. **Top-K problems**: Use partition for finding k smallest/largest elements
4. **Multi-dimensional data**: Native support for axis-based sorting
5. **Scientific computing**: Integration with NumPy ecosystem (pandas, scikit-learn)
6. **Index-based sorting**: argsort for sorting related arrays together

## When NOT to Use

- **Small arrays** (<100 elements): Python list.sort() overhead is negligible
- **Mixed type data**: NumPy arrays are homogeneous, use Python lists
- **String sorting**: Python's native sort handles Unicode better
- **Custom comparison functions**: NumPy doesn't support cmp parameter

## Optimization Tips

```python
# Ensure C-contiguous arrays for best performance
arr = np.ascontiguousarray(arr)  # Convert if needed

# Use in-place sort to save memory
arr.sort()  # Better than arr = np.sort(arr)

# For integers, request stable sort to trigger radix sort
int_arr.sort(kind='stable')  # O(n) radix sort!

# Avoid unnecessary copies
# Bad: sorted_arr = np.sort(arr.copy())
# Good: sorted_arr = np.sort(arr)  # Already makes a copy

# Use partition for top-k instead of full sort
# Bad: top_100 = np.sort(arr)[:100]  # O(n log n)
# Good:
indices = np.argpartition(arr, 100)[:100]
top_100 = np.sort(arr[indices])  # O(n + 100 log 100)
```

## Integration with Pandas

```python
import pandas as pd
import numpy as np

# Pandas uses NumPy sorting under the hood
df = pd.DataFrame({
    'A': np.random.randint(0, 100, 1000),
    'B': np.random.randn(1000)
})

# These use NumPy's efficient sorting
df_sorted = df.sort_values('A')
df_sorted_multi = df.sort_values(['A', 'B'])

# Access underlying NumPy array for custom sorting
arr = df['A'].values
indices = np.argsort(arr)
df_custom = df.iloc[indices]
```

## Key Insights

1. **Radix sort advantage**: Integer arrays get O(n) sorting with kind='stable'
2. **Partition for top-k**: 5-10x faster than full sort for small k values
3. **Memory layout matters**: Contiguous arrays enable vectorization
4. **Type specialization**: NumPy optimizes for specific data types
5. **Integration**: Works seamlessly with pandas, scikit-learn, scipy

## Performance Benchmarks

Typical performance (1M elements):
- Python list.sort(): ~150ms
- np.sort() (quicksort): ~15ms (10x faster)
- np.sort(kind='stable') integers: ~8ms (O(n) radix sort)
- np.partition() for top-100: ~3ms (50x faster than full sort)

## References

- NumPy documentation: https://numpy.org/doc/stable/reference/generated/numpy.sort.html
- Sorting HOW TO: https://numpy.org/doc/stable/reference/routines.sort.html
