# Domain Explainer: Speech & Audio AI Technical Concepts

**Audience**: Business decision-makers, non-technical founders, team leads
**Purpose**: Explain technical terminology and concepts in speech/audio AI transcription
**Focus**: "What does this term mean?" NOT "Which platform should I choose?"

**Reading time**: 15-20 minutes

---

## Core Technology Concepts

### What is Speech-to-Text (Transcription)?

**Speech-to-text** converts spoken audio into written text. Modern AI systems like Whisper (OpenAI) can transcribe hours of meeting audio into searchable text with 95-98% accuracy on clear audio.

**How it works** (simplified):
1. **Audio preprocessing**: Convert sound waves into frequency patterns (spectrogram)
2. **Acoustic model**: AI identifies phonemes (sound units) from audio patterns
3. **Language model**: AI predicts words from phonemes using context (grammar, vocabulary)
4. **Output**: Text transcript with timestamps, punctuation, speaker labels

**Example**: "Let's schedule the meeting for Tuesday" → AI hears /lɛts ʃɛdʒul ðə mitɪŋ fɔr tuzdeɪ/ → outputs "Let's schedule the meeting for Tuesday"

---

## Transcription Technology Terms

### Speaker Diarization

**What it means**: "Who said what" - identifying and labeling different speakers in a conversation.

**How it works**: AI analyzes voice characteristics (pitch, tone, pace) to cluster utterances by speaker, then labels them as "Speaker 1", "Speaker 2", etc. Advanced systems can handle 6-8 speakers.

**Why it's difficult**:
- Similar voices (same gender, age, accent)
- Crosstalk (multiple people talking simultaneously)
- Poor audio quality (phone calls, background noise)

**Business value**: Meeting notes with speaker attribution (e.g., "Alice: We should prioritize feature X" vs "Bob: I disagree...")

---

### Word Error Rate (WER)

**What it means**: Industry standard metric for transcription accuracy. Measures percentage of words transcribed incorrectly.

**Formula**: WER = (Substitutions + Deletions + Insertions) / Total Words × 100

**Accuracy levels**:
- **4-5% WER**: Excellent (96-95% accuracy) - Rev AI, GPT-4o Transcribe
- **6-7% WER**: Very good (94-93% accuracy) - Whisper, AssemblyAI, Deepgram
- **10-15% WER**: Acceptable (90-85% accuracy) - Noisy audio, strong accents
- **>20% WER**: Poor (< 80% accuracy) - Unusable for most applications

**Example**:
- Reference: "I need to schedule a meeting for Tuesday" (7 words)
- Transcription: "I need to schedule the meeting on Tuesday" (8 words)
- Errors: 2 (substitution: "a" → "the", insertion: "on")
- WER = 2/7 × 100 = 28.6% (poor accuracy)

---

### Hallucinations

**What it means**: AI generates text that wasn't actually spoken.

**When it happens**: Whisper (OpenAI) has a known issue where silence, music, or background noise sometimes produces phantom text.

**Example**:
- **Audio**: 30 seconds of silence
- **Hallucination**: "Thank you for watching. Please like and subscribe." (common YouTube outro phrase from training data)

**Why it matters**: Legal, medical, or financial transcripts with hallucinations can create false records.

**Mitigation**: AssemblyAI Universal-2 model reduces hallucinations by 30% compared to Whisper. Rev AI uses hybrid AI+human review for critical applications.

---

### Real-Time Transcription vs Post-Processing

**Real-time transcription**:
- Audio streams to AI as meeting happens
- Text appears within 300ms-3 seconds (live captions)
- Higher computational cost (more expensive)
- Use case: Live accessibility captions, real-time coaching

**Post-processing (batch transcription)**:
- Full audio file uploaded after meeting ends
- AI processes entire file at once
- Cheaper, higher accuracy (can analyze full context)
- Use case: Meeting notes, podcast transcripts

**Example**: Otter.ai live captions (real-time, 1-2 sec latency) vs Whisper API (batch, processes 1-hour file in 24 minutes).

---

## Meeting Bot Technology

### How Meeting Bots Work

**Step-by-step process**:
1. **Calendar integration**: User grants OAuth permission to read Google Calendar or Outlook
2. **Meeting detection**: Bot scans calendar for upcoming Zoom/Google Meet/Teams meetings
3. **Auto-join**: Bot enters meeting as participant 2-3 minutes before start
4. **Bot visibility**: Meeting participants see "Fireflies Notetaker" or "Otter.ai Assistant" in participant list
5. **Recording**: Bot records audio stream (requires meeting host permission in some cases)
6. **Upload**: Audio sent to cloud for transcription
7. **Transcription**: AI converts audio to text (real-time or post-call)
8. **Summary generation**: LLM (Claude, GPT-4) creates meeting notes, action items
9. **Storage**: Transcript stored in platform dashboard, searchable, shareable

**Privacy consideration**: Bot visibility means all meeting participants see automated recording. This has consent implications for client calls, legal discussions, medical consultations.

---

### OAuth (Calendar Integration)

**What it means**: Authorization protocol that allows apps to access your calendar without seeing your password.

**How it works**:
1. You click "Connect Calendar" in Fireflies/Otter
2. Redirected to Google/Microsoft login page
3. You approve permissions: "Fireflies wants to read your calendar events"
4. Platform receives temporary access token (not your password)
5. Platform can now read calendar events, but can't access email, files, etc.

**Why it's secure**: Platform never sees your password. You can revoke access anytime from Google/Microsoft account settings.

---

## AI Features & Processing

### Action Item Extraction

**What it means**: AI automatically identifies tasks mentioned in meeting and formats as to-do list.

**How it works**: Natural Language Processing (NLP) detects phrases like:
- "Let's schedule..." → Schedule meeting
- "Bob will send the report by Friday" → Bob: Send report (due: Friday)
- "We need to review the proposal" → Review proposal

**Output example**:
```
Action Items:
□ Alice: Schedule follow-up meeting with legal (due: this week)
□ Bob: Send Q4 revenue report (due: Friday)
□ Team: Review vendor proposal (due: next Monday)
```

**Accuracy**: 60-80% depending on LLM backend (GPT-4 > Claude > GPT-3.5). Always review before importing to task manager.

---

### Sentiment Analysis

**What it means**: AI detects emotional tone from speech (frustrated, excited, confused, neutral).

**How it works**: Analyzes:
- **Word choice**: "terrible", "amazing", "confused"
- **Tone of voice**: Pitch, pace, volume
- **Context**: Sarcasm, escalation, de-escalation

**Use cases**:
- **Sales calls**: Detect objections, buying signals
- **Customer support**: Flag frustrated customers for manager review
- **Team meetings**: Identify morale issues, engagement

**Limitations**: 70-85% accuracy. Misses sarcasm, cultural communication styles, non-native speaker patterns.

---

### Prompt Caching (Claude-specific)

**What it means**: LLM optimization that caches frequently used context to reduce cost and latency.

**How it works**: When summarizing 50 meeting transcripts with same system prompt:
- **First call**: Full prompt (2K system + 8K transcript = 10K tokens) costs $0.03 (Claude Sonnet)
- **Cached calls**: Only new transcript (8K tokens) costs $0.003 (90% cheaper)
- Cache lasts 5 minutes

**Business value**: Document analysis, meeting summaries with repeated templates save 34-78% cost.

**Example**: Consultant transcribes 100 meetings/month:
- Without caching: 100 × $0.03 = $3/month
- With caching: $0.03 + 99 × $0.003 = $0.33/month (89% savings)

---

## Accuracy & Performance Metrics

### Noise Robustness

**What it means**: How well transcription handles background noise (air conditioning, traffic, keyboard typing).

**Measurement**: WER degr

adation from clean audio to noisy audio.
- **Good noise robustness**: +4-5% WER degradation (AssemblyAI 10.5% clean → 14.1% noisy = +3.6%)
- **Poor noise robustness**: +10-15% WER degradation

**Mitigation**:
- Use high-quality microphones (USB condenser vs laptop built-in)
- Noise cancellation software (Krisp, NVIDIA RTX Voice)
- Choose APIs with noise-reduction preprocessing

---

### Latency vs Throughput

**Latency**: Time from when you speak to when text appears.
- **Real-time transcription**: 300ms-3 seconds (Deepgram 300ms, Otter 1-2 sec)
- **Batch processing**: Minutes to hours (Whisper processes 1-hour file in 24 minutes)

**Throughput**: How much audio processed per unit of time.
- **Measured as RTFx** (Real-Time Factor): 2,728x = processes 2,728 hours of audio in 1 hour
- **Example**: Deepgram processes 14-minute video in 5 seconds = 168x real-time

**Trade-off**: Real-time has higher latency per word (2-3 sec delay) but immediate feedback. Batch has lower latency overall (24 min for 1 hour) but must wait for full file.

---

### Custom Vocabulary (Keyword Boosting)

**What it means**: User-provided word list to improve transcription accuracy on domain-specific terms.

**Use cases**:
- **Medical**: Drug names ("lisinopril", "metformin"), procedures ("cholecystectomy")
- **Legal**: Case names, legal terms ("plaintiff", "deposition", "voir dire")
- **Tech**: Product names ("Kubernetes" not "cue burn it ease", "PostgreSQL" not "post gray sequel")

**How to use**:
1. Create list of 50-200 domain-specific terms
2. Upload to platform (AssemblyAI, Deepgram support; Whisper API does not)
3. AI increases probability of these words during transcription

**Improvement**: 10-30% WER reduction on technical jargon (medical: 25% WER → 18% WER with custom vocabulary).

---

## Privacy & Compliance

### HIPAA BAA (Business Associate Agreement)

**What it means**: Legal contract required when third-party service handles Protected Health Information (PHI).

**PHI includes**: Patient names, diagnoses, treatment plans, appointment dates, phone numbers.

**Requirements**:
- Service must offer BAA (many free tiers don't)
- Service must encrypt data in transit and at rest
- Service must allow data deletion on request
- Service must not train AI models on customer PHI

**Platforms offering HIPAA BAA**:
- **Free tier**: Fathom (no extra cost)
- **Paid tier**: AssemblyAI, Rev AI, Fireflies Enterprise
- **No HIPAA**: Otter (has "safeguards" but no BAA), Grain

**Misconception**: "HIPAA-compliant" doesn't mean secure - it means contractual obligations exist. Otter lacks E2EE (end-to-end encryption), so even with "safeguards", patient data could be accessed by Otter employees.

---

### PII Redaction

**What it means**: Automatic removal of Personally Identifiable Information from transcripts.

**PII includes**:
- Social Security Numbers (123-45-6789)
- Credit card numbers (4111-1111-1111-1111)
- Names, addresses, phone numbers, email addresses

**How it works**: AI detects PII patterns, replaces with [REDACTED] or [SSN], [CREDIT_CARD].

**Example**:
- **Original**: "My SSN is 123-45-6789 and credit card is 4111-1111-1111-1111"
- **Redacted**: "My SSN is [SSN] and credit card is [CREDIT_CARD]"

**Only provider with PII redaction**: AssemblyAI (as of Nov 2024). Critical for call centers, healthcare, financial services.

---

### Data Residency

**What it means**: Geographic location where audio and transcripts are stored.

**Why it matters**:
- **GDPR**: EU law requires EU citizen data stored in EU (not US)
- **Privacy laws**: Some countries prohibit data export (China, Russia)
- **Compliance**: Financial regulations may require data in specific jurisdictions

**Options**:
- **US-only**: Most platforms (Fireflies, Otter, Whisper API, Deepgram, Rev AI)
- **EU option**: AssemblyAI (Dublin servers), self-hosted Whisper
- **No option**: Grain, Fathom (US-only)

**Misconception**: "Cloud" doesn't mean "everywhere". Data is physically stored in specific data centers (AWS us-east-1, Google us-central1, etc.).

---

## Integration & Development

### Webhook vs Polling

**Webhook**: Platform sends notification to your server when transcript is ready.
- **How it works**: You provide URL (https://your-app.com/transcript-ready), platform POSTs JSON when done
- **Advantage**: Instant notification, no wasted API calls
- **Use case**: Real-time integrations (send transcript to CRM immediately)

**Polling**: Your server repeatedly checks "Is transcript ready yet?"
- **How it works**: Call GET /status every 5-10 seconds until complete
- **Disadvantage**: Wastes API calls, higher latency
- **Use case**: Simple scripts, no webhook infrastructure

**Example**:
- **Webhook**: Platform notifies in 1 second after transcription → total time 1 sec
- **Polling**: Check every 10 seconds, transcription takes 45 sec → total time 50 sec (5 checks)

---

### API Rate Limits

**What it means**: Maximum number of requests allowed per time period.

**Common limits**:
- **Concurrent requests**: 100 REST API calls, 50 WebSocket connections (simultaneous)
- **Daily limits**: 1,000-10,000 API calls per day (depending on tier)
- **File size**: 25MB-2GB per audio file

**What happens when exceeded**:
- **HTTP 429 Error**: "Too Many Requests" - retry after X seconds
- **Account suspension**: Repeated violations may lock account
- **Overage charges**: Some platforms charge extra (Deepgram, AssemblyAI)

**Mitigation**:
- Implement rate limiting in your code (max 100 concurrent requests)
- Use batching (send 10 files at once vs 1000 individual requests)
- Upgrade to higher tier (enterprise plans often have higher limits)

---

### Development Effort (Custom Build)

**What it means**: Engineering hours required to build custom transcription solution.

**Effort breakdown**:
- **Basic transcription** (Whisper API only): 56-84 hours ($5,600-$8,400)
  - API integration (16-24 hours)
  - File upload handling (8-12 hours)
  - Transcript storage (12-16 hours)
  - Basic UI (20-32 hours)

- **Transcription + Summary** (Whisper + Claude): 82-126 hours ($8,200-$12,600)
  - Above + LLM integration (16-24 hours)
  - Prompt engineering (10-18 hours)

- **Full meeting bot** (calendar + Zoom + CRM): 260-400 hours ($26,000-$40,000)
  - Above + calendar integration (40-60 hours)
  - Zoom API integration (60-90 hours)
  - CRM sync (40-60 hours)
  - Meeting bot infrastructure (80-120 hours)

**Ongoing maintenance**: $4,800-$9,000/year (10-20 hours/month)
- API updates, bug fixes, feature requests

**Misconception**: "It's just an API call" - building production-ready systems requires infrastructure, error handling, monitoring, security, compliance.

---

## Pricing Models

### Usage-Based vs Flat Subscription

**Usage-based (APIs)**:
- Pay per minute of audio transcribed
- Cost: $0.003-$0.035/min ($0.18-$2.10/hour)
- **Advantage**: Only pay for what you use (10 hours/month = $2-21)
- **Disadvantage**: Unpredictable costs if volume spikes

**Flat subscription (SaaS)**:
- Pay per user per month/year
- Cost: $100-240/user/year (Pro/Business tiers)
- **Advantage**: Predictable budgeting, unlimited transcription (fair use limits)
- **Disadvantage**: Overpaying if low volume (5 hours/month on $120/year plan = $2/hour)

**Break-even example**:
- SaaS: $120/year = $10/month
- API: $0.36/hour (Whisper)
- Break-even: $10 / $0.36 = 28 hours/month

**If you transcribe**:
- <28 hours/month → API cheaper
- \>28 hours/month → SaaS cheaper

---

### Total Cost of Ownership (TCO)

**What it means**: All costs over 3-year period (subscriptions + development + maintenance + hidden costs).

**TCO components**:
- **Subscriptions**: $0-$20,000/year (depending on team size, tier)
- **Development**: $0-$40,000 (one-time, for custom builds)
- **Maintenance**: $0-$9,000/year (API builds only)
- **Training**: $0-$2,000 (onboarding team on new platform)
- **Migration**: $300-$10,000 (switching platforms)
- **Opportunity cost**: Lost productivity during setup (1-80 hours)

**Example: 10-person sales team**:
- **Grain Business**: $5,400 (subscriptions only, 3-year)
- **Custom Whisper + HubSpot**: $36,400 ($26K dev + $1,080 API + $9,240 maintenance)
- **Winner**: Grain (6.7× cheaper)

---

## Whisper & Open-Source Concepts

### Whisper Commoditization

**What it means**: OpenAI's Whisper (open-source, MIT license) democratizes high-quality transcription, driving commercial API prices down.

**How it creates commoditization**:
1. **680K hours training data** - rivals commercial quality (95-98% accuracy)
2. **MIT license** - free for commercial use (no royalties)
3. **Whisper API pricing** - $0.006/min ($0.36/hour) sets price floor
4. **Wide adoption** - 60-80% of SaaS platforms likely use Whisper backend

**Impact on market**:
- **2022**: Rev AI $1.20/hour (human + AI hybrid)
- **2023**: Whisper API launches at $0.36/hour (70% cheaper)
- **2024**: Deepgram drops to $0.26/hour (28% cheaper than Whisper to compete)
- **2030 projection**: $0.20/hour (30-50% deflation expected)

**Strategic implication**: Avoid 3-year contracts at 2024 pricing (you'll overpay 30-50% in years 2-3 as prices drop).

---

### Self-Hosted vs Cloud API

**Self-hosted Whisper**:
- Run Whisper on your own servers (AWS EC2, on-prem)
- **Advantages**: 100% privacy, no per-minute costs, offline capability
- **Disadvantages**: Requires GPU ($1,000-10,000), DevOps skills, maintenance
- **Cost**: $0 API fees, but $100-$500/month infrastructure + $5,000-10,000 setup

**Cloud API (Whisper API, AssemblyAI)**:
- Send audio to vendor's servers, get transcript back
- **Advantages**: No setup, elastic scaling, enterprise features (PII redaction, real-time)
- **Disadvantages**: Per-minute costs, privacy concerns (audio uploaded to cloud)
- **Cost**: $0.36-$0.90/hour API fees, $0 infrastructure

**When self-hosted makes sense**:
- Privacy-critical (healthcare, legal) + high volume (500+ hours/month)
- Break-even: 500 hours/month × $0.36 = $180/month API costs vs $200/month GPU + maintenance

**Misconception**: "Self-hosted is always cheaper" - not true for low volume (<100 hours/month). Cloud APIs avoid upfront $5K-10K setup cost.

---

## Strategic Concepts

### Lock-In Risk (1-5 Scale)

**What it means**: Difficulty of switching to a different platform.

**Factors**:
1. **Data portability**: Can you export all transcripts? (JSON, TXT, SRT formats)
2. **API lock-in**: Vendor-specific API requires code rewrite
3. **Workflow lock-in**: Team dependency on meeting bot UX, integrations
4. **Cost lock-in**: Sunk development costs ($10K-40K for custom builds)
5. **Feature lock-in**: Unique features hard to replace (PII redaction, prompt caching)

**Lock-in scores**:
- **1.0/5 (minimal)**: Whisper API, Deepgram (easy JSON export, standard API, no workflow dependency)
- **3.0/5 (moderate)**: Fireflies (CRM integrations, team analytics, AI Apps proprietary)
- **3.4/5 (high)**: Grain (deep HubSpot integration, Stories feature unique)

**Migration cost**:
- Low lock-in (1.0): 8-16 hours ($800-$2,400)
- High lock-in (3.4): 40-80 hours ($6,000-$16,000)

**Mitigation**: Abstraction layer (LangChain-style wrapper reduces switching cost 80%).

---

### Vendor Viability (5-Year/10-Year Survival)

**What it means**: Probability a vendor still exists in 5-10 years.

**Assessment factors**:
1. **Funding strength** (30%): How much runway? Series A/B/C raised?
2. **Market position** (25%): Market share, growth trajectory, customer base
3. **Strategic backing** (20%): Corporate parent (Microsoft, Google) or independent?
4. **Revenue/profitability** (15%): Profitable or burning cash?
5. **Competitive moat** (10%): Unique defensible advantages

**Survival probability examples**:
- **Whisper (Microsoft-backed)**: 95% (5-year), 85% (10-year)
- **Rev AI (profitable parent)**: 90% (5-year), 75% (10-year)
- **Fireflies (VC-backed)**: 75% (5-year), 50% (10-year), 60-70% acquisition risk
- **Grain (VC-backed, small)**: 65% (5-year), 40% (10-year), 70-80% acquisition risk

**Strategic implication**: VC-backed startups face 60-80% acquisition probability by 2028. Choose corporate-backed or profitable vendors for long-term stability.

---

### Time Horizon Planning

**What it means**: Different strategies for different time periods.

**0-1 year horizon**:
- Focus on current features, pricing (S1-S3 research)
- All vendors safe to use
- Contract length: Month-to-month or annual

**1-3 year horizon**:
- Factor in vendor viability, lock-in risk (S4 analysis)
- Choose stable vendors (corporate-backed, profitable)
- Contract length: Annual (avoid 3-year contracts)

**3-5 year horizon**:
- Assume technology shifts, plan for migration
- Build abstraction layer if using APIs
- Contract length: Annual or month-to-month only

**5+ year horizon**:
- Assume transcription commoditizes (98%+ accuracy standard)
- Self-hosted Whisper competitive for 80%+ use cases
- Platforms compete on features (multimodal, AI participants, compliance)

**Strategic implication**: Technology moves in 2-3 year cycles (Whisper 2022 → dominant 2024). Avoid long-term commitments.

---

## Common Misconceptions

### "Transcription accuracy is 100% now with AI"
**Reality**: 95-98% on clean audio, 85-90% on noisy audio or strong accents. Legal, medical, financial applications need 99%+ (hybrid AI+human like Rev AI).

### "Whisper API is always cheaper than SaaS"
**Reality**: Break-even at 28 hours/month (Whisper $0.36/hour vs SaaS $10/month). For solo users (<28 hours/month), SaaS may be cheaper. Also doesn't include development effort for custom builds ($5,600-$40,000).

### "Meeting bots are invisible"
**Reality**: Bot shows up as participant ("Fireflies Notetaker"). Privacy implication for client calls - requires disclosure and consent.

### "All platforms use the same AI model"
**Reality**: ~60-80% likely use Whisper or Whisper-derived models, but 20-40% use proprietary models (Rev AI Reverb, AssemblyAI Universal-2, Deepgram Nova). Accuracy varies 4-7% WER range.

### "Free tiers are bait-and-switch"
**Reality**: Fathom Free is genuinely unlimited (verified Nov 2024). Otter Free is limited to 300 min/month (upgrade trigger at 10 hours/month).

### "3-year contracts save money"
**Reality**: Technology shifts too fast. Whisper 2022 → dominant 2024 (2-year cycle). Expect 30-50% pricing deflation by 2030. Avoid multi-year contracts unless guaranteed pricing freeze + early exit clause.

### "Self-hosted Whisper is always better"
**Reality**: Commercial APIs have advantages (real-time <300ms latency, PII redaction, enterprise compliance, global scale). Self-hosted makes sense for privacy-critical + high-volume (500+ hours/month), not low-volume (<100 hours/month).

### "VC funding means company is successful"
**Reality**: Grain ($20M raised), Fathom ($22M raised), Fireflies ($19M raised) have 40-70% 10-year survival probability. 60-80% acquisition risk by 2028. Corporate-backed (Whisper, Rev AI) or profitable companies safer long-term.

---

**Document status**: Generic research (no platform recommendations)
**For platform comparisons**: See S1 provider profiles, S2 comprehensive analysis, S3 use case scenarios
**For strategic analysis**: See S4 vendor viability, lock-in mitigation, AI trajectory
**Last updated**: November 24, 2025
**Version**: 1.0
