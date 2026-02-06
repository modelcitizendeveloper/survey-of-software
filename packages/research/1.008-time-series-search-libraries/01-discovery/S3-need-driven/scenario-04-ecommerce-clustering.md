# Scenario 4: E-commerce Customer Behavior Clustering

## Business Context

**Industry**: E-commerce, SaaS, Digital Products
**Pain Point**: Personalized recommendations based on purchase timing patterns
**Current Approach**: Collaborative filtering (ignores temporal behavior)
**Opportunity**: 15-30% increase in conversion from time-aware recommendations

## Use Case: Customer Journey Clustering

### Problem Statement

Two customers with identical total purchase amounts have very different behaviors:
- **Customer A**: Steady weekly purchases (loyal subscriber)
- **Customer B**: Burst purchases during sales (discount-driven)

Need clustering based on **temporal patterns** (not just purchase totals) to:
- Segment customers by behavior type
- Personalize offers (A gets loyalty rewards, B gets sale alerts)
- Predict churn (sudden pattern changes indicate risk)

### Data Profile

- **Volume**: 100K active customers, 1M transactions/month
- **Features**: Purchase amount, time between purchases, category mix over time
- **Pattern length**: 30-90 day windows (seasonal behavior)

## Recommended Solution: tslearn TimeSeriesKMeans with DTW

### Rationale

**Why tslearn + DTW**:
1. **DTW distance**: Handles timing variations (customer who buys "late" one month is similar to one who bought "early" next month)
2. **Shape-based clustering**: Groups customers by behavior pattern, not magnitude
3. **Interpretability**: Can visualize cluster centroids to understand each segment

```python
from tslearn.clustering import TimeSeriesKMeans
from tslearn.preprocessing import TimeSeriesScalerMeanVariance
import numpy as np

# Create purchase time series per customer (daily purchase amount, 90-day window)
customer_sequences = transactions.groupby('customer_id').apply(
    lambda x: create_daily_purchase_series(x, days=90)
)
X = np.array(list(customer_sequences.values))  # (100000, 90, 1)

# Normalize to focus on pattern (not magnitude)
X_normalized = TimeSeriesScalerMeanVariance().fit_transform(X)

# Cluster with DTW distance
dtw_kmeans = TimeSeriesKMeans(n_clusters=8, metric="dtw", max_iter=10, random_state=42)
clusters = dtw_kmeans.fit_predict(X_normalized)

# Analyze cluster centroids
for cluster_id in range(8):
    centroid = dtw_kmeans.cluster_centers_[cluster_id]
    customers_in_cluster = np.where(clusters == cluster_id)[0]
    analyze_segment(cluster_id, centroid, customers_in_cluster)
```

### Discovered Segments (Example)

1. **Loyal Subscribers** (22% of customers): Steady weekly purchases, low variance
2. **Sale Hunters** (18%): Burst activity during promotions, dormant otherwise
3. **New Customer Ramp** (15%): Increasing frequency over first 90 days
4. **Churn Risk** (8%): Declining frequency, irregular patterns
5. **Seasonal Shoppers** (12%): Monthly spikes (payday pattern)
6. **Impulse Buyers** (10%): Random large purchases, no pattern
7. **Gift Shoppers** (8%): Annual spikes (holidays, birthdays)
8. **B2B Customers** (7%): Predictable monthly orders

### Personalization Strategies by Segment

**Loyal Subscribers**:
- Reward consistency (loyalty points for streak maintenance)
- Early access to new products
- Subscription savings offers

**Sale Hunters**:
- Alert 24 hours before sales start
- "Flash sale" gamification
- Bundle discounts (increase AOV)

**Churn Risk**:
- Re-engagement campaigns
- Win-back discount (15-20% off next purchase)
- Survey to understand drop-off reason

### Expected Outcomes

- **Conversion rate**: +18% from personalized offers
- **Customer LTV**: +25% from churn reduction
- **Email engagement**: +35% (relevant timing = higher opens)
- **Revenue impact**: $2M/year on $20M revenue base

### ROI

- **Implementation cost**: $75K (2 months, clustering + personalization engine)
- **Annual revenue increase**: $2M
- **Payback**: 2 weeks

## Alternative: STUMPY for Churn Prediction

**When to use**: If you want to detect sudden behavior changes (not just segment)

```python
# For each customer, compare recent 30 days to their historical baseline
for customer_id, purchases in customers.items():
    recent = purchases[-30:]
    historical = purchases[:-30]

    # Matrix profile distance = how different is recent vs. historical
    mp = stumpy.stump(historical, m=7)  # 7-day patterns
    distance = stumpy.match(recent, historical, mp)

    if distance > churn_threshold:
        flag_for_retention_campaign(customer_id, reason='behavior_change')
```

**Trade-offs**:
- ✅ Detects individual customer anomalies (churn prediction)
- ❌ Doesn't create interpretable segments for marketing

## Success Metrics

- **Cluster quality**: Silhouette score >0.4, within-cluster variance <30% of between-cluster
- **Segment stability**: 80%+ customers remain in same segment month-to-month (segments are meaningful)
- **Business impact**: +15%+ conversion from personalized campaigns
- **Churn reduction**: -20% churn in "at-risk" segment

## References

- DTW for customer segmentation: Liao (2005) - "Clustering of time series data—a survey"
- E-commerce behavior clustering: Aghabozorgi et al. (2015) - "Time-series clustering – A decade review"
