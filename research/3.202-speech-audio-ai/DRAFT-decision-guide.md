# Domain Explainer: Speech & Audio AI Services

**Audience**: Business decision-makers, non-technical founders, consultants
**Purpose**: Explain meeting transcription and audio AI platforms in business terms
**Reading time**: 5-7 minutes

---

## What is this category?

**Speech & Audio AI** encompasses platforms and APIs that convert spoken audio (meetings, calls, podcasts, interviews) into text transcripts, then extract insights like summaries, action items, and key topics.

**The core promise**: Automate the tedious work of note-taking, allow teams to focus on conversations, and create searchable records of verbal discussions.

---

## Why does this matter for your business?

### The Manual Status Quo

Without speech AI:
- **Meeting participants** split attention between conversation and note-taking
- **Post-meeting**: Someone spends 15-30 minutes writing meeting notes
- **Knowledge loss**: Details forgotten, action items missed
- **Non-searchable**: Can't find "what did we decide about X in Q2?"

**Time cost**: 2-4 hours/week per person with 5+ meetings/week

### The Automated Alternative

With speech AI platforms:
1. **Bot joins meeting** (Zoom, Google Meet, Teams) automatically from calendar
2. **Real-time transcription** creates verbatim record while meeting happens
3. **AI summarization** generates meeting notes, action items, decisions within minutes
4. **Searchable archive** allows searching across all meetings ("pricing discussion")

**Time savings**: 80-90% reduction in manual note-taking work

---

## Two Paths: SaaS Platform vs Custom API Pipeline

### Path A: SaaS Meeting Platform

**Examples**: Fireflies.ai ($10/mo), Otter.ai ($17/mo), Grain ($15/mo)

**How it works**:
- Grant platform access to your Google/Outlook calendar
- Platform sends "meeting bot" to auto-join scheduled meetings
- Bot records audio, transcribes in real-time, generates AI summary
- Web dashboard shows all meeting transcripts, searchable, shareable

**Pros**:
- ✅ **Zero setup**: Connect calendar, start transcribing same day
- ✅ **Automatic**: Bot joins every meeting, no manual intervention
- ✅ **Collaboration features**: Share clips, comment on transcripts, team workspaces
- ✅ **Flat pricing**: $10-20/user/month regardless of meeting volume

**Cons**:
- ❌ **Privacy concerns**: Audio uploaded to platform servers
- ❌ **Bot visibility**: Every meeting has visible "Fireflies Notetaker" participant
- ❌ **Limited customization**: Stuck with platform's summary format, UI
- ❌ **Higher cost at scale**: $200/mo for 10 users vs $50/mo for custom API

**Best for**: Small teams (1-10 users), non-sensitive meetings, need convenience over customization

---

### Path B: Custom API Pipeline

**Examples**: Whisper API ($0.006/min) + Claude ($3/M tokens) for summarization

**How it works**:
- Manually upload meeting recordings to Whisper API
- Receive transcript JSON file
- Send transcript to LLM API (Claude, GPT-4) with "summarize this meeting" prompt
- Store results in your own database/notes system

**Pros**:
- ✅ **60-80% cheaper** at high volume (100+ hours/month)
- ✅ **Privacy control**: Audio never leaves your infrastructure if using self-hosted Whisper
- ✅ **Custom workflows**: Integrate with your CRM, task manager, custom prompts
- ✅ **No bot visibility**: Process recordings after meeting ends

**Cons**:
- ❌ **Manual upload**: Must remember to record meetings, upload files
- ❌ **Engineering required**: Build API integration, storage, UI (20-40 hours)
- ❌ **No real-time transcription**: Process after meeting ends
- ❌ **Maintenance burden**: Update code when APIs change

**Best for**: High-volume users (100+ hours/month), privacy-sensitive industries, technical teams

---

## Cost Comparison

### Scenario: 5 consultants, 20 meetings/week, 1-hour average

**SaaS Platform (Fireflies.ai)**:
- Cost: $50/month (5 users × $10/user)
- **Annual**: $600/year
- Includes: Unlimited meetings, automatic transcription, team workspace

**Custom API (Whisper + Claude)**:
- Whisper: 20 hours/week × 4.3 weeks × $0.36/hour = $31/month
- Claude: 20 meetings/week × 8K tokens × 4.3 weeks × $3/M = $2/month
- **Annual**: $396/year ($33/month)
- **Savings**: 34% cheaper ($204/year saved)
- Excludes: Engineering time (20-40 hours initial setup)

**Break-even**: Custom API saves money IF you have:
- 50+ hours/month transcription volume (Whisper cost < SaaS subscription)
- Engineering resources to build/maintain (20-40 hours upfront, 2-4 hours/year maintenance)

**Rule of thumb**: SaaS wins for small teams (<10 users), custom APIs win for high volume (>100 hours/month) or privacy-sensitive use cases.

---

## Key Decision Factors

### 1. **Privacy & Compliance**

**Question**: Can meeting audio be uploaded to third-party servers?

- **Healthcare (HIPAA)**: May require self-hosted Whisper + local LLM
- **Legal (attorney-client privilege)**: Custom pipeline mandatory
- **General business**: SaaS platforms acceptable with BAA (Business Associate Agreement)
- **Public meetings**: No privacy concerns, SaaS platforms fine

**Privacy spectrum** (most to least private):
1. Self-hosted Whisper + local LLM (audio never leaves your infrastructure)
2. Custom API with encryption in transit (Whisper API with immediate deletion policy)
3. SaaS platform with data residency guarantees (European servers for GDPR)
4. Standard SaaS platform (audio stored indefinitely on US servers)

---

### 2. **Meeting Volume**

**SaaS platforms** have flat pricing ($10-20/user/month):
- ✅ **Cost-effective** for low/medium volume (1-20 hours/user/month)
- ❌ **Expensive** for high volume (50+ hours/user/month)

**Custom APIs** have usage-based pricing ($0.006-0.02/min):
- ❌ **Inefficient** for low volume (engineering overhead not worth $5/month savings)
- ✅ **Big savings** for high volume (100+ hours/month = $200+ SaaS vs $50 API)

**Break-even point**: ~50 hours/month per user (custom API becomes cheaper)

---

### 3. **Accuracy Requirements**

**Whisper API** (OpenAI) is state-of-the-art (2024):
- 95-98% accuracy on clear audio, standard accents
- 85-90% accuracy on poor audio, strong accents, technical jargon

**SaaS platforms** use various backends:
- Premium platforms (Otter, Fireflies) use Whisper or equivalent
- Budget platforms may use older models (90-93% accuracy)

**Test before committing**: Upload 3-5 real meeting recordings, compare accuracy across platforms.

**Accuracy failure modes**:
- **Technical jargon**: "Kubernetes" transcribed as "cue burn it ease"
- **Strong accents**: Non-native English speakers misunderstood
- **Crosstalk**: Multiple speakers talking simultaneously creates gibberish
- **Poor audio**: Phone calls, bad microphones reduce accuracy 10-20%

**Mitigation**: Use high-quality microphones, avoid crosstalk, create custom vocabulary lists (platform-specific feature)

---

### 4. **Integration Requirements**

**SaaS platforms** offer pre-built integrations:
- **Calendar**: Google Calendar, Outlook (auto-join meetings)
- **Video**: Zoom, Google Meet, Microsoft Teams, Webex
- **CRM**: Salesforce, HubSpot (sync call notes to customer records)
- **Task management**: Asana, Monday, Notion (create action items)

**Custom APIs** require engineering:
- **Calendar integration**: Build OAuth flow to read calendar events (8-12 hours)
- **Recording capture**: Integrate with Zoom API, Teams Graph API (12-16 hours)
- **CRM sync**: Build custom sync logic (8-16 hours per CRM)

**Decision**: If you need 3+ integrations, SaaS platform engineering savings (40-60 hours) outweigh subscription cost for first 2-3 years.

---

### 5. **Use Case Specialization**

Different platforms optimize for different use cases:

| Platform | Best For | Key Feature |
|----------|----------|-------------|
| **Fireflies.ai** | General meetings | Best calendar integration, team collaboration |
| **Otter.ai** | Real-time collaboration | Live transcript sharing, in-meeting notes |
| **Grain** | Sales calls | Video clip creation, coaching tools, CRM sync |
| **Fathom** | Privacy-focused teams | Free tier, no bot visibility option |
| **Whisper API** | Custom workflows | Cheapest, most flexible, privacy control |
| **AssemblyAI** | Developers | Best API docs, real-time streaming |
| **Deepgram** | High-volume transcription | Fastest processing, bulk discounts |
| **Rev AI** | Maximum accuracy | Human transcription option (99% accuracy, $1.20/hour) |

---

## Technology Evolution (5-Year Outlook)

### 2024-2025: Current State
- Whisper API is state-of-the-art for transcription (95-98% accuracy)
- LLM summarization quality varies (GPT-4 > Claude > GPT-3.5)
- SaaS platforms commoditize on convenience, not core accuracy

### 2026-2027: Expected Changes
- **Accuracy convergence**: All platforms reach 97-99% accuracy (Whisper-quality models commoditize)
- **Real-time improvement**: Real-time transcription latency drops from 2-3 sec to <1 sec
- **Multimodal**: Platforms analyze video (body language, screen shares) not just audio
- **Pricing deflation**: API costs drop 30-50% as compute gets cheaper

### 2028-2030: Transformative Shifts
- **AI meeting participants**: Bots don't just transcribe, they ask questions, synthesize viewpoints
- **Enterprise consolidation**: M&A consolidates 10+ platforms into 3-4 dominant players
- **Open-source competitive**: Self-hosted Whisper + Llama rivals commercial platforms
- **Regulatory pressure**: GDPR-style meeting consent laws require explicit opt-in

**Strategic implication**: Avoid 3+ year SaaS contracts (technology will shift dramatically), prefer month-to-month or annual contracts.

---

## Common Pitfalls

### 1. **Not testing accuracy with real meetings**
- ❌ **Mistake**: Choose platform based on marketing claims
- ✅ **Fix**: Upload 5 real meeting recordings, compare transcripts side-by-side

### 2. **Ignoring meeting consent**
- ❌ **Mistake**: Auto-record all meetings without asking
- ✅ **Fix**: Announce recording at start ("This meeting is being recorded for notes"), get verbal consent

### 3. **Over-relying on AI summaries**
- ❌ **Mistake**: Trust AI summary without reviewing transcript
- ✅ **Fix**: Spot-check 10-20% of summaries for accuracy, train team to review critical decisions

### 4. **Vendor lock-in**
- ❌ **Mistake**: Store 2 years of meeting transcripts in proprietary format
- ✅ **Fix**: Export transcripts monthly to JSON/plain text, store in your own archive

### 5. **Privacy violations**
- ❌ **Mistake**: Record client calls with attorney-client privilege, upload to SaaS platform
- ✅ **Fix**: Document privacy policy (what gets recorded, where stored, retention period), get client consent

---

## Decision Framework

**Use SaaS Platform IF**:
- ✅ Small team (1-10 users)
- ✅ Low/medium volume (<50 hours/month per user)
- ✅ Need convenience (calendar integration, auto-join bots)
- ✅ No privacy concerns (general business meetings)
- ✅ Non-technical team (no engineering resources)

**Use Custom API Pipeline IF**:
- ✅ High volume (100+ hours/month)
- ✅ Privacy-sensitive industry (healthcare, legal, finance)
- ✅ Custom workflow needs (integrate with proprietary CRM, custom prompts)
- ✅ Technical team (have engineering resources for 20-40 hour build)
- ✅ Cost-conscious (60-80% savings at scale)

**Hybrid Approach** (use both):
- SaaS platform for day-to-day meetings (convenience)
- Custom API for sensitive/high-volume transcription (privacy + cost)
- Example: Fireflies for internal team meetings, Whisper API for client calls

---

## Next Steps

After reading this explainer:

1. **Estimate volume**: How many meeting hours/month do you need transcribed?
2. **Assess privacy**: Are there HIPAA, attorney-client, or trade secret concerns?
3. **Test accuracy**: Upload 3-5 real meeting recordings to 2-3 platforms (free trials)
4. **Calculate TCO**: Compare SaaS subscription vs custom API cost for your volume
5. **Review research**: Read S1-S4 discovery documents for detailed platform comparisons

**Research roadmap**:
- **S1 (Rapid)**: 8 provider overviews (2-3 hours reading)
- **S2 (Comprehensive)**: Feature matrix, pricing TCO, accuracy benchmarks (4-6 hours reading)
- **S3 (Need-Driven)**: 5 use case scenarios matching your context (2-4 hours reading)
- **S4 (Strategic)**: Vendor viability, lock-in mitigation, 5-year outlook (2-3 hours reading)

**Time investment**: 10-16 hours reading research → save hundreds of hours/year in meeting notes + make informed $600-6,000/year spending decision.

---

**Document status**: Generic research (no client-specific recommendations)
**For client-specific recommendations**: See `business/client-engagements/[client-name]/`
**Last updated**: November 24, 2025
