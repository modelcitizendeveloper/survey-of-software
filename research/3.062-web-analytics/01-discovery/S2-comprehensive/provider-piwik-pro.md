# Piwik PRO

**Category:** Enterprise GDPR-Compliant Analytics
**Hosting:** Cloud (EU) or On-Premise
**Pricing Model:** Tiered subscription + Enterprise
**Primary Market:** Enterprise, regulated industries, government
**Website:** https://piwik.pro/

---

## Overview

Piwik PRO is an enterprise-focused, GDPR-compliant analytics and customer data platform. Originally forked from Matomo (formerly Piwik), it evolved into a proprietary platform targeting highly regulated industries requiring maximum privacy and security.

**Market Position:** Premium GDPR-compliant analytics for enterprises, especially regulated sectors (healthcare, finance, government).

**Philosophy:** "Privacy-first analytics & data activation platform for the digital age."

---

## Core Features

### Integrated Platform
- **Analytics:** Full web + mobile app analytics
- **Tag Manager:** Built-in tag management
- **Consent Manager:** Cookie consent management (powered by Cookie Information)
- **Customer Data Platform (CDP):** Data aggregation and activation

### Analytics Capabilities
- Traffic tracking, conversion funnels, e-commerce
- Custom reports and dashboards
- User segmentation and cohorts
- Real-time analytics
- Multi-site roll-up reporting
- API access

### Privacy Features
- Built-in GDPR, LGPD, PIPEDA compliance
- Consent management integrated
- Data anonymization tools
- EU data residency (cloud) or on-premise
- Anonymous tracking (4x more session data)

---

## Pricing Structure (New 2025 Model)

### Pricing Tiers (Effective August 4, 2025)

**Business Plan:**
- **Starting:** €35/month (£29.60/month)
- **Target:** Small to mid-size businesses
- **Hosting:** EU cloud (Sweden)
- **Features:** Core analytics, tag manager, consent manager

**Enterprise Tiers:**

1. **Trusted Insights**
   - Growth-oriented organizations
   - Advanced analytics, cross-channel integration
   - Data activation capabilities
   - Up to 500M monthly actions
   - Price: Custom (contact sales)

2. **Secure Intelligence**
   - Highly regulated industries
   - Maximum security features
   - Unlimited reporting capabilities
   - Private cloud hosting options
   - Price: Custom (likely $50K-100K+/year)

3. **Ultimate/On-Premise**
   - Full on-premise deployment
   - Complete control and customization
   - Dedicated support
   - Price: Custom (likely $100K-300K+/year)

**Historical Pricing (Pre-2025):**
- Core (Free): Discontinued December 2025
- Enterprise: Estimated $50K-150K+/year

**Cost Comparison:**
- **Small Business (100K actions):** €35+/month (Business)
- **Mid-Market (1M actions):** Custom Enterprise pricing
- **Large Enterprise (10M+ actions):** $50K-300K+/year

---

## Privacy & Compliance

### GDPR Compliance
**Status:** ✅ **Fully compliant by design**

- Built-in GDPR, LGPD, PIPEDA, HIPAA compliance
- Consent Manager integrated
- EU cloud hosting (Sweden)
- On-premise option for maximum control
- Data residency guarantees

### Data Residency
- **Cloud:** EU (Sweden) by default
- **On-Premise:** Your choice
- **Enterprise:** Private cloud options

### Cookie Requirements
- **Consent Manager:** Built-in (powered by Cookie Information)
- **Compliant Tracking:** With or without consent
- **Anonymous Mode:** Enhanced data collection without PII

---

## Implementation

### Tracking Code
```html
<!-- Piwik PRO Container -->
<script type="text/javascript">
  (function(window, document, dataLayerName, id) {
    window[dataLayerName]=window[dataLayerName]||[],
    window[dataLayerName].push({start:(new Date).getTime(),event:"stg.start"});
    var scripts=document.getElementsByTagName('script')[0],
        tags=document.createElement('script');
    function stgCreateCookie(a,b,c){var d="";if(c){var e=new Date;e.setTime(e.getTime()+24*c*60*60*1e3),d="; expires="+e.toUTCString()}document.cookie=a+"="+b+d+"; path=/"}
    var isStgDebug=(window.location.href.match("stg_debug")||document.cookie.match("stg_debug"))&&!window.location.href.match("stg_disable_debug");
    stgCreateCookie("stg_debug",isStgDebug?1:"",isStgDebug?14:-1);
    var qP=[];dataLayerName!=="dataLayer"&&qP.push("data_layer_name="+dataLayerName),isStgDebug&&qP.push("stg_debug");
    var qPString=qP.length>0?("?"+qP.join("&")):"";
    tags.async=!0,tags.src="https://your-instance.piwik.pro/"+id+".js"+qPString,scripts.parentNode.insertBefore(tags,scripts);
    !function(a,n,i){a[n]=a[n]||{};for(var c=0;c<i.length;c++)!function(i){a[n][i]=a[n][i]||{},a[n][i].api=a[n][i].api||function(){var a=[].slice.call(arguments,0);"string"==typeof a[0]&&window[dataLayerName].push({event:n+"."+i+":"+a[0],parameters:[].slice.call(arguments,1)})}}(i[c])}(window,"ppms",["tm","cm"]);
  })(window, document, 'dataLayer', 'YOUR_CONTAINER_ID');
</script>
```

**Difficulty:** 5/10 (enterprise complexity)
**Time:** 1-4 hours (full setup with Tag Manager)

---

## Pros and Cons

### Pros ✅
1. **Enterprise GDPR:** Built for regulated industries
2. **All-in-One:** Analytics + Tag Manager + Consent Manager + CDP
3. **EU Data Residency:** Guaranteed (cloud)
4. **On-Premise Option:** Maximum control
5. **HIPAA/Finance Compliant:** Suitable for healthcare, finance
6. **Anonymous Tracking:** 4x more data without PII
7. **Dedicated Support:** Enterprise SLAs

### Cons ❌
1. **Expensive:** €35/month minimum, Enterprise $50K-300K+/year
2. **Proprietary:** Not open-source (vs Matomo)
3. **Complexity:** Enterprise-grade = more complex
4. **Overkill:** Too much for simple needs
5. **Free Tier Ending:** Core plan discontinued (Dec 2025)

---

## Best Fit Scenarios

### Ideal For ✅
- **Regulated Industries:** Healthcare (HIPAA), finance, government
- **Enterprise EU:** Need GDPR compliance + advanced features
- **Data Residency Required:** EU hosting mandatory
- **All-in-One Platform:** Want analytics + consent + CDP
- **Maximum Privacy Control:** On-premise deployment needed

### Not Ideal For ❌
- **Small Businesses:** Too expensive, complex
- **Simple Needs:** Overkill (use Plausible, Fathom)
- **Budget-Constrained:** Expensive vs alternatives
- **Open-Source Preference:** Proprietary (use Matomo)

---

## Recommendation Summary

**Use Piwik PRO if:**
- You're in regulated industry (healthcare, finance, government)
- GDPR + HIPAA compliance critical
- Enterprise budget ($50K-300K/year)
- Need EU data residency guarantees
- Want all-in-one platform (analytics + consent + CDP)

**Avoid if:**
- Small business with limited budget
- Simple analytics needs
- Prefer open-source (use Matomo instead)
- Don't need enterprise compliance features

---

**Last Updated:** October 11, 2025
**Pricing Update:** August 4, 2025 (new model)
**Best For:** Enterprise GDPR-compliant analytics for regulated industries
