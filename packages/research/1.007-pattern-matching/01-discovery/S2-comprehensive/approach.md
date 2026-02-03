# S2 Approach: Comprehensive Discovery

## What S2 Discovers

S2 answers: **HOW do pattern matching algorithms work?**

Focus: Deep technical analysis, algorithm mechanics, optimization trade-offs.

## Coverage

### Algorithm Internals
- Data structures (failure functions, shift tables, automata)
- Step-by-step execution flow
- Preprocessing vs matching phases
- Memory layouts and access patterns

### Technical Trade-offs
- Time complexity (best/average/worst case)
- Space complexity (tables, auxiliary structures)
- Cache behavior and memory locality
- Branch prediction and SIMD opportunities

### Implementation Details
- Edge cases and correctness
- Optimization techniques
- Parallelization opportunities
- Hardware acceleration considerations

## Evaluation Methodology

For each algorithm, S2 examines:
- **Mechanism**: How it avoids redundant comparisons
- **Data structures**: What auxiliary information it maintains
- **Complexity analysis**: Formal time/space bounds
- **Performance characteristics**: When it excels vs struggles
- **Implementation considerations**: Practical optimization opportunities

## S2 Does NOT Cover

- Quick decision-making → See S1
- Specific use cases → See S3
- Strategic viability → See S4
- Code examples → See library documentation

## Reading Time

~30-45 minutes for complete S2 pass
