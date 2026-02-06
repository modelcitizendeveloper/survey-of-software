# S2 Approach: Comprehensive Discovery

## What S2 Discovers

S2 answers: **HOW do these tokenization libraries work?**

Focus: Deep technical analysis, algorithms, optimization trade-offs.

## Coverage

### Algorithm Details
- Internal architecture (BiLSTM-CRF, Transformer, etc.)
- Dictionary structures and lookup mechanisms
- Unknown word handling (HMM, neural models)
- Probability calculations and scoring

### Technical Trade-offs
- Vocabulary size vs sequence length
- Memory vs speed optimizations
- CPU vs GPU requirements
- Character vs word vs subword granularity

### Implementation Details
- Training procedures (for neural models)
- Configuration parameters and their effects
- Performance tuning options
- Integration patterns

## Evaluation Methodology

For each library, S2 examines:
- **Architecture**: How it segments text internally
- **Training approach**: What data it needs, how it learns
- **Configuration**: Critical parameters and their impact
- **Feature matrix**: Comprehensive capability comparison
- **Optimization trade-offs**: What you sacrifice for what gains

## S2 Does NOT Cover

- Quick decision-making → See S1
- Specific use cases → See S3
- Strategic viability → See S4

## Reading Time

~30-45 minutes for complete S2 pass
