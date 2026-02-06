# S3: Need-Driven Discovery - Trie Libraries Use Case Patterns

**Experiment**: 1.042 - Trie Libraries
**Stage**: S3 - Need-Driven Discovery (Generic Use Case Patterns)
**Date**: 2025-10-10
**Methodology**: MPSE Stage 3 - Generic problem patterns with parameters, NOT application-specific

---

## Table of Contents
1. [Use Case Pattern Taxonomy](#use-case-pattern-taxonomy)
2. [Pattern Catalog](#pattern-catalog)
3. [Decision Framework](#decision-framework)
4. [Anti-Patterns](#anti-patterns)
5. [Migration Patterns](#migration-patterns)

---

## Use Case Pattern Taxonomy

### Classification Dimensions

1. **Data Mutability**
   - Static: Build once, query many times
   - Semi-static: Periodic bulk updates
   - Dynamic: Continuous insertions/deletions

2. **Query Pattern**
   - Exact match: "Does key exist?"
   - Prefix search: "All keys starting with X"
   - Longest prefix: "Best matching prefix for path"
   - Wildcard: "Keys matching pattern"

3. **Scale Profile**
   - Small: <10k keys
   - Medium: 10k-1M keys
   - Large: 1M-100M keys
   - Extreme: >100M keys

4. **Performance Priority**
   - Latency: Minimize query time
   - Throughput: Maximize ops/sec
   - Memory: Minimize footprint
   - Balanced: No single bottleneck

---

## Pattern Catalog

### Pattern 1: Autocomplete / Type-ahead Search

#### **Problem Definition**
As user types incrementally, suggest completions from dictionary.

#### **Parameters**
- **Dictionary size**: N keys (e.g., 10k-10M words/phrases)
- **Query frequency**: High (100-1000 queries/sec)
- **Latency requirement**: <50ms for good UX
- **Result count**: Top-K results (typically K=5-20)
- **Update frequency**: Low to moderate

#### **Trie Advantages**
- ✅ O(p) prefix lookup where p = prefix length (independent of N)
- ✅ Natural lexicographic ordering
- ✅ Can limit results without scanning entire dictionary

#### **Library Selection**

```python
# Decision tree:
if dictionary_size < 100k and updates_frequent:
    library = "pygtrie"  # Simple, mutable
elif dictionary_size < 10M and updates_rare:
    library = "datrie"  # Fast, memory efficient
elif dictionary_size > 10M or extreme_memory_constraints:
    library = "marisa-trie"  # Succinct, immutable
```

#### **Reference Implementation Pattern**

```python
import pygtrie

class AutocompleteEngine:
    def __init__(self, phrases_with_scores):
        """
        phrases_with_scores: [(phrase, score), ...]
        Score could be: frequency, recency, user preference, etc.
        """
        self.trie = pygtrie.CharTrie()
        for phrase, score in phrases_with_scores:
            self.trie[phrase.lower()] = score

    def suggest(self, prefix, max_results=10):
        """Return top-K completions for prefix"""
        if not prefix:
            return []

        # Get all matches
        matches = list(self.trie.items(prefix=prefix.lower()))

        # Sort by score (descending)
        matches.sort(key=lambda x: x[1], reverse=True)

        # Return top-K
        return [phrase for phrase, score in matches[:max_results]]

# Usage
engine = AutocompleteEngine([
    ("apple", 100),
    ("application", 50),
    ("appetite", 30),
])
engine.suggest("app")  # ["apple", "application", "appetite"]
```

#### **Performance Parameters**
- **Query latency**: 1-10ms for prefix length 3-10
- **Memory**: 100-300 bytes/phrase (pygtrie)
- **Build time**: 100ms per 10k phrases

#### **Extensions**
- **Fuzzy matching**: Edit distance tolerance
- **Context-aware**: Different completions per user/context
- **Distributed**: Partition by prefix for horizontal scaling

---

### Pattern 2: HTTP/URL Routing

#### **Problem Definition**
Match incoming request path to handler based on route patterns.

#### **Parameters**
- **Route count**: Typically 10-1000 routes
- **Request rate**: High (100-10k req/sec)
- **Route patterns**: Static segments + wildcards + parameters
- **Priority**: Longest prefix match (most specific route wins)

#### **Trie Advantages**
- ✅ Longest prefix match built-in
- ✅ O(m) lookup (path length), not O(routes)
- ✅ Natural hierarchical structure matches URL structure

#### **Example Routes**
```
/api/users/:id
/api/users/:id/posts
/api/users/:id/posts/:post_id
/api/admin/*
/static/*
```

#### **Reference Implementation Pattern**

```python
import pygtrie
import re

class Router:
    def __init__(self):
        self.trie = pygtrie.StringTrie(separator='/')
        self.wildcard_routes = []  # Special handling

    def add_route(self, path, handler):
        """Register route with handler"""
        if '*' in path or ':' in path:
            # Parametric/wildcard route
            pattern = self._compile_pattern(path)
            self.wildcard_routes.append((pattern, handler, path))
        else:
            # Static route (exact match)
            self.trie[path] = handler

    def route(self, path):
        """Find handler for path"""
        # Try exact match first
        if path in self.trie:
            return self.trie[path], {}

        # Try longest prefix match
        try:
            prefix = self.trie.longest_prefix(path)
            return prefix.value, {}
        except KeyError:
            pass

        # Try wildcard/parametric routes
        for pattern, handler, route_path in self.wildcard_routes:
            match = pattern.match(path)
            if match:
                return handler, match.groupdict()

        # No match
        return None, {}

    def _compile_pattern(self, path):
        """Convert route pattern to regex"""
        # /api/users/:id -> /api/users/(?P<id>[^/]+)
        pattern = path.replace('/', r'\/')
        pattern = re.sub(r':(\w+)', r'(?P<\1>[^/]+)', pattern)
        pattern = pattern.replace('*', '.*')
        return re.compile(f'^{pattern}$')

# Usage
router = Router()
router.add_route('/api/users', list_users_handler)
router.add_route('/api/users/:id', get_user_handler)
router.add_route('/api/users/:id/posts', get_user_posts_handler)

handler, params = router.route('/api/users/123')
# handler = get_user_handler, params = {'id': '123'}
```

#### **Performance Parameters**
- **Routing latency**: <1ms per request
- **Memory**: ~1KB per 100 routes
- **Scalability**: O(path_length), independent of route count

#### **Alternative Approach: Radix Tree**
For more complex wildcard support, custom radix tree may be better:

```python
# Radix tree node stores path segments, not characters
# /api/users -> ['api', 'users']
# Better for URL structure
```

---

### Pattern 3: IP Address Routing / Longest Prefix Match

#### **Problem Definition**
Given IP address, find most specific matching route (CIDR notation).

#### **Parameters**
- **Routing table size**: 100k-10M entries (BGP scale)
- **Lookup rate**: Very high (millions/sec in hardware)
- **IP version**: IPv4 (32-bit) or IPv6 (128-bit)
- **Match type**: Longest prefix match

#### **Trie Structure**
Binary trie with 2 children per node (0/1 bits).

#### **Reference Implementation Pattern**

```python
import pygtrie

class IPRouter:
    """IPv4 routing table using binary trie"""

    def __init__(self):
        self.trie = pygtrie.StringTrie()

    def add_route(self, cidr, next_hop):
        """Add CIDR route: '192.168.1.0/24' -> next_hop"""
        ip, prefix_len = cidr.split('/')
        prefix_len = int(prefix_len)

        # Convert IP to binary string
        ip_int = self._ip_to_int(ip)
        binary = format(ip_int, '032b')[:prefix_len]

        self.trie[binary] = next_hop

    def route(self, ip_address):
        """Find next hop for IP address"""
        ip_int = self._ip_to_int(ip_address)
        binary = format(ip_int, '032b')

        # Longest prefix match
        try:
            prefix = self.trie.longest_prefix(binary)
            return prefix.value
        except KeyError:
            return None  # No route

    def _ip_to_int(self, ip):
        """Convert '192.168.1.1' to integer"""
        octets = ip.split('.')
        return sum(int(octet) << (8 * (3 - i)) for i, octet in enumerate(octets))

# Usage
router = IPRouter()
router.add_route('192.168.0.0/16', 'gateway1')
router.add_route('192.168.1.0/24', 'gateway2')  # More specific
router.add_route('192.168.1.128/25', 'gateway3')  # Even more specific

router.route('192.168.1.200')  # Returns 'gateway3' (longest match)
```

#### **Specialized Library**
For production IP routing, use `radix` package (C-optimized):

```python
import radix

rtree = radix.Radix()
rnode = rtree.add('192.168.1.0/24')
rnode.data['next_hop'] = 'gateway1'

rnode = rtree.search_best('192.168.1.100')
next_hop = rnode.data['next_hop']
```

#### **Performance Parameters**
- **Lookup latency**: O(32) for IPv4, O(128) for IPv6
- **Memory**: Depends on route overlap/hierarchy
- **Hardware acceleration**: TCAM in network switches

---

### Pattern 4: Spell Checking / Dictionary Validation

#### **Problem Definition**
Validate if word exists in dictionary, suggest corrections if not.

#### **Parameters**
- **Dictionary size**: 50k-500k words (language-dependent)
- **Query frequency**: Moderate (per keystroke or per sentence)
- **Languages**: Single or multiple
- **Update frequency**: Very low (dictionary rarely changes)

#### **Trie Advantages**
- ✅ Exact match in O(m)
- ✅ Can generate "nearby" words (edit distance 1-2)
- ✅ Memory efficient for large dictionaries

#### **Reference Implementation Pattern**

```python
import marisa_trie

class SpellChecker:
    def __init__(self, dictionary_words):
        """Build from word list"""
        self.trie = marisa_trie.Trie(dictionary_words)
        self.words = set(dictionary_words)  # For fast membership

    def is_valid(self, word):
        """Check if word is in dictionary"""
        return word.lower() in self.trie

    def suggest_corrections(self, word, max_edit_distance=2):
        """Find similar words using edit distance"""
        candidates = set()

        # Generate candidates within edit distance
        candidates.update(self._edits1(word))
        if max_edit_distance >= 2:
            for edit1 in self._edits1(word):
                candidates.update(self._edits1(edit1))

        # Filter to valid words
        return [w for w in candidates if w in self.words]

    def _edits1(self, word):
        """All edits 1 step away"""
        letters = 'abcdefghijklmnopqrstuvwxyz'
        splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]

        deletes = [L + R[1:] for L, R in splits if R]
        transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
        replaces = [L + c + R[1:] for L, R in splits if R for c in letters]
        inserts = [L + c + R for L, R in splits for c in letters]

        return set(deletes + transposes + replaces + inserts)

# Usage
checker = SpellChecker(['cat', 'cats', 'dog', 'hello', 'world'])
checker.is_valid('cat')  # True
checker.is_valid('cta')  # False
checker.suggest_corrections('cta')  # ['cat']
```

#### **Advanced: Trie-based Edit Distance**
Walk trie while computing Levenshtein distance on-the-fly (more efficient than generating all candidates).

#### **Performance Parameters**
- **Validation**: <1ms per word
- **Correction generation**: 10-100ms (depends on edit distance)
- **Memory**: 5-15 bytes/word (marisa-trie)

---

### Pattern 5: Text Deduplication / Common Substring Finding

#### **Problem Definition**
Find repeated substrings across text corpus for compression or deduplication.

#### **Parameters**
- **Text size**: Varies (documents, logs, DNA sequences)
- **Substring length**: Variable (find all common substrings)
- **Use case**: Compression, plagiarism detection, DNA analysis

#### **Trie Type**: Suffix Tree (all suffixes of text)

#### **Problem with Standard Tries**
Suffix trees are complex; Python libraries limited.

#### **Reference Implementation Pattern**

```python
# Conceptual suffix tree usage (no mature Python library)
# For real use, consider:
# 1. suffix-tree package (limited)
# 2. C++ bindings (libdivsufsort)
# 3. Specialized tools (e.g., for DNA: BioPython)

class SimpleSuffixTrie:
    """Naive suffix trie for demonstration"""

    def __init__(self, text):
        import pygtrie
        self.trie = pygtrie.CharTrie()
        self.text = text

        # Insert all suffixes
        for i in range(len(text)):
            suffix = text[i:]
            self.trie[suffix] = i  # Store starting position

    def find_repeated_substrings(self, min_length=3):
        """Find substrings that appear multiple times"""
        repeated = []

        # Walk trie, find nodes with multiple children
        # (indicates branching = repeated prefix)
        # Simplified: check prefixes manually
        seen_prefixes = {}
        for i in range(len(self.text)):
            for j in range(i + min_length, len(self.text) + 1):
                substring = self.text[i:j]
                if substring in seen_prefixes:
                    repeated.append((substring, seen_prefixes[substring], i))
                else:
                    seen_prefixes[substring] = i

        return repeated

# Usage
text = "banana"
suffix_trie = SimpleSuffixTrie(text)
# Suffixes: "banana", "anana", "nana", "ana", "na", "a"
# Common: "ana" appears at positions 1 and 3
```

#### **Practical Alternative**
For production text deduplication, use specialized algorithms:
- Rolling hash (Rabin-Karp)
- Bloom filters for seen substrings
- Specialized suffix array libraries

---

### Pattern 6: Prefix-based Caching / CDN Routing

#### **Problem Definition**
Route requests to nearest cache/CDN based on path prefix.

#### **Parameters**
- **Path patterns**: URL prefixes
- **Routing rules**: Map prefix to cache tier/region
- **Update frequency**: Low (routing policy changes)
- **Query frequency**: Very high (every request)

#### **Example Routing Rules**
```
/static/images/* -> CDN region: US-WEST
/static/videos/* -> CDN region: US-EAST (video-optimized)
/api/* -> Origin server
/api/public/* -> Edge cache (cacheable API)
```

#### **Reference Implementation Pattern**

```python
import pygtrie

class CDNRouter:
    def __init__(self):
        self.trie = pygtrie.StringTrie(separator='/')

    def add_rule(self, prefix, target):
        """Add routing rule"""
        self.trie[prefix] = target

    def route(self, path):
        """Find target for path (longest prefix match)"""
        try:
            prefix = self.trie.longest_prefix(path)
            return prefix.value
        except KeyError:
            return "origin"  # Default

# Usage
router = CDNRouter()
router.add_rule('/static', 'cdn-static')
router.add_rule('/static/images', 'cdn-images')
router.add_rule('/api/public', 'edge-cache')

router.route('/static/images/logo.png')  # 'cdn-images' (most specific)
router.route('/static/css/style.css')    # 'cdn-static'
router.route('/api/users')               # 'origin' (no match)
```

#### **Performance Requirements**
- **Latency**: <100μs (routing is critical path)
- **Memory**: Minimal (small rule set)
- **Concurrency**: Read-only, highly parallel

---

### Pattern 7: Hierarchical Configuration / Policy Inheritance

#### **Problem Definition**
Apply configuration/policy based on hierarchical path, with inheritance.

#### **Parameters**
- **Hierarchy**: Organization units, file paths, network topology
- **Inheritance**: Child inherits parent's policy unless overridden
- **Query**: Find effective policy for specific path

#### **Example: File Permissions**
```
/home/users/* -> read-only
/home/users/alice/* -> read-write (override)
/home/users/alice/private/* -> no-access (override)
```

#### **Reference Implementation Pattern**

```python
import pygtrie

class PolicyEngine:
    def __init__(self):
        self.trie = pygtrie.StringTrie(separator='/')

    def set_policy(self, path, policy):
        """Set policy for path"""
        self.trie[path] = policy

    def get_policy(self, path):
        """Get effective policy (longest prefix)"""
        try:
            prefix = self.trie.longest_prefix(path)
            return prefix.value
        except KeyError:
            return None  # No policy

    def get_inherited_policies(self, path):
        """Get all policies in hierarchy (for merging)"""
        policies = []
        parts = path.strip('/').split('/')
        for i in range(1, len(parts) + 1):
            prefix = '/' + '/'.join(parts[:i])
            if prefix in self.trie:
                policies.append((prefix, self.trie[prefix]))
        return policies

# Usage
engine = PolicyEngine()
engine.set_policy('/home/users', {'permission': 'read'})
engine.set_policy('/home/users/alice', {'permission': 'write'})
engine.set_policy('/home/users/alice/private', {'permission': 'none'})

engine.get_policy('/home/users/alice/documents')  # {'permission': 'write'}
engine.get_policy('/home/users/bob/documents')    # {'permission': 'read'}

# Get full inheritance chain
engine.get_inherited_policies('/home/users/alice/private/file.txt')
# [
#   ('/home/users', {'permission': 'read'}),
#   ('/home/users/alice', {'permission': 'write'}),
#   ('/home/users/alice/private', {'permission': 'none'}),
# ]
```

#### **Use Cases**
- File system permissions
- Cloud IAM policies (AWS resource paths)
- Network firewall rules (IP hierarchies)
- Organization access control

---

### Pattern 8: Version/Path-based API Routing

#### **Problem Definition**
Route API requests based on version prefix or path structure.

#### **Parameters**
- **API versions**: v1, v2, v3, etc.
- **Graceful migration**: Support multiple versions
- **Deprecation**: Track which versions are active

#### **Reference Implementation Pattern**

```python
import pygtrie

class APIRouter:
    def __init__(self):
        self.trie = pygtrie.StringTrie(separator='/')

    def register(self, path, version, handler):
        """Register versioned endpoint"""
        full_path = f"/{version}/{path.lstrip('/')}"
        self.trie[full_path] = {
            'handler': handler,
            'version': version,
            'path': path
        }

    def route(self, request_path):
        """Find handler for request"""
        try:
            entry = self.trie.longest_prefix(request_path)
            return entry.value
        except KeyError:
            return None

    def list_endpoints(self, version=None):
        """List all endpoints (optionally filtered by version)"""
        endpoints = []
        for path, entry in self.trie.items():
            if version is None or entry['version'] == version:
                endpoints.append((path, entry))
        return endpoints

# Usage
router = APIRouter()
router.register('/users', 'v1', handle_users_v1)
router.register('/users', 'v2', handle_users_v2)
router.register('/users/:id', 'v1', handle_user_v1)

router.route('/v1/users')      # handle_users_v1
router.route('/v2/users')      # handle_users_v2
router.route('/v1/users/123')  # handle_user_v1

# List all v1 endpoints
router.list_endpoints('v1')
```

---

## Decision Framework

### Step 1: Characterize Your Use Case

Answer these questions:

1. **What is the primary query pattern?**
   - [ ] Exact match (key lookup)
   - [ ] Prefix search (autocomplete)
   - [ ] Longest prefix match (routing)
   - [ ] Pattern matching (wildcards)

2. **How large is the dataset?**
   - [ ] Small (<10k keys)
   - [ ] Medium (10k-1M keys)
   - [ ] Large (1M-100M keys)
   - [ ] Extreme (>100M keys)

3. **How often does data change?**
   - [ ] Static (never or rarely)
   - [ ] Semi-static (batch updates daily/weekly)
   - [ ] Dynamic (continuous updates)

4. **What is the performance priority?**
   - [ ] Query latency (<1ms)
   - [ ] Throughput (millions ops/sec)
   - [ ] Memory efficiency (<10 bytes/key)
   - [ ] Balanced

5. **What are the deployment constraints?**
   - [ ] Pure Python (no C dependencies)
   - [ ] Can use C extensions
   - [ ] Distributed/multi-process
   - [ ] Embedded/resource-constrained

---

### Step 2: Apply Decision Tree

```
START: Do you need prefix operations?
│
├─ NO: Use hash table (Python dict)
│  └─ Tries add overhead without benefit
│
└─ YES: Continue
    │
    ├─ Dataset static (build once)?
    │   │
    │   ├─ YES: Memory critical?
    │   │   │
    │   │   ├─ YES: Use marisa-trie
    │   │   │   └─ 5-15 bytes/key, immutable
    │   │   │
    │   │   └─ NO: Use datrie
    │   │       └─ Fast queries, moderate memory
    │   │
    │   └─ NO: Dynamic updates frequent?
    │       │
    │       ├─ YES: Use pygtrie or hat-trie
    │       │   └─ Mutable, reasonable performance
    │       │
    │       └─ NO: Use datrie
    │           └─ Good balance
    │
    └─ Pure Python required?
        │
        ├─ YES: Use pygtrie
        │   └─ No C dependencies
        │
        └─ NO: See above
```

---

### Step 3: Validate with Benchmarks

**Create a representative workload**:

```python
import time

def benchmark_trie(trie, queries):
    """Measure query performance"""
    start = time.perf_counter()
    for query in queries:
        _ = query in trie
    end = time.perf_counter()

    qps = len(queries) / (end - start)
    return qps

# Run on your data
qps = benchmark_trie(your_trie, your_queries)
print(f"Queries per second: {qps:,.0f}")
```

---

## Anti-Patterns

### Anti-Pattern 1: Trie for Random Key Lookup

**Problem**: Using trie when hash table would suffice

```python
# ❌ BAD: Trie for random access
trie = pygtrie.CharTrie()
for key, value in items:
    trie[key] = value

result = trie['specific_key']  # No prefix operation needed
```

```python
# ✅ GOOD: Hash table for random access
data = dict(items)
result = data['specific_key']  # 10× faster, simpler
```

**When is trie justified?**
- Only if you also need prefix searches on same data
- Or if you need lexicographic ordering

---

### Anti-Pattern 2: Mutable Trie for Static Data

**Problem**: Using mutable trie (pygtrie) for static dictionary

```python
# ❌ BAD: Mutable trie for spell checker
trie = pygtrie.CharTrie()
for word in large_dictionary:  # 500k words
    trie[word] = True
# 50-100 MB memory, pure Python overhead
```

```python
# ✅ GOOD: Immutable compressed trie
trie = marisa_trie.Trie(large_dictionary)
# 5-10 MB memory, faster queries
```

**Trade-off**: Build time higher, but one-time cost

---

### Anti-Pattern 3: Trie for Binary Data Without Consideration

**Problem**: Using character-based trie for binary keys

```python
# ❌ BAD: CharTrie with binary data
trie = pygtrie.CharTrie()
trie[b'\x00\x01\x02'.decode('latin1')] = value  # Hacky
```

```python
# ✅ GOOD: Byte-oriented trie
trie = marisa_trie.BytesTrie([b'\x00\x01\x02', b'\xff\xfe\xfd'])
```

---

### Anti-Pattern 4: Trie Rebuild on Every Update

**Problem**: Rebuilding immutable trie for small changes

```python
# ❌ BAD: Rebuild marisa-trie frequently
def add_word(words_set, new_word):
    words_set.add(new_word)
    return marisa_trie.Trie(words_set)  # Expensive rebuild
```

```python
# ✅ GOOD: Use mutable trie or batch updates
# Option 1: Mutable trie
trie = pygtrie.CharTrie(words)
trie[new_word] = True  # O(m) update

# Option 2: Batch updates (if immutable needed)
pending_updates = set()
# ... collect updates ...
# Rebuild once per hour/day with pending_updates
```

---

### Anti-Pattern 5: Ignoring Alphabet Constraints (datrie)

**Problem**: Using datrie without understanding alphabet limitation

```python
# ❌ BAD: Insufficient alphabet
trie = datrie.Trie('abcdefghijklmnopqrstuvwxyz')
trie['hello!'] = 1  # ERROR: '!' not in alphabet
```

```python
# ✅ GOOD: Comprehensive alphabet
alphabet = 'abcdefghijklmnopqrstuvwxyz .,!?'
trie = datrie.Trie(alphabet)
trie['hello!'] = 1  # OK
```

---

## Migration Patterns

### Pattern 1: Dict → Trie (Adding Prefix Search)

**Scenario**: Existing dict-based system needs autocomplete

**Migration Strategy**:

```python
# Phase 1: Parallel data structures
class DataStore:
    def __init__(self):
        self.dict = {}      # Legacy
        self.trie = pygtrie.CharTrie()  # New

    def set(self, key, value):
        self.dict[key] = value
        self.trie[key] = value

    def get(self, key):
        return self.dict[key]  # Use existing code path

    def prefix_search(self, prefix):
        # New functionality
        return list(self.trie.items(prefix=prefix))

# Phase 2: Migrate reads to trie
class DataStore:
    def get(self, key):
        return self.trie[key]  # Switch to trie

# Phase 3: Remove dict
class DataStore:
    def __init__(self):
        self.trie = pygtrie.CharTrie()
```

---

### Pattern 2: Upgrade to Faster Library

**Scenario**: pygtrie → datrie for performance

**Migration Strategy**:

```python
# Export from pygtrie
old_trie = pygtrie.CharTrie(existing_data)
items = list(old_trie.items())

# Determine alphabet
import string
alphabet = string.ascii_lowercase + string.ascii_uppercase + string.digits + ' .,!?'

# Import to datrie
new_trie = datrie.Trie(alphabet)
for key, value in items:
    try:
        new_trie[key] = value
    except Exception as e:
        print(f"Failed to import {key}: {e}")
        # Handle charset issues

# Verify
assert len(new_trie) == len(old_trie)
```

---

### Pattern 3: Distributed Trie with Redis

**Scenario**: Single-node trie → distributed system

**Migration Strategy**:

```python
# Local trie (original)
trie = pygtrie.CharTrie(data)

# Distributed: Store in Redis, cache locally
import redis
import pickle

class DistributedTrie:
    def __init__(self, redis_client):
        self.redis = redis_client
        self.local_cache = None
        self.cache_ttl = 300  # 5 minutes

    def _refresh_cache(self):
        """Load trie from Redis"""
        serialized = self.redis.get('trie:data')
        if serialized:
            self.local_cache = pickle.loads(serialized)
        else:
            self.local_cache = pygtrie.CharTrie()

    def get(self, key):
        if self.local_cache is None:
            self._refresh_cache()
        return self.local_cache.get(key)

    def prefix_search(self, prefix):
        if self.local_cache is None:
            self._refresh_cache()
        return list(self.local_cache.items(prefix=prefix))

    def update_from_source(self, new_data):
        """Rebuild trie and publish to Redis"""
        new_trie = pygtrie.CharTrie(new_data)
        serialized = pickle.dumps(new_trie)
        self.redis.set('trie:data', serialized)
        self.redis.publish('trie:update', 'new_version')
```

---

## Summary: Quick Reference Table

| Use Case | Dataset Size | Mutability | Recommended Library | Rationale |
|----------|--------------|------------|---------------------|-----------|
| Autocomplete | <100k | Dynamic | `pygtrie` | Simple, mutable, good API |
| Autocomplete | 100k-10M | Static | `datrie` | Fast, memory efficient |
| Autocomplete | >10M | Static | `marisa-trie` | Succinct, extreme memory savings |
| HTTP Routing | <1k routes | Dynamic | `pygtrie.StringTrie` | Path-based trie, mutable |
| IP Routing | Any | Semi-static | `radix` (specialized) | CIDR-optimized |
| Spell Check | 50k-500k | Static | `marisa-trie` | Large dictionary, immutable |
| Dictionary Validation | Any | Dynamic | `pygtrie` | Frequent updates |
| Text Deduplication | N/A | Static | Suffix tree (specialized) | Requires advanced algorithm |
| CDN Routing | <1k rules | Static | `pygtrie.StringTrie` | Longest prefix match |
| Config Inheritance | <10k paths | Semi-static | `pygtrie.StringTrie` | Hierarchical policy |

---

**Status**: ✅ S3 Complete - Generic use case patterns with decision frameworks
**Next Stage**: S4 Strategic Discovery (technology evolution)
