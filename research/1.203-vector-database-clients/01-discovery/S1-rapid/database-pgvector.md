# pgvector Database Profile

## Overview

**Name**: pgvector
**Developer**: Andrew Kane (community-maintained)
**First Release**: 2021
**Primary Language**: C (PostgreSQL extension)
**License**: PostgreSQL License (permissive, similar to BSD/MIT)
**GitHub Stars**: ~13,000 (December 2025)
**Website**: https://github.com/pgvector/pgvector

pgvector is a PostgreSQL extension that adds vector similarity search to your existing PostgreSQL database. Instead of running a separate vector database, you add vector capabilities to the database you already use. This "no new infrastructure" approach is its primary value proposition.

## Core Capabilities

### Vector Storage & Search
- Native PostgreSQL vector type
- Up to 16,000 dimensions per vector (2,000 indexed)
- Exact and approximate nearest neighbor search
- Multiple distance functions

### Distance Metrics
- **L2 (Euclidean)**: `<->` operator
- **Inner Product**: `<#>` operator (negative, use with normalized vectors)
- **Cosine**: `<=>` operator
- **L1 (Manhattan)**: `<+>` operator (0.7.0+)
- **Hamming/Jaccard**: For bit vectors (0.7.0+)

### Index Types
1. **IVFFlat**: Inverted file index
   - Faster build, lower recall
   - Good for memory-constrained environments

2. **HNSW** (0.5.0+): Hierarchical Navigable Small World
   - Better query performance
   - Higher memory usage
   - Industry standard algorithm

### Advanced Features (0.8.0+)
- **Iterative Index Scans**: Prevents "overfiltering"
- **Quantization**: 8-bit, 2-byte float support
- **Sparse Vectors**: Up to 1,000 non-zero dimensions
- **Half Vectors**: 2-byte floats for memory efficiency

## Programming Languages

### Works with Any PostgreSQL Client
pgvector uses standard SQL, so any PostgreSQL client works:

**Python**:
- psycopg2/psycopg3
- asyncpg
- SQLAlchemy
- Django ORM
- `pgvector-python` helper library

**JavaScript/TypeScript**:
- pg (node-postgres)
- Prisma
- TypeORM

**Other Languages**:
- Any language with PostgreSQL drivers
- Go, Java, Ruby, PHP, .NET, etc.

## Deployment Modes

### 1. Local PostgreSQL
```sql
CREATE EXTENSION vector;
```

### 2. Docker
```bash
docker run -e POSTGRES_PASSWORD=postgres ankane/pgvector
```

### 3. Managed PostgreSQL Services
Pre-installed or easily enabled:
- **Supabase**: Built-in, optimized
- **Neon**: Serverless Postgres with pgvector
- **AWS RDS**: Available as extension
- **Google Cloud SQL**: Supported
- **Azure Database**: Supported
- **Railway**: One-click enable

### 4. Self-Hosted
Any PostgreSQL 12+ installation.

## Learning Curve & Documentation

### Learning Curve
**Easy** (if you know PostgreSQL):
- Standard SQL syntax
- Familiar ORM patterns
- No new concepts beyond vectors

**Moderate** (if new to PostgreSQL):
- PostgreSQL basics first
- Then vector concepts

### Documentation Quality
- **GitHub README**: Comprehensive
- **Managed Service Docs**: Supabase, Neon have excellent pgvector guides
- **Blog Posts**: Many tutorials available
- **LangChain/LlamaIndex**: Integration docs

### Time to First Query
- Existing PostgreSQL: ~5 minutes
- New PostgreSQL: ~15 minutes
- Managed service: ~10 minutes

## Community & Ecosystem

### GitHub Activity
- ~13,000 stars
- Active development (0.8.0 released October 2024)
- Regular feature additions
- Community-driven

### Framework Integrations
- **LangChain**: `PGVector` class
- **LlamaIndex**: Native support
- **Django**: django-pgvector
- **SQLAlchemy**: Direct support
- **Rails**: neighbor gem

### ORM Support
Works with all PostgreSQL ORMs:
- SQLAlchemy (Python)
- Django ORM
- Prisma (TypeScript)
- ActiveRecord (Ruby)
- Ecto (Elixir)

## Performance Characteristics

### Query Performance
- HNSW: Competitive with dedicated vector DBs at moderate scale
- IVFFlat: Faster builds, slightly lower recall
- Performance depends on PostgreSQL tuning

### Scalability
- **Sweet spot**: Up to 100 million vectors
- **Comfortable**: 10-50 million vectors
- **Beyond 100M**: Consider dedicated vector DBs

### Optimization Tips
From pgvector docs and AWS blog:
- Increase `maintenance_work_mem` for faster HNSW builds
- Use `ef_construction` parameter wisely
- Parallel index building (0.5.1+): 3.25x speedup
- Monitor with `EXPLAIN ANALYZE`

### Benchmark Context
pgvector is "good enough" for most use cases but won't match Qdrant or Milvus in raw performance at scale. The trade-off is operational simplicity.

## Best Use Cases

### 1. Already Using PostgreSQL
The killer use case - no new infrastructure:
- Add vectors to existing tables
- Join with relational data
- Single database to manage

### 2. Moderate Scale (<100M Vectors)
When scale doesn't justify dedicated vector DB:
- Internal tools
- Small-medium applications
- MVP/early-stage products

### 3. Relational + Vector Queries
When you need both in one query:
```sql
SELECT * FROM products
WHERE category = 'electronics'
  AND price < 100
ORDER BY embedding <=> query_vector
LIMIT 10;
```

### 4. Managed PostgreSQL Users
Teams using Supabase, Neon, RDS, etc.:
- No additional service to manage
- Included in existing pricing
- Single connection string

### 5. Regulatory/Compliance
When data must stay in existing PostgreSQL:
- Data residency requirements
- Audit trail in one place
- Existing security posture

## Limitations

### 1. Scale Ceiling
Not designed for billions of vectors:
- Performance degrades beyond 100M
- Consider Milvus for massive scale

### 2. Feature Gap vs Dedicated DBs
Missing some advanced features:
- No native hybrid search (BM25 + vectors)
- Less sophisticated filtering optimization
- No GPU acceleration
- Fewer index algorithm options

### 3. PostgreSQL Dependency
Must run PostgreSQL:
- If you use MongoDB, no pgvector option
- Adds PostgreSQL if not already using

### 4. Tuning Complexity
Performance requires PostgreSQL expertise:
- Memory configuration
- Connection pooling
- Index parameter tuning

### 5. Resource Sharing
Vectors compete with other PostgreSQL workloads:
- May need dedicated instance
- Resource contention possible

## Production Readiness

### Managed Service Support
Excellent production path via managed services:
- **Supabase**: Production-ready, optimized
- **Neon**: Serverless scaling
- **AWS RDS/Aurora**: Enterprise-grade

### Self-Hosted Production
Standard PostgreSQL production practices:
- Replication
- Backups
- Monitoring
- Connection pooling

### Enterprise Adoption
Widely used in production:
- Backed by PostgreSQL's 30+ year track record
- No vendor lock-in
- Standard database operations

## Code Examples

### Basic Setup
```sql
-- Enable extension
CREATE EXTENSION vector;

-- Create table with vector column
CREATE TABLE items (
    id SERIAL PRIMARY KEY,
    content TEXT,
    embedding VECTOR(384)
);

-- Create HNSW index
CREATE INDEX ON items USING hnsw (embedding vector_cosine_ops);
```

### Insert and Query
```sql
-- Insert
INSERT INTO items (content, embedding)
VALUES ('Machine learning basics', '[0.1, 0.2, ...]');

-- Similarity search
SELECT id, content, embedding <=> '[0.1, 0.2, ...]' AS distance
FROM items
ORDER BY embedding <=> '[0.1, 0.2, ...]'
LIMIT 5;
```

### With Python (psycopg2)
```python
import psycopg2
from pgvector.psycopg2 import register_vector

conn = psycopg2.connect("postgresql://...")
register_vector(conn)

cur = conn.cursor()

# Insert
cur.execute(
    "INSERT INTO items (content, embedding) VALUES (%s, %s)",
    ("Document text", [0.1, 0.2, ...])
)

# Query
cur.execute("""
    SELECT id, content
    FROM items
    ORDER BY embedding <=> %s
    LIMIT 5
""", ([0.1, 0.2, ...],))

results = cur.fetchall()
```

### With SQLAlchemy
```python
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base
from pgvector.sqlalchemy import Vector

Base = declarative_base()

class Item(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True)
    content = Column(String)
    embedding = Column(Vector(384))

# Query
from sqlalchemy.orm import Session
from sqlalchemy import func

with Session(engine) as session:
    results = session.query(Item)\
        .order_by(Item.embedding.cosine_distance(query_vector))\
        .limit(5)\
        .all()
```

### With LangChain
```python
from langchain_postgres import PGVector
from langchain_openai import OpenAIEmbeddings

vectorstore = PGVector(
    embeddings=OpenAIEmbeddings(),
    collection_name="my_docs",
    connection="postgresql://user:pass@localhost/db"
)

# Add documents
vectorstore.add_documents(documents)

# Search
results = vectorstore.similarity_search("query text", k=4)
```

### Filtering with SQL
```sql
-- Combined relational + vector query
SELECT p.id, p.name, p.price
FROM products p
WHERE p.category = 'electronics'
  AND p.price BETWEEN 50 AND 200
  AND p.in_stock = true
ORDER BY p.embedding <=> $1
LIMIT 10;
```

## When to Choose pgvector

### Choose pgvector When:
- Already using PostgreSQL
- Scale is under 100M vectors
- Want single database to manage
- Need relational + vector queries
- Using managed PostgreSQL (Supabase, Neon)
- Team knows SQL/PostgreSQL

### Avoid pgvector When:
- Need billion-vector scale (use Milvus)
- Not using PostgreSQL
- Need hybrid BM25 + vector (use Weaviate)
- Maximum performance required (use Qdrant)
- Need GPU acceleration (use Milvus)

## Summary

pgvector is the **"no new infrastructure"** choice for vector search. By adding vectors to PostgreSQL, teams avoid the complexity of running a separate vector database. It's ideal for organizations already invested in PostgreSQL who need vector search at moderate scale. The trade-off is fewer specialized features and a scale ceiling compared to dedicated vector databases. Think of it as "good enough" vector search with operational simplicity.

---

**Sources**:
- [pgvector GitHub](https://github.com/pgvector/pgvector)
- [PostgreSQL 0.8.0 Release Notes](https://www.postgresql.org/about/news/pgvector-080-released-2952/)
- [Google Cloud - pgvector Performance](https://cloud.google.com/blog/products/databases/faster-similarity-search-performance-with-pgvector-indexes)
- [AWS - Accelerate HNSW with pgvector](https://aws.amazon.com/blogs/database/accelerate-hnsw-indexing-and-searching-with-pgvector-on-amazon-aurora-postgresql-compatible-edition-and-amazon-rds-for-postgresql/)
- [Neon pgvector Documentation](https://neon.com/docs/extensions/pgvector)
