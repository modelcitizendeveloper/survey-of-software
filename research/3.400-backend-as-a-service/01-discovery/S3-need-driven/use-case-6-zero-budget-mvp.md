# Use Case 6: Zero-Budget MVP (Side Project, $0-12/Month)

## Scenario Profile

**Developer**: Indie hacker, solo founder, side project
**Tech Stack**: Any (flexibility required)
**Experience**: Varies (beginner to expert)
**Priority**: Zero cost, fast deployment, lowest lock-in

## Requirements (Scoring Criteria)

1. **Cost** (Weight: High) - $0-12/month total (VPS + backend)
2. **Setup Speed** (Weight: High) - Minutes to first API, not hours
3. **Lock-In** (Weight: High) - Low lock-in (easy migration when scaling)
4. **Free Tier Generosity** (Weight: Medium) - Sufficient for MVP (1K-5K users)
5. **Scaling Path** (Weight: Medium) - Easy migration to paid tier or self-hosted when growing

## Provider Scoring

| Provider | Cost | Setup Speed | Lock-In | Free Tier | Scaling | **Total** |
|----------|------|-------------|---------|-----------|---------|-----------|
| **PocketBase** | 10 | 10 | 10 | 10 | 8 | **48/50** |
| **Supabase** | 9 | 9 | 7 | 9 | 9 | **43/50** |
| **Firebase** | 9 | 8 | 3 | 9 | 7 | **36/50** |
| **Xata** | 8 | 8 | 7 | 8 | 8 | **39/50** |
| **Appwrite** | 7 | 6 | 7 | 0 | 8 | **28/50** |
| **Nhost** | 7 | 7 | 7 | 7 | 8 | **36/50** |

## Winner: PocketBase (48/50)

**Why PocketBase Wins:**
- **$5/month total:** Hetzner CX11 VPS ($5), no BaaS fees (MIT open-source)
- **2-minute setup:** Download binary, run `./pocketbase serve`, backend live
- **Lowest lock-in (50/100):** SQLite database (standard SQL), REST API (easy to replace)
- **Unlimited free tier:** No storage limits, no request limits, no user limits (self-hosted)
- **Easy scaling:** Migrate to Supabase when exceeding SQLite limits (60-100 hours, $6K-10K)

**Cost Breakdown:**
- VPS: $5/month (Hetzner CX11: 1 CPU, 1 GB RAM, 25 GB SSD)
- BaaS: $0/month (MIT license, free forever)
- **Total: $5/month** (cheapest BaaS option)

**Use Cases:** Side projects, indie hacker MVPs, learning projects, weekend hackathons

**Limitation:** SQLite scaling (not for >10K concurrent users, migrate to Supabase/PostgreSQL when scaling)

## Runner-Up: Supabase (43/50)

**Why Second Place:**
- **$0/month:** Free tier (500 MB DB, 1 GB storage, 2 GB bandwidth, 50K MAU)
- **5-minute setup:** Signup, create project, database live
- **Moderate lock-in (75/100):** PostgreSQL (standard SQL, easy migration to self-hosted)
- **Generous free tier:** Sufficient for 1K-5K users
- **Easy scaling:** $25/month Pro tier when outgrowing free tier

**Cost Breakdown:**
- Free tier: $0/month (sufficient for MVP, 1K-5K users)
- Pro tier: $25/month (when scaling to 10K-100K users)
- **Total: $0-25/month**

**When to Choose:** Prefer managed cloud over self-hosting (no DevOps skills)

**Deduction:** Higher lock-in than PocketBase (75/100 vs 50/100), requires migration to paid tier when scaling

## Firebase: 36/50 (Acceptable)

**Why Third Place:**
- **$0/month:** Free tier (1 GB Firestore, 50K reads/day, 20K writes/day)
- **Generous free tier:** Sufficient for 1K-5K users
- **Good setup speed:** 10 minutes (Firebase Console, SDK integration)

**Deduction:**
- **Highest lock-in (85/100):** Firestore NoSQL, migration extremely difficult (200-400 hours)
- **Costs explode at scale:** Per-read pricing ($600/month for 1B reads)

**When to Choose:** Mobile app requiring offline sync (Firebase's unique advantage)

**WARNING:** Only choose Firebase if mobile offline sync is critical (accept 85/100 lock-in for this feature)

## Summary

**PocketBase** is the best zero-budget BaaS ($5/month VPS, lowest lock-in 50/100, 2-minute setup). **Supabase** is runner-up ($0 managed cloud, moderate lock-in 75/100, 5-minute setup). **Firebase** is viable ($0 free tier, but highest lock-in 85/100, only if mobile offline sync needed).

**Recommendation:**
1. **Default: PocketBase** ($5/month, lowest lock-in, self-host)
2. **Alternative: Supabase** ($0 managed cloud, no DevOps required)
3. **Mobile only: Firebase** (offline sync, accept 85/100 lock-in)

**Bottom Line:** For zero-budget MVPs, choose **PocketBase** (self-host $5/month) or **Supabase** (managed free tier). Avoid Firebase unless mobile offline sync is critical (lock-in too high for most MVPs).
