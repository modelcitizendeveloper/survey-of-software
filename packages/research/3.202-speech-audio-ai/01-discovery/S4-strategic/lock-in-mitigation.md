# Lock-in Risk & Migration Strategies
## Experiment 3.202: Speech & Audio AI Services

**Research Phase**: S4 - Strategic Selection
**Date**: 2025-11-24
**Purpose**: Quantify lock-in risks and provide migration playbooks for switching between providers

---

## Executive Summary

This analysis scores lock-in risk (1-5 scale) across 5 dimensions for 8 providers and provides time/cost estimates for migration scenarios.

**Lock-in Risk Scores (1 = minimal lock-in, 5 = severe lock-in)**:

| Provider | Data Portability | API/Integration | Workflow | Cost | Feature | **Overall Score** | Risk Level |
|----------|-----------------|----------------|----------|------|---------|-------------------|------------|
| **OpenAI Whisper** | 1.0 | 1.0 | 1.0 | 1.0 | 1.5 | **1.1** | Minimal |
| **Deepgram** | 1.0 | 1.0 | 1.0 | 1.0 | 1.5 | **1.1** | Minimal |
| **AssemblyAI** | 1.0 | 1.5 | 1.0 | 1.0 | 2.5 | **1.4** | Low |
| **Rev AI** | 1.5 | 1.0 | 1.0 | 1.0 | 2.0 | **1.3** | Low |
| **Fathom** | 2.0 | 2.0 | 2.5 | 1.5 | 2.0 | **2.1** | Low-Medium |
| **Otter.ai** | 2.5 | 2.5 | 3.0 | 2.0 | 2.5 | **2.6** | Medium |
| **Fireflies.ai** | 2.0 | 3.5 | 3.5 | 2.5 | 3.0 | **2.9** | Medium |
| **Grain** | 2.5 | 4.5 | 4.0 | 3.0 | 3.5 | **3.4** | Medium-High |

**Key Findings**:

1. **APIs have minimal lock-in** (Whisper, Deepgram, AssemblyAI, Rev AI: 1.1-1.4/5): Easy data export (JSON), standard integration patterns, minimal workflow dependency.

2. **SaaS platforms have medium lock-in** (Fathom, Otter, Fireflies, Grain: 2.1-3.4/5): Meeting bot workflows create dependency, CRM integrations increase switching costs.

3. **Grain has highest lock-in** (3.4/5): Deep HubSpot integration, video clip library (Stories), bi-directional CRM sync create significant switching friction.

4. **Migration costs vary 10×** (API-to-API: $800-2,400 vs SaaS-to-API: $3,000-10,000): Building custom workflow to replace SaaS meeting bot is expensive.

---

## Lock-in Scoring Methodology

### Scoring Dimensions (5 factors, weighted)

| Dimension | Weight | Scoring Criteria |
|-----------|--------|------------------|
| **Data Portability** | 25% | Can you export all data? Formats: JSON, TXT, SRT, PDF? |
| **API/Integration Lock-in** | 20% | CRM integrations, Zapier, custom development |
| **Workflow Lock-in** | 25% | Meeting bot dependency, auto-join workflows, team habits |
| **Cost Lock-in** | 15% | Contract length, cancellation penalties, sunk costs |
| **Feature Lock-in** | 15% | Unique features hard to replace (PII redaction, prompt caching) |

### Scoring Scale (1-5)

| Score | Severity | Description |
|-------|----------|-------------|
| **1** | Minimal | No lock-in; switch in <4 hours with zero data loss |
| **2** | Low | Minor friction; export is manual but complete; switch in 4-8 hours |
| **3** | Medium | Moderate friction; some features lost in migration; 8-16 hours |
| **4** | High | Significant friction; CRM integrations, workflow disruption; 20-40 hours |
| **5** | Severe | Catastrophic lock-in; proprietary formats, no export; 40+ hours |

### Overall Lock-in Score

**Formula**: (Data × 0.25) + (API × 0.20) + (Workflow × 0.25) + (Cost × 0.15) + (Feature × 0.15)

**Interpretation**:
- **1.0-1.9**: Minimal to low lock-in (safe for month-to-month contracts)
- **2.0-2.9**: Low-medium to medium lock-in (annual contracts acceptable, avoid 3-year)
- **3.0-3.9**: Medium-high lock-in (monthly contracts recommended, plan exit strategy)
- **4.0-5.0**: Severe lock-in (avoid unless critical, multi-provider strategy required)

---

## Lock-in Analysis by Provider

### 1. OpenAI Whisper API

| Dimension | Score | Rationale |
|-----------|-------|-----------|
| **Data Portability** | 1.0 | JSON response includes full transcript, timestamps, confidence scores. No vendor storage (user controls data). |
| **API/Integration** | 1.0 | Standard REST API; no proprietary integrations. Easy to swap with AssemblyAI, Deepgram (similar API format). |
| **Workflow** | 1.0 | API-only; no meeting bot or auto-join. User builds own workflow (zero dependency on Whisper-specific features). |
| **Cost** | 1.0 | Month-to-month billing; no contracts. Self-hosted option available (MIT license, zero cost). |
| **Feature** | 1.5 | Multilingual (99 languages) is unique; switching to English-only provider (Deepgram, Rev AI) loses this. |
| **Overall** | **1.1** | **Minimal lock-in** |

**Migration Difficulty**: Very easy (API-to-API swap takes 8-16 hours for code changes, testing).

**Mitigation Strategies**:
- Build abstraction layer (LangChain-style wrapper) to reduce API switching cost to 2-4 hours.
- Self-hosted Whisper as fallback (MIT license, zero vendor lock-in).

---

### 2. Deepgram API

| Dimension | Score | Rationale |
|-----------|-------|-----------|
| **Data Portability** | 1.0 | JSON response includes full transcript, timestamps, confidence scores. No vendor storage. |
| **API/Integration** | 1.0 | Standard REST/WebSocket API; similar to Whisper, AssemblyAI (easy swap). |
| **Workflow** | 1.0 | API-only; no meeting bot. User builds own workflow. |
| **Cost** | 1.0 | Month-to-month billing; no contracts. Free tier ($150-200 credits) for testing. |
| **Feature** | 1.5 | Real-time streaming (<300ms latency) is best-in-class; switching to batch-only provider (Whisper) loses this. |
| **Overall** | **1.1** | **Minimal lock-in** |

**Migration Difficulty**: Very easy (API-to-API swap takes 8-16 hours).

**Mitigation Strategies**:
- Build abstraction layer for API calls.
- Test backup provider (AssemblyAI, Whisper) quarterly to ensure migration readiness.

---

### 3. AssemblyAI API

| Dimension | Score | Rationale |
|-----------|-------|-----------|
| **Data Portability** | 1.0 | JSON response includes full transcript, timestamps, confidence scores, sentiment, PII redaction. No vendor storage. |
| **API/Integration** | 1.5 | Standard REST/WebSocket API, but PII redaction feature is unique (vendor-specific implementation). |
| **Workflow** | 1.0 | API-only; no meeting bot. User builds own workflow. |
| **Cost** | 1.0 | Month-to-month billing; no contracts. Free tier ($50 credits) for testing. |
| **Feature** | 2.5 | PII redaction, sentiment analysis, topic detection are advanced features; switching to Whisper/Deepgram loses these. |
| **Overall** | **1.4** | **Low lock-in** |

**Migration Difficulty**: Easy to moderate (API-to-API swap takes 8-16 hours, but PII redaction may require custom implementation).

**Mitigation Strategies**:
- If PII redaction is critical, build fallback using regex patterns or alternative providers (Azure Cognitive Services).
- Test sentiment analysis alternatives (AWS Comprehend, Google Cloud Natural Language) before committing.

---

### 4. Rev AI API

| Dimension | Score | Rationale |
|-----------|-------|-----------|
| **Data Portability** | 1.5 | JSON response includes transcript, timestamps. Human-reviewed transcripts (optional $1.99/min service) may have proprietary formatting. |
| **API/Integration** | 1.0 | Standard REST API; similar to Whisper, AssemblyAI. No proprietary integrations. |
| **Workflow** | 1.0 | API-only; no meeting bot. User builds own workflow. |
| **Cost** | 1.0 | Month-to-month billing; no contracts. Enterprise tier has volume discounts (no long-term commitment required). |
| **Feature** | 2.0 | Highest accuracy (47% better on challenging audio per Rev's 2024 report); switching to Whisper accepts 5-10% accuracy loss. |
| **Overall** | **1.3** | **Low lock-in** |

**Migration Difficulty**: Easy (API-to-API swap takes 8-16 hours, accuracy testing recommended).

**Mitigation Strategies**:
- Use Rev AI for accuracy-critical transcripts (20% of volume), Whisper for routine transcripts (80% of volume).
- Test Whisper accuracy on your specific audio domain before migrating fully.

---

### 5. Fathom (SaaS Meeting Platform)

| Dimension | Score | Rationale |
|-----------|-------|-----------|
| **Data Portability** | 2.0 | Export available (PDF, TXT, likely JSON), but manual export per meeting. No bulk export API for free tier. |
| **API/Integration** | 2.0 | CRM integrations (Salesforce, HubSpot), but integrations are basic (one-way sync, limited metadata). Zapier available. |
| **Workflow** | 2.5 | Meeting bot auto-joins calls; team relies on bot for recording. Switching requires retraining team to upload files manually or adopt new bot. |
| **Cost** | 1.5 | Free tier (unlimited for individuals), $24-29/user/month for teams (month-to-month billing). No long-term contracts. |
| **Feature** | 2.0 | GPT-4 summaries (5/month free tier) are unique; free tier is most generous among competitors (unlimited recordings, storage). |
| **Overall** | **2.1** | **Low-medium lock-in** |

**Migration Difficulty**: Moderate (SaaS-to-SaaS: 6-12 hours to export data, retrain team; SaaS-to-API: 20-40 hours to build meeting bot replacement).

**Mitigation Strategies**:
- Free tier users: Zero switching cost (export monthly, easy to try alternatives).
- Paid tier users: Monthly export recommended (PDF, TXT formats).
- Avoid deep CRM integration (use Zapier for one-way sync only to reduce lock-in).

---

### 6. Otter.ai (SaaS Meeting Platform)

| Dimension | Score | Rationale |
|-----------|-------|-----------|
| **Data Portability** | 2.5 | Export available (PDF, TXT, SRT), but manual export per meeting. No bulk export API. Free tier (300 min/month) limits export options. |
| **API/Integration** | 2.5 | CRM integrations (Salesforce, HubSpot, Zoom), Zapier available. OtterPilot for Sales has deeper Salesforce sync (bi-directional). |
| **Workflow** | 3.0 | Meeting bot auto-joins calls; 25M+ user base suggests strong workflow dependency. OtterPilot for Sales users rely on automated CRM sync. |
| **Cost** | 2.0 | Annual contracts common ($100/year Pro, $240/year Business). Monthly option available but costs 40-60% more ($16.99/month vs $8.33/month annual). |
| **Feature** | 2.5 | OtterPilot for Sales, live transcript editing, voice recognition (identifies speakers by voice) are differentiators. |
| **Overall** | **2.6** | **Medium lock-in** |

**Migration Difficulty**: Moderate to high (SaaS-to-SaaS: 12-20 hours due to 25M user base, team habits; SaaS-to-API: 30-50 hours for OtterPilot for Sales replacement).

**Mitigation Strategies**:
- Monthly export of transcripts (TXT, SRT formats) recommended.
- OtterPilot for Sales users: Test Fireflies or Grain before committing to annual contracts (avoid lock-in).
- Annual contracts acceptable for Pro tier ($100/year), but avoid Business tier multi-year contracts ($240/year × 3 = $720/user).

---

### 7. Fireflies.ai (SaaS Meeting Platform)

| Dimension | Score | Rationale |
|-----------|-------|-----------|
| **Data Portability** | 2.0 | Export available (PDF, TXT, JSON), bulk export possible via API (Enterprise tier only). Pro/Business tiers require manual export. |
| **API/Integration** | 3.5 | Deep CRM integrations (Salesforce, HubSpot), Zapier, API access (Enterprise). Fireflies AI Apps marketplace creates proprietary workflow dependencies. |
| **Workflow** | 3.5 | Meeting bot auto-joins calls, 2B+ minutes processed suggests strong adoption. AI Apps (candidate scoring, email generation) create workflow lock-in. |
| **Cost** | 2.5 | Annual contracts ($120/year Pro, $228/year Business). Enterprise tier may have multi-year commitments. |
| **Feature** | 3.0 | AI Apps marketplace, conversation analytics (talk time, sentiment), AskFred chatbot are unique. Topic tracking across meetings is differentiator. |
| **Overall** | **2.9** | **Medium lock-in** |

**Migration Difficulty**: High (SaaS-to-SaaS: 16-24 hours due to AI Apps, CRM integrations; SaaS-to-API: 40-60 hours to rebuild AI Apps workflows).

**Mitigation Strategies**:
- Monthly export of transcripts (JSON format preferred for metadata preservation).
- Avoid deep AI Apps dependencies (use sparingly, prefer generic Zapier workflows).
- Annual contracts acceptable for Pro tier ($120/year), but avoid Business tier multi-year contracts.
- Plan for migration by 2027-2028 (acquisition risk 60-70%, product may be sunset).

---

### 8. Grain (SaaS Meeting Platform)

| Dimension | Score | Rationale |
|-----------|-------|-----------|
| **Data Portability** | 2.5 | Export available (likely PDF, TXT, video clips), but Stories (video clip library) may have proprietary format. Manual export required. |
| **API/Integration** | 4.5 | Deep bi-directional HubSpot sync (deals, contacts, meeting notes auto-sync). Switching requires rebuilding HubSpot integration from scratch. |
| **Workflow** | 4.0 | Meeting bot auto-joins calls, video clip creation (Stories) for sales training. HubSpot users rely on automated deal updates, meeting logging. |
| **Cost** | 3.0 | Annual contracts ($180/user/year estimated). Enterprise tier likely has multi-year commitments. Switching cost includes rebuilding HubSpot workflows. |
| **Feature** | 3.5 | Best-in-class HubSpot integration, video clip library (Stories), sales training features are unique. No equivalent among competitors. |
| **Overall** | **3.4** | **Medium-high lock-in** |

**Migration Difficulty**: Very high (SaaS-to-SaaS: 24-40 hours to export data, rebuild HubSpot integration; SaaS-to-API: 60-80 hours to replicate HubSpot sync, Stories features).

**Mitigation Strategies**:
- **For HubSpot users**: Grain is best option short-term (1-3 years), but plan exit strategy.
- Monthly export of transcripts, video clips (Stories) recommended.
- Document HubSpot integration setup (deal updates, contact logging) for migration.
- Avoid multi-year contracts (high acquisition risk 70-80%; product may be sunset post-acquisition).
- **Migration path**: Grain → Fireflies (HubSpot integration) or native HubSpot meeting intelligence (by 2027-2028).

---

## Migration Playbooks

### Migration Scenario 1: SaaS-to-SaaS (Fireflies → Otter)

**Use Case**: Switching from Fireflies to Otter.ai due to pricing, features, or vendor consolidation.

**Time Estimate**: 6-12 hours (depending on team size, CRM integrations)

**Cost Estimate**: $300-1,200 (internal time + retrain team)

**Steps**:

1. **Data Export** (2-3 hours):
   - Export all transcripts from Fireflies (JSON, TXT, PDF formats).
   - Download video recordings (if applicable, Business tier+).
   - Export CRM integration data (meeting logs, action items synced to Salesforce/HubSpot).

2. **Otter Setup** (1-2 hours):
   - Create Otter accounts for all team members.
   - Configure calendar integration (Google Calendar, Outlook).
   - Set up CRM integration (Salesforce, HubSpot) to replicate Fireflies workflow.

3. **Team Retraining** (2-4 hours):
   - Train team on Otter UI (live transcript editing, commenting, action items).
   - Update meeting bot expectations (Otter Notetaker vs Fireflies Notetaker).

4. **CRM Workflow Adjustment** (1-3 hours):
   - Reconfigure CRM workflows (Zapier, native integrations) to use Otter instead of Fireflies.
   - Test meeting logging, action item sync.

**Data Loss**: Historical transcripts (archived in Fireflies) are not migrated to Otter. Users must export and store locally or in document management system (Google Drive, Sharepoint).

**Challenges**:
- Fireflies AI Apps workflows (candidate scoring, email generation) have no equivalent in Otter → manual workarounds required.
- CRM integration differences (Fireflies may have deeper Salesforce sync than Otter → functionality gap).

---

### Migration Scenario 2: SaaS-to-API (Otter → Whisper API)

**Use Case**: Switching from Otter to custom Whisper API build for cost savings at scale (50+ users, 5,000+ hours/year).

**Time Estimate**: 20-40 hours (development, testing, deployment)

**Cost Estimate**: $3,000-10,000 (dev time at $100-150/hour)

**Steps**:

1. **Data Export** (2-4 hours):
   - Export all transcripts from Otter (TXT, SRT formats).
   - Download recordings (if available).

2. **Custom Workflow Development** (12-24 hours):
   - Build file upload UI (replace Otter meeting bot with manual/automated upload).
   - Integrate Whisper API (REST calls, handle audio format conversion).
   - Build transcript storage (database or S3 bucket).
   - Implement search, playback UI (replace Otter's web interface).

3. **Meeting Bot Replacement** (4-8 hours):
   - Option A: Manual upload (users upload recordings post-meeting).
   - Option B: Automated recording (Zoom, Teams recording → auto-upload to Whisper API).
   - Option C: Build custom meeting bot (Zoom SDK, Teams Graph API → join meetings, record, transcribe).

4. **CRM Integration** (2-4 hours):
   - Replicate Otter CRM sync using Zapier or custom API calls (Salesforce, HubSpot).

5. **Testing & Deployment** (4-8 hours):
   - Test accuracy (Whisper vs Otter), fix formatting issues.
   - Train team on new workflow (upload → transcribe → search).

**Data Loss**: Otter-specific features (live editing, voice recognition, OtterPilot for Sales) are lost. Users must build custom equivalents or accept functionality gap.

**Challenges**:
- Meeting bot replacement is most expensive (Option C: 20-40 hours to build custom bot).
- Team resistance (Otter UI is polished; custom build may feel clunky).
- Ongoing maintenance (bug fixes, API updates) adds $4,800-9,000/year cost.

**ROI Breakpoint**: SaaS-to-API migration makes sense if:
- Team size >50 users (Otter Business: $240/user/year × 50 = $12,000/year vs Whisper API: $2,000-4,000/year).
- Volume >5,000 hours/year (Otter Business: 6,000 min/month/user × 50 = 300,000 min/year = 5,000 hours).
- 3-year horizon (amortize dev cost: $10,000 dev ÷ 3 = $3,333/year).

---

### Migration Scenario 3: API-to-SaaS (Whisper → Fireflies)

**Use Case**: Switching from custom Whisper API build to Fireflies due to team growth, meeting bot need, or maintenance burden.

**Time Estimate**: 4-8 hours (setup, data migration, team training)

**Cost Estimate**: $400-800 (internal time + Fireflies subscription)

**Steps**:

1. **Data Export from Custom Build** (1-2 hours):
   - Export transcripts from database/S3 (JSON, TXT formats).
   - Archive historical data.

2. **Fireflies Setup** (1-2 hours):
   - Create Fireflies accounts for all team members.
   - Configure calendar integration (auto-join meetings).
   - Set up CRM integration (Salesforce, HubSpot).

3. **Team Training** (2-4 hours):
   - Train team on Fireflies meeting bot (auto-join, recording permissions).
   - Introduce AI features (AskFred, action items, conversation analytics).

**Data Loss**: Historical transcripts from custom build are not migrated to Fireflies. Users must store locally or in document management system.

**Challenges**:
- Fireflies subscription cost ($120-228/user/year) eliminates cost savings from Whisper API build.
- Sunk cost of custom development ($10,000-40,000) is written off.

**When This Makes Sense**:
- Team grew beyond initial estimate (50 users → 200 users) → maintenance burden too high.
- Meeting bot workflow is critical (manual upload is friction for sales teams).
- CRM integration complexity increased (custom API calls → prefer native Fireflies sync).

---

### Migration Scenario 4: API-to-API (Whisper → AssemblyAI)

**Use Case**: Switching from Whisper API to AssemblyAI for advanced features (PII redaction, sentiment analysis, real-time streaming).

**Time Estimate**: 8-16 hours (code changes, testing, deployment)

**Cost Estimate**: $800-2,400 (dev time at $100-150/hour)

**Steps**:

1. **Code Migration** (4-8 hours):
   - Replace Whisper API calls with AssemblyAI API calls (REST/WebSocket).
   - Update audio format handling (Whisper accepts more formats; AssemblyAI may require conversion).
   - Adjust response parsing (JSON structure differs slightly).

2. **Feature Integration** (2-4 hours):
   - Enable PII redaction (AssemblyAI feature not in Whisper).
   - Integrate sentiment analysis, topic detection (optional).

3. **Testing** (2-4 hours):
   - Test accuracy (compare Whisper vs AssemblyAI on sample audio).
   - Verify PII redaction (test SSN, credit card redaction).
   - Load testing (ensure AssemblyAI API handles volume).

**Data Loss**: None (APIs are similar; full transcript, timestamps, confidence scores available in both).

**Challenges**:
- Pricing increase (AssemblyAI $0.37/hour vs Whisper $0.36/hour → 3% more expensive).
- Multilingual support (Whisper 99 languages vs AssemblyAI ~30 languages → feature loss).

**When This Makes Sense**:
- PII redaction is required (HIPAA, legal compliance).
- Real-time streaming needed (AssemblyAI Universal-Streaming <300ms latency).
- Sentiment analysis adds business value (customer support, sales calls).

---

## Lock-in Mitigation Strategies

### Strategy 1: Multi-Provider Approach

**Description**: Use primary provider + fallback provider to reduce vendor dependency.

**Implementation**:
- Primary provider (80% of volume): Fireflies, Otter, Whisper (based on use case).
- Fallback provider (20% of volume, monthly testing): AssemblyAI, Deepgram, Fathom.

**Cost Overhead**: 15-20% (testing fallback provider monthly, maintaining dual integrations).

**Benefits**:
- Rapid migration (fallback is already integrated, tested monthly).
- Negotiating leverage (primary vendor knows you have fallback ready).
- Risk reduction (if primary vendor is acquired/sunset, fallback activates immediately).

**Example**:
- Sales team uses Grain (primary) for HubSpot integration.
- Fallback: Fireflies (HubSpot integration available, test 5 meetings/month).
- If Grain is acquired by HubSpot → migrate to Fireflies in 6-12 hours.

---

### Strategy 2: Abstraction Layer (API Wrapper)

**Description**: Build LangChain-style wrapper around speech-to-text API to reduce switching cost.

**Implementation**:
- Create abstraction layer with standard interface:
  ```python
  def transcribe(audio_file, provider="whisper"):
      if provider == "whisper":
          return call_whisper_api(audio_file)
      elif provider == "assemblyai":
          return call_assemblyai_api(audio_file)
      elif provider == "deepgram":
          return call_deepgram_api(audio_file)
  ```
- Switching providers requires changing 1 line of code (provider="assemblyai").

**Upfront Cost**: 40-80 dev hours ($4,000-8,000).

**Payback**: Reduces API migration cost from 8-16 hours to 2-4 hours (80% reduction).

**When This Makes Sense**:
- High-volume API use (>5,000 hours/year, >$2,000/year API spend).
- 3+ year planning horizon (amortize $8,000 dev cost over 3 years = $2,667/year).
- Technology shift expected (Whisper commoditization, expect provider churn).

---

### Strategy 3: Regular Export Cadence

**Description**: Monthly export of all transcripts to local storage (Google Drive, Sharepoint, S3).

**Implementation**:
- Schedule monthly export (manual or automated via API if available).
- Store in standard formats (JSON, TXT, SRT) for easy import elsewhere.

**Time Overhead**: 1-2 hours/month (manual export) or 8-16 hours upfront (automated script).

**Benefits**:
- Protects against data loss if vendor shuts down.
- Enables migration testing (import historical transcripts into fallback provider).
- Compliance backup (GDPR, HIPAA require data retention).

**Example**:
- Fireflies user exports all transcripts monthly (JSON format).
- If Fireflies is acquired by Salesforce → transcripts are preserved locally.
- Import transcripts into Otter, Fathom, or custom build.

---

### Strategy 4: Prefer Standard Formats

**Description**: Choose providers with JSON/SRT export (standard formats) over proprietary formats.

**Ranking by Data Portability**:

| Provider | Export Formats | Portability Score |
|----------|----------------|-------------------|
| **Whisper API** | JSON (API response) | 5/5 (best) |
| **Deepgram** | JSON (API response), SRT | 5/5 (best) |
| **AssemblyAI** | JSON (API response), SRT | 5/5 (best) |
| **Rev AI** | JSON (API response), TXT | 4/5 (good) |
| **Fathom** | PDF, TXT, (likely JSON) | 3/5 (moderate) |
| **Otter** | PDF, TXT, SRT | 3/5 (moderate) |
| **Fireflies** | PDF, TXT, JSON (Enterprise) | 4/5 (good) |
| **Grain** | PDF, TXT, video clips (Stories) | 3/5 (moderate, proprietary Stories format) |

**Benefits**:
- JSON format preserves metadata (timestamps, confidence scores, speaker labels).
- SRT format is universal subtitle format (import into YouTube, Premiere Pro, DaVinci Resolve).

---

### Strategy 5: Avoid Long-Term Contracts in Fast-Moving Tech

**Recommendation by Provider**:

| Provider | Max Contract Length | Rationale |
|----------|---------------------|-----------|
| **Whisper, Deepgram, AssemblyAI, Rev AI** | Month-to-month or annual | API pricing is stable; no lock-in risk |
| **Fathom** | Month-to-month or annual | Low lock-in (2.1/5), recent Series A reduces shutdown risk |
| **Otter** | Annual acceptable | Market leader, strong funding; 3-year contracts risky due to freemium unsustainability |
| **Fireflies** | Month-to-month or annual | Acquisition risk (60-70%); avoid 3-year contracts |
| **Grain** | Month-to-month only | Highest acquisition risk (70-80%); product may be sunset post-HubSpot acquisition |

**Rationale**: Technology shifts accelerate (Whisper released 2022, dominant by 2024 = 2-year cycle). 3-year contracts made in 2025 may become obsolete by 2027 due to vendor acquisition, product sunset, or Whisper commoditization.

---

## Migration Cost Summary

| Migration Path | Time Estimate | Cost Estimate | Primary Challenge |
|----------------|---------------|---------------|-------------------|
| **SaaS → SaaS** | 6-12 hours | $300-1,200 | CRM integration differences, team retraining |
| **SaaS → API** | 20-40 hours | $3,000-10,000 | Building meeting bot replacement, UI development |
| **API → SaaS** | 4-8 hours | $400-800 | Sunk cost write-off, subscription cost increase |
| **API → API** | 8-16 hours | $800-2,400 | Code changes, testing, accuracy validation |

### Migration Cost Breakdown (SaaS → API Example)

| Activity | Hours | Cost @ $100/hr |
|----------|-------|----------------|
| Data export from SaaS | 2-4 | $200-400 |
| Custom workflow development | 12-24 | $1,200-2,400 |
| Meeting bot replacement (optional) | 4-8 | $400-800 |
| CRM integration | 2-4 | $200-400 |
| Testing & deployment | 4-8 | $400-800 |
| **Total** | **20-40** | **$3,000-10,000** |

---

## Strategic Recommendations

### For Small Teams (<10 users, <1,000 hours/year):

**Recommendation**: Prefer SaaS platforms with minimal lock-in (Fathom 2.1/5, Otter 2.6/5).

**Rationale**: Low switching cost (6-12 hours, $300-1,200) makes vendor churn acceptable. Focus on features, pricing (S1-S3 research) over long-term viability.

**Mitigation**: Monthly export of transcripts (TXT, JSON formats), month-to-month contracts.

---

### For Mid-Size Teams (10-30 users, 1,000-5,000 hours/year):

**Recommendation**: Balance lock-in risk with CRM integration needs.

**Options**:
- **If HubSpot CRM**: Grain (3.4/5 lock-in) acceptable for 1-3 years, plan migration to Fireflies or native HubSpot features by 2027-2028.
- **If Salesforce CRM**: Fireflies (2.9/5 lock-in) acceptable, prefer annual contracts (avoid 3-year).
- **If no CRM**: Otter (2.6/5 lock-in) or Fathom (2.1/5 lock-in).

**Mitigation**: Monthly export, multi-provider testing (fallback provider), avoid 3-year contracts.

---

### For Enterprise (50+ users, 5,000+ hours/year):

**Recommendation**: Build API with abstraction layer to minimize lock-in (1.1-1.4/5).

**Rationale**: High volume (5,000+ hours/year) justifies custom build ($3,000-10,000 upfront). Abstraction layer reduces future migration cost from 8-16 hours to 2-4 hours (80% reduction).

**Options**:
- **Primary API**: Whisper (1.1/5 lock-in, $0.36/hour, 99 languages).
- **Fallback API**: AssemblyAI (1.4/5 lock-in, $0.37/hour, PII redaction) or Deepgram (1.1/5 lock-in, $0.258/hour, real-time).

**Mitigation**: Abstraction layer, multi-provider testing quarterly, avoid SaaS platforms (medium lock-in 2.6-3.4/5).

---

## Revision History

| Date | Changes |
|------|---------|
| 2025-11-24 | Initial lock-in risk analysis and migration playbooks |
