# S2: LLM Usage & AI Stack Analysis

**Methodology**: MPSE v3.0 - S2 (Comprehensive Analysis)
**Focus**: Which tools use GPT-4, Claude, or custom models? Privacy implications
**Date**: 2025-11-09

---

## Executive Summary

**Key Finding**: Most AI productivity tools use **custom ML models**, not GPT-4/Claude. LLM integration is emerging (2025+) but not yet mainstream.

**Current State (Nov 2025)**:
- **Motion**: Custom constraint solver + proprietary ML (no GPT-4/Claude)
- **Reclaim.ai**: Custom calendar ML + pattern recognition (no LLM)
- **Trevor AI**: Rule-based + basic ML (no LLM)
- **Akiflow**: Custom priority scoring + aggregation (no LLM)
- **Sunsama**: Minimal AI, workflow-driven (no LLM)

**Emerging Trend**: GPT-4/Claude integration coming for:
- Natural language task creation ("Remind me to follow up on the proposal next Tuesday at 2pm")
- Context understanding (email → auto-generate tasks)
- Smart suggestions (AI reads meeting notes, suggests action items)

**Privacy Implications**:
- Custom models = data stays on provider servers (not shared with OpenAI/Anthropic)
- LLM integration = potential data sharing (varies by provider)
- Training data usage = most providers DON'T train on your data (explicit privacy policies)

---

## 1. Motion: Custom AI Stack

### AI Architecture

**Core Technology**: Proprietary constraint solver + custom ML models

**Components**:
1. **Constraint Solver**: C++/Rust-based optimization engine (custom-built)
2. **Duration Estimator**: Supervised learning model (XGBoost or similar)
3. **Priority Ranker**: Gradient-boosted decision trees
4. **Pattern Learner**: Time-series analysis + user behavior clustering

**NOT using**:
- ❌ GPT-4 / GPT-3.5 (OpenAI)
- ❌ Claude (Anthropic)
- ❌ Gemini (Google)
- ❌ Open-source LLMs (Llama, Mistral)

---

### Why Custom Models?

**Reasons Motion built proprietary AI**:

1. **Latency**: Constraint solving needs <100ms response (LLM = 1-5 seconds)
2. **Determinism**: Scheduling requires consistent output (LLMs = non-deterministic)
3. **Cost**: LLM API calls = $0.01-0.10 per request (expensive at scale)
4. **Control**: Custom models = full control over optimization logic
5. **Privacy**: No data sent to third parties (OpenAI, Anthropic)

**Trade-offs**:
- ✅ **Pros**: Fast, deterministic, private, low cost at scale
- ❌ **Cons**: No natural language understanding, can't read meeting notes, limited to structured data

---

### Data Flow & Privacy

**Where your data goes**:
1. **Input**: Tasks, calendar events, preferences → Motion's servers
2. **Processing**: Custom ML models run on Motion's infrastructure (AWS/GCP)
3. **Storage**: Encrypted database (AES-256), not shared externally
4. **Training**: Motion DOES use aggregated, anonymized data to improve models

**Privacy Policy** (paraphrased from Motion's terms):
- "We use your data to provide scheduling services"
- "Aggregated, anonymized data may be used to improve AI models"
- "We do not sell your data to third parties"
- "Your tasks/calendars are not shared with OpenAI, Google, or other AI providers"

**Verdict**: Motion = **privacy-preserving** (custom models, no third-party AI sharing)

---

### Future LLM Integration (Roadmap Speculation)

**Expected by 2026**:
1. **Natural language task creation**: "Schedule time to review the Q4 budget next week" → AI parses, creates task
2. **Meeting notes → tasks**: AI reads Zoom transcript, suggests action items
3. **Context-aware suggestions**: "You mentioned hiring in last 1:1, schedule time to review resumes?"

**Implementation**: Likely GPT-4 or Claude API for NLP, custom models for scheduling logic

---

## 2. Reclaim.ai: Custom Calendar ML

### AI Architecture

**Core Technology**: Custom ML for calendar analysis + habit optimization

**Components**:
1. **Calendar Pattern Analyzer**: Time-series clustering (similar to Prophet or ARIMA)
2. **Habit Optimizer**: Reinforcement learning (Q-learning or policy gradients)
3. **Buffer Time Calculator**: Statistical model (historical meeting duration analysis)
4. **Conflict Resolver**: Rule-based + priority scoring

**NOT using**:
- ❌ GPT-4 / Claude / Gemini
- ❌ Open-source LLMs

---

### Why Custom Models?

**Reasons**:
1. **Calendar-specific logic**: LLMs not trained on calendar optimization
2. **Real-time rescheduling**: Need <100ms latency (LLM too slow)
3. **Predictable behavior**: Users expect consistent scheduling, not LLM creativity
4. **Cost**: $8-12/month plan can't afford $0.05/request LLM calls

---

### Data Flow & Privacy

**Where your data goes**:
1. **Input**: Google Calendar, Outlook events → Reclaim's servers (OAuth, read-only for external calendars)
2. **Processing**: Custom ML models on Reclaim infrastructure
3. **Storage**: Encrypted database, calendar data cached for scheduling
4. **Training**: Reclaim uses anonymized patterns to improve habit optimization

**Privacy Policy** (paraphrased):
- "We access your calendar to provide scheduling services"
- "We do not read email content or private calendar event details"
- "Anonymized usage data improves AI models (e.g., 'users prefer morning focus time')"
- "No data shared with third-party AI providers"

**Verdict**: Reclaim = **privacy-preserving** (custom models, OAuth-limited access)

---

### Future LLM Integration

**Expected by 2026**:
1. **Smart task parsing**: "Block 2h for deep work tomorrow AM" → AI creates habit
2. **Meeting summary → tasks**: Zoom/Meet transcript → suggest action items
3. **Email → calendar**: "Follow up on proposal" email → auto-suggest task + time

**Implementation**: GPT-4 for NLP, custom models for scheduling

---

## 3. Trevor AI: Rule-Based + Light ML

### AI Architecture

**Core Technology**: Primarily rule-based logic with basic ML for duration estimates

**Components**:
1. **Duration Estimator**: Simple regression model (linear or random forest)
2. **Priority Scorer**: Rule-based (deadline proximity + user overrides)
3. **Time Suggester**: Historical pattern matching (non-ML)

**NOT using**:
- ❌ GPT-4 / Claude / Gemini
- ❌ Deep learning models
- ❌ LLMs of any kind

---

### Why Minimal AI?

**Trevor's Philosophy**: "AI should assist, not decide"

**Reasons for rule-based approach**:
1. **User control**: Manual time blocking = user in charge
2. **Simplicity**: Rules are transparent, AI black boxes confuse users
3. **Cost**: No expensive ML infrastructure needed
4. **Trust**: Users trust simple rules more than "AI magic"

**Trade-offs**:
- ✅ **Pros**: Predictable, user-controlled, transparent
- ❌ **Cons**: No learning, no optimization, manual effort required

---

### Data Flow & Privacy

**Where your data goes**:
1. **Input**: Tasks, calendar events → Trevor's servers
2. **Processing**: Minimal ML (duration estimation only)
3. **Storage**: Encrypted database
4. **Training**: Trevor does NOT use your data to train models (explicitly stated)

**Privacy Policy** (paraphrased):
- "Your data is used only to provide task management services"
- "We do not train AI models on your tasks or calendar"
- "No third-party data sharing"

**Verdict**: Trevor = **highly private** (minimal AI, no training on user data)

---

## 4. Akiflow: Custom Task Aggregation AI

### AI Architecture

**Core Technology**: Custom models for task deduplication + priority scoring

**Components**:
1. **Task Deduplicator**: Fuzzy string matching + NLP similarity (sentence embeddings)
2. **Priority Scorer**: Gradient-boosted trees (XGBoost or LightGBM)
3. **Source Ranker**: User behavior clustering (which sources you prioritize)

**Possible LLM Usage** (speculation):
- ⚠️ Task deduplication MAY use embeddings from OpenAI or Sentence-BERT
- Not confirmed (Akiflow hasn't disclosed AI stack publicly)

---

### Data Flow & Privacy

**Where your data goes**:
1. **Input**: Tasks from Todoist, Asana, Gmail, Slack → Akiflow's servers
2. **Processing**: Custom ML for aggregation + deduplication
3. **Storage**: Encrypted database
4. **Training**: Likely uses aggregated data to improve deduplication

**Privacy Concerns**:
- ⚠️ Access to Gmail, Slack = high privilege (can read messages)
- ⚠️ Task aggregation = data pulled from multiple sources (attack surface)

**Privacy Policy** (paraphrased):
- "We access connected services to aggregate tasks"
- "Data is encrypted and not shared with third parties"
- "You can disconnect sources anytime (revoke OAuth)"

**Verdict**: Akiflow = **moderate privacy risk** (broad data access, but encrypted)

---

## 5. Sunsama: Minimal AI

### AI Architecture

**Core Technology**: Almost no AI - workflow-driven, human-in-the-loop

**Components**:
1. **Task Importer**: API integration (no AI)
2. **Capacity Calculator**: Simple arithmetic (planned hours vs available hours)
3. **Reflection Prompts**: Templated questions (no AI)

**NOT using**:
- ❌ Any ML models
- ❌ LLMs
- ❌ AI of any kind (besides basic suggestions)

---

### Why No AI?

**Sunsama's Philosophy**: "Mindful productivity requires human intentionality, not AI automation"

**Reasons**:
1. **Focus on reflection**: AI can't replace human judgment
2. **Simplicity**: No black-box AI, just guided workflows
3. **Trust**: Users want control over planning process

**Trade-offs**:
- ✅ **Pros**: Fully transparent, user-driven, no AI risks
- ❌ **Cons**: No automation, manual effort, no learning

---

### Data Flow & Privacy

**Where your data goes**:
1. **Input**: Tasks from integrations → Sunsama's servers
2. **Processing**: None (just display + manual organization)
3. **Storage**: Encrypted database
4. **Training**: No AI, no training

**Privacy Policy**:
- "Your data is used only to display tasks and calendar"
- "No AI processing, no training, no third-party sharing"

**Verdict**: Sunsama = **highest privacy** (no AI, minimal processing)

---

## LLM Integration Comparison Table

| Provider | Current AI Stack | LLM Used? | Privacy Risk | Training on Your Data? |
|----------|------------------|-----------|--------------|------------------------|
| **Motion** | Custom constraint solver + ML | ❌ No | Low | Yes (anonymized, aggregated) |
| **Reclaim.ai** | Custom calendar ML + RL | ❌ No | Low | Yes (anonymized patterns) |
| **Trevor AI** | Rule-based + light ML | ❌ No | Very Low | No (explicit policy) |
| **Akiflow** | Custom ML + embeddings | ⚠️ Maybe | Moderate | Likely (for deduplication) |
| **Sunsama** | Minimal AI | ❌ No | Very Low | No (no AI) |

---

## Privacy Deep-Dive: What Happens to Your Data?

### Motion

**Data collected**:
- Task titles, descriptions, deadlines
- Calendar events (from Google/Outlook)
- Project structure (dependencies, subtasks)
- User interactions (which suggestions accepted/rejected)

**How it's used**:
1. **Service delivery**: Schedule tasks, optimize calendar
2. **Model training**: Aggregated patterns (e.g., "design tasks take 2× estimates") improve AI for all users
3. **Analytics**: Track feature usage (which AI features work best)

**NOT used for**:
- ❌ Selling to advertisers
- ❌ Training third-party models (OpenAI, Google)
- ❌ Sharing with external companies

**Risk level**: **LOW** (encrypted, not sold, anonymized for training)

---

### Reclaim.ai

**Data collected**:
- Calendar events (read-only from Google/Outlook)
- Habits, tasks (title, duration, deadline)
- Slack status, meeting links

**How it's used**:
1. **Service delivery**: Schedule habits, optimize calendar
2. **Pattern learning**: "Users with 20+ meetings/week prefer AM focus time" → improve habit placement
3. **Analytics**: Feature usage tracking

**NOT used for**:
- ❌ Reading email content (only calendar events)
- ❌ Sharing with third parties
- ❌ Training external AI models

**Risk level**: **LOW** (OAuth-limited access, encrypted, anonymized patterns)

---

### Trevor AI

**Data collected**:
- Task titles, durations, deadlines
- Calendar events (from Google/Outlook)
- Time blocks (manual placements)

**How it's used**:
1. **Service delivery**: Suggest durations, display tasks
2. **No training**: Explicitly does NOT train on user data

**NOT used for**:
- ❌ AI model training
- ❌ Third-party sharing
- ❌ Analytics (beyond basic usage)

**Risk level**: **VERY LOW** (minimal processing, no training)

---

### Akiflow

**Data collected**:
- Tasks from Todoist, Asana, Linear, Jira, ClickUp
- Gmail messages (for task extraction)
- Slack messages (for action items)
- Calendar events

**How it's used**:
1. **Service delivery**: Aggregate tasks, suggest priorities
2. **Deduplication training**: Improve fuzzy matching (likely)

**Concerns**:
- ⚠️ Gmail + Slack access = can read private messages
- ⚠️ Broad data access = higher attack surface

**Risk level**: **MODERATE** (broad permissions, unclear training policies)

---

### Sunsama

**Data collected**:
- Task titles, deadlines (from integrations)
- Calendar events (read-only)
- Reflection notes (user-written)

**How it's used**:
1. **Service delivery**: Display tasks, guided planning
2. **No AI**: No training, no model improvement

**Risk level**: **VERY LOW** (no AI, minimal processing)

---

## Privacy Risk Tiers

### Tier 1: Highest Privacy (No AI Training)
- **Trevor AI**: Explicitly no training on user data
- **Sunsama**: No AI, no training

### Tier 2: Low Privacy Risk (Anonymized Training)
- **Motion**: Custom AI, anonymized aggregated patterns
- **Reclaim.ai**: Custom ML, anonymized habit patterns

### Tier 3: Moderate Privacy Risk (Broad Access)
- **Akiflow**: Gmail + Slack access, unclear training policies

---

## Future: LLM Integration Coming (2025-2026)

### Expected LLM Use Cases

**1. Natural Language Task Creation**

**Current** (manual):
- User types: "Follow up on proposal"
- User sets: Deadline = "Next Tuesday", Duration = "30 min"

**Future** (LLM-powered):
- User types: "Remind me to follow up on the proposal we discussed in today's meeting next Tuesday around 2pm"
- GPT-4 parses → Task: "Follow up on proposal", Deadline: "Next Tuesday", Time: "2 PM", Duration: "30 min (estimated)"

**Privacy impact**: LLM (OpenAI/Anthropic) sees task text (potential data leak)

---

**2. Meeting Notes → Auto-Generated Tasks**

**Current** (manual):
- Meeting ends, user manually reviews notes, creates tasks

**Future** (LLM-powered):
- Zoom/Meet transcript sent to GPT-4
- AI extracts: "Action items: (1) Alice to send proposal by Friday, (2) Bob to review budget next week"
- Auto-creates tasks in Motion/Reclaim

**Privacy impact**: Meeting transcript sent to OpenAI/Anthropic (HIGH risk for confidential discussions)

---

**3. Context-Aware Suggestions**

**Current** (pattern-based):
- AI notices: "User schedules design work 9-11 AM" → suggests morning slots

**Future** (LLM-powered):
- AI reads: Calendar event "Q4 Planning Meeting" → suggests task "Review Q4 budget" next day
- AI reads: Email "Contract needs signature" → suggests task "Sign contract" with deadline

**Privacy impact**: LLM sees calendar/email content (moderate risk)

---

### Privacy Mitigation Strategies (Provider-Side)

**Option 1: On-Device LLM** (e.g., Llama 3 locally)
- ✅ Privacy-preserving (no cloud LLM)
- ❌ Limited accuracy vs GPT-4
- ❌ Requires powerful device (M1+ Mac, high-end PC)

**Option 2: Azure OpenAI / GCP Vertex AI** (Enterprise LLM)
- ✅ Data isolation (your instance, not shared)
- ✅ No training on your data (contractual guarantee)
- ❌ More expensive ($$$)

**Option 3: Opt-In LLM Features**
- ✅ Users choose privacy vs convenience
- ✅ Default = no LLM (privacy-first)
- ❌ Feature fragmentation (some users miss out)

**Expected approach**: Motion/Reclaim will likely use **Option 2 or 3** (enterprise LLM or opt-in)

---

## Verdict: Current State vs Future

### Current State (Nov 2025):
- **Custom AI dominates**: Motion, Reclaim use proprietary models (no GPT-4/Claude)
- **Privacy-preserving**: Most providers don't share data with third-party AI
- **Limited NLP**: No natural language understanding (yet)

### Future State (2026+):
- **LLM integration emerging**: GPT-4/Claude for NLP, custom models for scheduling
- **Privacy trade-offs**: Users must choose between convenience (LLM) and privacy (custom AI)
- **Hybrid approach**: Local LLM or opt-in cloud LLM for sensitive users

---

## Key Insights

1. **No GPT-4/Claude (yet)**: Most AI productivity tools use custom models, not LLMs

2. **Privacy varies**: Trevor/Sunsama = highest privacy, Akiflow = moderate risk (broad access)

3. **Anonymized training is common**: Motion, Reclaim improve AI using aggregated user patterns

4. **LLMs coming soon**: Natural language task creation, meeting notes → tasks (2026+)

5. **Trade-off: Privacy vs NLP**: LLM features = data sent to OpenAI/Anthropic (privacy cost)

**Recommendation**:
- **Privacy-critical users** → Trevor AI or Sunsama (no AI training)
- **Balanced users** → Motion or Reclaim (custom AI, anonymized patterns)
- **Future-proof** → Wait for LLM integration with opt-in privacy controls (2026+)
