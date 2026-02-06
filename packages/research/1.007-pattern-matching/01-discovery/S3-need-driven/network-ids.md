# Use Case: Network Intrusion Detection System (IDS)

## Who

**Persona**: Security engineer deploying network IDS
**Examples**: Snort, Suricata, Zeek (Bro)
**Scale**: 1-100 Gbps network traffic, 10K-1M attack signatures

## Why (Requirements)

### Functional Requirements
- **Deep packet inspection (DPI)**: Scan packet payloads for attack signatures
- **Multiple patterns**: Thousands to millions of signatures simultaneously
- **Real-time**: Must keep up with network speed (can't buffer indefinitely)
- **All matches**: Report every signature match (not just first)
- **Rule updates**: Add/remove signatures dynamically

### Non-Functional Requirements
- **Throughput**: Sustain 1-100 Gbps without packet loss
- **Latency**: <1ms per packet (minimal delay)
- **Memory bounded**: Can't use unlimited RAM for buffering
- **Zero false negatives**: Missing attack unacceptable
- **Low false positives**: Avoid alert fatigue

## Constraints Analysis

### Pattern Characteristics
- **Thousands of patterns**: 10K-100K typical, 1M+ for comprehensive
- **Variable length**: 5-500 bytes typical
- **Mostly byte strings**: Binary protocol patterns (not just text)
- **Some regex**: Complex patterns (HTTP headers, SQL injection)
- **Frequent updates**: New exploits discovered daily

### Text (Traffic) Characteristics
- **Streaming**: Packets arrive continuously
- **Small chunks**: Typical packet 64-1500 bytes
- **Binary data**: Not just text (protocols, encryption, media)
- **High volume**: Gigabits to terabits per second

### Performance Constraints
- **Throughput critical**: Must match wire speed
- **CPU-bound**: Pattern matching is main bottleneck
- **Memory limited**: Can't buffer many packets
- **Real-time**: Can't batch process later

## Solution: Aho-Corasick + Hyperscan

### Primary Recommendation: Hyperscan

**Choice**: Intel Hyperscan library
**Why**:
- Specifically designed for network IDS use case
- Handles 10K-1M+ patterns efficiently
- SIMD-optimized: 10-100 GB/s throughput
- Used by Snort, Suricata (production-proven)

**Architecture**:
- Hybrid DFA + NFA
- SIMD parallel state transitions
- Compressed pattern matching automaton
- Supports regex (limited) + exact strings

### Algorithm Rationale

**Why Aho-Corasick Foundation**:
- **O(n + z) time**: Linear in traffic, regardless of signature count
- **Single pass**: Scan each packet once, find all matches
- **Streaming**: No backtracking, processes byte-by-byte

**Why NOT other algorithms**:
- **Boyer-Moore × k**: O(k × n) where k = 10,000 → Infeasible
  - 1 GB/s per pattern → 10 TB/s for 10K patterns (impossible)
- **Rabin-Karp**: Hash collisions unpredictable, not deterministic
- **Naive**: O(nm × k) → Completely infeasible

**Why Hyperscan over vanilla AC**:
- **SIMD**: Check 32 bytes in parallel (AVX2)
- **DFA optimization**: Larger automaton but faster transitions
- **Hardware-aware**: Tuned for Intel x86 cache, prefetch
- **Compression**: Reduces memory footprint
- **Result**: 10-50x faster than naive AC implementation

### Architecture Overview

**Pattern Compilation (Offline)**:
```
Signatures (text rules)
  ↓
Parse & normalize
  ↓
Build Hyperscan database
  ↓
Compile to optimized DFA/NFA
  ↓
Load into memory (read-only)
```

**Runtime Matching (Online)**:
```
Packet arrives
  ↓
Extract payload
  ↓
Scan with Hyperscan
  ↓
Matches → Alert
  ↓
Continue to next packet
```

## Implementation Details

### Pattern Compilation

**Offline (on rule update)**:
```c
hs_database_t *database;
hs_compile_error_t *error;

// Compile 10K patterns into database
hs_error_t err = hs_compile_multi(
    patterns,        // Array of pattern strings
    flags,           // CASELESS, DOTALL, etc.
    ids,             // Pattern IDs for matches
    pattern_count,   // 10,000
    HS_MODE_BLOCK,   // Scan mode
    NULL,            // Platform (auto-detect)
    &database,
    &error
);
```

**Result**: Compiled database (100 MB-1 GB typical)

### Runtime Scanning

**For each packet**:
```c
hs_error_t err = hs_scan(
    database,       // Pre-compiled patterns
    packet_data,    // Packet payload
    packet_length,  // Bytes to scan
    0,              // Flags
    scratch,        // Scratch space (per-thread)
    match_callback, // Called for each match
    context         // User data
);
```

**Throughput**: 10-100 GB/s depending on pattern complexity

### Multi-Threading

**Per-Core Pattern Matching**:
```
NIC → Packet Distributor → Core 0 (Hyperscan instance)
                         → Core 1 (Hyperscan instance)
                         → Core 2 (Hyperscan instance)
                         → ... → Alert Aggregator
```

**Key**: Each core has own scratch space (thread-safe)

## Alternatives

### If ARM Platform (No Hyperscan)

**Problem**: Hyperscan requires x86 SSSE3+
**Solution**: Vectorscan (Hyperscan fork for ARM)
- ~80% performance of Hyperscan
- Supports ARM NEON SIMD

### If Lower Throughput (<1 Gbps)

**Problem**: Hyperscan overhead not needed
**Solution**: Standard Aho-Corasick library
- Python: pyahocorasick
- C: libahocorasick
- Simpler, less memory

### If Need Full Regex (PCRE Features)

**Problem**: Hyperscan regex support limited
**Solution**: Hybrid approach
- Hyperscan for exact string patterns (fast)
- Separate PCRE for complex regex (slower)
- Example: Snort 3.0 uses Hyperscan + PCRE

### If Memory Constrained

**Problem**: Hyperscan database can be GB-sized
**Solution**: Split patterns into groups
- High-priority signatures in memory
- Low-priority on-disk or secondary scan

## Performance Characteristics

### Snort 2 (Pre-Hyperscan)

**Algorithm**: AC + PCRE
**Throughput**: ~1-2 Gbps per core
**Limitation**: CPU-bound, can't keep up with 10G+ links

### Snort 3 / Suricata (With Hyperscan)

**Algorithm**: Hyperscan + PCRE
**Throughput**: ~10-20 Gbps per core
**Scaling**: 100 Gbps with 10-20 cores

### Hyperscan Benchmarks

| Pattern Count | Throughput (Single Core) |
|---------------|--------------------------|
| 1K patterns   | ~15 GB/s |
| 10K patterns  | ~10 GB/s |
| 100K patterns | ~5 GB/s  |
| 1M patterns   | ~2 GB/s  |

*Intel Xeon, AVX2, streaming mode*

## Real-World Examples

### Snort (Cisco)

**Version 2**: AC with Aho-Corasick-Boyer-Moore hybrid
**Version 3**: Hyperscan for exact strings + PCRE for regex
**Rules**: ~50K signatures (Snort community + commercial)
**Performance**: 10+ Gbps with Hyperscan

### Suricata (OISF)

**Algorithm**: Hyperscan (default), Aho-Corasick (fallback)
**Rules**: Compatible with Snort rules
**Performance**: Multi-threaded, scales to 100 Gbps
**Feature**: GPU acceleration experimental

### Zeek (Bro)

**Algorithm**: Custom DFA-based
**Focus**: Protocol analysis + pattern matching
**Performance**: ~10 Gbps typical
**Strength**: Deep protocol parsing

### CloudFlare WAF

**Algorithm**: Custom Aho-Corasick variant
**Rules**: Proprietary attack signatures
**Scale**: Tbps aggregate (millions of servers)
**Feature**: Distributed pattern matching

## Pitfalls to Avoid

### 1. Pattern Explosion

**Problem**: Adding too many patterns slows matching
**Example**: 1M patterns → 2 GB/s (vs 10 GB/s for 10K)

**Solution**: Prune patterns
- Remove duplicates
- Generalize similar patterns
- Prioritize high-severity

### 2. Regex Catastrophic Backtracking

**Problem**: Complex regex causes exponential time
**Example**: `(a+)+b` on "aaaaa..." hangs

**Solution**: Use Hyperscan (bounded NFA) or RE2 (linear time)

### 3. False Positives

**Problem**: Generic patterns match benign traffic
**Example**: Pattern "GET /" matches all HTTP

**Solution**: Context-aware rules
- Protocol decoders (parse HTTP first)
- Combine patterns with metadata checks

### 4. Memory Exhaustion

**Problem**: Hyperscan database too large for RAM
**Example**: 1M patterns → 5 GB database

**Solution**: Tier signatures
- Hot set in memory (critical CVEs)
- Cold set on-demand or secondary scan

### 5. Packet Loss

**Problem**: Can't keep up with network rate, packets dropped
**Example**: 100 Gbps NIC, but matching only 50 Gbps

**Solution**: Scale horizontally
- Multiple servers
- Load balance traffic
- Hardware acceleration (FPGA, SmartNIC)

## Deployment Considerations

### Hardware Requirements

**CPU**: Intel Xeon with SSSE3+ (AVX2 preferred)
**RAM**: 8-32 GB (pattern database + scratch + buffers)
**NIC**: DPDK-capable (bypass kernel for lower latency)
**Cores**: 10-20 cores for 100 Gbps

### Software Stack

**Packet Capture**: DPDK, AF_PACKET, PF_RING
**Pattern Matching**: Hyperscan or Vectorscan
**Protocol Parsing**: Custom or Suricata engine
**Alerting**: Syslog, SIEM integration

### Rule Management

**Updates**: Daily (new CVEs, threat intel)
**Testing**: Stage → validate → deploy
**Rollback**: Keep previous rule set (in case of false positives)

## Key Takeaways

**Best Choice**: Hyperscan (or Vectorscan for ARM)
- Industry standard for IDS/DPI
- 10-100x faster than vanilla AC
- Proven at scale (Snort, Suricata, CloudFlare)

**Critical Requirements**:
- **Multi-pattern**: AC-based (not BM × k)
- **Throughput**: SIMD optimization essential
- **Deterministic**: No probabilistic algorithms (RK)

**Architecture**:
- Compile patterns offline (takes time, that's OK)
- Runtime matching optimized (must be fast)
- Multi-threaded scaling (one core = ~10 Gbps)

**Not Suitable**:
- Boyer-Moore (single pattern, can't scale)
- Naive (O(nm × k) infeasible)
- Rabin-Karp (collisions unacceptable for security)

**Next Level**: Hardware acceleration
- SmartNICs (Netronome, Mellanox)
- FPGAs (custom pattern matching at wire speed)
- P4 programmable switches (in-network DPI)
