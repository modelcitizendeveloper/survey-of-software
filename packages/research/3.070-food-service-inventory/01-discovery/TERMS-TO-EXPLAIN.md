# Terms to Explain - Food Service Inventory Management

**Purpose**: Track technical terms, jargon, and concepts encountered during S1-S4 research that need explanation in the DOMAIN_EXPLAINER.md (created AFTER S2-S4 completion per MPSE methodology).

**Status**: Tracked during S1 (Nov 30, 2025), will expand during S2-S4

---

## Inventory Management Concepts

**Recipe Explosion / BOM (Bill of Materials)**
- Term appears in: Odoo, ERPNext+URY, MarketMan
- Context: "Menu item → ingredient list with quantities" (e.g., burger → bun, patty, lettuce, tomato, condiments)
- Why it matters: Automatic ingredient deduction when menu item sold (real-time inventory tracking)
- Needs explanation: How BOM differs from simple recipe, why "explosion" terminology

**COGS (Cost of Goods Sold) Automation**
- Term appears in: All platforms
- Context: "Ingredient costs → menu item cost → daily/monthly COGS for accounting"
- Why it matters: Real-time profitability tracking, P&L integration
- Needs explanation: Manual COGS calculation vs automated (POS sales × recipe cost), accounting integration flow

**Variance Analysis (Theoretical vs. Actual Usage)**
- Term appears in: MarketMan, xtraCHEF, Craftable, WISK
- Context: "Expected usage (sales × recipe quantities) vs actual inventory depletion"
- Why it matters: Identifies waste, theft, overpouring, portioning errors
- Needs explanation: How to interpret variance (2-4% acceptable, >5% investigate), common causes

**Par Levels and Automated Reordering**
- Term appears in: All platforms
- Context: "Minimum stock quantity triggers automatic purchase order generation"
- Why it matters: Prevents stockouts, reduces manual ordering workload
- Needs explanation: How to set par levels (lead time + safety stock), seasonal adjustment

**Shrink (Bar/Restaurant Context)**
- Term appears in: WISK, Craftable
- Context: "Inventory loss from theft, overpouring, spillage, spoilage" (bars: 5-15% typical)
- Why it matters: Major profit leakage, variance analysis catches shrink
- Needs explanation: Shrink vs waste (shrink = loss, waste = discarded), industry benchmarks

**Overpouring**
- Term appears in: WISK, Craftable (bar-specific)
- Context: "Bartender pours 1.75 oz instead of 1.5 oz spec (17% loss per drink)"
- Why it matters: Cumulative overpouring = 5-10% bar revenue loss
- Needs explanation: How hardware scales detect overpouring (partial bottle tracking), training vs technology solutions

---

## Invoice Processing & Procurement

**Invoice Digitization / OCR Processing**
- Term appears in: xtraCHEF, MarketMan
- Context: "Photograph invoice → AI extracts line items, prices, totals → auto-imports to system"
- Why it matters: Saves 5-10 min/invoice manual data entry (50 invoices/month = 6 hours)
- Needs explanation: OCR accuracy (95%+), validation workflow, error handling

**3-Way Match (PO → Receipt → Invoice)**
- Term appears in: Craftable, Odoo, ERPNext
- Context: "Purchase Order, Delivery Receipt, Invoice must match before payment approved"
- Why it matters: Prevents overpayment, catches delivery discrepancies, fraud detection
- Needs explanation: Matching rules (exact vs tolerance), variance thresholds, approval workflows

**EDI (Electronic Data Interchange) for Suppliers**
- Term appears in: MarketMan, Craftable
- Context: "Automatic supplier catalog sync (prices, product codes, availability)"
- Why it matters: Real-time pricing updates, automatic PO transmission, faster ordering
- Needs explanation: EDI vs API integration, setup complexity, supplier adoption rates

---

## Multi-Location & Scalability

**Multi-Location Centralized Management**
- Term appears in: MarketMan (HQ account), Odoo, ERPNext+URY, Craftable
- Context: "Single dashboard manages inventory across 3-10+ locations"
- Why it matters: Standardized recipes, bulk ordering, cross-location reporting
- Needs explanation: Centralized vs federated models, location-specific customization, data sync challenges

**Cross-Location Transfer Tracking**
- Term appears in: Odoo, ERPNext (warehouse transfers)
- Context: "Move ingredients from Location A warehouse to Location B, track in-transit inventory"
- Why it matters: Prevents double-counting, enables centralized purchasing with distribution
- Needs explanation: Transfer workflows, in-transit inventory accounting, loss tracking

---

## Perishable Inventory Specific

**Batch Tracking with Expiry Dates**
- Term appears in: Odoo, ERPNext
- Context: "Group items by delivery date, track expiry, prevent expired stock from being used"
- Why it matters: Food safety compliance, waste reduction (FIFO rotation)
- Needs explanation: Batch ID assignment, FIFO vs LIFO vs FEFO (First Expired First Out), expiry alerting

**FIFO (First In First Out) Rotation**
- Term appears in: Industry standard (all platforms should support)
- Context: "Use oldest inventory first to minimize spoilage"
- Why it matters: Perishable inventory management, waste reduction
- Needs explanation: Manual FIFO (physical rotation) vs automated (system tracks batch ages), audit enforcement

---

## Integration & Ecosystem

**POS Integration (Point of Sale)**
- Term appears in: All platforms
- Context: "Sales transactions from POS → automatic inventory depletion"
- Why it matters: Real-time COGS, no manual sales entry, accurate variance analysis
- Needs explanation: Integration depth (real-time vs batch sync, menu item mapping, modifier tracking)

**Kitchen Display System (KDS) Integration**
- Term appears in: ERPNext+URY (URY-specific feature)
- Context: "Kitchen screens show orders in real-time, track prep status"
- Why it matters: Coordinates kitchen workflow, integrates with inventory (86 items = mark out of stock)
- Needs explanation: KDS vs POS (KDS = kitchen-facing, POS = customer-facing), order routing, status tracking

---

## Waste Management & Sustainability

**Waste Tracking Categories**
- Term appears in: MarketMan, BlueCart
- Context: "Spoilage vs over-portioning vs theft vs damaged goods"
- Why it matters: Root cause analysis (spoilage = ordering issue, over-portioning = training issue)
- Needs explanation: How to categorize waste, waste entry workflows, reporting for sustainability goals

**Food Waste Percentage (Industry Benchmarks)**
- Term appears in: Industry research (ReFED, Supy, CrunchTime)
- Context: "4-10% of food purchases never reach customer (typical restaurant)"
- Why it matters: ROI calculation baseline, audit current state before platform selection
- Needs explanation: How to measure (physical waste audit vs variance analysis), industry norms by restaurant type

---

## Platform-Specific Terminology

**Toast Ecosystem (xtraCHEF Context)**
- Context: "Toast POS + xtraCHEF inventory = integrated front-of-house + back-of-house"
- Why it matters: Seamless data flow, but creates switching costs (vendor lock-in)
- Needs explanation: Toast hardware lock-in, software integrations, migration difficulty

**Bluetooth Scales (WISK Hardware)**
- Context: "Portable scales weigh partial bottles/kegs, sync weight to inventory app via Bluetooth"
- Why it matters: Eliminates estimation errors (visual vs weight), enables 99.7% accuracy
- Needs explanation: Scale cost, battery life, calibration, weight-to-volume conversion

**URY (ERPNext Restaurant Extension)**
- Context: "Open-source restaurant management module built on ERPNext ERP"
- Why it matters: Restaurant-specific workflows (POS, KDS, F&B inventory) vs generic ERP
- Needs explanation: URY project maturity (10 months production, 10+ outlets), community size, longevity risk

---

## Strategic Concepts (S4)

**Vendor Lock-In (SaaS Context)**
- Context: "Data export limitations, proprietary formats, integration dependencies"
- Why it matters: Migration cost increases over time, vendor pricing power
- Needs explanation: Lock-in mitigation (data export APIs, standard formats), switching cost estimation

**Acquisition Risk (Vendor Viability)**
- Context: "Probability platform gets acquired by larger player (e.g., Toast buying xtraCHEF in 2021)"
- Why it matters: Platform roadmap changes, pricing increases, feature deprecation
- Needs explanation: Signals (funding history, revenue scale, strategic buyers), mitigation strategies

**Open-Source Sustainability (Odoo, ERPNext)**
- Context: "Community Edition vs Enterprise Edition, maintainer incentives, longevity"
- Why it matters: Will platform exist in 5-10 years? Will bugs get fixed?
- Needs explanation: Open-source business models, community health metrics, fork risks

---

## AI & Automation (Emerging)

**Predictive Ordering AI (BlueCart 2025 Feature)**
- Context: "Historical usage + seasonality → automatically recommend order quantities"
- Why it matters: Reduces over-ordering waste, prevents stockouts
- Needs explanation: How AI models work (time series forecasting), data requirements (12+ months history), accuracy validation

**AI-Powered Recipe Creation (MarketMan Feature)**
- Context: "Upload ingredient list screenshot → AI matches to inventory, creates recipe"
- Why it matters: Saves 30-60 min manual recipe entry
- Needs explanation: OCR + ingredient matching, error rates, verification workflow

---

**Total Terms Tracked**: 29 terms/concepts
**Coverage**: S1 research (Nov 30, 2025)
**Next**: Expand during S2-S4 research, then create DOMAIN_EXPLAINER.md

**NOTE**: Domain explainer will be created AFTER S2-S4 completion per MPSE methodology guidelines. This file serves as tracking only.
