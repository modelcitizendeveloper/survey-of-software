# Use Case: Cybersecurity Teams

## Who Needs This

**Persona:** Alex, Threat Intelligence Analyst at financial services company

**Role:** Detects and analyzes cyber threats, tracks threat actor groups

**Organization:** Fortune 500 bank, Security Operations Center (SOC)

**Technical background:** Cybersecurity certifications, scripting ability, graph databases

**Team size:** 5-person threat intel team within 50-person SOC

## Why Community Detection Matters

### Problem 1: Botnet Detection

**Challenge:** Identify coordinated bot campaigns from network traffic
- Network graph: 100K IPs, 1M connections (internal + external)
- Botnet signature: synchronized C2 (command & control) communication
- Goal: Find infected machines before data exfiltration

**Attack pattern:**
- Infected machines connect to same C2 servers
- Synchronized behavior (all connect within 5-minute windows)
- Forms dense cluster in communication graph

**Without community detection:**
- Signature-based detection (misses zero-days)
- Manual investigation of alerts (slow, doesn't scale)
- Threshold-based rules (high false positives)

**With community detection:**
- Automated detection of anomalously dense clusters
- Typical departments: moderate density, organic growth
- Botnets: sudden appearance, ultra-high density

**Value:**
- Early detection (days before data loss)
- Scope identification (which machines infected?)
- C2 infrastructure mapping (block at firewall)

### Problem 2: Threat Actor Attribution

**Challenge:** Group malware samples by threat actor
- Malware similarity graph: 50K samples, 200K similarity edges
- Edges: code reuse, C2 overlap, behavioral patterns
- Goal: Attribute attacks to APT groups (China, Russia, Iran)

**Why it matters:**
- Different actors have different goals (espionage vs ransomware)
- Attribution informs response (legal, diplomatic, technical)
- Track actor evolution over time (new tools, new targets)

**Community detection use:**
- Each community = toolkit of one threat actor
- Novel sample → assign to community → attribute to actor
- Detect splits (actor fragmentation, new groups)

### Problem 3: Insider Threat Networks

**Challenge:** Identify collusion among employees
- Employee interaction graph: 10K employees, 50K interactions
- Interactions: email, file shares, physical proximity (badge scans)
- Insider risk: coordinated data theft by 2-5 person team

**Detection pattern:**
- Normal teams: moderate interaction, aligned with org chart
- Insider threat: sudden increase in cross-department interaction
- Pre-theft planning: tight cluster forms weeks before incident

**Value:**
- Early intervention (before theft occurs)
- Scope assessment (how many involved?)
- Evidence for investigation (who talked to whom?)

## Requirements

### Graph Characteristics

- **Size:** 10K-1M nodes (IPs, malware hashes, employees)
- **Type:** Directed (network flows, attack chains)
- **Temporal:** CRITICAL (threats evolve hourly)
- **Edge attributes:** Timestamps, volumes, protocols

### Quality Needs

**Speed:** CRITICAL
- Real-time threat detection (detect within minutes)
- Daily threat intel reports (run overnight)
- Incident response (results in <10 min during active breach)

**Precision:** HIGH
- False positives waste analyst time (limited resource)
- False negatives = missed breaches (catastrophic)
- Target: >90% precision, >70% recall

**Explainability:** HIGH
- Must explain to executives "why we think this is botnet X"
- Regulatory compliance (document detection method)
- Legal evidence (may go to court)

### Constraints

**Technical:**
- Stream processing (new data every second)
- Integration with SIEM (Splunk, QRadar)
- Graph database (Neo4j, JanusGraph)

**Operational:**
- 24/7 operation (can't have "batch window")
- Budget: enterprise licenses OK ($100K+)
- Expertise: security analysts, not data scientists

**Regulatory:**
- GDPR, SOX compliance (data privacy)
- Audit trail (explain every alert)
- Reproducibility (same data = same result for court)

## Success Criteria

**Good detection = actionable and defensible**
1. **Actionable:** Clear next step (block IPs, quarantine machines)
2. **Timely:** Detected before damage done
3. **Explainable:** Can show to auditor/judge "here's why we blocked this"
4. **Scalable:** Works at network speed (1M events/second)

**Bad detection = wasted effort**
- Alert fatigue (100s of false positives)
- Too slow (detected after breach)
- Unexplainable (can't defend to legal team)

## Algorithm Selection for This Persona

**Best fit: Label Propagation or Leiden (depending on use case)**

**For real-time botnet detection: Label Propagation**

**Why:**
- Extreme speed (1M nodes in minutes)
- Online/streaming variants exist
- Good enough quality for initial triage

**Why NOT perfect:**
- Lower precision (more false positives)
- Non-deterministic (hard to reproduce for audits)

**Workflow:**
- Label Propagation for initial detection
- Leiden refinement for high-confidence alerts
- Manual validation for incident response

**For threat actor attribution: Leiden**

**Why:**
- High quality (precision critical for attribution)
- Reproducible with seed (legal requirement)
- Well-connected communities (malware variants must share code)

**For insider threat: Leiden**

**Why:**
- Temporal analysis (re-run daily, track community evolution)
- Explainable (modularity easier to explain to non-technical executives)
- Hierarchical (teams within departments)

**Why NOT others:**
- ❌ Louvain: Disconnected communities (confuses investigation)
- ❌ Spectral: Too slow for real-time, requires knowing K
- ❌ Infomap: Information theory hard to explain in court

## Real-World Example

**Case study:** Detecting Mirai botnet infection at financial institution

**Network:** 200K devices (employees + IoT), 5M daily connections

**Method:** Label Propagation for initial scan, Leiden for confirmation

**Timeline:**
- **Day 0 (infection):** 500 IoT cameras infected (building security)
- **Day 1 (detection):** Label Propagation flags 480/500 as anomalous cluster
  - Normal departments: density ~0.3
  - Infected cluster: density ~0.9 (all talking to same C2)
- **Day 1 (confirmation):** Leiden confirms community structure
- **Day 1 (response):** 500 devices quarantined, C2 IPs blocked

**Result:**
- Zero data exfiltration (detected before attack phase)
- $2M potential loss avoided (DDoS ransom + downtime)
- Legal compliance (documented detection method for regulators)

**Why it worked:**
- Speed: Label Propagation fast enough for daily scan
- Quality: Leiden confirmation reduced false positives (manual validation required)
- Explainability: Modularity metric clear to executives ("this cluster is 3x denser than normal")

## Domain-Specific Considerations

### Adversarial Evasion

**Problem:** Attackers know defenders use community detection

**Evasion tactics:**
- Low-and-slow attacks (reduce cluster density)
- Distributed C2 (avoid central hub)
- Mimicry (match benign traffic patterns)

**Mitigation:**
- Multi-method detection (combine with anomaly detection)
- Temporal analysis (cluster evolution over time)
- Behavioral features (not just connectivity)

### Stream Processing

**Requirement:** Detect threats in near-real-time (minutes, not hours)

**Challenge:** Community detection typically batch-oriented

**Solutions:**
- Incremental algorithms (update partition as new edges arrive)
- Sliding window (detect on last 1 hour of data)
- Approximate methods (Label Propagation, fast but imperfect)

**Trade-off:** Speed vs quality (accept lower precision for speed)

### Ground Truth Scarcity

**Problem:** Unknown how many real threats in network

**Impact:** Can't measure recall (missed detections)

**Validation:**
- Red team exercises (simulate attacks, measure detection rate)
- Retrospective analysis (did we detect known-bad IPs?)
- Peer comparison (industry benchmarks)

## Integration with Security Stack

**Typical architecture:**
1. **Data collection:** SIEM, NetFlow, packet capture
2. **Graph construction:** Stream processing (Kafka, Flink)
3. **Community detection:** Batch (overnight) or streaming (Label Prop)
4. **Alerting:** SIEM integration (create ticket)
5. **Response:** Analyst investigation → block/quarantine

**Required integrations:**
- Neo4j (graph database)
- Splunk/QRadar (SIEM)
- Kafka (streaming)
- Python/Scala (scripting)

**Performance target:**
- Graph construction: <1 min latency
- Community detection: <10 min for daily batch, <1 min for streaming
- End-to-end: Alert within 15 minutes of anomaly

## Regulatory and Legal Considerations

**GDPR compliance:**
- Employee monitoring (insider threat) requires consent
- Data minimization (only store what's needed)
- Retention limits (delete old graphs)

**Legal evidence:**
- Reproducibility (same input = same output)
- Audit trail (document algorithm parameters)
- Expert testimony (analyst can explain method in court)

**Standards compliance:**
- NIST Cybersecurity Framework
- ISO 27001
- SOX (financial controls)

**Documentation requirements:**
- Algorithm selection rationale
- Parameter tuning justification
- Validation methodology
- False positive rate estimation
