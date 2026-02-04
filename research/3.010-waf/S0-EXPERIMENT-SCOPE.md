# S0: Experiment Scoping - Web Application Firewall (WAF)

**Experiment ID:** 3.010-waf
**Category:** Security Infrastructure
**Created:** October 11, 2025
**Status:** Scoping Complete → Ready for S1

---

## Challenge Definition

Modern web applications face constant security threats: DDoS attacks, bot traffic, SQL injection, credential stuffing, and malicious payloads. Developers need to decide between:

1. **Infrastructure-level security** (Cloudflare, AWS WAF, etc.)
2. **Application-level security** (code-based validation, middleware)
3. **Hybrid approaches** (infrastructure + application)

**Core Question:** What WAF and security solutions exist, and when should you choose infrastructure vs application-level protection?

---

## Experiment Scope

### **In Scope**
- Web Application Firewalls (WAF) - managed and self-hosted
- DDoS protection services
- Bot management and mitigation
- Rate limiting solutions
- IP allowlisting/denylisting
- Geographic blocking
- Infrastructure-level vs application-level security tradeoffs

### **Out of Scope**
- Authentication/authorization services (covered in 2.012)
- Secrets management (covered in 3.011)
- Network-level firewalls (outside web application scope)
- Compliance/audit services (covered in 3.092)
- Code security analysis (SAST/DAST)

---

## Key Discovery Questions

### S1: Rapid Library Search
- What are the major WAF providers? (Cloudflare, AWS WAF, Akamai, etc.)
- Which solutions are most commonly used?
- What's the "default choice" for startups vs enterprises?

### S2: Comprehensive Solution Analysis
- Full landscape: managed services vs self-hosted vs hybrid
- Feature comparison: DDoS, bot management, rate limiting, custom rules
- Pricing models: free tiers, per-request, flat monthly, enterprise
- Integration patterns: DNS-based, reverse proxy, CDN, API gateway

### S3: Need-Driven Discovery
- **Use case:** Webhook endpoint security (IP allowlisting, rate limiting)
- **Use case:** Public API protection (bot management, DDoS)
- **Use case:** Enterprise web app (compliance, custom rules)
- **Use case:** High-traffic content site (CDN + security)
- Requirements-to-solution matching framework

### S4: Strategic Selection
- **Decision tree:** When to use infrastructure vs application security?
- **Trade-offs:** Configuration speed vs control, cost vs features
- **Migration paths:** Starting simple, scaling to enterprise
- **Integration patterns:** How WAF fits with CDN, DNS, PaaS
- Future-proofing: vendor lock-in, multi-cloud strategies

---

## Expected Outcomes

### Deliverables
1. **S1:** Quick reference list of top 10-15 WAF solutions
2. **S2:** Comprehensive provider catalog with features/pricing
3. **S3:** Use case → solution matching guide
4. **S4:** Strategic decision framework with clear selection criteria
5. **SYNTHESIS:** Executive summary with decision tree

### Key Decision Framework
The critical output is a decision tree answering:

```
SCENARIO: I need to protect a web application/API

QUESTION 1: Do I need immediate protection (hours) or custom controls (weeks)?
→ Immediate: Infrastructure-level (Cloudflare, AWS WAF)
→ Custom: Consider application-level or hybrid

QUESTION 2: What's my traffic profile?
→ Low traffic (<1M requests/month): Look for free tiers
→ Medium traffic: Evaluate per-request pricing
→ High traffic: Negotiate enterprise contracts

QUESTION 3: What threats am I protecting against?
→ DDoS/bots: Infrastructure-level WAF (best protection)
→ Business logic attacks: Application-level validation
→ Both: Hybrid approach

QUESTION 4: What's my integration complexity?
→ DNS/CDN already exists: Leverage existing provider (Cloudflare, Akamai)
→ Greenfield: Choose based on features
→ Multi-region: Consider cloud-native WAF (AWS, GCP, Azure)
```

---

## Success Criteria

**S0 is complete when:**
- ✅ Challenge clearly defined (WAF landscape + decision framework)
- ✅ Scope boundaries set (what's in/out)
- ✅ Discovery questions articulated for S1-S4
- ✅ Expected outcomes and deliverables defined
- ✅ Ready to begin S1 rapid search

**Experiment is complete when:**
- Developer can quickly identify top WAF solutions (S1)
- Developer can compare features/pricing across landscape (S2)
- Developer can match requirements to solutions (S3)
- Developer can make strategic choice with confidence (S4)
- Decision tree enables 5-minute vs 5-week security tradeoff analysis

---

## Context Notes

### Why This Experiment Matters

**Real-world insight:** Infrastructure-level security (Cloudflare WAF rules) can be configured in 5 minutes, while implementing equivalent application-level security could take hours or days of development.

**Cost of wrong choice:**
- Choose application-level when infrastructure works → Wasted development time
- Choose infrastructure-level when custom logic needed → Security gaps

**Ideal outcome:** Clear decision framework that saves development time and improves security posture.

---

## Experiment Methodology

Following MPSE_V2 framework:
- **S0:** ✅ Scoping (this document)
- **S1:** Rapid search (30 min - identify top providers)
- **S2:** Comprehensive analysis (2-3 hours - full landscape)
- **S3:** Need-driven discovery (1-2 hours - use case matching)
- **S4:** Strategic selection (1 hour - decision framework)
- **SYNTHESIS:** Executive summary (30 min - consolidate findings)

**Total estimated time:** 5-7 hours of focused research

---

**Status:** S0 Complete - Ready for S1
**Next Step:** Begin S1 rapid library search
**Key Focus:** Infrastructure vs application security decision framework
