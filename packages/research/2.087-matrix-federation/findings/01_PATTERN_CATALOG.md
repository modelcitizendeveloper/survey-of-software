# Matrix Federation Pattern Catalog

Research for SMCP Swimsuit Issue 6: Federation between SMCP instances.

## 1. Federation Protocol Patterns

### 1.1 Server Discovery

Matrix uses a cascading discovery mechanism:

1. **`.well-known` delegation** (preferred): `https://<server_name>/.well-known/matrix/server`
   returns JSON with `m.server` key pointing to actual federation endpoint
2. **DNS SRV records**: `_matrix-fed._tcp.<hostname>` with priority/weight/port
3. **Fallback**: DNS A/AAAA records on port 8448

**SMCP mapping**: SMCP instances could publish `/.well-known/smcp/server` with:
```json
{
  "m.server": "smcp.example.com:443",
  "capabilities": ["naomi", "paulina", "roshumba"],
  "protocol_version": "1.0"
}
```

### 1.2 Request Authentication

Matrix authenticates all federation requests via Ed25519 signatures:

1. Server publishes signing keys at `/_matrix/key/v2/server`
2. Requests include `X-Matrix` Authorization header with:
   - origin server name
   - destination server name
   - request method, URI, content hash
   - Ed25519 signature

**Key rotation**: `verify_keys` (current) and `old_verify_keys` (deprecated but valid for
historical verification)

**Notary servers**: Third-party key verification avoiding single trust root (Perspectives model)

### 1.3 Transaction Model

Federation uses batched transactions:
- **PDUs** (Persistent Data Units): Room events, permanently stored, max 50 per transaction
- **EDUs** (Ephemeral Data Units): Typing indicators, presence, max 100 per transaction

Transaction format:
```json
{
  "origin": "sender.example.com",
  "origin_server_ts": 1234567890,
  "pdus": [...],
  "edus": [...]
}
```

**Delivery semantics**: At-least-once with idempotent event IDs

## 2. Room Model Patterns

### 2.1 Room Structure

- **Room ID**: Opaque identifier (e.g., `!abc123:server.example`)
- **Room aliases**: Human-readable (e.g., `#general:server.example`), can change over time
- **No single owner**: Rooms are replicated across all participating servers
- **Membership**: Explicit join/leave with power levels (0-100)

### 2.2 State vs Timeline Events

**State events** (persistent room configuration):
- `m.room.create`: Room creation, immutable
- `m.room.member`: Membership changes
- `m.room.power_levels`: Permission structure
- `m.room.name`, `m.room.topic`: Metadata

**Timeline events** (messages):
- `m.room.message`: Text, images, files
- Custom event types

**State resolution**: When state diverges (network partition), deterministic algorithm picks winner

### 2.3 Remote Join Handshake

When joining a room on a remote server:
1. Query directory server for room alias -> room ID + join candidates
2. Request room state from resident server
3. Construct and send `m.room.member` join event
4. Receive full room state

## 3. Event Graph (DAG) Patterns

### 3.1 DAG Structure

Events form a directed acyclic graph:
- Each event references 0+ parent events via `prev_events`
- Each event references authorization chain via `auth_events`
- Partial ordering gives chronological order within room

### 3.2 Event Authorization

6-stage validation for received events:
1. Format compliance
2. Signature verification
3. Hash integrity
4. Authorization against referenced auth events
5. Authorization against prior room state
6. "Soft failure" check against current state

**Rejected events**: Excluded from relay but may remain in DAG
**Soft-failed events**: Bypass client notification but participate in state resolution

### 3.3 State Resolution v2

When DAG branches merge:
1. Separate conflicted vs unconflicted state
2. Order power events by reverse topological power ordering
3. Apply iterative auth checks to power events
4. Order remaining events by mainline ordering
5. Apply iterative auth checks
6. Replace with unconflicted state where applicable

**Key insight**: Higher power levels take precedence; earlier events processed before later

### 3.4 Backfilling

- `/_matrix/federation/v1/backfill`: Retrieve historical events
- `/_matrix/federation/v1/get_missing_events`: Fill DAG gaps
- `/_matrix/federation/v1/state`: Snapshot at specific event

## 4. Identity Model Patterns

### 4.1 User Identifiers

Format: `@localpart:server.example.com`
- Localpart: User-chosen identifier
- Server: Authoritative homeserver for this user

**No global namespace**: Each server manages its own users

### 4.2 Cross-Signing Keys

Three key pairs per user:
1. **Master key**: User identity, signs other keys
2. **Self-signing key**: Signs user's own devices
3. **User-signing key**: Signs other users' master keys

**Trust chain**: Verify master key once, trust all their devices

### 4.3 Device Verification

- Device keys: Ed25519 (signing) + Curve25519 (encryption)
- Uploaded to homeserver
- Interactive verification: Emoji comparison, QR codes
- Once cross-signing established, only verify identity not individual devices

## 5. E2EE Patterns

### 5.1 Olm (1:1 Sessions)

Based on Signal's Double Ratchet:
- Bi-directional encrypted channel between two devices
- Perfect forward secrecy via ratchet
- One session per device pair

**Use case**: Bootstrapping Megolm sessions, direct messages

### 5.2 Megolm (Group Sessions)

Optimized for many recipients:
- Each sender creates outbound session for the room
- Single message encrypted once, all recipients decrypt
- Ratchet advances every message (forward secrecy)
- Session key shared via Olm to each recipient

**Session lifecycle**:
- Created on first message to room
- Rotated on membership change or after N messages (default 100)
- Recipients store session keys for decryption

### 5.3 Key Sharing

- New devices request historical keys from other devices
- Key backup to server (encrypted with recovery key)
- Session key forwarding (controlled sharing of old sessions)

### 5.4 Security Properties

**Forward secrecy**: Compromised key can't decrypt past messages (per-session)
**Partial backward secrecy**: Session rotation limits exposure window
**Deniability**: Message signatures use session keys, not identity keys

## 6. Linearized Matrix (MSC3995)

Simplified federation model for lightweight implementations:

### 6.1 Architecture

- **Hub server**: Central coordinator per room
- **Participant servers**: Lightweight, no DAG logic
- **DAG-capable servers**: Full Matrix homeservers, can join anytime

### 6.2 Key Simplifications

- Replace DAG with doubly-linked list
- Hub adds `prev_events`, `auth_events` for participants
- Deterministic ordering via `origin_server_ts` tiebreaker
- Participants generate "Linearized PDUs" without DAG fields

### 6.3 Compatibility

- DAG-capable servers extract linearized view for participants
- Room can transition between hub-only and DAG modes
- Starting point for new implementations (Room Version v11)

### 6.4 IETF/MIMI Connection

- Linearized Matrix proposed for MIMI working group
- Designed for MLS-centric environments
- Interoperability target for DMA-style messaging

## 7. Directory & Alias Resolution

### 7.1 Room Alias Lookup

1. Client requests `#room:server.example`
2. Query `/_matrix/federation/v1/query/directory?room_alias=...`
3. Receive room ID + list of participating servers
4. Select server for join handshake

### 7.2 Public Room Directory

- `/_matrix/federation/v1/publicRooms`: List public rooms
- Rooms opt-in to public listing
- Must have alias, be federated, explicitly marked public

## 8. Anti-Patterns & Lessons

### 8.1 Complexity of Full DAG

- State resolution algorithm is complex (v2 addresses v1 bugs)
- Every server must implement full algorithm
- CPU-intensive for large rooms with many forks

**Lesson**: Linearized Matrix exists precisely because full DAG is overkill for many use cases

### 8.2 E2EE Key Management

- Device proliferation creates key explosion (N users * M devices)
- Key verification UX is poor
- Key backup adds server trust requirements

**Lesson**: Start without E2EE, add when needed; consider simpler models for internal systems

### 8.3 Event Size Limits

- PDUs limited to 65535 bytes
- Media requires separate upload/download via content repository
- Large events split or referenced by ID

**Lesson**: Design events to be self-contained but bounded

### 8.4 Federation Failure Modes

- Network partitions cause DAG forks
- State resolution can produce surprising results
- Servers can go offline, causing delayed message delivery

**Lesson**: Design for eventual consistency, not strong consistency

---

## Sources

- [Matrix Specification Latest](https://spec.matrix.org/latest/)
- [Server-Server API v1.11](https://spec.matrix.org/v1.11/server-server-api/)
- [State Resolution v2 for the Hopelessly Unmathematical](https://matrix.org/docs/older/stateres-v2/)
- [Olm & Megolm Specification v1.17](https://spec.matrix.org/v1.17/olm-megolm/)
- [MSC3995: Linearized Matrix](https://github.com/matrix-org/matrix-spec-proposals/blob/travis/msc/linearized-matrix/proposals/3995-linearized-matrix.md)
- [Matrix.org Rooms & Events](https://matrix.org/docs/matrix-concepts/rooms_and_events/)
- [Cross-Signing Implementation Guide](https://matrix.org/docs/older/e2ee-cross-signing/)
- [Synapse Delegation Documentation](https://matrix-org.github.io/synapse/latest/delegate.html)
