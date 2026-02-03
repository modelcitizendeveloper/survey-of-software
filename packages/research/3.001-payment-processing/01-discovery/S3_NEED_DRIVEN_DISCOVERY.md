# S3: Need-Driven Discovery - Payment Processing Services

## Overview

This document analyzes payment processing provider fit for specific business use case patterns. Each section starts with business requirements, evaluates 2-3 best-fit providers, and provides decision criteria for choosing between finalists.

**Discovery Approach**: Use case requirements → provider fit analysis. Start with the need, find the best solution.

---

## Use Case Pattern #1: B2B SaaS Subscriptions

### Business Requirements

**Core Needs**:
- Monthly and annual billing cycles with prorated upgrades/downgrades
- Automated dunning management for failed payments
- Usage metering for tier-based or add-on services
- Customer self-service portal for subscription management
- Revenue recognition and financial reporting
- Seat-based or usage-based pricing models

**Technical Needs**:
- Webhook integration for subscription events
- API for programmatic subscription changes
- Support for trials, coupons, and discounts
- Multi-currency support for international customers
- Tax calculation and compliance (especially VAT/GST)

### Provider Fit Analysis

#### Stripe Billing (Best for Developer-Led Teams)

**Why It Fits**:
- Most comprehensive API for subscription management
- Advanced metering capabilities with real-time usage tracking
- Flexible billing logic: proration, billing anchors, invoice itemization
- Stripe Billing Portal provides customer self-service out-of-the-box
- Revenue Recognition reports for accrual accounting
- Strong webhook infrastructure for event-driven architecture

**Best For**:
- Teams with engineering resources to integrate APIs
- Companies needing custom billing logic or complex proration
- Businesses requiring precise usage metering (API calls, storage, seats)
- Startups wanting to avoid vendor lock-in with portable subscription data

**Limitations**:
- Requires tax calculation add-on (Stripe Tax) for automatic compliance
- Self-service portal has limited customization without coding
- More complex initial setup compared to merchant-of-record solutions

#### Paddle (Best for Global-First, Tax-Averse Teams)

**Why It Fits**:
- Merchant of Record model: Paddle handles all global tax compliance
- Built-in subscription management with dunning and recovery
- Customer portal included, no additional integration needed
- Handles VAT, GST, sales tax across 200+ countries automatically
- Single 1099 from Paddle simplifies accounting

**Best For**:
- Non-technical or small technical teams
- Companies selling internationally from day one
- Businesses wanting to avoid tax compliance burden entirely
- SaaS products with straightforward subscription models

**Limitations**:
- Less flexible for complex custom billing logic
- Higher effective fees (10% vs Stripe's 2.9% + metering costs)
- Less control over customer payment experience
- Limited API compared to Stripe for programmatic changes

#### Chargebee (Best for Complex Billing Requirements)

**Why It Fits**:
- Advanced subscription logic: multi-plan hierarchies, contract terms, amendments
- Sophisticated dunning workflows with customizable retry logic
- Revenue recognition automation aligned with ASC 606 / IFRS 15
- Extensive integrations with CRM, accounting, and analytics tools
- Support for hybrid pricing: subscriptions + one-time charges + usage

**Best For**:
- Mid-market to enterprise SaaS with complex billing needs
- Companies requiring contract-based billing with amendments
- Businesses needing advanced revenue recognition reporting
- Teams managing multiple products or service tiers

**Limitations**:
- Higher cost structure, typically starts at $300+/month
- More configuration complexity than simpler solutions
- May be overkill for early-stage or simple subscription models

### Decision Criteria

**Choose Stripe Billing if**:
- You have a technical team and want maximum API flexibility
- You need precise usage metering or complex proration logic
- You want to maintain control over customer payment flows
- You're building a developer-focused product

**Choose Paddle if**:
- You're selling globally and don't want tax compliance headaches
- You have limited technical resources for payment integration
- You want a simple all-in-one solution with predictable fees
- Your subscription model is relatively straightforward

**Choose Chargebee if**:
- You have complex multi-tier subscriptions or contract terms
- You need sophisticated revenue recognition automation
- You require extensive third-party integrations (Salesforce, NetSuite)
- You're past early stage and willing to invest in billing infrastructure

**Decision Tree**:
```
Is tax compliance a major concern (selling globally)?
├─ YES: Do you have technical resources?
│   ├─ YES → Stripe + Stripe Tax
│   └─ NO → Paddle
└─ NO: How complex is your billing logic?
    ├─ Simple subscriptions → Stripe Billing
    └─ Complex contracts/pricing → Chargebee
```

---

## Use Case Pattern #2: Digital Product Sales

### Business Requirements

**Core Needs**:
- One-time purchase processing with instant product delivery
- Global tax compliance (VAT, GST, sales tax across jurisdictions)
- Digital product distribution (license keys, downloads, course access)
- Affiliate or partner marketing programs
- Shopping cart abandonment recovery
- EU VAT MOSS compliance for digital goods

**Technical Needs**:
- Webhook for purchase events to trigger delivery
- Integration with course platforms, license managers, or download systems
- Support for coupons, bundles, and promotional pricing
- Email marketing integration for post-purchase sequences
- Fraud detection for high-value digital products

### Provider Fit Analysis

#### Lemon Squeezy (Best for Speed and Simplicity)

**Why It Fits**:
- Merchant of Record with automatic global tax handling
- Built-in digital product delivery and license key management
- Affiliate program functionality included
- Email marketing features for upsells and campaigns
- Simple setup: sell within hours, not days
- Transparent flat 5% + payment processing fees

**Best For**:
- Solo creators and small teams launching quickly
- Digital products: courses, ebooks, software licenses, templates
- Non-technical founders who want "just works" solution
- Businesses prioritizing speed to market over customization

**Limitations**:
- Less established than Stripe/PayPal (newer company, risk consideration)
- Fewer payment method options than larger competitors
- Limited API for advanced custom integrations
- Not ideal for high-volume or enterprise sales

#### Paddle (Best for Global Reach and Scale)

**Why It Fits**:
- Handles tax compliance in 200+ countries automatically
- Supports 40+ payment methods including local options
- Built-in fraud detection and chargeback management
- Localized checkout experiences increase conversion
- Strong track record with established digital product businesses

**Best For**:
- Established businesses selling globally
- Products with international customer base (Europe, Asia, LATAM)
- Teams needing enterprise-grade reliability
- Businesses selling both subscriptions and one-time products

**Limitations**:
- Higher fees (10% vs Lemon Squeezy's 5%)
- Less modern developer experience than Stripe
- Fewer built-in marketing features than Lemon Squeezy
- More complex onboarding process

#### Gumroad (Best for Creator Economy)

**Why It Fits**:
- Designed specifically for creators: artists, writers, educators
- Instant setup with zero technical knowledge required
- Built-in audience building tools (email list, updates)
- Pay-what-you-want pricing and flexible pricing models
- Strong community of creators for cross-promotion

**Best For**:
- Individual creators and solopreneurs
- Digital art, music, writing, small courses
- Businesses wanting direct creator-to-customer relationship
- Products where community and discovery matter

**Limitations**:
- Limited for B2B or professional software sales
- Less robust tax handling than Paddle/Lemon Squeezy
- Basic reporting and analytics
- Not suitable for complex product catalogs or enterprise needs

### Decision Criteria

**Choose Lemon Squeezy if**:
- You want to launch fast with minimal technical setup
- You're a small team or solo founder
- You need affiliate marketing capabilities built-in
- You prefer lower fees and modern tooling

**Choose Paddle if**:
- You have significant international revenue (>30% non-US)
- You need maximum payment method coverage
- You want enterprise-grade reliability and support
- You're selling both digital products and subscriptions

**Choose Gumroad if**:
- You're a creator selling to an audience (not B2B software)
- You value simplicity over advanced features
- You want built-in discovery and community features
- Your products are creative works (art, writing, courses)

**Decision Tree**:
```
What's your primary customer base?
├─ B2B / Professional → Paddle or Lemon Squeezy
└─ Creator audience → Gumroad

For B2B/Professional:
├─ Need to launch this week? → Lemon Squeezy
├─ Significant international revenue? → Paddle
└─ Moderate international, want speed? → Lemon Squeezy
```

---

## Use Case Pattern #3: Professional Services / Consulting

### Business Requirements

**Core Needs**:
- Professional invoicing with custom branding and line items
- Deposit/retainer collection with milestone-based payments
- Payment plans for larger projects (installments)
- ACH/bank transfer support for large B2B transactions
- QuickBooks or accounting software synchronization
- Client portal for viewing invoices and payment history

**Technical Needs**:
- Recurring invoicing for retainer clients
- Automated payment reminders and dunning
- Support for multiple payment methods (card, ACH, wire)
- Integration with time tracking or project management tools
- Tax calculation for services (often location-dependent)

### Provider Fit Analysis

#### Stripe Invoicing (Best for Tech-Savvy Service Providers)

**Why It Fits**:
- Powerful API for programmatic invoice generation
- Supports one-time, recurring, and payment plan invoicing
- ACH Direct Debit for lower-cost B2B transactions
- Hosted invoice pages with automatic payment reminders
- Integration with Stripe Tax for automatic tax calculation
- Webhook events for payment status updates

**Best For**:
- Consultants and agencies with technical capabilities
- Businesses needing custom invoice workflows or CRM integration
- Service providers wanting to build automated billing systems
- Teams processing high-value B2B payments (ACH saves fees)

**Limitations**:
- Requires more setup than all-in-one invoicing tools
- No built-in time tracking or project management
- QuickBooks sync requires third-party tools (Zapier, Synder)
- Less turnkey than Square for non-technical users

#### Square Invoicing (Best for Non-Technical Service Providers)

**Why It Fits**:
- Free invoicing with no monthly fees (only payment processing fees)
- Integrated with Square POS if you also take in-person payments
- Mobile-first: create and send invoices from phone
- Automatic payment reminders and scheduled recurring invoices
- Built-in estimates that convert to invoices
- Simple QuickBooks integration available

**Best For**:
- Solo consultants and small service businesses
- Non-technical users wanting simple, reliable invoicing
- Businesses mixing online invoicing with in-person payments
- Service providers prioritizing ease of use over customization

**Limitations**:
- Limited API for custom integrations
- No ACH Direct Debit (higher fees for large B2B payments)
- Less sophisticated dunning than Stripe
- Basic reporting compared to enterprise solutions

#### PayPal Invoicing (Best for Client Payment Preferences)

**Why It Fits**:
- Ubiquitous: clients often already have PayPal accounts
- Simple invoicing with professional templates
- Supports payment plans and deposits
- Mobile app for on-the-go invoice management
- Integration with PayPal balance for immediate fund access
- Free invoicing with standard PayPal transaction fees

**Best For**:
- Service providers with clients who prefer PayPal
- International consultants (PayPal widely accepted globally)
- Freelancers wanting instant access to funds
- Businesses already using PayPal for other purposes

**Limitations**:
- Less modern UX than Stripe or Square
- Limited customization of invoice appearance
- Funds held in PayPal account (requires transfer to bank)
- QuickBooks sync less robust than dedicated solutions

### Decision Criteria

**Choose Stripe Invoicing if**:
- You have technical resources to integrate APIs
- You need ACH for large B2B payments (saves 2%+ in fees)
- You want to automate invoice generation from your CRM/PM tools
- You're building a scalable service business with recurring clients

**Choose Square Invoicing if**:
- You want a free, simple solution with no monthly fees
- You're a solo consultant or small team
- You also take in-person payments (Square ecosystem)
- You prioritize ease of use and mobile access

**Choose PayPal Invoicing if**:
- Your clients specifically request PayPal as payment option
- You work internationally and need broad payment acceptance
- You want immediate access to funds via PayPal balance
- You prefer a familiar, established platform

**Decision Tree**:
```
Do you have technical resources for integration?
├─ YES: Are most payments >$5,000?
│   ├─ YES → Stripe (use ACH to save fees)
│   └─ NO → Stripe or Square (based on other needs)
└─ NO: Do clients prefer PayPal?
    ├─ YES → PayPal Invoicing
    └─ NO → Square Invoicing
```

**Special Consideration - Large B2B Payments**:
For consulting projects >$10,000, ACH saves significant fees:
- $10,000 via credit card: $290 in fees (2.9%)
- $10,000 via ACH: $50 in fees (0.5% capped)
- **Savings**: $240 per transaction → Choose Stripe for ACH Direct Debit

---

## Use Case Pattern #4: Marketplaces / Platforms

### Business Requirements

**Core Needs**:
- Payment splitting between platform and sellers/service providers
- Escrow or hold periods for transaction safety
- Multi-party payouts with flexible split logic
- KYC/KYB compliance for sellers (identity verification)
- Platform fee collection (percentage or fixed)
- Seller dashboard for earnings and payout management

**Technical Needs**:
- Connected accounts or seller onboarding API
- Programmable payment splits (dynamic percentages)
- Payout scheduling and management
- Compliance automation (1099 generation, tax reporting)
- Dispute and chargeback handling across parties
- Refund logic that reverses splits appropriately

### Provider Fit Analysis

#### Stripe Connect (Best for Flexibility and Customization)

**Why It Fits**:
- Three integration models: Express, Custom, Standard (choose control level)
- Sophisticated payment splitting with application fees or transfers
- Flexible payout timing: instant, daily, weekly, monthly, or on-demand
- Robust KYC/verification with customizable requirements
- Treasury API for embedded banking (balance accounts for sellers)
- Advanced features: multi-party authentication, seller dashboards

**Best For**:
- Tech companies building custom marketplace experiences
- Platforms needing complex split logic (tiered fees, bonuses)
- Businesses wanting white-label seller onboarding
- Marketplaces with unique compliance or payout requirements

**Account Types**:
- **Express**: Stripe-hosted onboarding, fastest setup, some branding
- **Custom**: Fully white-labeled, complete control, most development
- **Standard**: Sellers see Stripe branding, minimal integration

**Limitations**:
- Significant development effort for Custom accounts
- Complex compliance burden (platform responsibility)
- Requires technical team to implement and maintain
- Debugging multi-party payment flows can be challenging

#### PayPal Commerce Platform (Best for Seller Trust)

**Why It Fits**:
- Sellers and buyers already trust PayPal brand
- Simplified onboarding: sellers use existing PayPal accounts
- PayPal handles compliance and risk management
- Lower friction: buyers can check out with saved PayPal credentials
- Global reach with local payment methods in 200+ markets

**Best For**:
- Marketplaces where seller trust is critical
- International platforms with sellers in multiple countries
- Businesses wanting to minimize compliance overhead
- Platforms targeting demographics comfortable with PayPal

**Limitations**:
- Less flexibility than Stripe Connect for custom split logic
- Seller experience tied to PayPal branding
- Limited control over payout timing and seller experience
- API and developer experience less modern than Stripe

#### Adyen for Platforms (Best for Enterprise Scale)

**Why It Fits**:
- Built for high-volume, global marketplaces
- Single integration for 200+ countries and payment methods
- Advanced fraud detection and risk management
- Sophisticated split payment logic with multi-level fees
- White-label solution with complete control
- Dedicated support and compliance guidance

**Best For**:
- Established marketplaces with significant transaction volume
- Enterprise platforms with complex international operations
- Businesses needing custom payment method integrations
- Companies prioritizing payment optimization and authorization rates

**Limitations**:
- Requires significant volume (often >$50M annual processing)
- Higher complexity and longer onboarding process
- More expensive than Stripe for smaller platforms
- Requires dedicated technical resources

### Decision Criteria

**Choose Stripe Connect if**:
- You're building a custom marketplace with unique requirements
- You have engineering resources for integration and maintenance
- You need flexible split logic or dynamic fee structures
- You want to innovate on seller experience and embedded finance

**Choose PayPal Commerce Platform if**:
- Seller trust and brand recognition are critical
- You want to minimize platform compliance burden
- Your sellers are international and prefer PayPal
- You prioritize faster go-to-market over customization

**Choose Adyen for Platforms if**:
- You're processing >$50M annually or expect to soon
- You need maximum payment method coverage globally
- You require white-label solution with enterprise support
- You have dedicated technical and compliance teams

**Decision Tree**:
```
What's your transaction volume?
├─ <$10M annually: Stripe Connect or PayPal
│   ├─ Need custom seller experience? → Stripe Connect
│   └─ Want simplicity and trust? → PayPal
└─ >$50M annually: Stripe Connect or Adyen
    ├─ Maximum flexibility? → Stripe Connect
    └─ Enterprise scale/support? → Adyen
```

**Integration Complexity vs Control Spectrum**:
```
Low Control                              High Control
Low Complexity                        High Complexity
    │                                      │
    PayPal ──── Stripe Express ──── Stripe Custom ──── Adyen
```

---

## Use Case Pattern #5: Usage-Based / Metered Billing

### Business Requirements

**Core Needs**:
- Precise metering of API calls, storage, compute, or other resources
- Tiered or graduated pricing structures
- Mid-month billing or flexible billing cycles
- Transparent invoices showing usage breakdown
- Usage alerts and spending caps for customers
- Support for minimum commitments and overage charges

**Technical Needs**:
- Real-time or near-real-time usage reporting to billing system
- Idempotent usage event ingestion (no double-charging)
- Aggregation rules for different usage dimensions
- Proration when customers upgrade/downgrade mid-cycle
- API for customers to view current usage and projected costs
- Integration with internal metering infrastructure

### Provider Fit Analysis

#### Stripe Billing with Metered Usage (Best for Modern SaaS)

**Why It Fits**:
- Native usage metering with real-time reporting API
- Flexible aggregation: sum, max, last value during period
- Graduated or volume-based tiered pricing
- Customer portal shows current usage and projected costs
- Idempotent usage reporting prevents double-charging
- Support for multiple metering dimensions per subscription

**Best For**:
- API-first businesses (Twilio, SendGrid model)
- Companies with precise metering requirements
- Businesses wanting transparent usage-based pricing
- Teams comfortable with webhook-based architecture

**Capabilities**:
- Report usage via API: `meter_events.create()`
- Aggregation functions: sum, max, most_recent
- Tiers: graduated (per unit in tier) or volume (all units at tier rate)
- Minimum commitments via subscription base fee
- Usage alerts via webhooks when thresholds crossed

**Limitations**:
- Requires careful usage event design and testing
- Complex billing logic requires significant integration work
- No built-in data pipeline from infrastructure to billing
- Must build own usage dashboards for customers

#### Recurly (Best for Legacy Compatibility)

**Why It Fits**:
- Established usage billing for traditional SaaS
- Hybrid pricing: subscriptions + usage + one-time charges
- Usage-based add-ons and overage tracking
- Revenue recognition aligned with usage delivery
- Integration with legacy accounting systems

**Best For**:
- Companies migrating from older billing systems
- Businesses with hybrid pricing models
- Teams requiring sophisticated revenue recognition
- Enterprises needing multi-entity billing

**Limitations**:
- Less modern API and developer experience than Stripe
- Higher cost structure for mid-market
- Fewer payment method options
- Not ideal for startups or greenfield projects

#### Custom Solution (Best for Highly Complex Needs)

**Why It Fits**:
- Complete control over metering, aggregation, and billing logic
- Optimize for specific business model (credits, rollover, complex tiers)
- Integrate deeply with internal systems and data pipelines
- Innovate on usage presentation and customer experience

**Best For**:
- Large enterprises with unique billing requirements
- Companies where billing is competitive advantage
- Businesses with complex multi-dimensional usage models
- Teams with significant engineering resources

**Implementation Considerations**:
- Metering service: Kafka + time-series database for usage events
- Billing engine: Cron jobs to aggregate usage and generate invoices
- Payment processing: Stripe/Braintree for payment collection only
- Customer portal: Custom dashboards for usage visibility

**Limitations**:
- Significant upfront and ongoing engineering investment
- Must handle PCI compliance if storing payment methods
- Tax calculation complexity (often integrate Avalara/TaxJar)
- Opportunity cost: engineering time vs product development

### Decision Criteria

**Choose Stripe Billing if**:
- Your usage model fits standard aggregations (sum, max, most recent)
- You need transparent, real-time usage reporting
- You want to leverage Stripe's payment infrastructure
- You have engineering resources but want to minimize billing code

**Choose Recurly if**:
- You're migrating from an older billing system
- You need sophisticated revenue recognition automation
- Your pricing combines subscriptions, usage, and one-time charges
- You require multi-entity or multi-currency billing

**Choose Custom Solution if**:
- Your usage model is unique and competitive differentiator
- Standard billing platforms can't support your pricing logic
- You process massive volume where per-event costs matter
- You have dedicated engineering team for billing infrastructure

**Decision Tree**:
```
How complex is your usage model?
├─ Standard (API calls, storage, compute): Stripe Billing
├─ Hybrid (subscription + usage + one-time): Stripe or Recurly
│   ├─ Modern API-first → Stripe Billing
│   └─ Legacy integrations → Recurly
└─ Highly custom (credits, rollover, complex tiers):
    ├─ Early stage → Stripe + custom logic
    └─ Established with resources → Custom solution
```

**Metering Precision Requirements**:
- **Real-time visibility**: Stripe Billing (customer portal, API)
- **Batch daily/weekly**: Recurly or custom batch jobs
- **Complex aggregations**: Custom solution with OLAP database

---

## Summary Decision Matrix

### Quick Reference: Use Case to Provider Mapping

| Use Case | Primary Need | Best Fit | Alternative |
|----------|--------------|----------|-------------|
| **B2B SaaS Subscriptions** | Flexible billing logic | Stripe Billing | Paddle (if tax burden), Chargebee (if complex) |
| **Digital Product Sales** | Global tax + instant delivery | Lemon Squeezy | Paddle (if established), Gumroad (if creator) |
| **Professional Services** | Invoicing + large payments | Stripe (ACH) | Square (simplicity), PayPal (preference) |
| **Marketplaces** | Payment splits + compliance | Stripe Connect | PayPal (trust), Adyen (enterprise) |
| **Usage-Based Billing** | Precise metering | Stripe Billing | Recurly (legacy), Custom (complex) |

### Key Decision Factors Across Use Cases

**Technical Resources**:
- High technical capacity → Stripe (all use cases)
- Low technical capacity → Paddle, Lemon Squeezy, Square, PayPal

**International Revenue**:
- Significant (>30%) → Paddle, Stripe with Tax, Adyen
- Minimal (<10%) → Any provider, prioritize other factors

**Customization Needs**:
- High customization → Stripe, Adyen, Custom
- Low customization → Paddle, Lemon Squeezy, Gumroad, Square

**Complexity Tolerance**:
- Simple/fast launch → Lemon Squeezy, Gumroad, Square, PayPal
- Complex requirements → Stripe, Chargebee, Adyen, Custom

**Scale and Volume**:
- <$1M annual → Simple solutions (Lemon Squeezy, Square, Gumroad)
- $1M-$50M annual → Stripe, Paddle, Chargebee
- >$50M annual → Stripe, Adyen, Custom solutions

---

## If-Then Decision Logic

### For SaaS Founders

**If** non-technical founder + digital products + global sales
**Then** → Lemon Squeezy or Paddle

**If** technical team + B2B SaaS + complex subscriptions
**Then** → Stripe Billing or Chargebee

**If** developer tool + usage-based pricing
**Then** → Stripe Billing with metered usage

### For Service Providers

**If** solo consultant + simple invoicing
**Then** → Square Invoicing (free)

**If** agency + large B2B payments (>$5K)
**Then** → Stripe Invoicing (use ACH)

**If** international clients + PayPal preference
**Then** → PayPal Invoicing

### For Marketplace Builders

**If** early-stage + need custom seller experience
**Then** → Stripe Connect (Express accounts)

**If** established + international sellers + trust critical
**Then** → PayPal Commerce Platform

**If** enterprise scale + >$50M volume
**Then** → Adyen for Platforms

### For Product Sellers

**If** creator + digital art/courses + audience building
**Then** → Gumroad

**If** software product + global customers + non-technical
**Then** → Lemon Squeezy

**If** established business + international + enterprise features
**Then** → Paddle

---

## Anti-Patterns: Common Mismatches

### Don't Use Stripe If...
- You have no technical resources and need turnkey solution
- Tax compliance burden is your primary concern (use Paddle/Lemon Squeezy)
- You're a creator selling to audience (Gumroad is better fit)

### Don't Use Paddle If...
- You need highly customized billing logic (Stripe is more flexible)
- Your subscriptions are simple and US-only (paying for unused capabilities)
- 10% fees are problematic for low-margin products

### Don't Use Gumroad If...
- You're selling B2B software or professional services
- You need sophisticated subscription management
- You require detailed analytics and reporting

### Don't Use Stripe Connect If...
- You lack engineering resources for integration
- Your marketplace model is standard (PayPal might be simpler)
- You want to minimize platform compliance burden

### Don't Build Custom If...
- Your billing model fits existing platforms (not a differentiator)
- You're early-stage without product-market fit
- Engineering resources are better spent on core product

---

## Next Steps After Choosing a Provider

### Implementation Checklist

1. **Proof of Concept**:
   - Set up test account and sandbox environment
   - Implement one core workflow end-to-end
   - Validate assumptions about capabilities and limitations

2. **Integration Planning**:
   - Map business requirements to provider features
   - Design webhook handling and event processing
   - Plan for edge cases (refunds, failures, disputes)

3. **Testing Strategy**:
   - Test with real payment methods in test mode
   - Simulate edge cases: failed payments, chargebacks, refunds
   - Load test if expecting high volume

4. **Compliance Review**:
   - Understand your responsibilities (vs provider's)
   - Implement required KYC/AML if applicable
   - Plan for tax reporting and 1099 generation

5. **Customer Experience**:
   - Design clear, transparent pricing pages
   - Provide self-service tools (portal, invoice access)
   - Plan for payment failure communication and recovery

6. **Monitoring and Alerts**:
   - Set up alerts for failed payments, disputes, anomalies
   - Monitor authorization rates and conversion funnel
   - Track provider uptime and incident communications

---

*This analysis is part of the MPSE (Multi-Phase Systematic Evaluation) discovery methodology for experiment 3.001: Payment Processing Services.*
