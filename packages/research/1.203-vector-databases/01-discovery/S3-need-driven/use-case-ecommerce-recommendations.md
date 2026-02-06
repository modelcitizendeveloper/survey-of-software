# Use Case: E-Commerce Product Recommendations

## Scenario

**Context**: Mid-size e-commerce site (fashion/apparel)
**Data**: 2M products (images + metadata), 10M user interaction vectors
**Usage**: High traffic (5000 queries/second peak), recommendation engine
**Stack**: Kubernetes, microservices, real-time personalization

## Requirements

### Must-Have
1. ✅ **High QPS**: 5000+ queries/second sustained
2. ✅ **Complex filtering**: Multi-attribute (price, size, color, brand, in-stock, location)
3. ✅ **Low latency**: <50ms p95 (user-facing recommendations)
4. ✅ **Horizontal scaling**: Traffic spikes during sales events
5. ✅ **High availability**: 99.95% uptime (revenue-critical)

### Nice-to-Have
1. **Multi-vector support**: Product image embedding + text description embedding
2. **A/B testing**: Namespace isolation for experiments
3. **Cost optimization**: High scale = cost matters

## Candidate Evaluation

| Database | QPS | Filtering | Latency | Scaling | HA | Fit |
|----------|-----|-----------|---------|---------|----|----|
| **ChromaDB** | ❌ 1k | ⚠️ Basic | ✅ | ❌ | ❌ | **FAILS** (scale) |
| **Pinecone** | ✅ 10k+ | ⚠️ Good | ✅ | ✅ Auto | ✅ | **95% fit** (cost concern) |
| **Qdrant** | ✅ 20k+ | ✅ BEST | ✅ <10ms | ✅ Sharding | ✅ | **100% fit** |
| **Weaviate** | ✅ 15k+ | ✅ Good | ✅ 20ms | ✅ Sharding | ✅ | **95% fit** |

## Recommendation

### Primary: **Qdrant**

**Why:**
1. **Highest QPS**: 20k+ per node (4x requirement, room for growth)
2. **Best filtering**: Complex multi-attribute queries without perf hit
3. **Best latency**: <10ms p95 (5x under budget)
4. **Cost optimization**: Quantization reduces infrastructure cost by 90%
5. **Kubernetes-native**: Fits existing microservices architecture

**Cost comparison (12M vectors, 5k QPS):**
- Qdrant (self-hosted, quantized): **$400-600/month**
- Pinecone (managed): **$2000-4000/month**
- Savings: **$1400-3400/month** = $16k-40k/year

**Example query:**
```python
client.search(
    collection_name="products",
    query_vector=user_preference_embedding,
    query_filter={
        "must": [
            {"key": "in_stock", "match": {"value": true}},
            {"key": "price", "range": {"gte": 20, "lte": 100}},
            {"key": "size", "match": {"any": ["M", "L"]}},
            {"key": "location", "geo_radius": {...}}
        ]
    },
    limit=20
)
```

## Alternative: **Pinecone** (if DevOps is constraint)

**When to choose:**
- Team has no Kubernetes expertise
- Cost difference ($1.5k/month) acceptable vs hiring DevOps
- Speed-to-market > cost optimization

## Confidence

**Very High (95%)** - Qdrant's filtering + performance + cost optimization is unbeatable for this use case.
