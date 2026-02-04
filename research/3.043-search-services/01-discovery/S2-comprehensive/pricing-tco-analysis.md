# S2 Comprehensive: Pricing & TCO Analysis

**Total Cost of Ownership models across 7 search platforms**
**Last Updated**: November 14, 2025
**Analysis Period**: 3-year TCO projections
**Scenarios**: 6 usage profiles from small SaaS to large-scale marketplace

---

## Pricing Model Overview

| Platform | Pricing Model | Free Tier | Entry Paid | Cost Drivers | Pricing Transparency |
|----------|---------------|-----------|------------|--------------|---------------------|
| **Algolia** | Usage-based (searches + records) | 10K searches/mo | $0/mo → $1+ | Searches, records, bandwidth | Good (public pricing) |
| **Meilisearch** | Hybrid (usage or resources) | 50K searches/mo | $30/mo (Build) | Searches or RAM/CPU | Excellent (transparent) |
| **Typesense** | Resource-based (RAM/CPU) | None (OSS free) | $20/mo (Hobby) | RAM, CPU, nodes | Excellent (fixed tiers) |
| **Elasticsearch** | Tiered + usage (serverless option) | Limited | $95/mo (Basic) | Nodes, storage, data transfer | Moderate (complex calculator) |
| **AWS OpenSearch** | Instance + storage + transfer | 750hr/12mo (free tier) | ~$100/mo | Instance type, storage, I/O, transfer | Good (AWS calculator) |
| **Azure AI Search** | Tiered + AI enrichment | None | $74/mo (Basic) | Tier level, AI skillsets, bandwidth | Moderate (Azure calculator) |
| **Coveo** | Enterprise contracts (annual) | None | $50K/year | Queries, users, connectors, ML features | Poor (custom quotes only) |

**Key Insights**:
- **Algolia** usage-based = unpredictable costs (can spike 10× with traffic growth)
- **Typesense** most predictable (fixed resource pricing, no usage surprises)
- **Meilisearch** flexible (choose usage-based OR resource-based)
- **Coveo** enterprise-only (no SMB option, requires $50K+ annual budget)
- **Open-source options** (Meilisearch, Typesense, Elasticsearch) allow self-hosting to reduce costs

---

## Detailed Pricing Tiers

### Algolia Pricing (2025)

| Tier | Monthly Cost | Searches Included | Records Included | Overage Rates | Key Features |
|------|--------------|-------------------|------------------|---------------|--------------|
| **Build (Free)** | $0 | 10,000 | 1M | N/A | Basic search, typo tolerance, faceting |
| **Grow** | $0 base + usage | 10K (then $0.50/1K) | 100K (then $0.40/1K) | $0.50-1.75/1K searches | Analytics, advanced filtering |
| **Grow Plus** | Usage-based | $1.75/1K searches | $0.40/1K records | Higher rates | AI features, semantic search |
| **Premium** | $2K-10K+/mo | Negotiated | Negotiated | Custom | Personalization, LTR, A/B testing |
| **Elevate** | $10K-50K+/mo | Negotiated | Negotiated | Custom | NeuralSearch, full AI suite |

**Overage Pricing Examples**:
- 100K searches/month: $45 (after 10K free = 90K × $0.50/1K)
- 500K searches/month: $245 (490K × $0.50/1K)
- 1M searches/month: $495 (990K × $0.50/1K)
- 5M searches/month: $2,495 (4.99M × $0.50/1K)

**Negotiation Tips** (from web research):
- Standard discount: 24-34% on 24-month contracts
- Overage rate reduction: 30-50% (negotiate $0.25-0.35/1K instead of $0.50)
- Annual prepay discount: Additional 10-15%

**Hidden Costs**:
- Bandwidth: Typically included but can be charged at high scale
- Analytics retention: >90 days requires Premium tier
- Advanced features (AI, personalization): Require $10K+/month tiers

---

### Meilisearch Pricing (2025)

**Option 1: Usage-Based Pricing**

| Tier | Monthly Cost | Searches Included | Documents Included | Overage Rates |
|------|--------------|-------------------|-------------------|---------------|
| **Build** | $30 | 50,000 | 100,000 | $0.60/1K searches, $0.20/1K docs |
| **Pro** | $300 | 1,000,000 | 1,000,000 | $0.30/1K searches, $0.10/1K docs |

**Option 2: Resource-Based Pricing**

| Tier | Monthly Cost | RAM | CPU | Storage |
|------|--------------|-----|-----|---------|
| **Starter** | $30 | 2 GB | 0.5 vCPU | 50 GB |
| **Growth** | $100 | 8 GB | 2 vCPU | 200 GB |
| **Pro** | $300 | 16 GB | 4 vCPU | 500 GB |
| **Custom** | Custom | Custom | Custom | Custom |

**Key Advantages**:
- **Flexibility**: Choose usage-based OR resource-based (switch anytime)
- **MIT License**: Self-host for free (unlimited scale)
- **Hybrid Search**: Included at all tiers (even $30/month Build plan)
- **No overage surprises**: Resource-based = fixed cost
- **14-day free trial**: Test before committing

**Cost Examples**:
- 500K searches, 1M docs: $300/month (Pro plan)
- 2M searches, 5M docs: ~$600-900/month (usage-based overages or custom)
- Self-hosted: $0 license + infrastructure (e.g., $100-300/month cloud VMs)

---

### Typesense Pricing (2025)

**Typesense Cloud (Managed)**

| Tier | Monthly Cost | RAM | CPU | Storage | QPS Estimate |
|------|--------------|-----|-----|---------|--------------|
| **Hobby** | $20 | 0.5 GB | 0.5 vCPU | 10 GB | ~500 QPS |
| **Starter** | $49 | 2 GB | 1 vCPU | 50 GB | ~2K QPS |
| **Growth** | $120 | 8 GB | 4 vCPU | 200 GB | ~10K QPS |
| **Business** | $300 | 16 GB | 8 vCPU | 500 GB | ~20K QPS |
| **Enterprise** | $600+ | 32+ GB | 16+ vCPU | 1+ TB | 50K+ QPS |

**Self-Hosted (Open-Source)**

- **License**: GPL v3 (free for open-source projects, commercial license available)
- **Infrastructure cost**: $50-500/month (cloud VMs depending on scale)
- **Support**: Community (free) or paid support contracts

**Key Advantages**:
- **Fixed pricing**: No usage-based surprises (know exact cost)
- **Best price/performance**: $120/month handles 500K searches (vs Algolia $245+)
- **InstantSearch compatible**: Easy migration from Algolia
- **Memory-based pricing**: 25% overhead vs Algolia (per user reports)

**Cost Examples**:
- 100K docs, 500K searches: $120/month (Growth tier)
- 1M docs, 2M searches: $300/month (Business tier)
- 5M docs, 10M searches: $600-900/month (Enterprise tier)

---

### Elasticsearch Pricing (2025)

**Elastic Cloud (Managed)**

| Tier | Monthly Cost | Use Case | Storage | RAM | Features |
|------|--------------|----------|---------|-----|----------|
| **Basic** | $95+ | Dev/test | 8 GB | 1 GB | Basic search, security |
| **Standard** | $200+ | Small production | 30 GB | 4 GB | Alerting, ML (limited) |
| **Gold** | $500+ | Production | 100+ GB | 8+ GB | SAML, advanced ML |
| **Platinum** | $1,000+ | Enterprise | 500+ GB | 16+ GB | Full ML, advanced security |
| **Serverless** | Usage-based | Variable workloads | Pay per use | Elastic | Auto-scaling, simplified |

**Self-Hosted (Open Source + Paid Subscriptions)**

- **Open Source**: Free (Elastic License 2.0, not fully open)
- **Basic**: Free (includes X-Pack basic features)
- **Gold**: $95/month per node (advanced features)
- **Platinum**: Contact sales (full feature set)

**Serverless Pricing** (Simplified):
- **Search**: ~$0.10-0.30 per GB ingested
- **Observability**: ~$0.40-0.60 per GB ingested
- **Security**: ~$0.20-0.40 per GB ingested

**Key Considerations**:
- **Complex pricing**: Instance type + storage + data transfer + features
- **Hidden costs**: Cross-region replication, snapshots, monitoring
- **Engineering time**: High DevOps overhead (cluster management, tuning)

**Cost Examples**:
- Small cluster (3× m6g.large): $660/month (AWS self-hosted)
- Medium cluster (Elastic Cloud Gold): $800-1,200/month
- Large cluster (production): $2K-10K+/month

---

### AWS OpenSearch Pricing (2025)

**Pricing Components**:
1. **Instance costs**: $0.10-2.00+/hour (depending on instance type)
2. **Storage**: $0.10-0.135/GB-month (GP3, Magnetic, or UltraWarm)
3. **Data transfer**: $0.09-0.20/GB (outbound, varies by region)
4. **Optional**: Serverless, reserved instances (30-75% discount)

**Common Configurations**:

| Configuration | Monthly Cost | Use Case | Capacity |
|---------------|--------------|----------|----------|
| **Dev/Test** | $100-200 | Development | 1× t3.small + 100GB |
| **Small Production** | $400-600 | Small apps | 2× m6g.large + 500GB |
| **Medium Production** | $1,000-2,000 | Mid-scale | 3× m6g.xlarge + 1TB |
| **Large Production** | $3,000-10,000+ | Enterprise | 6+ r6g.2xlarge + multi-TB |

**Reserved Instance Pricing** (1-year commitment):
- **1-year**: 30-42% discount
- **3-year**: 50-75% discount

**Serverless Pricing** (Preview/GA in 2024-2025):
- **OCU** (OpenSearch Compute Units): ~$0.24/OCU-hour
- **Storage**: ~$0.024/GB-month
- **Estimated**: $500-2,000/month for typical workloads

**Key Advantages**:
- **AWS integration**: Free data transfer within VPC, IAM, CloudWatch, S3, Bedrock
- **Reserved instances**: Significant cost savings for predictable workloads
- **UltraWarm**: 90% storage cost reduction for warm/cold data

**Cost Example** (1TB data, 500K searches/month):
- 3× m6g.large instances: $360/month
- 1TB GP3 storage: $100/month
- Data transfer: $50-100/month
- **Total**: $510-560/month

---

### Azure AI Search Pricing (2025)

**Pricing Tiers**:

| Tier | Monthly Cost | Search Units | Storage | QPS | Features |
|------|--------------|--------------|---------|-----|----------|
| **Free** | $0 | 1 | 50 MB | Low | 3 indexes, limited docs |
| **Basic** | $74 | 1 (3 replicas max) | 2 GB | ~5 QPS | Production-ready |
| **Standard S1** | $250 | 1-12 | 25 GB | ~50 QPS | Partitions, replicas |
| **Standard S2** | $1,000 | 1-12 | 100 GB | ~200 QPS | High-scale |
| **Standard S3** | $2,000+ | 1-12 | 200 GB | ~500 QPS | Largest single shard |
| **Storage Optimized L1** | $2,000+ | 1-12 | 1 TB | ~100 QPS | Large document sets |
| **Storage Optimized L2** | $4,000+ | 1-12 | 2 TB | ~100 QPS | Massive storage |

**AI Enrichment Costs** (Cognitive Skills):
- **Built-in skills**: 20 free transactions/day, then $2/1K transactions
- **Custom skills**: Azure Functions pricing (consumption or premium)
- **OCR**: $1.50/1K images
- **Entity extraction**: $2/1K documents

**Key Considerations**:
- **Search Unit = Partition + Replica**: S1 with 3 partitions + 3 replicas = 9 SUs = $2,250/month
- **Bandwidth**: Included (no data transfer charges within Azure)
- **Semantic search**: Pay-per-query (additional cost on top of tier)

**Cost Examples**:
- Small SaaS: Basic tier = $74/month
- Medium e-commerce: S1 (3 SUs) = $750/month
- Large content site: S2 (6 SUs) = $6,000/month
- Enterprise knowledge base: L1 (storage-optimized) = $2,000-4,000/month

**Hidden Costs**:
- AI enrichment can add $100-1,000+/month
- Semantic search: Pay per query (can add 20-50% to base cost)
- Private endpoints: $7-10/month each

---

### Coveo Pricing (2025)

**Pricing Model**: Enterprise contracts (annual commitments)

**Estimated Tiers** (based on public reports, not official):

| Tier | Annual Cost | Monthly Equiv | Queries/Month | Users | Features |
|------|-------------|---------------|---------------|-------|----------|
| **SMB** | $50K-100K | $4K-8K | 500K-2M | 100-500 | Core search, basic ML |
| **Mid-Market** | $100K-250K | $8K-21K | 2M-10M | 500-2K | Advanced ML, connectors |
| **Enterprise** | $250K-500K+ | $21K-42K+ | 10M-50M+ | 2K-10K+ | Full platform, unlimited features |

**Pricing Factors**:
- **Query volume**: Primary cost driver (higher volume = higher cost)
- **Data sources**: Number of connectors (Salesforce, ServiceNow, SharePoint, etc.)
- **User count**: Named users or concurrent users
- **ML features**: Automatic Relevance Tuning, recommendations, personalization
- **Support level**: Standard, Premium, or Enterprise support

**Key Characteristics**:
- **No public pricing**: All quotes are custom (requires sales engagement)
- **High minimum**: $50K/year minimum (no SMB/startup option)
- **Annual contracts**: Typically 1-3 year commitments
- **All-inclusive**: Most features included (no nickel-and-diming)

**Cost Example** (estimated from reports):
- Mid-market company (5M queries/month, 1K users, 10 connectors): $150K-200K/year
- Enterprise (20M queries/month, 5K users, 50 connectors): $400K-600K/year

**ROI Justification** (from vendor claims):
- 20-40% CTR improvement (ML relevance)
- 30-50% reduction in support tickets (better self-service)
- 15-25% increase in e-commerce conversion (merchandising)
- Break-even at $500K+ annual revenue impact

---

## TCO Scenario Analysis (3-Year Projections)

### Scenario 1: Small SaaS (10K docs, 50K searches/month)

**Requirements**:
- 10,000 documents (product data, help docs)
- 50,000 searches/month (~2K searches/day)
- Basic faceting, typo tolerance
- North America traffic
- Small team (1-2 developers)

**Cost Comparison**:

| Platform | Year 1 | Year 2 | Year 3 | 3-Year TCO | Notes |
|----------|--------|--------|--------|------------|-------|
| **Algolia Build (Free)** | $0 | $0 | $0 | **$0** | Within free tier (10K searches) |
| **Meilisearch Build** | $360 | $360 | $360 | **$1,080** | $30/month (50K searches included) |
| **Typesense Hobby** | $240 | $240 | $240 | **$720** | $20/month (fixed) |
| **Self-hosted (Meilisearch)** | $600 | $600 | $600 | **$1,800** | $50/month VPS + $0 license |
| **Azure AI Search Basic** | $888 | $888 | $888 | **$2,664** | $74/month |
| **Elasticsearch Basic** | $1,140 | $1,140 | $1,140 | **$3,420** | $95/month |
| **AWS OpenSearch** | $1,200 | $1,200 | $1,200 | **$3,600** | t3.small instance |
| **Coveo** | N/A | N/A | N/A | **N/A** | Below minimum ($50K/year) |

**Winner**: Algolia (free tier) or Typesense ($720 over 3 years)

**Recommendation**: Start with Algolia free tier. If outgrow free tier, migrate to Meilisearch or Typesense.

**Engineering Time**:
- Algolia: 4-8 hours (setup + integration)
- Meilisearch: 8-12 hours (Docker + integration)
- Typesense: 8-12 hours (Docker + InstantSearch adapter)

**Total TCO (including engineering time @ $100/hour)**:
- Algolia: $400-800 (engineering) + $0 (license) = **$400-800**
- Meilisearch: $800-1,200 (engineering) + $1,080 (license) = **$1,880-2,280**
- Typesense: $800-1,200 (engineering) + $720 (license) = **$1,520-1,920**

---

### Scenario 2: Mid SaaS (100K docs, 500K searches/month)

**Requirements**:
- 100,000 documents (product catalog, knowledge base)
- 500,000 searches/month (~16K searches/day)
- Faceting, filtering, typo tolerance, autocomplete
- Multi-region (US + EU)
- Team: 3-5 developers

**Cost Comparison**:

| Platform | Year 1 | Year 2 | Year 3 | 3-Year TCO | Notes |
|----------|--------|--------|--------|------------|-------|
| **Typesense Growth** | $1,440 | $1,440 | $1,440 | **$4,320** | $120/month (8GB RAM, 4 vCPU) |
| **Meilisearch Pro** | $3,600 | $3,600 | $3,600 | **$10,800** | $300/month (1M searches) |
| **Algolia Grow** | $2,940 | $2,940 | $2,940 | **$8,820** | $245/month (490K overages @ $0.50/1K) |
| **Self-hosted Meilisearch** | $2,400 | $2,400 | $2,400 | **$7,200** | $200/month (2× VMs, multi-region) |
| **AWS OpenSearch** | $6,000 | $6,000 | $6,000 | **$18,000** | $500/month (2× m6g.large + storage) |
| **Elasticsearch Cloud** | $9,600 | $9,600 | $9,600 | **$28,800** | $800/month (Standard tier) |
| **Azure AI Search S1** | $3,000 | $3,000 | $3,000 | **$9,000** | $250/month (1 SU) |
| **Coveo** | $150,000 | $150,000 | $150,000 | **$450,000** | $50K-100K/year minimum |

**Winner**: Typesense ($4,320 over 3 years) or Meilisearch self-hosted ($7,200)

**Cost Savings**:
- Typesense vs Algolia: $4,500 saved (51% cheaper)
- Typesense vs AWS OpenSearch: $13,680 saved (76% cheaper)
- Typesense vs Coveo: $445,680 saved (99% cheaper)

**Engineering Time**:
- Typesense: 16-24 hours (multi-region setup, InstantSearch)
- Meilisearch: 20-30 hours (Docker, multi-region, custom UI)
- Algolia: 12-16 hours (multi-region config, InstantSearch)
- Elasticsearch: 40-80 hours (cluster setup, tuning, monitoring)

**Total TCO (including engineering @ $100/hour)**:
- Typesense: $1,600-2,400 + $4,320 = **$5,920-6,720**
- Meilisearch: $2,000-3,000 + $10,800 = **$12,800-13,800**
- Algolia: $1,200-1,600 + $8,820 = **$10,020-10,420**
- Elasticsearch: $4,000-8,000 + $28,800 = **$32,800-36,800**

**Recommendation**: Typesense for lowest TCO, Algolia if need global CDN + premium support.

---

### Scenario 3: E-Commerce (500K products, 2M searches/month)

**Requirements**:
- 500,000 products (SKUs, variants, inventory)
- 2,000,000 searches/month (~67K searches/day)
- Faceting (price, category, brand, rating, etc.)
- Merchandising (pinning, boosting, campaigns)
- Global traffic (US, EU, APAC)
- Team: 5-10 developers, 1-2 merchandisers

**Cost Comparison**:

| Platform | Year 1 | Year 2 | Year 3 | 3-Year TCO | Notes |
|----------|--------|--------|--------|------------|-------|
| **Typesense Business** | $3,600 | $3,600 | $3,600 | **$10,800** | $300/month (16GB RAM, 8 vCPU) |
| **Meilisearch Custom** | $7,200 | $7,200 | $7,200 | **$21,600** | $600/month (usage-based overages) |
| **Algolia Grow** | $11,880 | $11,880 | $11,880 | **$35,640** | $990/month (1.99M @ $0.50/1K) |
| **Algolia Grow Plus** | $41,760 | $41,760 | $41,760 | **$125,280** | $3,480/month (1.99M @ $1.75/1K) |
| **AWS OpenSearch** | $12,000 | $12,000 | $12,000 | **$36,000** | $1,000/month (3× m6g.xlarge + 2TB) |
| **Azure AI Search S2** | $12,000 | $12,000 | $12,000 | **$36,000** | $1,000/month (1 SU) |
| **Elasticsearch Gold** | $18,000 | $18,000 | $18,000 | **$54,000** | $1,500/month (production cluster) |
| **Coveo** | $180,000 | $180,000 | $180,000 | **$540,000** | $150K/year (mid-market e-commerce) |

**Winner (License Cost Only)**: Typesense ($10,800)

**Winner (Features + Cost)**: Algolia Grow ($35,640) - best merchandising, analytics

**Cost Savings**:
- Typesense vs Algolia Grow: $24,840 saved (70% cheaper)
- Algolia Grow vs Coveo: $504,360 saved (93% cheaper)

**Engineering Time**:
- Typesense: 40-60 hours (multi-region, custom merchandising UI)
- Algolia: 30-40 hours (InstantSearch, merchandising dashboard)
- Elasticsearch: 80-120 hours (cluster, custom merchandising, analytics)

**Merchandising Development** (if DIY):
- Typesense/Meilisearch: 80-160 hours (build custom admin UI for pinning, boosting)
- Algolia: 0-20 hours (visual merchandising included)
- Cost: $8,000-16,000 (developer time)

**Total TCO (including engineering + merchandising)**:
- Typesense: $4,000-6,000 + $8,000-16,000 + $10,800 = **$22,800-32,800**
- Algolia Grow: $3,000-4,000 + $0-2,000 + $35,640 = **$38,640-41,640**
- Elasticsearch: $8,000-12,000 + $10,000-20,000 + $54,000 = **$72,000-86,000**

**Recommendation**:
- **Budget-first**: Typesense + custom merchandising ($22K-33K TCO)
- **Feature-first**: Algolia Grow ($38K-42K TCO, saves 80-160 hours on merchandising)
- **Best ROI**: Algolia if merchandising saves >40 hours/year (break-even)

---

### Scenario 4: Content/Media Site (1M docs, 5M searches/month)

**Requirements**:
- 1,000,000 documents (articles, videos, podcasts)
- 5,000,000 searches/month (~166K searches/day)
- Full-text search, faceting, date filtering
- Image/video metadata search
- Global audience
- Team: 10-15 developers

**Cost Comparison**:

| Platform | Year 1 | Year 2 | Year 3 | 3-Year TCO | Notes |
|----------|--------|--------|--------|------------|-------|
| **Typesense Business+** | $7,200 | $7,200 | $7,200 | **$21,600** | $600/month (32GB RAM) |
| **Meilisearch Custom** | $12,000 | $12,000 | $12,000 | **$36,000** | $1,000/month (usage overages) |
| **Algolia Grow** | $29,880 | $29,880 | $29,880 | **$89,640** | $2,490/month (4.99M @ $0.50/1K) |
| **Algolia Premium** | $48,000 | $48,000 | $48,000 | **$144,000** | $4,000/month (annual contract, estimated) |
| **AWS OpenSearch** | $24,000 | $24,000 | $24,000 | **$72,000** | $2,000/month (6× m6g.xlarge) |
| **Elasticsearch Cloud** | $30,000 | $30,000 | $30,000 | **$90,000** | $2,500/month (Gold tier) |
| **Azure AI Search S2** | $18,000 | $18,000 | $18,000 | **$54,000** | $1,500/month (scaled SUs) |
| **Coveo** | $240,000 | $240,000 | $240,000 | **$720,000** | $200K/year (content platform) |

**Winner**: Typesense ($21,600) - 76% cheaper than Algolia, 97% cheaper than Coveo

**Cost Savings**:
- Typesense vs Algolia Grow: $68,040 saved (76% cheaper)
- Typesense vs AWS OpenSearch: $50,400 saved (70% cheaper)
- Meilisearch vs Algolia: $53,640 saved (60% cheaper)

**Engineering Time**:
- Typesense: 60-80 hours (large dataset, multi-region, optimization)
- Algolia: 40-60 hours (multi-region, analytics integration)
- Elasticsearch: 120-200 hours (large cluster, tuning, monitoring)

**Total TCO (including engineering @ $100/hour)**:
- Typesense: $6,000-8,000 + $21,600 = **$27,600-29,600**
- Meilisearch: $8,000-10,000 + $36,000 = **$44,000-46,000**
- Algolia Grow: $4,000-6,000 + $89,640 = **$93,640-95,640**
- Elasticsearch: $12,000-20,000 + $90,000 = **$102,000-110,000**

**Recommendation**: Typesense or Meilisearch (70-80% cost savings vs Algolia/Elasticsearch)

---

### Scenario 5: Enterprise Knowledge Base (5M docs, 1M searches/month)

**Requirements**:
- 5,000,000 documents (internal docs, SharePoint, Salesforce, Confluence)
- 1,000,000 searches/month (~33K searches/day)
- Document-level security (ACLs)
- 100+ data source connectors
- SSO/SAML authentication
- Team: 20+ IT staff, 5K+ employees

**Cost Comparison**:

| Platform | Year 1 | Year 2 | Year 3 | 3-Year TCO | Notes |
|----------|--------|--------|--------|------------|-------|
| **Typesense Enterprise** | $10,800 | $10,800 | $10,800 | **$32,400** | $900/month (large cluster) + custom connector dev |
| **Meilisearch Enterprise** | $18,000 | $18,000 | $18,000 | **$54,000** | $1,500/month (custom support) + connector dev |
| **AWS OpenSearch** | $36,000 | $36,000 | $36,000 | **$108,000** | $3,000/month (large cluster + support) |
| **Elasticsearch Platinum** | $48,000 | $48,000 | $48,000 | **$144,000** | $4,000/month (enterprise features + support) |
| **Azure AI Search L1** | $36,000 | $36,000 | $36,000 | **$108,000** | $3,000/month (storage-optimized + AI) |
| **Algolia Premium** | $72,000 | $72,000 | $72,000 | **$216,000** | $6,000/month (large-scale contract) |
| **Coveo** | $300,000 | $300,000 | $300,000 | **$900,000** | $100K-200K/year (100+ connectors, ML, security) |

**Connector Development Cost** (if DIY):
- Typesense/Meilisearch: $50K-150K (build 10-20 custom connectors)
- AWS OpenSearch: $30K-80K (build custom connectors, leverage AWS services)
- Algolia: $40K-100K (build connectors, custom ACL logic)
- Coveo: $0-20K (100+ connectors included, minimal custom work)

**Total TCO (including connectors)**:
- Typesense: $32,400 + $100,000 (connectors) = **$132,400**
- AWS OpenSearch: $108,000 + $50,000 (connectors) = **$158,000**
- Azure AI Search: $108,000 + $60,000 (connectors) = **$168,000**
- Elasticsearch: $144,000 + $50,000 (connectors) = **$194,000**
- Algolia: $216,000 + $70,000 (connectors) = **$286,000**
- Coveo: $900,000 + $10,000 (custom) = **$910,000**

**Winner (TCO)**: Typesense + custom connectors ($132K)

**Winner (Features + Speed to Market)**: Coveo ($910K) - 100+ connectors included, zero connector dev time

**ROI Break-Even Analysis**:
- Coveo premium: $910K - $158K (OpenSearch) = $752K premium
- Break-even if saves >7,520 hours (@ $100/hour) over 3 years
- Coveo value: 100+ connectors (save 2,000-5,000 hours), ML relevance (20-40% CTR), analytics
- **Verdict**: Coveo justified for large enterprises if connector dev would exceed 2,000 hours

**Recommendation**:
- **AWS-native**: AWS OpenSearch ($158K TCO, good AWS integration)
- **Azure-native**: Azure AI Search ($168K TCO, cognitive skills)
- **Budget-conscious**: Typesense/Meilisearch ($132-194K TCO, requires custom dev)
- **Best-in-class**: Coveo ($910K TCO, only if budget >$200K/year and need 100+ connectors)

---

### Scenario 6: Large-Scale Marketplace (10M docs, 20M searches/month)

**Requirements**:
- 10,000,000 listings (products, services, inventory)
- 20,000,000 searches/month (~666K searches/day)
- Real-time inventory updates
- Advanced merchandising
- Global distribution (multi-region)
- Team: 50+ engineers, 5-10 data scientists

**Cost Comparison**:

| Platform | Year 1 | Year 2 | Year 3 | 3-Year TCO | Notes |
|----------|--------|--------|--------|------------|-------|
| **Typesense Enterprise** | $21,600 | $21,600 | $21,600 | **$64,800** | $1,800/month (multi-region cluster) |
| **Meilisearch Enterprise** | $36,000 | $36,000 | $36,000 | **$108,000** | $3,000/month (custom support, multi-region) |
| **AWS OpenSearch** | $72,000 | $72,000 | $72,000 | **$216,000** | $6,000/month (large multi-region cluster) |
| **Elasticsearch Platinum** | $96,000 | $96,000 | $96,000 | **$288,000** | $8,000/month (enterprise cluster) |
| **Azure AI Search S3** | $84,000 | $84,000 | $84,000 | **$252,000** | $7,000/month (scaled SUs) |
| **Algolia Premium** | $144,000 | $144,000 | $144,000 | **$432,000** | $12,000/month (large enterprise contract) |
| **Algolia Elevate** | $300,000 | $300,000 | $300,000 | **$900,000** | $25,000/month (full AI suite) |
| **Coveo** | $480,000 | $480,000 | $480,000 | **$1,440,000** | $400K/year (large marketplace, ML) |

**Winner (License Only)**: Typesense ($64,800) - 85% cheaper than Algolia Premium

**Engineering & ML Development** (3-year):
- Typesense/Meilisearch: $200K-400K (custom relevance tuning, merchandising, analytics)
- Algolia Premium: $50K-100K (some custom dev, leverages built-in features)
- Algolia Elevate: $20K-50K (minimal custom dev, full AI suite)
- Elasticsearch: $300K-500K (extensive custom dev, ML, monitoring)
- Coveo: $30K-80K (minimal custom dev, ML included)

**Total TCO (including engineering)**:
- Typesense: $64,800 + $300,000 = **$364,800**
- Meilisearch: $108,000 + $250,000 = **$358,000**
- AWS OpenSearch: $216,000 + $350,000 = **$566,000**
- Elasticsearch: $288,000 + $400,000 = **$688,000**
- Algolia Premium: $432,000 + $75,000 = **$507,000**
- Algolia Elevate: $900,000 + $35,000 = **$935,000**
- Coveo: $1,440,000 + $50,000 = **$1,490,000**

**Winner (Total TCO)**: Meilisearch ($358K) or Typesense ($364K)

**Revenue Impact Consideration**:
- Algolia/Coveo claim 15-40% conversion improvement (ML relevance, merchandising)
- Marketplace revenue: $100M/year (example)
- 5% conversion improvement = $5M/year additional revenue
- Algolia Elevate premium over Meilisearch: $577K over 3 years
- **ROI**: If conversion improves >0.6%, Algolia Elevate pays for itself

**Recommendation**:
- **Cost-optimized**: Meilisearch or Typesense ($358-364K TCO, requires strong ML team)
- **Feature-optimized**: Algolia Elevate ($935K TCO, best-in-class ML/AI, saves 300+ engineering hours)
- **AWS-native**: AWS OpenSearch ($566K TCO, good AWS integration)
- **Best ML out-of-box**: Coveo ($1.49M TCO, only if budget >$400K/year)

---

## Cost Optimization Strategies

### 1. Tier Optimization
**Strategy**: Right-size tier based on actual usage (don't over-provision)

**Examples**:
- Algolia: Start with Grow, upgrade to Premium only when need advanced features
- AWS OpenSearch: Use t3.medium for dev, m6g.large for production (not r6g.xlarge)
- Azure AI Search: Start with Basic, scale to S1 only when exceed QPS limits

**Potential Savings**: 30-60% (avoiding over-provisioning)

---

### 2. Reserved Instance / Annual Commitments
**Strategy**: Commit to 1-3 year contracts for discounts

**Platforms**:
- AWS OpenSearch: 30-75% discount (reserved instances)
- Algolia: 24-34% discount (annual contracts)
- Elasticsearch: 20-40% discount (annual Elastic Cloud)

**Potential Savings**: 20-75% depending on commitment length

---

### 3. Self-Hosting (Open-Source)
**Strategy**: Self-host Meilisearch, Typesense, or Elasticsearch to avoid SaaS markup

**Cost Comparison** (500K searches/month):
- Meilisearch Cloud: $300/month
- Self-hosted Meilisearch: $100-200/month (cloud VMs)
- **Savings**: $100-200/month ($1,200-2,400/year)

**Trade-offs**:
- Add DevOps time (10-20 hours/month for monitoring, updates)
- Add infrastructure complexity (backups, security, updates)
- Break-even: Only worth it if have existing DevOps team

---

### 4. Hybrid Architecture
**Strategy**: Use different platforms for different use cases

**Examples**:
- Typesense for instant search (fast, cheap) + Elasticsearch for analytics (powerful aggregations)
- Meilisearch for product search + Coveo for enterprise knowledge base
- Algolia for customer-facing search + OpenSearch for internal tools

**Potential Savings**: 40-70% (use expensive platform only where needed)

---

### 5. Caching Layer
**Strategy**: Add caching (CDN, Redis) to reduce search API calls

**Cost Savings**:
- Algolia: Cache common searches, reduce billable API calls by 30-50%
- AWS OpenSearch: Cache aggregations, reduce compute costs
- Implementation: Cloudflare Workers, Redis, or application-level cache

**Potential Savings**: 30-50% on usage-based platforms (Algolia)

---

### 6. Overage Negotiation
**Strategy**: Negotiate lower overage rates with vendors

**Examples**:
- Algolia: Standard $0.50/1K → negotiate to $0.25-0.35/1K (30-50% reduction)
- Elasticsearch: Negotiate lower data transfer rates
- Coveo: Negotiate higher query caps before overages

**Potential Savings**: 30-50% on overage costs

---

### 7. Feature Rationalization
**Strategy**: Only pay for features you actually use

**Examples**:
- Don't need AI/ML? Use Meilisearch/Typesense instead of Algolia Elevate (save $900K/year)
- Don't need 100+ connectors? Use OpenSearch instead of Coveo (save $800K/year)
- Don't need real-time analytics? Use free Algolia tier instead of paid (save $2K-10K/year)

**Potential Savings**: 50-90% (avoid feature bloat)

---

## Hidden Costs to Watch

### 1. Data Transfer / Bandwidth
**Platforms Affected**: All (especially cloud platforms)

**Typical Costs**:
- AWS: $0.09-0.20/GB outbound
- Azure: $0.05-0.15/GB outbound (after free tier)
- Algolia: Usually included, but can be charged at high scale

**Mitigation**: Use CDN caching, compress responses, region-local queries

---

### 2. AI Enrichment / Skillsets
**Platforms Affected**: Azure AI Search, Coveo

**Typical Costs**:
- Azure OCR: $1.50/1K images
- Azure entity extraction: $2/1K documents
- Coveo ML features: Included but drive up base cost

**Mitigation**: Only enrich documents that need it (not all documents)

---

### 3. Support Contracts
**Platforms Affected**: All (especially Elasticsearch, AWS, Azure)

**Typical Costs**:
- Elasticsearch: 10-20% of license cost
- AWS Support: 3-10% of monthly bill (Business/Enterprise)
- Coveo: Included in enterprise contracts

**Mitigation**: Use community support for non-critical, pay for support only in production

---

### 4. Engineering Time / Opportunity Cost
**Platforms Affected**: All (especially DIY options)

**Typical Costs**:
- Elasticsearch: 200-500 hours/year (cluster management, tuning)
- Self-hosted Meilisearch: 100-200 hours/year (maintenance)
- Algolia: 20-50 hours/year (minimal maintenance)

**Calculation**:
- 300 hours/year @ $100/hour = $30,000/year hidden cost
- Elasticsearch "free" license + $30K engineering = $30K true cost
- Algolia $20K/year + $5K engineering = $25K true cost

**Mitigation**: Factor engineering time into TCO (use calculator below)

---

### 5. Migration / Lock-In Exit Costs
**Platforms Affected**: All (especially proprietary platforms)

**Estimated Migration Costs**:
- Algolia → Meilisearch: 40-80 hours (InstantSearch compatible)
- Elasticsearch → OpenSearch: 20-40 hours (API compatible)
- Coveo → Algolia: 200-400 hours (rebuild connectors, ML)
- Azure AI Search → Elasticsearch: 100-200 hours (rebuild enrichment pipeline)

**Mitigation**: Use open standards (REST API), avoid vendor-specific features, maintain export scripts

---

## TCO Calculator Framework

**Formula**:
```
Total Cost of Ownership (3-year) =
  License Costs (platform subscription)
  + Infrastructure Costs (servers, storage, bandwidth)
  + Engineering Time (setup, maintenance, tuning) @ hourly rate
  + Feature Development (custom merchandising, connectors, analytics)
  + Support Contracts (if applicable)
  + Migration Costs (if switching platforms)
  - Cost Savings (caching, optimization, negotiation)
```

**Example** (Mid SaaS, 500K searches/month):

**Option A: Typesense**
- License: $120/month × 36 = $4,320
- Infrastructure: $0 (managed cloud)
- Engineering (setup): 24 hours @ $100 = $2,400
- Engineering (maintenance): 5 hours/month × 36 × $100 = $18,000
- Feature dev (merchandising): 80 hours @ $100 = $8,000
- **Total TCO**: $32,720

**Option B: Algolia Grow**
- License: $245/month × 36 = $8,820
- Infrastructure: $0 (managed cloud)
- Engineering (setup): 16 hours @ $100 = $1,600
- Engineering (maintenance): 2 hours/month × 36 × $100 = $7,200
- Feature dev: 0 (built-in merchandising)
- **Total TCO**: $17,620

**Winner**: Algolia (lower total TCO despite higher license cost, due to lower engineering time)

**Key Insight**: Always include engineering time in TCO calculations. Cheaper platforms often have higher hidden costs (maintenance, feature development).

---

## Summary: Cost/Value Positioning

| Platform | Cost Tier | Best Value Scenario | Worst Value Scenario |
|----------|-----------|---------------------|----------------------|
| **Algolia** | Premium | Global e-commerce, instant search critical, strong budget | Small sites, unpredictable traffic, tight budget |
| **Meilisearch** | Budget | Startups, cost-conscious, instant search, flexible deployment | Need advanced ML, 100+ connectors, enterprise support |
| **Typesense** | Budget | Predictable pricing, instant search, linear scaling | Need built-in analytics, merchandising UI, complex ML |
| **Elasticsearch** | Mid-High | Observability, large-scale analytics, custom needs, strong team | Small team, need instant search, limited DevOps |
| **AWS OpenSearch** | Mid-High | AWS-heavy workload, RAG, Bedrock integration | Non-AWS infrastructure, small scale (<1M docs) |
| **Azure AI Search** | Mid-High | Azure ecosystem, document processing, cognitive skills | Non-Azure infrastructure, need fast latency (<50ms) |
| **Coveo** | Enterprise | Large enterprise, 100+ data sources, best ML, budget >$200K/year | SMB, budget <$50K/year, simple use cases |

---

**Last Updated**: November 14, 2025
**Methodology**: Vendor pricing pages, user reports, web research, TCO modeling
**Disclaimer**: Prices are estimates and subject to change. Always verify with vendors for current pricing.
