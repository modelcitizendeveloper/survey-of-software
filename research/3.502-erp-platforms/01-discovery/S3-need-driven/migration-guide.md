# S3 Need-Driven: Migration Guide

**Date**: November 2, 2025
**Purpose**: Step-by-step playbooks for migrating from accounting software to ERP
**Common Migrations**: QuickBooks → ERP, Xero → ERP, Spreadsheets → ERP

---

## I. Migration Planning Framework

### Pre-Migration Checklist

**3-6 Months Before Go-Live**:

1. **Business Requirements**
   - [ ] Document current pain points with existing system
   - [ ] Define must-have features in new ERP
   - [ ] Map business processes (order-to-cash, procure-to-pay, etc.)
   - [ ] Identify custom workflows and integrations needed

2. **Data Assessment**
   - [ ] Audit data quality (customers, vendors, items, transactions)
   - [ ] Clean up duplicates and obsolete records
   - [ ] Determine historical data cutoff (1 year? 3 years? 7 years?)
   - [ ] Document chart of accounts structure

3. **Team Preparation**
   - [ ] Identify ERP project champion (executive sponsor)
   - [ ] Form implementation team (accounting, operations, IT, users)
   - [ ] Budget for training (10-20% of implementation cost)
   - [ ] Plan for temporary help during cutover

4. **Vendor Selection**
   - [ ] Shortlist 2-3 ERP platforms (use S1 Recommendation)
   - [ ] Request demos focused on your workflows
   - [ ] Check references (3-5 companies in your industry)
   - [ ] Negotiate pricing and contract terms

5. **Implementation Partner**
   - [ ] Select experienced partner (ask for case studies)
   - [ ] Clarify scope (fixed-price vs time & materials)
   - [ ] Define success criteria and acceptance testing
   - [ ] Establish communication cadence (weekly standups)

---

## II. Migration Playbook: QuickBooks → ERP

### Scenario: 50-Person Manufacturing Company

**Current State**: QuickBooks Desktop Enterprise, 3 users, spreadsheets for inventory/manufacturing
**Target State**: Dynamics 365 BC Premium, 25 users, integrated financials + manufacturing
**Timeline**: 4-6 months
**Budget**: $75K ($30K implementation + $45K first year software)

---

### Phase 1: Discovery & Design (Weeks 1-4)

**Week 1-2: Requirements Gathering**
- Workshop #1: Chart of accounts mapping (QB → D365 BC)
- Workshop #2: Inventory management (items, BOMs, locations)
- Workshop #3: Manufacturing workflows (work orders, routing)
- Workshop #4: Order processing (sales orders, invoicing, shipping)

**Deliverables**:
- Requirements document (20-30 pages)
- Process flow diagrams (current vs future state)
- Data migration plan
- Integration requirements (e.g., Shopify, UPS)

**Week 3-4: System Configuration**
- Configure chart of accounts in D365 BC
- Set up item master (inventory items, BOMs)
- Configure manufacturing (work centers, routing)
- Set up customer/vendor masters
- Configure tax settings (Avalara integration if needed)

**Deliverables**:
- Configured D365 BC sandbox environment
- Configuration workbook (settings documentation)

---

### Phase 2: Data Migration (Weeks 5-8)

**Data Migration Priorities**:

**Must Migrate** (essential for operations):
- Chart of accounts (GL structure)
- Open balances (A/R, A/P as of cutover date)
- Customer master (active customers only)
- Vendor master (active vendors only)
- Item master (active SKUs only)
- Open sales orders
- Open purchase orders
- Current inventory balances

**Nice to Have** (historical data):
- 1-2 years of transaction history
- Closed invoices (for reference)
- Historical cost data

**Don't Migrate** (archive in QB):
- Old transactions (>2 years)
- Inactive customers/vendors
- Obsolete inventory items

**Data Migration Process**:

1. **Extract from QuickBooks**:
   - Export to Excel/CSV (Reports → Excel export)
   - Key reports: Trial balance, customer list, vendor list, item list, open invoices, open bills

2. **Transform Data**:
   - Clean up duplicates and errors
   - Map QB accounts → D365 BC accounts
   - Standardize formats (dates, phone numbers, addresses)
   - Validate data quality (no blanks, correct data types)

3. **Load into D365 BC**:
   - Use Data Management Framework (Excel import)
   - Import in sequence:
     1. Chart of accounts
     2. Customers/vendors
     3. Items
     4. Open A/R invoices
     5. Open A/P bills
     6. Sales orders/purchase orders
     7. Inventory balances
   - Validate each import (run reports, compare to QB)

**Week 5-6: First Data Migration (Test)**
- Extract data from QuickBooks
- Transform and load into D365 BC sandbox
- Identify data issues and cleanup needed

**Week 7-8: Second Data Migration (Dress Rehearsal)**
- Re-extract data (more recent)
- Apply lessons learned from first migration
- Full validation and reconciliation

**Deliverables**:
- Data migration scripts/templates
- Reconciliation report (QB vs D365 BC)

---

### Phase 3: Testing & Training (Weeks 9-12)

**Week 9-10: User Acceptance Testing (UAT)**

**Test Scenarios** (end-to-end workflows):
1. **Quote-to-Cash**: Create quote → Convert to sales order → Pick/pack/ship → Invoice → Receive payment
2. **Procure-to-Pay**: Create PO → Receive goods → Enter bill → Pay vendor
3. **Manufacturing**: Create work order → Issue materials → Complete production → Receive into inventory
4. **Month-End Close**: Run GL reports → Bank reconciliation → Financial statements
5. **Integrations**: Test Shopify orders sync, UPS shipping labels, etc.

**UAT Checklist**:
- [ ] All test scenarios pass
- [ ] Reports match expectations
- [ ] Performance acceptable (<3 sec for common tasks)
- [ ] Integrations working
- [ ] User feedback incorporated

**Week 11-12: Training**

**Training Plan**:
- **Session 1** (Executives, 2 hours): Dashboard, financial reports, KPIs
- **Session 2** (Accounting, 8 hours): G/L, A/R, A/P, bank rec, month-end close
- **Session 3** (Operations, 8 hours): Sales orders, purchase orders, inventory, shipping
- **Session 4** (Manufacturing, 8 hours): Work orders, BOMs, production, costing
- **Session 5** (All Users, 2 hours): Navigation, search, basic tasks

**Training Materials**:
- Video tutorials (15-20 short videos, 5-10 min each)
- Quick reference guides (1-page cheat sheets)
- Process documentation (step-by-step workflows)

**Deliverables**:
- UAT sign-off document
- Training materials
- Trained user base (certification optional)

---

### Phase 4: Cutover & Go-Live (Weeks 13-16)

**Cutover Strategy**: "Big Bang" (recommended for SMB)

**Alternative**: Parallel run (more costly, confusing)

**Cutover Weekend Plan** (Friday 5pm → Monday 8am):

**Friday 5pm - 11pm**:
- Close QuickBooks (last transactions posted)
- Run final reports from QB (backup everything)
- Extract final data (open balances, open orders)

**Saturday 8am - 8pm**:
- Load final data into D365 BC production
- Reconcile all balances (A/R, A/P, inventory, G/L)
- Test integrations (Shopify, payment processor, shipping)
- Final smoke test (create test sales order, invoice)

**Sunday 8am - 8pm**:
- Train super users on production system
- Create first week's production work orders
- Set up first week's sales orders
- Final reconciliation check

**Monday 8am**: **Go-Live**
- All users switch to D365 BC
- Help desk available (implementation partner + internal team)
- QuickBooks in read-only mode (reference only)

**Cutover Checklist**:
- [ ] QuickBooks closed and backed up
- [ ] Final data migrated and reconciled
- [ ] All integrations tested and working
- [ ] Super users trained on production
- [ ] Help desk staffed and ready
- [ ] Rollback plan documented (if catastrophic failure)

---

### Phase 5: Post-Go-Live Support (Weeks 17-20)

**Week 1-2 Post-Go-Live (Hypercare)**:
- Daily check-ins with users
- Resolve issues immediately (partner help desk)
- Monitor system performance
- Track and fix data issues
- Document workarounds and process changes

**Week 3-4 Post-Go-Live (Stabilization)**:
- Weekly check-ins with users
- First month-end close in new system
- Optimize workflows based on feedback
- Additional training as needed
- Document lessons learned

**Success Metrics**:
- [ ] All users able to complete daily tasks
- [ ] First month-end close completed successfully
- [ ] Financial reports accurate and reconciled
- [ ] No critical issues outstanding
- [ ] User satisfaction >7/10

**Deliverables**:
- Go-live checklist (signed off)
- Issue log (all issues resolved or documented)
- Lessons learned document
- Final reconciliation (QB vs D365 BC)

---

## III. Migration Cost Breakdown

### QuickBooks → Dynamics 365 BC (50-person company)

| Cost Component | Amount | Notes |
|----------------|--------|-------|
| **Software (Year 1)** | $35K | 25 users × $110/mo Premium |
| **Implementation** | $30K | Partner services (3-4 months) |
| **Data Migration** | Included | Part of implementation |
| **Training** | $5K | Video tutorials + live sessions |
| **Integrations** | $5K | Shopify, UPS, payment processor |
| **Contingency (10%)** | $7.5K | Unexpected issues |
| **TOTAL FIRST YEAR** | **$82.5K** | |

**Ongoing (Year 2+)**: $35K/year (software only)

---

## IV. Common Migration Pitfalls

### Pitfall #1: Underestimating Data Cleanup

**Problem**: "Our QuickBooks data is messy"
- 500 duplicate customer records
- Items with no descriptions
- Transactions with wrong accounts

**Solution**: Budget 20-40 hours for data cleanup **before** migration
- Hire temp bookkeeper to clean data
- Archive old/obsolete records
- Standardize naming conventions

**Cost**: $2K-$5K (well worth it)

---

### Pitfall #2: Not Closing QuickBooks

**Problem**: Keep using QuickBooks after go-live
- Dual entry (QB + ERP) creates confusion
- Data diverges immediately
- Defeats purpose of migration

**Solution**: **Close QuickBooks on cutover date**
- Make it read-only (for historical reference)
- Force all users to new system
- Burn the boats - no going back

---

### Pitfall #3: Insufficient Training

**Problem**: Users don't know how to use new ERP
- Productivity drops 40-60% for 2-4 weeks
- User frustration and resistance
- Workarounds emerge (spreadsheets, emails)

**Solution**: Over-invest in training
- 8+ hours hands-on training per user
- Video library for reference
- Super users in each department
- Help desk for first 2 weeks

**Cost**: $5K-$15K (critical investment)

---

### Pitfall #4: Skipping UAT

**Problem**: Go live without thorough testing
- Discover critical issues on Day 1
- Scramble to fix in production
- Users lose confidence

**Solution**: Full UAT with real users
- Test every workflow end-to-end
- Use real data (not dummy data)
- Get user sign-off before go-live

**Time**: 2-4 weeks (don't rush)

---

### Pitfall #5: Big Bang Without Backup Plan

**Problem**: Go-live fails catastrophically
- Data didn't migrate correctly
- Critical integration broken
- System performance unacceptable

**Solution**: Have rollback plan
- Keep QuickBooks data available
- Document rollback procedures
- Test rollback during dress rehearsal
- Accept that rollback = restart migration

**Note**: Rollback is rare (<5% of migrations) but plan for it

---

## V. Migration Playbook: Xero → ERP

### Key Differences from QuickBooks Migration

**Xero is Cloud-Native** (easier data export):
- API access for automated data extraction
- Real-time data vs QB backup files
- Better data quality (modern software)

**Common Xero → ERP Paths**:
1. **Xero → NetSuite** (fast-growing SaaS companies, $10M+ revenue)
2. **Xero → Dynamics 365 BC** (Microsoft ecosystem, <$50M revenue)
3. **Xero → Odoo** (budget-conscious, technical teams)

**Migration Timeline**: 3-5 months (similar to QuickBooks)

**Key Advantage**: Xero users are already comfortable with cloud software (shorter learning curve)

---

## VI. Migration Playbook: Spreadsheets → ERP

### Scenario: 25-Person Distribution Company

**Current State**: Excel for everything (inventory, orders, invoicing), QuickBooks for basic accounting
**Target State**: Odoo Enterprise (budget-conscious) or Dynamics 365 BC
**Timeline**: 4-8 months
**Challenge**: **No structured data** (highest migration risk)

**Critical Success Factor**: Process design **before** data migration

**Steps**:
1. **Document spreadsheet logic** (formulas, macros, workflows)
2. **Design ERP processes** (how should it work in ERP?)
3. **Extract data from spreadsheets** (one-time snapshot)
4. **Transform to ERP format** (heavy cleanup required)
5. **Load into ERP** (expect multiple iterations)
6. **Extensive UAT** (workflows will change significantly)

**Risk**: 40-50% of spreadsheet migrations fail due to poor planning

**Success Rate**:
- With experienced partner: 70-80% success
- DIY migration: 30-40% success

**Recommendation**: Hire experienced implementation partner (worth the cost)

---

## VII. Migration Timeline Comparison

| Migration Path | Timeline | Complexity | Success Rate | Notes |
|----------------|----------|------------|--------------|-------|
| **QuickBooks → Dynamics BC** | 3-6 months | ⭐⭐⭐ Medium | 80-90% | Most common, well-documented |
| **QuickBooks → NetSuite** | 4-8 months | ⭐⭐⭐⭐ High | 70-80% | More complex, expensive |
| **QuickBooks → Odoo** | 3-5 months | ⭐⭐⭐ Medium | 70-80% | Partner quality critical |
| **Xero → ERP** | 3-5 months | ⭐⭐ Low-Medium | 85-95% | Cloud → cloud easier |
| **Spreadsheets → ERP** | 6-12 months | ⭐⭐⭐⭐⭐ Very High | 50-60% | Highest risk, needs expert help |
| **Legacy ERP → Modern ERP** | 6-12 months | ⭐⭐⭐⭐ High | 60-70% | Complex, many integrations |

---

## VIII. Migration Budget Rules of Thumb

### Implementation Cost as % of Annual Software

| ERP Platform | Implementation as % of Annual Software | Example |
|--------------|---------------------------------------|---------|
| **Dynamics 365 BC** | 50-100% | $35K software → $20K-$35K implementation |
| **NetSuite** | 100-200% | $60K software → $60K-$120K implementation |
| **SAP Business One** | 150-300% | $30K software → $45K-$90K implementation |
| **Odoo** | 100-300% | $15K software → $15K-$45K implementation |
| **Acumatica** | 50-100% | $70K software → $35K-$70K implementation |

**Rule of Thumb**: Budget 1-2x annual software cost for implementation

---

## IX. Month-End Close Checklist (First Month in New ERP)

**Week 1-3: Daily Transactions**
- [ ] Post all invoices daily
- [ ] Enter all bills daily
- [ ] Process payments daily
- [ ] Reconcile cash daily
- [ ] Monitor for data issues

**Week 4: Month-End Close**
- [ ] Run trial balance (compare to previous month)
- [ ] Bank reconciliation (all accounts)
- [ ] Review A/R aging (follow up on collections)
- [ ] Review A/P aging (schedule payments)
- [ ] Accrue expenses (payroll, rent, utilities)
- [ ] Depreciation (if not automated)
- [ ] Adjusting journal entries
- [ ] Run final financial statements
- [ ] Compare to QuickBooks (last month before migration)
- [ ] Document any discrepancies

**Success Criteria**:
- Trial balance balances (debits = credits)
- Financial statements accurate
- Reconciliations complete
- No critical data issues
- Close completed within 10 business days

---

## X. Key Takeaways

1. **Plan for 3-6 months** (don't rush, most failures are due to rushing)
2. **Budget 1-2x annual software** for implementation
3. **Invest in training** (10-20% of implementation cost)
4. **Clean data before migration** (garbage in = garbage out)
5. **Full UAT is critical** (test everything before go-live)
6. **Close old system** (no dual entry post-migration)
7. **Expect productivity drop** (40-60% for 2-4 weeks post-go-live)
8. **Hire experienced partner** (worth the cost, especially for first ERP)

**Most Important**: **Executive sponsorship** - CEO/CFO must champion the project

---

**Next**: See `graduation-triggers.md` for when to move from accounting software to ERP.
