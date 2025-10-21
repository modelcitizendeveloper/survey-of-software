# S3 Need-Driven Recommendation: POS Selection by Business Type

**Methodology:** Need-Driven Discovery (requirement-focused, use-case matching)
**Last Updated:** October 20, 2025

---

## Quick Decision Guide

**Answer 3 questions to find your POS:**

### **Question 1: What type of business?**
- Restaurant → Continue to Q2
- Retail → Continue to Q3
- Service (salon, spa, fitness) → **Square Appointments** (Free-$60/mo) or **Vagaro** ($25+/mo)
- Mobile/Pop-up → **Square** reader ($50) or **SumUp** (UK/Europe, 1.69%)

### **Question 2 (Restaurants): Service style?**
- Quick-service/Counter → **Square** (Free-$60/mo) or **Toast** ($69+/mo)
- Full-service/Table service → **Toast** ($69+/mo) or **TouchBistro** ($69+/mo)
- Bar/Wine bar → **Square** or **Toast** (with BevSpot integration)
- Food truck/Catering → **Square** (mobile-optimized)

### **Question 3 (Retail): Inventory complexity?**
- Simple (few SKUs, no variants) → **Square** (Free-$60/mo)
- Medium (variants, suppliers) → **Shopify POS** ($89+/mo) or **Clover** ($14.95+/mo)
- Complex (fashion, multi-location) → **Lightspeed Retail** ($69+/mo)
- Retail + E-commerce → **Shopify POS** ($89+/mo)

---

## Recommendations by Business Type

### **Restaurants: Quick-Service / Fast-Casual**

**Primary:** **Square for Restaurants** (Free or $60/mo)
- Best for: Counter service, limited menu, mobile ordering
- Processing: 2.6% + 10¢ standard
- Hardware: $299 Register or $799 Terminal
- Strengths: Simple setup, affordable, mobile-friendly
- Weaknesses: Limited table management, basic kitchen display

**Alternative:** **Toast** ($69/mo + processing)
- When to choose: Need kitchen display system, online ordering integration
- Processing: 2.49% + 15¢
- Hardware: Bundled (lease or purchase)
- Strengths: Purpose-built for restaurants, excellent support
- Weaknesses: Higher cost, lock-in to Toast ecosystem

---

### **Restaurants: Full-Service / Table Service**

**Primary:** **Toast** ($69-$165/mo + processing)
- Best for: Table service, complex menus, bar tabs, split bills
- Key features: Table management, coursing, server assignments, tip pooling
- Processing: 2.49% + 15¢ (negotiable for volume)
- TCO Example: $100K/mo revenue = ~$2,559/mo total cost
- See detailed analysis: `use-case-restaurant-full-service.md`

**Alternative:** **TouchBistro** ($69/mo per terminal)
- When to choose: Need offline reliability (hybrid cloud + local)
- Processing: Bring your own (processor-agnostic)
- Strengths: Best offline mode, flexible payment processing
- Weaknesses: iPad-only, requires local server for multi-terminal

---

### **Bars / Wine Bars**

**Primary:** **Square for Restaurants** (Free or $60/mo)
- Best for: Simple setup, tab management, tips
- Inventory: Basic pour tracking (integrate BevSpot for advanced)
- Processing: 2.6% + 10¢

**Alternative:** **Toast** (if need advanced beverage features)
- When to choose: Complex drink menu, happy hour pricing, modifier-heavy
- Strengths: Better beverage-specific features, online ordering for pickup

---

### **Retail: General / Small Shop**

**Primary:** **Square for Retail** (Free or $60/mo)
- Best for: Simple inventory, single/few locations, straightforward needs
- Inventory: Variants, categories, low stock alerts
- Processing: 2.6% + 10¢
- Hardware: $49 reader to $799 terminal
- Strengths: Free plan, easy setup, affordable hardware

**Alternative:** **Clover** ($14.95-$104.95/mo)
- When to choose: Want app marketplace, customization, receipt printing
- Strengths: 300+ apps, customizable workflows
- Weaknesses: Higher cost, Fiserv processing fees

---

### **Retail: Fashion / Apparel / Complex Inventory**

**Primary:** **Lightspeed Retail** ($69-$89/mo starting)
- Best for: Variants (size, color, style), seasons, suppliers, purchase orders
- Inventory: Advanced features (matrix variants, multi-location transfers)
- Processing: Lightspeed Payments or bring your own
- Strengths: Best retail inventory management, reporting
- Weaknesses: Higher cost, steeper learning curve

**Alternative:** **Shopify POS Pro** ($89/mo + Shopify plan)
- When to choose: Also selling online, want unified inventory
- Strengths: Seamless online/offline, omnichannel customer view
- Weaknesses: E-commerce plan required ($79-$399/mo)

---

### **Retail: Multi-Location (5+ stores)**

**Primary:** **Lightspeed Retail** ($189+/mo for multi-location plans)
- Best for: Chain management, centralized reporting, inventory transfers
- Features: Central dashboard, multi-store inventory, consolidated reporting
- Strengths: Purpose-built for chains
- Weaknesses: Enterprise pricing

**Alternative:** **Shopify POS** (contact for multi-location pricing)
- When to choose: E-commerce + multi-location retail
- Strengths: Unified platform, scalable
- Weaknesses: Higher total cost

---

### **Retail + E-Commerce (Omnichannel)**

**Primary:** **Shopify POS Pro** ($89/mo + Shopify plan $79+/mo)
- Best for: Physical store + online store, unified inventory
- Features: Buy online/pickup in store, unified customer profiles, centralized inventory
- Processing: 2.7% online + 2.5% in-store (with Shopify Payments)
- Strengths: Best omnichannel experience, seamless integration
- Weaknesses: Higher monthly cost ($168+/mo minimum)

**Alternative:** **Square** (POS + Square Online)
- When to choose: Budget-conscious, simpler e-commerce needs
- Strengths: Affordable, easier setup
- Weaknesses: Less sophisticated omnichannel features

---

### **Services: Solo Practitioner (Salon, Spa, Personal Trainer)**

**Primary:** **Square Appointments** (Free to $60/mo)
- Best for: Appointment booking, solo or small team
- Features: Online booking, calendar, client management, deposits
- Processing: 2.6% + 10¢
- Strengths: Free tier, integrated with Square ecosystem
- Weaknesses: Limited features for larger teams

---

### **Services: Multi-Provider (Salons, Spas, Fitness Studios)**

**Primary:** **Vagaro** ($25/mo per provider)
- Best for: Salons, spas, fitness with multiple staff
- Features: Appointment booking, packages, memberships, payroll, marketing
- Processing: 2.35% + 20¢
- Strengths: Purpose-built for services industry, comprehensive features
- Weaknesses: Per-provider pricing adds up

**Alternative:** **Square Appointments Plus** ($50-$60/mo)
- When to choose: Prefer Square ecosystem, smaller team (2-5 providers)
- Strengths: Affordable, good features for price
- Weaknesses: Limited team scheduling features vs Vagaro

---

### **Mobile / Pop-up / Events**

**Primary:** **Square** reader ($50-$59)
- Best for: Farmers markets, craft fairs, events, mobile businesses
- Hardware: Contactless + Chip Reader ($50), phone/tablet-based
- Processing: 2.6% + 10¢
- Strengths: Portable, affordable, fast setup
- Weaknesses: Phone/tablet dependency, limited offline capability

**Alternative (UK/Europe):** **SumUp** (1.69% processing, £0/mo)
- Best for: European markets, lower processing fees
- Hardware: £19-£79 readers
- Strengths: Lowest processing in Europe, no monthly fee
- Weaknesses: Limited features vs Square

---

## Decision Matrix Summary

| Business Type | Simple/Budget | Advanced Features | Omnichannel | Multi-Location |
|---------------|---------------|-------------------|-------------|----------------|
| **QSR/Fast-Casual** | Square (Free) | Toast ($69/mo) | Square + Square Online | Toast (multi-location) |
| **Full-Service Restaurant** | Toast ($69/mo) | Toast ($165/mo) | Toast + Online Ordering | Toast (multi-location) |
| **Bar/Wine Bar** | Square (Free) | Toast ($69/mo) | Square + Online | Toast |
| **General Retail** | Square (Free) | Clover ($105/mo) | Shopify POS ($168/mo) | Lightspeed ($189+/mo) |
| **Fashion/Apparel** | Square ($60/mo) | Lightspeed ($69/mo) | Shopify POS ($168/mo) | Lightspeed ($189+/mo) |
| **Solo Service** | Square Appts (Free) | Square Appts Plus ($50/mo) | N/A | N/A |
| **Multi-Provider Service** | Square Appts ($50/mo) | Vagaro ($25/provider) | N/A | Vagaro (multi-location) |
| **Mobile/Events** | Square ($50 reader) | Square Register ($299) | N/A | N/A |

---

## Common Scenarios

### **"I'm opening my first coffee shop"**
→ **Square for Restaurants** (Free plan + $299 Register)
- Quick setup, affordable, mobile ordering via Square app
- Upgrade to $60/mo plan when revenue >$20K/mo

### **"I'm opening a full-service Italian restaurant with wine bar"**
→ **Toast** ($69/mo + $2,500/mo processing on $100K revenue)
- Table management, coursing, wine list, online ordering
- See `use-case-restaurant-full-service.md` for details

### **"I'm opening a boutique clothing store"**
→ **Lightspeed Retail** ($69/mo starting)
- Matrix inventory (size/color variants), seasonal management
- Upgrade to Shopify POS if launching e-commerce store

### **"I have a retail store and want to add online sales"**
→ **Shopify POS Pro** ($89/mo + Shopify plan $79+/mo)
- Unified inventory, buy online/pickup in-store
- Seamless omnichannel experience

### **"I'm a freelance hairstylist"**
→ **Square Appointments** (Free plan)
- Online booking, client management, mobile payments
- Upgrade to $50/mo when adding another stylist

### **"I run a 3-chair salon"**
→ **Vagaro** ($75/mo for 3 providers)
- Team scheduling, packages, memberships, marketing
- Better than Square for multi-provider services

---

## What NOT to Choose (Common Mistakes)

❌ **Toast for retail** - Overkill, restaurant-specific features wasted
❌ **Shopify POS for restaurant** - Not designed for table service
❌ **Clover for simple single-location retail** - Overpaying for customization you won't use
❌ **Square for 10-location chain** - Outgrown capabilities, need Lightspeed/enterprise
❌ **Free plan if doing >$50K/mo** - Paid plans save money at volume (better processing rates)

---

## Next Steps

1. **Identify your business type** from this guide
2. **Review primary recommendation** details (see use-case files)
3. **Sign up for free trial** (most platforms offer 30 days)
4. **Test with real transactions** (parallel with current system if migrating)
5. **Evaluate after 2-4 weeks** (staff feedback, feature gaps, costs)

**Note:** 15+ additional use-case documents planned. Currently complete:
- ✅ `use-case-restaurant-full-service.md` (comprehensive example)
- ⏳ 15 more use cases (coming soon)

---

**Last Updated:** October 20, 2025
**Methodology:** S3 Need-Driven Discovery (requirement-focused use-case matching)
**Companion Documents:** See `use-case-*.md` files for detailed business-type analysis
