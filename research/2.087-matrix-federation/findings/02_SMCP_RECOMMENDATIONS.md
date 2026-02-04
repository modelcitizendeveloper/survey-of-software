# SMCP Federation Recommendations

Recommendations for Swimsuit Issue 6: Federation between SMCP instances.

## Executive Summary

Matrix provides a rich federation model, but SMCP's needs are simpler. Focus on Linearized
Matrix patterns (hub-spoke) rather than full DAG replication. Adopt server discovery,
skip complex state resolution, simplify identity to service accounts.

## Pattern Recommendations

### ADOPT: Server Discovery via Well-Known

**Matrix pattern**: `.well-known/matrix/server` with delegation

**SMCP implementation**:
```
GET https://example.com/.well-known/smcp/server
{
  "endpoint": "https://smcp.example.com:443",
  "version": "1.0",
  "components": ["paulina", "naomi", "roshumba"],
  "public_key": "ed25519:abc123..."
}
```

**Why adopt**:
- Standard HTTP, no DNS complexity
- Self-documenting capability advertisement
- Paulina (registry) already tracks local capabilities; extend to remote

**Implementation effort**: Low (HTTP endpoint + JSON schema)

### ADOPT: Request Signing

**Matrix pattern**: Ed25519 signatures in X-Matrix header

**SMCP implementation**:
```
X-SMCP-Authorization: origin=smcp.alice.com destination=smcp.bob.com
  key_id=ed25519:abc123 sig=base64...
```

**Why adopt**:
- Prevents request spoofing
- Enables multi-hop routing (through intermediate SMCP instances)
- Already have cryptographic primitives in Python ecosystem

**Simplification**: Single signing key per instance (no key rotation initially)

**Implementation effort**: Medium (signing/verification library)

### ADOPT: Linearized Event Model

**Matrix pattern**: MSC3995 hub-spoke with doubly-linked list

**SMCP implementation**:
```yaml
# Naomi event (cross-instance)
event:
  id: evt_abc123
  origin: smcp.alice.com
  prev_event: evt_xyz789
  type: naomi:task.completed
  room: !kitchen:smcp.alice.com  # shared channel
  timestamp: 2025-01-08T12:00:00Z
  data:
    task_id: 236364
    title: "Make bread"
```

**Why adopt**:
- Simpler than full DAG
- Natural fit for Naomi event bus
- One hub per channel avoids complex state resolution

**Key design decisions**:
- Naomi becomes "hub" for channels it creates
- Remote Naomi instances are "participants"
- Hub assigns `prev_event` to maintain ordering

**Implementation effort**: Medium (extend Naomi protocol)

### ADOPT: Channel-Based Sharing

**Matrix pattern**: Rooms as shared state containers

**SMCP implementation**:
- Create "channels" in Naomi for cross-instance coordination
- Channel ID: `!name:origin.server.com`
- Membership explicit (like Matrix `m.room.member`)

**Use cases**:
1. **Shared project channel**: Multiple SMCP instances collaborate on Vikunja tasks
2. **Notification fanout**: Events published to channel, all participants receive
3. **Workflow handoff**: Judith workflows span instances

**Why adopt**:
- Clean isolation (channels are independent)
- Explicit membership (audit trail)
- Familiar model from Matrix/Slack

**Implementation effort**: Medium-High (Naomi protocol extension)

### SKIP: Full DAG Replication

**Matrix pattern**: Complete event DAG with state resolution

**Why skip**:
- Complexity vastly exceeds SMCP needs
- State resolution algorithm is bug-prone
- Requires significant CPU for large channels
- Linearized model sufficient for orchestration

**Alternative**: If network partitions occur, hub reconciles on reconnection

### SKIP: E2EE (Olm/Megolm)

**Matrix pattern**: Double ratchet + group ratchet encryption

**Why skip for now**:
- SMCP instances are infrastructure, not end-users
- Inter-service communication can use TLS + signed requests
- E2EE adds key management complexity

**When to reconsider**:
- Multi-tenant SMCP with untrusted instances
- Sensitive artifact sharing (credentials, PII)
- Regulatory requirements

**Simpler alternative**: TLS mutual authentication + HMAC message signing

### SIMPLIFY: Identity Model

**Matrix pattern**: @user:server with cross-signing, multiple devices

**SMCP simplification**:
```
smcp://instance-name/component
Examples:
  smcp://alice.example/naomi      # Alice's event bus
  smcp://alice.example/paulina    # Alice's registry
  smcp://bob.example/vikunja      # Bob's Vikunja MCP
```

**Why simplify**:
- SMCP instances are services, not multi-device users
- One identity per instance (or component)
- No device tracking needed

**Trust model**:
- Instance public key = instance identity
- Trust instance = trust all its components
- Roshumba routes cross-instance calls via Paulina's remote registry

### SIMPLIFY: Membership Management

**Matrix pattern**: Power levels 0-100, complex ACLs per event type

**SMCP simplification**:
- Binary membership: member or not
- Channel creator has admin rights
- Admin can add/remove members
- All members can publish events

**Why simplify**:
- SMCP is infrastructure, not social platform
- Fine-grained ACLs add configuration burden
- Start simple, add complexity when needed

## Architecture Recommendation

### Federated SMCP Components

```
                    ┌────────────────────────────────┐
                    │    SMCP Federation Protocol    │
                    │  (Linearized event streaming)  │
                    └───────┬───────────────┬────────┘
                            │               │
        ┌───────────────────┴───┐       ┌───┴───────────────────┐
        │   smcp.alice.com      │       │   smcp.bob.com        │
        │                       │       │                       │
        │ Paulina ◄─────────────┼───────┼───► Paulina           │
        │ (remote registry)     │       │    (remote registry)  │
        │                       │       │                       │
        │ Naomi ◄───────────────┼───────┼───► Naomi             │
        │ (federated channels)  │       │    (federated channels)│
        │                       │       │                       │
        │ Roshumba ─────────────┼───────┼───► Roshumba          │
        │ (cross-instance calls)│       │    (cross-instance calls)│
        └───────────────────────┘       └───────────────────────┘
```

### Federation Capabilities by Component

| Component | Federation Role | Priority |
|-----------|-----------------|----------|
| **Paulina** | Remote registry discovery | P0 |
| **Naomi** | Cross-instance event channels | P0 |
| **Roshumba** | Route calls to remote servers | P1 |
| **Gail** | Optional log aggregation | P2 |
| **Judith** | Cross-instance workflows | P2 |
| **Kathy** | Config sync (selective) | P3 |
| **Vendela** | Remote health monitoring | P3 |

### Implementation Phases

**Phase 1: Discovery & Identity** (Swimsuit Issue 6a)
- `.well-known/smcp/server` endpoint
- Instance signing keys
- Paulina tracks remote instances
- Basic health ping across instances

**Phase 2: Event Federation** (Swimsuit Issue 6b)
- Naomi federated channels
- Linearized event protocol
- Subscribe to remote channels
- Publish to channels with remote members

**Phase 3: Remote Calls** (Swimsuit Issue 6c)
- Roshumba cross-instance routing
- Remote capability discovery via Paulina
- Signed request forwarding
- Response correlation

**Phase 4: Workflows & Aggregation** (Swimsuit Issue 6d)
- Judith workflows spanning instances
- Gail log aggregation (optional)
- Kathy config sharing (selective)

## Protocol Sketch

### Federation Handshake

```
Alice -> Bob: GET /.well-known/smcp/server
Bob -> Alice: {endpoint, version, components, public_key}

Alice -> Bob: POST /federation/v1/invite
              {channel: "!project:alice.com", inviter: "alice.com", invitee: "bob.com"}
              X-SMCP-Authorization: origin=alice.com ...

Bob -> Alice: {accepted: true, events_since: null}
```

### Event Publication

```
Alice -> Bob: PUT /federation/v1/send/{txn_id}
{
  "origin": "alice.com",
  "origin_server_ts": 1736352000000,
  "events": [
    {
      "id": "evt_abc",
      "type": "naomi:task.completed",
      "channel": "!project:alice.com",
      "prev_event": "evt_xyz",
      "data": {...}
    }
  ]
}

Bob -> Alice: {"processed": ["evt_abc"]}
```

### Remote Tool Call

```
Alice -> Bob: POST /federation/v1/call
{
  "call_id": "call_123",
  "target": "bob.com/vikunja",
  "tool": "list_tasks",
  "params": {"project_id": 14891}
}
X-SMCP-Authorization: origin=alice.com ...

Bob -> Alice: {
  "call_id": "call_123",
  "result": {...}
}
```

## Risks & Mitigations

### Risk: Network Partitions

**Impact**: Events may be delivered out of order or lost
**Mitigation**:
- Linearized model with single hub per channel
- Hub queues events for offline participants
- Participants request backfill on reconnection

### Risk: Rogue Instance

**Impact**: Malicious events, spam, resource exhaustion
**Mitigation**:
- Explicit channel membership (invite-only)
- Rate limiting per origin
- Signature verification on all requests
- Admin can remove instances from channels

### Risk: Complexity Creep

**Impact**: Federation becomes as complex as full Matrix
**Mitigation**:
- Strict scope: only patterns listed as ADOPT
- No DAG, no E2EE, simplified identity
- Each phase must be useful standalone
- Document what we're NOT building

## Success Criteria

Swimsuit Issue 6 complete when:
- [ ] Two SMCP instances discover each other via well-known
- [ ] Naomi channel spans both instances
- [ ] Event published on Alice appears on Bob
- [ ] Roshumba routes tool call from Alice to Bob's Vikunja
- [ ] Round-trip latency < 500ms for direct calls

## Non-Goals

Explicitly NOT in scope for Swimsuit Issue 6:
- End-to-end encryption
- Multi-device identity
- Complex access control (power levels)
- Full DAG state resolution
- Bridging to Matrix protocol
- Anonymous/ephemeral participation

---

## Sources

- [Matrix Server-Server API](https://spec.matrix.org/latest/server-server-api/)
- [MSC3995: Linearized Matrix](https://github.com/matrix-org/matrix-spec-proposals/pull/3995)
- [SMCP Specification](file:///home/ivanadamin/gt/solutions/crew/ivan/development/projects/smcp/smcp-spec.md)
- [Factumerit Matrix Issues](file:///home/ivanadamin/gt/factumerit/.beads/issues.jsonl) (context: existing Matrix bot)
