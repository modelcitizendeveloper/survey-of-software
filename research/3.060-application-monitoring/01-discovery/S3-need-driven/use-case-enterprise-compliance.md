# Use Case: Enterprise with Compliance Requirements
## SOC2, HIPAA, FedRAMP Application Monitoring

**Pattern**: Enterprise B2B SaaS with regulatory compliance
**Stack**: Any production-grade stack, multi-region deployment
**Example**: Healthcare SaaS, financial services, government contractors

---

## Scenario Description

### Who This Is For

- B2B SaaS companies pursuing SOC2 Type II
- Healthcare applications handling PHI (HIPAA)
- Financial services with PCI-DSS requirements
- Government contractors needing FedRAMP
- Enterprise software with customer compliance obligations

### Typical Requirements

- SOC2 Type II audit preparation
- HIPAA compliance for healthcare data
- PCI-DSS for payment processing
- FedRAMP for government contracts
- GDPR for European customers
- ISO 27001 certification

### Pain Points to Solve

1. Need audit-ready error monitoring (SOC2 control evidence)
2. Cannot send PHI/PII to third-party SaaS (HIPAA)
3. Customer security questionnaires ask about monitoring
4. Need BAA (Business Associate Agreement) from vendors
5. Must demonstrate incident detection and response
6. Penetration tests flag lack of monitoring
7. Compliance frameworks require security logging

---

## Requirements Profile

### Must-Have Features

- **SOC2/ISO 27001 certified vendor** (for trust reports)
- **BAA available** (for HIPAA compliance)
- **SSO/SAML** (centralized access control)
- **RBAC** (role-based access control)
- **Audit logs** (who accessed what error data)
- **Data residency** (EU/US regions for GDPR)
- **Encryption at rest and in transit** (AES-256, TLS 1.3)
- **Data retention controls** (configurable purging)
- **PII scrubbing** (automatic removal of sensitive data)

### Nice-to-Have Features

- On-premise deployment option (air-gapped environments)
- SCIM provisioning (automated user management)
- Advanced threat detection (anomaly detection)
- Compliance reporting (pre-built audit reports)
- Integration with SIEM (Splunk, QRadar)
- Custom SLA guarantees (99.9%+ uptime)

### Budget Reality

- Small enterprise (50-200 employees): $500-2,000/month
- Mid-market (200-1,000 employees): $2,000-10,000/month
- Large enterprise (1,000+ employees): $10,000-50,000/month

### Compliance Checklist

**SOC2 Type II:**
- CC6.1: Logical access controls (SSO, RBAC)
- CC6.6: Vulnerability management (monitoring)
- CC6.7: Infrastructure monitoring
- CC7.2: System monitoring (error detection)

**HIPAA:**
- §164.308(a)(1)(ii)(D): Information system activity review
- §164.312(a)(1): Access controls (SSO, RBAC)
- §164.312(e)(1): Transmission security (encryption)
- BAA required for vendors processing PHI

**PCI-DSS:**
- Requirement 10: Track and monitor all access to network resources
- Requirement 11: Regularly test security systems

---

## Provider Fit Analysis

### Datadog (Score: 98/100)

**Compliance Certifications:**
- SOC2 Type II ✓
- ISO 27001 ✓
- HIPAA (with BAA) ✓
- PCI-DSS Level 1 ✓
- FedRAMP Authorized (Moderate) ✓
- GDPR compliant ✓

**Enterprise Features:**
- SSO/SAML (Okta, Azure AD, Google)
- RBAC with granular permissions
- Audit logs (all user actions tracked)
- Data residency (US, EU, AP regions)
- PII scrubbing (automatic text patterns)
- Custom data retention (14-365+ days)
- SCIM provisioning
- BAA available on Enterprise plan

**Pricing for Compliance:**
- Enterprise: Custom pricing (typically $1,500-5,000/month minimum)
- Includes: APM, Infrastructure, Logs, SIEM, Security Monitoring
- BAA: No additional cost

**TCO (12 months):**
- Small enterprise: $18,000-36,000/year
- Mid-market: $60,000-120,000/year
- Large enterprise: $120,000-600,000/year

**Integration Effort:** 40 hours (full deployment + compliance documentation)

**Audit Readiness:** Excellent (Datadog provides SOC2 report for auditors)

### New Relic (Score: 96/100)

**Compliance Certifications:**
- SOC2 Type II ✓
- ISO 27001 ✓
- HIPAA (with BAA) ✓
- PCI-DSS ✓
- FedRAMP Authorized (Moderate) ✓
- GDPR compliant ✓

**Enterprise Features:**
- SSO/SAML
- RBAC with custom roles
- Audit logs
- Data residency (US, EU)
- PII obfuscation (drop filter rules)
- Compliance dashboard (pre-built)
- SCIM provisioning
- BAA available (no additional cost)

**Pricing for Compliance:**
- Enterprise: Custom (typically $1,000-4,000/month)
- Full Platform license (unlimited features)
- Data Plus add-on for extended retention

**TCO (12 months):**
- Small enterprise: $12,000-30,000/year
- Mid-market: $48,000-100,000/year
- Large enterprise: $100,000-500,000/year

**Integration Effort:** 30 hours (deployment + compliance setup)

**Audit Readiness:** Excellent (provides compliance documentation)

### Sentry (Score: 90/100)

**Compliance Certifications:**
- SOC2 Type II ✓
- GDPR compliant ✓
- HIPAA (BAA available on Enterprise) ✓
- ISO 27001 (in progress) ⚠️
- FedRAMP: Not authorized ✗

**Enterprise Features:**
- SSO/SAML
- RBAC
- Audit logs (on Enterprise)
- Data residency (US, EU via self-hosted)
- PII scrubbing (beforeSend hooks)
- Custom data retention
- SCIM provisioning (Enterprise)
- BAA available

**Pricing for Compliance:**
- Enterprise: Custom (typically $500-2,000/month)
- Self-hosted option available (HIPAA preferred)

**TCO (12 months):**
- Small enterprise: $6,000-24,000/year
- Mid-market: $24,000-60,000/year
- Self-hosted: $10,000-30,000/year (infra + maintenance)

**Integration Effort:** 20 hours (SaaS) or 60 hours (self-hosted)

**Audit Readiness:** Good (provides SOC2 report, BAA template)

### Splunk (Score: 95/100)

**Compliance Certifications:**
- SOC2 Type II ✓
- ISO 27001 ✓
- HIPAA (with BAA) ✓
- PCI-DSS ✓
- FedRAMP High ✓ (highest authorization)
- GDPR compliant ✓

**Enterprise Features:**
- Comprehensive SIEM capabilities
- Advanced RBAC
- Full audit trail
- On-premise or cloud
- Unlimited data retention (self-hosted)
- Machine learning for anomaly detection
- Pre-built compliance dashboards
- BAA included

**Pricing for Compliance:**
- Cloud: $150/GB ingested (expensive!)
- On-premise: $2,000-10,000+ per indexer
- Typical: $3,000-15,000/month

**TCO (12 months):**
- Small enterprise: $36,000-100,000/year
- Mid-market: $100,000-300,000/year
- Large enterprise: $300,000-2,000,000/year

**Integration Effort:** 80 hours (complex deployment)

**Audit Readiness:** Best-in-class (designed for compliance)

### Honeybadger (Score: 75/100)

**Compliance Certifications:**
- GDPR compliant ✓
- SOC2: Not certified ✗
- HIPAA: No BAA available ✗

**Enterprise Features:**
- SSO/SAML (on larger plans)
- Basic RBAC
- Privacy-focused (minimal data collection)
- EU hosting option
- PII scrubbing tools

**Pricing for Compliance:**
- Large: $199/month (limited enterprise features)
- Custom: Contact for SSO/compliance needs

**TCO (12 months):**
- Small enterprise: $2,388/year (Limited compliance)

**Integration Effort:** 10 hours

**Audit Readiness:** Poor (no SOC2, no BAA)

### Self-Hosted: Sentry On-Premise (Score: 92/100)

**Compliance Benefits:**
- Full data control (PHI never leaves your infrastructure)
- No BAA needed (you're the sole processor)
- Custom retention (keep data forever or purge immediately)
- Air-gapped deployment (government/military)
- Audit logs under your control

**Challenges:**
- You must maintain SOC2/HIPAA controls
- DevOps burden (updates, scaling, backup)
- Uptime responsibility
- Need dedicated team

**Pricing:**
- Software: Free (open source)
- Infrastructure: $500-3,000/month (k8s, database, object storage)
- Labor: 1-2 FTE DevOps engineers

**TCO (12 months):**
- Infrastructure: $6,000-36,000/year
- Labor: $150,000-300,000/year (2 engineers)
- **Total: $156,000-336,000/year**

**Integration Effort:** 120 hours (initial deployment + hardening)

**Audit Readiness:** Full control (you build compliance documentation)

---

## Recommendation

### Top Choice: Datadog (98/100)

**Why Datadog wins for enterprise compliance:**
1. **FedRAMP High** - Highest government authorization (vs Moderate for others)
2. **Comprehensive compliance** - SOC2, HIPAA, PCI, ISO, GDPR all covered
3. **Unified platform** - Errors + APM + logs + SIEM (single vendor for auditors)
4. **BAA included** - No additional cost on Enterprise
5. **Proven at scale** - Trusted by Fortune 500 healthcare/financial firms

**When to choose Datadog:**
- Need FedRAMP (government contracts)
- Want unified observability + security platform
- Budget allows $1,500-5,000/month
- Multi-cloud or Kubernetes infrastructure
- Prefer established, low-risk vendor

**Migration Path:**
- Start: Enterprise trial (POC with compliance review)
- Month 1-3: Deploy APM + Infrastructure monitoring
- Month 3-6: Add Security Monitoring (SIEM)
- Ongoing: Annual SOC2 audit (Datadog provides reports)

### Runner-Up: New Relic (96/100)

**When to choose New Relic:**
- Need lower cost than Datadog ($1K vs $1.5K+ per month)
- Want all-inclusive pricing (simpler budgeting)
- Don't need FedRAMP High (Moderate is sufficient)
- Prefer consumption-based over host-based pricing

**Trade-offs vs Datadog:**
- 20-30% cheaper at similar scale
- Slightly less mature SIEM features
- FedRAMP Moderate (not High)
- Better for mid-market than Fortune 500

### Budget Alternative: Sentry Enterprise (90/100)

**When to choose Sentry:**
- Need SOC2 + HIPAA but not FedRAMP
- Budget-constrained ($500-1K/month vs $1.5K-5K)
- Focus on error tracking, not full observability
- Willing to use self-hosted for maximum compliance

**Trade-offs vs Datadog:**
- 50-70% cheaper
- Less comprehensive (errors + APM only, no SIEM)
- No FedRAMP authorization
- Self-hosted option for HIPAA-strict environments

### Maximum Control: Sentry Self-Hosted (92/100)

**When to choose self-hosted:**
- HIPAA-strict environment (no PHI to third parties)
- Government/military (air-gapped network)
- Unlimited data retention requirements
- Have in-house DevOps team (2+ engineers)

**Trade-offs:**
- Higher total cost ($150K+/year with labor)
- You own uptime and maintenance
- Full compliance control
- No vendor dependency

---

## Cost Comparison: 12-Month TCO

### Small Enterprise (50-200 employees, 30 services)
- **Datadog**: $18,000-36,000/year (Enterprise + SIEM)
- **New Relic**: $12,000-30,000/year (Enterprise)
- **Sentry**: $6,000-24,000/year (Enterprise SaaS)
- **Splunk**: $36,000-100,000/year (Cloud or on-prem)
- **Sentry Self-Hosted**: $156,000/year (infra + 2 FTE)
- **Honeybadger**: $2,388/year (NOT compliant - missing SOC2/BAA)

**Winner: Sentry Enterprise ($6K-24K), but Datadog worth premium for FedRAMP/full compliance**

### Mid-Market (200-1,000 employees, 100+ services)
- **Datadog**: $60,000-120,000/year
- **New Relic**: $48,000-100,000/year
- **Sentry**: $24,000-60,000/year
- **Splunk**: $100,000-300,000/year
- **Sentry Self-Hosted**: $180,000-250,000/year

**Winner: New Relic ($48K-100K) for best value at scale**

### Large Enterprise (1,000+ employees, 500+ services)
- **Datadog**: $120,000-600,000/year
- **New Relic**: $100,000-500,000/year
- **Sentry**: Not ideal (scale limits)
- **Splunk**: $300,000-2,000,000/year
- **Sentry Self-Hosted**: $200,000-400,000/year

**Winner: New Relic ($100K-500K), Datadog if need FedRAMP High**

---

## Compliance Feature Matrix

| Feature | Datadog | New Relic | Sentry Ent | Splunk | Sentry Self |
|---------|---------|-----------|------------|---------|-------------|
| SOC2 Type II | ✓ | ✓ | ✓ | ✓ | You maintain |
| ISO 27001 | ✓ | ✓ | In progress | ✓ | You maintain |
| HIPAA BAA | ✓ | ✓ | ✓ | ✓ | Not needed |
| PCI-DSS | ✓ | ✓ | ✗ | ✓ | You maintain |
| FedRAMP High | ✓ | ✗ (Moderate) | ✗ | ✓ | N/A |
| GDPR | ✓ | ✓ | ✓ | ✓ | ✓ |
| SSO/SAML | ✓ | ✓ | ✓ | ✓ | ✓ (setup req) |
| SCIM | ✓ | ✓ | ✓ | ✓ | ✓ (setup req) |
| Audit Logs | ✓ | ✓ | ✓ | ✓ | ✓ |
| Data Residency | US/EU/AP | US/EU | US/EU | Any | Full control |
| PII Scrubbing | Auto | Manual | Manual | Manual | Full control |

---

## Implementation Guide

### Datadog Enterprise Setup (Recommended)

**Phase 1: Compliance Review (Week 1-2)**
```
1. Request Datadog SOC2 report from account manager
2. Review BAA template with legal team
3. Configure data residency (US vs EU)
4. Set up SSO with Okta/Azure AD
```

**Phase 2: Deployment (Week 3-6)**
```
5. Deploy Datadog agents on all hosts
6. Configure APM on critical services
7. Set up log collection (with PII scrubbing)
8. Create RBAC roles (admin, developer, auditor)
```

**Phase 3: Compliance Configuration (Week 7-8)**
```
9. Enable audit logs
10. Configure data retention per compliance needs
11. Set up compliance dashboard
12. Create alert rules for security events
13. Document monitoring controls for SOC2 audit
```

**Phase 4: Audit Preparation (Ongoing)**
```
14. Export audit logs monthly
15. Review access controls quarterly
16. Update runbooks for incident response
17. Provide Datadog SOC2 report to auditors
```

**Time to production:** 8 weeks
**Time to audit-ready:** 12 weeks

### PII Scrubbing Configuration

**Datadog automatic scrubbing:**
```yaml
logs_config:
  logs_no_ssl: false
  processing_rules:
    - type: mask_sequences
      name: mask_credit_cards
      pattern: \d{4}-\d{4}-\d{4}-\d{4}
      replace_placeholder: "[credit_card_redacted]"

    - type: mask_sequences
      name: mask_ssn
      pattern: \d{3}-\d{2}-\d{4}
      replace_placeholder: "[ssn_redacted]"

    - type: mask_sequences
      name: mask_email
      pattern: \b[\w._%+-]+@[\w.-]+\.[A-Z]{2,}\b
      replace_placeholder: "[email_redacted]"
```

**Sentry beforeSend hook:**
```python
def before_send(event, hint):
    # Remove sensitive fields
    if event.get('request'):
        event['request'].pop('cookies', None)
        event['request'].pop('headers', None)

    # Scrub exception messages
    if event.get('exception'):
        for exc in event['exception']['values']:
            exc['value'] = re.sub(
                r'\b[\w._%+-]+@[\w.-]+\.[A-Z]{2,}\b',
                '[email]',
                exc['value'],
                flags=re.IGNORECASE
            )

    return event

sentry_sdk.init(
    dsn="...",
    before_send=before_send,
)
```

---

## Audit Documentation Template

### SOC2 Control Evidence (Example)

**CC7.2 - System Monitoring**

*Control Description:* The organization monitors its systems to identify anomalies, performance issues, and security incidents.

*Implementation:* We use Datadog for comprehensive application monitoring:
- Error tracking across all production services
- APM for performance monitoring (p95 latency < 500ms)
- Log aggregation with 90-day retention
- Real-time alerting via PagerDuty

*Evidence:*
1. Datadog SOC2 Type II report (Appendix A)
2. Screenshot of monitoring dashboard (Appendix B)
3. Alert configuration export (Appendix C)
4. Incident response runbook (Appendix D)
5. Audit log showing 90-day error history (Appendix E)

**HIPAA §164.308(a)(1)(ii)(D) - Information System Activity Review**

*Requirement:* Implement procedures to regularly review records of information system activity.

*Implementation:*
- All application errors logged to Datadog
- Weekly review of error trends by engineering team
- Monthly security review of audit logs
- Automated alerts for anomalous error rates

*Evidence:*
1. Datadog BAA (signed) (Appendix F)
2. Weekly error review meeting notes (Appendix G)
3. Audit log access report (Appendix H)

---

## Key Takeaways

1. **Datadog for FedRAMP/government** - Only option with FedRAMP High authorization
2. **New Relic for mid-market B2B** - 20-30% cheaper, SOC2 + HIPAA covered
3. **Sentry for budget compliance** - 50-70% cheaper, good for SOC2 only
4. **Self-host for HIPAA-strict** - No PHI to third parties, but $150K+/year cost
5. **BAA is non-negotiable for HIPAA** - Must have signed agreement before going live
6. **Budget $1,000-5,000/month** - Enterprise compliance monitoring is not cheap
7. **Plan 8-12 weeks for deployment** - Compliance setup takes longer than technical setup
