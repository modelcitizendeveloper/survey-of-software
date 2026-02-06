# CRM (Customer Relationship Management): Technical Concepts and Domain Knowledge

**Document Purpose**: Explain CRM concepts for business stakeholders, CTOs, and decision-makers.

**This document explains**: What CRM is, how it works, types of CRM, and when to use it.

**This document does NOT**: Compare specific platforms (see S1-S4 research) or advocate for particular solutions.

---

## 1. Technical Concept Definitions

### What is CRM?

Customer Relationship Management (CRM) is a system for managing interactions with customers and prospects throughout the customer lifecycle.

**Core Functions**:
- **Contact Management**: Store customer information (name, email, phone, company, history)
- **Sales Pipeline**: Track deals through stages (lead → qualified → proposal → closed)
- **Interaction History**: Log calls, emails, meetings, notes
- **Task Management**: Reminders, follow-ups, assignments
- **Reporting**: Sales forecasts, conversion rates, pipeline health

**Types of CRM**:

**1. Operational CRM** (Sales Focus)
- **Purpose**: Automate sales, marketing, and service processes
- **Features**: Lead scoring, pipeline management, email sequences, territory assignment
- **Examples**: Pipedrive, Close, Salesforce Sales Cloud
- **Use case**: B2B sales teams tracking deals

**2. Analytical CRM** (Data Focus)
- **Purpose**: Analyze customer data for insights
- **Features**: Reporting, dashboards, customer segmentation, predictive analytics
- **Examples**: Salesforce with Einstein Analytics, HubSpot Analytics
- **Use case**: Enterprise sales analyzing win rates, forecasting

**3. Collaborative CRM** (Team Focus)
- **Purpose**: Share customer information across departments
- **Features**: Shared inbox, internal notes, handoff workflows, customer timeline
- **Examples**: HubSpot, Salesforce, Zoho
- **Use case**: Sales, support, and marketing teams collaborating on accounts

**4. Strategic CRM** (Relationship Focus)
- **Purpose**: Long-term customer retention and loyalty
- **Features**: Customer lifetime value tracking, loyalty programs, retention campaigns
- **Examples**: HubSpot Marketing Hub, Salesforce Marketing Cloud
- **Use case**: B2C businesses maximizing customer lifetime value

---

## 2. CRM vs Other Systems

### CRM vs Spreadsheet

**Spreadsheet** (Google Sheets, Excel):
- ✅ Flexible, familiar, free
- ❌ No automation, manual updates, hard to scale
- **When to use**: <50 customers, simple tracking, solo founder

**CRM**:
- ✅ Automation (follow-up reminders, email sequences), team collaboration
- ❌ Cost, learning curve, setup time
- **When to use**: >50 customers, sales team, complex pipeline

### CRM vs Project Management

**Project Management** (Asana, Monday.com):
- **Focus**: Task completion, project milestones, team workflows
- **Structure**: Tasks → Projects → Teams

**CRM**:
- **Focus**: Customer relationships, sales pipeline, deal tracking
- **Structure**: Contacts → Deals → Pipeline stages

**Overlap**: Both have tasks, reminders, team collaboration. CRM adds customer context.

### CRM vs Marketing Automation

**Marketing Automation** (Mailchimp, ActiveCampaign):
- **Focus**: Email campaigns, lead nurturing, audience segmentation
- **Structure**: Lists → Campaigns → Automation workflows

**CRM**:
- **Focus**: 1:1 sales relationships, deal tracking, pipeline management
- **Structure**: Individual contacts → Deals → Sales stages

**Integration**: Many modern CRMs include marketing automation (HubSpot, Zoho, ActiveCampaign).

---

## 3. Key CRM Concepts

### Lead vs Contact vs Deal

**Lead**:
- Person who showed interest but not yet qualified
- Example: Downloaded whitepaper, filled out contact form
- Stage: Top of funnel

**Contact**:
- Qualified person with complete information
- Example: Had discovery call, fit ICP (ideal customer profile)
- Stage: Middle of funnel

**Deal/Opportunity**:
- Potential sale with revenue value
- Example: Sent proposal for $50K contract
- Stage: Bottom of funnel

**Relationship**:
```
Lead → (qualify) → Contact → (create opportunity) → Deal → (close) → Customer
```

### Pipeline Stages

Typical B2B sales pipeline:
1. **Lead**: Unqualified prospect
2. **Qualified**: Fit criteria, expressed interest
3. **Meeting Scheduled**: Discovery call booked
4. **Proposal Sent**: Quote or proposal delivered
5. **Negotiation**: Discussing terms, pricing
6. **Closed Won**: Customer signed contract
7. **Closed Lost**: Deal fell through (lost to competitor, budget, timing)

**Customization**: Every business has different stages based on sales process.

### Lead Scoring

**Purpose**: Prioritize leads most likely to convert

**Scoring factors**:
- **Demographic**: Job title, company size, industry (fit score)
- **Behavioral**: Website visits, email opens, content downloads (engagement score)
- **Explicit**: Budget confirmed, timeline set, decision-maker identified (intent score)

**Example**:
- CEO at 100-person company (+30 points)
- Downloaded case study (+10 points)
- Requested demo (+50 points)
- **Total**: 90/100 = Hot lead

**Automation**: High-score leads auto-assigned to sales rep, trigger follow-up task.

### Sales Automation

**Email Sequences**:
- Day 1: Introduction email
- Day 3: Case study follow-up (if no reply)
- Day 7: Breakup email ("Should I close your file?")
- Auto-stop if reply received

**Task Automation**:
- New lead created → auto-create "Research company" task
- Demo completed → auto-create "Send proposal" task (due in 2 days)
- Deal moves to "Proposal Sent" → auto-create "Follow up" task (due in 3 days)

**Field Updates**:
- Email opened → Update "Last Engaged" date
- Deal stage changes → Update "Expected Close Date"

---

## 4. Integration Patterns

### Common Integrations

**Email** (Gmail, Outlook):
- Sync emails to CRM contact records
- Send emails from CRM
- Track opens, clicks
- **Value**: Complete communication history

**Calendar** (Google Calendar, Outlook):
- Sync meetings to CRM
- Show availability for scheduling
- Create calendar events from CRM
- **Value**: Meeting history tracked automatically

**Accounting** (QuickBooks, Xero):
- Sync invoices to CRM deals
- Track payment status
- Customer billing history
- **Value**: Finance and sales aligned

**POS** (Square, Toast, Lightspeed):
- Sync customer purchases to CRM
- Track customer lifetime value
- Loyalty program integration
- **Value**: B2C customer behavior insights

**Marketing** (Mailchimp, ActiveCampaign):
- Sync email campaigns to CRM
- Track campaign performance
- Segment customers for campaigns
- **Value**: Marketing and sales alignment

**Support** (Zendesk, Intercom):
- Sync support tickets to CRM
- Customer issue history
- Health score (support load = risk of churn)
- **Value**: Holistic customer view

---

## 5. When to Use CRM

### Business Scenarios

**Scenario 1: Simple B2C (Wine Bar)**
- **Customer count**: 200+ regulars
- **Sales complexity**: Low (walk-in customers)
- **CRM need**: Loyalty, marketing automation
- **Solution**: Lightweight CRM (Square Marketing) OR Spreadsheet+
- **Alternative**: No CRM (POS handles loyalty)

**Scenario 2: B2B SaaS (Software Sales)**
- **Customer count**: 50-500 prospects, 10-50 customers
- **Sales complexity**: High (multi-touch, demos, proposals)
- **CRM need**: Pipeline tracking, automation, forecasting
- **Solution**: Lightweight CRM (Pipedrive, Close) → Enterprise (Salesforce) as scale

**Scenario 3: Hybrid (Wine Bar + Wholesale)**
- **B2C**: 200+ retail customers (handled by POS loyalty)
- **B2B**: 10-50 distributor accounts (complex sales)
- **CRM need**: Sales pipeline for B2B only
- **Solution**: Lightweight CRM for B2B (Zoho Bigin), POS for B2C

**Scenario 4: Agency (Client Management)**
- **Customer count**: 20-100 clients
- **Sales complexity**: Medium (proposals, ongoing projects)
- **CRM need**: Client history, project tracking, renewal reminders
- **Solution**: CRM + Project Management integration (HubSpot + Asana)

---

## 6. Build vs Buy Decision

### When to Build Custom CRM

**Good reasons**:
- ✅ Unique workflow that platforms can't support
- ✅ Industry-specific requirements (compliance, data structure)
- ✅ Technical team with capacity
- ✅ Integration with proprietary systems

**Bad reasons**:
- ❌ "We're special" (most sales processes are similar)
- ❌ Cost savings (build cost often exceeds licensing)
- ❌ Control (platforms are highly customizable now)

**Build cost**: 40-200 hours initial development + ongoing maintenance

### When to Buy CRM Platform

**Good reasons**:
- ✅ Standard sales process (lead → qualified → proposal → close)
- ✅ Need integrations (email, calendar, accounting)
- ✅ Want automation (sequences, scoring, workflows)
- ✅ Team collaboration required
- ✅ Limited technical resources

**Cost**: $10-300/user/month depending on platform and features

---

## 7. Common Mistakes

### Over-Engineering for Size

**Mistake**: Small business (10 customers) buys Salesforce ($150/user/month)
- **Problem**: 90% of features unused, complexity overhead
- **Fix**: Start with Spreadsheet+ or Lightweight CRM ($10-30/user)

### Under-Investing at Scale

**Mistake**: 500-customer business still using Google Sheets
- **Problem**: Manual errors, lost follow-ups, no automation
- **Fix**: Lightweight CRM minimum (Pipedrive, Zoho)

### Ignoring Integrations

**Mistake**: Choose CRM that doesn't integrate with existing stack
- **Problem**: Manual data entry, duplicate records, context loss
- **Fix**: Evaluate integration ecosystem BEFORE buying

### No Adoption Plan

**Mistake**: Buy CRM, don't train team, low adoption
- **Problem**: Sales team keeps using old methods (email, spreadsheet)
- **Fix**: Training, incentives, gradual rollout

### Customization Debt

**Mistake**: Over-customize CRM, hard to upgrade or migrate
- **Problem**: Locked into old version, can't use new features
- **Fix**: Minimize customization, use platform defaults when possible

---

## 8. Migration Paths

### Spreadsheet → Lightweight CRM

**Trigger**: >50 customers OR sales team >1 OR missing follow-ups

**Process**:
1. Export spreadsheet to CSV
2. Import to CRM (Pipedrive, Zoho, Close)
3. Map fields (Name → Contact Name, Email → Email, etc.)
4. Train team on new system
5. Run parallel for 2 weeks
6. Sunset spreadsheet

**Effort**: 5-10 hours
**Risk**: Low (data is simple, easy to export)

### Lightweight → Enterprise CRM

**Trigger**: >2,000 customers OR complex automation OR enterprise features (territories, forecasting)

**Process**:
1. Export data from lightweight CRM (API or CSV)
2. Map custom fields to enterprise CRM schema
3. Migrate email/calendar integrations
4. Rebuild automation (sequences, workflows)
5. Train team on new interface
6. Run parallel for 1 month
7. Sunset old CRM

**Effort**: 40-80 hours
**Risk**: Medium (data mapping complexity, automation rebuild)

### CRM → CRM Migration

**Trigger**: Better pricing, better features, vendor dissatisfaction

**Challenge**: Lock-in (data export, integration rebuild, team retraining)

**Mitigation**:
- Choose CRM with robust API and data export
- Avoid over-customization
- Document workflows before migration

---

## Conclusion

CRM is a spectrum from manual (spreadsheet) to automated (platform) to custom-built. The right choice depends on customer count, sales complexity, and team size.

**Key Takeaways**:
1. Start simple (spreadsheet or lightweight CRM)
2. Upgrade when pain points emerge (>50 customers, missing follow-ups, team collaboration)
3. Evaluate integrations before buying
4. Avoid over-engineering (most businesses don't need Salesforce)
5. Plan for migration (lock-in is real, exit strategy matters)

---

**Document Version**: 1.0
**Last Updated**: 2025-10-21
**Scope**: CRM technical concepts and domain knowledge for business stakeholders
