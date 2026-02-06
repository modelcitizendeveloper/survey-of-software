# ModSecurity & Coraza - Self-Hosted Open Source WAF Analysis

## Provider Overview

**Solutions:** ModSecurity (C++) & Coraza (Go)
**Type:** Open source, self-hosted WAF engines
**License:** Apache 2.0 License
**Primary Model:** Embedded WAF module for web servers/proxies
**Unique Value:** Zero licensing cost, full control, privacy

ModSecurity and Coraza represent the self-hosted, open-source alternative to cloud-based WAF services. ModSecurity is the veteran (est. 2002), while Coraza is the modern Go-based successor aiming for ModSecurity compatibility with better performance.

## Architecture and Deployment

### ModSecurity
**Status:** NGINX integration EOL (March 31, 2024)
**Supported Platforms:**
- Apache HTTP Server (mod_security2)
- IIS (experimental)
- NGINX (deprecated, EOL)
- Envoy (via WebAssembly)

**LibModSecurity (v3):**
- Core library in C++
- Platform-agnostic connector architecture
- Requires connector for each web server

### Coraza
**Status:** Active development, OWASP project
**Supported Platforms:**
- NGINX (via coraza-nginx)
- Envoy (native integration)
- Caddy (native integration)
- Traefik (plugin)
- Kubernetes Ingress Controllers
- Standalone HTTP server mode

**Architecture:**
- Written in Go (better performance, memory safety)
- 100% compatible with ModSecurity SecLang rules
- Compatible with OWASP CRS v4

### Deployment Model
- **Type:** Embedded module at origin (web server/reverse proxy)
- **Setup Time:** 2-8 hours (depending on complexity)
- **Integration Effort:** High - requires server configuration, rule tuning
- **Traffic Flow:** Client → Web Server/Proxy (with embedded WAF) → Application

### Key Advantages
- Zero licensing cost (Apache 2.0)
- Full control over rules and data
- No traffic proxied to third party (privacy)
- No vendor lock-in
- Customizable and extensible

### Considerations
- Requires expertise to deploy and maintain
- Manual rule updates and tuning
- No managed SOC team or support
- Performance overhead on origin servers
- Scaling requires infrastructure scaling

## Features and Capabilities

### Web Application Firewall (WAF)

**OWASP Core Rule Set (CRS):**
- Comprehensive OWASP Top 10 coverage
- 100+ rules for SQLi, XSS, RCE, LFI/RFI
- Continuously updated by OWASP community
- Paranoia levels (1-4) for sensitivity tuning
- Compatible with both ModSecurity and Coraza

**Rule Engine:**
- SecLang rule language (expressive, flexible)
- Positive and negative security models
- Chain rules for complex logic
- Variables, collections, transformations
- Actions: block, pass, log, redirect, custom

**Custom Rules:**
- Full SecLang syntax support
- Regex matching
- Conditional logic
- Macro/variable substitution
- Extensibility via Lua (ModSecurity) or Go (Coraza)

### Request Inspection
**Capabilities:**
- HTTP headers, body, query parameters
- Multipart form data
- JSON and XML parsing
- File upload inspection
- Response body inspection (optional)

**Limitations:**
- Performance impact with deep inspection
- Large body inspection can consume memory
- No cloud-based threat intelligence (self-managed)

### Rate Limiting
**ModSecurity:**
- Basic rate limiting via collections
- IP-based tracking
- Manual configuration required
- Limited granularity vs. cloud WAFs

**Coraza:**
- Similar to ModSecurity
- Improved performance in Go
- Still requires manual configuration

**Limitations:**
- No built-in distributed rate limiting
- Requires external data store (Redis) for multi-server rate limiting
- Less sophisticated than cloud WAF rate limiting

### Bot Management
**Capabilities:**
- User-agent string matching
- Basic bot signatures (OWASP CRS includes some)
- Challenge-response (requires custom implementation)

**Limitations:**
- No ML-powered behavioral analysis
- No device fingerprinting
- No JavaScript challenge built-in
- Significantly weaker than cloud bot management platforms

### DDoS Protection
**Capabilities:**
- Application-layer (L7) attack mitigation via rules
- Basic rate limiting

**Limitations:**
- No network-layer (L3/4) protection
- Not suitable for large volumetric attacks
- Requires separate DDoS mitigation (e.g., upstream cloud scrubbing)
- Limited compared to Cloudflare, Imperva

### Logging and Monitoring
**Capabilities:**
- Detailed request/response logging
- Rule match logging
- ModSecurity audit log format
- Integration with SIEM via syslog, log files
- JSON log output

**Limitations:**
- No built-in dashboard (requires external tools)
- Log volume can be substantial (performance/storage impact)
- No cloud-based analytics

## Pricing Structure

### Cost Breakdown

**Licensing:** $0 (Apache 2.0, free and open source)

**Infrastructure Costs:**
- **Server Resources:** CPU, memory for WAF processing (variable)
- **Storage:** Logs and rule storage
- **Bandwidth:** Standard hosting costs
- Estimate: $50-$500/month depending on traffic and server specs

**Operational Costs:**
- **Initial Setup:** 10-40 hours (depending on complexity)
- **Ongoing Maintenance:** 5-20 hours/month (rule updates, tuning, monitoring)
- **Personnel:** Security engineer or DevOps with WAF expertise
- Estimate: $2,000-$10,000/month in personnel time (if calculated)

**Third-Party Rules (Optional):**
- OWASP CRS: Free
- Commercial rules (e.g., Trustwave Spider Labs): $1,000-$5,000/year (discontinued for ModSecurity)

**Total Cost of Ownership (TCO):**
- **Small Deployment:** $50-$300/month infrastructure + personnel time
- **Medium Deployment:** $300-$1,000/month infrastructure + personnel time
- **Large Deployment:** $1,000-$5,000/month infrastructure + significant personnel time

**Cost Comparison:**
- **Cheapest Option:** If you already have expertise and infrastructure
- **Hidden Costs:** Personnel time for deployment, tuning, maintenance
- **Break-Even:** Typically cost-effective only if:
  - You have in-house expertise
  - You require full control/privacy
  - You're running many applications (amortize personnel time)
  - Traffic is very high (cloud WAF per-request fees expensive)

## Use Cases and Fit

### Ideal For:
1. **Privacy-Sensitive Applications**
   - No third-party traffic proxying
   - Full data control
   - Air-gapped or on-premise environments

2. **Organizations with Strong In-House Expertise**
   - Security engineers familiar with WAF concepts
   - DevOps teams comfortable with server configuration
   - Existing IaC and automation infrastructure

3. **Cost-Sensitive High-Traffic Applications**
   - Cloud WAF per-request fees expensive at scale
   - Amortize personnel costs across high traffic
   - Break-even at >1B requests/month

4. **Custom/Niche Deployment Scenarios**
   - Embedded systems, edge devices
   - Custom web server platforms
   - Unique integration requirements

5. **Multi-Application Portfolios**
   - Amortize personnel costs across many apps
   - Standardized rules across applications
   - Centralized management infrastructure

### Less Ideal For:
1. **Small Teams Without WAF Expertise**
   - Steep learning curve
   - Requires ongoing maintenance
   - False positive management complex

2. **Rapid Deployment Needs**
   - Setup takes hours/days vs. minutes for cloud WAF
   - Tuning period required
   - Risk of misconfiguration

3. **DDoS-Prone Applications**
   - No network-layer protection
   - Limited L7 DDoS mitigation
   - Requires separate DDoS solution

4. **Bot-Heavy Applications**
   - Weak bot management vs. cloud platforms
   - No ML-powered detection
   - Requires custom implementation

5. **Compliance-Driven Organizations**
   - No vendor SLAs or certifications
   - Auditing burden on your organization
   - Managed services (Imperva, AppTrana) easier for compliance

## Strengths

1. **Zero Licensing Cost**
   - Free and open source
   - No vendor lock-in
   - No per-request or per-domain fees

2. **Full Control and Privacy**
   - No third-party traffic proxying
   - Complete rule customization
   - Data stays on your infrastructure

3. **Flexibility and Extensibility**
   - SecLang rule language powerful
   - Custom integrations possible
   - Works with various web servers/proxies

4. **OWASP CRS Quality**
   - Mature, community-maintained ruleset
   - Comprehensive OWASP Top 10 coverage
   - Continuously updated

5. **No Vendor Lock-In**
   - Portable rules (SecLang standard)
   - Switch between ModSecurity and Coraza
   - Integrate with any infrastructure

6. **Coraza Performance**
   - Go-based, better performance than ModSecurity
   - Memory-safe (no C++ vulnerabilities)
   - Active development and community support

## Weaknesses

1. **High Operational Overhead**
   - Requires expertise to deploy and maintain
   - Manual rule updates and tuning
   - False positive management labor-intensive

2. **No Managed Support**
   - No SOC team or 24/7 monitoring
   - Community support only (no SLA)
   - Troubleshooting relies on internal team

3. **Limited DDoS Protection**
   - No network-layer (L3/4) mitigation
   - Application-layer (L7) limited to rules
   - Requires separate DDoS solution

4. **Weak Bot Management**
   - No ML-powered detection
   - No device fingerprinting
   - Significantly behind cloud platforms

5. **Scaling Challenges**
   - Performance overhead on origin servers
   - Distributed rate limiting requires external store
   - Horizontal scaling increases infrastructure complexity

6. **ModSecurity EOL for NGINX**
   - F5 NGINX deprecated ModSecurity (March 2024)
   - Coraza emerging as replacement but newer/less mature
   - Migration effort for existing ModSecurity users

7. **Hidden TCO**
   - Personnel time for deployment and maintenance
   - Opportunity cost vs. managed services
   - Break-even only at high scale or with existing expertise

## Integration Patterns

### NGINX + Coraza
```nginx
load_module modules/ngx_http_coraza_module.so;
http {
    coraza on;
    coraza_rules_file /etc/coraza/crs-setup.conf;
    coraza_rules_file /etc/coraza/rules/*.conf;
}
```

### Apache + ModSecurity
```apache
LoadModule security2_module modules/mod_security2.so
<IfModule security2_module>
    SecRuleEngine On
    Include /etc/modsecurity/crs-setup.conf
    Include /etc/modsecurity/rules/*.conf
</IfModule>
```

### Kubernetes Ingress (Coraza)
- Deploy Coraza-enabled NGINX Ingress Controller
- ConfigMap for rules and configuration
- Centralized policy management

### Envoy + Coraza
- Native Coraza Envoy filter
- WebAssembly (WASM) deployment
- Service mesh integration (Istio)

## Performance Characteristics

**Latency Impact:**
- ModSecurity: 5-20ms typical overhead (depends on ruleset)
- Coraza: 2-10ms typical overhead (better performance)
- Complex rules increase latency
- Body inspection adds significant overhead

**Throughput:**
- Depends on server resources (CPU, memory)
- Coraza more efficient than ModSecurity (Go vs. C++)
- Horizontal scaling possible but adds infrastructure

**Resource Usage:**
- CPU: 10-30% overhead per request (ruleset-dependent)
- Memory: Variable, body buffering can consume significant RAM
- Disk: Logs can grow rapidly

## Compliance and Certifications

**Direct Compliance:** None (software, not service)

**Compliance Support:**
- Can support PCI DSS requirements (WAF component)
- No vendor certifications (burden on your organization)
- Audit logs available for compliance evidence
- Self-attestation required

## Competitive Positioning

**Vs. Cloudflare:**
- ModSecurity/Coraza free (licensing), Cloudflare paid
- Cloudflare far easier to deploy and manage
- Cloudflare better DDoS, bot management, CDN
- ModSecurity/Coraza better for privacy, control, high scale

**Vs. AWS WAF:**
- ModSecurity/Coraza lower cost at very high traffic
- AWS WAF easier to manage, lower operational overhead
- AWS WAF better bot management, integration
- ModSecurity/Coraza works anywhere (not AWS-only)

**Vs. Imperva:**
- Imperva fully managed (no personnel burden), ModSecurity/Coraza self-managed
- Imperva significantly more expensive
- ModSecurity/Coraza better for privacy-sensitive applications
- Imperva far superior for ease of use, SLAs, support

## Recommendation Score

**Security Efficacy:** 3.5/5 (good WAF, weak bot/DDoS)
**Cost Efficiency:** 4.5/5 (free licensing, but hidden personnel costs)
**Feature Completeness:** 3/5 (solid WAF, minimal bot/DDoS)
**Integration Ease:** 2/5 (requires expertise, complex setup)
**Operational Complexity:** 2/5 (high maintenance, manual tuning)
**Vendor Factors:** 3/5 (no vendor support, community-driven)
**Performance:** 3/5 (overhead on origin, Coraza better)
**Compliance:** 2.5/5 (no certifications, self-attestation burden)

**Overall Score: 3.0/5**

## Final Assessment

ModSecurity and Coraza are viable WAF solutions for organizations with strong in-house security expertise and specific requirements around privacy, control, or cost at extreme scale. However, the hidden TCO (personnel time) often makes cloud-managed WAFs more cost-effective for most organizations.

**Best Choice For:** Privacy-sensitive applications (no third-party proxying), organizations with WAF expertise, cost-sensitive high-traffic applications (>1B req/month), custom/niche deployments, multi-application portfolios with centralized security teams.

**Consider Alternatives If:** Lack in-house WAF expertise (cloud WAFs far easier), need rapid deployment (hours vs. minutes), require DDoS protection (separate solution needed), need advanced bot management (cloud platforms vastly superior), or prefer managed services with SLAs (Imperva, AppTrana).

**Confidence Level:** High - open source, transparent, well-documented. Coraza is the future (ModSecurity NGINX EOL), active OWASP community support.
