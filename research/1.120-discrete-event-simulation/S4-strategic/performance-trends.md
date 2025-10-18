# Performance Trends and Scaling

## Python DES Performance Context

**Research finding**: Python DES ~2.2x slower than R-simmer (C++-backed DES).

**Implication**: Python DES is **not** competitive with compiled tools (Simul8, Arena, AnyLogic) for extreme performance.

---

## When Python DES is Sufficient

**Workloads**:
- <1M events
- Batch simulations (not real-time)
- Business modeling (capacity planning, optimization)

**Evidence**: All Python DES libraries handle typical business cases without performance issues.

---

## When to Consider Compiled Tools

**Workloads**:
- >10M events
- Real-time embedded systems
- Performance-critical applications (trading, control systems)

**Alternatives**:
- Simul8, Arena, AnyLogic (commercial)
- C++/Rust DES libraries (custom development)

---

## Scalability Limits

**Mesa-frames (2024)**: Created to address Mesa's performance with large agent counts.

**Implication**: Vanilla Mesa struggles with 10,000+ agents. Mesa-frames uses DataFrame-based approach for better scaling.

---

## Python Performance Mitigations

1. **PyPy**: Alternative Python interpreter (JIT compilation)
2. **Cython**: Compile hot paths to C
3. **Numba**: JIT compile numerical code
4. **Vectorization**: Use pandas/numpy operations (not loops)

---

## Trend: Python Good Enough for Most Use Cases

**Evidence**:
- Growing adoption (DataCamp courses, Real Python tutorials)
- Integration with data science ecosystem (pandas, matplotlib, scipy)
- Academic and industrial use (despite performance gap)

**Conclusion**: Performance rarely a blocker for Python DES in practice.

---

## Summary

Python DES is **adequate for 90% of simulation projects**. Choose Python for ecosystem and usability, not raw speed. For extreme performance, use compiled tools.
