# S4 Strategic Pass: Executive Summary

## Critical Strategic Decisions

### 1. TM Ownership is a Business Decision, Not a Technical One

**Question:** Who owns the translation memory?

**Impact:**
- **Client ownership:** Vendor independence, asset accumulation, premium cost
- **Agency ownership:** Cost savings (match discounts), vendor lock-in
- **Shared model:** Balanced, suitable for partnerships

**Recommendation:** Default to client ownership unless cost savings outweigh flexibility loss. Specify in contracts.

### 2. Cloud TMS is the Modern Default Choice

**Analysis:**
- Self-hosted: Only justified at scale (hundreds of users) or compliance requirements
- Cloud: Lower total cost of ownership for most organizations
- Open source: Best for individual translators or high-security environments

**Recommendation:** Start cloud (Smartcat, Phrase, Transifex), migrate to self-hosted only if scale or compliance demands it.

### 3. TM is a Depreciating Asset Without Maintenance

**Reality:** TM degrades over time without:
- Regular cleaning (20-45% removal typical)
- Terminology updates
- Content relevance checks

**Recommendation:**
- Quarterly TM audits
- Annual major cleaning
- Retirement of outdated segments (5-year lifecycle)

### 4. ROI is Measurable and Often Immediate

**Freelance Translator:**
- MemoQ ($44/month) pays for itself month 1 with 20-40% TM match rate

**Translation Agency:**
- Cloud TMS saves 15 PM hours/week vs. manual process
- Payback: 3-4 months

**Software Company:**
- Continuous localization reduces time-to-market from weeks to days
- Revenue impact >> tool cost

**Recommendation:** Calculate ROI before purchasing. Most commercial tools pay for themselves quickly.

## Decision Frameworks

### For Executives: Build vs. Buy

**Buy Commercial Tools When:**
- Standard workflows
- Need professional support
- Want fast time-to-value
- Team lacks dev resources

**Buy Cloud TMS When:**
- Distributed teams
- Continuous localization needs
- API integration required
- Want zero IT overhead

**Use Open Source When:**
- Budget-constrained
- Data sovereignty required
- Self-hosted infrastructure preferred

**Build Custom When:**
- Massive scale (Google/Facebook level)
- Unique workflows not supported commercially
- Dev team available for ongoing maintenance

**Default Recommendation:** Cloud TMS for most organizations

### For Managers: TM Governance

**Key Questions:**
1. Who owns TM? (Specify in vendor contracts)
2. How do we measure quality? (Quarterly audits, sampling)
3. Where is TMX stored? (Version control, backups)
4. Who can access/modify? (Read-only vs. edit vs. admin)
5. When do we clean? (Quarterly maintenance schedule)

**Default Recommendation:**
- Client owns TM
- TMX exported quarterly to git
- Quality audits semi-annually
- Professional cleaning annually

### For Teams: Migration Planning

**Red Flags Requiring Migration:**
- Vendor lock-in (can't export TMX)
- Tool doesn't meet needs (missing features)
- Cost not justified (paying for unused features)
- Compliance changes (data must move to self-hosted)

**Migration Checklist:**
1. Export TMX from current tool
2. Test import in target tool (verify round-trip)
3. Train team (budget 8-40 hours per person)
4. Pilot with one project
5. Gradual rollout (not big bang)

**Migration Cost:** 50-100 hours effort + subscription overlap (3-6 months)

**Default Recommendation:** Migrate during low season, plan 6-month transition

## Common Executive Questions

### "Should we build a custom TMS?"

**Answer:** No, unless:
- You're Google/Facebook/Microsoft scale
- Commercial tools can't handle your workflow
- You have a dedicated dev team for localization infrastructure

**Reality:** Even large companies (Airbnb, Shopify) use commercial TMS. Only tech giants build custom.

### "How much should we invest in TM?"

**Answer:** Calculate based on annual translation spend:

- **<$50K/year:** Free tools (OmegaT) or entry cloud TMS
- **$50K-$500K/year:** Commercial cloud TMS ($10K-30K/year tool cost)
- **>$500K/year:** Enterprise TMS + professional TM management ($50K-100K/year)

**Rule of Thumb:** Tool cost should be 10-20% of annual translation spend.

### "What's the payback period?"

**Answer:** Most tools: 3-6 months

**Drivers:**
- Productivity gain: 20-60% with TM reuse
- Cost savings: Match discounts (50-90% off for matches)
- Time savings: PM hours reduced with automation

### "How do we avoid vendor lock-in?"

**Answer:**
1. **Export TMX regularly** (quarterly)
2. **Test import in alternative tool** (annually)
3. **Avoid proprietary formats** (use XLIFF, TMX, TBX)
4. **Contractual export rights** (specify in vendor agreements)
5. **Version control** (TMX in git)

**Reality:** Some lock-in is acceptable if value delivered exceeds switching cost. Total vendor independence is expensive (limits feature usage).

## Strategic Priorities by Organization Type

### Individual Translator

**Priority:** Productivity with minimal cost

**Strategy:**
1. Start: OmegaT (free)
2. Upgrade: MemoQ ($44/month) if workload steady
3. Add: Trados only if clients require

### Translation Agency

**Priority:** Vendor management + automation

**Strategy:**
1. Cloud TMS with marketplace (Smartcat) or API (Phrase)
2. TM ownership model decided (client vs. agency)
3. Quality audits quarterly

### Software Company

**Priority:** Speed-to-market + automation

**Strategy:**
1. Cloud TMS with CI/CD integration (Phrase, Transifex, Lokalise)
2. Continuous localization from day 1
3. MT + TM hybrid (quality thresholds)

### Enterprise (Non-Tech)

**Priority:** Compliance + quality

**Strategy:**
1. Self-hosted if data sovereignty required
2. Professional TM management (dedicated team)
3. Governance framework (ownership, access, audits)

## Final Recommendation

**Most Organizations Should:**
- Use cloud TMS (Smartcat, Phrase, Transifex)
- Retain TM ownership (client-owned model)
- Export TMX quarterly to version control
- Clean TM annually (20-45% removal typical)
- Calculate ROI annually (justify continued investment)

**Exceptions:**
- High security: Self-hosted OmegaT
- Compliance: Self-hosted commercial TMS
- Freelancers: OmegaT or MemoQ
- Tech giants: Build custom (only at massive scale)

**Red Flags:**
- No TMX export capability
- Vendor contract doesn't specify TM ownership
- No version control for TM
- Match rates declining (quality degradation)
- No ROI measurement
