# S3 Scenario 4: Enterprise Knowledge Base (Unified Internal Search)

**Company Profile**: Mid to large enterprise, 1,000-10,000 employees
**Search Volume**: 5M documents (Confluence, SharePoint, Google Drive, Slack), 1M searches/month
**Budget**: $2K-100K/year for enterprise search
**Priority**: Unified search across 10-100 data sources, document-level security, SSO, ML relevance

---

## Business Context

### Company Details
- **Stage**: Growth to Enterprise (Series C+ or Public)
- **Team Size**: 1,000-10,000 employees
- **IT Team**: 50-200 IT staff, 5-20 on knowledge management
- **Revenue**: $100M-10B ARR
- **Growth**: 20-50% YoY (M&A activity, integration complexity)
- **Business Model**: B2B SaaS, enterprise software, consulting

### Technical Environment
- **Data Sources**: 10-100 systems (Confluence, SharePoint, Google Drive, Slack, Jira, Salesforce, ServiceNow, Box, Notion, GitHub, etc.)
- **Document Volume**: 5M documents (1M active, 4M archived)
- **Content Types**: Documents (40%), wiki pages (25%), chat messages (20%), tickets (10%), code (5%)
- **Update Frequency**: 10K-100K documents updated/day
- **Search Traffic**: 1M searches/month (10K employees × 100 searches/month)
- **Geographic Distribution**: Global (US, Europe, APAC, multi-region)
- **Security**: Document-level permissions (RBAC, SSO, Active Directory/Okta)

### Enterprise Search Requirements
- **Unified Search**: Single search bar across all systems (no silo hopping)
- **100+ Connectors**: Pre-built integrations (Confluence, SharePoint, Salesforce, ServiceNow, etc.)
- **Document-Level Security**: Respect permissions (user can only search docs they can access)
- **SSO Integration**: SAML 2.0, Active Directory, Okta, Azure AD
- **ML Relevance**: Learning to rank, behavioral signals (clicks, dwell time)
- **Federated Search**: Search multiple systems simultaneously (real-time or cached)
- **Compliance**: SOC 2, GDPR, HIPAA (audit logs, data residency)
- **Latency**: <500ms p95 (acceptable for enterprise search, not instant)
- **Scale**: 5M+ documents, 1M+ searches/month, 10K+ concurrent users

---

## Search Platform Evaluation

### Evaluation Criteria

| Criterion | Weight | Coveo | Azure AI Search | AWS OpenSearch | Algolia Premium | Meilisearch | Notes |
|-----------|--------|-------|----------------|---------------|----------------|-------------|-------|
| **100+ Connectors** | 30% | 10/10 | 7/10 | 4/10 | 3/10 | 2/10 | Coveo 100+ native, Azure 50+, others DIY |
| **Document Security** | 25% | 10/10 | 9/10 | 7/10 | 5/10 | 3/10 | Coveo/Azure enterprise-grade RBAC |
| **ML Relevance** | 15% | 10/10 | 8/10 | 6/10 | 9/10 | 4/10 | Coveo/Algolia best ML, Azure semantic |
| **Enterprise Support** | 10% | 10/10 | 8/10 | 7/10 | 8/10 | 5/10 | Coveo white-glove, Azure good |
| **Compliance (SOC 2, GDPR)** | 10% | 10/10 | 9/10 | 8/10 | 8/10 | 6/10 | All certified, Coveo most mature |
| **Cost Efficiency** | 10% | 3/10 | 6/10 | 6/10 | 4/10 | 9/10 | Coveo very expensive, Meili cheap |
| **Total Score** | 100% | **8.9/10** | **7.7/10** | **6.1/10** | **6.0/10** | **4.5/10** | Coveo wins for enterprise |

### Winner: Coveo (for large enterprises with budget $50K+/year, need 100+ connectors)
### Alternative: Azure AI Search (for Azure-native enterprises, budget $20K-50K/year)
### Budget Option: AWS OpenSearch + DIY Connectors (for tech-savvy teams, budget $10K-20K/year)

---

## Platform Deep Dive

### Option 1: Coveo Platform (Recommended for Fortune 500)

**Pricing**: **$50K-500K/year** (starts at $50K, scales with users, sources, queries)

**Pricing Model**:
- Base: $50K/year (1,000 users, 10 sources, 500K queries/month)
- Mid-market: $100K-200K/year (5,000 users, 50 sources, 2M queries/month)
- Enterprise: $200K-500K/year (10,000+ users, 100+ sources, 10M+ queries/month)

**Pros**:
- ✅ **100+ native connectors** (Confluence, SharePoint, Salesforce, ServiceNow, Box, Slack, Jira, GitHub, Notion, etc.)
- ✅ **Best ML relevance** (0.92 MRR, automatic learning from user behavior)
- ✅ **Document-level security** (automatic permission inheritance, RBAC)
- ✅ **SSO integration** (SAML 2.0, Active Directory, Okta, Azure AD, custom)
- ✅ **White-glove support** (dedicated CSM, 24/7 phone, <1h response SLA)
- ✅ **Enterprise compliance** (SOC 2, GDPR, HIPAA, ISO 27001, all regions)
- ✅ **Analytics dashboard** (query analytics, click tracking, no-results monitoring)
- ✅ **Salesforce/ServiceNow native** (embedded search, single-click integration)

**Cons**:
- ⚠️ **Very expensive** ($50K-500K/year vs AWS OpenSearch $10K-40K/year, 5-10× more)
- ⚠️ **Enterprise-only** (no self-service, requires sales engagement)
- ⚠️ **6-24 month lock-in** (6-24 month migration effort if leave)
- ⚠️ **100-250ms latency** (trades speed for ML relevance, slower than Algolia)

**TCO (3-year, 10K employees, 50 sources, 1M searches/month)**:
- License: $150K/year × 3 years = **$450,000**
- Implementation (400-800 hours): 600 hours × $150/hour = **$90,000**
- Maintenance (20 hours/month): 20 × 36 months × $150 = **$108,000**
- **Total TCO**: **$648,000** (3-year)

**When to Choose Coveo**:
- Fortune 500 or large enterprise (>5,000 employees)
- Need 50-100+ connectors (saves 500-2,000 hours vs DIY)
- Budget $50K-500K/year (can afford premium)
- Salesforce/ServiceNow heavy (native integrations)
- ML relevance critical (automatic learning, best-in-class)

**ROI Calculation**:
- **Time savings**: 100 connectors × 20 hours/connector (DIY) = 2,000 hours saved
- **Value**: 2,000 hours × $150/hour = **$300K saved**
- **Productivity gain**: 10K employees × 30 min/week faster search × 50 weeks × $50/hour = **$1.25M/year**
- **3-year value**: $300K + ($1.25M × 3) = **$4.05M**
- **Cost**: $648K
- **ROI**: ($4.05M - $648K) / $648K = **5.2× ROI**

---

### Option 2: Azure AI Search (Best for Azure-Native Enterprises)

**Pricing**: **$500-5K/month** ($6K-60K/year, scales with tier and replicas)

**Pricing Tiers**:
- Standard S1: $250/month (25GB, 3 replicas, 1M docs)
- Standard S2: $1,000/month (100GB, 12 replicas, 10M docs)
- Standard S3: $2,000/month (200GB, 12 replicas, 50M docs)
- Standard S3 HD: $4,000/month (1TB, 12 replicas, 200M docs)

**1M searches/month pricing**: Standard S2 ($1,000/month) = **$12K/year**

**Pros**:
- ✅ **50+ native indexers** (Azure Blob, SharePoint Online, Cosmos DB, SQL Database, Azure Data Lake)
- ✅ **Cognitive Skills** (OCR, entity recognition, key phrase extraction, language detection)
- ✅ **Semantic search** (L2 reranking, semantic understanding, better than keyword)
- ✅ **Azure AD integration** (RBAC, SSO, document-level security via Azure AD groups)
- ✅ **Blob Storage indexing** (zero-ETL, automatic crawling)
- ✅ **Azure ecosystem** (OpenAI, Cognitive Services, Synapse, Power BI)
- ✅ **Compliance** (SOC 2, GDPR, HIPAA, Azure trust center)

**Cons**:
- ⚠️ **Azure lock-in** (requires Azure Blob, AD, cognitive services, hard to migrate)
- ⚠️ **50-150ms latency** (slower than Algolia, acceptable for enterprise)
- ⚠️ **Complex OData queries** (steep learning curve, 2-4 weeks setup)
- ⚠️ **Limited connectors** (50+ Azure-native, but need DIY for Confluence, Slack, Jira)

**TCO (3-year, 5M docs, 1M searches/month)**:
- License: $1,000/month × 36 months = **$36,000**
- Connector development (500 hours): 500 × $150 = **$75,000**
- Maintenance (15 hours/month): 15 × 36 × $150 = **$81,000**
- **Total TCO**: **$192,000** (3-year)

**When to Choose Azure AI Search**:
- Azure-heavy (already using Blob Storage, Azure AD, Azure SQL)
- Need cognitive skills (OCR, entity extraction, multilingual)
- Budget $10K-50K/year (mid-market enterprise)
- Don't need 100+ connectors (can DIY 10-20 key systems)

**ROI Calculation**:
- **Productivity gain**: 5K employees × 30 min/week × 50 weeks × $50/hour = **$625K/year**
- **3-year value**: $625K × 3 = **$1.875M**
- **Cost**: $192K
- **ROI**: ($1.875M - $192K) / $192K = **8.8× ROI**

---

### Option 3: AWS OpenSearch + DIY Connectors (Budget-Conscious)

**Pricing**: **$1,200-3K/month** ($14K-36K/year, scales with instance size)

**AWS OpenSearch Setup**:
- 3× m5.xlarge.search instances (4 vCPU, 16GB RAM each)
- 3 replicas (high availability)
- 1TB storage (SSD, gp3)
- Cost: ~$1,500/month = **$18K/year**

**Pros**:
- ✅ **AWS integration** (IAM, CloudWatch, S3 snapshots, Kinesis, Lambda)
- ✅ **Proven at scale** (50B+ documents, battle-tested)
- ✅ **Powerful aggregations** (analytics, dashboards, visualizations)
- ✅ **OpenSearch Dashboards** (built-in, Kibana fork, analytics UI)
- ✅ **Cost-effective** ($18K/year vs Coveo $150K/year, 8× cheaper)

**Cons**:
- ⚠️ **DIY connectors** (need to build 10-50 connectors, 200-1,000 hours)
- ⚠️ **DIY document security** (need to implement RBAC, 100-200 hours)
- ⚠️ **Complex setup** (clusters, shards, replicas, 4-8 weeks implementation)
- ⚠️ **Higher maintenance** (30-40 hours/month vs Coveo 10-20 hours/month)

**TCO (3-year, 5M docs, 1M searches/month)**:
- License: $1,500/month × 36 months = **$54,000**
- Connector development (800 hours): 800 × $150 = **$120,000**
- RBAC implementation (200 hours): 200 × $150 = **$30,000**
- Maintenance (30 hours/month): 30 × 36 × $150 = **$162,000**
- **Total TCO**: **$366,000** (3-year)

**When to Choose AWS OpenSearch**:
- AWS-native (already using S3, IAM, CloudWatch, Kinesis)
- Tech-savvy team (comfortable building connectors, RBAC)
- Budget $15K-40K/year (can't afford Coveo, but need scale)
- Need 10-20 connectors (not 100+, DIY is feasible)

**ROI Calculation**:
- **Productivity gain**: 5K employees × 30 min/week × 50 weeks × $50/hour = **$625K/year**
- **3-year value**: $625K × 3 = **$1.875M**
- **Cost**: $366K
- **ROI**: ($1.875M - $366K) / $366K = **4.1× ROI**

---

### Option 4: Algolia Premium (Not Ideal for Enterprise Search)

**Pricing**: $5K-25K/month ($60K-300K/year)

**Why Not Recommended**:
- ❌ **No native connectors** (DIY for Confluence, SharePoint, Salesforce, etc.)
- ❌ **Limited document security** (basic RBAC, not enterprise-grade)
- ❌ **Expensive** ($60K-300K/year vs Azure AI Search $12K-60K/year, 5× more)
- ❌ **Optimized for different use case** (e-commerce, instant search, not enterprise knowledge)

**Only Consider If**: Need <50ms global latency (rare for enterprise search, 100-500ms acceptable)

---

## Architecture Pattern: Enterprise Unified Search

### Phase 1: Connector Integration (Coveo)

**Architecture**:
```
┌─────────────────────────────────────────────────────────────────┐
│                   Enterprise Search Portal                       │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ Unified Search UI (Single Search Bar)                    │   │
│  │  - Search box (autocomplete, query suggestions)           │   │
│  │  - Results (title, snippet, source, date, author)         │   │
│  │  - Facets (source, content type, date, department)        │   │
│  │  - SSO (Okta, Azure AD, SAML 2.0)                         │   │
│  │  - Document preview (inline, modal)                       │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                          │
                          │ Search API (with user context)
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                   Coveo Platform (Cloud)                         │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ Security Layer (Document-Level Permissions)               │   │
│  │  - User groups: Engineering, Sales, Marketing, HR        │   │
│  │  - Document ACLs: [Engineering], [All], [HR-only]        │   │
│  │  - Query: "performance review" → filter by ACL (HR-only) │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ Unified Index (5M documents from 50+ sources)             │   │
│  │  - Fields: title, body, source, author, date, ACLs        │   │
│  │  - ML Ranking: clicks, dwell time, conversions            │   │
│  │  - Searchable: title, body, metadata                      │   │
│  │  - Facets: source, content_type, date, department         │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                          │
                          │ Connectors (100+ native)
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                   Data Sources (10-100 systems)                  │
│                                                                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ Confluence   │  │ SharePoint   │  │ Google Drive │          │
│  │ (1M pages)   │  │ (2M docs)    │  │ (500K docs)  │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│                                                                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ Slack        │  │ Salesforce   │  │ ServiceNow   │          │
│  │ (500K msgs)  │  │ (200K recs)  │  │ (100K tkts)  │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│                                                                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ Jira         │  │ Notion       │  │ Box          │          │
│  │ (100K issues)│  │ (50K pages)  │  │ (300K docs)  │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└─────────────────────────────────────────────────────────────────┘
```

**Data Flow**:
1. **User searches** ("Q3 sales presentation") → Coveo receives query + user identity (via SSO)
2. **Security filter** → Coveo checks user's groups (Sales team) → filters index to docs user can access
3. **ML ranking** → Coveo ranks results by relevance + user behavior (past clicks, dwell time)
4. **Results returned** → Show top 10 results from Confluence, SharePoint, Google Drive (user has access)
5. **User clicks result** → Coveo tracks click, updates ML model (learn from behavior)

---

### Phase 2: Document Security (RBAC)

**Permission Inheritance**:
```
Confluence Space: "Sales Playbooks"
  - Permissions: Sales team (read), Sales leadership (read+write)
  - Documents: 500 pages

User: john@company.com
  - Groups: Sales team, Engineering
  - Query: "sales playbook"
  - Result: Can see "Sales Playbooks" (has Sales team access)

User: jane@company.com
  - Groups: Engineering, Product
  - Query: "sales playbook"
  - Result: Cannot see "Sales Playbooks" (no Sales team access)
```

**Coveo Implementation** (automatic):
- Connector crawls Confluence → extracts document ACLs (Sales team = read)
- Stores in index: `{ id: "page-123", title: "Q3 Sales Playbook", acl: ["Sales team"] }`
- User searches → Coveo adds filter: `acl IN user.groups` → only returns docs user can access

**DIY Implementation** (OpenSearch):
```javascript
// Index documents with ACLs
await opensearchClient.index({
  index: 'knowledge_base',
  id: 'confluence-page-123',
  body: {
    title: 'Q3 Sales Playbook',
    body: '...',
    source: 'Confluence',
    acl: ['Sales team', 'Sales leadership'] // Groups that can access this doc
  }
});

// Search with security filter
async function search(query, userGroups) {
  const results = await opensearchClient.search({
    index: 'knowledge_base',
    body: {
      query: {
        bool: {
          must: [
            { multi_match: { query: query, fields: ['title', 'body'] } }
          ],
          filter: [
            { terms: { acl: userGroups } } // Only docs user can access
          ]
        }
      }
    }
  });

  return results.hits.hits;
}

// Usage
const userGroups = ['Sales team', 'Engineering']; // From SSO/JWT
const results = await search('sales playbook', userGroups);
```

---

## Implementation Guide

### Option A: Coveo Implementation (4-6 Months)

**Phase 1: Planning & Design (Month 1)**
1. Identify data sources (Confluence, SharePoint, Salesforce, etc.)
2. Map user groups (Sales, Engineering, HR, etc.)
3. Define search UI requirements (facets, filters, ranking)
4. Engage Coveo sales (get quote, sign contract)

**Phase 2: Connector Configuration (Months 2-3)**
```yaml
# Coveo connectors (configure via admin console)
connectors:
  - name: Confluence
    type: Confluence Cloud
    url: https://company.atlassian.net
    auth: OAuth 2.0
    credentials: ${CONFLUENCE_API_TOKEN}
    schedule: Every 1 hour (incremental), Daily (full)
    permissions: Inherit from Confluence (space, page-level)

  - name: SharePoint Online
    type: SharePoint Online
    url: https://company.sharepoint.com
    auth: Azure AD OAuth
    credentials: ${SHAREPOINT_CLIENT_ID}
    schedule: Every 1 hour (incremental), Daily (full)
    permissions: Inherit from SharePoint (site, library-level)

  - name: Slack
    type: Slack
    workspace: https://company.slack.com
    auth: Slack App OAuth
    credentials: ${SLACK_BOT_TOKEN}
    schedule: Every 15 minutes (real-time)
    permissions: Inherit from Slack (channel membership)

  # ... (50+ more connectors)
```

**Phase 3: Search UI Development (Month 4)**
```jsx
// React search portal
import React, { useState } from 'react';
import { CoveoSearchBox, CoveoResultList, CoveoFacet, CoveoQuerySummary } from '@coveo/headless-react';

function EnterpriseSearch() {
  const [user, setUser] = useState(null);

  // Fetch user from SSO (Okta, Azure AD)
  useEffect(() => {
    fetchUserFromSSO().then(setUser);
  }, []);

  return (
    <div className="enterprise-search">
      <h1>Search {user?.name}'s Knowledge Base</h1>

      <CoveoSearchBox
        placeholder="Search Confluence, SharePoint, Slack, and more..."
        suggestions={true}
        userContext={{ userId: user?.id, groups: user?.groups }}
      />

      <div className="search-layout">
        <aside className="facets">
          <CoveoFacet field="source" title="Source" />
          <CoveoFacet field="content_type" title="Content Type" />
          <CoveoFacet field="date" title="Date" />
          <CoveoFacet field="department" title="Department" />
        </aside>

        <main className="results">
          <CoveoQuerySummary />
          <CoveoResultList
            resultTemplate={(result) => (
              <div className="result">
                <h3><a href={result.clickUri}>{result.title}</a></h3>
                <p>{result.excerpt}</p>
                <div className="meta">
                  <span className="source">{result.raw.source}</span>
                  <span className="author">By {result.raw.author}</span>
                  <span className="date">{new Date(result.raw.date).toLocaleDateString()}</span>
                </div>
              </div>
            )}
          />
        </main>
      </div>
    </div>
  );
}
```

**Phase 4: Testing & Launch (Months 5-6)**
- User acceptance testing (UAT with 50-100 employees)
- Relevance tuning (clicks, dwell time, no-results queries)
- Performance testing (1M searches/month load)
- Full launch (10K employees)

**Total Implementation**: 4-6 months, 400-800 hours

---

## Testing & Validation

### Security Testing

**Test document-level permissions**:
```javascript
// Test: User can only search docs they can access
const testCases = [
  {
    user: { email: 'john@company.com', groups: ['Sales team', 'Engineering'] },
    query: 'Q3 sales playbook',
    expectedSources: ['Confluence:Sales Playbooks', 'Google Drive:Sales Shared'],
    forbiddenSources: ['SharePoint:HR Documents']
  },
  {
    user: { email: 'jane@company.com', groups: ['Engineering', 'Product'] },
    query: 'Q3 sales playbook',
    expectedSources: [], // No access to Sales content
    forbiddenSources: ['Confluence:Sales Playbooks']
  }
];

for (const test of testCases) {
  const results = await coveoSearch(test.query, test.user);
  const sources = results.hits.map(hit => `${hit.source}:${hit.space}`);

  console.log(`User: ${test.user.email}, Query: "${test.query}"`);
  console.log(`Expected sources: ${test.expectedSources.join(', ')}`);
  console.log(`Actual sources: ${sources.join(', ')}`);
  console.log(`Security: ${test.forbiddenSources.every(src => !sources.includes(src)) ? '✅' : '❌ SECURITY VIOLATION'}`);
}
```

---

## Cost-Benefit Analysis (3-Year)

### Scenario: Enterprise (10K employees)

**Baseline (No Unified Search)**:
- Employees spend 2 hours/week searching for information (switching between Confluence, SharePoint, Slack, etc.)
- 52 weeks/year × 2 hours/week × 10K employees = **1.04M hours/year** spent searching

**With Unified Search (Coveo/Azure AI Search)**:
- Employees spend 1 hour/week searching (50% faster with unified search)
- 52 weeks/year × 1 hour/week × 10K employees = **520K hours/year**
- **Time saved**: 520K hours/year

**Productivity Value**:
- Average employee cost: $50/hour (loaded cost)
- Time saved: 520K hours/year × $50/hour = **$26M/year**
- **3-year value**: $26M × 3 = **$78M**

**TCO**:
- Coveo: $648K (3-year)
- Azure AI Search: $192K (3-year)
- AWS OpenSearch: $366K (3-year)

**ROI**:
- **Coveo**: ($78M - $648K) / $648K = **120× ROI**
- **Azure AI Search**: ($78M - $192K) / $192K = **406× ROI** (best)
- **AWS OpenSearch**: ($78M - $366K) / $366K = **213× ROI**

**Winner**: All options have massive ROI (enterprise search is high-value investment)

---

## Final Recommendation

### For Large Enterprise (>5,000 employees, budget $50K+/year):

**Choose Coveo**:
- ✅ 100+ native connectors (saves 500-2,000 hours vs DIY)
- ✅ Best ML relevance (automatic learning, 0.92 MRR)
- ✅ Document-level security (automatic permission inheritance)
- ✅ White-glove support (24/7, <1h response SLA)
- ✅ 120× ROI (3-year, productivity gains)

### For Azure-Native Enterprise (budget $10K-50K/year):

**Choose Azure AI Search**:
- ✅ 50+ Azure-native indexers (Blob, SharePoint, SQL, Cosmos)
- ✅ Cognitive skills (OCR, entity extraction, semantic search)
- ✅ Azure AD integration (RBAC, SSO)
- ✅ 406× ROI (3-year, best ROI due to lower cost)

### For Tech-Savvy, Budget-Conscious (budget $10K-40K/year):

**Choose AWS OpenSearch + DIY**:
- ✅ Cost-effective ($18K/year vs Coveo $150K/year)
- ✅ AWS integration (IAM, S3, CloudWatch, Kinesis)
- ✅ Proven at scale (50B+ docs)
- ✅ 213× ROI (3-year)

---

**Last Updated**: November 14, 2025
**Scenario**: Enterprise Knowledge Base (Unified Internal Search)
**Recommended Platform**: Coveo (large enterprise) or Azure AI Search (Azure-native)
**Expected ROI**: 120-406× (3-year, massive productivity gains)
