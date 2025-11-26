# 3.202: Speech & Audio AI Services

**Category**: AI & Advanced Capabilities (Tier 3)
**Status**: ✅ Complete (Nov 24, 2025)
**Research Method**: MPSE v3.0 (Multi-Provider Strategic Evaluation)
**Research Time**: 22 hours (S1: 3h, S2: 6h, S3: 8h, S4: 5h)

---

## Quick Links

- **[Domain Explainer](DOMAIN_EXPLAINER.md)** ✅ - Technical terminology guide (140+ terms, 15-20 min read)
- **[Metadata](metadata.yaml)** ✅ - Experiment tracking, scope, research questions
- **[S1: Rapid Discovery](01-discovery/S1-rapid/)** ✅ - Platform overviews (8 providers)
- **[S2: Comprehensive Analysis](01-discovery/S2-comprehensive/)** ✅ - Feature matrix, pricing TCO, benchmarks
- **[S3: Need-Driven Scenarios](01-discovery/S3-need-driven/)** ✅ - 6 use case scenarios
- **[S4: Strategic Selection](01-discovery/S4-strategic/)** ✅ - Vendor viability, lock-in, 5-year outlook

---

## What is this research?

**Speech & Audio AI** platforms and APIs convert spoken audio (meetings, calls, podcasts) into searchable text transcripts and AI-generated summaries, action items, insights.

**Two paths**:
1. **SaaS Meeting Platforms** - Fireflies.ai, Otter.ai, Grain (auto-join meetings, $10-20/mo)
2. **Custom API Pipelines** - Whisper API + Claude summarization (60-80% cheaper at scale)

**This research answers**:
- Which platform for which use case? (privacy, volume, accuracy requirements)
- SaaS convenience vs API cost savings - when does custom pipeline pay off?
- Accuracy comparison - how good is Whisper API vs SaaS platforms?
- Privacy considerations - HIPAA, GDPR, attorney-client privilege compliance?
- Lock-in risk - can you switch platforms, export transcripts easily?

---

## Research Progress

### ✅ ALL STAGES COMPLETE (Nov 24, 2025)

**Total**: 35 documents, ~500 KB research output, 22 hours research time

- [x] **Metadata & Navigation** (2 files)
  - metadata.yaml - Experiment tracking, completion summary
  - README.md - This file

- [x] **Domain Explainer** (1 file) - Created AFTER S1-S4 per MPSE methodology
  - DOMAIN_EXPLAINER.md - 140+ technical terms explained in business-friendly language

- [x] **S1: Rapid Discovery** (10 files, 3 hours)
  - 8 provider profiles (Fireflies, Otter, Grain, Fathom, Whisper, AssemblyAI, Deepgram, Rev AI)
  - Approach + Recommendations synthesis

- [x] **S2: Comprehensive Analysis** (7 files, 6 hours)
  - Feature matrix (30+ features × 8 providers)
  - Pricing TCO (5 scenarios, $0-$68,400 3-year range)
  - Accuracy benchmarks (4-7% WER range)
  - Integration complexity (6-400 hours dev effort)
  - Privacy compliance (HIPAA, GDPR, SOC 2, ISO 27001, PCI-DSS)
  - Synthesis

- [x] **S3: Need-Driven Scenarios** (8 files, 8 hours)
  - 6 use case scenarios (consultant, privacy, sales, research, content, multilingual)
  - ROI calculations (262x to ∞ return)
  - Code examples (Python for Whisper API, Deepgram, translation pipelines)
  - Decision trees + Implementation guides
  - Synthesis

- [x] **S4: Strategic Selection** (6 files, 5 hours)
  - Vendor viability (5-year/10-year survival 40-95%)
  - Lock-in mitigation (1.1-3.4/5 scale)
  - Whisper commoditization (30-50% pricing deflation by 2030)
  - AI trajectory (2025-2030 evolution)
  - Time horizon planning
  - Synthesis

---

## Key Questions This Research Answers

1. **SaaS vs API**: When does custom Whisper API pipeline pay off vs SaaS platform?
   - Answer preview: Break-even at ~50 hours/month (SaaS $50-100/mo vs API $20-30/mo)

2. **Accuracy**: How good is Whisper API vs commercial platforms?
   - Answer preview: Whisper is state-of-the-art (95-98%), most premium SaaS use Whisper backend

3. **Privacy**: Can healthcare/legal industries use SaaS platforms?
   - Answer preview: HIPAA requires BAA (some platforms offer), attorney-client needs self-hosted

4. **Cost**: What's the price range for 20 meetings/week?
   - Answer preview: SaaS $10-20/user/mo flat vs API $0.006/min usage-based

5. **Lock-in**: Can you export 2 years of transcripts and switch platforms?
   - Answer preview: Most platforms allow JSON/TXT export, migration effort 5-20 hours

---

## Research Scope

### Included
- ✅ Meeting transcription platforms (Fireflies, Otter, Grain, Fathom)
- ✅ Speech-to-text APIs (Whisper API, AssemblyAI, Deepgram, Rev AI)
- ✅ Real-time transcription services
- ✅ AI summarization and action item extraction
- ✅ Speaker diarization (who said what)
- ✅ Meeting platform integrations (Zoom, Google Meet, Teams)

### Excluded
- ❌ Text-to-speech / voice synthesis (separate category)
- ❌ Voice assistants / conversational AI (separate category)
- ❌ Self-hosted speech models without API service
- ❌ Call center analytics (specialized vertical)

---

## Providers Researched

### Tier 1: SaaS Meeting Platforms (4 providers)
1. **Fireflies.ai** - Market leader, $10/mo, best calendar integration
2. **Otter.ai** - Consumer favorite, $17/mo, real-time collaboration
3. **Grain** - Sales/coaching focus, $15/mo, video clip creation
4. **Fathom** - Free tier, privacy-focused, CRM integrations

### Tier 2: Speech-to-Text APIs (4 providers)
5. **OpenAI Whisper API** - State-of-the-art, $0.006/min ($0.36/hour)
6. **AssemblyAI** - Developer-friendly, $0.00025/sec ($0.90/hour), real-time
7. **Deepgram** - Fast + accurate, $0.0125/min ($0.75/hour), bulk discounts
8. **Rev AI** - Human transcription option, $0.02/min ($1.20/hour), 99% accuracy

---

## Integration Relationships

**Upstream** (feeds into this research):
- **3.200: LLM APIs** - Meeting summaries generated by Claude/GPT-4 after Whisper transcription

**Downstream** (this research feeds into):
- **3.130: Personal Productivity / GTD** - Meeting transcripts create action items for task management
- **3.136: Meeting Transcription** - Overlapping category (may merge or cross-reference)

**Parallel** (related research):
- **3.200: LLM APIs** - Summarization backend for meeting notes
- **3.501: CRM Platforms** - Sales call transcription integrates with CRM

---

## How to Use This Research

### For Decision-Makers (Non-Technical)
1. **Start**: Review S1 recommendations synthesis (quick overview of 8 providers)
2. **Estimate volume**: How many meeting hours/month need transcription?
3. **Review S3**: Find scenario matching your use case (consultant, sales, researcher)
4. **Compare options**: S2 feature matrix + pricing TCO for your volume
5. **Understand terms**: Read DOMAIN_EXPLAINER.md for technical vocabulary (created after S1-S4)
6. **Test before buying**: Upload 3-5 real meetings to 2-3 platforms (free trials)

### For Technical Teams (Engineers)
1. **Start**: S1 API provider profiles (Whisper, AssemblyAI, Deepgram, Rev AI)
2. **Deep dive S2**: Integration complexity, API documentation quality
3. **Custom pipeline**: S3 "consultant meetings" scenario includes Whisper API + Claude code
4. **Lock-in analysis**: S4 transcript export formats, platform switching costs

### For Researchers (Strategic Analysis)
1. **Read S1**: Provider overviews for market landscape
2. **Read S4**: Vendor viability, Whisper commoditization, 5-year AI trajectory
3. **Synthesis docs**: Cross-cutting insights across S1-S4

---

## Document Status

**Generic research**: No client-specific recommendations (maintained in `research/3.202-speech-audio-ai/`)

**Client-specific application**: Stored separately in `business/client-engagements/[client-name]/`

**Last updated**: November 24, 2025
**Version**: 1.0 (MPSE v3.0 methodology)
