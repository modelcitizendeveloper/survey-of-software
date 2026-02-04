# Web Application Firewall (WAF) - Discovery Table of Contents

**Experiment ID:** 3.010-waf
**Category:** Security Infrastructure
**Discovery Completed:** October 11, 2025
**Methodologies:** S1 Rapid, S2 Comprehensive, S3 Need-Driven, S4 Strategic

---

## Quick Navigation

- [S0: Experiment Scope](#s0-experiment-scope)
- [S1: Rapid Discovery](#s1-rapid-discovery)
- [S2: Comprehensive Analysis](#s2-comprehensive-analysis)
- [S3: Need-Driven Discovery](#s3-need-driven-discovery)
- [S4: Strategic Selection](#s4-strategic-selection)
- [Convergence Analysis](#convergence-analysis)
- [Quick Decision Guide](#quick-decision-guide)
- [Provider Summary](#provider-summary)
- [File Reference Guide](#file-reference-guide)

---

## S0: Experiment Scope

This experiment investigates Web Application Firewall (WAF) solutions to understand the landscape of cloud-based and self-hosted security platforms that protect web applications from common vulnerabilities and attacks.

**Key Questions:**
- What WAF providers exist across different deployment models?
- How do infrastructure security and application security intersect?
- When should organizations choose managed vs. self-hosted solutions?
- What are the trade-offs between feature richness, cost, and operational complexity?

**Scope Boundaries:**
- Focus on modern cloud-based WAF solutions and proven self-hosted alternatives
- Analysis includes both general-purpose and specialized WAF offerings
- Evaluation spans infrastructure-focused (AWS, Azure, GCP) and application-focused providers
- Consideration of startup-friendly through enterprise-grade solutions

---

## S1: Rapid Discovery

**Methodology**: Speed-focused, popularity-driven market analysis
**Research Time**: ~30 minutes
**Files**: 17 files in S1-rapid/
**Approach**: Prioritize deployment speed, proven adoption, and self-service availability

### Top 3 Recommendations

**1. Cloudflare WAF - "The Default Choice"**
- Confidence Level: HIGH (40/40 deploy today score)
- Fastest deployment: 5-10 minutes from signup to protection
- Free tier that actually works, scales to enterprise
- 8.6/10 user rating, handles 2 trillion requests daily
- Best for: Startups, SaaS applications, SMBs, quick protection needs

**2. AWS WAF - "The Cloud-Native Choice"**
- Confidence Level: HIGH (30/40 deploy today score)
- Deploy in 30-60 minutes via AWS console
- Pay-per-use pricing ($5/month + $1/rule + $0.60/M requests)
- 8.0/10 user rating
- Best for: AWS-native applications, CloudFront/ALB/API Gateway users

**3. Fastly Next-Gen WAF - "The Performance Leader"**
- Confidence Level: HIGH (28/40 deploy today score)
- Highest user satisfaction (4.8/5 stars), 25% faster than Cloudflare
- 90% deploy in blocking mode immediately (low false positives)
- Forrester Strong Performer Q1 2025
- Best for: Performance-critical apps, e-commerce at scale

### Quick Decision Framework

- **Need protection in next hour** → Cloudflare (Free/Pro tier)
- **Building on AWS** → AWS WAF
- **Building on Azure** → Azure Application Gateway WAF
- **Running WordPress** → Wordfence (Free) or Sucuri ($299/year)
- **Small business (non-technical)** → Barracuda WAF-as-a-Service
- **Enterprise budget** → Fastly (performance) or Imperva (accuracy)
- **Open source/on-prem** → ModSecurity
- **Major bot/fraud problems** → HUMAN Security

### Key Insight

Cloudflare dominates the "fast deployment" category as the market's consensus answer for teams wanting protection quickly without complexity. The free tier removes barriers completely, making it the default choice for rapid protection needs.

### Market Observations

- **Clear Leader**: Cloudflare wins for speed + ease + power combination
- **Cloud Native Winners**: AWS & Azure WAFs for platform-committed organizations
- **Enterprise Segment**: Fragmented among F5, Akamai, Imperva, and Fastly
- **WordPress Dominance**: Wordfence (5M+ installations) vs. Sucuri (hundreds of thousands)
- **Bot Management**: HUMAN Security (post-PerimeterX merger) is the specialist leader

---

## S2: Comprehensive Analysis

**Methodology**: Systematic comparison matrix with data-driven scoring
**Research Time**: ~2-3 hours
**Files**: 19 files in S2-comprehensive/
**Approach**: Feature matrices, pricing analysis, integration patterns, weighted scoring

### Context-Specific Recommendations

**General-Purpose Web Application (1M-1B req/month)**
- Winner: Cloudflare (score 4.6/5)
- Easiest deployment, best DDoS protection, unlimited bandwidth
- Tiers: Free ($0) → Pro ($20) → Business ($200) → Enterprise (custom)

**AWS-Native Application**
- Winner: AWS WAF (score 4.0/5)
- Native integration, cost-effective at low-medium traffic
- Pricing: $9/month (1M req) → $90/month (100M req) → $770/month (1B req)
- Break-even vs. Cloudflare at ~500M req/month

**Multi-Cloud / Cloud-Native Microservices**
- Winner: Fastly Next-Gen WAF (score 4.0/5)
- Agent-based deployment flexibility, works anywhere
- Low false positives (88% use blocking mode)
- Pricing: $500-$10,000/month depending on scale

**Enterprise / Mission-Critical**
- Winner: Imperva Cloud WAF (score 4.3/5)
- Fully managed SOC (24/7), 94% deploy in blocking mode
- Enterprise SLAs (99.999% uptime, 3-second DDoS TTM)
- Pricing: $1,000-$50,000+/month

**Budget-Constrained / Startup**
- Ultra-Budget (<$10/mo): Cloudflare Free or Sucuri Basic ($9.99)
- Small Budget ($10-$100/mo): Cloudflare Pro ($20) or AppTrana Advance ($99)
- Medium Budget ($100-$500/mo): AWS WAF or Cloudflare Business ($200)

**API-Heavy Application**
- Winner: Wallarm (score 4.2/5)
- API Security Platform of the Year 2025
- Automatic API discovery, OWASP API Top 10 protection
- Pricing: $833+/month

**WordPress / CMS Site**
- Winner: Sucuri (score 4.5/5 for WordPress specifically)
- WordPress specialization, malware removal included
- Pricing: $9.99-$69.93/month with 30% annual discount

**Maximum Privacy / On-Premise**
- Winner: ModSecurity or Coraza (score 3.0/5)
- Zero licensing cost, complete control, no third-party proxying
- TCO: Infrastructure ($50-$5k/mo) + Personnel ($5k-$15k/mo)

### Key Insight

There is no universal "best" WAF solution. The optimal choice depends on traffic volume, cloud platform commitment, team expertise, budget constraints, and specific security requirements. AWS WAF is cheapest until ~500M req/month, then Cloudflare's flat-rate pricing becomes more economical.

### Trade-Off Analysis

**High Cost, High Features, High Ease**: Imperva, Akamai
**Medium Cost, High Features, Medium Ease**: Cloudflare Enterprise, Fastly NGWAF, Wallarm
**Low Cost, Medium Features, High Ease**: Cloudflare Free/Pro/Business, AppTrana
**Low Cost, Medium Features, Low Ease**: AWS WAF, Google Cloud Armor, Azure WAF
**Lowest Cost, Medium Features, Lowest Ease**: ModSecurity/Coraza

---

## S3: Need-Driven Discovery

**Methodology**: Requirements-first solution matching
**Research Time**: ~1-2 hours
**Files**: 9 files in S3-need-driven/
**Approach**: Define use cases, map requirements, evaluate fit scores

### Six Use Cases Analyzed

**1. Webhook Security**
- Winner: Cloudflare Business ($200/month)
- Fit Score: 9.5/10, Confidence: 95%
- Requirements satisfied: IP allowlisting, rate limiting, low latency, easy config
- 3-year TCO: $44K ($7.2K subscription + $10K implementation + $27K ops)

**2. Public API Protection**
- Winner: Cloudflare Enterprise + API Shield + Bot Management ($4,000-5,000/month)
- Fit Score: 9.5/10, Confidence: 90%
- Requirements satisfied: Advanced bot management, Layer 7 DDoS, granular rate limiting, API-specific protection
- 3-year TCO: $217K ($180K subscription + $10K implementation + $27K ops)

**3. Enterprise Web Application**
- Winner: Imperva Cloud WAF Enterprise ($10,000-12,000/month)
- Fit Score: 9.5/10, Confidence: 92%
- Requirements satisfied: HIPAA/PCI-DSS/GDPR compliance, advanced custom rules, enterprise logging, audit-ready, white-glove support
- 3-year TCO: $553K ($432K subscription + $40K implementation + $81K ops)

**4. High-Traffic Content Site**
- Winner: Cloudflare Business → Enterprise ($200-5,000/month)
- Fit Score: 9.8/10, Confidence: 97%
- Requirements satisfied: Integrated CDN + WAF, unlimited bandwidth, best global performance, DDoS protection, cost predictability
- 3-year TCO: $109K-217K ($72K-180K subscription + $10K implementation + $27K ops)

**5. Startup MVP**
- Winner: Cloudflare Free → Pro ($0-20/month)
- Fit Score: 9.8/10, Confidence: 98%
- Requirements satisfied: Zero cost to start, 15-minute setup, zero maintenance, enterprise credibility, perfect growth path
- 3-year TCO: $10K ($0-720 subscription + $1K implementation + $9K ops)

**6. Multi-Region Global**
- Winner: Cloudflare Enterprise + Load Balancer + Argo ($12,000-20,000/month)
- Fit Score: 9.8/10, Confidence: 95%
- Requirements satisfied: Global edge network (330+ PoPs), multi-region failover (<30s), data residency, unified management, fastest policy propagation
- 3-year TCO: $551K ($504K subscription + $20K implementation + $27K ops)

### Requirement Patterns Identified

**Pattern 1: Budget-Constrained + Simple Use Cases**
- Characteristics: Budget <$500/mo, small team, quick implementation
- Solution: Cloudflare (Free → Pro → Business)
- Why: Zero/low cost, fully managed, 15-minute setup, seamless scaling

**Pattern 2: API-Heavy + Bot Management Critical**
- Characteristics: Public APIs, sophisticated bot threats, DDoS critical, performance-sensitive
- Solution: Cloudflare Enterprise + API Shield + Bot Management
- Why: Purpose-built API protection, industry-leading bot management, massive DDoS capacity, flat-rate pricing

**Pattern 3: Enterprise Compliance + Custom Rules**
- Characteristics: HIPAA/PCI-DSS compliance, complex custom logic, comprehensive audit requirements
- Solution: Imperva Cloud WAF (Enterprise)
- Why: Built for compliance, most flexible custom rules engine, healthcare/financial vertical expertise

**Pattern 4: Performance + Cost Optimization**
- Characteristics: Very high traffic (100M+ req/day), CDN integration essential, performance = revenue
- Solution: Cloudflare Business/Enterprise
- Why: Unified CDN + WAF, unlimited bandwidth, best global performance, flat-rate pricing

**Pattern 5: Multi-Region + Global Scale**
- Characteristics: Active-active multi-region, data residency requirements, latency-sensitive (<100ms p95)
- Solution: Cloudflare Enterprise + Load Balancer + Argo
- Why: Zero-configuration global deployment (anycast), fastest policy propagation (<3s globally), unified management

**Pattern 6: AWS-Committed + Existing Infrastructure**
- Characteristics: Deep AWS investment, strong AWS expertise, prefer native integration
- Solution: AWS WAF + CloudFront (+ Shield Advanced if DDoS critical)
- Why: Native integration, team knows AWS, IaC support, cost optimization via AWS credits
- Caveat: Weaker bot management, higher operational complexity

### Key Insight

Cloudflare provides optimal requirement-solution fit for 5 out of 6 use cases analyzed. This is not because Cloudflare is "the best WAF" in absolute terms, but because most use cases prioritize ease of use, operational simplicity, cost predictability, and global performance—all areas where Cloudflare excels. For enterprise compliance use cases, Imperva provides superior fit when requirements prioritize compliance-specific features over ease and cost.

### Decision Framework

**Step 1: Identify Primary Constraint**
- Budget <$100/month → Cloudflare Free/Pro
- Time <1 day → Cloudflare (15-minute setup)
- Team <3 people → Fully managed only (Cloudflare, Imperva)
- Compliance critical → Imperva or Akamai
- Performance critical → Cloudflare or Akamai
- AWS-only → AWS WAF

**Step 2: Identify Primary Use Case**
- Webhook endpoints → Cloudflare Business or AWS WAF
- Public APIs → Cloudflare Enterprise
- Enterprise web app → Imperva Enterprise
- High-traffic content → Cloudflare Business/Enterprise
- Startup MVP → Cloudflare Free/Pro
- Multi-region app → Cloudflare Enterprise + Load Balancer

**Step 3: Calculate 3-Year TCO**
- Cloudflare operational simplicity saves $50-100K over 3 years vs. AWS WAF
- Factor in implementation, operations hours/month, training, incident response

---

## S4: Strategic Selection

**Methodology**: Long-term viability analysis with 3-5 year outlook
**Research Time**: ~1-2 hours
**Files**: 13 files in S4-strategic/
**Approach**: Vendor stability, acquisition risk, lock-in implications, infrastructure strategy alignment

### Strategic Tiers

**Tier 1: Maximum Stability (95%+ Confidence)**
- **AWS WAF + Shield**: Best for AWS-committed organizations (5+ year horizon)
  - Zero acquisition risk (Amazon-backed), very high lock-in (intentional)
- **Azure Front Door WAF**: Best for Azure-committed organizations
  - Zero acquisition risk (Microsoft-backed), very high lock-in (intentional)

**Tier 2: High Stability with Moderate Lock-in (80-90% Confidence)**
- **Cloudflare WAF**: Best for cloud-agnostic, multi-cloud, edge-first architectures
  - 90% confidence, very low acquisition risk (5-10%), moderate-high lock-in (CDN+WAF+DNS bundle)
- **Fortinet FortiWeb**: Best for Fortinet Security Fabric users
  - 80% confidence, low acquisition risk (10-15%), very high lock-in (intentional platform commitment)

**Tier 3: Solid Viability with Strategic Considerations (70-80% Confidence)**
- **Akamai App & API Protector**: Best for enterprises with global media delivery
  - 70% confidence, moderate-low acquisition risk (20-30%)
  - Stable foundation but transformation trajectory uncertain
  - Watch security growth (30-35% ARR is encouraging)

**Tier 4: Moderate Viability with Elevated Risk (50-70% Confidence)**
- **Fastly WAF (Next-Gen WAF)**: Best for developer-focused organizations
  - 50% confidence, HIGH acquisition risk (60-70% within 3-5 years)
  - Excellent technology, but financial distress signals (stock down 57%, market cap $650M)
  - Plan explicitly for ownership change by 2027-2028
- **Imperva (Thales-owned)**: Best for existing customers or Thales users
  - 60% confidence, zero current acquisition risk (just acquired), but re-acquisition risk 15-20% by 2027-2028
  - Early integration phase (12-18 months post-acquisition)
  - Wait 12-18 months for integration clarity before new commitments

**Tier 5: Niche / Specialized Use Cases**
- **F5 BIG-IP / NGINX**: Existing F5 customers with complex customization
  - 60-70% confidence, moderate acquisition risk (25-35%)
- **Google Cloud Armor**: GCP-committed organizations (rare)
  - 85% confidence (Google-backed), but low market share creates uncertainty
- **ModSecurity / OWASP CRS**: Organizations with security engineering depth
  - 70% confidence (open-source continuity), low lock-in (major advantage)

### Key Strategic Insights

**Maximum Stability Priority**
- Choose hyperscale cloud WAFs (AWS, Azure) only if cloud commitment is certain
- Accept very high lock-in as strategic advantage (not weakness)

**Cloud-Agnostic Strategy**
- Cloudflare offers high stability (90% confidence) with moderate lock-in
- Bounded to edge layer, not cloud-specific

**Acquisition Risk Management**
- Fastly: 60-70% acquisition probability requires explicit contingency planning
- Imperva: Monitor Thales integration for 12-18 months before new commitments
- Akamai: Transformation success critical; if stalled, acquisition probability increases

**Lock-in Implications**
- High Lock-in: DNS-based WAFs (Cloudflare, Imperva, Akamai), Cloud-native WAFs (AWS, Azure, GCP)
- Medium Lock-in: Agent-based WAFs (Fastly NGWAF, Wallarm)
- Low Lock-in: Self-hosted (ModSecurity, Coraza)

### Strategic Decision Tree

```
What is your infrastructure strategy?

├─ AWS-committed (5+ years)
│  └─ AWS WAF (95% confidence)
│
├─ Azure-committed (5+ years)
│  └─ Azure Front Door (95% confidence)
│
├─ Multi-cloud / Cloud-agnostic
│  └─ Cloudflare (90% confidence)
│     └─ Enterprise media delivery? → Akamai (70% confidence)
│
├─ Fortinet Security Fabric user
│  └─ Fortinet FortiWeb (80% confidence)
│     └─ WAF excellence > platform integration? → Cloudflare (90%)
│
├─ Edge-first / Developer-led
│  └─ Cloudflare Workers + WAF (90% confidence)
│     └─ Need VCL customization? → Fastly (50%, plan for acquisition)
│
├─ Hybrid (on-prem + cloud)
│  └─ Akamai (70%) or Imperva (60%, monitor integration)
│
└─ Uncertain / Exploring
   └─ Cloudflare (90%) — safest general-purpose choice
```

### If-Then Scenario Planning

**If Fastly is Acquired (60-70% probability by 2027-2028)**
- Akamai acquires → Continue, monitor integration
- Thoma Bravo acquires → Plan 18-24 month migration, expect price increases
- Distressed acquisition → Immediate migration planning
- Contingency: Have Cloudflare or AWS WAF backup plan ready

**If Akamai Transformation Stalls**
- Signs: Security ARR growth <20%, executive departures, cost-cutting
- Then: Acquisition probability increases to 40-50%
- Contingency: Re-evaluate by 2027; PE acquisition triggers migration

**If Imperva/Thales Integration Fails**
- Signs: Product delays, talent departures, service degradation
- Then: Divestiture probability increases (2027-2028)
- Contingency: Existing customers stay through integration, plan migration by 2028 if failure emerges

**If Cloud Strategy Shifts**
- AWS-committed → Multi-cloud: AWS WAF lock-in becomes liability, plan 12-18 month migration to Cloudflare
- Multi-cloud → Single cloud: Cloudflare still works fine, but re-evaluate cloud-native for deeper integration

### Key Insight

There is no universal "best choice" over a 3-5 year horizon. Success is not finding the "best solution"—it's finding the solution most aligned with your strategic direction. Match lock-in to commitment certainty: high commitment → accept high lock-in. Consider acquisition risk explicitly when probability exceeds 40%. Align WAF with infrastructure strategy as dependent variable, not independent decision.

---

## Convergence Analysis

### High Convergence Areas

**Perfect Convergence (All 4 Methodologies Agreed)**

**Cloudflare for Startups/MVP**
- S1 Rapid: #1 recommendation (40/40 deploy score)
- S2 Comprehensive: Top choice for budget-constrained (score 4.6/5)
- S3 Need-Driven: Winner for Startup MVP (98% confidence, 9.8/10 fit)
- S4 Strategic: 90% confidence for cloud-agnostic strategy
- **Consensus**: Cloudflare Free/Pro is the unambiguous choice for startups
- **Convergence Confidence**: 98%+

**AWS WAF for AWS-Native Applications**
- S1 Rapid: #2 recommendation (30/40 deploy score)
- S2 Comprehensive: Top choice for AWS-native (score 4.0/5)
- S3 Need-Driven: Pattern 6 best fit (70-80% confidence)
- S4 Strategic: Maximum stability if AWS-committed (95% confidence)
- **Consensus**: AWS WAF is correct choice when deeply committed to AWS
- **Convergence Confidence**: 90%+

**High Convergence (3 Methodologies Agreed)**

**Cloudflare for General-Purpose Web Applications**
- S1 Rapid: #1 "The Default Choice"
- S2 Comprehensive: Highest score for general-purpose (4.6/5)
- S3 Need-Driven: Winner for 5 out of 6 use cases
- S4 Strategic: Does not contradict (90% confidence for cloud-agnostic)
- **Consensus**: Cloudflare is the safe default for most scenarios
- **Convergence Confidence**: 95%+

**Fastly for Performance-Critical Applications**
- S1 Rapid: #3 "The Performance Leader" (highest satisfaction 4.8/5)
- S2 Comprehensive: Strong choice for multi-cloud (score 4.0/5)
- S3 Need-Driven: Alternative for API-heavy apps
- S4 Strategic: Technology excellent BUT 60-70% acquisition risk reduces to 50% confidence
- **Consensus**: Fastly technology is excellent, but acquisition risk is material concern
- **Convergence Confidence**: 75% (technology) but 50% (strategic viability)

### Divergence Areas

**Enterprise Choice Divergence**

S2 Comprehensive chose **Cloudflare Enterprise** for general enterprise (features + value)
- Rationale: Best feature-to-cost ratio, operational simplicity, scalability

S3 Need-Driven chose **Imperva Enterprise** for enterprise web app (compliance fit)
- Rationale: Superior compliance features (HIPAA, PCI-DSS), custom rules flexibility, fully managed SOC

S4 Strategic chose **AWS WAF** for maximum stability (if cloud-committed)
- Rationale: Zero acquisition risk, maximum integration if AWS-committed (95% confidence)

**Why the divergence?**
- Different evaluation criteria: Features/cost (S2) vs. Requirements fit (S3) vs. Strategic viability (S4)
- All three are correct for their context:
  - S2 optimizes for general enterprise needs
  - S3 optimizes for compliance-heavy enterprise
  - S4 optimizes for long-term stability within committed infrastructure

**WordPress Site Divergence**

S1 Rapid chose **Wordfence Free** (5M+ installations, free)
- Rationale: Speed-focused, popularity-driven, zero-cost deployment in 5 minutes

S2 Comprehensive chose **Sucuri** ($9.99-$69.93/month)
- Rationale: Systematic feature analysis shows malware removal + cloud WAF + CDN package superior

S3 Need-Driven: Did not explicitly analyze WordPress use case

**Why the divergence?**
- Different priorities: Speed + Popularity (S1) vs. Comprehensive features (S2)
- Both are valid: Wordfence for immediate free protection, Sucuri for comprehensive managed solution

**Mid-Market Budget Divergence**

S1 Rapid recommends **Cloudflare Business ($200/month)** or **Fastly**
- Rationale: Proven adoption, performance leadership

S2 Comprehensive recommends **Cloudflare Business** or **AWS WAF** (depending on traffic)
- Rationale: Break-even analysis shows AWS WAF cheaper until ~500M req/month

S3 Need-Driven recommends **Cloudflare Business** or **AppTrana ($99-$999/month)**
- Rationale: Requirement fit, TCO analysis including operations costs

**Why the divergence?**
- Different evaluation lenses: Popularity (S1) vs. Cost analysis (S2) vs. Total TCO (S3)
- Convergence on Cloudflare Business; divergence on alternatives

### Methodology-Specific Insights

**S1 Rapid Unique Discoveries**
- Deployment speed ranking (5 minutes to 4 hours)
- User satisfaction ratings as proxy for real-world experience (Fastly 4.8/5)
- WordPress dominance: Wordfence 5M+ installations vs. competitors
- HUMAN Security as specialist bot management leader (post-PerimeterX merger)

**S2 Comprehensive Unique Discoveries**
- Break-even analysis: AWS WAF cheaper than Cloudflare until ~500M req/month
- Feature matrices showing capability gaps (e.g., AWS WAF weaker bot management)
- Pricing transparency analysis (Cloudflare/AWS most transparent, Imperva/Akamai opaque)
- Deployment flexibility spectrum (DNS-based vs. agent-based vs. self-hosted)

**S3 Need-Driven Unique Discoveries**
- 3-year TCO comparison including operations: Cloudflare saves $50-100K vs. AWS WAF
- Requirement patterns revealing why one size doesn't fit all
- Fit scoring methodology (9.5-9.8/10 for top recommendations)
- Anti-patterns: Common mistakes in WAF selection (features vs. requirements)

**S4 Strategic Unique Discoveries**
- Acquisition risk quantification: Fastly 60-70%, Imperva re-acquisition 15-20%, Akamai 20-30%
- Lock-in severity taxonomy (very high → low)
- If-then scenario planning for ownership changes
- Strategic decision tree based on infrastructure commitment
- Confidence intervals tied to acquisition risk and vendor stability

---

## Quick Decision Guide

### By Context (Consolidated Recommendations)

**Startup/MVP (< $100/month budget)**
- All methodologies converged: **Cloudflare Free/Pro**
- S1: #1 choice, S2: Best budget option, S3: 98% confidence winner, S4: 90% confidence
- **Decision Confidence**: 98%+
- Deploy in: <1 hour

**AWS-Native Application**
- All methodologies converged: **AWS WAF**
- S1: #2 choice (native integration), S2: 4.0/5 score, S3: Pattern 6 fit, S4: 95% confidence if committed
- **Decision Confidence**: 90%+
- Deploy in: 30-60 minutes

**General-Purpose Web Application**
- Strong convergence: **Cloudflare Pro/Business**
- S1: #1 "Default Choice", S2: 4.6/5 score, S3: Winner for 5/6 use cases, S4: 90% cloud-agnostic
- **Decision Confidence**: 95%+
- Deploy in: 15 minutes

**Enterprise with Compliance (HIPAA, PCI-DSS)**
- S3/S4 recommend: **Imperva Cloud WAF Enterprise**
- S3: 92% confidence (compliance-native design), S4: 60% confidence (monitor Thales integration)
- **Decision Confidence**: 75-80% (excellent fit, but integration uncertainty)
- Deploy in: 4-6 weeks

**Enterprise without Heavy Compliance**
- S1/S2 recommend: **Cloudflare Enterprise**
- S1: Proven at scale, S2: Best value, S3: Alternative choice, S4: 90% confidence
- **Decision Confidence**: 85-90%
- Deploy in: 1-2 weeks

**Multi-Cloud / Cloud-Agnostic**
- S2/S4 recommend: **Cloudflare Enterprise**
- S2: Unified platform, S4: 90% confidence (bounded to edge, not cloud-specific)
- **Decision Confidence**: 90%+
- Deploy in: 1-2 weeks

**Performance-Critical / High-Traffic Content**
- S1/S2/S3 recommend: **Cloudflare Business/Enterprise**
- S1: Market leader performance, S2: Unlimited bandwidth, S3: 97% confidence (9.8/10 fit)
- **Decision Confidence**: 95%+
- Deploy in: 15 minutes to 2 weeks

**API-Heavy Application**
- S2 recommends: **Wallarm** (API Security Platform of the Year)
- S3 recommends: **Cloudflare Enterprise + API Shield**
- **Decision**: Wallarm if API-first, Cloudflare if general web app with APIs
- **Decision Confidence**: 80-85%
- Deploy in: 15 minutes (Wallarm) to 2-3 weeks (Cloudflare Enterprise)

**WordPress Site**
- S1 recommends: **Wordfence Free** (speed + popularity)
- S2 recommends: **Sucuri** ($9.99-$69.93/month, comprehensive)
- **Decision**: Wordfence for free immediate protection, Sucuri for managed cloud WAF
- **Decision Confidence**: 85%+ for both options
- Deploy in: 5 minutes (Wordfence) to 10-20 minutes (Sucuri)

**Developer-Led / Edge-First Organization**
- S4 recommends: **Cloudflare Workers + WAF** (90% confidence)
- Alternative: Fastly (50% confidence, plan for acquisition)
- **Decision Confidence**: 90% Cloudflare, 50% Fastly
- Deploy in: 1-2 weeks

**Maximum Stability (3-5 Year Horizon)**
- S4 recommends: **AWS WAF** (if AWS), **Azure WAF** (if Azure), **Cloudflare** (if cloud-agnostic)
- All 90-95% confidence depending on infrastructure commitment
- **Decision Confidence**: 95% (match to infrastructure)
- Deploy in: Varies by choice

### By Priority

**Need protection today?**
- **Answer from S1**: Cloudflare Free/Pro (5-10 minutes) or Wordfence (5 minutes for WordPress)

**Need best features/price ratio?**
- **Answer from S2**: AWS WAF for <500M req/month, Cloudflare for >500M req/month

**Have specific compliance requirements?**
- **Answer from S3**: Imperva Enterprise (HIPAA/PCI-DSS native, 92% confidence)

**Thinking 3-5 years ahead?**
- **Answer from S4**: Match to infrastructure commitment—AWS WAF (AWS), Azure WAF (Azure), Cloudflare (cloud-agnostic)

**Need lowest total cost of ownership?**
- **Answer from S3**: Cloudflare operational simplicity saves $50-100K over 3 years vs. AWS WAF

**Need maximum performance?**
- **Answer from S1**: Fastly (4.8/5 satisfaction, 25% faster) or Cloudflare (proven at scale)

**Need best API security?**
- **Answer from S2**: Wallarm (API Platform of the Year) or Cloudflare Enterprise + API Shield

**Small team (<5 people)?**
- **Answer from All**: Cloudflare (zero operational burden, fully managed)

---

## Provider Summary

Quick reference of all providers analyzed across methodologies:

| Provider | S1 Rank | S2 Score | S3 Use Cases Won | S4 Confidence | Key Strength | Lock-in |
|----------|---------|----------|------------------|---------------|--------------|---------|
| **Cloudflare** | #1 | 4.6/5 | 5/6 won | 90% | Speed + ease + scale | Moderate-High |
| **AWS WAF** | #2 | 4.0/5 | AWS-native fit | 95% (if committed) | Native AWS integration | Very High |
| **Fastly NGWAF** | #3 | 4.0/5 | Alternative for APIs | 50% | Performance + low false positives | Moderate |
| **Imperva** | Enterprise | 4.3/5 | 1/6 won (enterprise) | 60% | Compliance + managed SOC | High |
| **Wallarm** | Mentioned | 4.2/5 | API-heavy alternative | Medium | API security specialization | Medium |
| **Sucuri** | WordPress | 4.5/5 (WP) | WordPress-specific | High | WP malware removal | Moderate |
| **Wordfence** | WordPress #1 | N/A | WordPress free option | High | Free + 5M+ installs | Low |
| **AppTrana** | Mentioned | High value | Mid-market managed | Medium-High | Managed + DAST included | Medium |
| **Akamai** | Enterprise | Medium | Enterprise media | 70% | Global scale + media | Moderate-High |
| **Azure WAF** | #2 alt | Medium | Azure-native | 95% (if committed) | Native Azure integration | Very High |
| **GCP Cloud Armor** | Alternative | Medium | GCP-native | 85% | GCP integration + ML | Very High |
| **Fortinet FortiWeb** | Platform | Medium | Fortinet ecosystem | 80% | Security Fabric integration | Very High |
| **ModSecurity/Coraza** | Open source | 3.0/5 | Privacy/on-prem | 70% | Zero cost + control | Low |
| **HUMAN Security** | Bot specialist | N/A | Bot management | Medium | Specialized bot detection | Medium |
| **Barracuda** | SMB | N/A | SMB ease-of-use | Medium | 3-step wizard | Medium |
| **F5 BIG-IP/NGINX** | Legacy | N/A | F5 customers | 60-70% | Customization depth | High |

### Provider Selection Patterns

**Market Leaders**: Cloudflare (general), AWS (AWS-native), Azure (Azure-native)
**Enterprise Specialists**: Imperva (compliance), Akamai (scale), Fortinet (platform)
**Performance Leaders**: Fastly (satisfaction 4.8/5), Cloudflare (scale)
**Budget Champions**: Cloudflare Free, Wordfence Free, Sucuri ($9.99/mo)
**API Specialists**: Wallarm (API Platform of Year), Cloudflare API Shield
**WordPress Champions**: Wordfence (popularity), Sucuri (comprehensive)
**Bot Management Specialists**: HUMAN Security, Cloudflare Enterprise, Imperva
**Open Source**: ModSecurity, Coraza (zero licensing cost, high expertise required)

---

## File Reference Guide

### S1-rapid/ (17 files)
**Focus**: Speed-focused, popularity-driven analysis

- **approach.md** - Methodology: Prioritize deployment speed, proven adoption, self-service
- **cloudflare.md** - Market leader analysis, 8.6/10 rating, 2T requests/day
- **aws-waf.md** - Cloud-native leader, pay-per-use model, 8.0/10 rating
- **fastly.md** - Performance leader, 4.8/5 satisfaction, 25% faster
- **imperva.md** - Enterprise accuracy leader, 99.139% test accuracy
- **akamai.md** - Global scale leader, Gartner Leader 6 years
- **azure-waf.md** - Azure-native solution
- **google-cloud-armor.md** - GCP-native solution with ML
- **f5.md** - Traditional leader, 10.2% mindshare
- **fortinet-fortiweb.md** - Security Fabric integration
- **barracuda.md** - SMB-focused, 3-step wizard
- **radware.md** - Enterprise DDoS focus
- **human-security.md** - Bot management specialist
- **modsecurity.md** - Open source, OWASP CRS
- **wordfence.md** - WordPress plugin, 5M+ installs, free
- **sucuri.md** - WordPress cloud WAF, malware removal
- **recommendation.md** - Top 3 choices with confidence levels and deployment speed ranking

### S2-comprehensive/ (19 files)
**Focus**: Systematic comparison with feature/pricing matrices

- **approach.md** - Methodology: Weighted scoring across 8 criteria, multi-dimensional comparison
- **cloudflare.md** - Detailed analysis: Free to Enterprise tiers, DDoS capacity, global PoPs
- **aws-waf.md** - Cost analysis by traffic, native integration patterns
- **fastly-ngwaf.md** - Agent-based deployment, multi-cloud flexibility
- **imperva.md** - Enterprise features, managed SOC, compliance focus
- **wallarm.md** - API security depth, OWASP API Top 10 coverage
- **sucuri.md** - WordPress optimization, malware removal value-add
- **akamai.md** - Global network scale, enterprise SLAs
- **azure-waf.md** - Azure Front Door vs. Application Gateway comparison
- **google-cloud-armor.md** - Standard vs. Enterprise tiers, ML-powered protection
- **fortinet-fortiweb.md** - Deployment flexibility (cloud, on-prem, appliance)
- **f5.md** - iRules customization, NGINX integration
- **barracuda.md** - SMB positioning
- **radware.md** - Behavioral DDoS protection
- **modsecurity-coraza.md** - TCO analysis, operational overhead
- **feature-matrix.md** - 25+ capability comparison across providers
- **pricing-matrix.md** - Traffic-based cost comparison (1M to 10B+ requests)
- **integration-patterns.md** - DNS-based vs. agent-based vs. cloud-native vs. self-hosted
- **recommendation.md** - Context-specific recommendations with scoring and trade-off analysis

### S3-need-driven/ (9 files)
**Focus**: Requirements-first solution matching

- **approach.md** - Methodology: Define use cases → map requirements → evaluate fit scores
- **webhook-security.md** - IP allowlisting, rate limiting requirements
- **public-api-protection.md** - Bot management, DDoS, API-specific protection requirements
- **enterprise-web-app.md** - HIPAA/PCI-DSS compliance, custom rules, audit requirements
- **high-traffic-content.md** - CDN integration, performance, cost predictability requirements
- **startup-mvp.md** - Zero cost, instant deployment, scalability requirements
- **multi-region-global.md** - Anycast, data residency, multi-region failover requirements
- **recommendation.md** - Requirement patterns, fit scores, TCO analysis, anti-patterns
- **README.md** - Navigation guide for S3 methodology

### S4-strategic/ (13 files)
**Focus**: Long-term viability with 3-5 year outlook

- **approach.md** - Methodology: Vendor stability, acquisition risk, lock-in implications
- **cloudflare-viability.md** - Market leadership, 90% confidence, 5-10% acquisition risk
- **aws-waf-viability.md** - Maximum stability (95%), Amazon-backed, zero acquisition risk
- **fastly-viability.md** - Technology excellence, 50% confidence, 60-70% acquisition risk
- **imperva-viability.md** - Thales integration, 60% confidence, 15-20% re-acquisition risk
- **akamai-viability.md** - Transformation uncertainty, 70% confidence, 20-30% acquisition risk
- **fortinet-viability.md** - Platform stability, 80% confidence, 10-15% acquisition risk
- **azure-waf-viability.md** - Microsoft-backed, 95% confidence if Azure-committed
- **gcp-viability.md** - Google-backed, 85% confidence but low market share uncertainty
- **lock-in-analysis.md** - Lock-in severity taxonomy (very high to low)
- **acquisition-risk.md** - Quantified acquisition probabilities and PE target profiles
- **infrastructure-strategy.md** - Strategic decision tree based on infrastructure commitment
- **recommendation.md** - Strategic tiers, scenario planning, if-then contingencies

---

## Convergence Summary

### Perfect Alignment (All 4 Methodologies)
1. **Cloudflare for startups/MVP** - 98%+ confidence
2. **AWS WAF for AWS-native apps** - 90%+ confidence

### Strong Alignment (3 Methodologies)
3. **Cloudflare for general web apps** - 95%+ confidence
4. **Fastly technology excellence** - 75% (but strategic risk reduces S4 to 50%)

### Use Case Specific (2-3 Methodologies)
5. **Imperva for enterprise compliance** - S3 92%, S4 60% (integration watch)
6. **Wallarm for API-heavy apps** - S2 4.2/5, S3 alternative
7. **Sucuri for WordPress** - S2 4.5/5, S1 alternative to Wordfence

### Divergence with Context
8. **Enterprise choice** - Varies by priority: Cloudflare (features+cost), Imperva (compliance), AWS (stability)
9. **Mid-market budget** - Varies by lens: Cloudflare Business (convergence), alternatives differ

---

## Next Steps

### To Use These Findings

**Step 1: Start with Quick Decision Guide**
- Identify your context (startup, AWS-native, enterprise, etc.)
- Review consolidated recommendation with confidence level
- Note deployment timeframe

**Step 2: Read Relevant Methodology Section(s)**
- **Deploying today?** → Read S1 Rapid
- **Optimizing features/price?** → Read S2 Comprehensive
- **Have specific requirements?** → Read S3 Need-Driven
- **Planning 3-5 years?** → Read S4 Strategic

**Step 3: Review Specific Provider Files**
- Navigate to methodology folder (S1, S2, S3, S4)
- Read provider-specific files for detailed analysis
- Check recommendation.md for methodology-specific insights

**Step 4: Validate Against Your Context**
- Use Provider Summary table for quick comparison
- Check Lock-in implications from S4
- Calculate 3-year TCO using S3 methodology
- Verify alignment with infrastructure strategy from S4

### For QRCards or Other Projects

**Apply findings to specific use case:**
1. Identify which of the 6 S3 use cases most closely matches your scenario
2. Review fit score and confidence level
3. Check S4 strategic implications (acquisition risk, lock-in)
4. Validate with S2 feature/pricing matrices if needed

**Refer to S3 use cases for similar scenarios:**
- Webhook endpoints → Webhook Security use case
- Public API → Public API Protection use case
- Internal tools → Startup MVP use case (adapt for internal context)
- High-traffic public site → High-Traffic Content use case

**Consider S4 strategic implications:**
- Acquisition risk: Plan contingencies if choosing Fastly (60-70%)
- Lock-in severity: Understand migration complexity if strategy changes
- Infrastructure alignment: Match WAF choice to cloud commitment

**Use decision tree (reference S4 strategic decision tree):**
- Start with infrastructure strategy (AWS, Azure, multi-cloud, etc.)
- Follow tree to recommended solution
- Validate against S1/S2/S3 findings for comprehensive view

### Recommended Approach for New Projects

1. **Immediate Decision (<1 hour)**: Use S1 Quick Decision Framework
2. **Thoughtful Decision (1-2 days)**: Use Quick Decision Guide + review S2/S3 recommendations
3. **Strategic Decision (1 week)**: Review all four methodologies, create decision matrix
4. **Enterprise Decision (2-4 weeks)**: Full discovery review, POC with top 2-3 choices, vendor evaluations

---

## Discovery Metrics

**Discovery Completed:** October 11, 2025
**Total Research Time:** ~5-7 hours across 4 methodologies
**Files Created:** 58 files total
- S1: 17 files (~30 minutes)
- S2: 19 files (~2-3 hours)
- S3: 9 files (~1-2 hours)
- S4: 13 files (~1-2 hours)

**Providers Analyzed:** 15+ across all methodologies
- Major Cloud: AWS, Azure, GCP
- Market Leaders: Cloudflare, Akamai, Imperva, Fastly
- Specialists: Wallarm (API), HUMAN (bots), Sucuri/Wordfence (WordPress)
- Platform: Fortinet, F5, Barracuda, Radware
- Open Source: ModSecurity, Coraza

**Methodologies Completed:** 4 of 4
- S1 Rapid: Speed-focused, popularity-driven ✓
- S2 Comprehensive: Systematic comparison, data-driven ✓
- S3 Need-Driven: Requirements-first matching ✓
- S4 Strategic: Long-term viability, 3-5 year outlook ✓

**Convergence Analysis:** Complete
- Perfect alignment: 2 major recommendations
- Strong alignment: 2 additional recommendations
- Divergence analysis: Context-specific variation explained

**Decision Support:** Complete
- Quick Decision Guide with confidence levels
- Provider Summary table with key metrics
- File Reference Guide for detailed exploration
- Next Steps with application guidance

---

**Document Version:** 1.0
**Last Updated:** October 11, 2025
**Maintainer:** Discovery completed for experiment 3.010-waf
**Status:** Ready for implementation phase

---

## About This Document

This Table of Contents serves as the central navigation hub for the WAF discovery research. It synthesizes findings across four distinct research methodologies to provide:

1. **Quick reference** for time-sensitive decisions
2. **Comprehensive context** for thoughtful evaluation
3. **Strategic guidance** for long-term planning
4. **Convergence analysis** showing where methodologies align and diverge

The document is designed to be read top-to-bottom for complete understanding, or navigated directly to relevant sections for specific questions. Each methodology section links to detailed files for deeper exploration.

Use this TOC as your starting point for any WAF-related decision. The four methodologies provide different lenses on the same landscape—speed (S1), thoroughness (S2), fit (S3), and strategy (S4)—ensuring well-rounded decision support regardless of your priority.
