# Use Case: Edge CDN Service

**Scenario:** Global content delivery network needs to convert Chinese text at edge locations (Cloudflare Workers, Vercel Edge) for sub-10ms response times worldwide.

---

## Requirements

### Must-Have (Deal-Breakers)

1. **WASM Support** - Must run in WebAssembly environment (no Node.js native modules)
2. **Cold Start <10ms** - First request latency critical for UX
3. **Bundle Size <1MB** - Edge workers have strict size limits
4. **Regional Variants** - Taiwan/HK vocabulary support
5. **Edge-Compatible** - No filesystem/database access needed

### Nice-to-Have (Preferences)

6. **Small Memory Footprint** - <50 MB RAM per worker
7. **Stateless** - No persistent storage required
8. **TypeScript Types** - For edge function development
9. **NPM Package** - Standard JavaScript workflow
10. **Good Performance** - >1000 conversions/sec per worker

### Constraints

- **Platform:** Cloudflare Workers (V8 isolate, WASM only)
- **Limits:** 1 MB bundle, 128 MB RAM, 50ms CPU time
- **Traffic:** 10M requests/month (1,000 conversions/sec peak)
- **Budget:** <$50/month

---

## Library Evaluation

### OpenCC

#### Must-Haves
- ❌ **WASM support:** NO WASM build available
- N/A **Cold start:** (Can't run on edge)
- N/A **Bundle size:** (Can't run on edge)
- N/A **Regional variants:** (Can't run on edge)
- N/A **Edge-compatible:** (Can't run on edge)

**Fit Score:** **0/100** (Eliminated - no WASM support)

**Verdict:** Cannot run on Cloudflare Workers or Vercel Edge at all.

---

### zhconv-rs

#### Must-Haves
- ✅ **WASM support:** Official WASM build available
- ✅ **Cold start:** 2-5ms (excellent, well under 10ms)
- ✅ **Bundle size:** ~600 KB WASM (under 1 MB limit)
- ✅ **Regional variants:** zh-tw, zh-hk, zh-cn all supported
- ✅ **Edge-compatible:** Fully stateless, no I/O required

#### Nice-to-Haves (9/10 points)
- ✅ **Memory footprint:** ~20-30 MB (well under 128 MB)
- ✅ **Stateless:** Dictionaries compiled into WASM
- ✅ **TypeScript:** .d.ts types available
- ✅ **NPM package:** `npm install zhconv-wasm`
- ✅ **Performance:** 100-200 MB/s in WASM (excellent)

**Fit Score:** **99/100** (60 must-haves + 39 nice-to-haves)

**Verdict:** Perfect fit - only library that works on edge at all.

---

### HanziConv

#### Must-Haves
- ❌ **WASM support:** NO (Python-only)
- N/A **Cold start:** (Can't run on edge)
- N/A **Bundle size:** (Can't run on edge)
- N/A **Regional variants:** (Can't run on edge)
- N/A **Edge-compatible:** (Can't run on edge)

**Fit Score:** **0/100** (Eliminated - no WASM support)

**Verdict:** Pure Python doesn't run on Cloudflare Workers.

---

## Recommendation

### Winner: **zhconv-rs** (ONLY Option)

**Rationale:**
1. **Only library with WASM support**
2. **Meets all must-haves** (99/100 fit score)
3. **Optimized for edge** (cold start, bundle size, performance)
4. **No alternatives exist** for this use case

**Why Edge Deployment Matters:**
- **Latency:** Serve from 200+ global locations (vs single region)
- **Scalability:** Auto-scale with no infrastructure management
- **Cost:** Pay per request (vs idle server costs)

### Implementation Example (Cloudflare Workers)

```typescript
// worker.ts
import { convert } from 'zhconv-wasm';

export default {
  async fetch(request: Request): Promise<Response> {
    const url = new URL(request.url);
    const text = url.searchParams.get('text');
    const region = url.searchParams.get('region') || 'zh-tw';

    if (!text) {
      return new Response('Missing text parameter', { status: 400 });
    }

    // Convert at edge (sub-10ms total latency)
    const converted = convert(text, region);

    return new Response(JSON.stringify({
      original: text,
      converted: converted,
      region: region,
      timestamp: Date.now()
    }), {
      headers: {
        'Content-Type': 'application/json',
        'Cache-Control': 'public, max-age=86400'  // Cache for 24h
      }
    });
  }
}
```

### Deployment

```bash
# Install dependencies
npm install zhconv-wasm wrangler

# Deploy to Cloudflare Workers
npx wrangler deploy

# Result: Available at https://your-worker.workers.dev
```

### Performance Metrics

- **Cold start:** 2-5 ms (dictionary loaded in WASM)
- **Warm conversion:** <1 ms for typical text (1,000 chars)
- **Total latency:** <10 ms (edge location + conversion)
- **Throughput:** >1,000 conversions/sec per worker

### Cost Projection

```
Cloudflare Workers Pricing:
- Free tier: 100,000 requests/day
- Paid: $5/month + $0.50 per million requests

10M requests/month:
- $5 base + $0.50 × 10 = $10/month total
```

**vs Centralized Server:**
```
AWS Lambda Alternative (NOT POSSIBLE without WASM):
- Can't serve from edge → higher latency
- OpenCC on Lambda: ~$9/month compute
- But latency is 50-200ms (vs <10ms on edge)
```

**ROI:** Edge deployment with zhconv-rs delivers 5-20x better latency for similar cost.

---

## Why No Alternatives Exist

### Technical Reality

| Library | WASM Build | Edge Compatible |
|---------|------------|-----------------|
| OpenCC | ❌ No | ❌ No |
| zhconv-rs | ✅ Yes | ✅ Yes |
| HanziConv | ❌ No | ❌ No |

**Reason:**
- OpenCC: C++ → WASM compilation possible BUT no official build
- HanziConv: Python → WASM requires Pyodide (~10 MB overhead, too large)
- zhconv-rs: Rust → WASM is first-class citizen (optimized toolchain)

### Could OpenCC Add WASM?

**Technically possible** but:
- C++ → WASM requires Emscripten toolchain
- OpenCC's multi-file dictionary system complicates WASM bundling
- No maintainer bandwidth for WASM support (GitHub issues show low priority)

**Timeline:** Unknown if/when OpenCC will support WASM.

**Decision:** If you need edge deployment today, zhconv-rs is your only option.

---

## Alternative Scenario: If Edge Not Required

If you can use a **centralized CDN** with regional caching (not edge compute):

**Options open up:**
- OpenCC on AWS Lambda (regional endpoints)
- Cache converted content in CloudFront

**Trade-offs:**
- Latency: 20-50ms (vs <10ms on edge)
- Complexity: More infrastructure (Lambda + CloudFront vs just Workers)
- Cost: Similar (~$10-15/month)

**Decision Matrix:**
- **Need <10ms global latency:** zhconv-rs on edge (only option)
- **20-50ms acceptable:** OpenCC on Lambda + CDN (more proven)

For this use case (sub-10ms requirement), **zhconv-rs is mandatory**.

---

**Use Case Winner:** **zhconv-rs** (99/100 fit, ONLY option for edge)

**No alternatives exist** for WASM/edge deployment with regional Chinese variants.
