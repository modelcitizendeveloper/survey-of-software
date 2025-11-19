# 2.072: GraphQL Standard Discovery

**Research Code**: 2.072
**Title**: GraphQL (API Query Language Standard)
**Category**: Open Standards - API Design
**Tier**: 2 (Portability Standards)
**Status**: In Progress
**Started**: 2025-11-19

## Research Question

**"How does GraphQL as an open standard enable API portability and reduce vendor lock-in compared to REST/OpenAPI and gRPC?"**

## Scope

Evaluate GraphQL as a **standard** (Tier 2), not specific implementations:

### In Scope
- **GraphQL specification**: Query language, schema definition, introspection
- **Backend compatibility**: Apollo Server, Hasura, Postgraphic, GraphQL Yoga, Hot Chocolate
- **Migration cost**: Switching between GraphQL server implementations
- **Portability analysis**: Schema/query compatibility across implementations
- **Federation standard**: Multi-service GraphQL composition
- **Lock-in assessment**: Proprietary extensions vs standard compliance

### Out of Scope
- Specific managed services (covered in Tier 3 if needed)
- Frontend GraphQL clients (Apollo Client, Relay, urql) - mention but don't deep-dive
- Performance benchmarking (focus on portability, not speed)
- GraphQL vs REST debates (focus on standards portability angle)

## Key Standards Context

**GraphQL Foundation** (Linux Foundation):
- Specification: https://spec.graphql.org/ (Oct 2021 spec, living standard)
- Governance: Neutral foundation (Facebook donated in 2018)
- Maturity: Production-grade, widely adopted (GitHub, Shopify, Netflix, etc.)

**Related Standards** (for comparison):
- **2.070**: OpenAPI/REST (request/response, no schema introspection)
- **2.071**: gRPC (RPC-style, Protocol Buffers, streaming)
- **2.072**: GraphQL (query language, schema-first, client-driven)

## Candidate Implementations (5+ Required for Tier 2)

### Server Implementations
1. **Apollo Server** (Node.js) - Most popular, extensions ecosystem
2. **Hasura** (Haskell) - Auto-generates from Postgres, real-time subscriptions
3. **Postgraphic** (Postgres-native) - Database-first approach
4. **GraphQL Yoga** (Node.js) - Lightweight, standards-compliant
5. **Hot Chocolate** (.NET) - Microsoft ecosystem
6. **Strawberry** (Python) - Type-safe, modern Python
7. **gqlgen** (Go) - Code-generation approach
8. **Juniper** (Rust) - Type-safe Rust implementation

### Federation Implementations
- **Apollo Federation** (proprietary extensions)
- **Mercurius** (Fastify-based)
- **GraphQL Mesh** (schema stitching)

## Use Case: API Design Portability

**Context**: Building API for multi-service application

**Requirements**:
- Schema-first design (contract-driven development)
- Client-driven queries (no over/under-fetching)
- Introspection for tooling (GraphiQL, schema validation)
- Portability: Switch between Node.js, Postgres-native, or Python implementations
- Federation: Compose schemas from multiple services
- Zero lock-in: Avoid proprietary extensions

**Success Criteria**:
- GraphQL schema portable across 3+ implementations (no syntax changes)
- Queries portable across implementations (standard compliance)
- Migration cost <40 hours (schema + resolver porting)
- Federation possible without vendor lock-in (Apollo Federation vs open alternatives)

## Discovery Methodology

Following MPSE Tier 2 framework:

### S1: Rapid Discovery (Target: 1.5-2 hours)
**Focus**: Specification overview, major implementations, ecosystem
- GraphQL specification features (queries, mutations, subscriptions, introspection)
- Top 5-7 implementations (stars, activity, language)
- Proprietary extensions landscape (Apollo Federation, Hasura subscriptions)
- Quick portability test: Same schema on 2-3 implementations

### S2: Comprehensive Discovery (Target: 2-3 hours)
**Focus**: Deep portability analysis, migration costs
- **Backend Compatibility Matrix**: Which features are standard vs proprietary
- **Migration Cost Analysis**: Hours to switch between implementations
- **Schema Portability**: Test same schema on 3+ implementations
- **Federation Portability**: Apollo Federation vs open alternatives
- **Lock-in Assessment**: Scoring 0-100 (target: <20 for standard-compliant)

### S3: Need-Driven Discovery (Target: 1.5-2 hours)
**Focus**: Use case scenarios requiring API portability
- **Scenario 1**: Postgres-first API (Postgraphic vs Hasura)
- **Scenario 2**: Multi-service architecture (Federation patterns)
- **Scenario 3**: Cloud migration (Node.js to managed service)
- **Scenario 4**: Language switch (Node.js → Python → Go)

### S4: Strategic Discovery (Target: 1.5-2 hours)
**Focus**: Specification evolution, ecosystem health, future-proofing
- **Specification Stability**: How often does spec change? Breaking changes?
- **Governance**: GraphQL Foundation neutrality vs Apollo influence
- **Ecosystem Trends**: Federation adoption, subscription patterns
- **10-Year Outlook**: GraphQL vs REST/gRPC coexistence
- **Lock-in Evolution**: Are proprietary extensions becoming standard?

**Total estimated time**: 7-9 hours

## Deliverables

1. **S1-S4 Discovery Documents**: Standard vs proprietary analysis
2. **Backend Compatibility Matrix**: 5+ implementations feature comparison
3. **Migration Cost Analysis**: Hours to switch implementations
4. **DOMAIN_EXPLAINER.md**: GraphQL as an API design standard
5. **DISCOVERY_SYNTHESIS.md**: Cross-methodology portability recommendation
6. **Recommendation**: When to use GraphQL standard, how to minimize lock-in

## Related Research

**Tier 2 (Open Standards) - API Layer**:
- **2.070**: OpenAPI/REST (request/response, resource-oriented)
- **2.071**: gRPC (RPC-style, Protocol Buffers, streaming)
- **2.072**: GraphQL (query language, schema-first, client-driven) ← THIS EXPERIMENT

**Tier 3 (Managed Services)**:
- **3.200**: LLM APIs (many use REST, some exploring GraphQL)
- **3.400**: Backend-as-a-Service (Hasura, Supabase GraphQL layers)

**Tier 1 (Libraries)**:
- Server implementations are Tier 1 (Apollo Server, Hasura, etc.)
- This experiment focuses on standard portability, not library selection

## Success Metrics

### Tier 2 Standards Assessment

- **Standards Body**: GraphQL Foundation (Linux Foundation) ✓
- **Maturity Level**: Production-grade, Oct 2021 specification
- **Backend Compatibility**: Target 5+ implementations
- **Migration Cost**: Target <40 hours to switch implementations
- **Lock-in Score**: Target <20/100 (standard-compliant = low lock-in)

### Portability Validation

- Same schema runs on 3+ implementations without changes
- Queries portable across implementations (no proprietary syntax)
- Federation patterns work without Apollo lock-in
- Clear migration playbook (Implementation A → Implementation B)

### Comparison with Related Standards

| Standard | Style | Streaming | Introspection | Schema-First | Lock-In |
|----------|-------|-----------|---------------|--------------|---------|
| OpenAPI/REST | Resource | No | Via spec docs | Optional | Low |
| gRPC | RPC | Yes | Via .proto | Required | Low-Medium |
| **GraphQL** | Query | Yes (subs) | Built-in | Required | **Target: Low** |

## Next Steps

1. **S1 Rapid Discovery** (TODAY):
   - Read GraphQL spec (spec.graphql.org)
   - Survey 5-7 implementations (GitHub stars, last update, language)
   - Identify proprietary extensions (Apollo Federation, Hasura features)
   - Quick portability test: Deploy same schema to Apollo Server + GraphQL Yoga
   - Document in `01-discovery/S1-rapid/`

2. **S2 Comprehensive** (Day 2):
   - Backend compatibility matrix (5+ implementations)
   - Migration cost estimates (implementation switching)
   - Schema portability validation (3+ servers)
   - Federation portability (Apollo vs open)

3. **S3-S4** (Days 3-4):
   - Use case scenarios
   - Strategic analysis (10-year outlook)
   - Final synthesis and recommendation

## Research Log

- **2025-11-19**: Project initialized, directory structure created
- Next: S1 Rapid Discovery - GraphQL specification and ecosystem survey

---

**Status**: ⬜ S1 Pending | ⬜ S2 Pending | ⬜ S3 Pending | ⬜ S4 Pending
**Next Action**: S1 - Read GraphQL spec, survey implementations, test portability
