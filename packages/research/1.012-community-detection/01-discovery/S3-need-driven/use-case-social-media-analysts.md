# Use Case: Social Media Analysts

## Who Needs This

**Persona:** Maya, Social Media Intelligence Analyst at a PR agency

**Role:** Monitors brand mentions, identifies influencer networks, tracks viral spread

**Organization:** Mid-sized PR/marketing firm serving Fortune 500 clients

**Technical background:** Data analytics, comfortable with Python, not a CS researcher

**Team size:** 2-4 analysts, shared engineering support

## Why Community Detection Matters

### Problem 1: Influencer Network Identification

**Challenge:** Client wants to identify "influencer clusters" for product launch
- Twitter network: 500K users, 5M follower relationships
- Need to find tightly-connected groups (not just high-follower individuals)
- Groups share audiences, co-amplify messages

**Without community detection:**
- Manual browsing of top followers (misses coordinated groups)
- Simple follower-count ranking (misses mid-tier but connected users)
- Ad-hoc clustering (inconsistent, not reproducible)

**With community detection:**
- Automated discovery of 50-100 influencer clusters
- Identify "connector" nodes bridging multiple communities
- Prioritize outreach to cluster centers (highest ROI)

### Problem 2: Echo Chamber Detection

**Challenge:** Client wants to understand how polarized their audience is
- Retweet network: 1M users, 10M edges
- Need to quantify "how many distinct camps exist?"
- Measure cross-camp communication (bridge edges)

**Value:**
- Tailor messaging for each identified cluster
- Identify bridge users for cross-pollination campaigns
- Quantify polarization trend over time

### Problem 3: Bot Network Detection

**Challenge:** Identify coordinated inauthentic behavior
- Suspicious spike in brand mentions (50K accounts in 2 hours)
- Need to find if it's organic or coordinated botnet
- Botnet signature: densely connected, synchronized posting

**Detection pattern:**
- Community detection finds abnormally dense clusters
- Real communities: gradual growth, varied activity
- Botnets: sudden appearance, uniform behavior

## Requirements

### Graph Characteristics

- **Size:** 100K-5M nodes (Twitter mentions, followers)
- **Type:** Directed (followers, retweets, mentions)
- **Temporal:** Yes (networks evolve weekly)
- **Edge attributes:** Timestamps, interaction types

### Quality Needs

**Explainability:** CRITICAL
- Must explain to non-technical clients "why these users are grouped"
- Modularity more intuitive than information-theoretic measures

**Accuracy:** MEDIUM
- 80-90% precision acceptable
- Manual validation budget: 100-200 communities

**Speed:** HIGH
- Weekly reports (need results in <1 hour)
- Exploratory analysis (need results in <10 minutes)

### Constraints

**Technical:**
- Runs on analyst laptops (16GB RAM, no GPU)
- Python + NetworkX ecosystem preferred
- Must integrate with Gephi for visualization

**Organizational:**
- Budget: $0 (open-source only)
- Expertise: Analytics, not CS research
- Training time: <1 week to ramp up new analysts

## Success Criteria

**Good communities = clients understand them**
1. **Nameable:** Cluster has clear theme (e.g., "fitness influencers," "political commentators")
2. **Actionable:** Can design targeted campaign for cluster
3. **Stable:** Communities don't radically change week-to-week (unless real event)
4. **Visualizable:** Can show in Gephi to clients

**Bad communities = unusable**
- Single giant community (no insights)
- Hundreds of tiny clusters (too granular)
- Disconnected nodes in same community (confusing)

## Algorithm Selection for This Persona

**Best fit: Leiden**

**Why:**
- Fast enough for weekly analysis (1M nodes in <10 min)
- High modularity (easy to explain)
- Guaranteed connected communities (avoids confusing disconnects)
- Good Gephi integration via NetworkX

**Why NOT others:**
- ❌ Louvain: Disconnected communities confuse clients
- ❌ Label Propagation: Low quality, hard to explain to clients
- ❌ Infomap: Information theory harder to explain than modularity
- ❌ Spectral: Too slow, requires knowing K in advance

**Implementation path:**
1. NetworkX for graph construction (familiar to analysts)
2. CDlib Leiden for community detection
3. Export to Gephi for client-facing visualizations

## Real-World Example

**Case study:** PR firm identified 12 micro-influencer clusters for fitness brand launch

**Network:** 200K Twitter users, 800K follower edges

**Method:** Leiden community detection, resolution=1.5 (smaller communities preferred)

**Result:**
- Found 12 communities: yoga, crossfit, running, weightlifting, etc.
- Reached out to top 3 users per community (36 influencers total)
- Campaign ROI: 5x vs broadcast approach

**Why it worked:**
- Communities matched real-world sub-niches
- Influencers within communities had shared audiences (co-amplification)
- Algorithm was fast enough to iterate weekly during campaign
