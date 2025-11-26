# Terms to Explain - 3.202 Speech & Audio AI

**Purpose**: Track technical terms, jargon, and concepts encountered during S1-S4 research that need explanation in DOMAIN_EXPLAINER.md

**Updated**: As research progresses

---

## Terms Encountered in S1 (Platform Profiles)

### Transcription Technology
- [ ] **Speaker diarization** - Who said what (identifying different speakers)
- [ ] **Word Error Rate (WER)** - Accuracy metric for transcription
- [ ] **Real-time transcription** - vs post-processing (timing tradeoffs)
- [ ] **Acoustic model** - How speech recognition models work
- [ ] **Language model** - Contextual understanding component

### Meeting Bot Technology
- [ ] **Meeting bot** - Automated participant that joins calls to record
- [ ] **Calendar integration** - OAuth, permissions, auto-join mechanics
- [ ] **Bot visibility** - Why meeting participants see "Fireflies Notetaker"

### AI Features
- [ ] **Prompt caching** - LLM optimization for repeated context (Claude feature)
- [ ] **Action item extraction** - NLP task identification
- [ ] **Sentiment analysis** - Emotional tone detection in meetings
- [ ] **Topic detection** - Automatic categorization

### Audio Quality
- [ ] **Sample rate** - Audio quality measurement (kHz)
- [ ] **Noise reduction** - Background noise filtering
- [ ] **Echo cancellation** - Audio preprocessing
- [ ] **Crosstalk** - Multiple speakers talking simultaneously

### Privacy & Compliance
- [ ] **BAA (Business Associate Agreement)** - HIPAA compliance requirement
- [ ] **Data residency** - Where audio/transcripts are stored geographically
- [ ] **Encryption in transit** - vs encryption at rest
- [ ] **PII redaction** - Removing personally identifiable information

### Integration Concepts
- [ ] **Webhook** - Real-time event notifications
- [ ] **API rate limits** - Request throttling
- [ ] **Batch processing** - vs real-time processing
- [ ] **CRM integration** - Syncing call notes to customer records

---

## Terms Encountered in S2 (Comprehensive Analysis)

### Performance Metrics
- [x] **Latency** - Time from speech to transcript (real-time: 1-3ms, batch: seconds to minutes)
- [x] **Throughput** - Hours processed per hour of wall-clock time (RTFx = Real-Time Factor)
- [x] **Concurrency** - Multiple files processed simultaneously (100 REST, 50 WebSocket typical)
- [x] **Processing Speed** - How fast audio is transcribed (Deepgram: 5s for 14min, Whisper: ~40% of duration)
- [x] **RTFx (Real-Time Factor)** - Speed multiplier (2,728x = processes 2,728 hours in 1 hour)

### Accuracy Metrics
- [x] **WER (Word Error Rate)** - Industry standard accuracy metric (errors/total words × 100)
- [x] **Hallucinations** - Phantom text not actually spoken (Whisper issue on silence/music)
- [x] **Accuracy on accents** - Performance variation by speaker accent (native vs non-native)
- [x] **Technical jargon handling** - Domain-specific vocabulary accuracy (medical, legal terms)
- [x] **Custom vocabulary** - User-provided word lists to improve accuracy (keyword boosting)
- [x] **Noise robustness** - Performance degradation in noisy environments (+4-7% WER typical)

### Pricing Models
- [x] **Per-minute pricing** - Usage-based API cost ($0.003-0.035/min)
- [x] **Flat subscription** - vs usage-based (SaaS platforms $100-240/user/year)
- [x] **Overage charges** - Cost when exceeding plan limits (fair-use policies)
- [x] **Enterprise pricing** - Custom contracts, volume discounts
- [x] **TCO (Total Cost of Ownership)** - 3-year cost including dev, maintenance, subscriptions
- [x] **Break-even point** - When API build becomes cheaper than SaaS (20-50 users typically)
- [x] **Amortized cost** - Dev cost spread over 3 years ($15K dev ÷ 3 = $5K/year)

### Compliance & Privacy
- [x] **SOC 2 Type II** - Security certification for service providers
- [x] **HIPAA BAA** - Business Associate Agreement for Protected Health Information
- [x] **GDPR** - EU data protection regulation (General Data Protection Regulation)
- [x] **ISO 27001** - Information security management certification
- [x] **PCI-DSS** - Payment Card Industry Data Security Standard
- [x] **Data residency** - Geographic location where data is processed/stored (US, EU)
- [x] **PII redaction** - Automatic removal of SSN, credit cards, names, addresses (AssemblyAI only)
- [x] **E2EE (End-to-End Encryption)** - Encryption where only user has decryption keys (Otter lacks this)
- [x] **Training on customer data** - Whether AI models use customer audio/transcripts for improvement

### Integration Complexity
- [x] **OAuth** - Authorization protocol for calendar/CRM integrations
- [x] **WebSocket** - Protocol for real-time streaming transcription
- [x] **Webhook** - Real-time event notifications (transcript ready)
- [x] **API rate limits** - Request throttling (100 concurrent typical)
- [x] **Development effort** - Hours to build custom solution (56-400 hours)
- [x] **Maintenance burden** - Ongoing cost to maintain custom build ($4,800-9,000/year)
- [x] **Lock-in** - Switching cost (SaaS: 6-12 hours, API build: $20-40K sunk cost)
- [x] **Time-to-value** - Setup to productive use (SaaS: < 1 hour, API: 2-14 weeks)

### API Features
- [x] **Batch processing** - Upload full file, get transcript back (vs streaming)
- [x] **Streaming API** - Real-time transcription via WebSocket
- [x] **Asynchronous processing** - Upload file, poll/webhook for results
- [x] **Speaker diarization** - Identifying and labeling different speakers (max 6-8 typically)
- [x] **Keyword boosting** - Increase likelihood of specific words (custom vocabulary feature)
- [x] **Confidence scores** - Per-word accuracy confidence (0.0-1.0)
- [x] **Smart formatting** - Auto-punctuation, capitalization
- [x] **Multichannel** - Separate audio channels for different speakers

### AI Models
- [x] **Whisper** - OpenAI's open-source speech model (680K hours training data)
- [x] **Reverb ASR** - Rev AI's proprietary model (25-30% better than previous gen)
- [x] **Nova-2/Nova-3** - Deepgram's latest models (30% WER reduction)
- [x] **Universal-2** - AssemblyAI's model (6.68% WER, 30% fewer hallucinations)
- [x] **Conformer + LLM decoder** - Architecture achieving 5-7% WER (best accuracy)
- [x] **CTC-based models** - Fast but less accurate (12% WER vs 5-7% attention-based)
- [x] **Encoder-decoder Transformer** - Whisper's architecture
- [x] **Log-Mel spectrogram** - Audio preprocessing for Whisper (30-second chunks)

---

## Terms Encountered in S3 (Use Case Scenarios)

### Workflow Patterns
- [ ] **Post-call processing** - Upload after meeting ends
- [ ] **Real-time streaming** - Transcribe while meeting happens
- [ ] **Hybrid workflow** - Mix of automated and manual processing

### Integration Patterns
- [ ] **Zapier integration** - No-code automation
- [ ] **Native integration** - vs third-party connectors
- [ ] **API-first architecture** - Build custom workflows

---

## Terms Encountered in S4 (Strategic Analysis)

### Vendor Viability & Survival Probability
- [ ] **5-year survival probability** - Likelihood vendor exists in 5 years (0-100%)
- [ ] **10-year survival probability** - Likelihood vendor exists in 10 years (accounting for market consolidation)
- [ ] **Acquisition risk** - Probability of being acquired by larger company (60-80% for startups like Grain, Fireflies)
- [ ] **Sunset risk** - Probability of product being discontinued (e.g., post-acquisition product shutdown)
- [ ] **Runway** - How long a startup can operate before needing more funding (calculated from total raised, burn rate)
- [ ] **Strategic backing** - Corporate parent support (Microsoft backing OpenAI Whisper, Rev.com backing Rev AI)
- [ ] **Competitive moat** - Defensible advantages that prevent competitors from taking market share
- [ ] **Series A/B/C funding** - Venture capital funding rounds (Seed → Series A → B → C → IPO or acquisition)

### Lock-in Risk & Migration
- [ ] **Lock-in score (1-5 scale)** - Quantified difficulty of switching providers (1 = minimal, 5 = severe)
- [ ] **Data portability** - Ability to export all transcripts, recordings, metadata (JSON, TXT, SRT formats)
- [ ] **API lock-in** - Dependency on vendor-specific API format, integrations (CRM, Zapier)
- [ ] **Workflow lock-in** - Team dependency on meeting bot, auto-join, specific UX patterns
- [ ] **Feature lock-in** - Unique features hard to replace (PII redaction, prompt caching, conversation intelligence)
- [ ] **Abstraction layer** - Code wrapper that standardizes API calls across providers (LangChain-style, reduces switching cost 80%)
- [ ] **Migration playbook** - Step-by-step plan for switching providers (time estimates, cost, challenges)
- [ ] **Sunk cost** - Non-recoverable investment in custom development ($10K-40K for API builds)

### Technology Evolution
- [x] **Whisper commoditization** - OpenAI's open-source model (680K hours training, MIT license) democratizing transcription; drives pricing to $0.36/hour
- [ ] **Commoditization timeline** - Market evolution: 2024-2025 (Whisper dominant) → 2026-2027 (competitors catch up) → 2028-2030 (transcription becomes utility)
- [ ] **Price floor** - Minimum viable price set by Whisper API ($0.006/min = $0.36/hour); commercial APIs must match or differentiate on features
- [ ] **Pricing deflation** - Expected 30-50% price reduction by 2030 (Whisper commoditization, cloud cost reductions)
- [ ] **Self-hosted competitive** - When self-hosted Whisper rivals commercial APIs (2024-2025: batch processing, 2026-2027: real-time, 2028-2030: 80%+ use cases)
- [ ] **WhisperX** - Whisper variant with Voice Activity Detection (VAD), batch inference, forced alignment (5-10× speedup)
- [ ] **Faster-Whisper** - Whisper variant using CTranslate2 (C++ inference engine) for 4× speedup, lower memory usage
- [ ] **Universal-Streaming** - AssemblyAI's real-time model (300ms latency, 41% faster than Deepgram)
- [ ] **Model quantization** - Compressing AI models for faster inference (e.g., 8-bit vs 32-bit precision)
- [ ] **On-device transcription** - Local processing on phone/laptop vs cloud processing (privacy, offline capability)

### API Standardization
- [ ] **De-facto standard** - Industry standard that emerges from usage (not formal W3C/IETF standard) - OpenAI Whisper API format emerging
- [ ] **API convergence** - Trend toward similar API formats across providers (60-70% probability by 2028)
- [ ] **OpenAI Whisper API format** - REST API pattern becoming reference: POST /v1/audio/transcriptions, JSON response with text + timestamps
- [ ] **S3-compatible** - Example of de-facto standard (MinIO, DigitalOcean Spaces clone AWS S3 API for compatibility)

### Market Dynamics
- [ ] **Land-and-expand** - SaaS pricing strategy (free tier → paid tier → enterprise tier)
- [ ] **Freemium model** - Free tier to paid conversion (Fathom unlimited free, Otter 300 min/month free)
- [ ] **Vendor lock-in** - Switching costs, proprietary formats (Grain 3.4/5 lock-in due to HubSpot integration)
- [ ] **Market consolidation** - M&A reducing 8 providers (2024) → 3-4 dominant players (2030)
- [ ] **M&A (Mergers & Acquisitions)** - Likely acquirers: Salesforce (Fireflies), HubSpot (Grain), Zoom (Otter, Fathom), AWS/Google (AssemblyAI, Deepgram)
- [ ] **ARR (Annual Recurring Revenue)** - Yearly subscription revenue (Otter $100M ARR, Rev.com $100M+ ARR)
- [ ] **Valuation** - Company worth based on funding rounds (OpenAI $157B, AssemblyAI undisclosed)
- [ ] **Burn rate** - Monthly cash spending (affects runway calculation)
- [ ] **Path to profitability** - Plan for becoming profitable (important for long-term survival)

### AI Trajectory (2025-2030)
- [ ] **Multimodal transcription** - Analyzing video (facial expressions), screen shares (slides), audio simultaneously (2027-2028)
- [ ] **AI meeting participants** - Bots that ask clarifying questions, synthesize viewpoints, provide real-time coaching (2027-2028)
- [ ] **Emotion detection** - AI analyzing frustration, excitement, confusion from tone + facial expressions (2027-2028)
- [ ] **Integrated translation** - Transcribe + translate in one API call (Spanish → English summary) - expected 2027-2028
- [ ] **AGI-adjacent capabilities** - AI attends meetings, makes low-stakes decisions with approval (speculative, 2029-2030)
- [ ] **Regulatory pressure** - GDPR-style meeting consent laws in US (American Privacy Rights Act) - expected 2028-2030
- [ ] **Real-time transcription (<500ms)** - Industry standard by 2026 (Deepgram 300ms today, Whisper variants catching up)
- [ ] **PII redaction standard** - Automatic SSN, credit card, name removal becomes standard feature by 2026 (currently AssemblyAI only)

### Strategic Planning
- [ ] **Time horizon planning** - Different strategies for 0-1 year, 1-3 years, 3-5 years, 5+ years
- [ ] **ROI threshold** - Minimum return on investment to justify custom build (3-year payback minimum)
- [ ] **Amortized cost** - Dev cost spread over 3 years ($10K dev ÷ 3 = $3,333/year)
- [ ] **Break-even analysis** - When custom build becomes cheaper than SaaS (typically 50+ users, 5,000+ hours/year)
- [ ] **Multi-provider strategy** - Primary (80% volume) + fallback (20% volume) to reduce vendor dependency (15% cost overhead)
- [ ] **Hybrid workflow** - SaaS for 80% (internal meetings, CRM integration), API for 20% (high-volume, sensitive, specialized)
- [ ] **Contract length strategy** - Month-to-month or annual contracts (avoid 3-year due to fast technology shifts)

---

## Concepts That Need High-Level Explanation

These require more than just definitions - need to explain "how it works":

1. **How does a meeting bot work?**
   - OAuth to calendar → detect meeting → join Zoom/Meet → record → upload → transcribe

2. **Why is Whisper API so cheap compared to SaaS platforms?**
   - SaaS bundles transcription + UI + storage + integrations
   - API is just the transcription engine

3. **What makes speaker diarization difficult?**
   - Similar voices, crosstalk, poor audio quality

4. **How does prompt caching work in Claude?**
   - Caches first 50K tokens of context, 10× cheaper for repeated use

5. **What's the difference between real-time and post-processing?**
   - Real-time: streaming transcription, higher latency, more expensive
   - Post-processing: full file upload, batch processing, cheaper

---

## Concepts That Need High-Level Explanation (S4 Additions)

6. **Why does Whisper commoditize transcription?**
   - Open-source + MIT license → anyone can use for free
   - 680K hours training data → rivals commercial quality
   - Sets price floor ($0.36/hour) → commercial APIs must match or differentiate on features

7. **What is lock-in risk and how to mitigate?**
   - Lock-in = difficulty of switching providers (1-5 scale)
   - APIs have minimal lock-in (1.1/5) vs SaaS platforms (2.1-3.4/5)
   - Mitigation: abstraction layer (80% reduction in switching cost), multi-provider strategy, monthly export

8. **How to assess vendor viability?**
   - 5 factors: Funding strength (30%), Market position (25%), Strategic backing (20%), Revenue (15%), Competitive moat (10%)
   - Corporate-backed (Whisper, Rev AI) safer than VC-backed startups (Grain, Fathom, Fireflies)
   - Acquisition risk: Grain 70-80%, Fireflies 60-70%, Fathom 60-70%, Otter 40-50%

9. **When does self-hosted Whisper rival commercial APIs?**
   - 2024-2025: Batch processing parity (cost savings, privacy)
   - 2026-2027: Real-time gap closes (WhisperX, Faster-Whisper <500ms latency)
   - 2028-2030: Competitive for 80%+ use cases (only extreme low-latency, global scale, enterprise compliance remain commercial advantages)

10. **What is time horizon planning?**
    - 0-1 year: Focus on features, pricing (S1-S3 research)
    - 1-3 years: Factor in vendor viability, lock-in risk (S4 analysis)
    - 3-5 years: Assume technology shifts, plan for migration
    - 5+ years: Assume commoditization, self-hosted competitive

## Common Misconceptions to Address

**S1-S3 Misconceptions:**
- ❌ "Transcription accuracy is 100% now with AI" → Reality: 95-98% on good audio, 85-90% on poor audio
- ❌ "Whisper API is always cheaper" → Reality: SaaS wins for low volume (<50 hours/month)
- ❌ "Meeting bots are invisible" → Reality: Bot shows up as participant (privacy implication)
- ❌ "All platforms use the same underlying model" → Reality: Whisper is common but not universal

**S4 Strategic Misconceptions:**
- ❌ "All vendors will survive 5 years" → Reality: 60-80% acquisition risk for startups (Grain, Fireflies, Fathom)
- ❌ "Switching providers is always expensive" → Reality: APIs have minimal lock-in (1.1/5), SaaS platforms vary (2.1-3.4/5)
- ❌ "3-year contracts save money" → Reality: Technology shifts too fast; expect 30-50% pricing deflation by 2030
- ❌ "Transcription quality is differentiation" → Reality: Whisper commoditizes quality (95-98%); platforms compete on features (CRM, analytics, compliance)
- ❌ "Self-hosted Whisper is always better" → Reality: Commercial APIs have advantages (real-time <300ms, enterprise compliance, global scale)
- ❌ "VC-backed startups are safe" → Reality: Grain $20M, Fathom $22M, Fireflies $19M have 40-70% 10-year survival probability vs Microsoft-backed Whisper 85%

---

## Next Steps

After completing S1-S4:
1. Review this list
2. Group related terms by concept
3. Write DOMAIN_EXPLAINER.md focusing on these terms
4. Use business-friendly language (avoid circular definitions)
5. Include diagrams where helpful (e.g., meeting bot workflow)
