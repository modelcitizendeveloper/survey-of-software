# Ecosystem Maturity Assessment

## Maturity Indicators (Research-Based)

### SimPy: Most Mature
**Age**: 20+ years (since 2002)
**Evidence**:
- Survived 3 major version rewrites (v2, v3, v4)
- Active Google Group with 1000+ messages
- Extensive Stack Overflow presence
- Real Python tutorial (indicates mainstream adoption)
- DataCamp course (commercial educational validation)

**Maturity score**: 10/10
**Long-term viability**: HIGH (proven staying power)

---

### Mesa: Academically Mature
**Age**: 10 years (since ~2015)
**Evidence**:
- JOSS publication (2025): "Mesa 3: Agent-based modeling with Python in 2025"
- Google Summer of Code participation (2024, 2025)
- 3,100 GitHub stars (high engagement)
- Active development (version 3.x in 2024-2025)
- Example models repository

**Maturity score**: 8/10
**Long-term viability**: HIGH (academic backing, active development)

---

### salabim: Recently Mature
**Age**: 7 years (JOSS paper 2018)
**Evidence**:
- JOSS publication validates academic quality
- Active development (version 25.0.12 in 2025)
- Comprehensive manual
- Smaller community (~100-200 stars)

**Maturity score**: 7/10
**Long-term viability**: MEDIUM (active development, but smaller community)

---

### Ciw: Academic Tool
**Age**: 7-8 years (paper ~2017)
**Evidence**:
- Published research paper
- 128 GitHub stars
- Active maintenance (version 3.1.4)
- Academic focus (queueing theory)

**Maturity score**: 7/10
**Long-term viability**: MEDIUM (niche tool, academic support)

---

### desmod: Corporate Tool
**Age**: 8-9 years (~2016)
**Evidence**:
- Corporate backing (Western Digital)
- ReadTheDocs documentation
- <100 GitHub stars (low public visibility)
- Stable but slow update cycle

**Maturity score**: 7/10
**Long-term viability**: MEDIUM (corporate dependency risk)

---

## Development Activity Trends (2024-2025)

| Library | Recent Activity | Indicator |
|---------|----------------|-----------|
| SimPy | Regular releases | Stable maintenance |
| Mesa | Major v3.0 release | Active innovation |
| salabim | Frequent updates | Active development |
| Ciw | Incremental updates | Stable maintenance |
| desmod | Slow cycle | Corporate priority dependent |

---

## Community Health Metrics

| Library | GitHub Stars | PyPI Downloads | Community Activity |
|---------|-------------|----------------|-------------------|
| SimPy | N/A (GitLab) | High (inferred) | Google Group, SO active |
| Mesa | 3,100 | Medium | GitHub discussions active |
| salabim | ~100-200 | Low (974/week found) | Smaller, responsive |
| Ciw | 128 | Low | Academic niche |
| desmod | <100 | Very low | Corporate focus |

---

## Dependency Risk

**SimPy**: Minimal dependencies (Python stdlib only) → LOW RISK
**salabim**: Greenlet dependency → MEDIUM RISK (additional dependency)
**Ciw**: Minimal dependencies → LOW RISK
**Mesa**: More dependencies (visualization stack) → MEDIUM RISK
**desmod**: Depends on SimPy → LOW RISK (leverages SimPy's stability)

---

## Summary

**Most mature**: SimPy (20+ years, proven longevity)
**Fastest growing**: Mesa (academic backing, GSoC, major releases)
**Stable niche**: Ciw (queueing focus, academic support)
**Active alternative**: salabim (frequent updates, unique features)
**Corporate tool**: desmod (stable, but visibility low)

**Recommendation**: For long-term projects, SimPy and Mesa have strongest maturity indicators.
