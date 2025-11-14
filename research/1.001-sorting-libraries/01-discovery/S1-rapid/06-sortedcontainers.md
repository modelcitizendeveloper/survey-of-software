# SortedContainers - Maintained Sorted Collections

## Overview

SortedContainers is a pure-Python library providing sorted list, sorted dict, and sorted set
data structures. Unlike one-time sorting, these containers maintain sorted order automatically
as elements are added or removed, making them ideal for applications requiring persistent
sorted state.

**Key insight**: When you need frequent lookups or insertions while maintaining sorted order,
sorted containers are more efficient than repeatedly sorting a list.

## Library Information

**Package**: sortedcontainers (pip install sortedcontainers)
**Author**: Grant Jenks
**License**: Apache 2.0
**Status**: Mature, actively maintained, widely used
**Performance**: Pure Python, often faster than C-extension alternatives (blist, bintrees)

**Adoption**: Used by popular projects including:
- Zipline (quantitative finance)
- Angr (binary analysis)
- Trio (async I/O)
- Dask Distributed

## Core Data Structures

### SortedList
- Maintains sorted list with efficient insertion/deletion
- O(log n) insertion, O(log n) deletion, O(log n) search
- O(1) access by index

### SortedDict
- Dictionary with keys maintained in sorted order
- O(log n) insertion/deletion
- Supports range queries and indexing

### SortedSet
- Set with elements maintained in sorted order
- O(log n) insertion/deletion/membership test
- Set operations (union, intersection) optimized

## Complexity Analysis

**Time Complexity**:

Operation | List | SortedList | Improvement
----------|------|------------|------------
Insert + maintain sort | O(n log n) | O(log n) | n factor
Delete + maintain sort | O(n) | O(log n) | n/log n factor
Search (binary) | O(log n) | O(log n) | Same
Index access | O(1) | O(1) | Same
Range query | O(n) | O(log n + k) | Much faster

**Space Complexity**: O(n) - same as regular list/dict/set

## Performance Characteristics

**Advantages over repeated sorting**:
- 10-1000x faster for incremental updates
- Efficient range queries
- Maintains invariants automatically

**vs. Regular list with sort()**:
- After each insert: O(n log n) vs O(log n)
- After 1000 inserts: O(1000 * n log n) vs O(1000 * log n)

**vs. blist (C extension)**:
- Often faster despite being pure Python
- No compilation needed
- Better documentation and maintenance

## Python Implementation

### SortedList Basics

```python
from sortedcontainers import SortedList

# Create sorted list
sl = SortedList([3, 1, 4, 1, 5, 9, 2, 6])
print(sl)  # SortedList([1, 1, 2, 3, 4, 5, 6, 9])

# Add elements (maintains sorted order automatically)
sl.add(7)
print(sl)  # SortedList([1, 1, 2, 3, 4, 5, 6, 7, 9])

# Add multiple elements efficiently
sl.update([0, 10, 5])
print(sl)  # SortedList([0, 1, 1, 2, 3, 4, 5, 5, 6, 7, 9, 10])

# Remove elements
sl.remove(5)  # Removes first occurrence
print(sl)  # SortedList([0, 1, 1, 2, 3, 4, 5, 6, 7, 9, 10])

# Discard (doesn't raise error if not found)
sl.discard(100)  # No error

# Pop elements
last = sl.pop()  # Remove and return last element
first = sl.pop(0)  # Remove and return first element

# Index access (O(1))
print(sl[0])  # First element
print(sl[-1])  # Last element
print(sl[2:5])  # Slicing works

# Binary search
index = sl.bisect_left(5)  # Find insertion point
index = sl.bisect_right(5)  # Find insertion point (after existing)

# Count occurrences
count = sl.count(1)  # Count how many 1's
```

### Advanced SortedList Operations

```python
from sortedcontainers import SortedList

# Custom key function
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __repr__(self):
        return f"Person({self.name}, {self.age})"

# Sort by age
people = SortedList(key=lambda p: p.age)
people.add(Person('Alice', 30))
people.add(Person('Bob', 25))
people.add(Person('Charlie', 35))
print(people)
# [Person(Bob, 25), Person(Alice, 30), Person(Charlie, 35)]

# Range queries (very efficient)
sl = SortedList(range(1000))

# Find all elements in range [100, 200)
start_idx = sl.bisect_left(100)
end_idx = sl.bisect_left(200)
elements_in_range = sl[start_idx:end_idx]

# IRange - iterate over range efficiently
for item in sl.irange(100, 200):  # Exclusive end
    process(item)

# IRange with min/max parameters
for item in sl.irange(minimum=100, maximum=200, inclusive=(True, False)):
    process(item)
```

### SortedDict Examples

```python
from sortedcontainers import SortedDict

# Create sorted dictionary (keys are sorted)
sd = SortedDict({'c': 3, 'a': 1, 'b': 2})
print(sd)  # SortedDict({'a': 1, 'b': 2, 'c': 3})

# Add items (maintains key order)
sd['d'] = 4
sd['aa'] = 1.5

# Iterate in sorted key order
for key, value in sd.items():
    print(f"{key}: {value}")

# Access by index
first_key = sd.keys()[0]  # 'a'
first_value = sd.values()[0]  # 1

# Range queries on keys
sd = SortedDict({i: i**2 for i in range(100)})

# Get all items with keys in range [25, 50)
start_idx = sd.bisect_left(25)
end_idx = sd.bisect_left(50)
range_items = {sd.keys()[i]: sd.values()[i]
               for i in range(start_idx, end_idx)}

# IRange on keys
for key in sd.irange(25, 50):
    print(f"{key}: {sd[key]}")
```

### SortedSet Examples

```python
from sortedcontainers import SortedSet

# Create sorted set
ss = SortedSet([3, 1, 4, 1, 5, 9, 2, 6])
print(ss)  # SortedSet([1, 2, 3, 4, 5, 6, 9])

# Set operations (all maintain sorted order)
ss1 = SortedSet([1, 2, 3, 4, 5])
ss2 = SortedSet([4, 5, 6, 7, 8])

union = ss1 | ss2  # SortedSet([1, 2, 3, 4, 5, 6, 7, 8])
intersection = ss1 & ss2  # SortedSet([4, 5])
difference = ss1 - ss2  # SortedSet([1, 2, 3])
symmetric_diff = ss1 ^ ss2  # SortedSet([1, 2, 3, 6, 7, 8])

# Range queries
ss = SortedSet(range(100))
subset = ss.irange(25, 50)  # Elements in [25, 50)

# Index access
print(ss[0])  # Smallest element
print(ss[-1])  # Largest element
```

## Use Case: Running Median

```python
from sortedcontainers import SortedList

class RunningMedian:
    """
    Efficiently maintain median of streaming data.
    O(log n) insertion vs O(n log n) with repeated sorting.
    """

    def __init__(self):
        self.sorted_data = SortedList()

    def add(self, num):
        """Add number and return current median. O(log n)"""
        self.sorted_data.add(num)
        return self.get_median()

    def get_median(self):
        """Get current median. O(1)"""
        n = len(self.sorted_data)
        if n == 0:
            return None

        if n % 2 == 1:
            return self.sorted_data[n // 2]
        else:
            return (self.sorted_data[n // 2 - 1] +
                    self.sorted_data[n // 2]) / 2


# Usage
rm = RunningMedian()
for num in [5, 2, 8, 1, 9]:
    median = rm.add(num)
    print(f"Added {num}, median: {median}")

# Much faster than sorting after each insertion
# 1000 insertions: O(1000 log 1000) vs O(1000 * 1000 log 1000)
```

## Use Case: Time-Series Data with Range Queries

```python
from sortedcontainers import SortedDict
from datetime import datetime, timedelta

class TimeSeries:
    """
    Store time-series data with efficient range queries.
    """

    def __init__(self):
        self.data = SortedDict()

    def add(self, timestamp, value):
        """Add data point. O(log n)"""
        self.data[timestamp] = value

    def get_range(self, start_time, end_time):
        """Get all data in time range. O(log n + k)"""
        result = []
        for timestamp in self.data.irange(start_time, end_time):
            result.append((timestamp, self.data[timestamp]))
        return result

    def get_latest(self, n=1):
        """Get n most recent data points. O(n)"""
        keys = list(self.data.keys())[-n:]
        return [(k, self.data[k]) for k in keys]


# Usage
ts = TimeSeries()

# Add data points
base_time = datetime.now()
for i in range(1000):
    timestamp = base_time + timedelta(seconds=i)
    ts.add(timestamp, i ** 2)

# Query range (very efficient)
start = base_time + timedelta(seconds=100)
end = base_time + timedelta(seconds=200)
range_data = ts.get_range(start, end)
print(f"Found {len(range_data)} points in range")

# Get latest 10 points
latest = ts.get_latest(10)
```

## Use Case: Event Scheduling

```python
from sortedcontainers import SortedList
from datetime import datetime, timedelta

class Event:
    def __init__(self, time, description):
        self.time = time
        self.description = description

    def __lt__(self, other):
        return self.time < other.time

    def __repr__(self):
        return f"Event({self.time}, {self.description})"


class EventScheduler:
    """
    Maintain sorted list of events with efficient insertion.
    """

    def __init__(self):
        self.events = SortedList()

    def schedule(self, time, description):
        """Schedule new event. O(log n)"""
        self.events.add(Event(time, description))

    def get_next_events(self, n=5):
        """Get next n events. O(n)"""
        return list(self.events[:n])

    def process_due_events(self, current_time):
        """Process all events up to current time. O(k log n)"""
        due = []
        while self.events and self.events[0].time <= current_time:
            due.append(self.events.pop(0))
        return due


# Usage
scheduler = EventScheduler()
base = datetime.now()

# Schedule events (not in order)
scheduler.schedule(base + timedelta(hours=2), "Meeting")
scheduler.schedule(base + timedelta(hours=1), "Email")
scheduler.schedule(base + timedelta(hours=3), "Call")
scheduler.schedule(base + timedelta(minutes=30), "Reminder")

# Get upcoming events (already sorted)
upcoming = scheduler.get_next_events(3)
for event in upcoming:
    print(event)
```

## Performance Comparison

```python
import time
from sortedcontainers import SortedList

def benchmark_incremental_updates(n=10000):
    """Compare list.sort() vs SortedList for incremental updates."""

    import random
    data = [random.randint(0, 100000) for _ in range(n)]

    # Approach 1: Regular list with repeated sorting
    start = time.time()
    regular_list = []
    for num in data:
        regular_list.append(num)
        regular_list.sort()  # O(n log n) every time
    time_regular = time.time() - start

    # Approach 2: SortedList
    start = time.time()
    sorted_list = SortedList()
    for num in data:
        sorted_list.add(num)  # O(log n) every time
    time_sorted = time.time() - start

    print(f"Regular list + sort: {time_regular:.3f}s")
    print(f"SortedList: {time_sorted:.3f}s")
    print(f"Speedup: {time_regular / time_sorted:.1f}x")

# Run benchmark
benchmark_incremental_updates(10000)
# Typical output:
# Regular list + sort: 8.234s
# SortedList: 0.045s
# Speedup: 183.0x
```

## Best Use Cases

1. **Streaming data with order**: Maintaining sorted state as data arrives
2. **Range queries**: Frequently querying elements in a range
3. **Running statistics**: Median, percentiles on streaming data
4. **Event systems**: Scheduling, priority queues with updates
5. **Time-series databases**: Timestamp-indexed data
6. **Leaderboards**: Gaming, rankings that update frequently
7. **Order books**: Financial trading systems

## When NOT to Use

- **One-time sorting**: Just use list.sort() or sorted()
- **No lookups needed**: If only sorting once then iterating
- **Memory constrained**: Slightly higher memory overhead than plain list
- **Ultra-high-performance**: C++ implementations may be faster for critical paths
- **Small datasets** (<100 elements): Overhead not justified

## Integration Patterns

```python
# Pattern 1: Replace list in existing code
# Before:
data = []
data.append(item)
data.sort()

# After:
from sortedcontainers import SortedList
data = SortedList()
data.add(item)  # Already sorted

# Pattern 2: Custom comparison
from sortedcontainers import SortedList

class Task:
    def __init__(self, priority, name):
        self.priority = priority
        self.name = name

# Sort by priority (lower number = higher priority)
tasks = SortedList(key=lambda t: t.priority)
tasks.add(Task(1, "Critical"))
tasks.add(Task(5, "Low priority"))
tasks.add(Task(2, "Important"))
# Automatically sorted by priority

# Pattern 3: Replace heapq for priority queue
# heapq is min-heap only, SortedList is more flexible
from sortedcontainers import SortedList

pq = SortedList()
pq.add((priority, item))  # Add with priority
highest_priority = pq.pop(0)  # Get highest (or lowest)
```

## Key Insights

1. **Pure Python advantage**: No compilation, cross-platform, easy to debug
2. **Incremental updates**: 10-1000x faster than repeated sorting
3. **Range query optimization**: O(log n + k) vs O(n) for unsorted
4. **Production ready**: Battle-tested in major projects
5. **API familiarity**: Similar to built-in list/dict/set

## Practical Recommendations

```python
# Decision tree: When to use SortedContainers

def should_use_sorted_containers(scenario):
    """Determine if sorted containers are appropriate."""

    if scenario['one_time_sort']:
        return "No - use list.sort()"

    if scenario['updates_per_second'] < 10:
        return "Maybe - benchmark both approaches"

    if scenario['range_queries']:
        return "Yes - sorted containers excel here"

    if scenario['size'] < 100:
        return "No - overhead not worth it"

    if scenario['maintain_sorted_order']:
        return "Yes - designed for this use case"

    return "Benchmark both approaches"
```

## References

- Documentation: https://grantjenks.com/docs/sortedcontainers/
- PyPI: https://pypi.org/project/sortedcontainers/
- Benchmarks: https://grantjenks.com/docs/sortedcontainers/performance.html
- Source: https://github.com/grantjenks/python-sortedcontainers
