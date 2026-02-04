# Fastly Next-Gen WAF (Signal Sciences) - Comprehensive Analysis

## Provider Overview

**Company:** Fastly, Inc. (acquired Signal Sciences in 2020)
**Founded:** Signal Sciences 2014, acquired 2020
**Market Position:** Developer-focused, modern application security
**Primary Model:** Hybrid SaaS WAF (agent-based, edge, or cloud)
**Unique Value:** Extreme deployment flexibility, DevOps integration

Fastly Next-Gen WAF, originally Signal Sciences, pioneered the agent-based WAF architecture. Unlike traditional reverse proxy models, it can deploy at the application server, reverse proxy, or edge, providing unprecedented flexibility for modern cloud-native applications.

## Architecture and Deployment

### Deployment Models (Choose One or Multiple)
1. **Agent + Module Deployment (On-Prem WAF)**
   - Module: Installed in web server (NGINX, Apache, IIS) or application (via SDK)
   - Agent: Runs as service, makes block/allow decisions, sends telemetry to cloud
   - Traffic inspection: Inline at origin
   - Setup time: 30-60 minutes

2. **Cloud WAF (Reverse Proxy)**
   - Fastly hosts agent in their cloud
   - Simple DNS change to route traffic through Fastly
   - No software installation required
   - Setup time: 15-30 minutes

3. **Edge WAF (Fastly CDN Integration)**
   - Integrated with Fastly's edge cloud platform
   - Includes DDoS protection, TLS management, CDN
   - Full edge compute capabilities via Compute@Edge
   - Setup time: 30-60 minutes

4. **Hybrid Deployments**
   - Combine agent-based + cloud for layered security
   - Multi-site protection with unified policies
   - Flexibility to protect heterogeneous infrastructure

### Technical Architecture
**Agent-Module Topology:**
- Module: Lightweight inspection engine embedded in traffic path
- Agent: Decision engine, rate limiting, threat intelligence integration
- Cloud: Management plane, dashboards, threat intel aggregation

**Key Advantages:**
- Zero network changes for agent-based deployment
- Deploys anywhere (cloud, on-prem, containers, serverless)
- Observability without blocking (monitor mode)
- Works with any proxy/load balancer

**Considerations:**
- Agent requires compute resources (CPU, memory)
- Agent-based deployment needs software installation per node
- Cloud/Edge models similar constraints to other reverse proxy WAFs

## Features and Capabilities

### Web Application Firewall (WAF)
**Protection Coverage:**
- OWASP Top 10 comprehensive coverage
- Zero-day attack detection via anomaly detection
- Advanced application attacks (business logic abuse)
- API abuse and schema violations
- Attack attribution and IP reputation

**Detection Engine:**
- Signal-based detection (high confidence, low false positives)
- Request rate anomaly detection
- Attack surface mapping
- Threat intelligence from Network Learning Exchange (NLX)

**Rule Management:**
- Power Rules: Complex rule creation with expressions
- Templated rules for common use cases
- Tag-based rule application (flexible targeting)
- Version control and rollback support
- No manual signature updates (cloud-managed)

### Network Learning Exchange (NLX)
**Unique Feature:**
- Collective threat intelligence across all Fastly NGWAF customers
- Real-time IP reputation sharing
- Attack pattern recognition
- Opt-in (but valuable for detection accuracy)
- Anonymized threat data aggregation

### Rate Limiting and Abuse Prevention
**Capabilities:**
- Advanced rate limiting per IP, signal, custom keys
- Distributed rate limiting across infrastructure
- Account takeover prevention
- Credential stuffing detection
- API abuse prevention

**Granularity:**
- Per-second, per-minute, per-hour windows
- Complex aggregation keys (IP + endpoint + user)
- Dynamic thresholds based on behavior
- Action customization (block, challenge, log)

### Bot Management
**Detection Methods:**
- Behavioral analysis
- Device fingerprinting
- JavaScript challenge
- CAPTCHA integration
- Known bot identification

**Categories:**
- Good bots (search engines, monitoring)
- Bad bots (scrapers, attackers)
- Unknown bots (requires classification)
- Custom bot definitions

### API Security
**Features:**
- Automatic API discovery
- OpenAPI/Swagger schema validation
- REST, gRPC, GraphQL, WebSocket protection
- API abuse detection (unexpected parameters, values)
- Rate limiting per endpoint
- Authentication enforcement

**Visibility:**
- API endpoint inventory
- Parameter tracking
- Schema drift detection
- Sensitive data exposure alerts

### Advanced Protection
**Account Takeover (ATO) Prevention:**
- Login anomaly detection
- Credential stuffing protection
- Impossible travel detection
- Device intelligence

**Client-Side Protection:**
- Magecart/formjacking detection
- JavaScript injection monitoring
- Third-party script visibility

**DDoS Protection (Edge WAF only):**
- Layer 7 DDoS mitigation
- Distributed denial of service protection
- Traffic surge handling
- Rate limiting at edge

## Pricing Structure

### Pricing Model
**Structure:**
- Priced per site (workspace) and average requests per second (RPS)
- All deployments: site fee + RPS fee
- Edge WAF: Additional CDN/delivery charges

**Free Trial:**
- Up to $50/month of traffic free
- No commitment required
- Full feature access during trial

### Deployment Pricing
**On-Prem WAF (Agent-Module):**
- Site-based pricing (exact figures not public)
- Estimated: $500-$2,000/month per site (varies by RPS)
- One-time implementation services fee (first deployment)
- No per-request charges (included in RPS capacity)

**Cloud WAF:**
- Similar site + RPS pricing to on-prem
- No infrastructure costs (Fastly-hosted)
- Estimated: $500-$2,500/month per site

**Edge WAF:**
- Site + RPS pricing for WAF component
- Additional Fastly delivery charges (CDN bandwidth, compute)
- Estimated: $1,000-$5,000/month per site (including delivery)
- Scales with bandwidth usage

### Implementation Services
**One-Time Fees:**
- First deployment includes implementation services
- Typical range: $5,000-$15,000 (varies by complexity)
- Includes onboarding, configuration, training
- Subsequent sites may have reduced fees

### Cost Considerations
**Hidden/Additional Costs:**
- Edge WAF: Delivery charges can be significant (bandwidth, compute)
- Implementation services (one-time)
- Premium support tiers (optional)
- Professional services for custom integrations

**Volume Discounts:**
- Enterprise pricing for high RPS or many sites
- Annual contracts provide discounts
- Multi-site deployments may receive bundled pricing

## Use Cases and Fit

### Ideal For:
1. **DevOps/Cloud-Native Teams**
   - Agent-based deployment fits CI/CD workflows
   - Infrastructure-as-Code friendly
   - Observability-first approach (monitor before block)

2. **Heterogeneous Infrastructures**
   - Multi-cloud deployments (AWS, Azure, GCP)
   - Hybrid cloud + on-premise
   - Microservices and containerized applications

3. **API-Heavy Applications**
   - Strong API discovery and protection
   - Schema validation and abuse detection
   - Supports modern API protocols (gRPC, GraphQL)

4. **Applications Requiring Zero Network Changes**
   - Agent-based deployment doesn't alter network topology
   - Works behind existing load balancers/proxies
   - Gradual rollout without infrastructure risk

5. **Security-Conscious Developers**
   - Developer-friendly UI and APIs
   - Integrates with SIEM, SOAR, incident response tools
   - Detailed attack visibility for debugging

### Less Ideal For:
1. **Budget-Constrained Projects**
   - Pricing typically higher than cloud-native WAFs (AWS, Azure)
   - Implementation fees add to initial cost
   - Better suited for mid-market to enterprise

2. **Simple, Static Websites**
   - Overkill for basic content sites
   - Simpler solutions like Cloudflare Free/Pro sufficient
   - Cost-benefit doesn't justify for low-risk sites

3. **Organizations Without DevOps Capability**
   - Agent management requires some technical expertise
   - Self-tuning is minimal but monitoring needed
   - Managed service alternatives (AppTrana) may be better fit

4. **Extremely High Traffic (>10B req/month)**
   - RPS-based pricing can become expensive
   - Flat-rate providers (Cloudflare Enterprise) may be more cost-effective
   - Edge WAF delivery charges scale with bandwidth

## Strengths

1. **Deployment Flexibility**
   - Unique agent-based option (zero network changes)
   - Multiple deployment models (on-prem, cloud, edge)
   - Works anywhere (cloud, on-prem, containers, K8s, serverless)

2. **Low False Positives**
   - Signal-based detection (high confidence)
   - NLX threat intelligence reduces noise
   - DevOps teams can run in blocking mode quickly
   - Fastly claims 88% of customers use blocking mode (vs. log-only)

3. **Developer/DevOps Experience**
   - Clean, modern UI
   - Excellent API and integration options
   - Strong observability and debugging tools
   - Infrastructure-as-Code support

4. **API Security Excellence**
   - Automatic API discovery
   - Schema validation and drift detection
   - Supports modern protocols (gRPC, GraphQL, WebSockets)
   - Strong API abuse prevention

5. **Gartner Recognition**
   - Only vendor to be Customers' Choice for WAAP 7 years in a row
   - High customer satisfaction scores
   - Strong analyst backing

6. **Network Learning Exchange (NLX)**
   - Collective threat intelligence
   - Real-time IP reputation
   - Improves detection accuracy across customer base
   - Unique differentiator vs. competitors

## Weaknesses

1. **Higher Pricing**
   - More expensive than cloud-native WAFs (AWS, Azure, GCP)
   - Implementation fees add to initial costs
   - Not cost-competitive for price-sensitive projects

2. **Complexity (Agent-Based)**
   - Agent deployment requires software installation per node
   - Agent resource consumption (CPU, memory)
   - Operational overhead for agent updates and monitoring

3. **Limited DDoS Protection (Except Edge WAF)**
   - On-prem and Cloud WAF lack comprehensive DDoS mitigation
   - Requires separate DDoS protection for large volumetric attacks
   - Edge WAF includes DDoS but adds cost

4. **Pricing Opacity**
   - No public pricing (must contact sales)
   - Implementation fees variable
   - Difficult to estimate costs without quote

5. **Edge WAF Delivery Costs**
   - Bandwidth and compute charges can be significant
   - Less transparent than competitors (Cloudflare unlimited bandwidth)
   - Delivery costs scale unpredictably with traffic patterns

6. **Smaller Market Share**
   - Less prevalent than Cloudflare, AWS, Azure
   - Smaller community and third-party integrations
   - Fewer tutorials and community resources

## Integration Patterns

### Agent-Module Integration (On-Prem)
1. Install Agent on application server (Docker, K8s, VM)
2. Install Module in web server (NGINX, Apache) or application (via SDK)
3. Configure Agent to communicate with Fastly cloud
4. Deploy Power Rules and policies via dashboard
5. Monitor signals and tune rules

**Supported Platforms:**
- Web Servers: NGINX, Apache, IIS, OpenResty
- Reverse Proxies: NGINX, HAProxy, Envoy, Kong
- Application Servers: Java (filter), .NET, Python (WSGI), Go, Node.js
- Containers: Docker, Kubernetes (DaemonSet/Sidecar)
- Serverless: AWS Lambda, Azure Functions (limited)

### Cloud WAF Integration
1. Update DNS to point to Fastly-hosted agent
2. Configure origin server details
3. Set up SSL/TLS certificates
4. Deploy Power Rules via dashboard
5. Monitor and tune

### Edge WAF Integration
1. Set up Fastly CDN service
2. Enable Next-Gen WAF on service
3. Configure VCL (Varnish Configuration Language) if needed
4. Deploy rules and rate limiting
5. Leverage Compute@Edge for custom logic (optional)

### API and Automation
- REST API for programmatic configuration
- Terraform provider for Infrastructure-as-Code
- Webhook integrations for alerts
- SIEM/SOAR integrations (Splunk, Sumo Logic, Datadog)

## Performance Characteristics

**Latency Impact:**
- Agent-module: <5ms typical overhead (inline inspection)
- Cloud WAF: 10-20ms (reverse proxy latency)
- Edge WAF: 5-15ms (edge inspection + CDN benefits)

**Throughput:**
- Agent-module: Limited by agent CPU/memory (scalable horizontally)
- Cloud/Edge: Scales with Fastly infrastructure
- No explicit request rate limits (RPS capacity purchased)

**Reliability:**
- Agent-module: Depends on agent availability (high availability via redundancy)
- Cloud/Edge: Fastly SLA (~99.99% uptime)
- Fail-open mode available (continue on agent failure)

## Compliance and Certifications

- **PCI DSS:** Level 1 Service Provider
- **SOC 2 Type II:** Certified
- **ISO 27001:** Certified
- **GDPR:** Compliant tooling available
- **HIPAA:** Not a BAA provider (not suitable for PHI)
- **FedRAMP:** Not currently authorized

## Competitive Positioning

**Vs. Cloudflare:**
- Fastly more deployment flexible (agent-based option)
- Cloudflare easier to deploy (DNS only)
- Cloudflare more affordable (especially at scale)
- Fastly better API security and developer experience

**Vs. AWS WAF:**
- Fastly works anywhere (not AWS-only)
- AWS WAF more affordable at low-medium traffic
- Fastly easier to manage (less manual tuning)
- AWS WAF better for AWS-native applications

**Vs. Imperva:**
- Fastly more developer-friendly
- Imperva more enterprise-focused (managed services)
- Fastly better API security and modern app protection
- Imperva stronger traditional WAF and DDoS

**Vs. Akamai:**
- Fastly more affordable and agile
- Akamai more enterprise-established
- Fastly better DevOps integration
- Akamai better for global enterprises with complex needs

## Recommendation Score

**Security Efficacy:** 4.5/5 (excellent coverage, low false positives, NLX)
**Cost Efficiency:** 3/5 (good value but expensive vs. alternatives)
**Feature Completeness:** 4.5/5 (strong WAF, API security, bot management)
**Integration Ease:** 4/5 (flexible but agent complexity trade-off)
**Operational Complexity:** 4/5 (low false positives ease tuning, agent overhead)
**Vendor Factors:** 4/5 (strong backing, good support, smaller ecosystem)
**Performance:** 4/5 (low latency, scales well, agent resource usage)
**Compliance:** 4/5 (good certifications, not HIPAA BAA)

**Overall Score: 4.0/5**

## Final Assessment

Fastly Next-Gen WAF (Signal Sciences) excels as a modern, developer-friendly WAF solution with unmatched deployment flexibility. Its agent-based architecture is unique in the market, enabling protection without network topology changes—ideal for cloud-native, microservices, and multi-cloud environments.

**Best Choice For:** DevOps teams, cloud-native applications, heterogeneous infrastructures, API-heavy applications, organizations valuing deployment flexibility and low false positives, teams needing observability-first security.

**Consider Alternatives If:** Budget-constrained (AWS/Azure WAF cheaper), need fully managed services (AppTrana, Imperva managed), require strong DDoS protection (Cloudflare, Akamai), have simple static websites (overkill), or extremely high traffic where flat-rate pricing better (Cloudflare Enterprise).

**Confidence Level:** High - well-documented, strong analyst backing (Gartner Customers' Choice 7 years), though pricing opacity and limited public deployment examples reduce confidence slightly.
