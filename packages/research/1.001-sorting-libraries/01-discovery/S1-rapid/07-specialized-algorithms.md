# Specialized Sorting Algorithms

## Overview

Beyond general-purpose sorting algorithms, several specialized sorting techniques excel in specific
scenarios. These algorithms leverage domain-specific properties to achieve better performance than
O(n log n) comparison-based sorts or provide unique capabilities.

## Bucket Sort

### Description

Bucket sort distributes elements into buckets, sorts each bucket individually, then concatenates.
Works best when input is uniformly distributed over a range.

### Algorithm

1. Create n buckets for value ranges
2. Distribute elements into buckets
3. Sort each bucket (any algorithm)
4. Concatenate buckets in order

### Complexity

**Time**: O(n + k) average case, O(n²) worst case
**Space**: O(n + k) where k is number of buckets
**Stability**: Depends on bucket sorting algorithm

### Python Implementation

```python
def bucket_sort(arr, num_buckets=10):
    """
    Bucket sort for uniformly distributed data.

    Best for: floats in [0, 1), uniformly distributed integers
    """
    if not arr:
        return arr

    # Determine range
    min_val, max_val = min(arr), max(arr)
    bucket_range = (max_val - min_val) / num_buckets

    # Create buckets
    buckets = [[] for _ in range(num_buckets)]

    # Distribute elements
    for num in arr:
        if num == max_val:
            buckets[-1].append(num)
        else:
            bucket_idx = int((num - min_val) / bucket_range)
            buckets[bucket_idx].append(num)

    # Sort each bucket and concatenate
    sorted_arr = []
    for bucket in buckets:
        sorted_arr.extend(sorted(bucket))  # Use any sort

    return sorted_arr


# Example: Sort floats in [0, 1)
import random
data = [random.random() for _ in range(10000)]
sorted_data = bucket_sort(data, num_buckets=100)

# O(n) when data is uniformly distributed
```

### Use Cases

- Sorting floats in known range (0-1, 0-100)
- Uniformly distributed test scores
- Hash table implementations
- Image processing (pixel values 0-255)

## Shell Sort

### Description

Shell sort is an optimization of insertion sort that allows exchange of far-apart elements.
It uses a gap sequence to compare elements at increasing distances.

### Algorithm

1. Start with large gap (e.g., n/2)
2. Perform gapped insertion sort
3. Reduce gap (e.g., gap = gap/2)
4. Repeat until gap = 1

### Complexity

**Time**: O(n log n) to O(n^(3/2)) depending on gap sequence
**Space**: O(1) - in-place
**Stability**: Unstable

### Python Implementation

```python
def shell_sort(arr):
    """
    Shell sort with Knuth's gap sequence: h = 3h + 1.

    Better than insertion sort, worse than quicksort.
    Useful when: simple code needed, small to medium data.
    """
    n = len(arr)

    # Determine starting gap (Knuth's sequence)
    gap = 1
    while gap < n // 3:
        gap = gap * 3 + 1

    # Perform gapped insertion sorts
    while gap > 0:
        for i in range(gap, n):
            temp = arr[i]
            j = i

            # Gapped insertion sort
            while j >= gap and arr[j - gap] > temp:
                arr[j] = arr[j - gap]
                j -= gap

            arr[j] = temp

        gap //= 3  # Next gap in sequence

    return arr


# Example
import random
data = [random.randint(0, 1000) for _ in range(1000)]
shell_sort(data)

# Faster than insertion sort, simpler than quicksort
```

### Gap Sequences

```python
# Different gap sequences affect performance

def shell_sort_sedgewick(arr):
    """Shell sort with Sedgewick's gap sequence."""
    # Sedgewick gaps: 1, 5, 19, 41, 109, 209, 505, 929, ...
    gaps = [1]
    k = 1
    while True:
        gap = 9 * (2**k - 2**(k//2)) + 1 if k % 2 else 8 * 2**k - 6 * 2**(k//2) + 1
        if gap >= len(arr):
            break
        gaps.append(gap)
        k += 1

    # Sort with each gap (largest to smallest)
    for gap in reversed(gaps):
        for i in range(gap, len(arr)):
            temp = arr[i]
            j = i
            while j >= gap and arr[j - gap] > temp:
                arr[j] = arr[j - gap]
                j -= gap
            arr[j] = temp

    return arr


# Knuth sequence: better average performance
# Sedgewick sequence: better worst-case performance
```

### Use Cases

- Embedded systems (simple, low memory)
- Small to medium datasets (< 10K elements)
- Partially sorted data
- When code simplicity matters

## Bitonic Sort

### Description

Bitonic sort is a comparison-based parallel sorting algorithm that works well on GPU/parallel
architectures. It builds a bitonic sequence then sorts it.

### Complexity

**Time**: O(log² n) parallel time, O(n log² n) work
**Space**: O(n)
**Parallelism**: Highly parallelizable

### Python Implementation

```python
def bitonic_sort(arr, ascending=True):
    """
    Bitonic sort - good for parallel execution.

    Note: Array length must be power of 2.
    """
    def bitonic_merge(arr, low, cnt, ascending):
        if cnt > 1:
            k = cnt // 2
            for i in range(low, low + k):
                if (arr[i] > arr[i + k]) == ascending:
                    arr[i], arr[i + k] = arr[i + k], arr[i]
            bitonic_merge(arr, low, k, ascending)
            bitonic_merge(arr, low + k, k, ascending)

    def bitonic_sort_recursive(arr, low, cnt, ascending):
        if cnt > 1:
            k = cnt // 2
            bitonic_sort_recursive(arr, low, k, True)
            bitonic_sort_recursive(arr, low + k, k, False)
            bitonic_merge(arr, low, cnt, ascending)

    # Pad to power of 2 if necessary
    n = len(arr)
    next_power = 1
    while next_power < n:
        next_power *= 2

    arr.extend([float('inf')] * (next_power - n))

    bitonic_sort_recursive(arr, 0, next_power, ascending)

    # Remove padding
    return arr[:n]


# Best used with parallel execution framework
from concurrent.futures import ThreadPoolExecutor

def parallel_bitonic_sort(arr):
    """Parallelize bitonic sort operations."""
    # Implementation would use ThreadPoolExecutor for comparisons
    # Most beneficial on GPU with libraries like CuPy
    return bitonic_sort(arr)
```

### Use Cases

- GPU sorting (CUDA, OpenCL)
- Hardware implementations (FPGA)
- Parallel architectures
- Fixed-size power-of-2 datasets

## Cycle Sort

### Description

Cycle sort minimizes the number of writes to memory, making it useful for situations where
writes are expensive (flash memory, distributed systems).

### Complexity

**Time**: O(n²)
**Space**: O(1)
**Writes**: Minimal - at most n writes

### Python Implementation

```python
def cycle_sort(arr):
    """
    Cycle sort - minimizes writes to memory.

    Use when: writes are expensive (SSD wear, network)
    """
    writes = 0

    # Iterate through array to find cycles
    for cycle_start in range(len(arr) - 1):
        item = arr[cycle_start]

        # Find position to put item
        pos = cycle_start
        for i in range(cycle_start + 1, len(arr)):
            if arr[i] < item:
                pos += 1

        # If item already in correct position
        if pos == cycle_start:
            continue

        # Skip duplicates
        while item == arr[pos]:
            pos += 1

        # Put item in correct position
        arr[pos], item = item, arr[pos]
        writes += 1

        # Rotate rest of cycle
        while pos != cycle_start:
            pos = cycle_start
            for i in range(cycle_start + 1, len(arr)):
                if arr[i] < item:
                    pos += 1

            while item == arr[pos]:
                pos += 1

            arr[pos], item = item, arr[pos]
            writes += 1

    return arr, writes


# Example
data = [5, 2, 8, 1, 9, 3, 7]
sorted_data, num_writes = cycle_sort(data)
print(f"Sorted with only {num_writes} writes")
# Sorted with only 6 writes (optimal)
```

### Use Cases

- Flash memory (minimize write cycles)
- EEPROM storage
- Network-based storage (expensive writes)
- Educational purposes (understanding permutations)

## Pancake Sort

### Description

Pancake sort sorts using only "flip" operations (reversing prefix of array). Mainly theoretical
but has practical applications in genome rearrangement.

### Complexity

**Time**: O(n²)
**Space**: O(1)
**Flips**: At most 2n - 3

### Python Implementation

```python
def pancake_sort(arr):
    """
    Pancake sort - sorts using only reversals.

    Interesting property: sorts using at most 2n-3 reversals.
    """
    def flip(arr, k):
        """Reverse first k elements."""
        arr[:k] = reversed(arr[:k])

    def find_max_index(arr, n):
        """Find index of maximum in first n elements."""
        max_idx = 0
        for i in range(n):
            if arr[i] > arr[max_idx]:
                max_idx = i
        return max_idx

    n = len(arr)
    for curr_size in range(n, 1, -1):
        # Find index of maximum in unsorted part
        max_idx = find_max_index(arr, curr_size)

        # Move maximum to end if not already there
        if max_idx != curr_size - 1:
            # Flip to bring maximum to front
            flip(arr, max_idx + 1)
            # Flip to bring maximum to current end
            flip(arr, curr_size)

    return arr


# Example
data = [3, 6, 2, 8, 1, 5]
pancake_sort(data)
print(data)  # [1, 2, 3, 5, 6, 8]
```

### Use Cases

- Genome rearrangement problems
- Algorithm education
- Robotics (sorting with limited operations)
- Puzzle solving

## Comparison of Specialized Algorithms

```python
import time
import random

def benchmark_specialized_sorts(n=1000):
    """Compare specialized sorting algorithms."""

    # Generate different data types
    uniform_data = [random.random() for _ in range(n)]
    random_ints = [random.randint(0, n) for _ in range(n)]

    print(f"Benchmarking with n={n}")
    print("-" * 50)

    # Bucket sort (uniform data)
    data = uniform_data.copy()
    start = time.time()
    bucket_sort(data)
    print(f"Bucket sort (uniform):  {(time.time() - start)*1000:.2f}ms")

    # Shell sort
    data = random_ints.copy()
    start = time.time()
    shell_sort(data)
    print(f"Shell sort:             {(time.time() - start)*1000:.2f}ms")

    # Python's built-in (for comparison)
    data = random_ints.copy()
    start = time.time()
    data.sort()
    print(f"Built-in sort:          {(time.time() - start)*1000:.2f}ms")

benchmark_specialized_sorts(10000)
```

## Decision Matrix

```python
def choose_specialized_sort(data_properties):
    """
    Recommend specialized sorting algorithm based on data properties.
    """
    # Uniform distribution in known range
    if data_properties['uniform_distribution']:
        return "bucket_sort"

    # Minimize writes
    if data_properties['expensive_writes']:
        return "cycle_sort"

    # GPU/parallel hardware
    if data_properties['parallel_hardware']:
        return "bitonic_sort"

    # Simple code, small data
    if data_properties['simplicity_priority'] and data_properties['size'] < 10000:
        return "shell_sort"

    # Limited operations (only reversals)
    if data_properties['reversal_only']:
        return "pancake_sort"

    # Default recommendation
    return "timsort (built-in)"


# Examples
print(choose_specialized_sort({
    'uniform_distribution': True,
    'expensive_writes': False,
    'parallel_hardware': False,
    'simplicity_priority': False,
    'size': 100000,
    'reversal_only': False
}))  # "bucket_sort"
```

## Key Insights

1. **Domain-specific advantage**: Specialized sorts win in narrow domains
2. **Trade-offs**: Often sacrifice generality for specific performance
3. **Simplicity value**: Shell sort still useful for simple embedded systems
4. **Write optimization**: Cycle sort's minimal writes matter for flash/network
5. **Parallel potential**: Bitonic sort shines on GPU, not CPU

## Practical Recommendations

**Use bucket sort when**:
- Data uniformly distributed in known range
- Working with floats in [0, 1)
- Histogram-style problems

**Use shell sort when**:
- Need simple O(n log n)-ish sort
- Code size/complexity matters
- Small to medium datasets

**Use cycle sort when**:
- Minimizing writes is critical
- Flash memory or EEPROM
- Network storage

**Use bitonic sort when**:
- GPU implementation available
- Data size is power of 2
- Parallel hardware

**Avoid these when**:
- General-purpose sorting needed → Use Timsort
- Large datasets → Use NumPy or external sort
- Need stability → Use merge sort or Timsort

## References

- "The Art of Computer Programming Vol 3: Sorting and Searching" - Knuth
- "Introduction to Algorithms" (CLRS) - Various sorting algorithms
- Shell sort gap sequences: https://oeis.org/A003586 (Knuth), A036562 (Sedgewick)
