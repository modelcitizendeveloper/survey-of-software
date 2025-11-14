# Antipatterns and Pitfalls: Common Sorting Mistakes and How to Fix Them

## Executive Summary

Sorting performance problems rarely stem from choosing "the wrong algorithm" - they usually result from structural mistakes like sorting unnecessarily, using the wrong data structure, or optimizing prematurely. This document catalogs common antipatterns with real-world examples and practical fixes, organized by severity and frequency.

**Critical insight**: 90% of sorting performance issues are solved by avoiding sorting, not by optimizing it.

---

## Part 1: The Seven Deadly Sins of Sorting

### Sin 1: Sorting When You Don't Need To

**Antipattern**: Sort data just to extract extremes
```python
# ❌ WRONG: Sort entire list to get top 10
data = fetch_data()  # 1 million items
sorted_data = sorted(data, reverse=True)
top_10 = sorted_data[:10]

# Time complexity: O(n log n)
# For n=1M: ~20 million operations

# ✅ RIGHT: Use heap to find top 10
import heapq
top_10 = heapq.nlargest(10, data)

# Time complexity: O(n log k) where k=10
# For n=1M: ~1 million operations (20x faster)
```

**Why it happens**: Developers default to "sort then slice" pattern

**Real-world impact**:
- API endpoint that returns top 100 products (sorted 100K products)
- Reduced latency: 500ms → 25ms (20x improvement)
- Implementation time: 5 minutes (change 1 line)

**Detection**: Search codebase for `sorted(...)[:n]` or `sort()` followed by slice

**Variations**:
```python
# ❌ Finding minimum/maximum by sorting
min_val = sorted(data)[0]  # O(n log n)
max_val = sorted(data, reverse=True)[0]  # O(n log n)

# ✅ Use built-in functions
min_val = min(data)  # O(n)
max_val = max(data)  # O(n)

# ❌ Checking if element exists (sorted then search)
sorted_data = sorted(data)
exists = target in sorted_data  # Still O(n) for list membership

# ✅ Use set
data_set = set(data)  # O(n) once
exists = target in data_set  # O(1)
```

**Fix decision tree**:
- Need top K elements? → `heapq.nlargest()` or `heapq.nsmallest()`
- Need min/max? → `min()` or `max()`
- Need median? → `statistics.median()` (uses quickselect, not full sort)
- Need to check membership? → Convert to `set`
- Actually need sorted data? → Then sort

### Sin 2: Repeated Sorting of Same Data

**Antipattern**: Re-sort on every insertion/update
```python
# ❌ WRONG: Re-sort after every addition
leaderboard = []
for score in incoming_scores:
    leaderboard.append(score)
    leaderboard.sort(reverse=True)  # O(n log n) every iteration!

# Total complexity: O(n² log n)
# For n=10,000: ~1.3 billion operations
```

**Why it happens**:
- Incremental programming (add feature by feature)
- Not thinking about data structure invariants

**Real-world example**:
- Gaming leaderboard: 10K scores, 100 updates/second
- Before: 100 × O(10K log 10K) = ~13M operations/second → 500ms CPU
- After: 100 × O(log 10K) = ~1,300 operations/second → 0.05ms CPU
- **10,000x improvement**

**Fix**: Use sorted container
```python
# ✅ RIGHT: Maintain sorted order
from sortedcontainers import SortedList

leaderboard = SortedList()
for score in incoming_scores:
    leaderboard.add(score)  # O(log n) insertion

# Total complexity: O(n log n)
# For n=10,000: ~130,000 operations (10,000x better)
```

**Alternative fixes**:
```python
# If using NumPy (numerical data)
import numpy as np
scores = np.array(incoming_scores)
sorted_indices = np.argsort(scores)  # Sort once at end

# If using pandas
import pandas as pd
df = pd.DataFrame({'score': incoming_scores})
df = df.sort_values('score')  # Sort once at end

# If using database
# Let database maintain sorted index
# SELECT * FROM leaderboard ORDER BY score DESC LIMIT 100
```

**When to sort repeatedly** (rare cases):
- Data changes completely each time (no incremental update possible)
- Sorting cost is negligible (< 100 items)
- Simplicity matters more than performance

### Sin 3: Wrong Data Structure for Access Pattern

**Antipattern**: Using list when you need sorted, searchable collection
```python
# ❌ WRONG: List + repeated sorting + binary search
class ProductCatalog:
    def __init__(self):
        self.products = []

    def add_product(self, product):
        self.products.append(product)
        self.products.sort(key=lambda p: p.price)  # O(n log n)

    def find_in_price_range(self, min_price, max_price):
        # Binary search for range
        import bisect
        # ... complex binary search logic ...
        # Still need to keep list sorted
```

**Why it happens**:
- Learning Python with basic data structures (list, dict)
- Not knowing about SortedContainers, pandas, databases

**Fix 1**: Use SortedContainers
```python
# ✅ BETTER: SortedList with key function
from sortedcontainers import SortedKeyList

class ProductCatalog:
    def __init__(self):
        self.products = SortedKeyList(key=lambda p: p.price)

    def add_product(self, product):
        self.products.add(product)  # O(log n)

    def find_in_price_range(self, min_price, max_price):
        # Built-in range query
        start_idx = self.products.bisect_key_left(min_price)
        end_idx = self.products.bisect_key_right(max_price)
        return self.products[start_idx:end_idx]  # O(log n + k)
```

**Fix 2**: Use pandas (if data is tabular)
```python
# ✅ BETTER: pandas DataFrame with index
import pandas as pd

class ProductCatalog:
    def __init__(self):
        self.df = pd.DataFrame(columns=['id', 'name', 'price'])
        self.df = self.df.set_index('price').sort_index()

    def add_product(self, product):
        new_row = pd.DataFrame([product], index=[product.price])
        self.df = pd.concat([self.df, new_row]).sort_index()

    def find_in_price_range(self, min_price, max_price):
        return self.df.loc[min_price:max_price]  # O(log n + k)
```

**Fix 3**: Use database (best for large datasets)
```python
# ✅ BEST: SQLite with indexed column
import sqlite3

class ProductCatalog:
    def __init__(self):
        self.conn = sqlite3.connect(':memory:')
        self.conn.execute('''
            CREATE TABLE products (
                id INTEGER PRIMARY KEY,
                name TEXT,
                price REAL
            )
        ''')
        self.conn.execute('CREATE INDEX idx_price ON products(price)')

    def add_product(self, product):
        self.conn.execute(
            'INSERT INTO products (id, name, price) VALUES (?, ?, ?)',
            (product.id, product.name, product.price)
        )

    def find_in_price_range(self, min_price, max_price):
        cursor = self.conn.execute(
            'SELECT * FROM products WHERE price BETWEEN ? AND ?',
            (min_price, max_price)
        )
        return cursor.fetchall()  # O(log n + k) with index
```

**Decision matrix**:
- < 1,000 items: SortedContainers
- 1,000-100,000 items: SortedContainers or pandas
- > 100,000 items: Database (SQLite, DuckDB)
- Need persistence: Database
- Need complex queries: Database

### Sin 4: Sorting by Multiple Keys Inefficiently

**Antipattern**: Multiple passes of sorting
```python
# ❌ WRONG: Sort multiple times
data.sort(key=lambda x: x.name)
data.sort(key=lambda x: x.age)
data.sort(key=lambda x: x.score, reverse=True)

# Confusion: Which sort order wins? (Last one!)
# Performance: 3 × O(n log n) instead of 1 × O(n log n)
```

**Why it happens**:
- Misunderstanding stable sort
- Trying to sort by priority (thinking last sort is secondary)

**Fix**: Single sort with tuple key
```python
# ✅ RIGHT: Single sort with tuple
data.sort(key=lambda x: (-x.score, x.age, x.name))

# Sorts by:
# 1. Score (descending, note the negative)
# 2. Age (ascending, if score tied)
# 3. Name (ascending, if score and age tied)

# Performance: 1 × O(n log n)
# Complexity: Simple, clear intent
```

**Common mistake**: Forgetting sort stability
```python
# ❌ WRONG: Thinking this works
data.sort(key=lambda x: x.name)  # Secondary sort
data.sort(key=lambda x: x.score, reverse=True)  # Primary sort
# This works ONLY if x.score is stable sort (it is in Python)
# But confusing and error-prone

# ✅ RIGHT: Explicit tuple (clearer intent)
data.sort(key=lambda x: (-x.score, x.name))
```

**Pandas equivalent**:
```python
# ✅ Sort by multiple columns
df.sort_values(['score', 'age', 'name'],
               ascending=[False, True, True])
```

### Sin 5: Sorting Large Objects Instead of Indices

**Antipattern**: Moving large objects during sort
```python
# ❌ WRONG: Sorting large objects directly
class LargeObject:
    def __init__(self, id, score, data):
        self.id = id
        self.score = score
        self.data = data  # 1 MB of data each

objects = [LargeObject(...) for _ in range(100000)]
sorted_objects = sorted(objects, key=lambda x: x.score)

# Problem: Moving 1 MB objects during sort is slow
# Each swap copies 1 MB
# Total data moved: ~100 GB (100K objects × ~1 MB × log n swaps)
```

**Why it happens**: Not thinking about memory access patterns

**Fix 1**: Sort indices, not objects (indirect sort)
```python
# ✅ RIGHT: Sort indices
objects = [LargeObject(...) for _ in range(100000)]
indices = list(range(len(objects)))
indices.sort(key=lambda i: objects[i].score)

# Access in sorted order
for i in indices:
    process(objects[i])

# Data moved during sort: ~100K integers × 8 bytes × log n = ~10 MB
# 10,000x less data movement
```

**Fix 2**: Extract keys, sort with argsort
```python
# ✅ RIGHT: NumPy argsort (if numerical)
import numpy as np

scores = np.array([obj.score for obj in objects])
sorted_indices = np.argsort(scores)

for i in sorted_indices:
    process(objects[i])
```

**Fix 3**: Use pandas with large objects
```python
# ✅ RIGHT: Pandas sorts indices internally
df = pd.DataFrame({
    'score': [obj.score for obj in objects],
    'object': objects  # Store reference, not copy
})
df_sorted = df.sort_values('score')

for obj in df_sorted['object']:
    process(obj)
```

**When it matters**:
- Object size > 100 bytes: Consider indirect sort
- Object size > 1 KB: Definitely use indirect sort
- Object size < 50 bytes: Direct sort is fine (cache-friendly)

### Sin 6: Premature Optimization (Custom Sort Implementation)

**Antipattern**: Implementing custom sorting algorithm
```python
# ❌ WRONG: Custom quicksort implementation
def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort(left) + middle + quicksort(right)

data = [...]
sorted_data = quicksort(data)

# Problems:
# 1. Slower than built-in (Timsort is optimized C code)
# 2. Not stable (quicksort isn't stable)
# 3. Worst-case O(n²) for sorted input
# 4. Uses O(n) extra space (list comprehensions create copies)
# 5. Maintenance burden (bugs, edge cases)
```

**Benchmarks**:
```python
import timeit
import random

data = [random.randint(0, 10000) for _ in range(10000)]

# Custom quicksort: ~45ms
time_custom = timeit.timeit(lambda: quicksort(data.copy()), number=100)

# Built-in sort: ~8ms
time_builtin = timeit.timeit(lambda: sorted(data), number=100)

# Built-in is 5.6x faster (and more reliable)
```

**Why it happens**:
- Educational: Learned algorithms in class, wants to use them
- Misguided optimization: "I can make it faster"
- Not knowing built-in is highly optimized

**Fix**: Use built-in sort
```python
# ✅ RIGHT: Just use built-in
sorted_data = sorted(data)

# Or for in-place:
data.sort()
```

**Only implement custom sort if**:
1. Built-in doesn't support your use case (extremely rare)
2. You've profiled and proven built-in is bottleneck
3. You have domain knowledge (e.g., know data is always nearly sorted)
4. You're working on a sorting library (NumPy, pandas)

**Better optimizations**:
- Use NumPy for numerical data (10x faster than built-in)
- Use SortedContainers for incremental updates
- Avoid sorting entirely (use heap, set, dict)

### Sin 7: Ignoring Stability When It Matters

**Antipattern**: Using unstable sort when order matters
```python
# ❌ WRONG: Unstable sort loses original order
transactions = [
    {'user': 'Alice', 'amount': 100, 'timestamp': 1},
    {'user': 'Bob', 'amount': 100, 'timestamp': 2},
    {'user': 'Alice', 'amount': 100, 'timestamp': 3},
]

# Some sorts are unstable (heapsort, quicksort in C++)
# Python's sort is stable, but NumPy's quicksort is not:
import numpy as np
indices = np.argsort([t['amount'] for t in transactions], kind='quicksort')
# Result: Alice-1, Alice-3, Bob-2 (timestamp order lost!)
# Expected: Alice-1, Bob-2, Alice-3 (preserve timestamp order)
```

**Why it matters**:
- Multi-key sorting: Stable sort preserves secondary order
- UI consistency: Same input → same output order
- Testing: Reproducible results

**Fix**: Ensure stable sort
```python
# ✅ RIGHT: Use stable sort
# Python's built-in is always stable:
transactions.sort(key=lambda t: t['amount'])

# NumPy: Specify kind='stable' or 'mergesort'
indices = np.argsort([t['amount'] for t in transactions], kind='stable')

# Pandas: sort is stable by default
df.sort_values('amount')  # Stable
```

**Stability comparison**:
- **Python list.sort()**: Always stable ✓
- **NumPy sort()**: Default depends on version (use `kind='stable'`)
- **Pandas sort_values()**: Always stable ✓
- **C++ std::sort()**: Unstable ✗ (use std::stable_sort)
- **Java Arrays.sort()**: Stable for objects, unstable for primitives
- **Rust slice.sort()**: Stable ✓

**When stability doesn't matter**:
- Single key sort
- Unique values (no ties)
- Don't care about tie-breaking order

**When stability is critical**:
- Multi-stage sorting
- UI display (user expectations)
- Compliance/audit requirements

---

## Part 2: Performance Antipatterns

### Antipattern 2.1: Sorting in a Loop

**Bad code**:
```python
# ❌ WRONG: Sort inside loop
results = []
for category in categories:
    items = fetch_items(category)  # 1000 items
    items.sort(key=lambda x: x.price)
    results.append(items[:10])

# If 100 categories: 100 × O(1000 log 1000) = ~1M operations
```

**Fix**: Batch sorting
```python
# ✅ RIGHT: Collect all, sort once
all_items = []
for category in categories:
    items = fetch_items(category)
    all_items.extend(items)

all_items.sort(key=lambda x: (x.category, x.price))
# Group by category after sorting
from itertools import groupby
results = {cat: list(items)[:10]
           for cat, items in groupby(all_items, key=lambda x: x.category)}

# 1 × O(100K log 100K) = ~1.7M operations
# But: Only if categories don't matter for display order
```

**Better fix**: Don't sort at all
```python
# ✅ BEST: Get top 10 per category without full sort
import heapq

results = []
for category in categories:
    items = fetch_items(category)
    top_10 = heapq.nsmallest(10, items, key=lambda x: x.price)
    results.append(top_10)

# 100 × O(1000 × log 10) = ~230K operations (4x better)
```

### Antipattern 2.2: Converting to List Just to Sort

**Bad code**:
```python
# ❌ WRONG: Convert NumPy array to list
import numpy as np

data = np.random.randint(0, 1000, size=1000000)
sorted_data = sorted(data.tolist())  # Convert to list: slow!

# Problems:
# 1. data.tolist() copies 1M integers: ~30ms
# 2. sorted() uses Python comparison: ~150ms
# Total: ~180ms
```

**Fix**: Use NumPy's sort
```python
# ✅ RIGHT: Sort in NumPy
sorted_data = np.sort(data)  # ~8ms (20x faster)

# Or in-place:
data.sort()  # Even faster (no copy)
```

**Similar mistakes**:
```python
# ❌ Converting pandas to list
df['column'].tolist().sort()

# ✅ Use pandas
df.sort_values('column')

# ❌ Converting set to list just to sort
sorted_list = sorted(list(my_set))

# ✅ Direct conversion
sorted_list = sorted(my_set)  # Works on any iterable
```

### Antipattern 2.3: Sorting When Database Can Do It

**Bad code**:
```python
# ❌ WRONG: Fetch all, sort in Python
import sqlite3

conn = sqlite3.connect('data.db')
cursor = conn.execute('SELECT * FROM users')
users = cursor.fetchall()
sorted_users = sorted(users, key=lambda u: u[2])  # Sort by column 2

# Problems:
# 1. Fetch all rows (memory)
# 2. Transfer over network (if remote DB)
# 3. Sort in Python (slower than DB index)
```

**Fix**: Let database sort
```python
# ✅ RIGHT: Database sorts (uses index if available)
cursor = conn.execute('SELECT * FROM users ORDER BY age')
users = cursor.fetchall()  # Already sorted

# If you need top N:
cursor = conn.execute('SELECT * FROM users ORDER BY age LIMIT 100')

# Database can use index: O(log n + k) instead of O(n log n)
```

**When to sort in application**:
- Complex Python-specific comparison (custom objects)
- Data from multiple sources (can't sort in single query)
- Post-processing required before sorting

**When to sort in database**:
- Simple column sorting
- Large datasets (> 100K rows)
- Database has index on sort column
- Need pagination (LIMIT + OFFSET)

---

## Part 3: Correctness Antipatterns

### Antipattern 3.1: Incorrect Key Function

**Bad code**:
```python
# ❌ WRONG: Key function returns unsortable type
users = [
    {'name': 'Alice', 'tags': ['python', 'rust']},
    {'name': 'Bob', 'tags': ['java']},
]

# This crashes: lists aren't comparable
users.sort(key=lambda u: u['tags'])
# TypeError: '<' not supported between instances of 'list' and 'list'
```

**Fix**: Sort by sortable attribute
```python
# ✅ RIGHT: Sort by number of tags
users.sort(key=lambda u: len(u['tags']))

# Or: Sort by first tag (with default)
users.sort(key=lambda u: u['tags'][0] if u['tags'] else '')

# Or: Sort by all tags (convert to tuple)
users.sort(key=lambda u: tuple(u['tags']))
```

### Antipattern 3.2: Comparing None Without Handling

**Bad code**:
```python
# ❌ WRONG: Fails when None present
data = [5, 3, None, 1, 8]
sorted_data = sorted(data)
# TypeError: '<' not supported between instances of 'NoneType' and 'int'
```

**Fix 1**: Filter out None
```python
# ✅ Remove None values
sorted_data = sorted(x for x in data if x is not None)
```

**Fix 2**: Sort None to end
```python
# ✅ Sort None values to end
sorted_data = sorted(data, key=lambda x: (x is None, x))
# Result: [1, 3, 5, 8, None]

# Explanation: Tuples sort lexicographically
# (False, 1) < (False, 3) < ... < (True, None)
```

**Fix 3**: Use pandas (handles NaN gracefully)
```python
import pandas as pd
df = pd.DataFrame({'value': [5, 3, None, 1, 8]})
df.sort_values('value', na_position='last')
# NaN goes to end by default
```

### Antipattern 3.3: Forgetting In-Place vs Return

**Bad code**:
```python
# ❌ WRONG: Expecting list.sort() to return value
data = [3, 1, 4, 1, 5]
sorted_data = data.sort()  # Returns None!
print(sorted_data)  # None

# ❌ WRONG: Expecting sorted() to modify in-place
data = [3, 1, 4, 1, 5]
sorted(data)  # Returns new list, data unchanged
print(data)  # [3, 1, 4, 1, 5] - still unsorted!
```

**Fix**: Know the difference
```python
# ✅ In-place modification (returns None)
data = [3, 1, 4, 1, 5]
data.sort()  # Modifies data
print(data)  # [1, 1, 3, 4, 5]

# ✅ Return new list (original unchanged)
data = [3, 1, 4, 1, 5]
sorted_data = sorted(data)
print(data)  # [3, 1, 4, 1, 5] - unchanged
print(sorted_data)  # [1, 1, 3, 4, 5]
```

**Memory consideration**:
```python
# For large data, in-place is better (no copy)
data = [random.randint(0, 1000) for _ in range(1_000_000)]

# In-place: ~8 MB memory
data.sort()

# New list: ~16 MB memory (original + sorted copy)
sorted_data = sorted(data)
```

---

## Part 4: Engineering Antipatterns

### Antipattern 4.1: Over-Engineering with Parallel Sort

**Bad code**:
```python
# ❌ WRONG: Parallel sort for 10K items
from concurrent.futures import ProcessPoolExecutor

def parallel_sort(data, num_processes=4):
    chunk_size = len(data) // num_processes
    chunks = [data[i:i+chunk_size] for i in range(0, len(data), chunk_size)]

    with ProcessPoolExecutor(max_workers=num_processes) as executor:
        sorted_chunks = list(executor.map(sorted, chunks))

    # Merge sorted chunks
    return merge_sorted_lists(sorted_chunks)

data = list(range(10000))
result = parallel_sort(data)

# Problems:
# 1. Process overhead: ~50ms (much larger than sorting time)
# 2. IPC overhead: Copying data between processes
# 3. Complexity: 50 lines vs 1 line
# 4. Result: 10x SLOWER than built-in sort
```

**Benchmark**:
```python
data = [random.randint(0, 100000) for _ in range(10000)]

# Parallel sort: ~80ms
time_parallel = timeit.timeit(lambda: parallel_sort(data.copy()), number=10) / 10

# Built-in sort: ~2ms
time_builtin = timeit.timeit(lambda: sorted(data), number=10) / 10

# Built-in is 40x faster!
```

**Fix**: Use built-in unless data is huge
```python
# ✅ RIGHT: Simple and fast
sorted_data = sorted(data)

# Only parallelize if:
# - Data > 10 million items
# - Sorting is proven bottleneck (profiled)
# - Using library that handles it (Polars, Dask)
```

### Antipattern 4.2: Micro-Optimizing the Wrong Thing

**Bad code**:
```python
# ❌ WRONG: Optimizing comparison function
def expensive_key(item):
    # Heavily optimized key function
    return item.value  # Saved 5 nanoseconds per call!

data.sort(key=expensive_key)

# Meanwhile: Loading data from disk takes 5 seconds
# Sorting takes 0.01 seconds
# Optimized key saves: 0.0001 seconds
# Wasted developer time: 4 hours
```

**Fix**: Profile first, optimize bottleneck
```python
import cProfile

def process_data():
    data = load_from_disk()  # ← This is slow (5 seconds)
    data.sort(key=lambda x: x.value)  # ← This is fast (0.01 seconds)
    return data

cProfile.run('process_data()')

# Profile reveals: 99.8% time in load_from_disk
# Optimize that instead!
```

---

## Part 5: Real-World Case Studies

### Case Study 1: E-Commerce Product Listing

**Problem**: Product page slow (800ms)

**Original code**:
```python
def get_products(category, sort_by='price'):
    products = db.query(Product).filter(category=category).all()  # 10K products

    if sort_by == 'price':
        products.sort(key=lambda p: p.price)
    elif sort_by == 'rating':
        products.sort(key=lambda p: p.rating, reverse=True)
    elif sort_by == 'newest':
        products.sort(key=lambda p: p.created_at, reverse=True)

    return products[:100]  # Return first 100
```

**Problems identified**:
1. Fetching all 10K products (400ms)
2. Sorting all 10K products (30ms)
3. Returning only 100 (99% waste)

**Fix**:
```python
def get_products(category, sort_by='price', limit=100):
    query = db.query(Product).filter(category=category)

    if sort_by == 'price':
        query = query.order_by(Product.price)
    elif sort_by == 'rating':
        query = query.order_by(Product.rating.desc())
    elif sort_by == 'newest':
        query = query.order_by(Product.created_at.desc())

    return query.limit(limit).all()  # Fetch only 100
```

**Result**:
- Time: 800ms → 40ms (20x faster)
- Database uses index (O(log n + 100) instead of O(10K))
- Less memory (100 objects instead of 10K)

**Lessons**:
- Push sorting to database
- Don't fetch more data than needed
- Use database indexes

### Case Study 2: Log Analysis Pipeline

**Problem**: Daily log analysis taking 6 hours

**Original code**:
```python
def analyze_logs(log_file):
    # 100 million log entries
    logs = []
    for line in open(log_file):
        logs.append(parse_log(line))

    # Sort by timestamp for time-series analysis
    logs.sort(key=lambda log: log.timestamp)  # ← 30 minutes

    # Process in chronological order
    for log in logs:
        process(log)
```

**Problems**:
1. Loading all logs in memory (20 GB)
2. Sorting 100M items (30 minutes)
3. Logs are already 95% sorted (timestamped at creation)

**Fix**:
```python
def analyze_logs(log_file):
    import polars as pl

    # Polars reads and sorts efficiently
    logs = pl.read_csv(log_file, has_header=True)
    logs = logs.sort('timestamp')  # ← 2 minutes (15x faster)

    # Process in batches (streaming)
    for batch in logs.iter_slices(n_rows=100000):
        process_batch(batch)
```

**Result**:
- Time: 6 hours → 1.5 hours (4x improvement)
- Memory: 20 GB → 2 GB (streaming)
- Polars exploits: Multi-threading, SIMD, Arrow format

**Lessons**:
- Use modern libraries (Polars, DuckDB)
- Stream data when possible
- Timsort excels at nearly-sorted data (but Polars is even better)

### Case Study 3: Real-Time Leaderboard

**Problem**: Game leaderboard updates slow under load

**Original code**:
```python
class Leaderboard:
    def __init__(self):
        self.scores = []  # [(player_id, score), ...]

    def update_score(self, player_id, score):
        # Remove old score
        self.scores = [(pid, s) for pid, s in self.scores if pid != player_id]
        # Add new score
        self.scores.append((player_id, score))
        # Re-sort entire leaderboard
        self.scores.sort(key=lambda x: x[1], reverse=True)  # ← O(n log n)

    def get_top_100(self):
        return self.scores[:100]

# Under load: 1000 updates/second, 10K players
# Each update: O(10K log 10K) = ~130K operations
# Total: 130M operations/second → 500ms CPU per update
```

**Fix**:
```python
from sortedcontainers import SortedList

class Leaderboard:
    def __init__(self):
        # SortedList sorted by score (descending)
        self.scores = SortedList(key=lambda x: -x[1])
        self.player_scores = {}  # player_id → (player_id, score)

    def update_score(self, player_id, score):
        # Remove old score if exists
        if player_id in self.player_scores:
            self.scores.remove(self.player_scores[player_id])

        # Add new score
        entry = (player_id, score)
        self.scores.add(entry)  # ← O(log n)
        self.player_scores[player_id] = entry

    def get_top_100(self):
        return self.scores[:100]

# Each update: O(log 10K) = ~13 operations
# Total: 13K operations/second → 0.05ms CPU per update
# 10,000x improvement!
```

**Result**:
- CPU usage: 50% → 0.005%
- Latency: 500ms → 0.05ms (10,000x improvement)
- Scalability: Can handle 100K+ players

**Lessons**:
- Incremental data structures beat batch sorting
- SortedContainers is underutilized gem
- Algorithmic improvement > hardware upgrade

---

## Conclusion: The Antipattern Avoidance Checklist

**Before writing sorting code, ask**:

1. ☐ **Do I need to sort at all?**
   - Can I use heap, set, dict, or database query instead?

2. ☐ **Am I sorting more than once?**
   - Should I use SortedContainers to maintain sorted order?

3. ☐ **Am I sorting more data than I need?**
   - Can I use heapq.nlargest/nsmallest for top-K?
   - Can I sort in database with LIMIT?

4. ☐ **Am I using the right data structure?**
   - List vs SortedList vs DataFrame vs Database?

5. ☐ **Is the data type suitable?**
   - NumPy arrays for numerical data?
   - Polars for large tabular data?

6. ☐ **Do I need stability?**
   - Using stable sort when ties must preserve order?

7. ☐ **Have I profiled?**
   - Is sorting actually the bottleneck?
   - Or am I optimizing the wrong thing?

**Remember**: The best sorting code is the sorting you don't have to write. The second best is using built-in sort(). Custom optimization should be the last resort, not the first instinct.
