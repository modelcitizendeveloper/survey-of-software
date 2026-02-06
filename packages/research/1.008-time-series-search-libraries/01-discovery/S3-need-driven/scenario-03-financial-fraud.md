# Scenario 3: Financial Fraud Detection

## Business Context

**Industry**: Financial Services (Banks, Payment Processors, Cryptocurrency Exchanges)
**Pain Point**: Transaction pattern fraud detection
**Current Approach**: Rule-based systems + manual investigation
**Cost**: $5-10B annual fraud losses globally, 95% false positive rate

## Use Case: Motif Discovery for Fraud Patterns

### Problem Statement

Credit card fraud patterns evolve faster than rule updates. Need unsupervised discovery of suspicious transaction patterns (rapid small purchases before large withdrawal, circular money movement between accounts, ATM skimming signatures).

### Data Profile

- **Volume**: 1M transactions/day per mid-size bank
- **Features**: Transaction amount, time, merchant category, location
- **Pattern length**: 5-20 transactions (fraud schemes span hours to days)
- **Labeled data**: <1% (fraud is rare, labels lag investigation by weeks)

## Recommended Solution: STUMPY for Motif Discovery

### Rationale

**Why STUMPY**:
1. **Unsupervised**: Finds recurring patterns without labels
2. **Motif discovery**: Identifies repeated fraud schemes automatically
3. **AB-joins**: Compares transaction sequences across accounts (finds coordinated fraud)
4. **Performance**: Can process millions of transaction sequences

```python
import stumpy
import numpy as np

# Convert transactions to time series (amount over time per account)
account_sequences = transactions.groupby('account_id').apply(
    lambda x: x.sort_values('timestamp')['amount'].values
)

# Find recurring patterns across all accounts (motifs = potential fraud rings)
mp = stumpy.stump(np.concatenate(account_sequences), m=10)  # 10-transaction windows
motifs = stumpy.motifs(mp, max_motifs=100)

# For each motif, find all occurrences across accounts
for motif_idx, motif_distances in motifs:
    accounts_with_pattern = find_accounts_with_pattern(motif_idx)
    if len(accounts_with_pattern) > 5:
        # Same pattern in 5+ accounts = likely fraud ring
        flag_for_investigation(accounts_with_pattern, pattern=motif_idx)
```

### Expected Outcomes

- Fraud detection rate: 60% → 85% (+25% more fraud caught)
- False positive rate: 95% → 30% (-65% fewer false alarms)
- **Novel pattern discovery**: 15-20 new fraud schemes detected per quarter
- **Investigation efficiency**: 70% reduction in analyst time per alert

### ROI

- **Implementation cost**: $100K (3 months, 2 engineers)
- **Annual benefit**: $5M (prevented fraud) + $500K (reduced investigation labor)
- **Payback**: 1 week

## Alternative: tsfresh + Isolation Forest

**When to use**: If you have labeled fraud examples and want feature-based detection

```python
from tsfresh import extract_features
from sklearn.ensemble import IsolationForest

# Extract 794 features from transaction sequences
features = extract_features(transactions, column_id='account_id', column_sort='timestamp')

# Train Isolation Forest on normal transactions
clf = IsolationForest(contamination=0.01)  # Expect 1% fraud
clf.fit(features[labels == 'normal'])

# Detect anomalies
predictions = clf.predict(features)  # -1 = fraud, 1 = normal
```

**Trade-offs**:
- ✅ Can incorporate labeled fraud examples
- ✅ Feature importance helps investigators understand "why" flagged
- ❌ Doesn't find motifs (repeated patterns across accounts)
- ❌ Slower (feature extraction on millions of transactions)

## Success Metrics

- **Fraud detection rate**: 85%+ (benchmark: 60% baseline)
- **False positive rate**: <35% (benchmark: 95% baseline)
- **Novel pattern detection**: 10+ new schemes per quarter
- **Investigation time per alert**: <30 minutes (benchmark: 2 hours)
- **Time to detection**: <24 hours from first fraudulent transaction

## References

- Matrix Profile for fraud detection: Gharghabi et al. (2019) - "Matrix Profile XII: MPdist: A Novel Time Series Distance Measure to Allow Data Mining in More Challenging Scenarios"
- Financial fraud patterns: Yeh et al. (2017) - "Time Series Joins, Motifs, Discords and Shapelets: a Unifying View that Exploits the Matrix Profile"
