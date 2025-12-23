# Synapse Platform Documentation

**Last Updated**: 2025-12-23
**Status**: Phase 1 Deployed (verification pending)

---

## Overview

Documentation for `matrix.factumerit.app` - a self-hosted Matrix homeserver (Synapse + MAS) serving as a unified platform for multiple bot services and applications.

**Current Architecture**:
```
Vikunja → Authentik → MAS (patched) → Synapse
```

**Potential Simplified Architecture** (testing pending):
```
Vikunja → MAS (patched) → Synapse
```

---

## Documentation Index

### Strategic Planning

**[01-PLATFORM_VISION.md](./01-PLATFORM_VISION.md)**
- Multi-project bot platform vision
- Bot identity strategy (`@tasks:`, `@research:`, etc.)
- Architecture options (single bot vs multiple specialists)
- Cost model and implementation phases
- **Status**: Phase 1 deployed, Phase 2+ planned

**[02-SYNAPSE_CAPABILITIES.md](./02-SYNAPSE_CAPABILITIES.md)**
- Why Synapse over Dendrite (MAS requirement)
- Capabilities unlocked: OIDC, Admin API, App Services, Federation
- Resource trade-offs (RAM, startup time)
- Roadmap with checkboxes
- **Status**: Foundation deployed, enhanced features pending

---

### Operational Guides

**[03-DEPLOYMENT_LESSONS.md](./03-DEPLOYMENT_LESSONS.md)**
- Battle-tested deployment knowledge
- Critical nginx routes for MAS
- Render-specific issues (TLS, ports, PostgreSQL)
- MAS email claims bug and patch
- OIDC client setup examples
- Debugging checklist
- **Status**: Current, updated with MAS patch lessons

**[04-SECURITY_MODEL.md](./04-SECURITY_MODEL.md)**
- Authentication layers (MAS, bot authorization)
- Authorization patterns (public, private, admin bots)
- Rate limiting strategy
- Data access control (per-user isolation)
- Secrets management
- Audit logging
- **Status**: Draft, to be refined as bots are deployed

**[05-MONITORING_RUNBOOK.md](./05-MONITORING_RUNBOOK.md)**
- Health check endpoints for all services
- Key metrics and alert thresholds
- Common issues and troubleshooting
- Backup and recovery procedures
- Maintenance windows
- **Status**: Draft, alerting not yet implemented

---

### User-Facing

**[06-USER_ONBOARDING.md](./06-USER_ONBOARDING.md)**
- How to get a Matrix account
- Choosing and setting up a Matrix client
- First interaction with bots
- Connecting Vikunja account
- Common first-time issues
- Bot command reference
- Privacy and data retention
- **Status**: Draft, will update as user base grows

---

## Quick Links

### Live Services

- **Matrix homeserver**: https://matrix.factumerit.app
- **Vikunja**: https://vikunja.factumerit.app
- **Authentik**: https://auth.factumerit.app

### Related Documentation

- **Factumerit analysis**: [../factumerit/](../factumerit/) - Vikunja bot architecture
- **Architecture simplification**: [../factumerit/30-ARCHITECTURE-SIMPLIFICATION-OPPORTUNITY.md](../factumerit/30-ARCHITECTURE-SIMPLIFICATION-OPPORTUNITY.md)
- **ADRs**: `development/projects/impl-1131-vikunja/vikunja-mcp/docs/adr/`
  - ADR-019: Matrix Platform Pivot
  - ADR-020: Shared PostgreSQL Strategy
  - ADR-021: Synapse over Dendrite
  - ADR-022: Authentik as IdP Bridge
  - ADR-024: Patch MAS for Email Claims

### Issue Tracking

- **Beads prefix**: `solutions-`
- **Key issues**:
  - `solutions-55jz` - MAS email bug fix (CLOSED)
  - `solutions-hfes` - Test direct Vikunja → MAS connection (OPEN)
  - `solutions-fxwe` - Phase 1.0b: Configure Vikunja OIDC (OPEN)
  - `solutions-2d37` - Monitor upstream MAS issue (OPEN)

---

## Current Status (2025-12-23)

### ✅ Completed

- [x] Synapse + MAS deployed to Render
- [x] PostgreSQL shared database configured
- [x] MAS email claims bug identified and patched
- [x] Authentik deployed as IdP bridge
- [x] Vikunja OIDC configured (via Authentik)
- [x] Documentation suite created

### 🔄 In Progress

- [ ] Verify MAS patch returns email claims
- [ ] Test Vikunja login end-to-end
- [ ] Test direct Vikunja → MAS connection
- [ ] Monitor upstream MAS issue #5374

### 📋 Planned

- [ ] Deploy first bot service (`@tasks:factumerit.app`)
- [ ] Implement rate limiting
- [ ] Set up monitoring and alerting
- [ ] Add research bot (`@research:factumerit.app`)
- [ ] Enable federation to matrix.org

---

## Cost Summary

| Component | Plan | Monthly |
|-----------|------|---------|
| factumerit-matrix (Synapse+MAS patched) | Starter 512MB | $7 |
| factumerit-db (PostgreSQL) | Basic 256MB | $7 |
| factumerit-authentik (IdP bridge) | Standard 2GB | $25 |
| vikunja-factumerit | Starter 512MB | $7 |
| Render Professional base | - | $19 |
| **Total** | | **$65/mo** |

**Potential savings**: $25/mo if Authentik can be removed (see 30-ARCHITECTURE-SIMPLIFICATION-OPPORTUNITY.md)

---

## Contributing

This documentation is a living resource. Update as you:
- Deploy new features
- Discover new issues
- Learn new lessons
- Onboard new users

**Commit convention**:
```bash
git add analyses/synapse/
git commit -m "Update [doc-name]: [what changed]"
```

**Keep it real**:
- ✅ Document failures and workarounds
- ✅ Mark status clearly (deployed, draft, pending)
- ✅ Update checklists as you progress
- ✅ Capture context while it's hot

---

## Questions?

- **Technical issues**: See [05-MONITORING_RUNBOOK.md](./05-MONITORING_RUNBOOK.md)
- **Security concerns**: See [04-SECURITY_MODEL.md](./04-SECURITY_MODEL.md)
- **User onboarding**: See [06-USER_ONBOARDING.md](./06-USER_ONBOARDING.md)
- **Everything else**: ivan@ivantohelpyou.com

