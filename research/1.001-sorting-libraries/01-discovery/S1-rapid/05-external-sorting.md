# External Sorting for Large Datasets

## Overview

External sorting algorithms handle datasets too large to fit in RAM by processing data in chunks
and using disk storage for intermediate results. These algorithms minimize I/O operations while
sorting data that may be gigabytes or terabytes in size.

**Core principle**: Break large data into memory-sized chunks, sort each chunk, write to disk,
then merge sorted chunks using minimal memory.

## Algorithm: External Merge Sort

External merge sort is the standard approach for sorting large files:

1. **Phase 1 - Run Creation**:
   - Read chunk of data that fits in memory (e.g., 100MB)
   - Sort chunk using efficient in-memory sort (Timsort)
   - Write sorted chunk (run) to temporary file
   - Repeat until entire file processed

2. **Phase 2 - K-way Merge**:
   - Open k sorted run files
   - Use min-heap to merge runs efficiently
   - Read one block from each run into memory
   - Write merged output to final file

## Complexity Analysis

**Time Complexity**:
- Phase 1 (run creation): O(n log n) - sorting chunks
- Phase 2 (merging): O(n log k) where k is number of runs
- Overall: O(n log n)

**Space Complexity**: O(M) where M is available memory
- Memory usage is bounded regardless of input size
- Typically use 90% of available RAM for buffers

**I/O Complexity**:
- Each record read/written exactly 2 times (read once, write once in each phase)
- Total I/O: 2n for run creation + 2n for merge = 4n
- Optimizations can reduce to ~3n

## Performance Characteristics

**Factors affecting performance**:
1. **Chunk size**: Larger chunks = fewer runs = faster merge
2. **Number of runs (k)**: More RAM allows larger k in k-way merge
3. **Disk I/O speed**: SSD vs HDD makes 10-100x difference
4. **Merge strategy**: k-way vs multi-pass merge
5. **Buffering**: Larger buffers reduce I/O overhead

**Typical performance**:
- Sorting 10GB file with 1GB RAM: 5-15 minutes on SSD
- Sorting 100GB file with 8GB RAM: 1-3 hours on SSD
- I/O is the bottleneck: ~70-90% of time spent on disk operations

## Python Implementation

### Basic External Merge Sort

```python
import heapq
import os
import tempfile
from typing import Iterator, List
import pickle

class ExternalSort:
    """
    External merge sort for large files that don't fit in memory.

    Features:
    - Configurable memory limit
    - Efficient k-way merge with heap
    - Automatic cleanup of temporary files
    """

    def __init__(self, max_memory_mb=100):
        self.max_memory = max_memory_mb * 1024 * 1024  # Convert to bytes
        self.temp_files = []

    def sort_file(self, input_file, output_file, key=None):
        """
        Sort large file using external merge sort.

        Args:
            input_file: Path to input file (one item per line)
            output_file: Path to output file
            key: Optional key function for sorting
        """
        # Phase 1: Create sorted runs
        self._create_sorted_runs(input_file, key)

        # Phase 2: Merge runs
        self._merge_runs(output_file, key)

        # Cleanup
        self._cleanup()

    def _create_sorted_runs(self, input_file, key=None):
        """Read chunks, sort, write to temp files."""
        chunk = []
        chunk_size = 0
        run_number = 0

        with open(input_file, 'r') as f:
            for line in f:
                line = line.rstrip('\n')
                line_size = len(line.encode('utf-8'))

                # Check if adding this line exceeds memory limit
                if chunk_size + line_size > self.max_memory and chunk:
                    # Write current chunk
                    self._write_sorted_chunk(chunk, run_number, key)
                    chunk = []
                    chunk_size = 0
                    run_number += 1

                chunk.append(line)
                chunk_size += line_size

            # Write final chunk
            if chunk:
                self._write_sorted_chunk(chunk, run_number, key)

    def _write_sorted_chunk(self, chunk, run_number, key=None):
        """Sort chunk and write to temporary file."""
        chunk.sort(key=key)

        temp_file = tempfile.NamedTemporaryFile(
            mode='w',
            delete=False,
            prefix=f'run_{run_number}_'
        )
        self.temp_files.append(temp_file.name)

        for item in chunk:
            temp_file.write(f"{item}\n")

        temp_file.close()

    def _merge_runs(self, output_file, key=None):
        """K-way merge of all sorted runs."""
        # Open all run files
        file_handles = [open(f, 'r') for f in self.temp_files]

        # Initialize heap with first line from each file
        heap = []
        for i, fh in enumerate(file_handles):
            line = fh.readline().rstrip('\n')
            if line:
                sort_key = key(line) if key else line
                heapq.heappush(heap, (sort_key, i, line))

        # Merge using heap
        with open(output_file, 'w') as out:
            while heap:
                sort_key, file_idx, line = heapq.heappop(heap)
                out.write(f"{line}\n")

                # Read next line from same file
                next_line = file_handles[file_idx].readline().rstrip('\n')
                if next_line:
                    next_key = key(next_line) if key else next_line
                    heapq.heappush(heap, (next_key, file_idx, next_line))

        # Close all files
        for fh in file_handles:
            fh.close()

    def _cleanup(self):
        """Remove temporary files."""
        for temp_file in self.temp_files:
            try:
                os.remove(temp_file)
            except OSError:
                pass
        self.temp_files = []


# Example usage
def example_basic():
    # Create large test file
    with open('large_data.txt', 'w') as f:
        for i in range(10_000_000, 0, -1):
            f.write(f"{i}\n")

    # Sort with 100MB memory limit
    sorter = ExternalSort(max_memory_mb=100)
    sorter.sort_file('large_data.txt', 'sorted_data.txt')

    # Verify first few lines
    with open('sorted_data.txt', 'r') as f:
        for i in range(10):
            print(f.readline().rstrip())
```

### Optimized External Sort for Binary Data

```python
import struct
import heapq
import tempfile
import os

class ExternalSortBinary:
    """
    Optimized external sort for binary numerical data.
    Much faster than text-based sorting due to:
    - Fixed record size
    - No parsing overhead
    - Efficient buffering
    """

    def __init__(self, max_memory_mb=100, record_format='i'):
        """
        Args:
            max_memory_mb: Memory limit in MB
            record_format: struct format ('i' for int, 'f' for float, etc.)
        """
        self.max_memory = max_memory_mb * 1024 * 1024
        self.record_format = record_format
        self.record_size = struct.calcsize(record_format)
        self.temp_files = []

    def sort_file(self, input_file, output_file):
        """Sort binary file of fixed-size records."""
        # Phase 1: Create sorted runs
        self._create_runs(input_file)

        # Phase 2: Merge runs
        self._merge_runs(output_file)

        # Cleanup
        self._cleanup()

    def _create_runs(self, input_file):
        """Create sorted runs from input file."""
        chunk_size = self.max_memory // self.record_size

        with open(input_file, 'rb') as f:
            run_number = 0

            while True:
                # Read chunk
                chunk_bytes = f.read(chunk_size * self.record_size)
                if not chunk_bytes:
                    break

                # Unpack to list
                n_records = len(chunk_bytes) // self.record_size
                chunk = list(struct.unpack(
                    f'{n_records}{self.record_format}',
                    chunk_bytes
                ))

                # Sort
                chunk.sort()

                # Write to temp file
                temp_file = tempfile.NamedTemporaryFile(
                    mode='wb',
                    delete=False,
                    prefix=f'run_{run_number}_'
                )
                self.temp_files.append(temp_file.name)

                # Pack and write
                packed = struct.pack(
                    f'{len(chunk)}{self.record_format}',
                    *chunk
                )
                temp_file.write(packed)
                temp_file.close()

                run_number += 1

    def _merge_runs(self, output_file):
        """K-way merge of binary runs."""
        # Open all runs
        file_handles = [open(f, 'rb') for f in self.temp_files]

        # Buffer size per file
        buffer_size = (self.max_memory // len(file_handles)) // self.record_size

        # Initialize heap
        heap = []
        buffers = [[] for _ in file_handles]

        # Fill initial buffers
        for i, fh in enumerate(file_handles):
            self._fill_buffer(fh, buffers[i], buffer_size)
            if buffers[i]:
                value = buffers[i].pop(0)
                heapq.heappush(heap, (value, i))

        # Merge
        with open(output_file, 'wb') as out:
            output_buffer = []

            while heap:
                value, file_idx = heapq.heappop(heap)
                output_buffer.append(value)

                # Flush output buffer if full
                if len(output_buffer) >= buffer_size:
                    self._flush_buffer(out, output_buffer)

                # Refill input buffer if needed
                if not buffers[file_idx]:
                    self._fill_buffer(
                        file_handles[file_idx],
                        buffers[file_idx],
                        buffer_size
                    )

                # Add next value from same file
                if buffers[file_idx]:
                    next_value = buffers[file_idx].pop(0)
                    heapq.heappush(heap, (next_value, file_idx))

            # Flush remaining output
            if output_buffer:
                self._flush_buffer(out, output_buffer)

        # Close files
        for fh in file_handles:
            fh.close()

    def _fill_buffer(self, file_handle, buffer, size):
        """Read records from file into buffer."""
        buffer.clear()
        chunk_bytes = file_handle.read(size * self.record_size)
        if chunk_bytes:
            n_records = len(chunk_bytes) // self.record_size
            buffer.extend(struct.unpack(
                f'{n_records}{self.record_format}',
                chunk_bytes
            ))

    def _flush_buffer(self, file_handle, buffer):
        """Write buffer to file and clear."""
        packed = struct.pack(
            f'{len(buffer)}{self.record_format}',
            *buffer
        )
        file_handle.write(packed)
        buffer.clear()

    def _cleanup(self):
        """Remove temporary files."""
        for temp_file in self.temp_files:
            try:
                os.remove(temp_file)
            except OSError:
                pass


# Example: Sort 1 billion integers (4GB file)
def example_binary():
    import random

    # Create large binary file
    print("Creating test file...")
    with open('large_numbers.bin', 'wb') as f:
        for _ in range(100_000_000):  # 100M integers = 400MB
            num = random.randint(0, 1_000_000_000)
            f.write(struct.pack('i', num))

    # Sort with 100MB memory
    print("Sorting...")
    import time
    start = time.time()

    sorter = ExternalSortBinary(max_memory_mb=100, record_format='i')
    sorter.sort_file('large_numbers.bin', 'sorted_numbers.bin')

    print(f"Sorted in {time.time() - start:.2f} seconds")

    # Verify
    with open('sorted_numbers.bin', 'rb') as f:
        for i in range(10):
            num = struct.unpack('i', f.read(4))[0]
            print(num)
```

### Using Python's heapq for External Sort

```python
import heapq
import csv
import tempfile
import os

def external_sort_csv(input_csv, output_csv, sort_column, max_memory_mb=100):
    """
    External sort for CSV files by specific column.

    Useful for log files, database dumps, etc.
    """
    max_rows = (max_memory_mb * 1024 * 1024) // 1000  # Rough estimate

    temp_files = []

    # Phase 1: Create sorted runs
    with open(input_csv, 'r', newline='') as f:
        reader = csv.DictReader(f)
        chunk = []

        for row in reader:
            chunk.append(row)

            if len(chunk) >= max_rows:
                # Sort chunk
                chunk.sort(key=lambda x: x[sort_column])

                # Write to temp file
                temp_file = tempfile.NamedTemporaryFile(
                    mode='w',
                    delete=False,
                    newline='',
                    suffix='.csv'
                )
                temp_files.append(temp_file.name)

                writer = csv.DictWriter(temp_file, fieldnames=reader.fieldnames)
                writer.writeheader()
                writer.writerows(chunk)
                temp_file.close()

                chunk = []

        # Write final chunk
        if chunk:
            chunk.sort(key=lambda x: x[sort_column])
            temp_file = tempfile.NamedTemporaryFile(
                mode='w',
                delete=False,
                newline='',
                suffix='.csv'
            )
            temp_files.append(temp_file.name)
            writer = csv.DictWriter(temp_file, fieldnames=reader.fieldnames)
            writer.writeheader()
            writer.writerows(chunk)
            temp_file.close()

    # Phase 2: K-way merge
    readers = [csv.DictReader(open(f, 'r', newline='')) for f in temp_files]
    with open(output_csv, 'w', newline='') as out:
        writer = csv.DictWriter(out, fieldnames=reader.fieldnames)
        writer.writeheader()

        # Initialize heap
        heap = []
        for i, r in enumerate(readers):
            try:
                row = next(r)
                heapq.heappush(heap, (row[sort_column], i, row))
            except StopIteration:
                pass

        # Merge
        while heap:
            _, i, row = heapq.heappop(heap)
            writer.writerow(row)

            try:
                next_row = next(readers[i])
                heapq.heappush(heap, (next_row[sort_column], i, next_row))
            except StopIteration:
                pass

    # Cleanup
    for f in temp_files:
        os.remove(f)
```

## Best Use Cases

1. **Log file sorting**: Multi-GB log files sorted by timestamp
2. **Database dumps**: Sorting large CSV/TSV exports
3. **Data preprocessing**: ETL pipelines with large intermediate files
4. **Batch processing**: Periodic sorting of accumulated data
5. **Limited memory environments**: Cloud instances with small RAM

**Example scenarios**:
- Sorting 50GB access logs on 4GB RAM machine
- Processing genomic data files (100GB+)
- Merging multiple large sorted files
- Preparing data for bulk database inserts (sorted input faster)

## When NOT to Use

- **Data fits in memory**: Use in-memory sort (10-100x faster)
- **Random access needed**: External sort requires sequential processing
- **Frequent updates**: External sort is batch-only
- **Real-time requirements**: Too slow for interactive applications
- **Distributed data**: Use distributed sorting (Spark, MapReduce)

## Optimization Strategies

```python
# 1. Maximize chunk size (use most of available RAM)
import psutil
available_mb = psutil.virtual_memory().available // (1024 * 1024)
chunk_size_mb = int(available_mb * 0.8)  # Use 80% of available

# 2. Use SSD for temporary files
import tempfile
tempfile.tempdir = '/path/to/ssd'  # Set to fast SSD

# 3. Optimize number of runs (larger chunks = fewer runs)
# Fewer runs = faster merge
# Formula: num_runs = ceil(file_size / chunk_size)

# 4. Use binary format when possible (10x faster than text)
# Bad: text CSV with parsing
# Good: binary struct format or pickle

# 5. Buffer I/O operations
# Use large read/write buffers (1-10MB)
with open('file', 'rb', buffering=10*1024*1024) as f:
    pass

# 6. Consider compression for I/O-bound scenarios
import gzip
# Compressed I/O can be faster if CPU > disk speed
```

## Key Insights

1. **I/O is the bottleneck**: 70-90% of time spent on disk operations
2. **SSD makes huge difference**: 10-100x faster than HDD for external sort
3. **Binary format advantage**: 5-10x faster than text parsing
4. **Chunk size critical**: Larger chunks = fewer runs = faster merge
5. **Memory management**: Use as much RAM as safely possible

## Practical Recommendations

```python
def choose_sorting_strategy(file_size_gb, available_ram_gb):
    """Recommend sorting strategy based on resources."""

    if file_size_gb <= available_ram_gb * 0.5:
        return "in_memory_sort"  # Load entire file into RAM

    if file_size_gb <= available_ram_gb * 2:
        return "memory_mapped_sort"  # Use mmap

    if file_size_gb > available_ram_gb * 10:
        return "distributed_sort"  # Consider Spark/Dask

    return "external_merge_sort"  # Classic external sort


# Example decisions
print(choose_sorting_strategy(file_size_gb=2, available_ram_gb=8))
# Output: "in_memory_sort"

print(choose_sorting_strategy(file_size_gb=50, available_ram_gb=4))
# Output: "external_merge_sort"
```

## References

- "Introduction to Algorithms" (CLRS), Chapter 8: External Sorting
- "Database System Concepts": External Sorting chapter
- Python tempfile module: https://docs.python.org/3/library/tempfile.html
- Python heapq module: https://docs.python.org/3/library/heapq.html
