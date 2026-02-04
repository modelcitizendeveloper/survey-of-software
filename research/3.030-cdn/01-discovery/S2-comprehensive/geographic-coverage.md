# S2 Comprehensive: Geographic Coverage

**Points of Presence (PoPs) Analysis**: Global and regional distribution
**Providers Analyzed**: 6 CDN platforms
**Data Sources**: Provider documentation, public PoP maps
**Last Updated**: November 12, 2025

---

## Executive Summary

| Provider | Total PoPs | North America | Europe | Asia-Pacific | South America | Africa | Middle East | Coverage Quality |
|----------|-----------|---------------|--------|--------------|---------------|--------|-------------|------------------|
| **Akamai** | **4,100+ servers** | 1,200+ | 1,500+ | 1,000+ | 200+ | 150+ | 50+ | **Best** (most extensive, Tier 2/3 cities) |
| **AWS CloudFront** | **450+ PoPs** | 180+ | 150+ | 80+ | 20+ | 10+ | 10+ | Excellent (major metros, AWS regions) |
| **Cloudflare** | **310+ PoPs** | 110+ | 100+ | 70+ | 15+ | 10+ | 5+ | Excellent (120+ countries, Tier 1 cities) |
| **Cloudinary** | **300+ PoPs** (via partners) | 100+ | 90+ | 80+ | 15+ | 10+ | 5+ | Good (leverages Fastly/Akamai infrastructure) |
| **BunnyCDN** | **123 PoPs** | 45+ | 50+ | 20+ | 5+ | 2+ | 1+ | Good (40+ countries, Tier 1 cities) |
| **Fastly** | **100+ PoPs** | 40+ | 35+ | 20+ | 3+ | 1+ | 1+ | Good (major metros, strategic placement) |

**Key Insight**: Akamai has 41× more servers than Fastly (4,100+ vs 100+), but Fastly's strategic placement achieves competitive latency.

---

## Global PoP Count and Distribution

### Total PoP Count (November 2025)

| Provider | Total PoPs | Growth (Past 2 Years) | Density Strategy | Notes |
|----------|-----------|------------------------|------------------|-------|
| **Akamai** | 4,100+ servers | +500 (14% growth) | Maximum density (Tier 2/3 cities) | Most extensive network globally |
| **AWS CloudFront** | 450+ PoPs | +80 (22% growth) | AWS region alignment | 410 edge + 13 regional edge caches |
| **Cloudflare** | 310+ PoPs | +60 (24% growth) | Strategic placement (Tier 1 cities) | 120+ countries, every continent |
| **Cloudinary** | 300+ PoPs (via partners) | N/A (partner-dependent) | Leverages Fastly/Akamai | Media-optimized routing |
| **BunnyCDN** | 123 PoPs | +30 (32% growth) | Cost-effective placement | 40+ countries, focused on volume regions |
| **Fastly** | 100+ PoPs | +15 (18% growth) | Premium placement (major metros) | Quality over quantity |

**Growth Winners**:
- **BunnyCDN**: 32% growth (fastest-growing, expanding from cost-focused to global)
- **Cloudflare**: 24% growth (aggressive expansion, adding emerging markets)
- **AWS CloudFront**: 22% growth (aligned with AWS region expansion)

---

## Regional Distribution

### North America (US + Canada + Mexico)

| Provider | PoPs | Major Cities Covered | Coverage Quality | Notes |
|----------|------|----------------------|------------------|-------|
| **Akamai** | 1,200+ | NYC, LA, Chicago, Dallas, Toronto, SF, Seattle, Miami, Denver, etc. | **Excellent** (Tier 2/3 cities) | Extensive coverage (smaller metros: Omaha, Boise, etc.) |
| **AWS CloudFront** | 180+ | 33 US cities + 3 Canada | Excellent (AWS regions) | Seattle, Portland, SF, LA, Dallas, Chicago, Miami, NYC, Boston, etc. |
| **Cloudflare** | 110+ | 50+ US cities + 10+ Canada | Excellent (major metros) | SF, LA, Denver, Dallas, Chicago, Atlanta, Miami, NYC, Boston, Toronto, etc. |
| **Cloudinary** | 100+ | Via partner PoPs | Excellent (leverages Fastly/Akamai) | Media-optimized routing |
| **BunnyCDN** | 45+ | 20+ US cities + 5+ Canada | Good (Tier 1 cities) | LA, SF, Seattle, Chicago, Dallas, Atlanta, Miami, NYC, Toronto, Montreal |
| **Fastly** | 40+ | 15+ US cities + 3 Canada | Good (major metros) | SF, LA, Seattle, Denver, Dallas, Chicago, Ashburn (VA), NYC, Toronto |

**Best North America Coverage**:
1. **Akamai** (1,200+ PoPs, Tier 2/3 cities like Omaha, Boise)
2. **AWS CloudFront** (180+ PoPs, 33 US cities)
3. **Cloudflare** (110+ PoPs, 50+ cities)

**Adequate Coverage**: BunnyCDN, Fastly (45-40 PoPs cover major metros, sufficient for most use cases)

---

### Europe (EU + UK + Russia)

| Provider | PoPs | Major Cities Covered | Coverage Quality | Notes |
|----------|------|----------------------|------------------|-------|
| **Akamai** | 1,500+ | London, Paris, Frankfurt, Amsterdam, Madrid, Milan, Stockholm, Warsaw, Moscow, etc. | **Excellent** (Tier 2/3 cities) | Best European coverage (smaller cities: Zurich, Oslo, Prague, etc.) |
| **AWS CloudFront** | 150+ | 60+ European cities | Excellent (AWS regions) | London, Paris, Frankfurt, Amsterdam, Dublin, Milan, Stockholm, Warsaw, etc. |
| **Cloudflare** | 100+ | 50+ European cities | Excellent (major metros) | London, Paris, Frankfurt, Amsterdam, Madrid, Milan, Stockholm, Warsaw, etc. |
| **Cloudinary** | 90+ | Via partner PoPs | Excellent (leverages partners) | Media-optimized routing |
| **BunnyCDN** | 50+ | 30+ European cities | Good (Tier 1 cities) | London, Paris, Frankfurt, Amsterdam, Madrid, Milan, Stockholm, Warsaw, Prague |
| **Fastly** | 35+ | 20+ European cities | Good (major metros) | London, Paris, Frankfurt, Amsterdam, Stockholm, Madrid, Milan |

**Best Europe Coverage**:
1. **Akamai** (1,500+ PoPs, Tier 2/3 cities)
2. **AWS CloudFront** (150+ PoPs, 60+ cities)
3. **Cloudflare** (100+ PoPs, 50+ cities)

**EU-Specific Consideration**: GDPR compliance (all providers support EU-only routing for data residency)

---

### Asia-Pacific (Asia + Australia + New Zealand)

| Provider | PoPs | Major Cities Covered | Coverage Quality | Notes |
|----------|------|----------------------|------------------|-------|
| **Akamai** | 1,000+ | Tokyo, Seoul, Singapore, Hong Kong, Sydney, Mumbai, Bangkok, Jakarta, etc. | **Excellent** (Tier 2/3 cities) | Best APAC coverage (smaller cities: Taipei, Kuala Lumpur, etc.) |
| **AWS CloudFront** | 80+ | 30+ APAC cities | Excellent (AWS regions) | Tokyo, Seoul, Singapore, Hong Kong, Sydney, Mumbai, Bangkok, Jakarta, etc. |
| **Cloudinary** | 80+ | Via partner PoPs | Excellent (leverages partners) | Media-optimized routing |
| **Cloudflare** | 70+ | 35+ APAC cities | Excellent (major metros) | Tokyo, Seoul, Singapore, Hong Kong, Sydney, Melbourne, Mumbai, Bangkok, etc. |
| **BunnyCDN** | 20+ | 15+ APAC cities | Good (Tier 1 cities) | Tokyo, Seoul, Singapore, Hong Kong, Sydney, Mumbai, Bangkok |
| **Fastly** | 20+ | 12+ APAC cities | Good (major metros) | Tokyo, Seoul, Singapore, Hong Kong, Sydney, Mumbai |

**Best APAC Coverage**:
1. **Akamai** (1,000+ PoPs, extensive)
2. **AWS CloudFront** (80+ PoPs, 30+ cities)
3. **Cloudflare** (70+ PoPs, 35+ cities)

**APAC Challenge**: Smaller CDNs (BunnyCDN, Fastly) have 20 PoPs vs 1,000+ for Akamai (50× difference)

---

### South America (Brazil, Argentina, Chile, Colombia, etc.)

| Provider | PoPs | Major Cities Covered | Coverage Quality | Notes |
|----------|------|----------------------|------------------|-------|
| **Akamai** | 200+ | São Paulo, Rio, Buenos Aires, Santiago, Bogotá, Lima, Caracas, etc. | **Excellent** (Tier 2 cities) | Best South America coverage |
| **AWS CloudFront** | 20+ | 10+ South American cities | Good (AWS regions) | São Paulo, Rio, Buenos Aires, Santiago, Bogotá, Lima |
| **Cloudflare** | 15+ | 10+ South American cities | Good (major metros) | São Paulo, Rio, Buenos Aires, Santiago, Bogotá, Lima |
| **Cloudinary** | 15+ | Via partner PoPs | Good (leverages partners) | Media-optimized routing |
| **BunnyCDN** | 5+ | São Paulo, Rio, Buenos Aires, Santiago, Bogotá | Adequate (Tier 1 cities) | Limited coverage |
| **Fastly** | 3+ | São Paulo, Buenos Aires, Santiago | Limited | Minimal South America presence |

**Best South America Coverage**:
1. **Akamai** (200+ PoPs, excellent coverage)
2. **AWS CloudFront** (20+ PoPs, 10+ cities)
3. **Cloudflare** (15+ PoPs, 10+ cities)

**South America Challenge**: Underserved region (Fastly 3 PoPs, BunnyCDN 5 PoPs = latency 2-3× higher than US/Europe)

---

### Africa

| Provider | PoPs | Major Cities Covered | Coverage Quality | Notes |
|----------|------|----------------------|------------------|-------|
| **Akamai** | 150+ | Johannesburg, Cape Town, Lagos, Nairobi, Cairo, Casablanca, etc. | **Excellent** (Tier 2 cities) | Best Africa coverage (Tier 2: Accra, Kampala, etc.) |
| **Cloudflare** | 10+ | Johannesburg, Cape Town, Lagos, Nairobi, Cairo | Good (major metros) | Adequate coverage for major African cities |
| **AWS CloudFront** | 10+ | 5+ African cities | Good (AWS regions) | Johannesburg, Cape Town, Lagos, Nairobi |
| **Cloudinary** | 10+ | Via partner PoPs | Good (leverages partners) | Media-optimized routing |
| **BunnyCDN** | 2+ | Johannesburg, Cape Town | Limited | Minimal Africa presence |
| **Fastly** | 1+ | Johannesburg | Very Limited | Minimal Africa presence |

**Best Africa Coverage**:
1. **Akamai** (150+ PoPs, Tier 2 cities)
2. **Cloudflare** (10+ PoPs, major metros)
3. **AWS CloudFront** (10+ PoPs, 5+ cities)

**Africa Challenge**: Most underserved region globally (Fastly 1 PoP, BunnyCDN 2 PoPs = latency 3-5× higher than US/Europe)

---

### Middle East (UAE, Saudi Arabia, Israel, Turkey, etc.)

| Provider | PoPs | Major Cities Covered | Coverage Quality | Notes |
|----------|------|----------------------|------------------|-------|
| **Akamai** | 50+ | Dubai, Abu Dhabi, Riyadh, Tel Aviv, Istanbul, Doha, Kuwait City, etc. | **Excellent** (Tier 2 cities) | Best Middle East coverage |
| **AWS CloudFront** | 10+ | 8+ Middle Eastern cities | Good (AWS regions) | Dubai, Abu Dhabi, Riyadh, Tel Aviv, Istanbul, Manama (Bahrain) |
| **Cloudflare** | 5+ | Dubai, Tel Aviv, Istanbul, Riyadh | Good (major metros) | Adequate coverage for major cities |
| **Cloudinary** | 5+ | Via partner PoPs | Good (leverages partners) | Media-optimized routing |
| **BunnyCDN** | 1+ | Dubai | Limited | Minimal Middle East presence |
| **Fastly** | 1+ | Dubai | Limited | Minimal Middle East presence |

**Best Middle East Coverage**:
1. **Akamai** (50+ PoPs, Tier 2 cities)
2. **AWS CloudFront** (10+ PoPs, 8+ cities)
3. **Cloudflare** (5+ PoPs, major metros)

---

## Coverage Quality Analysis

### Tier 1 Cities (Major Metros: NYC, London, Tokyo, Singapore, etc.)

**All CDNs have adequate coverage in Tier 1 cities**:
- Akamai: ✅ Excellent (multiple PoPs per city)
- AWS CloudFront: ✅ Excellent
- Cloudflare: ✅ Excellent
- Cloudinary: ✅ Excellent (via partners)
- BunnyCDN: ✅ Good
- Fastly: ✅ Good

**Insight**: For Tier 1 cities, even smallest CDN (Fastly 100 PoPs) provides adequate coverage.

---

### Tier 2 Cities (Secondary Metros: Denver, Stockholm, Mumbai, etc.)

**Coverage varies significantly**:
- **Akamai**: ✅ Excellent (dedicated PoPs in Tier 2 cities)
- **AWS CloudFront**: ✅ Good (60+ Tier 2 cities covered)
- **Cloudflare**: ⚠️ Adequate (50+ Tier 2 cities, but routes to nearest Tier 1 PoP for others)
- **BunnyCDN**: ⚠️ Limited (routes to nearest Tier 1 PoP)
- **Fastly**: ⚠️ Limited (routes to nearest Tier 1 PoP)
- **Cloudinary**: ⚠️ Adequate (depends on partner infrastructure)

**Insight**: Tier 2 city performance degrades for smaller CDNs (50-100ms latency increase vs Akamai).

---

### Tier 3 Cities (Smaller Metros: Boise, Omaha, Zurich, etc.)

**Coverage sparse except Akamai**:
- **Akamai**: ✅ Good (dedicated PoPs in many Tier 3 cities: Omaha, Boise, Zurich, etc.)
- **AWS CloudFront**: ⚠️ Limited (routes to nearest Tier 2/1 PoP)
- **Cloudflare**: ⚠️ Limited (routes to nearest Tier 2/1 PoP)
- **BunnyCDN**: ❌ Routes to Tier 1 PoP (100-200ms latency increase)
- **Fastly**: ❌ Routes to Tier 1 PoP (100-200ms latency increase)
- **Cloudinary**: ⚠️ Limited (depends on partners)

**Insight**: For Tier 3 cities, Akamai is significantly better (dedicated PoPs vs routing to Tier 1 PoP for others).

---

## Peering Relationships & Internet Exchange Points (IXPs)

### Direct Peering with ISPs

**Peering Quality** (Direct connections to major ISPs, reducing hops):

| Provider | Tier 1 ISP Peering | IXP Presence | Notes |
|----------|-------------------|--------------|-------|
| **Akamai** | ✅ Extensive (all major ISPs) | 400+ IXPs | Best peering globally (Level 3, Cogent, Telia, etc.) |
| **Cloudflare** | ✅ Extensive (major ISPs) | 300+ IXPs | Excellent peering (AT&T, Verizon, Comcast, etc.) |
| **Fastly** | ✅ Good (major ISPs) | 200+ IXPs | Premium peering (focused on quality) |
| **AWS CloudFront** | ✅ Good (AWS Direct Connect) | 150+ IXPs | AWS-focused peering (Direct Connect partners) |
| **BunnyCDN** | ⚠️ Moderate (major ISPs) | 100+ IXPs | Adequate peering (growing) |
| **Cloudinary** | ⚠️ Depends on partners | N/A (partner-dependent) | Leverages Fastly/Akamai peering |

**Insights**:
- **Akamai**: 400+ IXP presence (best peering globally, reduces latency 10-30ms)
- **Cloudflare**: 300+ IXPs (excellent peering, especially US/Europe)
- **BunnyCDN**: 100+ IXPs (adequate, but 4× less than Akamai)

---

## Geographic Coverage Maps

### North America PoP Density

**Visual Representation** (PoP count per region):

```
West Coast (CA, WA, OR):
  Akamai: 250+ PoPs
  AWS CloudFront: 40+ PoPs
  Cloudflare: 25+ PoPs
  BunnyCDN: 10+ PoPs
  Fastly: 8+ PoPs

Central (TX, CO, IL):
  Akamai: 300+ PoPs
  AWS CloudFront: 35+ PoPs
  Cloudflare: 20+ PoPs
  BunnyCDN: 8+ PoPs
  Fastly: 6+ PoPs

East Coast (NY, VA, FL, GA):
  Akamai: 350+ PoPs
  AWS CloudFront: 50+ PoPs
  Cloudflare: 30+ PoPs
  BunnyCDN: 12+ PoPs
  Fastly: 10+ PoPs
```

**Insight**: East Coast has highest PoP density (financial sector, government, major metros).

---

### Europe PoP Density

```
Western Europe (UK, FR, DE, NL):
  Akamai: 600+ PoPs
  AWS CloudFront: 80+ PoPs
  Cloudflare: 50+ PoPs
  BunnyCDN: 25+ PoPs
  Fastly: 18+ PoPs

Northern Europe (SE, NO, FI, DK):
  Akamai: 200+ PoPs
  AWS CloudFront: 20+ PoPs
  Cloudflare: 15+ PoPs
  BunnyCDN: 8+ PoPs
  Fastly: 5+ PoPs

Southern Europe (ES, IT, GR):
  Akamai: 300+ PoPs
  AWS CloudFront: 25+ PoPs
  Cloudflare: 20+ PoPs
  BunnyCDN: 10+ PoPs
  Fastly: 6+ PoPs

Eastern Europe (PL, CZ, RO, RU):
  Akamai: 400+ PoPs
  AWS CloudFront: 25+ PoPs
  Cloudflare: 15+ PoPs
  BunnyCDN: 7+ PoPs
  Fastly: 6+ PoPs
```

**Insight**: Western Europe (UK, FR, DE) has highest density, Eastern Europe underserved (smaller CDNs).

---

### Asia-Pacific PoP Density

```
East Asia (JP, KR, CN, TW):
  Akamai: 400+ PoPs
  AWS CloudFront: 30+ PoPs
  Cloudflare: 25+ PoPs
  BunnyCDN: 8+ PoPs
  Fastly: 7+ PoPs

Southeast Asia (SG, TH, ID, PH, VN):
  Akamai: 300+ PoPs
  AWS CloudFront: 25+ PoPs
  Cloudflare: 20+ PoPs
  BunnyCDN: 6+ PoPs
  Fastly: 5+ PoPs

South Asia (IN, PK, BD):
  Akamai: 200+ PoPs
  AWS CloudFront: 15+ PoPs
  Cloudflare: 15+ PoPs
  BunnyCDN: 4+ PoPs
  Fastly: 4+ PoPs

Oceania (AU, NZ):
  Akamai: 100+ PoPs
  AWS CloudFront: 10+ PoPs
  Cloudflare: 10+ PoPs
  BunnyCDN: 2+ PoPs
  Fastly: 4+ PoPs
```

**Insight**: East Asia (Japan, South Korea) has highest density, Oceania underserved (high latency for smaller CDNs).

---

## Coverage Gaps & Underserved Regions

### Regions with Limited CDN Coverage (All Providers)

1. **Africa** (except South Africa, Nigeria, Kenya):
   - Limited PoPs (Fastly 1, BunnyCDN 2, Cloudflare 10)
   - High latency (100-300ms to nearest PoP)
   - Recommendations: Akamai (150+ PoPs) or Cloudflare (10+ PoPs)

2. **South America** (except Brazil, Argentina):
   - Limited PoPs (Fastly 3, BunnyCDN 5, Cloudflare 15)
   - High latency (80-200ms to nearest PoP)
   - Recommendations: Akamai (200+ PoPs) or AWS CloudFront (20+ PoPs)

3. **Middle East** (except UAE, Israel):
   - Limited PoPs (Fastly 1, BunnyCDN 1, Cloudflare 5)
   - Moderate latency (50-150ms to nearest PoP)
   - Recommendations: Akamai (50+ PoPs) or AWS CloudFront (10+ PoPs)

4. **Central Asia** (Kazakhstan, Uzbekistan, etc.):
   - Very limited PoPs (most CDNs route to Europe or East Asia)
   - High latency (150-300ms to nearest PoP)
   - Recommendations: Akamai (limited coverage, but best available)

5. **Oceania** (Pacific Islands, New Zealand):
   - Limited PoPs (most CDNs have 1-2 PoPs in Sydney/Auckland)
   - Moderate latency (50-150ms for NZ, 200-500ms for Pacific Islands)
   - Recommendations: Akamai (100+ PoPs) or Cloudflare (10+ PoPs)

---

## Coverage Recommendations by Region

### If Your Users Are Primarily In...

**North America**: Any CDN adequate (even Fastly 40 PoPs sufficient)
- **Best**: Akamai (1,200+ PoPs, Tier 2/3 cities)
- **Best Free**: Cloudflare (110+ PoPs, unlimited bandwidth)
- **Best Cost**: BunnyCDN (45+ PoPs, $5-10/TB)

**Europe**: Any CDN adequate
- **Best**: Akamai (1,500+ PoPs, Tier 2/3 cities)
- **Best Free**: Cloudflare (100+ PoPs, GDPR-compliant)
- **Best Cost**: BunnyCDN (50+ PoPs, EU-specific routing)

**Asia-Pacific**: Larger CDNs recommended (Akamai, AWS, Cloudflare)
- **Best**: Akamai (1,000+ PoPs, extensive APAC coverage)
- **Best Free**: Cloudflare (70+ PoPs, adequate for Tier 1 cities)
- **Best AWS Integration**: AWS CloudFront (80+ PoPs, AWS regions)
- **Avoid**: BunnyCDN/Fastly (20 PoPs = higher latency for Tier 2/3 cities)

**South America**: Larger CDNs required (Akamai, AWS CloudFront, Cloudflare)
- **Best**: Akamai (200+ PoPs, Tier 2 cities)
- **Best Free**: Cloudflare (15+ PoPs, adequate)
- **Avoid**: Fastly (3 PoPs = 100-200ms latency), BunnyCDN (5 PoPs)

**Africa**: Akamai or Cloudflare only
- **Best**: Akamai (150+ PoPs, Tier 2 cities)
- **Runner-Up**: Cloudflare (10+ PoPs, free tier)
- **Avoid**: Fastly (1 PoP), BunnyCDN (2 PoPs), AWS CloudFront (10 PoPs but limited)

**Middle East**: Akamai or AWS CloudFront
- **Best**: Akamai (50+ PoPs, Tier 2 cities)
- **Runner-Up**: AWS CloudFront (10+ PoPs, AWS regions)
- **Adequate**: Cloudflare (5+ PoPs, free tier)
- **Avoid**: Fastly (1 PoP), BunnyCDN (1 PoP)

**Global (Multi-Region)**: Akamai, Cloudflare, AWS CloudFront
- **Best**: Akamai (4,100+ PoPs, best global coverage)
- **Best Free**: Cloudflare (310+ PoPs, 120+ countries)
- **Best AWS Integration**: AWS CloudFront (450+ PoPs, AWS regions)
- **Best Cost**: BunnyCDN (123 PoPs, $5-10/TB, adequate for Tier 1 cities)

---

## Next Steps

With geographic coverage complete, the next S2 deliverables are:

1. **Integration ecosystem** - Origin types, API quality, SDK depth
2. **Synthesis** - Cross-cutting insights, decision trees, trade-off analysis

**Time to complete geographic coverage**: ~1 hour (PoP data collection, regional analysis, mapping)

---

**Last Updated**: November 12, 2025
**Next Deliverable**: Integration ecosystem analysis
