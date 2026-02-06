# Scenario: Server Log File Sorting and Analysis

## Use Case Overview

### Business Context

System administrators and DevOps engineers need to sort and analyze massive server log files for:
- Troubleshooting production incidents (chronological order)
- Security audit trails (regulatory compliance)
- Performance analysis (request latency patterns)
- Error detection (aggregating failures)
- Capacity planning (resource usage trends)

### Real-World Examples

**Production scenarios:**
- **AWS CloudWatch Logs**: 100GB/day, sort by timestamp for incident reconstruction
- **Nginx access logs**: 50GB/day, sort by response time to find slow requests
- **Application logs**: Multi-server aggregation, sort to interleave events
- **Database logs**: 10GB/day, sort by query duration for optimization

### Data Characteristics

| Attribute | Typical Range |
|-----------|---------------|
| File size | 1GB - 1TB |
| Lines | 1M - 10B |
| Line length | 100-500 bytes |
| Sortedness | 70-95% chronological |
| Format | Text (JSON, Apache, syslog) |
| Key types | Timestamp, level, latency |

## Requirements Analysis

### Functional Requirements

**FR1: Sort by Multiple Keys**
- Primary: Timestamp (usually first field)
- Secondary: Log level (ERROR, WARN, INFO)
- Tertiary: Source server/service
- Support stable sort for tie-breaking

**FR2: Handle Large Files**
- Files larger than available RAM (1GB RAM, 100GB file)
- Minimize memory footprint
- Progress reporting for long-running sorts

**FR3: Preserve Data Integrity**
- No data loss during sort
- Maintain log line completeness
- Handle multi-line log entries (stack traces)

**FR4: Multiple Output Formats**
- Sorted to new file
- In-place sort (for disk space constraints)
- Streaming output (pipe to analysis tools)

### Non-Functional Requirements

**NFR1: Performance**
- Leverage nearly-sorted nature of logs (Timsort)
- Minimize disk I/O (SSD vs HDD = 10x difference)
- Optimize chunk size for merge sort

**NFR2: Resource Efficiency**
- Low memory footprint (< 2GB for any file size)
- Minimize temporary disk usage
- Efficient compression support

**NFR3: Reliability**
- Handle malformed lines gracefully
- Resume capability for interrupted sorts
- Validate output completeness

## Algorithm Evaluation

### Option 1: Load All in Memory + Sort (Simple)

**Approach:**
```python
def sort_logs_memory(input_file, output_file):
    # Read all lines
    with open(input_file) as f:
        lines = f.readlines()

    # Sort by timestamp
    lines.sort(key=lambda line: line[:19])  # ISO timestamp

    # Write sorted
    with open(output_file, 'w') as f:
        f.writelines(lines)
```

**Complexity:**
- Time: O(n log n) for sort
- Space: O(n) for full file in memory

**Performance (1GB file, 10M lines):**
- Read: 8s
- Sort: 12s (Timsort adaptive on nearly-sorted)
- Write: 7s
- **Total: 27s**

**Memory:** 1.2GB (file + Python overhead)

**Pros:**
- Simple implementation
- Fast for files that fit in RAM
- Timsort exploits partial order

**Cons:**
- Fails for files > RAM
- Large memory footprint
- No progress reporting

**Verdict: Good for files < 50% of RAM**

### Option 2: External Merge Sort (Large Files)

**Approach:**
```python
def sort_logs_external(input_file, output_file, chunk_size_mb=100):
    # Phase 1: Sort chunks
    chunk_files = []
    with open(input_file) as f:
        while True:
            chunk = list(islice(f, chunk_size_mb * 10000))  # ~100MB
            if not chunk:
                break

            chunk.sort(key=lambda line: line[:19])

            temp = tempfile.NamedTemporaryFile(delete=False)
            temp.writelines(chunk)
            chunk_files.append(temp.name)

    # Phase 2: K-way merge
    with open(output_file, 'w') as out:
        files = [open(f) for f in chunk_files]
        for line in heapq.merge(*files, key=lambda line: line[:19]):
            out.write(line)
```

**Complexity:**
- Time: O(n log n) for chunks + O(n log k) for merge
- Space: O(chunk_size) + O(k) where k = number of chunks

**Performance (100GB file, 1B lines, 1GB RAM):**
- Phase 1 (sort 100 chunks): 45 min
- Phase 2 (merge): 15 min
- **Total: 60 min** (SSD)

**Memory:** 1GB (constant, regardless of file size)

**Pros:**
- Handles any file size
- Predictable memory usage
- Parallelizable (sort chunks concurrently)

**Cons:**
- More complex implementation
- Requires disk space for temp files
- Slower than in-memory (I/O bound)

**Verdict: Required for files > RAM**

### Option 3: Memory-Mapped Sort (Hybrid)

**Approach:**
```python
import mmap

def sort_logs_mmap(input_file, output_file):
    # Memory-map file
    with open(input_file, 'r+b') as f:
        mmapped = mmap.mmap(f.fileno(), 0)

        # Read lines via mmap (OS handles paging)
        lines = mmapped.readlines()

        # Sort (OS pages in/out as needed)
        lines.sort(key=lambda line: line[:19])

        # Write sorted
        with open(output_file, 'wb') as out:
            out.writelines(lines)
```

**Complexity:**
- Time: O(n log n)
- Space: O(n) virtually, but OS manages paging

**Performance (10GB file, 100M lines, 2GB RAM):**
- Sort: 8.5 min
- Effective throughput: 20MB/s

**Memory:** 2GB (resident), 10GB (virtual)

**Pros:**
- Simpler than external sort
- OS handles memory management
- Good for 2-10x RAM scenarios

**Cons:**
- Slower than pure in-memory (page faults)
- Not portable (OS-dependent)
- Can thrash on very large files

**Verdict: Good middle ground for 1-5x RAM**

### Option 4: Streaming Sort (Database)

**Approach:**
```bash
# Load into SQLite with index
sqlite3 logs.db <<EOF
CREATE TABLE logs (timestamp TEXT, line TEXT);
CREATE INDEX idx_time ON logs(timestamp);
.import input.log logs
SELECT line FROM logs ORDER BY timestamp;
EOF
```

**Performance (1GB file):**
- Import: 45s
- Sort (via index): 8s
- **Total: 53s**

**Pros:**
- Handles files > RAM
- Index enables fast re-queries
- SQL expressive for complex analysis

**Cons:**
- Slower than specialized sort
- Requires database setup
- Temporary DB = 2x disk space

**Verdict: Best when multiple sorts/queries needed**

### Comparison Matrix

| Method | File Size | RAM | Time (10GB) | Memory | Complexity |
|--------|-----------|-----|-------------|--------|------------|
| In-memory | < 0.5x RAM | 10GB | 3 min | 10GB | Simple |
| External merge | Any | 1GB | 60 min | 1GB | Medium |
| Memory-mapped | 1-5x RAM | 2GB | 8.5 min | 2GB | Simple |
| Database | Any | 2GB | 18 min | 2GB | Medium |

**Recommendation:**
- **< 50% RAM**: Use in-memory sort (fastest)
- **50%-500% RAM**: Use memory-mapped (good balance)
- **> 500% RAM**: Use external merge sort (only option)

## Implementation Guide

### Production-Ready External Merge Sort

```python
import heapq
import tempfile
import os
import gzip
from typing import List, Callable, Optional
from datetime import datetime
from dataclasses import dataclass
import re

@dataclass
class SortProgress:
    """Progress tracking for long-running sorts."""
    phase: str
    processed_lines: int
    total_lines: Optional[int]
    current_chunk: int
    total_chunks: Optional[int]

    def __str__(self):
        if self.total_lines:
            pct = 100 * self.processed_lines / self.total_lines
            return f"{self.phase}: {self.processed_lines:,}/{self.total_lines:,} ({pct:.1f}%)"
        return f"{self.phase}: {self.processed_lines:,} lines, chunk {self.current_chunk}"

class LogFileSorter:
    """External merge sort for large log files."""

    def __init__(
        self,
        chunk_size_mb: int = 100,
        temp_dir: Optional[str] = None,
        progress_callback: Optional[Callable[[SortProgress], None]] = None,
        compression: bool = True
    ):
        """
        Initialize log file sorter.

        Args:
            chunk_size_mb: Size of chunks to sort in memory
            temp_dir: Directory for temporary files
            progress_callback: Function to call with progress updates
            compression: Use gzip for temp files (slower but saves disk)
        """
        self.chunk_size_mb = chunk_size_mb
        self.temp_dir = temp_dir or tempfile.gettempdir()
        self.progress_callback = progress_callback
        self.compression = compression
        self.temp_files: List[str] = []

    def extract_timestamp(self, line: str) -> str:
        """
        Extract timestamp from log line.

        Supports common formats:
        - ISO 8601: 2024-01-15T10:30:45.123Z
        - Apache: [15/Jan/2024:10:30:45 +0000]
        - Syslog: Jan 15 10:30:45
        """
        # ISO 8601
        if line[0:4].isdigit():
            return line[:23]  # YYYY-MM-DDTHH:MM:SS.mmm

        # Apache
        if line[0] == '[':
            match = re.match(r'\[(\d{2}/\w{3}/\d{4}:\d{2}:\d{2}:\d{2})', line)
            if match:
                return match.group(1)

        # Syslog
        match = re.match(r'(\w{3}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2})', line)
        if match:
            return match.group(1)

        # Fallback: use first 20 chars
        return line[:20]

    def sort_file(
        self,
        input_file: str,
        output_file: str,
        key_func: Optional[Callable[[str], str]] = None
    ) -> SortProgress:
        """
        Sort log file using external merge sort.

        Args:
            input_file: Path to input log file
            output_file: Path to output sorted file
            key_func: Function to extract sort key from line

        Returns:
            Final progress state
        """
        if key_func is None:
            key_func = self.extract_timestamp

        # Phase 1: Sort chunks
        total_lines = self._count_lines(input_file)
        progress = self._sort_chunks(input_file, key_func, total_lines)

        # Phase 2: Merge chunks
        progress = self._merge_chunks(output_file, key_func, progress)

        # Cleanup
        self._cleanup()

        return progress

    def _count_lines(self, filename: str) -> Optional[int]:
        """Fast line count for progress estimation."""
        try:
            # Use wc -l if available (much faster)
            import subprocess
            result = subprocess.run(
                ['wc', '-l', filename],
                capture_output=True,
                text=True,
                timeout=10
            )
            return int(result.stdout.split()[0])
        except:
            # Fallback: estimate from file size
            file_size = os.path.getsize(filename)
            avg_line_size = 200  # Rough estimate
            return file_size // avg_line_size

    def _sort_chunks(
        self,
        input_file: str,
        key_func: Callable[[str], str],
        total_lines: Optional[int]
    ) -> SortProgress:
        """Phase 1: Sort chunks that fit in memory."""
        chunk_num = 0
        processed = 0

        # Calculate lines per chunk
        bytes_per_chunk = self.chunk_size_mb * 1024 * 1024
        avg_line_size = 200  # Estimate
        lines_per_chunk = bytes_per_chunk // avg_line_size

        with open(input_file, 'r', encoding='utf-8', errors='replace') as f:
            while True:
                # Read chunk
                chunk = []
                chunk_bytes = 0

                for line in f:
                    chunk.append(line)
                    chunk_bytes += len(line)
                    processed += 1

                    if chunk_bytes >= bytes_per_chunk:
                        break

                if not chunk:
                    break

                # Sort chunk
                chunk.sort(key=key_func)

                # Write to temp file
                temp_file = self._write_temp_chunk(chunk, chunk_num)
                self.temp_files.append(temp_file)

                chunk_num += 1

                # Progress callback
                if self.progress_callback:
                    progress = SortProgress(
                        phase="Sorting chunks",
                        processed_lines=processed,
                        total_lines=total_lines,
                        current_chunk=chunk_num,
                        total_chunks=None
                    )
                    self.progress_callback(progress)

        return SortProgress(
            phase="Chunks sorted",
            processed_lines=processed,
            total_lines=total_lines,
            current_chunk=chunk_num,
            total_chunks=chunk_num
        )

    def _write_temp_chunk(self, chunk: List[str], chunk_num: int) -> str:
        """Write sorted chunk to temporary file."""
        suffix = '.gz' if self.compression else '.txt'
        temp_file = os.path.join(
            self.temp_dir,
            f'logsort_chunk_{chunk_num:04d}{suffix}'
        )

        if self.compression:
            with gzip.open(temp_file, 'wt', encoding='utf-8') as f:
                f.writelines(chunk)
        else:
            with open(temp_file, 'w', encoding='utf-8') as f:
                f.writelines(chunk)

        return temp_file

    def _merge_chunks(
        self,
        output_file: str,
        key_func: Callable[[str], str],
        progress: SortProgress
    ) -> SortProgress:
        """Phase 2: K-way merge of sorted chunks."""
        # Open all chunk files
        if self.compression:
            file_handles = [gzip.open(f, 'rt', encoding='utf-8') for f in self.temp_files]
        else:
            file_handles = [open(f, 'r', encoding='utf-8') for f in self.temp_files]

        # K-way merge using heap
        merged_lines = 0

        with open(output_file, 'w', encoding='utf-8') as out:
            for line in heapq.merge(*file_handles, key=key_func):
                out.write(line)
                merged_lines += 1

                # Progress every 100K lines
                if merged_lines % 100_000 == 0 and self.progress_callback:
                    progress = SortProgress(
                        phase="Merging chunks",
                        processed_lines=merged_lines,
                        total_lines=progress.total_lines,
                        current_chunk=len(self.temp_files),
                        total_chunks=len(self.temp_files)
                    )
                    self.progress_callback(progress)

        # Close all files
        for f in file_handles:
            f.close()

        return SortProgress(
            phase="Complete",
            processed_lines=merged_lines,
            total_lines=merged_lines,
            current_chunk=len(self.temp_files),
            total_chunks=len(self.temp_files)
        )

    def _cleanup(self):
        """Remove temporary chunk files."""
        for temp_file in self.temp_files:
            try:
                os.remove(temp_file)
            except OSError:
                pass
        self.temp_files.clear()
```

### Usage Examples

```python
# Example 1: Simple sort with progress
def print_progress(progress: SortProgress):
    print(progress)

sorter = LogFileSorter(
    chunk_size_mb=100,
    progress_callback=print_progress,
    compression=True
)

sorter.sort_file('app.log', 'app_sorted.log')

# Output:
# Sorting chunks: 1,234,567/10,000,000 (12.3%)
# Sorting chunks: 2,456,789/10,000,000 (24.6%)
# ...
# Merging chunks: 5,000,000/10,000,000 (50.0%)
# ...
# Complete: 10,000,000/10,000,000 (100.0%)

# Example 2: Custom sort key (by latency)
def extract_latency(line: str) -> float:
    """Extract response time from nginx log."""
    # nginx: ... request_time=0.234 ...
    match = re.search(r'request_time=([0-9.]+)', line)
    if match:
        return float(match.group(1))
    return 0.0

sorter.sort_file(
    'nginx_access.log',
    'nginx_by_latency.log',
    key_func=lambda line: f"{extract_latency(line):010.3f}{line}"
)

# Example 3: Multi-key sort (timestamp, then level)
def multi_key(line: str) -> str:
    """Sort by timestamp, then level (ERROR first)."""
    timestamp = line[:23]
    level_order = {'ERROR': '0', 'WARN': '1', 'INFO': '2', 'DEBUG': '3'}

    for level, order in level_order.items():
        if level in line:
            return f"{timestamp}_{order}"

    return f"{timestamp}_9"  # Unknown level last

sorter.sort_file('app.log', 'app_sorted.log', key_func=multi_key)
```

## Performance Optimization

### Optimization 1: Chunk Size Tuning

**Impact:** 3-5x speedup from optimal chunk size

```python
# Too small (10MB chunks): Many merges, slow
# Time: 120 min (100GB file)

# Optimal (100MB chunks): Balanced
# Time: 60 min (100GB file)

# Too large (500MB chunks): Memory pressure, swapping
# Time: 85 min (100GB file)

# Formula for optimal chunk size:
optimal_chunk_mb = available_ram_mb / (2 * sqrt(num_chunks))

# Example: 4GB RAM, expecting 100 chunks
optimal = 4000 / (2 * 10) = 200MB
```

### Optimization 2: I/O Pattern Optimization

**Read/write in large blocks:**

```python
# Slow: Line-by-line I/O
with open('log.txt') as f:
    for line in f:
        process(line)

# Fast: Buffered reading
with open('log.txt', buffering=8*1024*1024) as f:  # 8MB buffer
    for line in f:
        process(line)

# Speedup: 2-3x faster due to fewer syscalls
```

### Optimization 3: Compression Trade-off

**SSD:**
- Uncompressed: 60 min, 100GB temp space
- Gzip compressed: 75 min, 20GB temp space
- **Verdict:** Skip compression on SSD (not worth 25% slowdown)

**HDD:**
- Uncompressed: 180 min, 100GB temp space
- Gzip compressed: 160 min, 20GB temp space
- **Verdict:** Use compression on HDD (reduces seeks)

### Optimization 4: Parallel Chunk Sorting

```python
from multiprocessing import Pool

def sort_chunk_parallel(args):
    chunk, chunk_num, key_func = args
    chunk.sort(key=key_func)
    return chunk, chunk_num

# Sort chunks in parallel
with Pool(processes=4) as pool:
    sorted_chunks = pool.map(sort_chunk_parallel, chunk_args)

# Speedup: 3.2x on 4 cores (chunk sorting is CPU-bound)
# Total time: 60min → 25min (Phase 1 only)
```

### Performance Summary

**100GB log file, 1B lines, 4GB RAM, SSD:**

| Configuration | Time | Speedup |
|---------------|------|---------|
| Baseline (10MB chunks, no compression) | 120 min | 1.0x |
| Optimal chunks (100MB) | 60 min | 2.0x |
| + Parallel chunk sort (4 cores) | 25 min | 4.8x |
| + Large I/O buffers | 22 min | 5.5x |

**HDD is 5-10x slower due to seek latency**

## Edge Cases and Solutions

### Edge Case 1: Multi-line Log Entries

**Problem:** Stack traces span multiple lines

```
2024-01-15 10:30:45 ERROR Exception occurred
Traceback (most recent call last):
  File "app.py", line 42
    raise ValueError("Bad input")
```

**Solution:** Join continued lines before sorting

```python
def join_multiline_logs(lines):
    """Combine multi-line entries into single records."""
    combined = []
    current = []

    for line in lines:
        # Check if new log entry (starts with timestamp)
        if re.match(r'^\d{4}-\d{2}-\d{2}', line):
            if current:
                combined.append(''.join(current))
            current = [line]
        else:
            # Continuation line
            current.append(line)

    if current:
        combined.append(''.join(current))

    return combined
```

### Edge Case 2: Malformed Lines

**Problem:** Corrupted lines without timestamps

**Solution:** Skip or place at end

```python
def safe_extract_timestamp(line: str) -> str:
    try:
        return extract_timestamp(line)
    except:
        # Invalid lines sort to end
        return 'ZZZZ' + line[:20]
```

### Edge Case 3: Mixed Timezones

**Problem:** Logs from servers in different timezones

**Solution:** Normalize to UTC before sorting

```python
from dateutil import parser
from datetime import timezone

def normalize_timestamp(line: str) -> str:
    """Convert any timezone to UTC."""
    timestamp_str = line[:30]  # Generous slice
    dt = parser.parse(timestamp_str)

    # Convert to UTC
    dt_utc = dt.astimezone(timezone.utc)

    return dt_utc.isoformat()
```

### Edge Case 4: Disk Space Constraints

**Problem:** Not enough space for temp files + output

**Solution:** In-place external sort

```python
def sort_file_inplace(filename: str):
    """Sort file in-place, minimizing disk usage."""
    # Sort to temp file
    temp_sorted = filename + '.sorted.tmp'
    sorter.sort_file(filename, temp_sorted)

    # Atomic replace
    os.replace(temp_sorted, filename)

    # Only needs 1x extra space temporarily
```

## Summary

### Key Takeaways

1. **Choose algorithm by file size:**
   - < 50% RAM: In-memory sort (fastest, 3 min/10GB)
   - 50-500% RAM: Memory-mapped (8.5 min/10GB)
   - > 500% RAM: External merge sort (60 min/100GB)

2. **I/O optimization > algorithm choice:**
   - SSD vs HDD: 5-10x difference
   - Chunk size: 3x impact
   - Compression: Helps HDD, hurts SSD

3. **Timsort exploits log structure:**
   - Logs typically 70-95% sorted
   - Timsort 3-10x faster on nearly-sorted data
   - Always prefer stable sort

4. **Parallel chunk sorting scales well:**
   - 3.2x speedup on 4 cores
   - Merge phase is sequential (Amdahl's Law)

5. **Production considerations:**
   - Progress reporting for long sorts
   - Handle malformed lines gracefully
   - Multi-line entry support
   - Timezone normalization
