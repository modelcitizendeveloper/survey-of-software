# Radix Sort and Counting Sort

## Overview

Radix sort and counting sort are non-comparison-based sorting algorithms that achieve linear O(n)
time complexity under specific conditions. They work by exploiting the structure of integers or
fixed-range data, making them significantly faster than comparison-based sorts for appropriate
use cases.

**Key difference from comparison sorts**: These algorithms don't compare elements directly; instead,
they use the numeric properties of keys to determine position.

## Algorithm Descriptions

### Counting Sort

Counting sort works by:
1. Counting occurrences of each distinct value
2. Computing cumulative counts (positions)
3. Placing elements in output array based on counts

Best for: Small range of integer values (k ≈ n or k < n)

### Radix Sort

Radix sort works by:
1. Sorting elements digit by digit (or byte by byte)
2. Using a stable sort (typically counting sort) for each digit
3. Processing from least significant digit (LSD) to most significant digit (MSD)

Best for: Fixed-width integers, strings of similar length

## Complexity Analysis

### Counting Sort
**Time Complexity**: O(n + k) where k is the range of input values
**Space Complexity**: O(n + k) for count array and output array
**Stability**: Stable (preserves relative order)

### Radix Sort
**Time Complexity**: O(d(n + k)) where d is number of digits, k is base
- For integers with fixed bit width: O(n) effectively
- For b-bit numbers using base 2^b: O(n)

**Space Complexity**: O(n + k) for the underlying stable sort
**Stability**: Stable (requires stable subroutine)

## When They're Faster

**Counting sort wins when**:
- k (range) is small relative to n
- Data is integers in known range
- Example: Sorting 1M numbers between 0-1000

**Radix sort wins when**:
- Integers with limited digits/bits
- Fixed-length strings
- Example: Sorting 32-bit integers (O(n) vs O(n log n))

## Python Implementation

### Counting Sort

```python
def counting_sort(arr, max_val=None):
    """
    Counting sort for non-negative integers.

    Time: O(n + k), Space: O(n + k)
    k = max_val + 1
    """
    if not arr:
        return arr

    # Determine range
    if max_val is None:
        max_val = max(arr)

    # Count occurrences
    count = [0] * (max_val + 1)
    for num in arr:
        count[num] += 1

    # Compute cumulative counts
    for i in range(1, len(count)):
        count[i] += count[i - 1]

    # Build output array (stable)
    output = [0] * len(arr)
    for num in reversed(arr):  # Reverse to maintain stability
        output[count[num] - 1] = num
        count[num] -= 1

    return output


# Example usage
arr = [4, 2, 2, 8, 3, 3, 1]
sorted_arr = counting_sort(arr)
print(sorted_arr)  # [1, 2, 2, 3, 3, 4, 8]


# Optimized for small range
def counting_sort_inplace(arr, min_val, max_val):
    """In-place counting sort with known range."""
    k = max_val - min_val + 1
    count = [0] * k

    # Count frequencies
    for num in arr:
        count[num - min_val] += 1

    # Overwrite original array
    idx = 0
    for val in range(min_val, max_val + 1):
        arr[idx:idx + count[val - min_val]] = [val] * count[val - min_val]
        idx += count[val - min_val]

    return arr
```

### Radix Sort (LSD)

```python
def radix_sort(arr, base=10):
    """
    Radix sort for non-negative integers using LSD approach.

    Time: O(d(n + base)) where d is max number of digits
    Space: O(n + base)
    """
    if not arr:
        return arr

    # Find maximum number to determine number of digits
    max_num = max(arr)

    # Process each digit position
    exp = 1  # Current digit position (1, 10, 100, ...)
    while max_num // exp > 0:
        counting_sort_by_digit(arr, exp, base)
        exp *= base

    return arr


def counting_sort_by_digit(arr, exp, base):
    """Stable counting sort by specific digit position."""
    n = len(arr)
    output = [0] * n
    count = [0] * base

    # Count occurrences of digits
    for num in arr:
        digit = (num // exp) % base
        count[digit] += 1

    # Cumulative counts
    for i in range(1, base):
        count[i] += count[i - 1]

    # Build output array (reverse for stability)
    for i in range(n - 1, -1, -1):
        digit = (arr[i] // exp) % base
        output[count[digit] - 1] = arr[i]
        count[digit] -= 1

    # Copy back to original array
    for i in range(n):
        arr[i] = output[i]


# Example usage
arr = [170, 45, 75, 90, 802, 24, 2, 66]
radix_sort(arr)
print(arr)  # [2, 24, 45, 66, 75, 90, 170, 802]


# Optimized for specific bit widths
def radix_sort_binary(arr):
    """Radix sort using binary digits (base 2)."""
    if not arr:
        return arr

    max_num = max(arr)
    bit = 0

    while (1 << bit) <= max_num:
        # Stable partition by bit value
        zeros = [x for x in arr if not (x >> bit) & 1]
        ones = [x for x in arr if (x >> bit) & 1]
        arr[:] = zeros + ones
        bit += 1

    return arr
```

### Radix Sort for Strings

```python
def radix_sort_strings(strings, max_len=None):
    """
    Radix sort for fixed-length or similar-length strings.
    Sorts from rightmost character to leftmost (LSD).
    """
    if not strings:
        return strings

    # Determine maximum length
    if max_len is None:
        max_len = max(len(s) for s in strings)

    # Pad strings to same length
    strings = [s.ljust(max_len) for s in strings]

    # Sort by each character position (right to left)
    for pos in range(max_len - 1, -1, -1):
        # Counting sort by character at position pos
        buckets = [[] for _ in range(256)]  # ASCII range

        for s in strings:
            char_code = ord(s[pos])
            buckets[char_code].append(s)

        # Flatten buckets
        strings = [s for bucket in buckets for s in bucket]

    # Remove padding
    return [s.rstrip() for s in strings]


# Example
words = ['apple', 'application', 'apply', 'ape', 'apricot']
sorted_words = radix_sort_strings(words)
print(sorted_words)
```

## Performance Comparison

```python
import time
import random
from statistics import mean

def benchmark_sorts(n, k):
    """Compare counting sort, radix sort, and Python's sort."""

    # Generate data: n numbers in range [0, k)
    data = [random.randint(0, k-1) for _ in range(n)]

    # Python's Timsort
    test_data = data.copy()
    start = time.time()
    test_data.sort()
    timsort_time = time.time() - start

    # Counting sort
    test_data = data.copy()
    start = time.time()
    result = counting_sort(test_data, k-1)
    counting_time = time.time() - start

    # Radix sort
    test_data = data.copy()
    start = time.time()
    radix_sort(test_data)
    radix_time = time.time() - start

    print(f"n={n:,}, k={k:,}")
    print(f"  Timsort:      {timsort_time:.4f}s")
    print(f"  Counting sort: {counting_time:.4f}s ({timsort_time/counting_time:.1f}x)")
    print(f"  Radix sort:    {radix_time:.4f}s ({timsort_time/radix_time:.1f}x)")
    print()

# Best case for counting sort: k is small
benchmark_sorts(1_000_000, 1_000)

# Best case for radix sort: fixed-width integers
benchmark_sorts(1_000_000, 1_000_000_000)

# Worst case: k is very large
benchmark_sorts(100_000, 100_000_000)
```

## Best Use Cases

### Counting Sort

1. **Sorting small-range integers**: Ages (0-120), grades (0-100), ratings (1-5)
2. **Histogram computation**: Frequency analysis
3. **Subroutine for radix sort**: Stable digit sorting
4. **Known bounded data**: Port numbers, character codes

```python
# Example: Sort student grades (0-100)
grades = [85, 92, 78, 85, 95, 88, 92, 85]
sorted_grades = counting_sort(grades, max_val=100)
# O(n + 100) = O(n) time
```

### Radix Sort

1. **Fixed-width integers**: 32-bit or 64-bit integers, IP addresses
2. **Sorting strings**: Fixed-length codes, IDs, license plates
3. **Large datasets with small keys**: Millions of records with limited value range
4. **Lexicographic sorting**: Multi-field records with integer fields

```python
# Example: Sort 32-bit unsigned integers
import numpy as np

def radix_sort_numpy(arr):
    """Leverage NumPy for efficient radix sort."""
    # NumPy's stable sort uses radix sort for integers!
    return np.sort(arr, kind='stable')

# This is O(n) for integers
large_array = np.random.randint(0, 2**32, 1_000_000, dtype=np.uint32)
sorted_array = radix_sort_numpy(large_array)
```

## When NOT to Use

**Counting sort limitations**:
- Large range (k >> n): Memory explosion, slower than O(n log n)
- Floating-point numbers: Requires discretization
- Negative numbers: Needs offset adjustment
- Unknown range: Requires preprocessing

**Radix sort limitations**:
- Variable-length data: Padding overhead
- Non-integer keys: Requires key extraction
- Small datasets: Overhead not justified
- Complex comparison logic: Not applicable

## Integration with NumPy

```python
import numpy as np

# NumPy automatically uses radix sort for integers with stable sort!
arr = np.random.randint(0, 1_000_000, 1_000_000)

# This uses O(n) radix sort internally
sorted_arr = np.sort(arr, kind='stable')

# Verify it's fast
import time
start = time.time()
np.sort(arr, kind='stable')
stable_time = time.time() - start

start = time.time()
np.sort(arr, kind='quicksort')
quick_time = time.time() - start

print(f"Stable (radix): {stable_time:.4f}s")
print(f"Quicksort: {quick_time:.4f}s")
# Radix sort is typically 1.5-2x faster for integers
```

## Key Insights

1. **Linear time is achievable**: O(n) sorting exists for the right data types
2. **NumPy's secret weapon**: Automatic radix sort for integer arrays
3. **Range matters**: Counting sort only works when k is reasonable
4. **Stability is critical**: Radix sort requires stable subroutines
5. **Not general-purpose**: Limited to specific data types and ranges

## Practical Recommendations

```python
# Decision tree for sorting integers

def choose_sort(data, data_range=None):
    """Recommend sorting algorithm based on data characteristics."""
    n = len(data)

    if data_range is None:
        data_range = max(data) - min(data) + 1

    # Use counting sort if range is small
    if data_range <= 10 * n:
        return "counting_sort"

    # Use radix sort for fixed-width integers
    if all(isinstance(x, int) and x < 2**32 for x in data):
        return "radix_sort (or NumPy stable sort)"

    # Default to Timsort
    return "built-in sort()"

# Examples
print(choose_sort([1, 2, 3, 4, 5] * 1000))  # counting_sort
print(choose_sort(list(range(1_000_000))))  # radix_sort
print(choose_sort([random.random() for _ in range(1000)]))  # built-in sort()
```

## References

- "Introduction to Algorithms" (CLRS), Chapter 8: Counting Sort and Radix Sort
- NumPy sorting internals: Automatic radix sort for integers
- Open Data Structures, Section 11.2: Counting Sort and Radix Sort
