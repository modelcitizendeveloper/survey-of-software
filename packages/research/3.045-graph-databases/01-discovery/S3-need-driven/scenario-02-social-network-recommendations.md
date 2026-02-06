# S3: Social Network / Recommendation Engine

**Use Case:** Social networking platform with friend recommendations
**Scale:** 10M users, 100M friendships (growing to 100M users, 1B friendships)
**Queries:** 200M reads/month, 10M writes/month
**Priority:** Low latency (<50ms), real-time recommendations, massive scale

---

## Business Context

**Problem:**
Social networking platform needs graph database for:
1. **Friend recommendations:** "People you may know" (friends-of-friends, mutual connections)
2. **Content recommendations:** "Posts your friends liked"
3. **Network analytics:** Influencer detection (high centrality), community detection (interest groups)
4. **Real-time queries:** <50ms latency for user-facing features
5. **Massive scale:** 10M users today, 100M users in 3 years

**Current State:**
- Using PostgreSQL (relational database)
- Queries like "friends of friends" require multiple joins (slow, 500ms-2s)
- Friend recommendations calculated in batch overnight (stale data)
- Cannot scale beyond 10M users (table scans too slow)

**Desired State:**
- Real-time friend recommendations (<50ms queries)
- Graph traversal optimized for 2-3 hop queries (friends-of-friends-of-friends)
- Graph algorithms (PageRank for influencers, community detection for groups)
- Scale to 100M users, 1B friendships (10× growth)

---

## Data Model

### Nodes

**User:**
```json
{
  "user_id": "user_12345",
  "name": "Alice",
  "location": "NYC",
  "interests": ["tech", "travel", "food"],
  "joined": "2024-01-15"
}
```

**Post:**
```json
{
  "post_id": "post_67890",
  "user_id": "user_12345",
  "content": "Just visited the Grand Canyon!",
  "created": "2025-11-15T14:30:00Z"
}
```

### Edges

**FRIENDS_WITH:**
```cypher
(user_a:User)-[:FRIENDS_WITH {since: "2024-03-01"}]->(user_b:User)
```

**LIKED:**
```cypher
(user:User)-[:LIKED {timestamp: "2025-11-15T15:00:00Z"}]->(post:Post)
```

**COMMENTED:**
```cypher
(user:User)-[:COMMENTED {text: "Amazing!", timestamp: "..."}]->(post:Post)
```

---

## Key Queries

### Query 1: Friend Recommendations (Friends of Friends)

```cypher
// Find friends of friends who are not already friends
MATCH (me:User {user_id: "user_12345"})-[:FRIENDS_WITH]-(friend)-[:FRIENDS_WITH]-(fof:User)
WHERE NOT (me)-[:FRIENDS_WITH]-(fof)
  AND me <> fof
WITH fof, count(DISTINCT friend) AS mutual_friends
RETURN fof.user_id, fof.name, mutual_friends
ORDER BY mutual_friends DESC
LIMIT 10
```

**Performance Requirement:** <50ms (user-facing)

---

### Query 2: Content Recommendations (Friends' Liked Posts)

```cypher
// Find posts liked by friends that user hasn't seen
MATCH (me:User {user_id: "user_12345"})-[:FRIENDS_WITH]-(friend)-[:LIKED]->(post:Post)
WHERE NOT (me)-[:LIKED]->(post)
  AND NOT (me)-[:COMMENTED]->(post)
WITH post, count(DISTINCT friend) AS friend_likes
RETURN post.post_id, post.content, friend_likes
ORDER BY friend_likes DESC, post.created DESC
LIMIT 20
```

**Performance Requirement:** <100ms (feed generation)

---

### Query 3: Influencer Detection (PageRank)

```cypher
// Find most influential users (high PageRank)
CALL pagerank.get()
YIELD node, rank
WHERE node:User
RETURN node.user_id, node.name, rank
ORDER BY rank DESC
LIMIT 100
```

**Use Case:** Identify influencers for partnerships, advertising targeting

---

### Query 4: Community Detection (Interest Groups)

```cypher
// Identify communities (friend groups)
CALL louvain.get()
YIELD node, community_id
WHERE node:User
RETURN community_id, collect(node.user_id) AS members, count(*) AS size
ORDER BY size DESC
LIMIT 50
```

**Use Case:** Auto-suggest groups based on communities

---

## Scale Projections

| Metric | Current (Year 1) | Year 2 | Year 3 (Target) |
|--------|------------------|--------|-----------------|
| **Users** | 10M | 30M | 100M |
| **Friendships** | 100M | 300M | 1B |
| **Posts** | 50M | 150M | 500M |
| **Queries/Month** | 200M | 600M | 2B |
| **Writes/Month** | 10M | 30M | 100M |
| **Avg Friends/User** | 10 | 10 | 10 |

---

## Database Evaluation

### Requirements

**Must-Have:**
- ✅ Horizontal scaling (grow to 100M users, 1B edges)
- ✅ Low latency (<50ms for 2-3 hop queries)
- ✅ High read throughput (200M-2B queries/month = 80-800 qps average, 5K-50K qps peak)
- ✅ Graph algorithms (PageRank, community detection)
- ✅ Write throughput (10M-100M writes/month = 4-40 wps average, 100-500 wps peak)

**Nice-to-Have:**
- ⚠️ Managed service (reduce ops burden)
- ⚠️ Multi-region (global user base)

---

## Option 1: TigerGraph Enterprise ✅ RECOMMENDED

**Pricing:**
- Year 1 (10M users): $3,000/month
- Year 3 (100M users): $10,000/month (estimated)
- **3-Year TCO: ~$200,000**

**Pros:**
- ✅ **Best at massive scale** (proven to 100B+ edges)
- ✅ **Real-time deep-link analytics** (2-3 hop queries in 10-30ms)
- ✅ **Distributed MPP** (horizontal scaling, linear growth)
- ✅ **30+ graph algorithms** (PageRank, Louvain, centrality)
- ✅ **High throughput** (10K-50K qps reads, 10K wps writes)
- ✅ **Managed service** (eliminate ops burden)
- ✅ **Multi-region support** (global deployment)

**Cons:**
- ❌ Expensive ($3K-10K/month, but justified at this scale)
- ❌ Highest lock-in (GSQL proprietary)
- ⚠️ Requires enterprise sales process (no self-service)

**Why Recommended:**
- Only database proven at 100M+ users scale with <50ms latency
- Real-time friend recommendations (10-30ms queries)
- Distributed architecture scales linearly (10M → 100M users)
- High read throughput (10K-50K qps) handles peak traffic
- 30+ algorithms (PageRank for influencers, Louvain for communities)
- Worth the cost at this scale ($10K/month = $0.0001/user at 100M scale)

---

## Option 2: JanusGraph (Self-Hosted) ⚠️ COST-EFFECTIVE ALTERNATIVE

**Pricing:**
- Year 1 (10M users): $1,500/month (5 JG nodes + 15 Cassandra nodes)
- Year 3 (100M users): $5,000/month (10 JG + 30 Cassandra)
- **3-Year TCO: ~$110,000**

**Pros:**
- ✅ **Proven to trillions of edges** (Netflix, Uber historical use)
- ✅ **Lowest lock-in** (Apache open source, Gremlin standard)
- ✅ **Write-optimized** (Cassandra backend, 10K-100K wps)
- ✅ **Lowest cost** ($1.5K-5K/month vs TigerGraph $3K-10K)
- ✅ **Horizontal scaling** (add Cassandra nodes linearly)

**Cons:**
- ❌ **No graph algorithms** (must build custom or export to NetworkX)
- ⚠️ **Complex ops** (manage JanusGraph + Cassandra + Elasticsearch clusters)
- ⚠️ **Slower queries** (50-200ms 2-3 hop vs TigerGraph 10-30ms)
- ❌ Requires strong ops team (3 systems to manage)

**Why Alternative:**
- 50% cost of TigerGraph ($110K vs $200K over 3 years)
- No algorithms = dealbreaker if influencer detection, community detection critical
- Complex ops acceptable if have strong ops team
- Good for write-heavy workloads (new friendships, posts)

**Choose JanusGraph if:**
- Cost-sensitive (startup budget)
- Have strong ops team (can manage distributed clusters)
- Don't need graph algorithms (or can build custom)
- Write-heavy workload (Cassandra backend optimized)

---

## Option 3: Neo4j Enterprise ❌ NOT RECOMMENDED (SINGLE-NODE LIMITED)

**Pricing:**
- Year 1: $200/month (32GB RAM self-hosted) + $150K/year license = $12.7K/month
- Year 3: Cannot scale beyond ~50M edges (single node limit)
- **3-Year TCO: $460K+ (and cannot reach 100M users)**

**Pros:**
- ✅ Best graph algorithms (60+)
- ✅ Best ecosystem (most mature)
- ✅ Cypher query language (most readable)

**Cons:**
- ❌ **Single-node limited** (cannot scale to 100M users, 1B edges)
- ❌ **Extremely expensive** ($150K+/year Enterprise license)
- ❌ **Enterprise clustering limited** (not true horizontal scaling)
- ❌ Low write throughput (100-500 wps, insufficient for 10M writes/month)

**Why NOT Recommended:**
- Cannot scale to target (100M users, 1B edges)
- Prohibitively expensive ($460K+ over 3 years, 4× TigerGraph)
- Single-node architecture fundamentally limited

---

## Option 4: Memgraph Enterprise ❌ NOT RECOMMENDED (RAM-LIMITED)

**Pricing:**
- Year 1 (10M users): $800/month (64GB RAM managed)
- Year 3 (100M users): $3,000+/month (256GB+ RAM required)
- **3-Year TCO: ~$100,000**

**Pros:**
- ✅ Fastest queries (<1ms single-hop, 2-10ms 2-3 hop)
- ✅ 30+ graph algorithms
- ✅ Low lock-in (openCypher)

**Cons:**
- ❌ **In-memory = RAM-limited** (100M users, 1B edges = 500GB-1TB RAM = $5,000+/month)
- ❌ **Expensive at scale** (RAM costs grow linearly)
- ⚠️ Enterprise clustering available but expensive

**Why NOT Recommended:**
- RAM limitation makes scale expensive (1TB RAM = $5,000-10,000/month)
- TigerGraph cheaper at 100M users scale ($10K for distributed vs $10K+ for 1TB RAM)
- In-memory advantage diminishes at massive scale (distributed beats single large node)

---

## Option 5: Amazon Neptune ⚠️ IF AWS-COMMITTED

**Pricing:**
- Year 1: $2,000/month (db.r6g.4xlarge + replicas)
- Year 3: $6,000/month (db.r6g.12xlarge + replicas)
- **3-Year TCO: ~$150,000**

**Pros:**
- ✅ AWS-native (IAM, VPC, CloudWatch, Lambda integration)
- ✅ Managed service (eliminate ops)
- ✅ Multi-AZ HA built-in
- ✅ Horizontal scaling (read replicas)

**Cons:**
- ❌ **No graph algorithms** (Neptune Analytics $17K/month extra!)
- ⚠️ AWS lock-in (cannot self-host, cannot multi-cloud)
- ⚠️ Expensive ($150K vs JanusGraph $110K)
- ⚠️ Slower than TigerGraph (50-200ms vs 10-30ms)

**Choose Neptune if:**
- AWS-committed (already on AWS, deep IAM integration)
- Don't need algorithms (or budget $17K/month for Neptune Analytics)
- Prefer managed service (no ops team)

**Otherwise:** TigerGraph better (faster, cheaper, includes algorithms)

---

## Final Recommendation

### Winner: TigerGraph Enterprise

**Reasoning:**
- ✅ Only database proven at 100M users scale with <50ms latency
- ✅ Real-time friend recommendations (10-30ms 2-3 hop queries)
- ✅ 30+ graph algorithms (influencer detection, community detection)
- ✅ High throughput (10K-50K qps reads, 10K wps writes)
- ✅ Managed service (eliminate ops burden)
- ✅ Multi-region support (global deployment)
- ✅ Cost justified ($10K/month = $0.0001/user at 100M users)

**Cost Comparison (3-Year TCO):**
1. JanusGraph (self-hosted): $110K (cheapest, but no algorithms, complex ops)
2. TigerGraph Enterprise: $200K (best performance + algorithms)
3. Neptune: $150K (managed, but no algorithms)
4. Neo4j Enterprise: $460K+ (cannot scale, prohibitively expensive)

**Trade-Off:**
- TigerGraph 80% more expensive than JanusGraph ($200K vs $110K)
- But includes algorithms (worth it for influencer detection, communities)
- Simpler ops (managed vs self-hosted 30-node Cassandra cluster)
- Faster queries (10-30ms vs 50-200ms)

**Alternative: JanusGraph if:**
- Budget-constrained (startup, $110K acceptable but $200K not)
- Have strong ops team (can manage distributed clusters)
- Don't need algorithms (or can export to Python/NetworkX for batch analytics)

---

## Implementation Plan

**Phase 1: Migration (Month 1-2)**
1. Setup TigerGraph cluster (start with 10M users, 100M edges)
2. Migrate user data from PostgreSQL → TigerGraph (GSQL load jobs)
3. Migrate friendship edges (100M edges)
4. Test queries (friend recommendations, content recommendations)

**Phase 2: Production Cutover (Month 3)**
1. Parallel writes (PostgreSQL + TigerGraph) for 2 weeks
2. Switch reads to TigerGraph (monitor latency, errors)
3. Cutover fully to TigerGraph
4. Decommission PostgreSQL friendship tables

**Phase 3: Algorithm Integration (Month 4-5)**
1. Run PageRank nightly → Identify influencers
2. Run Louvain weekly → Detect communities
3. Build dashboards (influencer metrics, community stats)
4. A/B test friend recommendations (TigerGraph vs old batch system)

**Phase 4: Optimization (Month 6+)**
1. Tune query performance (index optimization, cache tuning)
2. Monitor scale (add nodes as users grow)
3. Multi-region deployment (global latency <50ms)

**Estimated Effort:** 6 months with 2-3 engineers

---

**Next:** Scenario 03 (Fraud Detection)
