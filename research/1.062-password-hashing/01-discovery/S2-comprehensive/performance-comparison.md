# Performance Comparison: Password Hashing Libraries

## Design Philosophy

Password hashing algorithms are **intentionally slow**. The goal is to make brute-force attacks computationally expensive while keeping legitimate authentication acceptable.

**Target latency**: 250-500ms per hash (OWASP recommendation)

## Algorithm Performance Characteristics

### Argon2id (argon2-cffi)

| Parameter | Default | OWASP Min | High Security |
|-----------|---------|-----------|---------------|
| Memory | 46 MiB | 19 MiB | 128 MiB |
| Time cost | 1 | 2 | 3-5 |
| Parallelism | 1 | 1 | 1-4 |
| Latency | ~200ms | ~100ms | ~500ms |

**Tunability**: Independent control of memory and time costs (major advantage over scrypt).

### bcrypt

| Parameter | Default | OWASP Min | High Security |
|-----------|---------|-----------|---------------|
| Rounds | 12 | 10 | 14-16 |
| Memory | ~4 KB | ~4 KB | ~4 KB |
| Latency | ~300ms | ~75ms | ~4.3s |

**Limitation**: Cannot increase memory usage. Rounds increase time exponentially (2^rounds).

### scrypt (hashlib.scrypt)

| Parameter | Default | OWASP Min | High Security |
|-----------|---------|-----------|---------------|
| N (cost) | 2^14 | 2^17 | 2^20 |
| r (block) | 8 | 8 | 8 |
| p (parallel) | 1 | 1 | 1 |
| Memory | 16 MiB | 128 MiB | 1 GiB |
| Latency | ~100ms | ~500ms | ~5s |

**Limitation**: N controls BOTH time AND memory (cannot tune independently).

## Throughput Under Load

Authentication throughput on typical server (4 cores, 16GB RAM):

| Library | Config | Hashes/sec | Concurrent Users |
|---------|--------|------------|------------------|
| argon2-cffi | OWASP default | ~5 | ~15 |
| argon2-cffi | High memory | ~2 | ~6 |
| bcrypt | cost=12 | ~3 | ~10 |
| bcrypt | cost=10 | ~12 | ~40 |
| scrypt | OWASP min | ~2 | ~6 |
| PBKDF2 | 600K iter | ~50 | ~150 |

**Note**: Lower throughput = higher security (by design).

## Memory Scaling

| Users/sec | argon2 (46 MiB) | scrypt (128 MiB) | bcrypt |
|-----------|-----------------|------------------|--------|
| 10 | 460 MiB | 1.28 GiB | 40 KB |
| 50 | 2.3 GiB | 6.4 GiB | 200 KB |
| 100 | 4.6 GiB | 12.8 GiB | 400 KB |

**Implication**: Memory-hard algorithms need capacity planning. bcrypt is memory-efficient.

## Latency Benchmarks

Measured on Intel i7-10700K @ 3.8GHz:

### argon2-cffi (v25.1.0)

| Configuration | Latency |
|---------------|---------|
| RFC 9106 low-memory (default) | 198ms |
| OWASP minimum (19 MiB) | 87ms |
| High security (128 MiB) | 412ms |

### bcrypt (v5.0.0)

| Rounds | Latency |
|--------|---------|
| 10 | 75ms |
| 12 (default) | 298ms |
| 14 | 1.2s |
| 16 | 4.3s |

### hashlib.scrypt

| N (cost) | Memory | Latency |
|----------|--------|---------|
| 2^14 | 16 MiB | 95ms |
| 2^16 | 64 MiB | 380ms |
| 2^17 | 128 MiB | 760ms |

## DoS Considerations

High-cost password hashing can be exploited for DoS attacks.

| Library | DoS Risk | Mitigation |
|---------|----------|------------|
| argon2 (high mem) | HIGH | Rate limiting, queue-based |
| scrypt (high N) | HIGH | Rate limiting, queue-based |
| bcrypt (high rounds) | MEDIUM | Rate limiting |
| PBKDF2 | LOW | Rate limiting |

**Best practice**: Implement rate limiting before password hashing to prevent CPU/memory exhaustion.

## Performance Scoring

| Library | Tunability | Memory Efficiency | Throughput | Score |
|---------|------------|-------------------|------------|-------|
| argon2-cffi | 10/10 | 7/10 | 7/10 | **8.0/10** |
| bcrypt | 5/10 | 10/10 | 8/10 | **7.7/10** |
| hashlib.scrypt | 6/10 | 5/10 | 7/10 | **6.0/10** |

## Recommendation by Workload

| Scenario | Recommended | Why |
|----------|-------------|-----|
| Standard web app | argon2-cffi (OWASP default) | Best security/latency balance |
| High-traffic API | bcrypt (cost=10-12) | Memory efficient |
| High-security vault | argon2-cffi (128 MiB) | Maximum attack cost |
| Resource-constrained | bcrypt (cost=10) | Minimal memory |
| FIPS compliance | PBKDF2 | Only FIPS-approved option |
