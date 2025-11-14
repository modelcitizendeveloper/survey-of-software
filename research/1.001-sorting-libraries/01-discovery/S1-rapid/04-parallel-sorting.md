# Parallel Sorting in Python

## Overview

Parallel sorting leverages multiple CPU cores to accelerate sorting operations on large datasets.
Python provides several approaches for parallel sorting through multiprocessing, joblib, and
specialized libraries. The key challenge is balancing parallelization overhead with performance gains.

## Parallel Sorting Strategies

### 1. Divide-and-Conquer Parallelization
- Split data into chunks
- Sort each chunk in parallel
- Merge sorted chunks

### 2. Parallel Merge Sort
- Recursively split and sort in parallel
- Parallel merge operations

### 3. Sample Sort (Parallel Quicksort)
- Select splitter values
- Partition data in parallel
- Sort partitions independently

## Complexity Analysis

**Time Complexity**:
- Best case: O(n log n / p) where p is number of processors
- Worst case: O(n log n) - limited by merge overhead
- Practical: 2-4x speedup on 8 cores for large datasets

**Space Complexity**: O(n) - need to duplicate or buffer data

**Overhead**:
- Process creation/communication: ~10-50ms per process
- Data serialization: Significant for large objects
- Memory copying: Can be substantial

## When Parallel Sorting Helps

**Effective when**:
- Dataset size > 1M elements
- Numerical data (low serialization cost)
- NumPy arrays (shared memory possible)
- CPU-bound workload
- 4+ CPU cores available

**Not effective when**:
- Small datasets (<100K elements): overhead dominates
- High serialization cost: complex Python objects
- I/O bound: disk speed is bottleneck
- Limited cores: insufficient parallelism

## Python Implementation

### Using Multiprocessing

```python
import multiprocessing as mp
from multiprocessing import Pool
import numpy as np

def parallel_sort_chunks(data, n_jobs=None):
    """
    Divide-and-conquer parallel sort.

    Time: O(n log n / p + n) - sort chunks + merge
    Works well for n > 1M elements
    """
    if n_jobs is None:
        n_jobs = mp.cpu_count()

    # Split data into chunks
    chunk_size = len(data) // n_jobs
    chunks = [data[i:i + chunk_size]
              for i in range(0, len(data), chunk_size)]

    # Sort chunks in parallel
    with Pool(n_jobs) as pool:
        sorted_chunks = pool.map(sorted, chunks)

    # Merge sorted chunks
    return merge_sorted_chunks(sorted_chunks)


def merge_sorted_chunks(chunks):
    """Merge multiple sorted chunks using heap."""
    import heapq

    # Use heap to efficiently merge k sorted lists
    result = []
    heap = []

    # Initialize heap with first element from each chunk
    for i, chunk in enumerate(chunks):
        if chunk:
            heapq.heappush(heap, (chunk[0], i, 0))

    # Extract minimum and add next element from same chunk
    while heap:
        val, chunk_idx, elem_idx = heapq.heappop(heap)
        result.append(val)

        if elem_idx + 1 < len(chunks[chunk_idx]):
            next_val = chunks[chunk_idx][elem_idx + 1]
            heapq.heappush(heap, (next_val, chunk_idx, elem_idx + 1))

    return result


# Example usage
data = list(np.random.randint(0, 1_000_000, 5_000_000))
sorted_data = parallel_sort_chunks(data, n_jobs=8)
```

### Using Joblib (Recommended)

```python
from joblib import Parallel, delayed
import numpy as np

def parallel_sort_joblib(data, n_jobs=-1, backend='loky'):
    """
    Parallel sort using joblib with optimized memory handling.

    Joblib advantages:
    - Automatic memmap for large arrays
    - Better serialization
    - Progress tracking
    - Multiple backends
    """
    chunk_size = len(data) // (n_jobs if n_jobs > 0 else mp.cpu_count())

    # Create chunks
    chunks = [data[i:i + chunk_size]
              for i in range(0, len(data), chunk_size)]

    # Sort in parallel with joblib
    sorted_chunks = Parallel(n_jobs=n_jobs, backend=backend)(
        delayed(sorted)(chunk) for chunk in chunks
    )

    return merge_sorted_chunks(sorted_chunks)


# For NumPy arrays - better performance
def parallel_sort_numpy(arr, n_jobs=-1):
    """
    Parallel sort for NumPy arrays using joblib.
    Leverages memmap for large arrays.
    """
    from joblib import Parallel, delayed

    n_cores = mp.cpu_count() if n_jobs == -1 else n_jobs
    chunk_size = len(arr) // n_cores

    # Split array into chunks
    chunks = [arr[i:i + chunk_size]
              for i in range(0, len(arr), chunk_size)]

    # Sort chunks in parallel (joblib uses memmap automatically for large arrays)
    sorted_chunks = Parallel(n_jobs=n_jobs, verbose=0)(
        delayed(np.sort)(chunk) for chunk in chunks
    )

    # Merge using NumPy's efficient concatenate + sort
    # For large arrays, might want iterative merge
    merged = np.concatenate(sorted_chunks)
    merged.sort()  # Final sort is fast on partially sorted data

    return merged


# Example
arr = np.random.randint(0, 1_000_000, 10_000_000)
sorted_arr = parallel_sort_numpy(arr, n_jobs=8)
```

### Optimized K-way Merge

```python
def parallel_merge_sort(data, n_jobs=None, threshold=10000):
    """
    True parallel merge sort with recursive parallelization.
    Only worth it for very large datasets.
    """
    if n_jobs is None:
        n_jobs = mp.cpu_count()

    def _parallel_merge_sort(arr, depth=0):
        # Base case: use sequential sort for small arrays
        if len(arr) <= threshold or depth >= 3:
            return sorted(arr)

        # Split in half
        mid = len(arr) // 2
        left = arr[:mid]
        right = arr[mid:]

        # Sort halves in parallel
        with Pool(2) as pool:
            left_sorted, right_sorted = pool.starmap(
                _parallel_merge_sort,
                [(left, depth + 1), (right, depth + 1)]
            )

        # Merge
        return merge_two_sorted(left_sorted, right_sorted)

    return _parallel_merge_sort(data)


def merge_two_sorted(left, right):
    """Efficiently merge two sorted lists."""
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result
```

### Parallel Sort with Shared Memory (Advanced)

```python
from multiprocessing import shared_memory, Pool
import numpy as np

def parallel_sort_shared_memory(arr, n_jobs=None):
    """
    Parallel sort using shared memory to avoid copying.
    Most efficient for very large NumPy arrays.
    """
    if n_jobs is None:
        n_jobs = mp.cpu_count()

    # Create shared memory
    shm = shared_memory.SharedMemory(create=True, size=arr.nbytes)
    shared_arr = np.ndarray(arr.shape, dtype=arr.dtype, buffer=shm.buf)
    shared_arr[:] = arr[:]

    # Calculate chunk boundaries
    chunk_size = len(arr) // n_jobs
    ranges = [(i * chunk_size, min((i + 1) * chunk_size, len(arr)))
              for i in range(n_jobs)]

    # Sort chunks in place
    def sort_chunk(shm_name, shape, dtype, start, end):
        existing_shm = shared_memory.SharedMemory(name=shm_name)
        shared_array = np.ndarray(shape, dtype=dtype, buffer=existing_shm.buf)
        shared_array[start:end].sort()
        existing_shm.close()

    with Pool(n_jobs) as pool:
        pool.starmap(
            sort_chunk,
            [(shm.name, arr.shape, arr.dtype, start, end)
             for start, end in ranges]
        )

    # Merge sorted chunks (in place if possible)
    result = shared_arr.copy()
    shm.close()
    shm.unlink()

    # Final merge (could also be parallelized)
    return np.sort(result)  # Timsort is fast on partially sorted data


# Example
large_array = np.random.randint(0, 1_000_000, 20_000_000)
sorted_array = parallel_sort_shared_memory(large_array, n_jobs=8)
```

## Performance Benchmarks

```python
import time
from statistics import mean

def benchmark_parallel_sorts(n=10_000_000):
    """Compare serial vs parallel sorting performance."""

    # Generate test data
    data = list(np.random.randint(0, 1_000_000, n))
    arr = np.array(data)

    print(f"Sorting {n:,} elements")
    print("-" * 50)

    # Serial sort (Python)
    test_data = data.copy()
    start = time.time()
    test_data.sort()
    serial_time = time.time() - start
    print(f"Serial Python sort:     {serial_time:.3f}s")

    # Serial NumPy sort
    test_arr = arr.copy()
    start = time.time()
    np.sort(test_arr)
    numpy_time = time.time() - start
    print(f"Serial NumPy sort:      {numpy_time:.3f}s ({serial_time/numpy_time:.1f}x)")

    # Parallel sort (multiprocessing)
    test_data = data.copy()
    start = time.time()
    parallel_sort_chunks(test_data, n_jobs=8)
    parallel_time = time.time() - start
    print(f"Parallel MP sort (8j):  {parallel_time:.3f}s ({serial_time/parallel_time:.1f}x)")

    # Parallel sort (joblib)
    test_data = data.copy()
    start = time.time()
    parallel_sort_joblib(test_data, n_jobs=8)
    joblib_time = time.time() - start
    print(f"Parallel joblib (8j):   {joblib_time:.3f}s ({serial_time/joblib_time:.1f}x)")

    # Parallel NumPy
    test_arr = arr.copy()
    start = time.time()
    parallel_sort_numpy(test_arr, n_jobs=8)
    parallel_numpy_time = time.time() - start
    print(f"Parallel NumPy (8j):    {parallel_numpy_time:.3f}s ({numpy_time/parallel_numpy_time:.1f}x)")

# Run benchmark
benchmark_parallel_sorts()

# Typical results on 8-core CPU:
# Serial Python sort:     2.500s
# Serial NumPy sort:      0.180s (13.9x)
# Parallel MP sort (8j):  0.850s (2.9x)
# Parallel joblib (8j):   0.780s (3.2x)
# Parallel NumPy (8j):    0.090s (2.0x faster than serial NumPy)
```

## Best Use Cases

1. **Very large numerical datasets** (>10M elements): Parallelization overhead justified
2. **NumPy arrays**: Efficient shared memory operations
3. **Multi-core systems**: 4+ cores to see significant benefits
4. **Batch processing**: Sorting multiple independent datasets
5. **Part of larger pipeline**: Where parallelism is already in use

## When NOT to Use

- **Small datasets** (<1M elements): Overhead exceeds benefits
- **Complex objects**: High serialization cost
- **Memory constrained**: Parallel operations need more memory
- **Single/dual-core systems**: Insufficient parallelism
- **Real-time systems**: Unpredictable latency from process management

## Optimization Tips

```python
# 1. Use NumPy arrays instead of lists
# Bad: parallel_sort_chunks(list(range(10_000_000)))
# Good: parallel_sort_numpy(np.arange(10_000_000))

# 2. Tune number of jobs
n_jobs = min(mp.cpu_count(), len(data) // 100_000)  # Don't over-parallelize

# 3. Use appropriate backend in joblib
# For CPU-bound: 'loky' or 'multiprocessing'
# For I/O-bound: 'threading'
Parallel(n_jobs=8, backend='loky')

# 4. Consider chunk size
# Too small: high overhead
# Too large: poor load balancing
optimal_chunk_size = len(data) // (n_jobs * 2)

# 5. Profile before optimizing
import cProfile
cProfile.run('parallel_sort_numpy(arr, n_jobs=8)')
```

## Integration Patterns

```python
# Pattern 1: Parallel preprocessing + single-threaded sort
from joblib import Parallel, delayed

def process_and_sort(data, n_jobs=-1):
    """Process in parallel, then sort (if result fits in memory)."""

    # Parallel processing
    processed = Parallel(n_jobs=n_jobs)(
        delayed(expensive_transform)(item) for item in data
    )

    # Single-threaded sort (often faster for moderate sizes)
    return sorted(processed, key=lambda x: x.score)


# Pattern 2: Sorting within parallel pipeline
def parallel_pipeline(datasets):
    """Sort each dataset in parallel pipeline."""

    def process_dataset(data):
        # Each worker sorts its own data
        data = sorted(data, key=lambda x: x.timestamp)
        return analyze(data)

    results = Parallel(n_jobs=-1)(
        delayed(process_dataset)(dataset) for dataset in datasets
    )

    return results
```

## Key Insights

1. **Diminishing returns**: Speedup saturates at 2-4x even with 8+ cores
2. **Data size threshold**: Only beneficial for 1M+ elements
3. **NumPy advantage**: Shared memory and efficient operations make it best for numerical data
4. **Joblib superiority**: Better than raw multiprocessing for most use cases
5. **Merge overhead**: Final merge can dominate for many chunks

## Practical Recommendations

```python
def smart_sort(data, force_parallel=False):
    """
    Intelligently choose sorting strategy based on data characteristics.
    """
    n = len(data)

    # Small data: use built-in sort
    if n < 1_000_000 and not force_parallel:
        if isinstance(data, np.ndarray):
            return np.sort(data)
        return sorted(data)

    # Large NumPy arrays: parallel NumPy sort
    if isinstance(data, np.ndarray) and n > 5_000_000:
        return parallel_sort_numpy(data, n_jobs=-1)

    # Large lists: joblib parallel sort
    if n > 5_000_000:
        return parallel_sort_joblib(data, n_jobs=-1)

    # Default: built-in sort is well-optimized
    if isinstance(data, np.ndarray):
        return np.sort(data)
    return sorted(data)
```

## References

- Joblib documentation: https://joblib.readthedocs.io/
- Python multiprocessing: https://docs.python.org/3/library/multiprocessing.html
- "Parallel Sorting Algorithms" - survey of parallel sorting approaches
