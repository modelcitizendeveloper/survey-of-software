# TM as Strategic Asset: Governance and Ownership

## TM Ownership Models

### Model 1: Client Owns TM

**Scenario:** Translation agency provides services, client retains TM

**Typical Contract:**
- Agency delivers TMX file at project end
- Client owns all translation assets
- Agency cannot reuse TM for other clients

**Advantages (Client):**
- Full control of language assets
- Vendor independence (can switch agencies)
- TM value accumulates to client

**Advantages (Agency):**
- Clear IP boundaries
- Premium pricing (creating new asset for client)

**Use When:** Long-term client relationships, sensitive content

### Model 2: Agency Owns TM

**Scenario:** Agency retains TM, offers discounts for matches to same client

**Typical Contract:**
- Client receives translated deliverables, not TMX
- Agency leverages TM for efficiency (passes savings as match discounts)
- Client locked into agency (TM not portable)

**Advantages (Agency):**
- Asset accumulation
- Client stickiness
- Cross-client TM leverage (if allowed)

**Disadvantages (Client):**
- Vendor lock-in
- Must renegotiate or pay to obtain TMX

**Use When:** Commodity content, clients prioritize cost over control

### Model 3: Shared TM

**Scenario:** TM jointly owned, both parties can use

**Typical Contract:**
- Agency delivers TMX at project end
- Agency can reuse TM for same client only
- Client can use with other vendors

**Advantages:**
- Balanced incentives
- Client flexibility
- Agency efficiency gains

**Use When:** Partnership model, ongoing relationships

## TM Quality Standards

### Quality Tiers

**Tier 1: Production Quality**
- Human-translated
- Reviewed by second linguist
- QA checks passed
- Suitable for direct reuse

**Tier 2: Reference Quality**
- Human-translated
- Light review only
- Suitable for fuzzy matching, requires review

**Tier 3: MT Post-Edited**
- Machine-translated + human post-edit
- Variable quality
- Use with caution, review required

### Quality Metrics

**Acceptance Criteria:**
- **Accuracy:** <1% mistranslation rate (sampled)
- **Consistency:** Terminology adherence 95%+
- **Completeness:** No empty segments
- **Formatting:** Inline codes preserved

**Measurement:**
- Quarterly TM audits
- Sample 500 random segments
- Human review against criteria
- Score and trend over time

## TM Asset Valuation

### Valuation Models

**Cost-Based:**
- Value = cost to recreate
- Example: 100,000 segments × $0.10/word × 10 words/segment = $100,000

**Market-Based:**
- Value = savings from reuse
- Example: 40% match rate × 50% discount × $100K annual translation = $20K/year savings

**Strategic:**
- Value = vendor independence + time-to-market
- Intangible but significant

### Amortization

**Treat TM as Capital Asset:**
- Initial creation cost: $100K
- Useful life: 5 years (before content outdated)
- Annual value: $20K

**Maintenance:**
- Cleaning/updates: $5K/year
- Net value: $15K/year

## Governance Framework

### Roles and Responsibilities

**TM Owner:**
- Decides quality standards
- Approves new entries
- Manages access

**TM Custodian (Agency or Internal Team):**
- Maintains TM
- Performs cleaning
- Generates reports

**Contributors (Translators):**
- Add new segments
- Follow quality standards
- Flag issues

### Quality Control Process

1. **Entry:** New translations added to TM (automatic or manual)
2. **Review:** Periodic audits (quarterly)
3. **Cleaning:** Remove duplicates, fix errors
4. **Approval:** TM Owner signs off on major updates
5. **Distribution:** Export TMX, version control

### Access Control

**Levels:**
- **Read-Only:** Translators can use TM, cannot modify
- **Contribute:** Translators can add segments (automatic)
- **Edit:** TM managers can modify existing segments
- **Admin:** TM owner controls access, exports, deletes

### Versioning

**Practice:** Version TMX exports

**Example:**
- `company-tm-2025-Q1.tmx` (quarterly snapshots)
- `company-tm-2025-12-31.tmx` (year-end archival)

**Storage:** Git or document management system

## TM Lifecycle

### Phase 1: Creation (Years 0-1)

**Focus:** Build TM from scratch or legacy translations

**Activities:**
- Alignment of existing translations
- Initial projects (low match rates)
- Quality standards definition

**Metrics:** Segment count growth

### Phase 2: Growth (Years 1-3)

**Focus:** Accumulate segments, increase match rates

**Activities:**
- Ongoing projects
- Cross-project TM reuse
- Termbase development

**Metrics:** Match rate increases (20% → 40% → 60%)

### Phase 3: Maturity (Years 3-5)

**Focus:** Optimize quality, maintain relevance

**Activities:**
- Regular cleaning
- Terminology updates
- Segment retirement (outdated content)

**Metrics:** Match rate stabilizes, quality improves

### Phase 4: Renewal (Years 5+)

**Focus:** Address content obsolescence

**Activities:**
- Major content refresh (product rebrand, new features)
- TM segmentation (archive old, create new)
- Technology migration (new CAT tool, new TMS)

**Metrics:** Match rate may drop temporarily, then recover

## Best Practices

**1. Contract Clarity:** Define TM ownership in all vendor contracts

**2. Regular Exports:** Export TMX quarterly (disaster recovery)

**3. Quality Over Quantity:** Don't hesitate to delete low-quality segments

**4. Versioning:** Treat TM like source code (git, tags, releases)

**5. Audit Trail:** Track who added/modified segments (metadata)

**6. Stakeholder Alignment:** TM governance involves legal, procurement, localization team

## Red Flags

**Warning Signs:**
- No TM ownership clause in vendor contracts
- No access to TMX exports
- Match rates declining over time (quality degradation)
- TM never cleaned (accumulating garbage)
- No version control (can't recover from errors)
