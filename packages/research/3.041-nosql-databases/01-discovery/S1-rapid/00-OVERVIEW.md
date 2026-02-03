# S1: Rapid Search - NoSQL Databases

**Research Date:** November 16, 2025
**Methodology:** MPSE v3.0 - Section 1 (Rapid Search)
**Scope:** Identify major NoSQL database categories and managed service providers

---

## NoSQL Database Categories

NoSQL databases are non-relational databases optimized for specific data models and access patterns. Four main categories:

### 1. Document Databases
**Data Model:** JSON/BSON documents with nested structures
**Use Cases:** Content management, user profiles, catalogs, mobile apps
**Query Pattern:** Flexible queries on document fields
**Key Providers:** MongoDB Atlas, Firestore, Couchbase Cloud, DocumentDB

### 2. Key-Value Stores
**Data Model:** Simple key → value mappings
**Use Cases:** Session storage, caching (as database), user preferences, shopping carts
**Query Pattern:** Get/set by key only
**Key Providers:** DynamoDB, Redis Enterprise Cloud, Azure Table Storage, Upstash

### 3. Wide-Column Stores
**Data Model:** Tables with flexible column families
**Use Cases:** Time-series data, IoT, event logging, analytics
**Query Pattern:** Range queries on partition keys
**Key Providers:** Cassandra (managed), ScyllaDB Cloud, Bigtable, HBase

### 4. Graph Databases
**Data Model:** Nodes and edges (relationships)
**Use Cases:** Social networks, recommendation engines, fraud detection, knowledge graphs
**Query Pattern:** Traversals, path finding, relationship queries
**Key Providers:** Neo4j Aura, Neptune, ArangoDB (multimodel)

---

## Multi-Model Databases

Some databases support multiple data models:
- **Azure Cosmos DB:** Document, key-value, graph, column-family (all-in-one)
- **ArangoDB:** Document, graph, key-value
- **FaunaDB:** Document with relational features

---

## Provider Categories

### Level 5: Full Platform (Database + Hosting + Services)
- Supabase (Postgres + real-time + auth)
- Firebase (Firestore + hosting + auth)
- AWS Amplify (DynamoDB + AppSync + hosting)

### Level 4: Managed Database Services
- **MongoDB Atlas** (document)
- **DynamoDB** (key-value)
- **Firestore** (document)
- **Neo4j Aura** (graph)
- **Azure Cosmos DB** (multi-model)
- **Cassandra-as-a-Service** (DataStax Astra, Instaclustr)
- **ScyllaDB Cloud** (wide-column)
- **Redis Enterprise Cloud** (key-value)

### Level 3: Cloud Provider Managed
- **AWS DocumentDB** (MongoDB-compatible)
- **AWS DynamoDB** (proprietary key-value)
- **AWS Neptune** (graph)
- **Google Firestore** (document)
- **Google Bigtable** (wide-column)
- **Azure Cosmos DB** (multi-model)

### Level 2: Self-Hosted Open Source
- MongoDB Community
- Cassandra (Apache)
- Redis (open source)
- Neo4j Community
- CouchDB
- ArangoDB Community

---

## Key Decision Factors

1. **Data Model Match:** Does your data naturally fit documents, key-value, wide-column, or graph?
2. **Query Patterns:** Simple key lookups vs complex queries vs relationship traversals
3. **Scale Requirements:** Horizontal scaling needs (NoSQL strength)
4. **Consistency Requirements:** Eventual vs strong consistency trade-offs
5. **Cloud Ecosystem:** AWS/GCP/Azure native vs cloud-agnostic
6. **Cost Model:** Provisioned vs serverless vs pay-per-operation
7. **Open Source Option:** Self-hosted available? (Path 3 vs Path 1)

---

## Research Questions for S2-S4

1. **When to choose NoSQL over SQL?** (Decision framework)
2. **Cost comparison:** Serverless (DynamoDB, Firestore) vs provisioned (Atlas, Cassandra)
3. **Lock-in risk:** MongoDB wire protocol vs AWS-proprietary APIs
4. **Performance:** Single-digit millisecond latency claims
5. **Migration complexity:** Moving between NoSQL providers
6. **Open standards:** None exist (unlike 2.050 PostgreSQL for SQL)

---

## Provider Count

- **Total providers identified:** 20+
- **Deep dive candidates (S2):** 8-10
  - MongoDB Atlas (document leader)
  - DynamoDB (AWS key-value)
  - Firestore (Google document)
  - Cassandra/DataStax Astra (wide-column)
  - Redis Enterprise Cloud (key-value)
  - Neo4j Aura (graph leader)
  - Azure Cosmos DB (multi-model)
  - ScyllaDB Cloud (Cassandra alternative)

---

**Next:** Individual provider profiles
