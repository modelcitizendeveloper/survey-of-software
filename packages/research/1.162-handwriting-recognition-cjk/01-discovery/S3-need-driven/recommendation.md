# S3 Need-Driven Discovery: Recommendation

## Use Case Decision Matrix

| Use Case | Recommended Solution | Confidence | Key Trade-Off |
|----------|---------------------|------------|---------------|
| **IME** | Pure Zinnia | 95% | Latency non-negotiable, accuracy adequate with LM |
| **Document Archives** | Google Cloud Vision | 90% | Accuracy critical, cost justified by archival value |
| **Language Learning** | Hybrid (Zinnia + Google) | 88% | Realtime feedback + accurate grading both required |
| **Healthcare Forms** | Zinnia/Tegaki on-prem | 92% | Privacy non-negotiable, accuracy acceptable @ 90% |
| **Note-Taking App** | Hybrid or Pure Zinnia | 85% | Offline + cost critical, accuracy nice-to-have |

---

## Use Case 1: Input Method Editor (IME)

### Requirements Fit

| Requirement | Weight | Zinnia | Tegaki | Google | Azure |
|-------------|--------|--------|--------|--------|-------|
| Latency < 50ms (P95) | Must-have | ✅ 40ms | ❌ 150ms | ❌ 400ms | ❌ 500ms |
| Offline capable | Must-have | ✅ Yes | ✅ Yes | ❌ No | ❌ No |
| Memory < 10MB | Must-have | ✅ 2-5MB | ⚠️ 15MB | ✅ N/A | ✅ N/A |
| Accuracy > 80% | Must-have | ✅ 85-90% | ✅ 82-88% | ✅ 96-98% | ✅ 94-97% |
| Cost $0/request | Must-have | ✅ Free | ✅ Free | ❌ $1.50/1K | ❌ $10/1K |

**Must-have hits:**
- Zinnia: 5/5 ✅
- Tegaki: 4/5 (fails latency)
- Google: 2/5 (fails latency, offline, cost)
- Azure: 2/5 (fails latency, offline, cost)

**Winner:** Zinnia (only solution meeting all must-haves)

**Confidence:** 95% (well-documented IME deployments prove feasibility)

**Trade-off accepted:** 85-90% accuracy sufficient because:
- Language model provides context-based correction
- Users typically input phrases, not isolated characters
- Single-character 85% → Phrase-level 95%+ with good LM

---

## Use Case 2: Document Digitization (Archives)

### Requirements Fit

| Requirement | Weight | Zinnia | Tegaki | Google | Azure |
|-------------|--------|--------|--------|--------|-------|
| Accuracy > 95% | Must-have | ❌ 85-90% | ❌ 82-88% | ✅ 96-98% | ✅ 94-97% |
| Cursive handling | Must-have | ⚠️ 70-80% | ⚠️ 68-78% | ✅ 92-96% | ✅ 90-95% |
| Multi-language | Nice-to-have | ⚠️ CJK | ⚠️ CJK | ✅ 100+ | ✅ 100+ |
| Batch processing | Nice-to-have | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Low cost | Nice-to-have | ✅ Free | ✅ Free | ⚠️ $1.50/1K | ❌ $10/1K |

**Must-have hits:**
- Zinnia: 0/2 (fails accuracy, cursive)
- Tegaki: 0/2 (fails accuracy, cursive)
- Google: 2/2 ✅
- Azure: 2/2 ✅

**Winner:** Google Cloud Vision (slightly better accuracy + lower cost than Azure)

**Confidence:** 90% (archival applications justify cloud cost)

**Trade-off accepted:** $1.50/1000 requests acceptable because:
- Archival digitization is one-time batch job (not continuous)
- 10K documents × $0.0015 = $15 (negligible for preservation budget)
- Accuracy errors in archives = permanent data loss

**Google vs Azure:** Google preferred unless:
- Enterprise compliance required (HIPAA, FedRAMP) → Azure
- Already in Azure ecosystem → Azure (integration simpler)

---

## Use Case 3: Language Learning Application

### Requirements Fit

| Requirement | Weight | Zinnia | Tegaki | Google | Hybrid |
|-------------|--------|--------|--------|--------|--------|
| Realtime feedback < 100ms | Must-have | ✅ 30ms | ⚠️ 100ms | ❌ 300ms | ✅ 30ms (fast path) |
| Accuracy > 95% (grading) | Must-have | ❌ 85-90% | ❌ 82-88% | ✅ 96-98% | ✅ 94-96% |
| Stroke order validation | Must-have | ✅ Yes | ✅ Yes | ❌ No | ✅ Yes (Zinnia) |
| Cost-effective | Must-have | ✅ Free | ✅ Free | ❌ High vol | ✅ 30% cloud |
| Offline nice-to-have | Nice-to-have | ✅ Yes | ✅ Yes | ❌ No | ⚠️ Degraded |

**Must-have hits:**
- Zinnia: 3/4 (fails accuracy)
- Tegaki: 3/4 (fails accuracy)
- Google: 2/4 (fails latency, stroke order)
- **Hybrid: 4/4** ✅

**Winner:** Hybrid (Zinnia realtime + Google validation)

**Confidence:** 88% (architecture addresses conflicting requirements)

**Architecture:**
```
Student draws stroke → Zinnia preview (30ms)
  ↓
Student completes character → Google validation (300ms async)
  ↓
Result: Fast feedback (Zinnia) + Accurate grade (Google)
```

**Cost analysis (1M students, 100 characters/student/month):**
- Pure Google: 100M requests × $1.50/1000 = $150,000/month
- Hybrid (30% Google): 30M requests × $1.50/1000 = $45,000/month
- **Savings:** $105,000/month ($1.26M/year)

**Trade-off accepted:** Requires both technologies (complexity), but cost savings justify integration effort.

---

## Use Case 4: Healthcare Forms (Privacy-Sensitive)

### Requirements Fit

| Requirement | Weight | Zinnia | Tegaki | Google | Azure Stack |
|-------------|--------|--------|--------|--------|-------------|
| On-premise (HIPAA) | Must-have | ✅ Yes | ✅ Yes | ❌ Cloud | ✅ Yes |
| No data transmission | Must-have | ✅ Yes | ✅ Yes | ❌ Cloud | ✅ Local |
| Accuracy > 90% | Must-have | ⚠️ 85-90% | ❌ 82-88% | ✅ 96-98% | ✅ 94-97% |
| Audit trail | Nice-to-have | ⚠️ DIY | ⚠️ DIY | ✅ Built-in | ✅ Built-in |
| Cost-effective | Nice-to-have | ✅ Free | ✅ Free | ❌ N/A | ❌ $100K+ |

**Must-have hits:**
- Zinnia: 2.5/3 (marginal accuracy)
- Tegaki: 2/3 (fails accuracy)
- Google: 0/3 (cloud-only)
- Azure Stack: 3/3 ✅ (but expensive)

**Winner:** Zinnia (cost-effective) or Azure Stack (if budget allows)

**Confidence:** 92% (privacy requirements eliminate cloud)

**Decision criteria:**
- **Budget < $20K:** Zinnia on-premise (free, adequate accuracy)
- **Budget > $50K:** Azure Stack (best accuracy, compliance features)

**Trade-off accepted:**
- Zinnia: Lower accuracy (85-90%) accepted because medical staff verify
- Azure Stack: High cost ($100K+ setup) justified by compliance value

**Mitigation strategy (Zinnia):**
- Human-in-the-loop: Staff verify recognized text (reduces error impact)
- Confidence threshold: Flag low-confidence recognition for manual review
- Result: Effective accuracy 98%+ (85-90% auto + 100% human on low-conf)

---

## Use Case 5: Mobile Note-Taking App

### Requirements Fit

| Requirement | Weight | Zinnia | Tegaki | Google | Hybrid |
|-------------|--------|--------|--------|--------|--------|
| Realtime < 200ms | Must-have | ✅ 30ms | ⚠️ 100ms | ⚠️ 300ms | ✅ 30-100ms |
| Offline capable | Must-have | ✅ Yes | ✅ Yes | ❌ No | ⚠️ Degraded |
| Cost $0/request | Must-have | ✅ Free | ✅ Free | ❌ $1.50/1K | ⚠️ 30% cloud |
| Accuracy > 90% | Nice-to-have | ⚠️ 85-90% | ❌ 82-88% | ✅ 96-98% | ✅ 93-95% |
| Cross-device sync | Nice-to-have | ⚠️ DIY | ⚠️ DIY | ✅ Yes | ⚠️ DIY |

**Must-have hits:**
- Zinnia: 3/3 ✅
- Tegaki: 3/3 ✅ (but slower)
- Google: 1/3 (fails offline, cost)
- Hybrid: 2.5/3 (marginal on cost)

**Winner:** Zinnia (primary) or Hybrid (premium tier)

**Confidence:** 85% (depends on business model)

**Recommendation by business model:**

**Freemium model:**
- Free tier: Pure Zinnia (85-90% accuracy, fully offline)
- Premium tier ($5-10/mo): Hybrid (93-95% accuracy, sync via cloud)
- Upsell value: Better accuracy justifies $5-10/mo subscription

**Subscription-only model:**
- Hybrid from day 1 (93-95% accuracy differentiates from free competitors)
- Cost: $0.45-$0.75/user/month (assuming 30 notes/month, 70% Zinnia)
- Margins: Acceptable for $5-10/mo subscription

**Trade-off accepted:**
- Free tier: Lower accuracy (85-90%) sufficient for casual users
- Premium: 30% cloud cost ($0.45/user/mo) justified by subscription revenue

---

## Convergence with S1/S2

| Finding | S1 (Rapid) | S2 (Comprehensive) | S3 (Need-Driven) | Convergence |
|---------|------------|-------------------|------------------|-------------|
| **Zinnia for IME** | Recommended | 8.21/10 (highest) | Only solution (95% conf) | ✅ Strong |
| **Cloud for accuracy** | Recommended | 9.5/10 accuracy | Required (Archives, Learning) | ✅ Strong |
| **Hybrid optimal** | Recommended | 93-95% accuracy | Best for Learning, Notes | ✅ Strong |
| **Privacy = on-prem** | Mentioned | Not analyzed | Healthcare requires | ✅ New insight |
| **No single winner** | Stated | Quantified | Validated by use cases | ✅ Strong |

**New insight from S3:** Privacy-sensitive use cases (healthcare, legal, finance) eliminate cloud options entirely. This creates binary decision: on-premise open-source (Zinnia/Tegaki) or expensive on-premise cloud (Azure Stack). No middle ground.

---

## Decision Framework

### Step 1: Classify Your Requirements

**Performance-critical:** Latency < 50ms AND offline required
→ **Zinnia** (no alternative)

**Accuracy-critical:** Accuracy > 95% AND cost acceptable
→ **Cloud ML** (Google or Azure)

**Privacy-critical:** Data must stay on-premise
→ **On-premise** (Zinnia/Tegaki or Azure Stack)

**Cost-critical:** Zero per-request cost AND accuracy > 85%
→ **Zinnia or Hybrid**

**Balanced:** Multiple competing requirements
→ **Hybrid** (best trade-offs)

### Step 2: Validate Must-Haves

Check if chosen solution meets ALL must-have requirements. If any must-have fails:
- Can requirement be relaxed? (e.g., 92% accuracy acceptable instead of 95%)
- Can workaround mitigate gap? (e.g., human verification for low-confidence)
- If no flexibility: Choose different solution or build custom

### Step 3: Optimize Nice-to-Haves

Maximize nice-to-have requirements met, weighted by business value.

### Step 4: Assess Risk

**Technical risk:**
- Open-source: Maintenance burden, expertise required
- Cloud: Vendor lock-in, pricing changes

**Business risk:**
- High cost: Budget constraints
- Low accuracy: User satisfaction, error correction costs

**Mitigation:**
- Start with lowest-risk solution (often cloud ML)
- Add optimizations (e.g., Zinnia fast path) once validated

---

## Gap Analysis

### Identified Gaps

**Gap 1: No solution provides <50ms latency + 95%+ accuracy**
- Cloud ML: High accuracy but 250-600ms latency
- Zinnia: Low latency but 85-90% accuracy
- **Workaround:** Hybrid (fast preview + async validation)

**Gap 2: No affordable on-premise solution with 95%+ accuracy**
- Zinnia/Tegaki: Affordable but 85-90% accuracy
- Azure Stack: 95% accuracy but $100K+ cost
- **Workaround:** Human-in-the-loop (verify low-confidence)

**Gap 3: Cloud ML lacks stroke order validation**
- Google/Azure: Image-based, no temporal data
- Zinnia/Tegaki: Stroke-aware
- **Workaround:** Use Zinnia for stroke validation + cloud for final accuracy check

**Gap 4: Open-source training requires ML expertise**
- Pre-trained models adequate for Japanese
- Chinese/Korean models less mature
- **Workaround:** Start with pre-trained, custom train only if needed

---

## Final Recommendation

**Use case-specific recommendations validated:**
- ✅ IME: Pure Zinnia (95% confidence)
- ✅ Archives: Google Cloud (90% confidence)
- ✅ Learning: Hybrid (88% confidence)
- ✅ Healthcare: Zinnia on-premise (92% confidence)
- ✅ Note-taking: Zinnia or Hybrid (85% confidence)

**Overall pattern:** No single solution fits all use cases. Choose based on priority:
1. **Privacy first?** → On-premise open-source
2. **Performance first?** → Zinnia
3. **Accuracy first?** → Cloud ML
4. **Balanced?** → Hybrid

**Confidence:** 87% (use case analysis validates S1/S2 recommendations)

**Next step:** S4 (Strategic) to assess long-term viability (5-10 year outlook)
