# S2-Comprehensive: Technical Architecture Analysis

**Research Date**: 2026-01-16
**Duration**: Extended technical deep-dive
**Focus**: Mathematical formulas, memory models, implementation details

---

## SM-2 Algorithm Technical Architecture

### Mathematical Foundation

**Core Formula: Easiness Factor (EF)**

```
EF' = EF + (0.1 - (5-q) * (0.08 + (5-q) * 0.02))
```

Where:
- `EF'` = New easiness factor
- `EF` = Old easiness factor
- `q` = Quality of response (0-5 grade scale)

**Initial Values**:
- All items start with `EF = 2.5`
- Minimum allowed: `EF = 1.3` (if calculated EF < 1.3, set to 1.3)

**Sources**:
- [SuperMemo 2: Algorithm](https://super-memory.com/english/ol/sm2.htm)
- [SM-2 Algorithm Explained](https://tegaru.app/en/blog/sm2-algorithm-explained)

### Interval Calculation

```
I(1) = 1 day
I(2) = 6 days
For n > 2: I(n) = I(n-1) * EF
```

Where:
- `I(n)` = Inter-repetition interval after the n-th repetition (in days)
- `EF` = E-Factor of the item

**Sources**:
- [SuperMemo 2: Algorithm](https://super-memory.com/english/ol/sm2.htm)

### Quality Rating Scale (0-5)

| Grade | Meaning |
|-------|---------|
| **5** | Perfect response |
| **4** | Correct response after hesitation |
| **3** | Correct response with serious difficulty |
| **2** | Incorrect; correct one seemed easy to recall |
| **1** | Incorrect; correct one remembered |
| **0** | Complete blackout |

**Logic**:
- If `q >= 3` (correct): Proceed with normal interval progression
- If `q < 3` (incorrect): Reset `n = 0`, `I = 1`, EF unchanged

**Sources**:
- [SM-2 Algorithm Explained](https://tegaru.app/en/blog/sm2-algorithm-explained)
- [SATHEE: SM-2 Algorithm](https://sathee.iitk.ac.in/pyqs/spaced-repetition/algorithms/sm2-algorithm/)

### Three Core Variables

1. **Repetition Number (n)**: Count of successful reviews
2. **Easiness Factor (EF)**: Difficulty rating (1.1 to 2.5)
3. **Interval (I)**: Days until next review

### Limitations

1. **Hardcoded Initial Intervals**: 1-day and 6-day first intervals don't account for individual differences
2. **Static Difficulty**: Assumes item difficulty is constant over time
3. **Coarse Granularity**: 6-point scale (0-5) lacks nuance
4. **No Forgetting Curve**: Doesn't model retrievability probability

**Sources**:
- [Application of a computer to improve results](https://www.supermemo.com/en/archives1990-2015/english/ol/sm2)

---

## SM-18 Algorithm Technical Architecture

### Two-Component Model of Memory

**Fundamental Variables**:

1. **Stability (S)**: Duration of memory if undisturbed (measured in days)
2. **Retrievability (R)**: Probability of successful recall at any given time

**Theory**: Two variables are sufficient to describe the status of unitary memory

**Sources**:
- [Two components of memory](https://supermemo.guru/wiki/Two_components_of_memory)
- [Algorithm SM-17](https://supermemo.guru/wiki/Algorithm_SM-17)

### Key Improvements Over SM-17

1. **Dynamic Item Difficulty**: Departure from assumption that difficulty is constant
   - Evidence: Dramatic changes in item difficulty during learning
   - Explanation: **Anchoring** - new mnemonic context converts difficult → easy overnight

2. **Improved Stabilization Function**: Better approximation of memory stability increase

3. **Parameter Optimizations**: Several minor tuning improvements

**Sources**:
- [Algorithm SM-18](https://supermemo.guru/wiki/Algorithm_SM-18)
- [SuperMemo Algorithm](https://help.supermemo.org/wiki/SuperMemo_Algorithm)

### Stabilization Function

**Inputs**:
- Stability at review (S, in days)
- Retrievability at review (R)
- Memory complexity (item difficulty)

**Outputs**:
- New stability (S')

**Implementation**: Uses memory matrices:
- **Stabilization matrix (SInc[])**: Stores stability increase factors
- **Recall matrix (Recall[])**: Stores recall probabilities

**Sources**:
- [Algorithm SM-18](https://supermemo.guru/wiki/Algorithm_SM-18)
- [Stabilization](https://supermemo.guru/wiki/Stabilization)

### Release and Status

- **Release Date**: 2019 (May)
- **Used in**: SuperMemo 18
- **Predecessor**: SM-17 (2016) - first two-component model implementation
- **Availability**: Proprietary (licensing required)

**Sources**:
- [SuperMemo - Wikipedia](https://en.wikipedia.org/wiki/SuperMemo)
- [SuperMemo Algorithm](https://help.supermemo.org/wiki/SuperMemo_Algorithm)

---

## FSRS Algorithm Technical Architecture

### DSR Model (Difficulty, Stability, Retrievability)

**Origin**: DHP model from MaiMemo (variant of DSR model)

**Three Core Variables**:

1. **Retrievability (R)**: Probability of successful recall at given moment
   - Depends on: Time elapsed since last review, memory stability (S)

2. **Stability (S)**: Time (days) for R to decrease from 100% to 90%
   - Example: `S = 365` → entire year before recall probability drops to 90%

3. **Difficulty (D)**: Inherent complexity of information
   - Affects: How fast stability grows after each review

**Sources**:
- [The Algorithm](https://github.com/open-spaced-repetition/fsrs4anki/wiki/The-Algorithm)
- [A technical explanation of FSRS](https://expertium.github.io/Algorithm.html)

### Mathematical Formulas

**Retrievability Formula (Forgetting Curve)**:

```
R(t, S) = (1.0 + F * (t / S))^C
```

Where:
- `F = 19.0 / 81.0` (decay factor)
- `C = -0.5` (decay power)
- `t` = Time elapsed since review
- `S` = Stability

**Sources**:
- [Implementing FSRS in 100 Lines](https://borretti.me/article/implementing-fsrs-in-100-lines)
- [The fundamental of FSRS](https://github.com/open-spaced-repetition/fsrs4anki/wiki/The-fundamental-of-FSRS/8c793cefb3ec361cd6fa6ab8f750e31c3da57e8e)

### FSRS-6 Parameters

**Version**: FSRS-6 (latest as of 2026)
**Parameter Count**: 21 parameters (denoted as $w_i$)

**Purpose**: Used in formulas for D, S, and R calculations

**Training**: Machine learning optimizes parameters to best fit user's review history

**Sources**:
- [The Algorithm](https://github.com/open-spaced-repetition/fsrs4anki/wiki/The-Algorithm)
- [Technical Principles of FSRS](https://www.oreateai.com/blog/technical-principles-and-application-prospects-of-the-free-spaced-repetition-scheduler-fsrs/36ee752bd462235d0d5b903059bc8684)

### Implementation Details

**Card State**:
- **Retrievability**: Computed dynamically
- **Stability**: Property of card object (persistent)
- **Difficulty**: Property of card object (persistent)

**Algorithm Flow**:
1. Calculate current retrievability (R)
2. Update stability (S) and difficulty (D) after review
3. Calculate next review interval
4. Schedule card for that day

**Sources**:
- [Implementing FSRS in 100 Lines](https://borretti.me/article/implementing-fsrs-in-100-lines)
- [ABC of FSRS](https://github.com/open-spaced-repetition/fsrs4anki/wiki/abc-of-fsrs)

### Training Data

- **Initial (2023)**: 700M reviews from 20K users
- **Current (2026)**: ~1.7B reviews from 20K Anki users

**Sources**:
- [The History of FSRS for Anki](https://www.lesswrong.com/posts/G7fpGCi8r7nCKXsQk/the-history-of-fsrs-for-anki)

---

## Comparative Technical Analysis

### Memory Model Comparison

| Feature | SM-2 | SM-18 | FSRS |
|---------|------|-------|------|
| **Variables** | n, EF, I | S, R | D, S, R |
| **Difficulty** | Static (EF) | Dynamic | Dynamic |
| **Forgetting Curve** | No | Yes | Yes |
| **Retrievability** | No | Yes | Yes |
| **Parameters** | 0 (hardcoded) | Proprietary | 21 (ML-optimized) |

### Formula Complexity

**SM-2**: Simple arithmetic (linear EF adjustment)
- Easiest to understand and implement
- ~50 lines of code

**FSRS**: Moderate complexity (power functions, 21 parameters)
- Can be implemented in ~100 lines
- Requires parameter optimization (ML)

**SM-18**: High complexity (proprietary matrices)
- Full implementation details not publicly available
- Requires SuperMemo licensing

### Implementation Comparison

| Algorithm | Lines of Code | Dependencies | Optimization Required |
|-----------|---------------|--------------|----------------------|
| **SM-2** | ~50 | None | No |
| **FSRS** | ~100-200 | ML for training | Yes (21 parameters) |
| **SM-18** | Unknown | Proprietary | Yes (matrices) |

**Sources**:
- [Implementing FSRS in 100 Lines](https://borretti.me/article/implementing-fsrs-in-100-lines)
- [GitHub - cnnrhill/sm-2](https://github.com/cnnrhill/sm-2)

---

## Performance Benchmarks (2025)

### Algorithm Success Rates

| Algorithm | Success Rate |
|-----------|--------------|
| **LECTOR** | 90.2% |
| **FSRS** | 89.6% |
| **SSP-MMC** | 88.4% |
| **Anki SM-2** | 60.5% |
| **SM-2** | 47.1% |

**Note**: SM-18/SM-20 data not included (proprietary benchmarks)

**Sources**:
- [LECTOR: LLM-Enhanced Concept-based Test-Oriented Repetition](https://arxiv.org/html/2508.03275v1)
- [Benchmark of Spaced Repetition Algorithms](https://expertium.github.io/Benchmark.html)

### Review Efficiency

**FSRS vs SM-2**:
- **20-30% fewer reviews** for same retention level
- Example: 90% retention with FSRS requires 70-80% of SM-2 review count

**SM-2 vs Traditional Methods**:
- **50-70% time reduction** compared to non-SRS methods

**Sources**:
- [What spaced repetition algorithm does Anki use?](https://faqs.ankiweb.net/what-spaced-repetition-algorithm)
- [FSRS vs SM-2 Guide](https://memoforge.app/blog/fsrs-vs-sm2-anki-algorithm-guide-2025/)

---

## Python Library Implementations

### SM-2 Libraries

1. **anki-sm-2** (GitHub: open-spaced-repetition)
   - Implements Anki's SM-2-based algorithm
   - Available on PyPI
   - Active maintenance

2. **sm-2** (GitHub: open-spaced-repetition)
   - Standalone SM-2 implementation
   - Minimal dependencies

3. **supermemo2** (PyPI)
   - Pure Python implementation
   - Simple API

**Sources**:
- [GitHub - anki-sm-2](https://github.com/open-spaced-repetition/anki-sm-2)
- [GitHub - sm-2](https://github.com/open-spaced-repetition/sm-2)
- [supermemo2 · PyPI](https://pypi.org/project/supermemo2/)

### FSRS Libraries

1. **fsrs-rs-python**
   - Python bindings for fsrs-rs (Rust implementation)
   - Size: 6MB (vs 2GB pure Python)
   - Performance optimized

2. **py-fsrs**
   - Pure Python implementation
   - Optimization-focused

3. **fsrs4anki**
   - Anki integration
   - Includes helper utilities
   - Active development

**Sources**:
- [Open Spaced Repetition GitHub](https://github.com/open-spaced-repetition)
- [GitHub - fsrs4anki](https://github.com/open-spaced-repetition/fsrs4anki)

### Library Comparison

| Library | Language | Size | Performance | Maintenance |
|---------|----------|------|-------------|-------------|
| **anki-sm-2** | Python | Small | Fast | Active |
| **fsrs-rs-python** | Rust + Python | 6MB | Very Fast | Active |
| **py-fsrs** | Python | Medium | Moderate | Active |

---

## Integration Complexity

### SM-2 Integration

**Complexity**: Low
- Simple state (3 variables per card)
- No training required
- Stateless (no cross-card dependencies)

**Typical Integration Steps**:
1. Install library: `pip install supermemo2`
2. Initialize card state (n=0, EF=2.5, I=0)
3. After each review: Pass quality (0-5), get next interval
4. Store updated state

**Code Example** (pseudocode):
```python
from supermemo2 import SMTwo

card = SMTwo(quality=0, interval=0, repetitions=0, efactor=2.5)
quality = 4  # User rated "correct after hesitation"
card.review(quality)
next_interval = card.interval  # Days until next review
```

**Sources**:
- [supermemo2 · PyPI](https://pypi.org/project/supermemo2/)
- [GitHub - thyagoluciano/sm2](https://github.com/thyagoluciano/sm2)

### FSRS Integration

**Complexity**: Moderate
- Complex state (D, S, R per card)
- Requires parameter optimization (initial training)
- Benefits from large review history dataset

**Typical Integration Steps**:
1. Install library: `pip install fsrs`
2. Collect user review history (if available)
3. Optimize 21 parameters using ML (or use defaults)
4. Initialize card state (D, S)
5. After each review: Calculate R, update D/S, get next interval
6. Periodically re-optimize parameters

**Anki Integration** (built-in as of 23.10):
- Toggle FSRS in Deck Options → Advanced section
- Anki auto-optimizes parameters from review history
- Migration: 1-5 minutes depending on deck size

**Sources**:
- [How to use FSRS on Anki](https://forums.ankiweb.net/t/how-to-use-the-next-generation-spaced-repetition-algorithm-fsrs-on-anki/25415)
- [ABC of FSRS](https://github.com/open-spaced-repetition/fsrs4anki/wiki/abc-of-fsrs)

### SM-18 Integration

**Complexity**: Not Applicable (Proprietary)
- Requires SuperMemo license
- Source code not publicly available
- Integration only possible via SuperMemo API (expected 2026)

**Sources**:
- [SuperMemo Algorithm FAQ](https://supermemopedia.com/wiki/SuperMemo_Algorithm_FAQ)

---

## Production Considerations

### Scalability

**SM-2**:
- ✅ Scales to millions of cards (stateless, simple calculations)
- ✅ Constant-time operations
- ✅ No training required

**FSRS**:
- ✅ Scales to millions of cards (per-card state)
- ⚠️ Parameter optimization requires significant review history
- ⚠️ Retraining becomes expensive with large datasets

**SM-18**:
- ✅ Production-proven in SuperMemo
- ⚠️ Proprietary licensing required

### Observability

**SM-2**:
- Simple metrics: EF distribution, interval distribution
- Easy to debug (few variables)

**FSRS**:
- Complex metrics: D/S/R distributions, parameter values
- Requires visualization tools for debugging
- FSRS Helper add-on provides observability

**Sources**:
- [FSRS Helper](https://ankiweb.net/shared/info/759844606)

### Maintenance Burden

| Algorithm | Setup Time | Ongoing Maintenance | Retraining Frequency |
|-----------|------------|---------------------|----------------------|
| **SM-2** | Minutes | None | Never |
| **FSRS** | 1-5 min (migration) | Low | Optional (monthly) |
| **SM-18** | N/A (proprietary) | SuperMemo handles | Unknown |

---

## Summary

### SM-2 Strengths
- ✅ Simplicity (50 lines of code)
- ✅ Zero-configuration
- ✅ Well-understood (40+ years of use)
- ✅ No training required
- ❌ Lower performance (47-60% success rate)
- ❌ Static difficulty assumption

### FSRS Strengths
- ✅ High performance (89.6% success rate)
- ✅ 20-30% fewer reviews than SM-2
- ✅ Dynamic difficulty modeling
- ✅ Open-source, ML-optimized
- ❌ More complex (100-200 lines, 21 parameters)
- ❌ Requires optimization step

### SM-18 Strengths
- ✅ Most advanced model (two-component memory)
- ✅ Dynamic difficulty (anchoring effects)
- ✅ Production-proven (SuperMemo)
- ❌ Proprietary (licensing required)
- ❌ Not available for open-source projects
- ❌ No public benchmarks

---

**Research Duration**: 3 hours
**Primary Sources**: Official documentation, mathematical papers, implementation guides
**Confidence Level**: High for SM-2 and FSRS, Medium for SM-18 (proprietary, limited public info)
