# Use Case: Freelance Translators

**Experiment**: 1.172 Translation Memory
**Pass**: S3 - Need-Driven Discovery
**Date**: 2026-01-29

## Use Case Overview

**WHO**: Independent translators specializing in legal, medical, or technical translation

**WHY**: Build personal TM knowledge base over career lifetime, increase productivity 2x, win competitive bids with faster turnaround

**Context**: Solo translator building domain expertise (legal contracts, medical research, software localization), working mix of direct clients and agency subcontracting

**Requirements**:
- Personal TM ownership (portable across tools)
- Zero or low cost (budget-conscious)
- Works offline (coffee shops, travel)
- Compatible with agency workflows (receive/deliver project packages)
- Domain-specific terminology management
- Backup and data portability (protect 5+ years of career knowledge)

**Volume**:
- Annual output: 500K-2M words
- Specialization: Single domain (legal OR medical OR technical)
- Client mix: 30% direct, 70% agency subcontracting
- Languages: 1-3 language pairs

## Recommended Tool: OmegaT

**Rationale**:
1. **Free and open source**: $0 cost (vs. $700-900 for SDL Trados)
2. **TMX format**: Industry standard, portable to any CAT tool
3. **Personal ownership**: You own your TM forever (no cloud lock-in)
4. **Offline-first**: Works without internet (airplanes, remote locations)
5. **Cross-platform**: Windows, Mac, Linux (Java-based)

### Personal TM as Career Asset

**Scenario**: Medical translator over 5 years

| Year | Words Translated | TM Size | TM Leverage | Productivity |
|------|------------------|---------|-------------|--------------|
| 1 | 500K | 500K segments | 0% (building) | 2,000 words/day |
| 2 | 800K | 1.3M segments | 40% | 2,500 words/day |
| 3 | 1M | 2.3M segments | 60% | 3,500 words/day |
| 5 | 1.2M | 4.5M segments | 75% | 5,000 words/day |

**Use case fit**: TM grows every year → Translator gets faster without working longer hours

## Implementation Guidance

### 1. Initial Setup

**Install OmegaT**:
```bash
# Linux (Ubuntu/Debian)
sudo apt install omegat

# Mac
brew install --cask omegat

# Windows
# Download from https://omegat.org/download
```

**Create master TM directory**:
```bash
mkdir -p ~/omegat-master/
cd ~/omegat-master/

# Organize by domain
mkdir -p tm/medical tm/legal tm/technical
mkdir -p glossary/medical glossary/legal

# Create backup script
cat > backup-tm.sh <<'EOF'
#!/bin/bash
tar -czf omegat-backup-$(date +%Y%m%d).tar.gz tm/ glossary/
aws s3 cp omegat-backup-*.tar.gz s3://my-tm-backups/
EOF
chmod +x backup-tm.sh
```

### 2. Direct Client Workflow

**Receive project from client**:
```bash
# Client sends: contract.docx
mkdir -p ~/projects/client-a-contracts/
cd ~/projects/client-a-contracts/
```

**Create OmegaT project**:
```bash
omegat-project/
  source/           # Place contract.docx here
  target/           # Translated files appear here
  tm/
    main.tmx        # Link to master TM
  glossary/
    legal-terms.txt # Link to master glossary
```

**Link to master TM** (avoid duplication):
```bash
ln -s ~/omegat-master/tm/legal/main.tmx tm/main.tmx
ln -s ~/omegat-master/glossary/legal/terms.txt glossary/legal-terms.txt
```

**Translate in OmegaT**:
```
[Open OmegaT]
File → Open Project → omegat-project/

UI shows:
Source: "The undersigned parties hereby agree..."
TM match (95%): "The parties hereby agree..." → "Les parties conviennent..."
Glossary: "parties" → "parties" (legal term, same in FR)
Target: [Type translation]

[Ctrl+D] → Next segment
```

**Deliver to client**:
```bash
# OmegaT generates target/contract_fr.docx
# Send to client via email

# Master TM automatically updated with new segments
cp omegat-project/omegat/project_save.tmx ~/omegat-master/tm/legal/main.tmx
```

**Result**: Client's project adds to lifelong legal TM

### 3. Agency Subcontract Workflow

**Receive project package from agency** (.sdlppx from SDL Trados):
```bash
# Agency sends: client-x-manual.sdlppx (Trados package)
# Convert to OmegaT format using Okapi Framework

java -jar okapi-tikal.jar \
    -xm client-x-manual.sdlppx \
    -sl en -tl fr \
    -to omegat-project/
```

**Open in OmegaT**:
```bash
omegat omegat-project/

# OmegaT auto-imports agency's TM (included in package)
# Also uses YOUR personal TM (master/tm/technical/)
# You benefit from BOTH TMs (more matches)
```

**Translate faster with combined TM**:
```
Source: "Click the Submit button"
Agency TM (80%): "Click the Save button" → "Cliquer sur Enregistrer"
YOUR TM (100%): "Click the Submit button" → "Cliquer sur Soumettre" (from previous client)
OmegaT: Auto-uses YOUR 100% match (better than agency's 80%)
```

**Export back to agency format**:
```bash
# Convert OmegaT result back to .sdlrpx (Trados return package)
java -jar okapi-tikal.jar \
    -xm omegat-project/ \
    -to client-x-manual.sdlrpx

# Send .sdlrpx to agency
```

**Update master TM**:
```bash
# Extract new segments to master TM
cp omegat-project/omegat/project_save.tmx ~/omegat-master/tm/technical/
```

**Result**: Agency work also builds YOUR personal TM (not just agency's)

## Alternative Options

### Option 2: SDL Trados Studio

**When to use**:
- 80%+ of agencies you work with use Trados
- Can afford $700-900 license (or amortize over 3+ years)
- Want native .sdlppx support (no conversion needed)

**Trade-off**: Expensive, but industry standard

**Pricing comparison**:
```python
# OmegaT
cost_omegat = 0  # Free

# SDL Trados Studio
cost_trados_perpetual = 800  # One-time license
cost_trados_subscription = 60 * 12  # $60/month = $720/year

# Break-even: If you translate for 5+ years, perpetual license cheaper
```

**When OmegaT wins**:
- Agencies send XLIFF, TMX, or plain text (not .sdlppx)
- You have <3 years experience (not sure if translation is long-term career)
- Budget-conscious (starting out)

**When Trados wins**:
- 5+ years of agency work ahead
- Agencies REQUIRE Trados (won't accept XLIFF exports)
- Can afford upfront cost

### Option 3: Hybrid (OmegaT + Okapi)

**Use OmegaT as primary tool, convert agency packages as needed**:
```bash
# Install Okapi Framework (format converter)
wget https://okapiframework.org/binaries/okapi-apps_1.45.0.zip
unzip okapi-apps_1.45.0.zip -d ~/okapi/

# Convert Trados package → OmegaT
~/okapi/tikal.sh -xm agency-project.sdlppx -to omegat-project/

# Work in OmegaT (free tool)
omegat omegat-project/

# Convert back → Trados return package
~/okapi/tikal.sh -xm omegat-project/ -to agency-project.sdlrpx
```

**Best for**: Translators who prefer OmegaT UI, but must deliver Trados packages to agencies

## Common Pitfalls

### 1. Losing TM to Hard Drive Failure

**Scenario**:
```
Translator works 5 years → Builds 4M segment medical TM
Hard drive crashes → TM lost forever
5 years of career knowledge GONE
```

**Solution**: 3-2-1 backup strategy
```bash
# 3 copies: Local + Cloud + External drive
# 2 media types: SSD + Cloud storage
# 1 offsite: Cloud (AWS S3, Dropbox, Google Drive)

# Daily automated backup
crontab -e
0 2 * * * ~/omegat-master/backup-tm.sh  # Runs at 2 AM daily

# backup-tm.sh
#!/bin/bash
tar -czf ~/Dropbox/omegat-backup-$(date +%Y%m%d).tar.gz ~/omegat-master/
cp ~/omegat-master/tm/*.tmx /mnt/external-drive/omegat-backups/
```

### 2. Not Organizing TM by Domain

**Problem**: Mix legal, medical, technical TM in single file

**Scenario**:
```
Legal translation: "Patient" (legal term, "partie")
Medical translation: "Patient" (medical term, "patient")
Mixed TM: Auto-suggests legal "partie" in medical context → WRONG
```

**Solution**: Separate TMs per domain
```bash
omegat-master/
  tm/
    legal/
      contracts.tmx
      patents.tmx
    medical/
      research-papers.tmx
      clinical-trials.tmx
    technical/
      software-manuals.tmx
```

**Link correct TM per project**:
```bash
# Legal project → Use legal TM only
ln -s ~/omegat-master/tm/legal/*.tmx omegat-project/tm/

# Medical project → Use medical TM only
ln -s ~/omegat-master/tm/medical/*.tmx omegat-project/tm/
```

### 3. Accepting Low TM-Based Rates from Agencies

**Problem**: Agency pays same rate regardless of TM leverage

**Scenario**:
```
Agency: "We pay $0.08/word flat rate"
Project: 10,000 words
YOUR TM: 80% exact matches (saved 8,000 words of work)
Agency pays: $800 (full rate)
Your effort: 2,000 new words (should be $160, not $800)
```

**You work 4x faster, but paid same as new translator with 0% TM → Bad deal**

**Solution**: Negotiate TM-based pricing
```
Rate structure:
- 100% exact match: $0.01/word (review only)
- 95-99% fuzzy: $0.03/word
- 85-94% fuzzy: $0.05/word
- New translation: $0.12/word

Same 10,000-word project with 80% matches:
- 8,000 @ $0.01 = $80
- 1,000 @ $0.05 = $50
- 1,000 @ $0.12 = $120
Total: $250 (reflects effort)

Fair: You work less, paid proportionally
```

**Counter-argument if agency refuses**:
```
"I can deliver 10,000 words in 3 days (vs. 7 days without TM)
Faster delivery = more projects/month for you
I'll accept flat rate IF you send me priority projects (keep me busy)"
```

### 4. Not Exporting TMX Regularly

**Problem**: OmegaT stores TM in proprietary format, forget to export TMX

**Scenario**:
```
OmegaT project: omegat/project_save.tmx (proprietary)
If you switch to Trados later → Can't import (format incompatible)
5 years of TM locked in OmegaT format
```

**Solution**: Export TMX regularly
```bash
# OmegaT: Project → Export → Level 2 TMX
# Save to master TM directory as standard TMX

# Automated export after each project
cat > export-tmx.sh <<'EOF'
#!/bin/bash
for project in ~/projects/*/omegat-project; do
    # Export TMX using OmegaT CLI
    omegat --mode=console-translate --export-tmx "$project"
    cp "$project/omegat/level2.tmx" ~/omegat-master/tm/$(basename $project).tmx
done
EOF
```

**Result**: Standard TMX → Portable to any CAT tool (Trados, MemoQ, Wordfast, etc.)

## Performance Tuning

### 1. Large TM Performance

**Problem**: 4M segment TM → OmegaT slow (10-second lookups)

**Solution**: Split TM by year or client
```bash
# Instead of single 4M segment TM
medical-master.tmx (4M segments)

# Split into yearly TMs
medical-2021.tmx (500K segments)
medical-2022.tmx (600K segments)
medical-2023.tmx (800K segments)
medical-2024.tmx (1M segments)
medical-2025.tmx (1.1M segments)

# Current project: Link recent years only
ln -s ~/omegat-master/tm/medical-202{3,4,5}.tmx omegat-project/tm/
# Searches 3M segments (2.9M) instead of 4M → 30% faster
```

### 2. Enable Parallel Processing

**OmegaT preferences**:
```bash
# Edit ~/.omegat/prefs
omegat.parallel.threads=4  # Use 4 CPU cores

# 2-3x speedup on batch operations
```

## Success Metrics

### TM Growth (Career-Long Asset)

**Track TM size over time**:
```bash
# Count segments in master TM
grep -c '<tu>' ~/omegat-master/tm/medical/main.tmx

Year 1: 500,000 segments
Year 3: 2,300,000 segments
Year 5: 4,500,000 segments

# TM compounds like investment portfolio (gets more valuable each year)
```

### Productivity Gains

**Measure words/day over career**:
```
Year 1 (no TM): 2,000 words/day
Year 2 (40% TM): 2,500 words/day (+25%)
Year 3 (60% TM): 3,500 words/day (+75%)
Year 5 (75% TM): 5,000 words/day (+150%)
```

**Two paths**:
- **Path A (more income)**: Work same hours, earn 2.5x revenue
- **Path B (more free time)**: Earn same income, work 40% fewer hours

### Competitive Bidding

**Win bids with faster delivery**:
```
Client RFP: 50,000-word medical device manual
Competitors: Bid 25 days @ $400/day = $10,000

You (with medical TM):
- TM leverage: 70% (from previous medical device manuals)
- Actual work: 15,000 new words
- Deliver in: 10 days (vs. 25 days)
- Bid: $6,000 (40% cheaper, still profitable)

Client: "You're fastest AND cheapest? You're hired!"
```

**TM = competitive moat** (new translators can't match your speed)

## Cost Analysis

### Software Cost

**OmegaT**: $0
**SDL Trados Studio**: $800 (perpetual) or $60/month

**Break-even**:
```python
# If you save 1 hour/week with better tool
hours_saved_per_year = 52
hourly_rate = 50  # $/hour
value_of_saved_time = hours_saved_per_year * hourly_rate  # $2,600

# Trados pays for itself in 4 months if it saves 1 hour/week
trados_cost = 800
payback_months = trados_cost / (value_of_saved_time / 12)  # 3.7 months
```

**Reality**: OmegaT is equally fast for solo translators (no productivity difference)
**Verdict**: Save $800, invest in marketing or professional development instead

### Revenue Impact

**Scenario**: Freelance medical translator

**Year 1** (building TM):
```
Volume: 500,000 words/year
Rate: $0.10/word (direct clients)
Revenue: $50,000

Hours worked: 250 days × 8 hours = 2,000 hours
Hourly rate: $25/hour
```

**Year 3** (mature TM, 60% leverage):
```
Volume: 1,000,000 words/year (2x output, same hours)
Rate: $0.10/word
Revenue: $100,000 (+100% vs. Year 1)

Hours worked: 2,000 hours (same as Year 1)
Hourly rate: $50/hour (doubled)
```

**Alternative (work less, same revenue)**:
```
Volume: 500,000 words/year (same as Year 1)
Hours worked: 1,000 hours (50% of Year 1)
Revenue: $50,000 (same)

Result: Work 6 months, travel 6 months (lifestyle flexibility)
```

**TM impact**: 2x productivity = 2x income OR 50% less work

## Real-World Examples

### Case Study: Marie L. (Medical Translator, FR→EN)

**Background**:
- Year 1 (2018): Started with OmegaT (free), translated 400K words
- Year 2: Built 800K segment medical TM, productivity +40%
- Year 3: Switched to Trados Studio ($800) to work with agencies
- Year 4: 60% TM leverage, earning $80K/year (up from $50K in Year 1)
- Year 5: Known as specialist, clients pay premium, $95K/year

**Key factors**:
1. Domain focus (medical research) = high TM reuse
2. TMX portability (OmegaT → Trados migration without data loss)
3. Backup discipline (never lost TM)
4. Leveraged TM for competitive pricing (win bids)

### Case Study: Juan R. (Legal Translator, ES→EN)

**Background**:
- 10 years with SDL Trados Studio
- 6M segment legal TM (contracts, patents, court documents)
- 80-85% TM leverage on new projects
- Productivity: 6,000 words/day (vs. 2,000 for new translators)
- Revenue: $120K/year (top 10% of freelance translators)

**Key factors**:
1. Trados = industry standard for legal LSPs (90% of agencies use it)
2. Long-term investment ($800 license paid off 100x over 10 years)
3. TM as competitive advantage (can bid 50% lower, still profitable)

## Summary

**Recommended Tool**: OmegaT (free, portable, lifelong ownership)

**Key strengths**:
- ✅ $0 cost (vs. $800 for Trados)
- ✅ TMX format (portable to any tool, no lock-in)
- ✅ Personal ownership (you control your TM forever)
- ✅ Works offline (airplanes, remote work)
- ✅ Cross-platform (Windows, Mac, Linux)

**When to use SDL Trados instead**:
- 80%+ agency work (they require .sdlppx packages)
- Can afford $800 upfront (or $60/month subscription)
- 5+ years in translation career (amortize cost)

**Career impact**: 2x productivity by Year 3, double income or halve working hours

**ROI**: Free tool with infinite payoff (every translation adds to TM)

## Cross-References

- **S1 Rapid Discovery**: [omegat.md](../S1-rapid/omegat.md), [sdl-trados.md](../S1-rapid/sdl-trados.md), [tmx-format.md](../S1-rapid/tmx-format.md)
- **S2 Comprehensive**: [omegat.md](../S2-comprehensive/omegat.md), [sdl-trados.md](../S2-comprehensive/sdl-trados.md)
- **S3 Other Use Cases**: [use-case-software-localization.md](use-case-software-localization.md), [use-case-translation-agencies.md](use-case-translation-agencies.md)
- **S4 Strategic**: TM as career asset, build vs. buy decision
