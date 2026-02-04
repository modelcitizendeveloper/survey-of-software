# WebSocket Protocol (RFC 6455)

## Standard Overview

**RFC**: IETF RFC 6455 (December 2011)
**Purpose**: Full-duplex communication over single TCP connection
**Port**: 80 (ws://) or 443 (wss:// - encrypted)

## Protocol Characteristics

### Connection Lifecycle
1. HTTP upgrade handshake (1 RTT overhead)
2. Persistent bidirectional channel
3. Frame-based message passing
4. Explicit close handshake

### Performance Baseline

**Handshake Overhead**:
- Initial connection: ~1 RTT for HTTP upgrade
- TLS handshake: +1-2 RTT for wss://
- Total connection establishment: 50-150ms depending on latency

**Message Latency** (after connection established):
- Minimum: 1 RTT (round-trip time)
- LAN: 1-5ms RTT
- Same region: 10-50ms RTT
- Cross-continent: 100-300ms RTT

**Frame Overhead**:
- Minimum 2 bytes per frame
- Masking: 4 additional bytes (client → server)
- Total overhead: 2-14 bytes depending on payload size

## Browser Support

**Universal Support**: All modern browsers since 2013
- Chrome 16+
- Firefox 11+
- Safari 6+
- Edge (all versions)
- Mobile: iOS Safari 6+, Android Chrome 4.4+

## Server Implementations

**Popular Libraries**:
- Node.js: `ws`, `socket.io`, `uWebSockets.js`
- Python: `websockets`, `aiohttp`, `tornado`
- Go: `gorilla/websocket`, `nhooyr.io/websocket`
- Java: `javax.websocket`, Spring WebSocket
- Rust: `tokio-tungstenite`, `actix-web`

## Limitations

**Not HTTP**:
- Cannot leverage HTTP caching
- Separate connection pooling
- Load balancer complexity (sticky sessions)

**Connection Overhead**:
- Each connection consumes server memory (8-64KB per connection)
- 10K connections = ~80-640MB RAM minimum

**No Built-in Features**:
- No presence detection
- No message history/replay
- No automatic reconnection
- No pub/sub routing (application layer)

## Real-World Latency Factors

**Network Type**:
- Wired LAN: 1-5ms
- WiFi (same building): 5-20ms
- 4G mobile: 30-100ms
- 5G mobile: 10-40ms

**Geographic Distance**:
- Same city: 5-20ms
- Same region: 20-50ms
- Cross-continent: 100-300ms
- Satellite: 500-700ms

**The Physics Constraint**: Speed of light = ~100ms per 10,000km
- New York ↔ London: ~70ms minimum
- San Francisco ↔ Tokyo: ~100ms minimum
- No technology can beat physics

## Conclusion

WebSocket provides the **foundation** for real-time communication:
- Minimum latency = 1 RTT (dictated by network, not protocol)
- Efficient framing (low overhead)
- Universal browser support

**For sub-50ms synchronization**: Requires low-latency network path + geographic proximity + efficient server implementation.
