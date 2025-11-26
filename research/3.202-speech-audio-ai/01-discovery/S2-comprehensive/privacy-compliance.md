# Privacy & Compliance Analysis
## Experiment 3.202: Speech & Audio AI Services

**Research Phase**: S2 - Comprehensive Analysis
**Date**: 2025-11-24
**Focus**: Data protection, regulatory compliance, security controls

---

## Overview

This document compares privacy and compliance capabilities across 8 speech/audio AI providers, focusing on certifications (SOC 2, HIPAA, GDPR), data residency, encryption, and privacy features critical for regulated industries.

---

## Compliance Certifications Matrix

| Provider | SOC 2 Type II | HIPAA BAA | GDPR Compliant | ISO 27001 | PCI-DSS | Regional Data Processing |
|----------|---------------|-----------|----------------|-----------|---------|-------------------------|
| **Fireflies** | ✅ | ✅ (Enterprise) | ✅ | ⚠️ Not disclosed | ⚠️ Not disclosed | US (Enterprise: Private storage) |
| **Otter** | ✅ | ⚠️ Safeguards (not BAA) | ✅ | ✅ | ⚠️ Not disclosed | Cloud (not disclosed) |
| **Grain** | ⚠️ Not disclosed | ⚠️ Not disclosed | ⚠️ Not disclosed | ⚠️ Not disclosed | ⚠️ Not disclosed | ⚠️ Not disclosed |
| **Fathom** | ✅ | ✅ | ✅ | ✅ | ⚠️ Not disclosed | US/Canada (AWS) |
| **Whisper API** | ✅ (OpenAI) | ❌ Not for PHI | ⚠️ No EU servers | ⚠️ Not disclosed | ⚠️ Not disclosed | US (OpenAI infrastructure) |
| **AssemblyAI** | ✅ | ✅ | ✅ | ⚠️ Not disclosed | ✅ Level 1 (2025) | US or EU (Dublin) |
| **Deepgram** | ⚠️ Not disclosed | ⚠️ Not disclosed | ⚠️ Not disclosed | ⚠️ Not disclosed | ⚠️ Not disclosed | ⚠️ Not disclosed |
| **Rev AI** | ✅ | ✅ | ✅ | ⚠️ Not disclosed | ✅ | ⚠️ Not disclosed |

**Legend**:
- ✅ = Certified/Available
- ⚠️ = Not publicly disclosed (may be available, contact vendor)
- ❌ = Not available/compliant

**Key Insights**:
1. **Best compliance transparency**: Fathom (SOC 2, HIPAA, GDPR, ISO 27001), AssemblyAI (SOC 2, HIPAA, GDPR, PCI)
2. **HIPAA BAA available**: Fireflies (Enterprise), Fathom, AssemblyAI, Rev AI
3. **EU data processing**: AssemblyAI (Dublin), others not disclosed or US-only
4. **Least transparent**: Grain, Deepgram (limited public compliance docs)

**Sources**: S1 profiles, vendor security pages

---

## HIPAA Compliance Comparison

**Business Associate Agreement (BAA)** = Legal contract required for handling Protected Health Information (PHI)

### Providers with HIPAA BAA

| Provider | BAA Available | Tier Required | Cost Impact | Features |
|----------|---------------|---------------|-------------|----------|
| **Fireflies** | ✅ | Enterprise | Custom pricing | SOC 2, encryption, admin controls |
| **Fathom** | ✅ | All tiers | No additional cost | SOC 2, ISO 27001, strong compliance |
| **AssemblyAI** | ✅ | All tiers | No additional cost | PII redaction, SOC 2, EU processing |
| **Rev AI** | ✅ | All tiers | No additional cost | 96%+ accuracy, SOC 2, PCI |

### Providers Without HIPAA BAA

| Provider | Status | Alternative |
|----------|--------|-------------|
| **Otter** | ⚠️ "HIPAA safeguards" | Not a formal BAA; limited for PHI |
| **Grain** | ⚠️ Not disclosed | Likely not available |
| **Whisper API** | ❌ Not for PHI | OpenAI policy excludes PHI |
| **Deepgram** | ⚠️ Not disclosed | Contact sales for enterprise |

**Use Case Recommendations**:
- **Medical transcription**: Fathom, AssemblyAI, Rev AI (BAA at no extra cost)
- **Healthcare SaaS**: Fireflies Enterprise (if need meeting bot features)
- **Avoid for PHI**: Whisper API (explicitly not HIPAA-compliant), Otter (no BAA)

---

## GDPR Compliance & EU Data Processing

**General Data Protection Regulation** = EU law requiring data protection and privacy

### GDPR Compliance Matrix

| Provider | GDPR Compliant | EU Data Centers | Data Residency Choice | Data Deletion |
|----------|----------------|-----------------|----------------------|---------------|
| **Fireflies** | ✅ | Enterprise only | Enterprise | User-controlled |
| **Otter** | ✅ | ⚠️ Not disclosed | No | Last 25 meetings (Free) |
| **Grain** | ⚠️ Not disclosed | ⚠️ | ⚠️ | ⚠️ |
| **Fathom** | ✅ | US/Canada (AWS) | No | Unlimited storage, user deletes |
| **Whisper API** | ⚠️ No EU servers | No | No | Auto-deleted post-processing |
| **AssemblyAI** | ✅ | **EU (Dublin)** | ✅ US or EU | Configurable |
| **Deepgram** | ⚠️ Not disclosed | ⚠️ | ⚠️ | ⚠️ |
| **Rev AI** | ✅ | ⚠️ Not disclosed | ⚠️ | Configurable (Enterprise) |

**Best for EU Customers**:
1. **AssemblyAI** - Only provider with **explicit EU data processing option** (Dublin)
2. **Fathom** - GDPR compliant, though US/Canada servers
3. **Fireflies** - GDPR compliant, Enterprise can negotiate EU storage

**Concerns**:
- **Whisper API**: No EU servers (data processed in US)
- **Grain, Deepgram**: Limited public GDPR documentation

---

## Data Storage & Retention

### Storage Locations

| Provider | Data Centers | Customer Choice | Encryption at Rest | Encryption in Transit |
|----------|--------------|-----------------|-------------------|----------------------|
| **Fireflies** | US (AWS) | Enterprise: Private storage | ✅ | ✅ TLS |
| **Otter** | Cloud (not disclosed) | No | ⚠️ No E2EE | ✅ TLS |
| **Grain** | ⚠️ Not disclosed | ⚠️ | ⚠️ | ⚠️ Assumed |
| **Fathom** | US/Canada (AWS) | No | ✅ | ✅ |
| **Whisper API** | US (OpenAI) | No | ⚠️ Not disclosed | ✅ HTTPS |
| **AssemblyAI** | US or EU (Dublin) | ✅ | ✅ | ✅ HTTPS/TLS |
| **Deepgram** | ⚠️ Not disclosed | ⚠️ | ⚠️ Assumed | ✅ |
| **Rev AI** | ⚠️ Not disclosed | ⚠️ | ✅ | ✅ |

**Security Concern**: **Otter lacks end-to-end encryption** (E2EE) at rest - potential vulnerability

### Data Retention Policies

| Provider | Free Tier | Paid Tier | Automatic Deletion | User Control |
|----------|-----------|-----------|-------------------|--------------|
| **Fireflies** | 800min/seat | Unlimited (Business+) | Free tier quota | ✅ Manual delete |
| **Otter** | 25 meetings | Extended | Free tier limit | ✅ Manual delete |
| **Grain** | 20 meetings cap | Extended | ⚠️ | ⚠️ |
| **Fathom** | Unlimited | Unlimited | No | ✅ Manual delete |
| **Whisper API** | N/A | N/A | Yes (immediate post-processing) | ✅ User-managed |
| **AssemblyAI** | N/A | N/A | Configurable | ✅ User-managed |
| **Deepgram** | N/A | N/A | ⚠️ | ✅ |
| **Rev AI** | ⚠️ | Configurable (Enterprise) | ⚠️ | ✅ |

**Key Differences**:
- **SaaS platforms**: Store recordings long-term (Fathom unlimited, others tier-dependent)
- **APIs**: Process and discard (Whisper immediate deletion, AssemblyAI configurable)
- **GDPR "Right to be Forgotten"**: All providers support manual deletion; AssemblyAI offers configurable auto-deletion

---

## PII Redaction & Data Protection Features

**Personally Identifiable Information (PII)** = SSN, credit card numbers, names, addresses, etc.

### PII Redaction Capabilities

| Provider | PII Redaction | Automatic Detection | Redaction Types | Use Case |
|----------|---------------|---------------------|----------------|----------|
| **Fireflies** | ❌ | N/A | N/A | Not for PII-sensitive use cases |
| **Otter** | ❌ | N/A | N/A | Not for PII-sensitive |
| **Grain** | ❌ | N/A | N/A | Customer-facing (be cautious) |
| **Fathom** | ❌ | N/A | N/A | Not for PII-sensitive |
| **Whisper API** | ❌ | N/A | N/A | Not for PII-sensitive |
| **AssemblyAI** | ✅ | ✅ Auto | SSN, CC, names, addresses, phone, email | **Best for compliance** |
| **Deepgram** | ❌ | N/A | N/A | Not for PII-sensitive |
| **Rev AI** | ❌ | N/A | N/A | Not for PII-sensitive |

**Critical Finding**: **Only AssemblyAI offers built-in PII redaction** - critical for:
- Call center transcription (customer data protection)
- HIPAA compliance (automatic PHI redaction)
- GDPR compliance (personal data minimization)
- Financial services (PCI-DSS, credit card protection)

**Alternative for Other Providers**:
- Post-processing PII removal (custom code)
- Manual review and redaction (labor-intensive)
- Avoid transcribing PII-sensitive conversations

---

## AI Model Training on Customer Data

**Privacy Concern**: Do providers use customer audio/transcripts to train AI models?

| Provider | Trains on Customer Data | Policy Transparency | Contractual Protection |
|----------|------------------------|---------------------|------------------------|
| **Fireflies** | ❌ No | ✅ Explicit policy | ✅ |
| **Otter** | ❌ No | ✅ "Third-party AI providers cannot train" | ✅ Contractual |
| **Grain** | ⚠️ Not disclosed | ⚠️ | ⚠️ |
| **Fathom** | ❌ No | ✅ **"Never trains on data"** | ✅ Contractual (OpenAI, Anthropic, Google) |
| **Whisper API** | ❌ No | ✅ OpenAI policy | ✅ |
| **AssemblyAI** | ❌ No | ✅ Explicit policy | ✅ |
| **Deepgram** | ⚠️ Not disclosed | ⚠️ | ⚠️ |
| **Rev AI** | ⚠️ Assumed no | ⚠️ Limited disclosure | ⚠️ |

**Best Privacy Policies**:
1. **Fathom**: Contractual guarantee with AI sub-processors (OpenAI, Anthropic, Google)
2. **Whisper API, AssemblyAI**: Explicit no-training policies
3. **Fireflies, Otter**: Clear no-training commitments

**Concerns**:
- **Grain, Deepgram, Rev AI**: Limited public documentation on training policies

---

## Access Controls & Authentication

### Enterprise Security Features

| Provider | SSO (Single Sign-On) | 2FA | RBAC (Role-Based Access) | Admin Console | Audit Logs |
|----------|---------------------|-----|--------------------------|---------------|-----------|
| **Fireflies** | ✅ Enterprise | ⚠️ Not disclosed | ✅ Business+ | ✅ Business+ | ⚠️ |
| **Otter** | ⚠️ Not disclosed | ✅ | ⚠️ | ✅ Business+ | ⚠️ |
| **Grain** | ✅ Enterprise | ⚠️ | ✅ Enterprise | ✅ Enterprise | ⚠️ |
| **Fathom** | ⚠️ Not disclosed | ✅ | ⚠️ | ✅ Pro+ | ⚠️ |
| **Whisper API** | N/A (API) | ✅ OpenAI account | N/A | N/A | ⚠️ OpenAI dashboard |
| **AssemblyAI** | ✅ Enterprise | ⚠️ Not disclosed | ✅ Enterprise | ⚠️ | ⚠️ |
| **Deepgram** | ⚠️ Not disclosed | ⚠️ | ⚠️ | ⚠️ | ⚠️ |
| **Rev AI** | ⚠️ Not disclosed | ⚠️ | ⚠️ | ⚠️ | ⚠️ |

**Enterprise-Ready**:
- **Fireflies, Grain, AssemblyAI**: SSO + RBAC + Admin controls (Enterprise tier)
- **Otter, Fathom**: 2FA + Admin console (Business/Pro tier)

**API-Based**: APIs (Whisper, AssemblyAI, Deepgram, Rev AI) rely on API key management (developer responsibility)

---

## Compliance Comparison by Industry

### Healthcare / Medical

**Requirements**: HIPAA BAA, SOC 2, PII redaction, encryption

| Provider | Suitable | Strengths | Limitations |
|----------|----------|-----------|-------------|
| **Fathom** | ✅ Excellent | HIPAA BAA (all tiers), SOC 2, ISO 27001, no extra cost | No PII redaction (manual review needed) |
| **AssemblyAI** | ✅ Excellent | HIPAA BAA, **PII redaction**, SOC 2, EU processing | API build required (no meeting bot) |
| **Rev AI** | ✅ Excellent | HIPAA BAA, 96%+ accuracy, SOC 2, PCI | No PII redaction |
| **Fireflies** | ⚠️ Enterprise only | HIPAA BAA (Enterprise tier), SOC 2 | High cost (Enterprise pricing), no PII redaction |
| **Otter** | ❌ Not suitable | No BAA (only "safeguards"), no E2EE | Privacy concerns |
| **Whisper API** | ❌ Not suitable | Explicitly not HIPAA-compliant | Cannot use for PHI |

**Recommendation**: AssemblyAI (best PII protection) or Fathom (best SaaS option) for medical transcription

---

### Legal / Law Firms

**Requirements**: SOC 2, high accuracy, data retention control, confidentiality

| Provider | Suitable | Strengths | Limitations |
|----------|----------|-----------|-------------|
| **Rev AI** | ✅ Excellent | 96%+ accuracy, SOC 2, PCI, GDPR, hybrid AI+human | Higher cost ($0.035/min) |
| **Fathom** | ✅ Good | SOC 2, ISO 27001, GDPR, unlimited storage | 95% accuracy (may need review) |
| **Fireflies** | ✅ Good | SOC 2, GDPR, unlimited storage (Business+) | Enterprise tier for highest security |
| **AssemblyAI** | ✅ Good | SOC 2, PII redaction, GDPR, EU processing | API build required |

**Recommendation**: Rev AI (highest accuracy + human backstop) or Fathom (cost-effective SaaS)

---

### Financial Services

**Requirements**: SOC 2, PCI-DSS, PII redaction, audit logs

| Provider | Suitable | Strengths | Limitations |
|----------|----------|-----------|-------------|
| **AssemblyAI** | ✅ Excellent | SOC 2, **PCI Level 1 (2025)**, **PII redaction** | API build required |
| **Rev AI** | ✅ Excellent | SOC 2, PCI, GDPR, high accuracy | No PII redaction |
| **Fireflies** | ⚠️ Enterprise only | SOC 2, Enterprise tier may support PCI (verify) | No PII redaction |

**Recommendation**: AssemblyAI (only provider with PCI + PII redaction)

---

### General Business / SaaS

**Requirements**: SOC 2, GDPR (if EU customers), reasonable security

| Provider | Suitable | Strengths | Limitations |
|----------|----------|-----------|-------------|
| **Fathom** | ✅ Excellent | SOC 2, ISO 27001, GDPR, free tier | Limited advanced features |
| **Fireflies** | ✅ Good | SOC 2, GDPR, extensive features | Business tier for CRM |
| **Otter** | ✅ Good | SOC 2, ISO 27001, GDPR | No E2EE, limited CRM |
| **Grain** | ⚠️ Limited transparency | Good for HubSpot users | Compliance docs not public |

**Recommendation**: Fathom (best free option) or Fireflies (feature-rich)

---

## Summary: Compliance Rankings

### Best Overall Compliance
1. **AssemblyAI** - SOC 2, HIPAA BAA, GDPR, PCI Level 1, **PII redaction**, EU processing
2. **Fathom** - SOC 2, HIPAA BAA, GDPR, ISO 27001 (most transparent SaaS)
3. **Rev AI** - SOC 2, HIPAA BAA, GDPR, PCI (highest accuracy)
4. **Fireflies** - SOC 2, HIPAA (Enterprise), GDPR

### Best for Regulated Industries
- **Healthcare**: AssemblyAI (PII redaction) > Fathom (HIPAA BAA at no cost)
- **Legal**: Rev AI (accuracy) > Fathom (cost-effective)
- **Financial**: AssemblyAI (PCI + PII redaction) > Rev AI (PCI)

### Least Transparent
1. **Grain** - Limited public compliance docs (verify with sales)
2. **Deepgram** - Limited public compliance docs
3. **Otter** - No HIPAA BAA, no E2EE

### Best Privacy Practices
1. **Fathom** - Contractual no-training guarantees, strong certifications
2. **AssemblyAI** - PII redaction, EU processing, transparent policies
3. **Whisper API** - No training, immediate data deletion

---

## Key Findings

1. **AssemblyAI only provider with PII redaction** - critical for call centers, healthcare, finance
2. **Fathom best SaaS compliance** - SOC 2, HIPAA, ISO 27001, GDPR at all tiers (no extra cost)
3. **Otter lacks HIPAA BAA and E2EE** - not suitable for sensitive data
4. **Grain, Deepgram least transparent** - limited public compliance documentation
5. **AssemblyAI only EU data processing option** - best for GDPR compliance
6. **HIPAA BAA available**: Fireflies (Enterprise), Fathom, AssemblyAI, Rev AI
7. **No SaaS platform offers PII redaction** - only AssemblyAI API

---

## Data Sources

- S1 provider profiles
- Vendor security pages (security.fireflies.ai, otter.ai/security, fathom.video/security, etc.)
- [AssemblyAI Benchmarks](https://www.assemblyai.com/benchmarks)
- Compliance certification listings (SOC 2, HIPAA, GDPR, ISO 27001)

---

**Last Updated**: 2025-11-24
**Next Document**: synthesis.md (cross-cutting insights and decision framework)
