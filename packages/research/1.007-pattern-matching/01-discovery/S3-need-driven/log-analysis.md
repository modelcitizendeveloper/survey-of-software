# Use Case: Log Analysis (System & Application Logs)

## Who

**Persona**: DevOps engineer, SRE, or security analyst
**Examples**: Parse system logs, application logs, web server logs
**Scale**: GB-TB per day, millions of log lines

## Why (Requirements)

### Functional Requirements
- **Error detection**: Find ERROR, WARNING, CRITICAL patterns
- **Security monitoring**: Detect suspicious patterns (failed logins, SQL injection)
- **Performance analysis**: Extract metrics (response times, status codes)
- **Debugging**: Find specific transaction IDs, user IDs
- **Aggregation**: Group by pattern (count 404s, 500s)

### Non-Functional Requirements
- **Streaming**: Process logs as they arrive (tail -f)
- **Throughput**: Keep up with log generation (100s MB/s)
- **Query flexibility**: Patterns change frequently (ad-hoc queries)
- **Memory efficient**: Can't buffer entire log history
- **Cost-effective**: Run on commodity hardware

## Constraints Analysis

### Pattern Characteristics
- **Multiple patterns**: 10-100 typical (error codes, keywords)
- **Mixed types**: Exact strings ("ERROR"), regex ("IP: \\d+\\.\\d+\\.\\d+\\.\\d+")
- **Dynamic**: Ad-hoc queries (not fixed pattern set)
- **Context-dependent**: "error" in message vs "error" in URL

### Text (Log) Characteristics
- **Structured**: Often key=value or JSON
- **Repetitive**: Same message templates repeated
- **Large volume**: GB-TB per day
- **Streaming**: Continuous arrival (tail -f, log shippers)
- **UTF-8**: Sometimes binary (protocol dumps)

### Performance Constraints
- **Latency**: Alert within seconds (not hours)
- **Throughput**: Process at log generation rate
- **Memory**: Can't load full log history
- **Distributed**: Logs on many servers

## Solution: Hybrid Approach (AC + Regex)

### Primary Recommendation: Purpose-Built Tools

**For Interactive Analysis**: grep, ripgrep, ag
**For Real-Time Monitoring**: ELK stack, Splunk, Datadog
**For Simple Keyword Search**: Aho-Corasick libraries

### Interactive Log Search (grep, ripgrep)

**Tool**: ripgrep (rg)
**Algorithm**: Hybrid (AC for literals, regex for patterns)
**Why**:
- Extremely fast (~10 GB/s single-threaded)
- Supports complex regex
- User-friendly (color output, context)

**Comparison**:
- **grep**: BM variant + regex (~500 MB/s)
- **ag** (Silver Searcher): Similar to ripgrep (~2 GB/s)
- **ripgrep**: Rust regex + SIMD (~10 GB/s)

**Use case**: Manual investigation, ad-hoc queries

### Real-Time Monitoring (Stream Processing)

**Architecture**:
```
App → Log Shipper (Filebeat) → Stream Processor (Logstash) → Storage (Elasticsearch) → Query (Kibana)
```

**Pattern Matching Stage** (Logstash):
- **Grok patterns**: Predefined regex for common formats
- **Aho-Corasick**: For exact keyword matching (custom filters)
- **Regex**: For complex extraction

**Example Grok Pattern**:
```
%{IP:client} \[%{TIMESTAMP_ISO8601:timestamp}\] "%{WORD:method} %{URIPATHPARAM:request}" %{NUMBER:status}
```

### Batch Processing (Historical Analysis)

**Tool**: ELK, Splunk, or custom scripts
**Approach**:
1. Load logs from storage
2. Apply filters (Aho-Corasick for keywords)
3. Extract fields (regex)
4. Aggregate (count, sum, etc.)

## Algorithm Selection

### For Exact Keywords (10-100 patterns)

**Choice**: Aho-Corasick
**Why**:
- Single pass finds all keywords
- O(n + z) regardless of keyword count
- Streaming-friendly

**Example**: Find all log lines with ["ERROR", "CRITICAL", "FATAL", "panic", "exception"]

**Library**:
- Python: pyahocorasick
- Go: cloudflare/ahocorasick
- Rust: aho-corasick crate

### For Complex Patterns (Regex)

**Choice**: Linear-time regex engine (RE2, Rust regex)
**Why**:
- Flexibility (IP addresses, timestamps, custom formats)
- Safety (no catastrophic backtracking)

**Example**: Extract IP addresses: `\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}`

**Library**:
- C++: RE2
- Rust: regex crate
- Go: regexp package (stdlib)

### For Structured Logs (JSON, key=value)

**Choice**: Specialized parser + indexed search
**Why**:
- Parse once, query many times
- Index on keys (faster than pattern matching)

**Example**: Elasticsearch indexes JSON logs, queries by field

## Implementation Patterns

### Pattern 1: Streaming Keyword Extraction

**Goal**: Extract all ERROR lines from live logs

**Pseudocode**:
```python
import pyahocorasick

# Build AC automaton
ac = pyahocorasick.Automaton()
for keyword in ["ERROR", "CRITICAL", "FATAL"]:
    ac.add_word(keyword, keyword)
ac.make_automaton()

# Stream logs
for line in sys.stdin:  # tail -f access.log | python script.py
    for end_pos, keyword in ac.iter(line):
        print(f"{keyword}: {line}")
```

**Performance**: ~500 MB/s (AC overhead minimal)

### Pattern 2: Regex Extraction

**Goal**: Extract HTTP status codes and response times

**Pseudocode**:
```python
import re

pattern = re.compile(r'status=(\d+) time=(\d+)ms')

for line in sys.stdin:
    match = pattern.search(line)
    if match:
        status, time = match.groups()
        # Aggregate metrics
```

**Performance**: ~100-500 MB/s (regex overhead significant)

### Pattern 3: Grok Parsing (Logstash)

**Goal**: Parse structured logs into fields

**Configuration**:
```
filter {
  grok {
    match => { "message" => "%{COMBINEDAPACHELOG}" }
  }
}
```

**Performance**: ~10-100 MB/s (regex-heavy, but flexible)

## Real-World Examples

### Ripgrep (rg)

**Use**: Fast command-line log search
**Algorithm**: Rust regex + memchr (SIMD)
**Performance**: 10 GB/s (single-threaded)
**Feature**: Respects .gitignore, color output

**Example**:
```bash
rg "ERROR" /var/log/*.log  # 10x faster than grep
```

### ELK Stack (Elasticsearch, Logstash, Kibana)

**Architecture**:
- **Logstash**: Ingest, parse (Grok), filter
- **Elasticsearch**: Index, store, search
- **Kibana**: Visualize, query

**Pattern Matching**:
- Grok for parsing (regex-based)
- AC for keyword filtering (custom plugins)
- Elasticsearch query DSL for search

**Scale**: Handles TB/day, distributed

### Splunk

**Use**: Commercial log analysis platform
**Algorithm**: Proprietary (likely AC + regex + indexing)
**Performance**: Processes GB-TB/day
**Feature**: Machine learning, anomaly detection

### Datadog

**Use**: SaaS log management
**Algorithm**: Similar to ELK (indexing + pattern matching)
**Feature**: Real-time alerts, integration with APM

## Performance Characteristics

### Interactive Search (ripgrep)

**Task**: Find "ERROR" in 10 GB log file
**Time**: ~1 second (10 GB/s)
**Memory**: ~10 MB (streaming)

### Real-Time Monitoring (Logstash + AC)

**Task**: Filter 100 keywords from 100 MB/s log stream
**Time**: Real-time (processes faster than generation)
**Memory**: ~100 MB (AC automaton + buffers)

### Batch Analysis (Elasticsearch)

**Task**: Query 1 TB of historical logs
**Time**: ~1-10 seconds (indexed search)
**Memory**: Distributed (shards across nodes)

## Common Pitfalls

### 1. Regex Catastrophic Backtracking

**Problem**: Complex regex on adversarial log line causes hang
**Example**: `(a+)+b` on "aaaaaaa..." (no 'b') → exponential time

**Solution**: Use linear-time regex (RE2, Rust regex)

### 2. Not Handling Multi-Line Logs

**Problem**: Stack traces span multiple lines, patterns split
**Example**: Java exception split across 10 lines

**Solution**: Use multi-line mode or reconstruct events before matching

### 3. Case Sensitivity Mismatch

**Problem**: Log says "Error" but pattern is "ERROR"
**Result**: Missed matches

**Solution**: Case-insensitive matching (AC flag, regex (?i))

### 4. Memory Exhaustion (Buffering)

**Problem**: Buffering entire log file before processing
**Example**: Load 100 GB log → OOM

**Solution**: Stream processing (line-by-line)

### 5. Ignoring Timestamp Ordering

**Problem**: Logs from distributed system out-of-order
**Example**: Alert fires before error logged

**Solution**: Buffer recent lines, sort by timestamp

## Optimization Strategies

### For High Volume (>1 GB/s)

**Strategy**: Parallel processing
```
Logs → Load Balancer → Worker 1 (AC + Regex)
                     → Worker 2 (AC + Regex)
                     → Worker N (AC + Regex)
                     → Aggregator
```

**Libraries**: Apache Kafka (streaming), Flink (stream processing)

### For Many Patterns (>1000 keywords)

**Strategy**: Use Aho-Corasick (not regex × k)
- Build AC once for all keywords
- Single pass through logs

**Performance**: O(n + z) regardless of keyword count

### For Complex Extraction

**Strategy**: Two-pass approach
1. **First pass (fast)**: AC to filter relevant lines
2. **Second pass (slow)**: Regex extraction on matches only

**Example**: Filter for "ERROR" lines first, then parse details

## Key Takeaways

**Best Choice Depends on Use Case**:
- **Interactive search**: ripgrep (fast, user-friendly)
- **Real-time monitoring**: ELK or Splunk (indexed search)
- **Simple keyword extraction**: Aho-Corasick (pyahocorasick, Go/Rust libs)
- **Complex patterns**: Linear-time regex (RE2, Rust regex)

**Algorithm Recommendations**:
- **10-100 keywords**: Aho-Corasick
- **Regex needed**: RE2 or Rust regex (linear time)
- **Mixed**: Hybrid (AC for keywords, regex for structure)

**Performance Priorities**:
1. **Throughput**: Must process faster than log generation
2. **Latency**: Alerts within seconds (for monitoring)
3. **Memory**: Streaming (don't buffer entire logs)

**Avoid**:
- Running regex × k times (use AC for keywords)
- Backtracking regex on untrusted input
- Loading entire log files into memory

**Production Pattern**:
- Structured logging (JSON, key=value)
- Index logs (Elasticsearch, Splunk)
- Query index (much faster than pattern matching)

**Pattern matching is a fallback**: Modern log systems index first, match second
