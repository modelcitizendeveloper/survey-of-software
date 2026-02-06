# Build vs. Buy: Strategic Decision Framework

## The Decision Matrix

### When to Buy Commercial CAT Tools

**Indicators:**
- Translation agency or professional translator
- Clients require specific tools (SDL Trados)
- Need professional support
- Advanced features justify cost (MemoQ LiveDocs, predictive typing)
- Team lacks dev resources for customization

**Cost:** $44-100/month per user (MemoQ, Trados subscription)

**ROI:** Pays for itself if productivity gain > subscription cost

### When to Use Open Source (OmegaT)

**Indicators:**
- Budget-constrained
- Data sovereignty requirements (legal, medical, government)
- Privacy-sensitive work
- Self-hosted infrastructure required
- Comfortable with community support

**Cost:** $0 licensing (but: setup time, learning curve, IT support)

**ROI:** Immediate savings on licensing, but requires technical capability

### When to Buy Cloud TMS (Smartcat, Phrase, Transifex)

**Indicators:**
- Translation agency with vendor network
- Software company with continuous localization needs
- Distributed team (remote translators)
- Need API integration for automation
- Want zero IT infrastructure overhead

**Cost:** Variable (Smartcat = service fees, Phrase = enterprise pricing, Transifex/Lokalise = per-seat or usage)

**ROI:** Productivity gains from automation + reduced overhead

### When to Build Custom Solution

**Indicators:**
- Unique workflow requirements
- Existing internal tools for translation
- Large scale (thousands of translators)
- Proprietary formats or systems
- Dev team available for maintenance

**Cost:** Development ($50K-500K+) + ongoing maintenance

**ROI:** Only at scale (Google, Facebook, Microsoft build their own)

## ROI Calculation Model

### Commercial CAT Tool ROI

**Scenario:** Freelance translator considering MemoQ

**Assumptions:**
- Translation rate: $0.10/word
- Volume: 50,000 words/month
- TM match rate: 40% (20% perfect, 20% fuzzy)
- Perfect match discount: 90% (client pays 10%)
- Fuzzy match discount: 50% (client pays 50%)

**Without CAT Tool:**
- Revenue: 50,000 × $0.10 = $5,000/month
- Time: 50,000 words ÷ 250 words/hour = 200 hours

**With CAT Tool (MemoQ @ $44/month):**
- Perfect matches: 10,000 words × 10% rate = $1,000 revenue, 40 hours
- Fuzzy matches: 10,000 words × 50% rate = $5,000 revenue, 100 hours (50% faster)
- New content: 30,000 words × 100% rate = $3,000 revenue, 120 hours
- **Total:** $9,000 revenue, 260 hours but earning more per hour

**Productivity Gain:** Translator handles more volume with TM reuse

**Payback:** Month 1 (tool pays for itself immediately)

### Cloud TMS ROI for Agencies

**Scenario:** Translation agency considering Smartcat vs. manual process

**Manual Process:**
- Project manager time: 20 hours/week @ $50/hour = $1,000/week
- Vendor coordination: Email, file transfers, version control
- Average project turnaround: 5 days

**Smartcat (automated workflow):**
- Setup time: 40 hours (one-time)
- PM time reduced: 5 hours/week @ $50/hour = $250/week
- Service fees: 5% of vendor payments
- Average project turnaround: 2 days (automation)

**Savings:** $750/week in PM time
**Cost:** Service fees (variable, assume 5% of $10K/week vendor = $500)

**Net Savings:** $250/week = $13K/year (plus faster turnaround)

**Payback:** 3-4 months

## Self-Hosted vs. Cloud TMS

### Self-Hosted Advantages

- Full data control (privacy, compliance)
- No per-user fees (fixed infrastructure cost)
- Customization flexibility
- No vendor dependency

### Self-Hosted Challenges

- Infrastructure costs (servers, storage, backups)
- IT staff for maintenance
- Security responsibility
- Update/patching overhead

### Cloud TMS Advantages

- Zero infrastructure overhead
- Automatic updates
- Vendor handles security
- Pay-as-you-grow
- Global availability

### Cloud TMS Challenges

- Data leaves your infrastructure
- Subscription costs scale with users
- Vendor dependency (lock-in risk)
- Compliance constraints (GDPR, data residency)

### Break-Even Analysis

**Self-Hosted Cost:** $50K setup + $20K/year maintenance = $70K year 1, $20K/year ongoing

**Cloud TMS Cost:** 50 users × $50/month × 12 = $30K/year

**Break-Even:** Year 3 ($50K + $20K + $20K + $20K = $110K vs. $30K + $30K + $30K + $30K = $120K)

**Conclusion:** Cloud cheaper unless:
- Very large scale (hundreds of users)
- Data sovereignty requirement justifies premium
- Existing infrastructure absorbs hosting cost

## Tool Migration Costs

**Scenario:** Migrating from SDL Trados to OmegaT (cost reduction)

**Migration Effort:**
1. Export TM from Trados (TMX) = 2 hours
2. Import TMX into OmegaT = 1 hour
3. Train team on OmegaT = 40 hours (8 hours/person × 5 people)
4. Adjust workflows = 20 hours

**Total:** ~63 hours @ $50/hour = $3,150 one-time

**Annual Savings:** 5 users × $600/year Trados = $3,000/year

**Payback:** 13 months

**Risk:** Productivity loss during transition, client requirements for Trados

## Recommendation Framework

### For Individual Translators

**Start:** OmegaT (free, learn TM concepts)

**Upgrade to MemoQ if:**
- Steady workload justifies $44/month
- Clients don't require Trados
- Advanced features (LiveDocs, Muse) provide value

**Upgrade to Trados if:**
- Multiple clients require it
- Industry standard in your niche

### For Translation Agencies

**Start:** Smartcat or Phrase (cloud TMS, vendor management)

**Consider Self-Hosted if:**
- 50+ in-house translators
- High security/compliance requirements
- Dev team available

### For Software Companies

**Start:** Cloud TMS with API (Transifex, Lokalise, Phrase)

**Build Custom if:**
- Massive scale (>100 languages, millions of strings)
- Unique workflows not supported by commercial tools
- Dev team wants full control

## Hidden Costs to Consider

### Commercial Tools

- Training time (learning curve)
- Vendor lock-in (switching costs)
- Subscription increases (price changes)

### Open Source

- Community support (slower than professional)
- DIY troubleshooting
- Feature gaps (may require workarounds)

### Self-Hosted

- Backups and disaster recovery
- Security patches and updates
- Monitoring and uptime

### Cloud

- Data egress fees (if migrating away)
- API rate limits (at scale)
- Service outages (dependency risk)

## Strategic Recommendation

**Most Organizations:** Start with cloud TMS (Smartcat, Phrase, Transifex)
- Low initial investment
- Fast time-to-value
- Easy to scale up or down

**Exception Cases:**
- **High security:** Self-hosted OmegaT
- **Agency translators:** MemoQ or Trados (client requirements)
- **Tech giants:** Build custom (scale justifies investment)
