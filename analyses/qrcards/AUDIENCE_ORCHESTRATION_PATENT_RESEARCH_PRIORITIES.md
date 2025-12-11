# Audience Orchestration Patent - Research Priorities

**Date**: December 2, 2025
**Purpose**: Validate technical feasibility and competitive differentiation before provisional patent filing
**Context**: NSA Northwest membership provides immediate audience for "patent pending" positioning
**Investment Decision**: $2,500 provisional filing - worth it only if technical claims are defensible

---

## Executive Summary

**Current State**: Audience Orchestration patent is 85% conceptual - real-time synchronization not yet built.

**Key Patent Claims to Validate**:
1. <50ms device synchronization across 1,000-10,000 devices
2. QR-based rapid device registration
3. Real-time audience segmentation and adaptive content delivery
4. Multi-modal content orchestration

**Research Goal**: 8-10 hours of targeted research to answer:
- Is <50ms sync achievable at scale? At what cost?
- What prior art exists? Are we differentiated or reinventing?
- Build vs buy: What infrastructure do we need?
- What do speakers/event organizers use now?

---

## Research Priority Queue

### Tier 1: Core Technical Claims (CRITICAL - Do Before Filing)

#### 2.073 - WebSocket & Real-time Communication Services

**Priority**: 🔴 CRITICAL
**Estimated Time**: 2-3 hours (S1-rapid)
**Status**: Not yet researched

**Research Questions**:
1. What latency is achievable with managed WebSocket services (Pusher, Ably, Socket.io)?
2. What are the scaling limits? Cost at 1,000 / 5,000 / 10,000 concurrent connections?
3. Self-hosted vs managed: What's the operational burden?
4. How do these services handle fan-out (one message to many devices)?
5. What's the realistic latency range? Is <50ms achievable or marketing fiction?

**Candidates to Evaluate**:
- **Pusher** - Market leader, simple API
- **Ably** - Enterprise focus, guaranteed ordering
- **Socket.io** - Self-hosted, open source
- **Supabase Realtime** - PostgreSQL-based, already in our stack consideration
- **Firebase Realtime Database** - Google infrastructure
- **AWS IoT Core** - Enterprise scale, complex
- **Centrifugo** - Self-hosted, high performance

**Success Criteria**:
- [ ] Latency benchmarks at scale (documented, not marketing claims)
- [ ] Cost model for 1,000-device event
- [ ] Integration complexity assessment
- [ ] Clear recommendation: build vs buy

**Patent Relevance**: The <50ms claim is the technical differentiator. If this is trivially achievable with off-the-shelf services, the patent may lack novelty. If it requires novel orchestration logic, that's where the IP lives.

---

#### 3.081 - Live Event Audience Engagement Platforms

**Priority**: 🔴 CRITICAL
**Estimated Time**: 2-3 hours (S1-rapid)
**Status**: Not yet researched

**Research Questions**:
1. What do Slido, Mentimeter, Poll Everywhere actually do?
2. Do any offer real-time content synchronization (not just polling)?
3. What's the state of "second screen" experiences at conferences?
4. Are there enterprise solutions for large-scale audience orchestration?
5. What's the pricing model? Per-event? Per-attendee?

**Candidates to Evaluate**:
- **Slido** (Cisco) - Q&A, polling, quizzes
- **Mentimeter** - Interactive presentations
- **Poll Everywhere** - Audience response
- **Kahoot!** - Gamified engagement
- **Crowdpurr** - Live trivia/games
- **Pigeonhole Live** - Enterprise Q&A
- **Glisser** - Presentation interaction

**Success Criteria**:
- [ ] Feature matrix: What do existing platforms offer?
- [ ] Gap analysis: What DON'T they do that we're claiming?
- [ ] Pricing benchmarks for competitive positioning
- [ ] Prior art risk assessment

**Patent Relevance**: If Slido already does "audience orchestration," we need to articulate what's novel about QR-based registration + real-time sync. The differentiation may be in the physical-digital bridge (QR tokens) rather than the sync itself.

---

#### 3.082 - Device Synchronization & Second Screen Technology

**Priority**: 🔴 CRITICAL
**Estimated Time**: 2-3 hours (S1-rapid)
**Status**: Not yet researched

**Research Questions**:
1. How do concert/stadium apps synchronize light shows across devices?
2. What technology powers "second screen" TV experiences?
3. Are there patents in this space we need to design around?
4. What's the state of the art in broadcast synchronization?
5. How do sports venues coordinate fan experiences?

**Areas to Investigate**:
- **Concert apps** (Coldplay wristbands, Phish app)
- **Stadium experiences** (NFL, NBA fan engagement)
- **Broadcast sync** (TV + phone experiences)
- **Gaming** (Twitch plays Pokemon, crowd-controlled games)
- **Academic research** on distributed synchronization

**Success Criteria**:
- [ ] Prior art inventory (patents, products, research)
- [ ] Technical approaches documented
- [ ] Differentiation opportunities identified
- [ ] Risk assessment for patent claims

**Patent Relevance**: This is where blocking patents may exist. Concert/stadium sync is a mature field. Our differentiation may be the QR-based registration flow + dynamic audience segmentation, not the sync itself.

---

### Tier 2: Supporting Infrastructure

#### 3.042 - Redis Hosting (Addendum: Pub/Sub for Real-time)

**Priority**: 🟡 MEDIUM
**Estimated Time**: 1-2 hours (S2-addendum to existing research)
**Status**: Exists but needs real-time focus

**Research Questions**:
1. How does Redis Pub/Sub perform for real-time fan-out?
2. What's the message throughput for 10,000 subscribers?
3. Redis Streams vs Pub/Sub for ordered delivery?
4. Managed Redis (Upstash, Redis Cloud) latency characteristics?

**Patent Relevance**: If we build on Redis pub/sub, the innovation is in the orchestration logic, not the transport layer.

---

#### 3.400 - Backend-as-a-Service (Addendum: Realtime Features)

**Priority**: 🟡 MEDIUM
**Estimated Time**: 1-2 hours (S2-addendum)
**Status**: Exists but needs realtime deep-dive

**Research Questions**:
1. Supabase Realtime: What are the actual latency numbers?
2. Firebase Realtime Database: Scaling characteristics?
3. Convex, Liveblocks, PartyKit: New entrants worth evaluating?
4. Do BaaS realtime features solve our problem out of the box?

**Patent Relevance**: If Supabase Realtime + simple orchestration logic = our product, we're building a feature, not patentable innovation. Need to identify what's novel.

---

### Tier 3: Competitive Landscape

#### 3.080 - Event Management Platforms

**Priority**: 🟢 LOW-MEDIUM
**Estimated Time**: 2 hours (S1-rapid)
**Status**: Empty (only CATEGORY_STRUCTURE.md exists)

**Research Questions**:
1. What do Hopin, Bizzabo, Whova offer for audience engagement?
2. Are there event platforms with real-time orchestration features?
3. What's the integration landscape? APIs, webhooks?
4. Pricing models: per-event, per-attendee, enterprise?

**Candidates to Evaluate**:
- **Hopin** - Virtual/hybrid events
- **Bizzabo** - Enterprise event management
- **Whova** - Conference app platform
- **Cvent** - Enterprise events
- **Eventbrite** - Ticketing (less relevant)
- **Swoogo** - Registration + engagement

**Patent Relevance**: Understanding the competitive landscape helps position the patent claims. If no event platform offers real-time orchestration, that's a market gap we're filling.

---

#### 3.083 - Audience Response Systems (New Category)

**Priority**: 🟢 LOW
**Estimated Time**: 1-2 hours (S1-rapid)
**Status**: Does not exist

**Research Questions**:
1. What hardware clicker systems exist? (iClicker, Turning Technologies)
2. How do speakers currently engage audiences?
3. What's the gap between clickers and our vision?
4. NSA members: What tools do professional speakers actually use?

**Patent Relevance**: Understanding the non-digital baseline helps articulate the innovation. "QR-based orchestration vs physical clickers" is a clearer differentiation story.

---

## Research Execution Plan

### Phase 1: Technical Validation (4-6 hours)

```
Day 1:
├─ 2.073 WebSocket Services (2-3 hours)
│  └─ Answer: Is <50ms achievable? At what cost/scale?
└─ 3.042 Redis Pub/Sub addendum (1 hour)
   └─ Answer: Is Redis sufficient for our needs?

Day 2:
├─ 3.081 Audience Engagement Platforms (2-3 hours)
│  └─ Answer: What exists? Where's our differentiation?
└─ 3.400 BaaS Realtime addendum (1 hour)
   └─ Answer: Does Supabase/Firebase solve this already?
```

### Phase 2: Competitive & Prior Art (3-4 hours)

```
Day 3:
├─ 3.082 Device Synchronization (2-3 hours)
│  └─ Answer: What prior art exists? Risk assessment?
└─ 3.080 Event Management (1-2 hours)
   └─ Answer: What's the competitive landscape?
```

### Phase 3: Decision Point

After ~8-10 hours of research:

**Proceed with $2,500 filing IF**:
- [ ] <50ms sync is achievable with reasonable infrastructure ($100-500/month)
- [ ] Clear differentiation from existing platforms identified
- [ ] No blocking patents discovered
- [ ] Novel claims articulated beyond "WebSocket + events"

**Defer/Abandon IF**:
- [ ] <50ms requires infrastructure beyond budget
- [ ] Existing platforms already do what we're claiming
- [ ] Blocking patents exist that require expensive design-around
- [ ] Innovation is in implementation, not patentable method

---

## Key Questions for Patent Claims

Based on research, we need to answer:

### Technical Novelty
1. **What's novel about QR-based device registration?** (vs app download, vs URL)
2. **What's novel about the orchestration logic?** (not the WebSocket transport)
3. **What's novel about audience segmentation?** (real-time vs pre-defined)
4. **What's novel about multi-modal delivery?** (vs existing adaptive streaming)

### Commercial Differentiation
1. **Why would NSA members pay for this?** (vs Slido, vs Mentimeter)
2. **What's the "10x better" story?** (faster setup? better engagement? lower cost?)
3. **What's the "patent pending" positioning?** (credibility signal to enterprise buyers)

### Risk Assessment
1. **Prior art in concert/stadium sync?** (Coldplay, Phish, stadium apps)
2. **Prior art in broadcast second-screen?** (TV sync patents)
3. **Prior art in audience response?** (iClicker, polling system patents)
4. **Freedom to operate?** (can we build without infringing?)

---

## Success Metrics for Research

### Research Quality
- [ ] Each S1-rapid produces clear recommendation
- [ ] Latency claims backed by benchmarks (not marketing)
- [ ] Prior art inventory with patent numbers
- [ ] Build vs buy decision with cost model

### Decision Confidence
- [ ] "File" or "Don't file" recommendation with rationale
- [ ] If file: refined claim language based on differentiation
- [ ] If don't file: what would change the decision?

### Time Budget
- [ ] Total research time: 8-10 hours
- [ ] Completed within 1 week
- [ ] Decision made before spending $2,500

---

## Connection to Patent Claims

From the provisional patent analysis (spawn-patents):

**Claim 1: QR-based rapid device registration (<50ms)**
- Research needed: 2.073 (WebSocket latency), 3.082 (prior art)
- Validation: Is <50ms the registration or the sync? Clarify claim.

**Claim 2: Real-time audience segmentation**
- Research needed: 3.081 (existing platforms), 3.080 (event management)
- Validation: What segmentation do existing tools offer?

**Claim 3: Synchronized content delivery**
- Research needed: 3.082 (device sync), 2.073 (WebSocket)
- Validation: Prior art in concert apps, broadcast sync

**Claim 4: Adaptive orchestration based on engagement**
- Research needed: 3.081 (engagement platforms)
- Validation: Do existing tools adapt in real-time?

---

## Next Steps

1. **Assign to spawn-solutions agent**: Add 2.073, 3.081, 3.082, 3.080 to priority queue
2. **Execute S1-rapid**: 8-10 hours over 1 week
3. **Synthesize findings**: Document in this file or new RESEARCH_SYNTHESIS.md
4. **Make filing decision**: Based on technical validation and prior art assessment
5. **If proceed**: Refine patent claims based on research insights

---

## Document History

| Date | Update |
|------|--------|
| 2025-12-02 | Initial creation - research priorities defined |

---

**Owner**: Ivan
**Related**: spawn-patents/analysis/qrcards/ (patent analysis framework)
**Decision Deadline**: Before spending $2,500 on provisional filing
