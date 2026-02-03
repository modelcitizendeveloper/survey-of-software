# String Processing Architecture Patterns

## Pattern 1: Centralized String Normalization

### Context
Multi-service architecture where strings cross service boundaries (user input, external APIs, database storage).

### Problem
Inconsistent normalization leads to:
- Duplicate entries (café vs café)
- Failed lookups (normalized vs unnormalized)
- Security issues (bypassing validation through alternate encodings)

### Solution: Normalization Gateway

```
┌─────────────┐
│   Client    │
└──────┬──────┘
       │ Raw input
       ↓
┌──────────────────────────────┐
│  API Gateway                 │
│  - UTF-8 validation          │
│  - Unicode normalization NFC │
│  - Whitespace trimming       │
│  - Length limits             │
└──────┬───────────────────────┘
       │ Normalized strings
       ↓
┌─────────────┐     ┌─────────────┐
│  Service A  │     │  Service B  │
│  (trust)    │     │  (trust)    │
└─────────────┘     └─────────────┘
```

**Implementation**:
```python
class NormalizationMiddleware:
    def process_request(self, request):
        for key, value in request.data.items():
            if isinstance(value, str):
                # Validate UTF-8
                value.encode('utf-8')  # Raises if invalid

                # Normalize
                value = unicodedata.normalize('NFC', value)

                # Trim whitespace
                value = value.strip()

                # Enforce limits
                if len(value) > MAX_STRING_LENGTH:
                    raise ValueError(f"{key} exceeds max length")

                request.data[key] = value
```

**Benefits**:
- Single source of truth for normalization rules
- Services can trust incoming strings
- Easier to audit and update rules

**Trade-offs**:
- Single point of failure
- Latency overhead (usually negligible)
- Must version normalization rules carefully

### When to Use
- Multi-service architectures
- User-facing applications with international users
- Systems with strict data quality requirements

## Pattern 2: Lazy String Parsing

### Context
Large payloads (JSON, XML) where most fields are unused by downstream consumers.

### Problem
Parsing entire document upfront wastes:
- CPU (parsing unused fields)
- Memory (storing unused data)
- Time (blocking on full parse)

### Solution: Streaming Parser with On-Demand Field Access

```rust
// Don't parse everything upfront
let mut parser = JsonStreamParser::new(large_json);

// Extract only what's needed
if let Some(user_id) = parser.get("user.id") {
    let user = fetch_user(user_id);

    // Only parse rest if needed
    if user.needs_full_profile {
        let full_data = parser.parse_all();
        process(full_data);
    }
}
```

**Benefits**:
- Faster p99 latency (skip unused fields)
- Lower memory usage
- Can short-circuit on validation failure

**Trade-offs**:
- More complex than full parse upfront
- May re-parse if accessing many fields
- Harder to debug (partial state)

### When to Use
- Large payloads (> 1MB)
- High read/parse ratios (many requests parse same data)
- Strict latency budgets (p99 < 100ms)

## Pattern 3: String Interning for High-Cardinality Keys

### Context
Systems tracking millions of keys (API keys, user IDs, session IDs) where same strings appear repeatedly.

### Problem
Without interning:
```
Memory per string: 24 bytes (object) + string data
1M unique strings: ~100MB overhead
10 refs to same string: 10x memory usage
```

### Solution: String Intern Pool

```python
from sys import intern

class KeyTracker:
    def __init__(self):
        self.stats = {}  # Uses interned strings as keys

    def record(self, api_key, metric, value):
        # Intern the key - same string → same object
        key = intern(api_key)

        # O(1) equality check (pointer comparison)
        if key not in self.stats:
            self.stats[key] = {}

        self.stats[key][metric] = value
```

**Benefits**:
- 50-90% memory reduction for high-cardinality keys
- O(1) equality checks (pointer comparison)
- Cache-friendly (same object in dict lookups)

**Trade-offs**:
- Intern pool lives forever (memory leak if unbounded)
- Thread-safety concerns (global intern table)
- Overhead for short-lived strings

### Mitigation: Bounded Intern Pool

```python
from functools import lru_cache

@lru_cache(maxsize=100_000)
def intern_bounded(s):
    return s

# LRU eviction prevents unbounded growth
```

### When to Use
- High-cardinality keys (> 100K unique values)
- Keys reused frequently (10+ refs per unique value)
- Dictionary/hash table heavy workloads

## Pattern 4: Regex Compilation Pipeline

### Context
Application with many regex patterns (content moderation, data extraction, validation).

### Problem
Compiling regex on each request:
- 100x slower than compiled regex
- Prevents optimization (inline, JIT)
- Wastes CPU on repeated compilation

### Solution: Startup Compilation + Hot Reload

```python
class RegexManager:
    def __init__(self):
        self.patterns = {}
        self.load_patterns()

    def load_patterns(self):
        """Load and compile all patterns at startup"""
        for name, pattern in load_config("patterns.yaml"):
            try:
                self.patterns[name] = re.compile(
                    pattern,
                    re.VERBOSE | re.IGNORECASE
                )
            except re.error as e:
                logger.error(f"Invalid pattern {name}: {e}")

    def match(self, pattern_name, text):
        pattern = self.patterns.get(pattern_name)
        if not pattern:
            raise KeyError(f"Unknown pattern: {pattern_name}")

        return pattern.search(text)

    def reload(self):
        """Hot reload without downtime"""
        new_patterns = self._load_patterns_from_config()

        # Atomic swap
        self.patterns = new_patterns
```

**Benefits**:
- 10-100x faster matching (pre-compiled)
- Centralized pattern management
- Can optimize patterns globally (deduplicate, merge)

**Trade-offs**:
- Startup time (compile all patterns)
- Memory (keep all compiled patterns in RAM)
- Deployment complexity (hot reload logic)

### When to Use
- Many regex patterns (> 10)
- High request volume
- Patterns change infrequently (weekly/daily, not per-request)

## Pattern 5: Multi-Stage Filtering Pipeline

### Context
Search or filtering system with expensive operations (fuzzy matching, ML models).

### Problem
Running expensive algorithms on entire dataset wastes resources when many items clearly don't match.

### Solution: Funnel Pattern (Cheap → Expensive)

```
┌──────────────────┐
│   All Items      │ 1M items
│   (100%)         │
└────────┬─────────┘
         │
         ↓
┌──────────────────┐
│ Stage 1: Prefix  │ Cheap: O(1) hash lookup
│ "starts with X"  │ → 100K items (10%)
└────────┬─────────┘
         │
         ↓
┌──────────────────┐
│ Stage 2: Regex   │ Medium: O(n) scan
│ "contains Y"     │ → 10K items (1%)
└────────┬─────────┘
         │
         ↓
┌──────────────────┐
│ Stage 3: Fuzzy   │ Expensive: O(n·m)
│ "similar to Z"   │ → 1K items (0.1%)
└────────┬─────────┘
         │
         ↓
┌──────────────────┐
│  Final Results   │ 1K items
└──────────────────┘
```

**Implementation**:
```python
def search(query, items):
    # Stage 1: Cheap prefix filter
    if query:
        prefix_filter = query[:3].lower()
        items = [i for i in items if i.prefix == prefix_filter]

    # Stage 2: Medium regex filter
    if items and has_pattern(query):
        pattern = compile_pattern(query)
        items = [i for i in items if pattern.search(i.text)]

    # Stage 3: Expensive fuzzy matching (only on remaining)
    if items and needs_fuzzy(query):
        items = fuzzy_rank(items, query, threshold=0.7)

    return items[:100]  # Top 100
```

**Benefits**:
- 10-100x faster (skip expensive operations on non-matches)
- Scalable to large datasets
- Can adjust stages dynamically (if stage 1 too selective, skip)

**Trade-offs**:
- Complexity (multiple stages to maintain)
- False negatives (if early stages too aggressive)
- Tuning required (threshold per stage)

### When to Use
- Large item sets (> 100K)
- Expensive matching algorithms (ML, fuzzy)
- High query volume (optimize hot path)

## Pattern 6: String-Based Event Sourcing

### Context
Event-driven architecture where events carry string payloads (JSON, Protobuf).

### Problem
- Schema evolution (adding/removing fields)
- Version compatibility (old consumers, new producers)
- Replay performance (parsing old events)

### Solution: Versioned String Schemas + Migration

```
Event Stream:
┌─────────────────────────────────────────┐
│ v1: {"user":"alice","action":"login"}   │
│ v2: {"user":"bob","action":"purchase",  │
│      "amount":50}                       │
│ v3: {"user_id":123,"event":"checkout",  │ ← Schema evolution
│      "cart_value":75.50}                │
└─────────────────────────────────────────┘
         │
         ↓
┌────────────────────────────────────────┐
│  Schema Registry + Migration           │
│  v1 → v2: Add amount (default: 0)      │
│  v2 → v3: Rename fields, parse types   │
└────────────────────────────────────────┘
         │
         ↓
┌────────────────────────────────────────┐
│  Consumer (sees v3 always)             │
└────────────────────────────────────────┘
```

**Implementation**:
```python
class EventMigrator:
    def __init__(self):
        self.migrations = {
            (1, 2): self.v1_to_v2,
            (2, 3): self.v2_to_v3,
        }

    def parse_event(self, raw_json):
        event = json.loads(raw_json)
        version = event.get("__version", 1)

        # Migrate to latest version
        while version < LATEST_VERSION:
            migration = self.migrations.get((version, version + 1))
            if migration:
                event = migration(event)
                version += 1

        return event

    def v1_to_v2(self, event):
        return {**event, "amount": 0, "__version": 2}

    def v2_to_v3(self, event):
        return {
            "user_id": hash(event["user"]),
            "event": event["action"],
            "cart_value": event.get("amount", 0.0),
            "__version": 3
        }
```

**Benefits**:
- Old events remain readable
- Gradual migration (no flag day)
- Consumers see consistent schema

**Trade-offs**:
- Migration overhead (parse + transform)
- Schema registry complexity
- Can't easily roll back schema changes

### When to Use
- Event sourcing systems
- Long-lived event logs (years)
- Multiple consumer versions in production

## Pattern 7: Content-Addressable String Storage

### Context
System with many large strings (documents, code, configs) with significant duplication.

### Problem
- Storing duplicate strings wastes space
- Hard to detect duplicates (compare all pairs)
- Version control of string data

### Solution: Content-Addressed Storage (CAS)

```
Strings → Hash → Deduplicated Storage
─────────────────────────────────────
"hello"  → SHA256 → /objects/5d41...
"world"  → SHA256 → /objects/7c21...
"hello"  → SHA256 → /objects/5d41... (reused!)
```

**Implementation**:
```python
import hashlib

class ContentAddressedStore:
    def __init__(self, storage_path):
        self.storage = storage_path

    def store(self, content: str) -> str:
        # Hash determines location
        content_hash = hashlib.sha256(
            content.encode('utf-8')
        ).hexdigest()

        path = self.storage / content_hash

        # Only write if not exists (deduplication)
        if not path.exists():
            path.write_text(content, encoding='utf-8')

        return content_hash

    def retrieve(self, content_hash: str) -> str:
        path = self.storage / content_hash
        return path.read_text(encoding='utf-8')
```

**Benefits**:
- Automatic deduplication (same content → same hash)
- Immutable storage (hash → content never changes)
- Integrity checking (recompute hash to verify)
- Delta compression (store only diffs)

**Trade-offs**:
- Indirection (hash lookup)
- Can't search content (need separate index)
- Orphan objects (need garbage collection)

### When to Use
- Large documents with versions (git-like)
- Configuration management
- Backup systems with deduplication

## Strategic Recommendations

### Choose Patterns by Scale

| Scale | Pattern | Rationale |
|-------|---------|-----------|
| Small (< 1K QPS) | Simple, inline | Premature optimization wasteful |
| Medium (1K-10K) | Compilation, caching | Clear wins, low complexity |
| Large (10K-100K) | Interning, multi-stage | Optimization pays for itself |
| Very large (> 100K) | CAS, distributed | Architecture-level concerns |

### Evolution Path

1. **Start simple**: Built-in string operations, standard libraries
2. **Measure**: Profile to find actual bottlenecks
3. **Optimize hot paths**: Apply targeted patterns (compilation, interning)
4. **Architect for scale**: When throughput demands, refactor architecture

### Avoid Premature Patterns

❌ Don't implement CAS for 100 documents
❌ Don't build custom intern pool for low cardinality
❌ Don't multi-stage filter for small datasets

✅ Use patterns when you hit limits
✅ Measure before and after
✅ Keep escape hatches (can roll back)
