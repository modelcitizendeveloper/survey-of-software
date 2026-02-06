# Use Case: Semantic Documentation Search (Internal Knowledge Base)

## Scenario

**Context**: Enterprise internal knowledge base for 5,000 employees
**Data**: 50K documentation pages, wikis, Confluence exports (200K vectors, 768-dim)
**Usage**: Low volume (~100 queries/day), not latency-critical
**Stack**: Internal Python app, existing Postgres infrastructure

## Requirements

### Must-Have
1. ✅ **Hybrid search**: Employees search both by exact terms (API names, error codes) AND semantically
2. ✅ **Easy deployment**: IT team manages, prefer minimal ops overhead
3. ✅ **Cost-effective**: Internal tool, limited budget (<$200/month)
4. ✅ **Integration with existing auth**: SSO, Active Directory

### Nice-to-Have
1. **GraphQL API**: Team familiar with GraphQL from other tools
2. **Knowledge graph**: Link related docs (e.g., API → tutorials → troubleshooting)
3. **Multi-tenancy**: Isolate departments if needed later

### Constraints
- **Scale**: Small (200K vectors), no growth expected
- **Performance**: Not critical (<1s acceptable)
- **Deployment**: On-prem preferred (air-gapped option valuable)

## Candidate Evaluation

| Database | Hybrid Search | Easy Deploy | Cost | Integration | Fit |
|----------|---------------|-------------|------|-------------|-----|
| **ChromaDB** | ❌ NO | ✅ BEST | ✅ $20/mo | ⚠️ Basic | **FAILS** (no hybrid) |
| **Pinecone** | ✅ YES | ✅ Zero-ops | ❌ $500+/mo | ✅ Good | **FAILS** (cost + cloud-only) |
| **Qdrant** | ✅ BM42 | ⚠️ Moderate | ✅ $50/mo | ✅ REST | **80% fit** |
| **Weaviate** | ✅ BEST (BM25) | ⚠️ Moderate | ✅ $100/mo | ✅ GraphQL | **100% fit** |

## Recommendation

### Primary: **Weaviate**

**Why:**
1. **Best hybrid search**: Native BM25 + vector in single query (critical requirement)
2. **GraphQL**: Team already familiar (nice-to-have becomes advantage)
3. **Knowledge graph**: Cross-references between docs (unique strength)
4. **On-prem**: Self-hosted option for air-gapped requirement
5. **Cost**: $100/month (well under budget)

**Example query:**
```graphql
{
  Get {
    Documentation(
      hybrid: {
        query: "authentication error 401"
        alpha: 0.7  # Weighted toward semantic
      }
      where: {
        path: ["department"]
        operator: Equal
        valueString: "Engineering"
      }
    ) {
      title
      content
      linkedDocs {  # Knowledge graph
        ... on Documentation { title }
      }
    }
  }
}
```

### Alternative: **Qdrant** (if GraphQL is unfamiliar)

**Why:**
- Lower cost ($50/month)
- BM42 hybrid search (slightly less elegant than Weaviate's BM25)
- REST API (more familiar to most teams)
- Better performance (though not needed here)

## Confidence

**Very High (90%)** - Hybrid search requirement clearly favors Weaviate. GraphQL familiarity seals the decision.
