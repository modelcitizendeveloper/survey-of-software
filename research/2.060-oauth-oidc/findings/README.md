# OAuth 2.0 / OIDC Research Findings

**Purpose**: Practical findings from real-world OIDC implementations, capturing edge cases, gotchas, and patterns not covered in the standard specification.

---

## Overview

This directory contains **findings** - specific technical discoveries made during implementation work. Unlike the main research (S1-S4 discovery), findings are:

- **Implementation-driven**: Discovered while building real systems
- **Specific**: Focus on particular edge cases or patterns
- **Actionable**: Include code examples and recommendations
- **Generic**: Written for any team implementing OIDC (no project-specific details)

---

## Findings Index

### F001: Email Claim Availability Across OIDC Providers

**File**: `F001-email-claim-availability.md`  
**Date**: 2025-12-30  
**Impact**: Critical

**Summary**: Not all OIDC providers share email addresses. The `email` claim is optional per OIDC spec. Applications relying on email as primary identifier must implement fallback strategies.

**Key Insight**: 
- ✅ Google, Microsoft, GitLab: Always provide email
- ⚠️ GitHub, Discord, Apple, Matrix: Conditional email
- ❌ Twitter/X, Reddit, Twitch: Never provide email

**Recommendation**: Use email-first with provider-scoped `sub` fallback for multi-provider support.

**Source**: Factumerit OIDC middleware implementation (Vikunja invite-only registration)

---

## Quick Reference

**File**: `QUICK_REFERENCE.md`

Lookup table for:
- Email claim availability by provider
- Required scopes for email + profile
- Sub claim formats and stability
- Token endpoints and JWKS URIs
- Implementation patterns
- Testing checklist
- Common pitfalls

**Use this when**: Starting a new OIDC integration and need quick answers.

---

## How to Use These Findings

### For New Implementations

1. **Start with QUICK_REFERENCE.md** - Get oriented on provider characteristics
2. **Read relevant findings** - Understand edge cases for your use case
3. **Choose implementation pattern** - Email-only vs multi-identity
4. **Test thoroughly** - Use testing checklist

### For Existing Implementations

1. **Check findings for your providers** - Are you handling edge cases?
2. **Review common pitfalls** - Are you vulnerable?
3. **Consider migration** - Do you need multi-identity support?

### For Research

1. **Findings inform decisions** - Use when evaluating OIDC providers
2. **Findings complement S1-S4** - Practical details vs strategic overview
3. **Findings are shareable** - Generic, no project-specific details

---

## Contributing Findings

When you discover something implementation-worthy:

1. **Create finding file**: `FXXX-descriptive-name.md`
2. **Use finding template**:
   ```markdown
   # Finding XXX: Title
   
   **Date**: YYYY-MM-DD
   **Category**: [Identity Claims | Security | Performance | ...]
   **Impact**: [Critical | High | Medium | Low]
   **Status**: [Validated | Hypothesis | Deprecated]
   
   ## Summary
   One-paragraph summary
   
   ## The Problem
   What issue did you encounter?
   
   ## Analysis
   Why does this happen?
   
   ## Solution
   How to handle it?
   
   ## Code Examples
   Show, don't tell
   
   ## Recommendations
   When to use this pattern
   
   ## References
   Links to specs, docs, discussions
   ```

3. **Update metadata.yaml**: Add finding to index
4. **Update QUICK_REFERENCE.md**: If applicable
5. **Update this README**: Add to findings index

---

## Relationship to Main Research

### Main Research (S1-S4)
- **Location**: `01-discovery/`
- **Purpose**: Strategic evaluation of OIDC as a standard
- **Audience**: Decision-makers, architects
- **Content**: Provider comparisons, adoption recommendations, cost-benefit analysis

### Findings (This Directory)
- **Location**: `findings/`
- **Purpose**: Tactical implementation guidance
- **Audience**: Developers, implementers
- **Content**: Edge cases, code patterns, gotchas

**Example**:
- **S1-S4**: "Should we adopt OIDC? Which providers? What's the migration cost?"
- **Findings**: "How do I handle providers without email? What's the database schema?"

---

## Finding Categories

### Identity Claims
- Email availability (F001)
- Sub claim uniqueness (TODO: F002)
- Email verification trust (TODO: F003)

### Security
- JWT signature verification (TODO)
- CSRF protection patterns (TODO)
- Token storage best practices (TODO)

### Performance
- Token caching strategies (TODO)
- JWKS caching (TODO)
- Connection pooling (TODO)

### Provider-Specific
- Apple's first-login-only email (covered in F001)
- GitHub's conditional email (covered in F001)
- Matrix homeserver variations (covered in F001)

---

## Future Findings

Potential topics for future findings:

- **F002**: Sub claim uniqueness and stability across providers
- **F003**: Email verification and trust levels
- **F004**: Privacy implications of email-based identity
- **F005**: Refresh token rotation patterns
- **F006**: Multi-tenant OIDC architecture
- **F007**: OIDC for mobile apps (PKCE flow)
- **F008**: Handling provider downtime gracefully
- **F009**: Account linking UX patterns
- **F010**: OIDC for CLI tools (device flow)

---

## Changelog

- **2025-12-30**: Created findings directory with F001 (email claim availability) and QUICK_REFERENCE
- **2025-10-11**: Completed main S1-S4 research (see `01-discovery/`)

---

## See Also

- **STANDARD_EXPLAINER.md** - OAuth 2.0 and OIDC fundamentals
- **01-discovery/DISCOVERY_TOC.md** - Main research table of contents
- **applications/factumerit/vikunja-oidc-middleware/** - Implementation that generated F001

---

**Maintained by**: spawn-solutions research team  
**Generic content**: Safe to share publicly (no project-specific details)

