# Feature Matrix: Comprehensive Comparison
## Experiment 3.202: Speech & Audio AI Services

**Research Phase**: S2 - Comprehensive Analysis
**Date**: 2025-11-24
**Source**: S1 provider profiles + web research (Nov 2024)

---

## Legend

- ✅ **Full Support** - Feature fully available
- ❌ **Not Available** - Feature not offered
- ⚠️ **Partial/Limited** - Feature available with restrictions or on specific tiers
- 💰 **Paid Tier Only** - Requires paid plan (noted in cell)
- 🏢 **Enterprise Only** - Requires Enterprise tier or custom contract
- **Numbers** - Specific metrics (e.g., language count, max speakers)

---

## SAAS MEETING PLATFORMS vs APIS

### Platform Categories
- **SaaS Platforms**: Fireflies, Otter, Grain, Fathom (meeting bots with built-in features)
- **APIs**: Whisper, AssemblyAI, Deepgram, Rev AI (developer-focused, build-your-own)

---

## 1. CORE TRANSCRIPTION FEATURES

| Feature | Fireflies | Otter | Grain | Fathom | Whisper API | AssemblyAI | Deepgram | Rev AI |
|---------|-----------|-------|-------|--------|-------------|------------|----------|---------|
| **Real-time Transcription** | ✅ Live | ✅ Live | ❌ Post-call | ❌ Post-call | ❌ Batch only | ✅ Streaming | ✅ Streaming | ✅ Streaming |
| **Async/Batch Transcription** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Speaker Diarization** | ✅ Auto | ✅ Auto | ✅ Auto | ✅ Auto | ❌ Native (⚠️ WhisperX) | ✅ Built-in | ✅ Built-in | ✅ 8 EN / 6 Non-EN |
| **Max Speakers Supported** | Not disclosed | Not disclosed | Not disclosed | Not disclosed | N/A (3rd party) | Not disclosed | Not disclosed | 8 (EN) / 6 (Other) |
| **Languages Supported** | 69+ | 3 (EN/FR/ES) | Not disclosed | 28 | 99 | 99 | 30+ | 58+ |
| **Automatic Language Detection** | ✅ | ❌ Manual | Not disclosed | ⚠️ Limited | ✅ | ✅ 40+ langs | ✅ | ✅ |
| **Transcription Accuracy (WER)** | 95%+ claimed | 95%+ claimed | High (AssemblyAI) | 95% claimed | ~92% (8% WER) | 30% better than Whisper | 30% WER reduction | 96%+ claimed |
| **Custom Vocabulary** | ✅ Pro+ | ✅ Pro+ | ✅ Business+ | ⚠️ Limited | ✅ Prompts | ✅ Included | ✅ Keyword boost | ✅ 6,000 words (Enterprise) |
| **Word-level Timestamps** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Confidence Scores** | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ |
| **Processing Speed** | Standard | Standard | Fast (AssemblyAI) | 30 sec turnaround | Slow (~40% duration) | Fast (23s / 30min) | Fastest (5s / 14min) | Fast |

---

## 2. AI-POWERED FEATURES

| Feature | Fireflies | Otter | Grain | Fathom | Whisper API | AssemblyAI | Deepgram | Rev AI |
|---------|-----------|-------|-------|--------|-------------|------------|----------|---------|
| **AI Summarization** | ✅ GPT-powered | ✅ Auto | ✅ Custom templates | ✅ GPT-4 (5 free) | ❌ (Claude separately) | ✅ Built-in | ⚠️ Limited | ✅ |
| **Action Item Extraction** | ✅ Auto | ✅ Auto | ✅ Auto | ✅ Auto | ❌ | ✅ Auto | ❌ | ✅ |
| **Sentiment Analysis** | ✅ | ❌ | ✅ Business+ | ❌ | ❌ | ✅ Sentence-level | ✅ | ✅ EN only |
| **Topic Detection** | ✅ Tracking | ❌ | ✅ Trends | ❌ | ❌ | ✅ Classification | ⚠️ Basic | ✅ |
| **Keyword/Competitor Tracking** | ✅ Analytics | ⚠️ Search | ✅ Buying signals | ⚠️ Tags | ❌ | ✅ Entity detection | ✅ Keyword boost | ✅ |
| **PII Redaction** | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ Auto (SSN, CC, etc.) | ❌ | ❌ |
| **Content Moderation** | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ Detect sensitive | ❌ | ❌ |
| **Meeting Search (Natural Language)** | ✅ AskFred | ✅ Otter Chat | ✅ | ✅ Teams+ | ❌ | ✅ LeMUR | ✅ Deep Search | ✅ |
| **Custom AI Prompts** | ⚠️ Templates | ❌ | ✅ Business+ | ⚠️ Templates | ✅ Via API | ✅ LeMUR | ❌ | ⚠️ Limited |
| **Translation** | ❌ | ❌ | ❌ | ❌ | ✅ To English | ⚠️ Separate API | ❌ | ✅ |

---

## 3. CALENDAR & VIDEO PLATFORM INTEGRATIONS

| Feature | Fireflies | Otter | Grain | Fathom | Whisper API | AssemblyAI | Deepgram | Rev AI |
|---------|-----------|-------|-------|--------|-------------|------------|----------|---------|
| **Google Calendar** | ✅ Auto-join | ✅ Auto-join | ✅ Auto-join | ✅ Auto-join | ❌ (Custom build) | ❌ | ❌ | ❌ |
| **Outlook Calendar** | ✅ Auto-join | ✅ Auto-join | ✅ Auto-join | ✅ Auto-join | ❌ | ❌ | ❌ | ❌ |
| **Zoom** | ✅ Native | ✅ Native | ✅ Native | ✅ Native (origin) | ❌ | ❌ | ❌ | ❌ |
| **Google Meet** | ✅ Native | ✅ Native | ✅ Native | ✅ Native | ❌ | ❌ | ❌ | ❌ |
| **Microsoft Teams** | ✅ Native | ✅ Native | ✅ Native | ✅ Native | ❌ | ❌ | ❌ | ❌ |
| **Webex** | ✅ | ✅ | ✅ | ⚠️ Limited | ❌ | ❌ | ❌ | ❌ |
| **Total Platforms Supported** | 80+ | 3 main | 3 main | 3 main | N/A | N/A | N/A | N/A |
| **Meeting Bot Visibility** | Visible | Visible | Visible | Visible | N/A | N/A | N/A | N/A |
| **Audio/Video Upload** | ✅ | ✅ 3-10 files/mo | ⚠️ Limited | ⚠️ Limited | ✅ 25MB max | ✅ Unlimited | ✅ | ✅ |

---

## 4. CRM & PRODUCTIVITY INTEGRATIONS

| Feature | Fireflies | Otter | Grain | Fathom | Whisper API | AssemblyAI | Deepgram | Rev AI |
|---------|-----------|-------|-------|--------|-------------|------------|----------|---------|
| **Salesforce** | ✅ 💰Business+ | ⚠️ Limited | ✅ Business+ | ✅ Export | ❌ (Custom) | ❌ | ❌ | ❌ |
| **HubSpot** | ✅ 💰Business+ | ⚠️ Limited | ✅ Deep native | ✅ Sync | ❌ (Custom) | ❌ | ❌ | ❌ |
| **Pipedrive** | ✅ Zapier | ⚠️ Zapier | ⚠️ Zapier | ⚠️ Zapier | ❌ | ❌ | ❌ | ❌ |
| **Slack** | ✅ Share/notify | ✅ Share | ✅ Clips | ✅ Share | ❌ (Custom) | ❌ | ❌ | ❌ |
| **Notion** | ✅ Sync | ✅ Sync | ⚠️ Limited | ✅ Sync | ❌ (Custom) | ❌ | ❌ | ❌ |
| **Asana** | ✅ Tasks | ❌ | ⚠️ Zapier | ✅ Tasks | ❌ (Custom) | ❌ | ❌ | ❌ |
| **Trello** | ✅ Cards | ❌ | ⚠️ Zapier | ✅ Cards | ❌ (Custom) | ❌ | ❌ | ❌ |
| **Zapier** | ✅ 80+ apps | ✅ 1000+ apps | ✅ | ✅ 1000+ apps | ❌ (Custom) | ❌ | ❌ | ❌ |
| **API Access** | 🏢 Enterprise | ❌ None | ❌ None | ❌ None | ✅ Core product | ✅ Core product | ✅ Core product | ✅ Core product |

**Note**: APIs require custom integration for CRM/productivity tools. SaaS platforms offer pre-built connectors.

---

## 5. COLLABORATION & TEAM FEATURES

| Feature | Fireflies | Otter | Grain | Fathom | Whisper API | AssemblyAI | Deepgram | Rev AI |
|---------|-----------|-------|-------|--------|-------------|------------|----------|---------|
| **Team Workspaces** | ✅ Business+ | ✅ Pro+ | ✅ Business+ | ✅ Teams+ | ❌ | ❌ | ❌ | ❌ |
| **Comments/Annotations** | ✅ Threads | ✅ Inline | ✅ Tags | ✅ Tags | ❌ | ❌ | ❌ | ❌ |
| **Highlights/Bookmarks** | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| **Video Clip Creation** | ✅ Business+ | ❌ | ✅ Unique | ✅ | ❌ | ❌ | ❌ | ❌ |
| **Clip Stories (Multi-call)** | ❌ | ❌ | ✅ Unique | ❌ | ❌ | ❌ | ❌ | ❌ |
| **Assign Action Items** | ✅ | ✅ Pro+ | ✅ | ⚠️ Export | ❌ | ❌ | ❌ | ❌ |
| **Cross-meeting Search** | ✅ Analytics | ✅ Pro+ | ✅ Trends | ✅ Teams+ | ❌ | ❌ | ❌ | ❌ |
| **Mobile Apps** | ✅ iOS/Android | ✅ iOS/Android | ⚠️ Limited docs | ⚠️ Limited docs | ❌ | ❌ | ❌ | ❌ |
| **Admin Controls** | ✅ Business+ | ✅ Business+ | ✅ Enterprise | ✅ Pro+ | N/A | N/A | N/A | N/A |
| **Usage Analytics** | ✅ Team analytics | ✅ Business+ | ✅ Business+ | ⚠️ Limited | N/A | N/A | N/A | N/A |

---

## 6. EXPORT & DATA PORTABILITY

| Feature | Fireflies | Otter | Grain | Fathom | Whisper API | AssemblyAI | Deepgram | Rev AI |
|---------|-----------|-------|-------|--------|-------------|------------|----------|---------|
| **JSON Export** | ✅ | ⚠️ Limited | ⚠️ Limited | ⚠️ Limited | ✅ Native | ✅ Native | ✅ Native | ✅ Native |
| **Plain Text (TXT)** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **PDF Export** | ✅ | ✅ | ⚠️ Via print | ✅ | ❌ | ⚠️ Generate | ⚠️ Generate | ⚠️ Generate |
| **SRT Subtitles** | ✅ | ✅ | ⚠️ Limited | ⚠️ Limited | ✅ Generate | ✅ Generate | ✅ Generate | ✅ Generate |
| **VTT Subtitles** | ✅ | ⚠️ SRT only | ⚠️ Limited | ⚠️ Limited | ✅ Generate | ✅ Generate | ✅ Generate | ✅ Generate |
| **CSV/Excel** | ✅ Analytics | ❌ | ⚠️ Limited | ❌ | ❌ | ⚠️ Custom | ⚠️ Custom | ⚠️ Custom |
| **Audio/Video Download** | ✅ Business+ | ⚠️ Limited | ✅ | ⚠️ Limited | N/A | N/A | N/A | N/A |
| **Shareable Links** | ✅ | ✅ | ✅ Clips | ✅ Clips | ❌ | ❌ | ❌ | ❌ |
| **Embed Codes** | ⚠️ Limited | ❌ | ⚠️ Limited | ❌ | ❌ | ❌ | ❌ | ❌ |

---

## 7. PRIVACY & COMPLIANCE

| Feature | Fireflies | Otter | Grain | Fathom | Whisper API | AssemblyAI | Deepgram | Rev AI |
|---------|-----------|-------|-------|--------|-------------|------------|----------|---------|
| **SOC 2 Type II** | ✅ | ✅ | ⚠️ Not disclosed | ✅ | ✅ OpenAI | ✅ | ⚠️ Not disclosed | ✅ |
| **HIPAA BAA Available** | ✅ 🏢Enterprise | ⚠️ Safeguards | ⚠️ Not disclosed | ✅ | ❌ Not for PHI | ✅ | ⚠️ Not disclosed | ✅ |
| **GDPR Compliant** | ✅ | ✅ | ⚠️ Not disclosed | ✅ | ⚠️ No EU servers | ✅ EU processing | ⚠️ Not disclosed | ✅ |
| **ISO 27001** | ⚠️ Not disclosed | ✅ | ⚠️ Not disclosed | ✅ | ⚠️ Not disclosed | ⚠️ Not disclosed | ⚠️ Not disclosed | ⚠️ Not disclosed |
| **PCI-DSS** | ⚠️ Not disclosed | ⚠️ Not disclosed | ⚠️ Not disclosed | ⚠️ Not disclosed | ⚠️ Not disclosed | ✅ Level 1 (2025) | ⚠️ Not disclosed | ✅ |
| **Data Residency Options** | 🏢 US (Enterprise: Private) | ⚠️ Cloud-based | ⚠️ Not disclosed | US/Canada (AWS) | US (OpenAI) | US or EU (Dublin) | ⚠️ Not disclosed | ⚠️ Not disclosed |
| **Encryption in Transit** | ✅ TLS | ✅ TLS | ⚠️ Assumed | ✅ | ✅ HTTPS | ✅ HTTPS/TLS | ✅ | ✅ |
| **Encryption at Rest** | ✅ | ⚠️ No E2EE | ⚠️ Not disclosed | ✅ | ⚠️ Not disclosed | ✅ | ⚠️ Assumed | ✅ |
| **No Training on Customer Data** | ✅ Policy | ✅ Policy | ⚠️ Not disclosed | ✅ Contractual | ✅ Policy | ✅ Policy | ⚠️ Not disclosed | ⚠️ Assumed |
| **SSO (Single Sign-On)** | ✅ 🏢Enterprise | ⚠️ Not disclosed | ✅ 🏢Enterprise | ⚠️ Not disclosed | N/A | ✅ 🏢Enterprise | ⚠️ Not disclosed | ⚠️ Not disclosed |
| **2FA (Two-Factor Auth)** | ⚠️ Not disclosed | ✅ | ⚠️ Not disclosed | ✅ | ✅ OpenAI acct | ⚠️ Not disclosed | ⚠️ Not disclosed | ⚠️ Not disclosed |

---

## 8. PRICING & STORAGE

| Feature | Fireflies | Otter | Grain | Fathom | Whisper API | AssemblyAI | Deepgram | Rev AI |
|---------|-----------|-------|-------|--------|-------------|------------|----------|---------|
| **Free Tier** | ✅ 800min storage | ✅ 300min/mo | ⚠️ 20 meetings | ✅ Unlimited | ❌ Pay-as-go | ✅ $50 credit | ✅ $150-200 credit | ⚠️ Trial/limited |
| **Free Tier Limits** | 3 credits (desktop) | 300min/mo, 30min/call | 20 total meetings | 5 GPT-4/mo | N/A | $50 = ~135 hours | $150 = ~580 hours | Not disclosed |
| **Starting Paid Price** | $18/user/mo | $8.33/user/mo (annual) | $15/user/mo (annual) | $24/user/mo | $0.006/min | $0.00617/min (Best) | $0.0043/min | $0.035/min (std) |
| **Storage on Free** | 800 min/seat | 25 meetings | 20 meetings cap | Unlimited | N/A | N/A | N/A | N/A |
| **Storage on Paid** | Unlimited (Business+) | Extended | Extended | Unlimited | N/A | N/A | N/A | N/A |
| **Overage Charges** | ⚠️ Fair use | ⚠️ Fair use | ❌ | ❌ | ✅ Per-minute | ✅ Per-minute | ✅ Per-minute | ✅ Per-minute |
| **Enterprise Pricing** | Custom | Custom | Custom | Custom | Volume discount | Volume discount | Volume discount | $1.20/hr (start) |

---

## 9. DEVELOPER & TECHNICAL

| Feature | Fireflies | Otter | Grain | Fathom | Whisper API | AssemblyAI | Deepgram | Rev AI |
|---------|-----------|-------|-------|--------|-------------|------------|----------|---------|
| **Public API** | 🏢 Enterprise | ❌ None | ❌ None | ❌ None | ✅ Core product | ✅ Core product | ✅ Core product | ✅ Core product |
| **Official SDKs** | ⚠️ Enterprise | ❌ | ❌ | ❌ | ✅ Python, Node | ✅ Python, Node, Java | ✅ Multiple | ✅ Multiple |
| **WebSocket Streaming** | N/A | N/A | N/A | N/A | ❌ | ✅ | ✅ | ✅ |
| **Webhooks/Callbacks** | ⚠️ Enterprise | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ | ✅ |
| **Max File Size** | Platform handles | Platform handles | Platform handles | Platform handles | 25MB | Flexible | Flexible | Flexible |
| **Concurrent Requests** | N/A | N/A | N/A | N/A | Rate limited | 100 (REST) / 50 (WS) | 100 (REST) / 50 (WS) | Not disclosed |
| **Self-Hosted Option** | ❌ | ❌ | ❌ | ❌ | ✅ Open-source | ❌ | ✅ 🏢Enterprise | ❌ |
| **Documentation Quality** | Good | Good | Fair | Good | Excellent | Excellent | Excellent | Good |
| **Developer Support** | Enterprise | Limited | Limited | Limited | Community + paid | Responsive | Responsive | "Developer-friendly" |

---

## 10. USE CASE SUITABILITY

| Use Case | Fireflies | Otter | Grain | Fathom | Whisper API | AssemblyAI | Deepgram | Rev AI |
|---------|-----------|-------|-------|--------|-------------|------------|----------|---------|
| **Solo Professional** | ⚠️ (Free limited) | ⚠️ (Free limited) | ❌ (20 meetings) | ✅ Best free | ✅ Cost-effective | ⚠️ (Dev needed) | ⚠️ (Dev needed) | ⚠️ (Higher cost) |
| **Small Team (5-10)** | ✅ Pro tier | ✅ Pro tier | ✅ Business tier | ✅ Standard | ⚠️ Custom build | ⚠️ Custom build | ⚠️ Custom build | ⚠️ Custom build |
| **Sales Team + CRM** | ✅ Business+ | ⚠️ Limited CRM | ✅ Excellent (HubSpot) | ⚠️ Export only | ❌ Custom build | ❌ Custom build | ❌ Custom build | ❌ Custom build |
| **Enterprise (50+ users)** | ✅ Enterprise | ✅ Enterprise | ✅ Enterprise | ✅ Pro | ⚠️ API for scale | ✅ API for scale | ✅ API for scale | ✅ API for scale |
| **Custom Application** | ⚠️ Enterprise API | ❌ No API | ❌ No API | ❌ No API | ✅ Ideal | ✅ Ideal | ✅ Ideal | ✅ Ideal |
| **Real-time Captioning** | ✅ Live transcription | ✅ Live captions | ❌ Post-call | ❌ Post-call | ❌ | ✅ Streaming | ✅ Streaming | ✅ 1-3ms latency |
| **Compliance/HIPAA** | ✅ Enterprise BAA | ⚠️ Safeguards | ⚠️ Not disclosed | ✅ Certified | ❌ | ✅ BAA available | ⚠️ Not disclosed | ✅ BAA available |
| **Budget-Conscious** | ⚠️ Fair free tier | ⚠️ Limited free | ❌ | ✅ Best free tier | ✅ Cheapest API | ⚠️ Mid-range | ✅ Cheapest API | ❌ Higher cost |
| **Speed Critical** | ⚠️ Standard | ⚠️ Standard | ✅ Fast | ✅ 30-sec | ❌ Slowest | ✅ Fast (23s/30min) | ✅ Fastest (5s/14min) | ✅ Fast |
| **99 Languages** | ❌ (69+) | ❌ (3) | ❌ | ❌ (28) | ✅ Best | ✅ 99 langs | ⚠️ 30+ | ✅ 58+ |

---

## KEY INSIGHTS FROM FEATURE MATRIX

### SaaS Platforms: Strengths
1. **Fathom**: Best free tier (truly unlimited storage), fastest summaries (30 sec), strong compliance
2. **Fireflies**: Most comprehensive integrations (80+ platforms), team analytics, extensive AI features
3. **Grain**: Unique video clip + Stories feature, deep HubSpot integration, customer-facing focus
4. **Otter**: Real-time live captions, educational pricing, clean interface

### SaaS Platforms: Limitations
1. **No public APIs** (except Fireflies Enterprise)
2. **CRM integrations gated** (Business tier required for Fireflies, Grain)
3. **Free tiers restrictive** (except Fathom)
4. **Limited language support** (Otter only 3 languages)

### APIs: Strengths
1. **Whisper**: Cheapest ($0.006/min), 99 languages, open-source option
2. **AssemblyAI**: Most comprehensive features (PII redaction, sentiment, summarization)
3. **Deepgram**: Fastest (5s for 14min), best accuracy/speed balance, cost-effective
4. **Rev AI**: Highest accuracy claim (96%+), HIPAA BAA, hybrid AI+human option

### APIs: Limitations
1. **No meeting bot** - requires custom calendar integration
2. **No CRM connectors** - build your own integrations
3. **Developer effort** - not plug-and-play
4. **No real-time** for Whisper (batch only)

---

## DECISION FRAMEWORK INPUTS

**Choose SaaS Platform if**:
- Need plug-and-play meeting bot (calendar auto-join)
- Want pre-built CRM integrations (Salesforce, HubSpot)
- Team collaboration features required (comments, clips, search)
- Limited technical resources (no developers)

**Choose API if**:
- Building custom application
- High-volume transcription (100+ hours/month)
- Need specific technical features (real-time streaming, PII redaction)
- Cost optimization critical (API cheaper at scale)
- Custom workflow required (unique integrations)

---

## Data Sources

- S1 provider profiles (/home/ivanadamin/spawn-solutions/research/3.202-speech-audio-ai/01-discovery/S1-rapid/)
- [AssemblyAI Blog: Top AI Notetakers 2025](https://www.assemblyai.com/blog/top-ai-notetakers)
- [Deepgram: Best AI Meeting Tools 2023](https://deepgram.com/learn/best-ai-tools-for-transcribing-meetings-in-2023)
- [Deepgram: Best Speech-to-Text APIs 2025](https://deepgram.com/learn/best-speech-to-text-apis)
- [Fireflies HubSpot Integration](https://fireflies.ai/integrations/crm/hubspot)
- [Otter HubSpot Integration Guide](https://help.otter.ai/hc/en-us/articles/19439009788951-Otter-ai-HubSpot-Integration-Guide)
- Official vendor documentation (Nov 2024)

---

**Last Updated**: 2025-11-24
**Next Step**: Use this matrix for S2 pricing-tco.md (TCO scenarios) and synthesis.md (decision framework)
