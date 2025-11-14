# Memory-Efficient Sorting Techniques

## Overview

Memory-efficient sorting techniques minimize RAM usage while sorting large datasets. These approaches
are critical for systems with limited memory, large data processing, or when working with data
that exceeds available RAM.

## Approaches to Memory-Efficient Sorting

### 1. In-Place Sorting
### 2. Memory-Mapped Files
### 3. Streaming/Iterator-Based Sorting
### 4. Chunked Processing
### 5. External Sorting (covered in 05-external-sorting.md)

## In-Place Sorting Algorithms

In-place algorithms sort with O(1) or O(log n) extra space.

### Space Complexity Comparison

Algorithm | Space Complexity | In-Place?
----------|-----------------|----------
Quicksort | O(log n) | Yes (stack)
Heapsort | O(1) | Yes
Shell sort | O(1) | Yes
Insertion sort | O(1) | Yes
Timsort | O(n) | No
Merge sort | O(n) | No (standard)

### Python Implementation: In-Place Quicksort

```python
def quicksort_inplace(arr, low=0, high=None):
    """
    In-place quicksort using O(log n) stack space.

    Best for: Memory-constrained environments, large arrays.
    """
    if high is None:
        high = len(arr) - 1

    if low < high:
        # Partition and get pivot index
        pi = partition(arr, low, high)

        # Recursively sort left and right
        quicksort_inplace(arr, low, pi - 1)
        quicksort_inplace(arr, pi + 1, high)

    return arr


def partition(arr, low, high):
    """Partition array around pivot."""
    pivot = arr[high]
    i = low - 1

    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]

    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


# Example
import random
data = [random.randint(0, 1000) for _ in range(100000)]
quicksort_inplace(data)
# Uses minimal extra memory
```

### In-Place Heapsort

```python
def heapsort_inplace(arr):
    """
    In-place heapsort with O(1) extra space.

    Advantages:
    - Guaranteed O(n log n)
    - True O(1) space
    - No recursion overhead
    """
    def heapify(arr, n, i):
        """Heapify subtree rooted at index i."""
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2

        if left < n and arr[left] > arr[largest]:
            largest = left

        if right < n and arr[right] > arr[largest]:
            largest = right

        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            heapify(arr, n, largest)

    n = len(arr)

    # Build max heap
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)

    # Extract elements from heap
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        heapify(arr, i, 0)

    return arr


# Example
data = [12, 11, 13, 5, 6, 7]
heapsort_inplace(data)
print(data)  # [5, 6, 7, 11, 12, 13]
```

## Memory-Mapped File Sorting

Memory-mapped files allow working with data larger than RAM by mapping file contents to memory.

### Using mmap for Large Files

```python
import mmap
import struct
import os

def sort_large_binary_file_mmap(filename, record_size=4, format_char='i'):
    """
    Sort large binary file using memory mapping.

    Advantages:
    - OS handles memory management
    - Can work with files larger than RAM
    - Random access to data
    """
    file_size = os.path.getsize(filename)
    num_records = file_size // record_size

    # Open file with memory mapping
    with open(filename, 'r+b') as f:
        mm = mmap.mmap(f.fileno(), 0)

        # Read all records (OS pages in/out as needed)
        records = []
        for i in range(num_records):
            offset = i * record_size
            mm.seek(offset)
            value = struct.unpack(format_char, mm.read(record_size))[0]
            records.append((value, offset))

        # Sort by value
        records.sort(key=lambda x: x[0])

        # Write back in sorted order
        temp_data = bytearray(file_size)
        for i, (value, _) in enumerate(records):
            offset = i * record_size
            struct.pack_into(format_char, temp_data, offset, value)

        # Copy sorted data back
        mm.seek(0)
        mm.write(temp_data)
        mm.close()


# Example: Sort 1GB file of integers
def create_large_file(filename, num_records):
    """Create test file."""
    import random
    with open(filename, 'wb') as f:
        for _ in range(num_records):
            f.write(struct.pack('i', random.randint(0, 1_000_000)))

# Create 250M integers = 1GB file
# create_large_file('large.bin', 250_000_000)
# sort_large_binary_file_mmap('large.bin')
```

### Memory-Mapped NumPy Arrays

```python
import numpy as np

def sort_large_numpy_mmap(filename, dtype='int32'):
    """
    Sort large NumPy array using memory mapping.

    Most memory-efficient approach for numerical data.
    """
    # Open as memory-mapped array
    mm_array = np.memmap(filename, dtype=dtype, mode='r+')

    # NumPy's sort works on memory-mapped arrays!
    # Only active pages are in RAM
    mm_array.sort()

    # Changes are written back to file
    del mm_array  # Ensure write-back


# Create large memory-mapped array
def create_large_mmap_array(filename, size, dtype='int32'):
    """Create large array as memory-mapped file."""
    mm_array = np.memmap(filename, dtype=dtype, mode='w+', shape=(size,))
    mm_array[:] = np.random.randint(0, 1_000_000, size)
    del mm_array

# Example: Sort 2GB array (500M integers)
# create_large_mmap_array('large.npy', 500_000_000)
# sort_large_numpy_mmap('large.npy')
```

## Streaming/Iterator-Based Sorting

Process data in streams to avoid loading everything into memory.

### Generator-Based Sorting

```python
def merge_sorted_streams(*streams):
    """
    Merge multiple sorted streams with minimal memory.

    Memory usage: O(k) where k is number of streams.
    """
    import heapq

    # Create heap with first element from each stream
    heap = []
    for stream_idx, stream in enumerate(streams):
        try:
            first_item = next(stream)
            heapq.heappush(heap, (first_item, stream_idx, stream))
        except StopIteration:
            pass

    # Yield elements in sorted order
    while heap:
        value, stream_idx, stream = heapq.heappop(heap)
        yield value

        try:
            next_item = next(stream)
            heapq.heappush(heap, (next_item, stream_idx, stream))
        except StopIteration:
            pass


# Example: Merge sorted log files
def read_sorted_file(filename):
    """Generator that yields sorted values from file."""
    with open(filename) as f:
        for line in f:
            yield int(line.strip())

# Merge multiple sorted files with minimal memory
files = ['sorted1.txt', 'sorted2.txt', 'sorted3.txt']
streams = [read_sorted_file(f) for f in files]
merged = merge_sorted_streams(*streams)

# Process merged stream
for value in merged:
    process(value)  # Memory usage stays constant
```

### Chunked Processing with Limited Memory

```python
class ChunkedSorter:
    """
    Sort large dataset in chunks with memory limit.

    Combines chunking with external sort strategy.
    """

    def __init__(self, max_memory_mb=100):
        self.max_memory = max_memory_mb * 1024 * 1024

    def sort_large_file(self, input_file, output_file,
                        item_size_estimate=100):
        """
        Sort large file in chunks.

        Args:
            input_file: Input filename
            output_file: Output filename
            item_size_estimate: Estimated bytes per item
        """
        chunk_size = self.max_memory // item_size_estimate
        temp_files = []

        # Phase 1: Sort chunks
        with open(input_file) as f:
            chunk = []
            for line in f:
                chunk.append(line.strip())

                if len(chunk) >= chunk_size:
                    temp_file = self._write_sorted_chunk(chunk)
                    temp_files.append(temp_file)
                    chunk = []

            # Final chunk
            if chunk:
                temp_file = self._write_sorted_chunk(chunk)
                temp_files.append(temp_file)

        # Phase 2: Merge chunks
        self._merge_files(temp_files, output_file)

    def _write_sorted_chunk(self, chunk):
        """Sort chunk and write to temp file."""
        import tempfile
        chunk.sort()

        temp = tempfile.NamedTemporaryFile(mode='w', delete=False)
        for item in chunk:
            temp.write(f"{item}\n")
        temp.close()

        return temp.name

    def _merge_files(self, files, output_file):
        """Merge sorted files."""
        streams = [self._read_file(f) for f in files]
        merged = merge_sorted_streams(*streams)

        with open(output_file, 'w') as out:
            for item in merged:
                out.write(f"{item}\n")

        # Cleanup
        import os
        for f in files:
            os.remove(f)

    def _read_file(self, filename):
        """Generator to read file line by line."""
        with open(filename) as f:
            for line in f:
                yield line.strip()


# Example usage
sorter = ChunkedSorter(max_memory_mb=50)
sorter.sort_large_file('large_input.txt', 'sorted_output.txt')
```

## Partial Sorting for Memory Efficiency

When you only need top-k elements, partial sorting uses less memory.

### Top-K with Heap

```python
import heapq

def top_k_elements(iterable, k, key=None):
    """
    Find top k elements with O(k) memory.

    Much more efficient than sorting when k << n.
    """
    if key is None:
        return heapq.nlargest(k, iterable)
    return heapq.nlargest(k, iterable, key=key)


# Example: Find top 100 from 1 billion items
def large_dataset_generator():
    """Simulate large dataset."""
    import random
    for _ in range(1_000_000_000):
        yield random.randint(0, 1_000_000)

# Memory usage: ~800 bytes for heap (not 4GB for all data!)
top_100 = top_k_elements(large_dataset_generator(), 100)
```

### Streaming Median (Memory-Efficient)

```python
import heapq

class StreamingMedian:
    """
    Maintain median with O(1) memory per element.

    For very large streams, can sample instead.
    """

    def __init__(self):
        self.low = []  # Max heap (inverted)
        self.high = []  # Min heap

    def add(self, num):
        """Add number and rebalance heaps."""
        if not self.low or num <= -self.low[0]:
            heapq.heappush(self.low, -num)
        else:
            heapq.heappush(self.high, num)

        # Rebalance
        if len(self.low) > len(self.high) + 1:
            heapq.heappush(self.high, -heapq.heappop(self.low))
        elif len(self.high) > len(self.low):
            heapq.heappush(self.low, -heapq.heappop(self.high))

    def get_median(self):
        """Get current median."""
        if len(self.low) > len(self.high):
            return -self.low[0]
        return (-self.low[0] + self.high[0]) / 2


# Process billion records with constant memory
median_tracker = StreamingMedian()
for value in large_dataset_generator():
    median_tracker.add(value)
    if need_median_now():
        print(median_tracker.get_median())
```

## Memory Usage Comparison

```python
import sys

def compare_memory_usage():
    """Compare memory usage of different sorting approaches."""

    # Generate test data
    n = 1_000_000
    data = list(range(n, 0, -1))

    # Measure list + sort
    import copy
    data_copy = copy.copy(data)
    size_before = sys.getsizeof(data_copy)
    data_copy.sort()
    size_after = sys.getsizeof(data_copy)
    print(f"list.sort(): {size_before:,} bytes")

    # NumPy array (more compact)
    import numpy as np
    arr = np.array(data, dtype=np.int32)
    arr_size = arr.nbytes
    print(f"NumPy array: {arr_size:,} bytes")
    print(f"Memory savings: {size_before / arr_size:.1f}x")

    # Memory-mapped (minimal RAM usage)
    print(f"Memory-mapped: ~0 bytes (paged from disk)")


compare_memory_usage()
# Output:
# list.sort(): 8,000,056 bytes
# NumPy array: 4,000,000 bytes
# Memory savings: 2.0x
# Memory-mapped: ~0 bytes (paged from disk)
```

## Best Practices

### 1. Choose Right Data Structure

```python
# For large numerical data, use NumPy
import numpy as np
arr = np.array(data, dtype=np.int32)  # 4 bytes per int
# Not: list of ints (28 bytes per int in Python!)

# For very large data, use memory mapping
arr = np.memmap('data.npy', dtype='int32', mode='r+')
```

### 2. Use Generators for Pipelines

```python
# Bad: Load everything into memory
data = [process(line) for line in open('huge_file.txt')]
data.sort()

# Good: Use generators
def process_file(filename):
    with open(filename) as f:
        for line in f:
            yield process(line)

# Process in chunks or external sort
```

### 3. Leverage In-Place Operations

```python
# Bad: Creates copies
data = sorted(data)  # New list

# Good: In-place
data.sort()  # No extra memory

# For NumPy
arr.sort()  # In-place, O(1) extra space
```

## Key Insights

1. **Data structure matters**: NumPy arrays use 2-7x less memory than Python lists
2. **Memory mapping**: Enables sorting datasets larger than RAM
3. **In-place algorithms**: Heapsort, quicksort use O(1)-O(log n) space
4. **Streaming approach**: Constant memory for merge operations
5. **Partial sorting**: Top-k with heap uses O(k) instead of O(n)

## Practical Recommendations

```python
def choose_memory_efficient_sort(data_size_gb, available_ram_gb):
    """Recommend memory-efficient sorting strategy."""

    ratio = data_size_gb / available_ram_gb

    if ratio < 0.5:
        return "NumPy in-place sort (arr.sort())"

    if ratio < 1.5:
        return "Memory-mapped NumPy array"

    if ratio < 10:
        return "External merge sort"

    return "Distributed sort (Spark, Dask)"


# Examples
print(choose_memory_efficient_sort(2, 8))
# "NumPy in-place sort (arr.sort())"

print(choose_memory_efficient_sort(10, 4))
# "External merge sort"
```

## References

- NumPy memory mapping: https://numpy.org/doc/stable/reference/generated/numpy.memmap.html
- Python mmap: https://docs.python.org/3/library/mmap.html
- Heapq module: https://docs.python.org/3/library/heapq.html
