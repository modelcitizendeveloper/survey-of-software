# Turbopack - S1 Rapid Assessment

## Popularity Metrics (2024)

### npm Downloads
- **Not available standalone** (integrated into Next.js)
- Next.js downloads: millions, but Turbopack opt-in
- Cannot measure independent adoption

### GitHub Stars
- **Vercel/next.js repo**: ~127K stars (includes Next.js)
- Turbopack code now in Next.js monorepo
- No standalone repository star count

### Framework Adoption
- **Only for Next.js** (exclusive integration)
- Stable as of October 2024
- Default bundler in Next.js 15
- Zero adoption outside Next.js ecosystem

### Community
- Next.js community (large)
- Turbopack-specific discussion limited
- Corporate backing: Vercel

## Quick Assessment

### Does It Work? YES (for Next.js only)
- Install: Use Next.js 15 (automatic)
- First bundle: Very fast (claimed 45.8% faster than Webpack)
- Documentation: Part of Next.js docs
- Learning curve: N/A (transparent to users)

### Performance
- **Dev server cold start**: Fast (Next.js with Turbopack)
- **HMR**: Very fast (claimed improvements)
- **Production build**: Still uses Webpack (Turbopack not prod-ready)
- **Bundle size**: N/A (Next.js handles it)

### Key Features
1. Rust-based (high performance)
2. Incremental computation (only rebuild changed code)
3. Next.js integration (first-class)
4. Fast dev experience
5. Still beta for production builds

## Strengths (S1 Lens)

### Performance Claims
- 45.8% faster than Webpack for vercel.com
- Rust-based (compiled, efficient)
- Incremental computation
- Built by Webpack creator (Tobias Koppers)

### Next.js Integration
- Default in Next.js 15
- Transparent (just works)
- Optimized for React Server Components
- Growing with Next.js adoption

### Technical Innovation
- Modern architecture
- Incremental compilation
- Rust performance
- Webpack successor vision

## Weaknesses (S1 Lens)

### Next.js Only
- Cannot use outside Next.js
- No general-purpose bundler
- No framework choice
- Locked to Vercel ecosystem

### Not Production Ready
- Dev mode stable (Oct 2024)
- Production builds still use Webpack
- Limited maturity
- Unproven at scale

### No Independent Adoption
- Zero popularity outside Next.js
- No download metrics
- No community outside Next.js
- Can't evaluate independently

### Limited Track Record
- Recently stable (2024)
- No battle-testing
- Unknown edge cases
- Unproven reliability

## S1 Popularity Score: N/A (Not Applicable)

**Rationale**:
Cannot assess popularity independently. If you use Next.js, you get Turbopack. If you don't, you can't use it. Not a general-purpose build tool, so S1 methodology doesn't apply cleanly.

## S1 "Just Works" Score: 8/10 (for Next.js)

**Rationale**:
- Works transparently in Next.js
- No configuration needed
- Fast experience
- **But**: Only Next.js, not production-ready

## S1 Recommendation

**Use Turbopack if you**:
- Already using Next.js 15+
- Want faster Next.js dev experience
- Trust Vercel's roadmap
- Willing to use beta tech

**Skip if**:
- Not using Next.js (can't use it)
- Need production builds (still Webpack)
- Want proven, stable tooling
- Need framework flexibility

## S1 Confidence: LOW (as general tool)

Turbopack is not a general-purpose build tool yet. It's a Next.js bundler in dev mode. The S1 methodology (crowd wisdom) can't evaluate it because:
1. No independent adoption data
2. Locked to single framework
3. Not production-ready
4. Too new for crowd validation

## S1 Position in Ecosystem

**Not a Vite/Webpack alternative**: Turbopack is Next.js-specific infrastructure
**Not separately adoptable**: Comes with Next.js or not at all
**Not comparable**: Different category (framework tool vs general bundler)

## S1 Verdict

**For Next.js users**: Use it (default, transparent, faster)
**For everyone else**: Irrelevant (can't use it)
**As general build tool**: Not applicable

The popularity data is clear: if you're building with Next.js, Turbopack is your bundler (no choice needed). If you're not using Next.js, evaluate Vite, Webpack, etc. instead.

## S1 Future Outlook

**IF** Turbopack becomes general-purpose (big if):
- Could compete with Vite
- Vercel backing is strong
- Rust performance is real
- Webpack creator involved

**Current reality**: Next.js only, wait for maturity

The S1 approach says: wait for crowd validation. Turbopack has potential but needs years of adoption data before S1 can confidently recommend it outside Next.js.
