# S3 Need-Driven Discovery: Recommendations

**Experiment**: 1.172 Translation Memory
**Pass**: S3 - Need-Driven Discovery
**Date**: 2026-01-29

## Use Case Decision Matrix

| Use Case | WHO | PRIMARY NEED | Recommended Tool | Alternative | ROI Timeline |
|----------|-----|--------------|------------------|-------------|--------------|
| **Software Localization** | SaaS companies, app developers | Git integration, version control | **OmegaT** (free, Git workflow) | Memsource (CI/CD automation) | 2nd release (3-6 months) |
| **Translation Agencies** | LSPs managing translator teams | Real-time collaboration, client isolation | **MemoQ Server** (team sync) | SDL Trados + GroupShare | Immediate (Month 1) |
| **Freelance Translators** | Independent translators | Personal TM ownership, zero cost | **OmegaT** (free, portable TMX) | SDL Trados (agency compatibility) | Year 2 (60% TM leverage) |

## Quick Selection Guide

### Step 1: WHO are you?

**Solo translator (1 person)**:
- Budget <$500 → **OmegaT** (free)
- Work with agencies → **SDL Trados Studio** ($800, industry standard)
- Direct clients only → **OmegaT** (sufficient)

**Small team (2-10 translators)**:
- Developer-friendly team → **OmegaT** (Git workflow)
- Non-technical translators → **Memsource** (web UI)
- Freelance network → **SDL Trados Studio** (most freelancers own it)

**Agency/LSP (10-100+ translators)**:
- Real-time collaboration needed → **MemoQ Server** (instant TM sync)
- Offline-first workflow → **SDL Trados + GroupShare** (project packages)
- Cloud-first organization → **Memsource** (SaaS, no infrastructure)

### Step 2: What's your annual volume?

**<100K words/year**: TM overhead may not justify investment → Use ad-hoc translation

**100K-500K words/year**:
- Free: **OmegaT**
- Paid ($500-2,000/year): **Memsource** or **SDL Trados Studio**

**500K-2M words/year**:
- Team collaboration: **MemoQ Server** or **SDL GroupShare**
- Solo: **OmegaT** or **SDL Trados Studio**

**>2M words/year**:
- Enterprise: **SDL GroupShare** (handles 100+ concurrent users)
- Cloud-first: **Memsource Enterprise**

### Step 3: Integration requirements?

**Git/version control** → **OmegaT** (seamless commit workflow)

**CI/CD pipelines** → **Memsource** (API-driven automation)

**Agency network (.sdlppx packages)** → **SDL Trados Studio** (native format)

**CMS (Confluence, WordPress)** → **Memsource** (connector plugins)

**On-premise only (data residency)** → **MemoQ Server** or **SDL GroupShare**

## Tool Comparison Summary

### OmegaT
**Best for**: Solo translators, software dev teams, budget-conscious users

**Strengths**:
- ✅ $0 cost (open source)
- ✅ Git integration (version control for translations)
- ✅ TMX format (portable, no lock-in)
- ✅ Cross-platform (Windows, Mac, Linux)

**Weaknesses**:
- ❌ No real-time team collaboration
- ❌ Steeper learning curve (less polished UI)
- ❌ No built-in project management

**Pricing**: Free

**When to choose**:
- You need Git integration (docs-as-code workflow)
- Budget is $0-500
- You value TM portability (TMX export)
- Solo translator or small developer-centric team

### MemoQ Server
**Best for**: Translation agencies (LSPs), teams of 10-100+ translators

**Strengths**:
- ✅ Real-time collaboration (multiple translators, instant TM sync)
- ✅ Client isolation (workspace separation for confidentiality)
- ✅ Cost-effective for teams (50 CAL license cheaper than 50 Trados seats)
- ✅ Freelance support (offline project packages)

**Weaknesses**:
- ❌ Expensive ($3,000-5,000/year + infrastructure)
- ❌ Requires server setup (Windows Server, SQL database)
- ❌ Smaller user base than SDL Trados (harder to hire trained translators)

**Pricing**: $3,000-5,000/year (50 CAL) + $300-500/month infrastructure

**When to choose**:
- Team size 10-100+ translators
- Need real-time collaboration (instant TM sync)
- Multiple simultaneous projects (50+ concurrent)
- Client data isolation required (LSP use case)

### SDL Trados Studio + GroupShare
**Best for**: Agencies with large freelance networks, enterprises, industry-standard workflows

**Strengths**:
- ✅ Industry standard (most freelancers already own Trados)
- ✅ Mature ecosystem (training, support, plugins)
- ✅ Enterprise-grade (100+ concurrent users on GroupShare)
- ✅ Strong QA features (number formatting, tag validation)

**Weaknesses**:
- ❌ Expensive ($900/user + $500/year GroupShare)
- ❌ Windows-only (no Mac/Linux support)
- ❌ Less real-time than MemoQ (batch updates vs. instant sync)

**Pricing**:
- Studio: $900 (perpetual) or $60/month (subscription)
- GroupShare: $500/user/year (team server)

**When to choose**:
- Large freelance network (most freelancers own Trados)
- Industry-standard workflows required
- Enterprise scale (100+ users)
- Hybrid in-house/freelance teams

### Memsource (Phrase TMS)
**Best for**: Cloud-first teams, SaaS companies, CI/CD automation

**Strengths**:
- ✅ Cloud-native (no infrastructure to manage)
- ✅ API-driven (CI/CD integration, Zapier, webhooks)
- ✅ Translator-friendly web UI (no software install)
- ✅ Flexible pricing (pay-as-you-grow)

**Weaknesses**:
- ❌ Cloud-only (no on-premise option)
- ❌ Smaller ecosystem (fewer trained translators than Trados)
- ❌ Less mature (newer tool, evolving features)

**Pricing**: $500-2,000/year (team plan, scales with users)

**When to choose**:
- Cloud-first organization (no on-premise infrastructure)
- Need API automation (CI/CD pipelines)
- Non-technical translators (web UI easier than desktop tools)
- SaaS/tech companies (modern stack)

## ROI Expectations by Use Case

### Software Localization
**Payback**: 2nd release (3-6 months)
**Steady-state savings**: 60-85% cost reduction on incremental updates
**Break-even volume**: 50K words (establish UI terminology)

**Example**:
```
v1.0 (initial): 50,000 words × $0.12/word = $6,000
v1.1 (with TM): 5,000 new + 40,000 matches = $1,000 (83% savings)
v1.2 (mature TM): 3,000 new + 45,000 matches = $560 (91% savings)
```

### Translation Agencies
**Payback**: Immediate (Month 1)
**Steady-state savings**: 40-60% translation cost reduction
**Break-even volume**: 500K words/year (justify TM server costs)

**Example**:
```
5M words/year without TM: $600,000 (@ $0.12/word)
5M words/year with TM (60% leverage): $350,000
Savings: $250,000/year
MemoQ cost: $11,000/year
ROI: 22.7x (payback in <3 weeks)
```

### Freelance Translators
**Payback**: Year 2 (60% TM reuse threshold)
**Steady-state savings**: 2x productivity = 2x income or 50% less work
**Break-even volume**: 500K words/year (TM reaches critical mass)

**Example**:
```
Year 1 (building TM): 2,000 words/day, $50,000/year
Year 3 (60% TM): 3,500 words/day, $87,500/year (+75% revenue)
Year 5 (75% TM): 5,000 words/day, $125,000/year (+150% revenue)
```

## Common Pitfalls Across All Use Cases

### 1. Over-Trusting Fuzzy Matches
**Problem**: Accept 75% fuzzy match without reviewing context
**Example**: "Delete file" → "Delete user" (85% match, WRONG context)
**Solution**: Review all matches <95%, especially UI-critical content

### 2. Not Cleaning TM Over Time
**Problem**: TM accumulates bad translations, outdated terminology
**Example**: "Cloud storage" → "cloud disk" (2015 translation, outdated)
**Solution**: Annual TM cleanup, flag low-quality segments for review

### 3. Mixing Domains in One TM
**Problem**: Legal terminology pollutes marketing TM, vice versa
**Example**: Legal "party" (participant) matches marketing "party" (celebration)
**Solution**: Separate TMs per domain/client, shared corporate glossary only

### 4. Not Backing Up TM
**Problem**: Years of TM work lost to hardware failure or cloud issue
**Example**: 5-year medical TM (4M segments) GONE → Career setback
**Solution**: 3-2-1 backup (3 copies, 2 media types, 1 offsite)

### 5. Ignoring TM Portability
**Problem**: Vendor lock-in, can't export TM when switching tools
**Example**: Proprietary format → Can't migrate to different tool
**Solution**: Use TMX-based tools or regularly export to TMX

## When NOT to Use Translation Memory

### 1. Creative Content
**Example**: Marketing taglines, advertising copy, literary translation
**Problem**: TM enforces consistency, kills creativity
**Alternative**: Human translation from scratch, maintain style guide

### 2. One-Time Projects
**Example**: Translating single book, one-time website migration
**Problem**: No future updates = TM investment never pays off
**Alternative**: Hire translator, skip TM overhead

### 3. Highly Volatile Content
**Example**: News articles, social media, rapidly changing product descriptions
**Problem**: Content changes so fast TM never accumulates reusable matches
**Alternative**: Machine translation + human post-editing (MTPE)

### 4. Very Low Volume
**Example**: <50K words/year translation volume
**Problem**: TM setup time exceeds productivity gains
**Alternative**: Ad-hoc translation with freelancers, basic terminology glossary

## Final Recommendations

### For Software Development Teams
**Start**: OmegaT (free, Git integration)
**Scale to**: Memsource (when team grows to 3+, need CI/CD)
**Consider**: SDL Trados if working with external LSPs who require it

### For Translation Agencies (LSPs)
**Start**: SDL Trados Studio (industry standard, freelance compatibility)
**Scale to**: MemoQ Server or SDL GroupShare (when team hits 10+ translators)
**Consider**: Memsource if clients demand cloud-based collaboration

### For Freelance Translators
**Start**: OmegaT (free, learn TM concepts without financial risk)
**Upgrade to**: SDL Trados Studio (when working with agencies, need compatibility)
**Consider**: Stay with OmegaT if majority work is direct clients, budget-conscious

## Cross-References

- **S1 Rapid Discovery**: [TMX format basics](../S1-rapid/tmx-format.md), [Quick tool comparison](../S1-rapid/recommendation.md)
- **S2 Comprehensive**: [OmegaT deep-dive](../S2-comprehensive/omegat.md), [MemoQ analysis](../S2-comprehensive/memoq.md), [SDL Trados evaluation](../S2-comprehensive/sdl-trados.md)
- **S3 Use Cases**: [Software localization](use-case-software-localization.md), [Translation agencies](use-case-translation-agencies.md), [Freelance translators](use-case-freelance-translators.md)
- **S4 Strategic Selection**: [Long-term TM strategy](../S4-strategic/tm-governance.md), [Build vs. buy analysis](../S4-strategic/build-vs-buy.md)
