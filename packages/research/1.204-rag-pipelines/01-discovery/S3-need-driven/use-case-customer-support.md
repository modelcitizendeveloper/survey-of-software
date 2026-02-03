# Use Case: Customer Support Chatbot

## Scenario

**Organization:** E-commerce SaaS platform (B2B, 10K business customers)
**Problem:** Support team overwhelmed with repetitive questions about product features, billing, integrations
**Goal:** Build AI chatbot to handle 70% of tier-1 support queries, reducing support load

## Requirements

### Must-Have Features

✅ **High query volume** - Handle 50K+ queries/month (peak: 100K+)
✅ **Low latency** - < 2 second response time (customers are impatient)
✅ **Conversation memory** - Multi-turn conversations (follow-up questions)
✅ **Fallback to human** - Escalate when confidence is low
✅ **Multi-language** - English, Spanish, French support

### Nice-to-Have Features

⚪ **Integration with ticketing** - Create tickets seamlessly
⚪ **Analytics dashboard** - Track query types, resolution rates
⚪ **A/B testing** - Test different retrieval strategies
⚪ **Auto-improving** - Learn from human feedback

### Constraints

📊 **Scale:** 50K-100K queries/month, spiky traffic (peak hours 10× baseline)
💰 **Budget:** **CRITICAL** - High volume = cost must be optimized
⏱️ **Latency:** < 2 seconds (firm SLA)
🔒 **Availability:** 99.9% uptime required
🛠️ **Team:** 1-2 engineers maintaining, not full-time

### Success Criteria

- Resolve 70% of tier-1 queries without human intervention
- Maintain < 2 sec response time at p95
- Customer satisfaction score > 4/5 for bot interactions
- **Cost < $5,000/month** (current per-agent cost × reduction)

---

## Framework Evaluation

### Cost Analysis (Critical Factor)

| Framework | Tokens/Query | 50K Queries/Month | 100K Queries/Month |
|-----------|--------------|-------------------|---------------------|
| **LangChain** | 2,400 | $1,200/mo | $2,400/mo |
| **LlamaIndex** | 1,600 | $800/mo | $1,600/mo |
| **Haystack** | 1,570 | $785/mo | $1,570/mo |

**Cost Differential (at 100K queries/month):**
- LangChain: $2,400/mo = $28,800/year
- LlamaIndex: $1,600/mo = $19,200/year (**33% savings** vs LangChain)
- Haystack: $1,570/mo = $18,840/year (**35% savings** vs LangChain)

**At scale (100K queries/month), Haystack saves $9,960/year vs LangChain.**

---

### LangChain - Fit Analysis

**Must-Haves:**
- ✅ **High volume**: Can handle (async support, batch processing)
- ⚠️ **Low latency**: 10ms overhead + 1-2 sec LLM call → ~2 sec total → ⚠️ Tight margin
- ✅ **Conversation memory**: Built-in (ConversationalRetrievalChain)
- ✅ **Fallback logic**: Can implement confidence thresholds
- ✅ **Multi-language**: Supports multi-language embeddings and LLMs

**Nice-to-Haves:**
- ⚪ **Ticketing integration**: Not built-in, custom development
- ⚪ **Analytics**: LangSmith provides some, but custom dashboard needed
- ⚪ **A/B testing**: Not built-in
- ⚪ **Auto-improving**: Custom feedback loop

**Constraints:**
- 💰 **Budget**: $28,800/year → ⚠️ **Exceeds $5K/month at 100K queries** ($2,400/mo)
- ⏱️ **Latency**: 10ms overhead → ⚠️ Cutting it close at 2 sec SLA
- 🔒 **Availability**: Depends on deployment (no inherent HA features)
- 🛠️ **Maintenance**: Large codebase, breaking changes → ⚠️ Higher burden

**Fit Score:** 68/100

**Strengths:**
- Conversation memory out of the box
- Multi-language support strong
- Ecosystem has customer support examples

**Weaknesses:**
- **Cost**: Highest of three ($9,960/year more than Haystack at 100K queries/month)
- **Latency**: Slowest overhead (10ms)
- Breaking changes increase maintenance

**Implementation Complexity:** Low-Medium (30-40 LOC for basic chatbot with memory)

---

### LlamaIndex - Fit Analysis

**Must-Haves:**
- ✅ **High volume**: Can handle
- ✅ **Low latency**: 6ms overhead → ✅ Better margin than LangChain
- ✅ **Conversation memory**: Via agentic RAG (slightly more setup than LangChain)
- ✅ **Fallback logic**: Can implement
- ✅ **Multi-language**: Supported

**Nice-to-Haves:**
- ⚪ **Ticketing integration**: Custom
- ⚪ **Analytics**: RAGAS integration for evaluation, but custom dashboard
- ⚪ **A/B testing**: Custom
- ⚪ **Auto-improving**: Custom

**Constraints:**
- 💰 **Budget**: $19,200/year → ✅ **Within budget** ($1,600/mo < $5K/mo)
- ⏱️ **Latency**: 6ms overhead + RAG = ~1.8 sec → ✅ Good margin
- 🔒 **Availability**: Custom deployment setup
- 🛠️ **Maintenance**: Moderate

**Fit Score:** 74/100

**Strengths:**
- **Cost**: 33% cheaper than LangChain ($9,600/year savings)
- **Latency**: Good (6ms overhead)
- **RAG performance**: 20-30% faster queries

**Weaknesses:**
- Conversation memory slightly more complex (agent setup vs chain)
- Smaller community for customer support use case examples

**Implementation Complexity:** Medium (40-50 LOC for chatbot with conversational agent)

---

### Haystack - Fit Analysis

**Must-Haves:**
- ✅ **High volume**: Designed for production scale, K8s-native
- ✅✅ **Low latency**: 5.9ms overhead → **Best margin** (~1.7 sec total)
- ⚠️ **Conversation memory**: Not built-in, requires custom pipeline state management
- ✅ **Fallback logic**: Can implement via pipeline branching
- ✅ **Multi-language**: Supported

**Nice-to-Haves:**
- ⚪ **Ticketing integration**: Custom
- ✅ **Analytics**: Built-in monitoring hooks, easier to add custom dashboard
- ⚪ **A/B testing**: Custom, but pipeline serialization helps (YAML configs)
- ⚪ **Auto-improving**: Custom

**Constraints:**
- 💰 **Budget**: $18,840/year → ✅✅ **Best cost** ($1,570/mo, well under $5K/mo limit)
- ⏱️ **Latency**: 5.9ms overhead → ✅✅ **Best performance**, comfortable margin
- 🔒 **Availability**: K8s-native → ✅✅ Can deploy highly available setup easily
- 🛠️ **Maintenance**: Stable API, component isolation → ✅ Lower burden

**Fit Score:** 80/100

**Strengths:**
- **Best cost efficiency**: $9,960/year savings vs LangChain
- **Best latency**: 5.9ms overhead = most headroom for 2 sec SLA
- **Production infrastructure**: K8s-native, monitoring, high availability
- **Observability**: Built-in logging/monitoring helps track issues

**Weaknesses:**
- **No built-in conversation memory**: Requires custom state management (adds ~50 LOC)
- More boilerplate initially

**Implementation Complexity:** Medium-High (60-80 LOC total: 40 for basic chatbot + 40 for conversation state)

---

## Comparison Matrix

| Requirement | LangChain | LlamaIndex | Haystack |
|-------------|-----------|------------|----------|
| **Cost (100K/mo)** | $2,400/mo ❌ | $1,600/mo ✅ | **$1,570/mo ✅✅** |
| **Latency overhead** | 10ms ⚠️ | 6ms ✅ | **5.9ms ✅✅** |
| **Conversation memory** | ✅✅ Built-in | ✅ Agent-based | ⚠️ Custom |
| **High availability** | ⚠️ Custom | ⚠️ Custom | ✅✅ K8s-native |
| **Observability** | ✅ LangSmith | ⚠️ Manual | ✅ Built-in |
| **Implementation (LOC)** | 30-40 | 40-50 | 60-80 |
| **Annual cost** | $28,800 | $19,200 | **$18,840** |

---

## Recommendation

### Primary: **Haystack**

**Fit: 80/100**

**Rationale:**

For high-volume customer support, **cost and latency are paramount**:

1. **Cost optimization critical**: At 100K queries/month, Haystack saves **$9,960/year** vs LangChain
   - This saving pays for ~1.5 months of engineering time
   - Scales linearly: 200K queries/month = $19,920/year savings

2. **Best latency**: 5.9ms overhead provides most headroom for 2 sec SLA
   - LangChain's 10ms cuts it close
   - Traffic spikes could push LangChain over SLA

3. **Production-ready**: K8s-native deployment = easy HA setup
   - 99.9% uptime easier to achieve
   - Observability built-in helps track issues in production

4. **ROI calculation**:
   - **Extra development time**: ~40 hours to build custom conversation state
   - **Engineering cost**: ~$5,000 one-time
   - **Savings vs LangChain**: $9,960/year
   - **Payback period**: 6 months
   - **Years 2-5**: Pure savings

**Trade-off Accepted:** Spending 1-2 weeks upfront to build conversation state saves ~$10K/year and ensures better latency.

### Alternative: **LlamaIndex** (for faster implementation)

**Fit: 74/100**

If time-to-market is more critical than cost optimization:

- Still saves $9,600/year vs LangChain
- Conversation via agents (less custom code than Haystack)
- Good latency (6ms)

**Trade-off:** Paying ~$360/year more than Haystack for easier conversation memory.

### Not Recommended: **LangChain** (for this use case)

**Fit: 68/100**

While LangChain has easiest conversation memory:

- **Cost**: $9,960/year premium over Haystack is unjustifiable
- **Latency**: 10ms overhead leaves least margin for SLA
- **Maintenance**: Breaking changes increase burden on small team

At high volume (100K+ queries/month), cost efficiency matters more than development convenience.

---

## Implementation Estimate

### Haystack (Recommended)

**MVP (Basic Chatbot):** 3-4 days
- Document loading (help docs, FAQs): 1 day
- RAG pipeline: 1 day
- Conversation state management: 1-2 days
- Testing: 1 day

**Production (HA, monitoring, fallback):** +2 weeks
- Kubernetes deployment: 3-4 days
- Monitoring/alerting: 2-3 days
- Fallback logic: 2 days
- Load testing: 2 days

**Total:** 3 weeks to production

### Cost Breakdown (Annual, at 100K queries/month)

- **API costs**: $18,840 (Haystack)
- **Hosting (K8s cluster)**: $3,600-6,000
- **Development (one-time)**: $15,000 (3 weeks × $5K/week)
- **Maintenance**: $6,000/year (2 hours/month × $250/hr)

**Total Year 1:** ~$43,000-46,000
**Total Year 2+:** ~$28,000/year (recurring)

**Cost Comparison with LangChain:**
- LangChain Year 1: $48,000-51,000 (higher API costs offset easier implementation)
- LangChain Year 2+: **$38,000/year** (recurring)

**5-Year TCO:**
- Haystack: $43K + ($28K × 4) = **$155,000**
- LangChain: $48K + ($38K × 4) = **$200,000**

**Haystack saves $45,000 over 5 years** despite higher initial development.

---

## Key Insight

For high-volume, cost-sensitive applications, **initial implementation convenience is a false economy**.

LangChain's built-in conversation memory saves 1-2 weeks upfront but costs $9,960/year extra. The payback period is < 6 months.

**S3 reveals Haystack's strength**: When cost and latency are primary constraints (high-volume production), Haystack's technical superiority (S2) becomes business-critical.

**S3 contradicts S1 recommendation**: Popularity (LangChain's 124K stars) is irrelevant when cost compounds at scale.
