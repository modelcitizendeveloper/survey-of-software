# Use Case 6: Hobbyist / Learning Project (Free Tier Priority)

## Scenario Profile

**Developer**: Student, hobbyist, or learning developer
**Project**: Personal project, portfolio site, learning app
**Budget**: $0/month (strict requirement)
**Traffic**: Low traffic, intermittent usage
**Priority**: Free forever, no credit card, sufficient for learning

## Requirements (Scoring Criteria)

1. **True Free Tier** (Weight: High)
   - $0/month, no credit card required
   - Not a trial (free indefinitely)
   - No surprise charges
   - Clear free tier limits

2. **Sufficient Resources** (Weight: High)
   - Enough for real learning projects
   - Can deploy actual apps, not just "hello world"
   - Database included (if needed)
   - Reasonable requests/month

3. **No Artificial Limitations** (Weight: Medium)
   - App doesn't sleep aggressively
   - Custom domains allowed (even if paid)
   - Can use for portfolio (not just learning)
   - Professional-looking URLs

4. **Learning-Friendly** (Weight: Medium)
   - Good documentation for beginners
   - Active community
   - Example projects
   - Easy to get help

5. **Upgrade Path** (Weight: Low)
   - Can upgrade to paid smoothly
   - Pricing is reasonable when ready
   - No forced migration
   - Features carry over

## Provider Scoring

| Provider | True Free | Resources | Limitations | Learning | Upgrade Path | **Total** |
|----------|-----------|-----------|-------------|----------|--------------|-----------|
| **Vercel** | 10 | 9 | 9 | 9 | 9 | **46/50** |
| Netlify | 10 | 9 | 9 | 9 | 8 | **45/50** |
| Railway | 8 | 8 | 7 | 8 | 9 | **40/50** |
| Render | 7 | 7 | 6 | 8 | 8 | **36/50** |
| Fly.io | 9 | 8 | 7 | 7 | 8 | **39/50** |
| PythonAnywhere | 8 | 6 | 5 | 7 | 7 | **33/50** |
| Cloudflare | 10 | 9 | 8 | 7 | 9 | **43/50** |

## Detailed Scoring Rationale

### Vercel: 46/50 (Winner)

**True Free Tier: 10/10**
- Completely free for personal projects
- No credit card required
- Free forever (not a trial)
- Very generous limits

**Sufficient Resources: 9/10**
- 100GB bandwidth/month
- Unlimited static sites
- 100k serverless function invocations
- 100 deployments/day
- More than enough for learning/portfolio

**No Artificial Limitations: 9/10**
- No app sleeping
- Custom domains on free tier
- Professional vercel.app URLs
- Can use for real projects/portfolio
- Only limitation: "Vercel" branding

**Learning-Friendly: 9/10**
- Excellent documentation
- Huge community (Next.js ecosystem)
- Many example projects
- Great for learning modern web dev

**Upgrade Path: 9/10**
- $20/month for unlimited
- Smooth upgrade, no migration
- All features carry over
- Very fair pricing

**Total: 46/50** - Best free tier for learning

### Netlify: 45/50 (Very Close Second)

**True Free Tier: 10/10**
- Free tier is permanent
- No credit card required
- Very generous
- 100GB bandwidth/month

**Sufficient Resources: 9/10**
- 300 build minutes/month
- 100GB bandwidth
- Unlimited sites
- 125k function invocations
- Excellent for learning

**No Artificial Limitations: 9/10**
- No sleeping
- Custom domains free
- netlify.app URLs are clean
- Can use for portfolio
- No major restrictions

**Learning-Friendly: 9/10**
- Great documentation
- JAMstack community
- Many tutorials
- Good for learning modern web architecture

**Upgrade Path: 8/10**
- $19/month for pro
- Fair pricing
- Smooth transition
- Similar to Vercel

**Total: 45/50** - Excellent alternative to Vercel

### Cloudflare (Pages + Workers): 43/50

**True Free Tier: 10/10**
- Completely free
- No credit card required
- Extremely generous limits
- Unlimited bandwidth (!)

**Sufficient Resources: 9/10**
- Unlimited bandwidth (unique!)
- 100k Worker requests/day
- 500 builds/month
- KV storage included
- Best free tier in terms of limits

**No Artificial Limitations: 8/10**
- No sleeping
- Custom domains free
- workers.dev and pages.dev URLs
- Can use for production
- Workers have some runtime limits

**Learning-Friendly: 7/10**
- Good documentation
- But steeper learning curve (Workers API)
- Smaller community than Vercel/Netlify
- More technical platform

**Upgrade Path: 9/10**
- $5/month for Workers
- Extremely cheap
- Best value paid tier
- Easy upgrade

**Total: 43/50** - Best value, slightly harder to learn

### Railway: 40/50

**True Free Tier: 8/10**
- $5 free credit/month
- Enough for small projects
- Credit card required (but not charged unless exceeded)
- De facto free for light usage

**Sufficient Resources: 8/10**
- $5 = ~500 hours/month of small service
- Enough for learning projects
- Database included
- Good for full-stack learning

**No Artificial Limitations: 7/10**
- No sleeping on free tier
- Custom domains (after adding card)
- railway.app URLs are okay
- Can use for real projects

**Learning-Friendly: 8/10**
- Beautiful dashboard
- Good docs
- Active Discord community
- Great for learning Docker/containers

**Upgrade Path: 9/10**
- Pay-per-resource model
- Smooth transition from free credit
- Fair pricing ($0.000463/GB-hour)
- No plan tiers, just usage

**Total: 40/50** - Best free tier for full-stack Docker apps

### Fly.io: 39/50

**True Free Tier: 9/10**
- Generous free tier (no credit card for basic usage)
- 3 shared-CPU VMs (256MB each)
- 3GB persistent storage
- 160GB outbound transfer
- Real free tier, not just credit

**Sufficient Resources: 8/10**
- 3 VMs enough for several projects
- Can run real apps
- Database possible (within limits)
- Good for learning

**No Artificial Limitations: 7/10**
- VMs can sleep (if no traffic)
- Custom domains free
- fly.dev URLs are fine
- Professional use allowed

**Learning-Friendly: 7/10**
- Excellent docs
- But Docker/containers required
- Steeper learning curve
- Good community

**Upgrade Path: 8/10**
- ~$2/month for minimal production
- Fair pay-per-resource model
- Smooth upgrade
- Good value

**Total: 39/50** - Great if you know Docker

### Render: 36/50

**True Free Tier: 7/10**
- Free tier available
- No credit card for free tier
- But limited to 750 hours/month
- Apps sleep after 15 min inactivity (major drawback)

**Sufficient Resources: 7/10**
- 750 hours/month (enough if you're careful)
- 512MB RAM
- Database free tier (90 day expiry - bad!)
- Okay for learning but limitations bite

**No Artificial Limitations: 6/10**
- Apps sleep after 15 min (annoying)
- Cold start is slow (30s+)
- Can't use for portfolio demos (sleeping issue)
- Free databases expire after 90 days (terrible)

**Learning-Friendly: 8/10**
- Good documentation
- Clear tutorials
- Active community
- Good for learning deploys

**Upgrade Path: 8/10**
- $7/month for always-on
- Fair pricing
- Easy upgrade
- No migration needed

**Total: 36/50** - Decent but sleeping and DB expiry hurt it

### PythonAnywhere: 33/50

**True Free Tier: 8/10**
- Free tier exists
- No credit card required
- Free forever
- But significant limitations

**Sufficient Resources: 6/10**
- 1 web app only
- 512MB storage
- No custom domains on free
- No HTTPS on free
- yourname.pythonanywhere.com URL
- Very limited but works for learning

**No Artificial Limitations: 5/10**
- No custom domains on free (big limitation)
- No HTTPS on free tier (unprofessional)
- Can't use for portfolio (URL, no HTTPS)
- Only 1 app (can't experiment much)

**Learning-Friendly: 7/10**
- Simple for Python beginners
- Good docs for Python
- Community is small
- Good if you only know Python

**Upgrade Path: 7/10**
- $5/month for paid tier
- Reasonable price
- But still limited vs competitors
- Not as modern as alternatives

**Total: 33/50** - Okay for pure learning, bad for portfolio

## Winner: Vercel

### Why Vercel Wins for Hobbyists

1. **True free forever**: No gotchas, no trials, just free
2. **Generous limits**: 100GB bandwidth enough for most personal projects
3. **No sleeping**: Apps always responsive (great for portfolio)
4. **Professional URLs**: vercel.app looks fine for portfolio
5. **Best DX**: Learn industry-standard tools (Next.js, etc.)

### When to Choose Alternatives

**Choose Netlify if:**
- Prefer JAMstack focus over Next.js
- Like Netlify's forms/identity features
- Similar to Vercel, slightly different ecosystem

**Choose Cloudflare if:**
- Want to learn edge computing
- Need unlimited bandwidth (big projects)
- Want best free tier in terms of limits
- Don't mind steeper learning curve

**Choose Railway if:**
- Learning full-stack with databases
- Want to learn Docker
- Need to run multiple services
- $5/month credit is very generous

**Choose Fly.io if:**
- Already know Docker
- Want to learn containers/distributed systems
- Need persistent storage
- 3 VMs = multiple projects

**Choose Render if:**
- Don't care about sleeping (15min inactivity)
- Just need quick deploys for learning
- Can live with cold starts

**Avoid PythonAnywhere for portfolio:**
- No HTTPS on free tier = unprofessional
- No custom domains = can't use for portfolio
- Limited to 1 app = can't experiment

## Learning Path Recommendations

### Beginner (New to Web Dev)
**Best**: Vercel or Netlify
- Deploy in minutes
- Focus on code, not infrastructure
- Learn modern frameworks
- Great documentation

### Intermediate (Want to Learn Full-Stack)
**Best**: Railway or Fly.io
- Learn databases, Docker
- Multi-service architecture
- More realistic to production
- $5 credit / free VMs enough

### Advanced (Want to Learn Edge/Distributed)
**Best**: Cloudflare Workers or Fly.io
- Learn edge computing
- Understand distributed systems
- Industry-relevant skills
- Both have generous free tiers

## QRCards Context

**If QRCards was a learning project:**

**Vercel/Netlify**: Would need to rewrite as JAMstack (not worth it)
**Railway**: Could deploy Flask app, learn Docker ($5 credit covers it)
**Fly.io**: Same as Railway, learn containers
**PythonAnywhere**: Actually perfect for learning Flask!
**Render**: Could work but sleeping is annoying

**Verdict**: PythonAnywhere free tier is actually ideal for learning Flask basics

**But for portfolio/production**: Upgrade to $5/month for HTTPS and custom domain, or use Railway's free credit for more modern deployment

## The "Portfolio Effect"

**Critical for hobbyists**: Can you show this in portfolio?

| Provider | Portfolio-Ready (Free Tier) |
|----------|----------------------------|
| Vercel | Yes - vercel.app, HTTPS, fast |
| Netlify | Yes - netlify.app, HTTPS, fast |
| Cloudflare | Yes - pages.dev, HTTPS, fast |
| Railway | Yes - railway.app, HTTPS, always-on |
| Fly.io | Yes - fly.dev, HTTPS, mostly-on |
| Render | No - sleeps after 15min, slow cold start |
| PythonAnywhere | No - no HTTPS, unprofessional URL |

**Winner for portfolio**: Vercel, Netlify, or Cloudflare
**Best for learning**: Still Vercel (portfolio + learning combined)
