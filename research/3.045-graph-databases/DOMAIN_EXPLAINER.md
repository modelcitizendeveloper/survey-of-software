# Graph Databases: Explained

**For:** Business professionals with general tech background
**Category:** 3.045 (Managed Services - Specialized Databases)
**Last Updated:** November 16, 2025

---

## What Problem Do Graph Databases Solve?

Imagine you're running a business where **relationships are as important as the data itself**:

**Scenario #1: You're building a social network**
- Every user has friends (relationships)
- You want to show "people you may know" (friends-of-friends)
- Using a traditional SQL database: You need complex joins across multiple tables
- Result: Slow queries (500ms-2s for 3 hops), doesn't scale

**Scenario #2: You're detecting fraud in payments**
- Fraudsters create multiple accounts from same device
- Money flows in circles (A → B → C → A = laundering)
- You need to find these patterns in real-time
- SQL: Hard to express circular patterns, slow to traverse

**Scenario #3: You're building a recommendation engine**
- "Customers who bought X also bought Y"
- "Products similar to what your friends liked"
- Requires traversing many relationships quickly
- SQL: Joins become exponentially slow beyond 2-3 levels

**Graph databases solve this:** They store relationships as first-class citizens, making relationship queries 10-1000× faster than SQL.

---

## The Core Idea: Data as a Network

Think of data as a **network diagram on a whiteboard:**

**SQL Database = Spreadsheet:**
- Data in tables with rows and columns
- Relationships via foreign keys (user_id references users table)
- Querying relationships = JOINS (expensive)
- Example: "Find friends of friends" requires multiple JOINs

**Graph Database = Network Diagram:**
- Data as **nodes** (circles on whiteboard: people, products, accounts)
- Relationships as **edges** (arrows connecting nodes: FRIENDS_WITH, BOUGHT, SENT_MONEY)
- Querying relationships = traversing arrows (fast)
- Example: "Find friends of friends" = follow arrows 2 hops (10-50ms)

**Key Difference:**
- SQL: "Find all users where user_id IN (SELECT friend_id FROM friendships WHERE user_id = 123)"
- Graph: "MATCH (user)-[:FRIENDS_WITH]->(friend) WHERE user.id = 123"

Graph queries are more readable and 10-1000× faster for relationship-heavy data.

---

## Real-World Analogy: LinkedIn

**SQL Approach (Traditional):**
```
Users Table:
| user_id | name    |
|---------|---------|
| 1       | Alice   |
| 2       | Bob     |
| 3       | Charlie |

Connections Table:
| user_id | connected_to |
|---------|--------------|
| 1       | 2            |
| 2       | 3            |
| 1       | 3            |
```

**Query:** "Find Alice's connections and their connections"
```sql
-- Step 1: Find Alice's direct connections
SELECT connected_to FROM connections WHERE user_id = 1;
-- Returns: 2, 3

-- Step 2: Find connections of Bob (2) and Charlie (3)
SELECT connected_to FROM connections WHERE user_id IN (2, 3);
-- Requires multiple queries or complex JOIN
```

**Performance:** 200-500ms for 2 hops, exponentially slower for 3+ hops

---

**Graph Database Approach:**
```
Nodes:
- Alice (User)
- Bob (User)
- Charlie (User)

Edges:
- Alice → CONNECTED → Bob
- Bob → CONNECTED → Charlie
- Alice → CONNECTED → Charlie
```

**Query:** "Find Alice's connections and their connections"
```cypher
MATCH (alice:User {name: 'Alice'})-[:CONNECTED*1..2]->(connection)
RETURN connection.name
```

**Performance:** 10-50ms for 2 hops, scales to 10+ hops

---

## When Should You Use a Graph Database?

### ✅ Use Graph Database When:

**1. Relationships Are Core to Your Business**
- Social networks (friends, followers, connections)
- Fraud detection (money flow patterns, shared devices)
- Recommendations (products liked by friends, similar items)
- Knowledge graphs (entities connected by relationships)
- Network analysis (influencers, communities, hubs)

**2. You Need Multi-Hop Queries (2+ Levels Deep)**
- Friends-of-friends (2 hops)
- Product recommendations (customers who bought X also bought Y)
- Organizational charts (who reports to whom, 5 levels deep)
- Supply chain tracing (product origin, 10+ hops)

**3. Your Schema Changes Frequently**
- Add new relationship types without schema migration
- Example: Add "WORKED_WITH" relationship without altering tables

**4. Real-Time Relationship Queries**
- Fraud detection (<100ms per transaction)
- Real-time recommendations (<50ms per page load)
- Live network analysis (who's trending right now)

---

### ❌ Avoid Graph Database When:

**1. Simple Data Without Complex Relationships**
- Accounting (invoices, payments) → Use SQL
- Inventory (products, quantities) → Use SQL
- Logs (time-series data) → Use time-series DB

**2. Aggregations and Reporting**
- "Total revenue by month" → SQL better
- "Average order value" → SQL better
- Graph databases can do this, but SQL is faster and cheaper

**3. Your Data Fits One Table**
- User profiles (no relationships) → Document DB (MongoDB, Firestore)
- Product catalog (no relationships) → Document DB
- Only use graph if relationships exist

**4. Budget <$50/Month and No Relationships**
- PostgreSQL (SQL) is cheaper for simple data
- Graph databases add cost/complexity without benefit

---

## Key Concepts: Nodes, Edges, Properties

### Nodes (Entities)

**What are they:** The "things" in your data (people, products, places)

**Example:**
```
Alice (Person)
- Properties: age=30, location="NYC", job="Engineer"

Product X (Product)
- Properties: price=49.99, category="Electronics"
```

### Edges (Relationships)

**What are they:** Connections between nodes with a type and direction

**Example:**
```
Alice → FRIENDS_WITH → Bob (since 2020)
Alice → BOUGHT → Product X (date: 2025-11-15, price: 49.99)
Alice → WORKS_AT → Company Y (title: "Engineer", start: 2024-01-01)
```

**Key:** Edges can have properties (when friendship started, purchase price, job title)

### Properties (Attributes)

**What are they:** Key-value pairs on nodes and edges

**Example:**
```
Node: Alice
- name: "Alice"
- age: 30
- location: "NYC"

Edge: Alice → FRIENDS_WITH → Bob
- since: "2020-03-15"
- strength: "close" (or numeric score)
```

---

## Query Language Examples

### Cypher (Neo4j, Memgraph) - Most Readable

**ASCII art style:**
```cypher
// Find Alice's friends
MATCH (alice:Person {name: "Alice"})-[:FRIENDS_WITH]->(friend)
RETURN friend.name

// Find friends-of-friends who like same products
MATCH (alice:Person {name: "Alice"})-[:FRIENDS_WITH*2]-(fof)
WHERE (fof)-[:LIKES]->(:Product)<-[:LIKES]-(alice)
RETURN fof.name, count(*) AS common_interests
ORDER BY common_interests DESC
```

### Gremlin (JanusGraph, Neptune) - Functional Style

**Traversal-based:**
```gremlin
// Find Alice's friends
g.V().has('Person', 'name', 'Alice')
  .out('FRIENDS_WITH')
  .values('name')

// Find friends-of-friends
g.V().has('Person', 'name', 'Alice')
  .repeat(out('FRIENDS_WITH')).times(2)
  .values('name')
```

### GraphQL (Dgraph) - API-First

**Declarative:**
```graphql
query {
  getPerson(name: "Alice") {
    name
    friends {
      name
      friends {
        name
      }
    }
  }
}
```

---

## Real-World Business Use Cases

### Use Case 1: Social Network (10M Users)

**Problem:** Show "people you may know" recommendations
**Data:** Users, friendships (100M relationships)

**SQL Approach:**
- JOIN friendships table multiple times (friends of friends)
- Query time: 500ms-2s (too slow for user-facing feature)
- Scales poorly beyond 2 hops

**Graph Database:**
- Traverse FRIENDS_WITH edges 2 hops
- Query time: 10-50ms (acceptable for real-time)
- Scales to 5+ hops easily

**Recommended Database:** TigerGraph Enterprise ($3K-10K/mo) or Neo4j Aura ($240-800/mo)
**Why:** Proven at social network scale, <50ms queries

---

### Use Case 2: Fraud Detection (5M Users, 50M Transactions/Month)

**Problem:** Detect fraud rings (multiple accounts from same device) and money laundering (circular money flows)
**Data:** Users, devices, bank accounts, transactions

**SQL Approach:**
- Detect circular flows: Recursive CTEs (slow, complex)
- Find shared devices: Multiple self-joins (slow)
- Query time: 200ms-2s (too slow for real-time scoring)

**Graph Database:**
- Circular flow: `MATCH path = (user)-[:SENT_MONEY*2..5]->(user)`
- Shared devices: `MATCH (user1)-[:USED_DEVICE]->(device)<-[:USED_DEVICE]-(user2)`
- Query time: <100ms (real-time transaction scoring)

**Recommended Database:** Neo4j Aura Professional ($240-480/mo)
**Why:** Best fraud detection ecosystem, 60+ algorithms (PageRank, community detection)

---

### Use Case 3: Product Recommendations (E-Commerce)

**Problem:** "Customers who bought X also bought Y" recommendations
**Data:** Products, customers, purchases (10M products, 50M purchases)

**SQL Approach:**
- Self-join purchases table (slow)
- Requires complex GROUP BY, HAVING
- Query time: 500ms-2s

**Graph Database:**
- `MATCH (p:Product)<-[:BOUGHT]-(c:Customer)-[:BOUGHT]->(other:Product)`
- Query time: 50-200ms
- Scales to "friends of customers who bought X also bought Y" (3+ hops)

**Recommended Database:** Neo4j Aura ($240/mo) or Memgraph Cloud ($199/mo)
**Why:** Fast queries, algorithms for collaborative filtering

---

## Choosing the Right Graph Database

### Decision Tree

```
Do you need graph algorithms (PageRank, community detection)?
├─ YES → Continue...
│   ├─ Budget <$100/mo?
│   │   └─ YES → Memgraph Community self-hosted ($24-84/mo) ✅
│   ├─ Budget $100-500/mo?
│   │   └─ YES → Neo4j Aura Professional ($65-240/mo) ✅
│   └─ Budget >$3K/mo, massive scale (>10M nodes)?
│       └─ YES → TigerGraph Enterprise ($3K-10K/mo) ✅
│
└─ NO (traversal only) → Continue...
    ├─ AWS-committed?
    │   └─ YES → Amazon Neptune ($120-1,500/mo) ⚠️
    └─ GraphQL-native needed?
        └─ YES → Dgraph ($0-200/mo) ⚠️
```

---

### Top Recommendations by Use Case

**Small Projects (<1M nodes, budget <$100/mo):**
- **Memgraph Community** (self-hosted, $24-84/mo): 30+ algorithms, 10× faster than Neo4j
- **Neo4j Community** (self-hosted, $48-84/mo): 60+ algorithms, best ecosystem
- **Free tiers:** Neo4j Aura Free, Dgraph Cloud Free (development only)

**Medium Projects (1M-10M nodes, budget $100-1K/mo):**
- **Neo4j Aura Professional** ($65-800/mo): Best ecosystem, managed
- **Memgraph Cloud** ($49-799/mo): Faster, lower lock-in

**Large Projects (10M-100M nodes, budget >$3K/mo):**
- **TigerGraph Enterprise** ($3K-10K/mo): Only database proven at 100M+ nodes scale
- **JanusGraph** (self-hosted, $1.5K-5K/mo): Open source, cheapest for massive scale

**Fraud Detection (any scale):**
- **Neo4j Aura** ($240-480/mo): Best fraud detection ecosystem, 60+ algorithms

**AWS-Committed:**
- **Amazon Neptune** ($120-1,500/mo): AWS-native, but expensive and no algorithms

---

## Cost Comparison (Apples-to-Apples)

**Same workload:** 100K nodes, 1M edges, 100K queries/month

| Database | Monthly Cost | Best For |
|----------|--------------|----------|
| **Memgraph Community (self-hosted)** | $24 | Cheapest, 30+ algorithms, fast |
| **Neo4j Community (self-hosted)** | $48 | 60+ algorithms, best ecosystem |
| **Neo4j Aura Professional** | $65-120 | Managed, eliminate ops |
| **Memgraph Cloud** | $49-199 | Managed, fastest, low lock-in |
| **Amazon Neptune Serverless** | $120-350 | AWS-native, **no algorithms** |
| **TigerGraph Cloud** | $99-499 | Enterprise scale, **highest lock-in** |

**Key Insight:** 20× cost variance ($24 self-hosted vs $499 TigerGraph)! Choosing the right database = huge cost impact.

---

## Trade-Offs: Graph vs SQL

### Graph Database Wins When:
- ✅ Relationships are core (social, fraud, recommendations)
- ✅ Multi-hop queries needed (2+ levels deep)
- ✅ Real-time relationship queries (<100ms)
- ✅ Schema evolves (add new relationship types frequently)

### SQL Database Wins When:
- ✅ Simple data (tables with few relationships)
- ✅ Aggregations dominant (SUM, AVG, GROUP BY)
- ✅ Structured data (accounting, inventory)
- ✅ Team knows SQL well (no learning curve)
- ✅ Budget <$50/month (PostgreSQL is cheaper)

**Pragmatic Advice:** Use SQL by default unless relationships are critical. Graph databases add complexity/cost—only use when relationships justify it.

---

## Common Misconceptions

**Myth #1: "Graph databases are faster than SQL"**
- **Reality:** Only for relationship queries (2+ hops). SQL is faster for aggregations, simple lookups.

**Myth #2: "Graph databases replace SQL"**
- **Reality:** They're different tools. Many companies use both (SQL for transactions, graph for relationships).

**Myth #3: "Graph databases are expensive"**
- **Reality:** Self-hosted options $24-84/mo (Memgraph, Neo4j). Managed services $65-500/mo. Can be 10× cheaper than wrong choice.

**Myth #4: "Graph databases are only for social networks"**
- **Reality:** Use cases span fraud detection, recommendations, knowledge graphs, supply chain, org charts.

**Myth #5: "Graph databases don't scale"**
- **Reality:** Proven to 100M+ nodes (TigerGraph), trillions of edges (JanusGraph at Netflix/Uber).

---

## Lock-In Considerations (Business Risk)

**What is lock-in?**
The difficulty (time, cost, risk) of switching to a different graph database.

**Low lock-in (easy to switch):**
- **Memgraph** (openCypher standard): Migrate to Neo4j in 1-2 weeks
- **JanusGraph** (Gremlin standard): Migrate to Neptune in 1-2 weeks
- **Dgraph** (open source): Self-host option, Apache 2.0 license

**High lock-in (hard to switch):**
- **TigerGraph** (GSQL proprietary): 3-6 months to migrate (complete query rewrite)
- **ArangoDB** (AQL proprietary): 2-3 months to migrate
- **Amazon Neptune** (AWS-only): Cannot self-host, 2-3 months to migrate

**Business Advice:**
- **Startups (0-3 years):** Lock-in OK if it means faster shipping (Neo4j Aura, TigerGraph acceptable)
- **Scale-ups (3-5 years):** Start planning exit paths, test migrations annually
- **Enterprises (5-10 years):** Choose low lock-in from day one (Memgraph, JanusGraph)

---

## Vendor Viability (Will They Exist in 5-10 Years?)

**Extremely safe (99%+ likely):**
- Neo4j (market leader, profitable, $200M+ revenue)
- Amazon Neptune (AWS core service)
- JanusGraph (open source, Linux Foundation)

**Very safe (90-95% likely):**
- Memgraph ($9.5M funding, fast-growing, high acquisition potential)
- TigerGraph ($105M funding, enterprise traction)

**Safe (85-90% likely):**
- Dgraph (open source, Apache 2.0)
- ArangoDB (multi-model niche)

**Business Advice:** All analyzed providers are safe for 5+ years. Vendor viability is not a primary concern (cost and features matter more).

---

## Summary: Graph Databases in Plain English

**What it is:**
Specialized database optimized for storing and querying relationships between data points.

**When to use it:**
When relationships are as important as the data itself (social networks, fraud detection, recommendations, knowledge graphs).

**Types:**
- **Neo4j** (market leader, 60+ algorithms, Cypher query language)
- **Memgraph** (10× faster, in-memory, openCypher, 30+ algorithms)
- **TigerGraph** (massive scale 100M+ nodes, GSQL proprietary)
- **Amazon Neptune** (AWS-native, Gremlin/openCypher, no algorithms)
- **JanusGraph** (open source, trillions of edges, Gremlin)
- **Dgraph** (GraphQL-native, open source)

**Cost:**
Varies widely (20× difference: $24 self-hosted vs $499 managed). Choose right database = major cost impact.

**Risk:**
Lock-in is real (TigerGraph GSQL = 3-6 months to migrate). Vendor viability not a concern (all safe for 5+ years).

**Pragmatic Advice:**
- Use SQL by default (simpler, cheaper)
- Use graph database when relationships are critical
- Start with Neo4j Aura Free or Memgraph Community (test before committing)
- Budget for migration every 5 years (technology refresh)

---

**Full Research:** 24 documents, 7,000+ lines (S1-S4 analysis)
**Location:** `/research/3.045-graph-databases/`

**Quick links:**
- S1: Provider profiles (Neo4j, Neptune, Memgraph, JanusGraph, TigerGraph, ArangoDB, Dgraph)
- S2: Feature matrix (50+ features), pricing TCO (6 scenarios), performance benchmarks
- S3: Business scenarios (social network, fraud detection, knowledge graph)
- S4: Vendor viability, technology evolution, lock-in mitigation, migration complexity
