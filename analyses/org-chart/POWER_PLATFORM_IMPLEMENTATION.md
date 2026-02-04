# Org-Chart: Power Platform Implementation Design

**Technical implementation details for Level 1 (Power Platform) solution**

---

## Data Storage Comparison

### Option 1: Dataverse ⭐ RECOMMENDED

**What it is:** Enterprise-grade relational database built into Power Platform

#### Data Model

```
Table: Employee
├── EmployeeID (Primary Key, Auto-number)
├── Email (Text, unique) - lookup from Azure AD
├── DisplayName (Text) - from AD or manual entry
├── JobTitle (Text)
├── DivisionID (Lookup to Division table)
├── ManagerID (Lookup to Employee table) - self-referential
├── Department (Text)
├── Location (Text)
├── StartDate (Date)
├── Status (Choice: Active, On Leave, Departed)
├── LastUpdatedBy (Lookup to User)
├── LastUpdatedDate (DateTime)
├── ApprovalStatus (Choice: Draft, Pending Review, Approved, Rejected)
└── Notes (Text, multiline)

Table: Division
├── DivisionID (Primary Key, Auto-number)
├── DivisionName (Text, unique)
├── ContactPersonEmail (Lookup to User)
├── ParentDivisionID (Lookup to Division table) - for nested divisions
├── DivisionHeadID (Lookup to Employee table)
└── LastReviewDate (DateTime)

Table: ApprovalHistory
├── ApprovalID (Primary Key, Auto-number)
├── EmployeeID (Lookup to Employee)
├── ReviewerEmail (Lookup to User)
├── ReviewDate (DateTime)
├── Action (Choice: Approved, Rejected, Requested Changes)
├── Comments (Text, multiline)
└── VersionSnapshot (Text, JSON) - store employee data at approval time

Table: OrgChartVersion
├── VersionID (Primary Key, Auto-number)
├── VersionDate (DateTime)
├── CreatedBy (Lookup to User)
├── Description (Text)
└── SnapshotData (Text, JSON) - full org chart at this point in time
```

#### Advantages ✅
- **Relationships:** Native hierarchical relationships (Manager → Employee, Division → Employee)
- **Security:** Row-level security (divisions see only their employees)
- **Validation:** Business rules enforced at database level (can't have circular reporting, required fields)
- **Audit:** Built-in audit log (who changed what, when)
- **Performance:** Optimized for Power Platform queries
- **Integration:** Direct connection to Power Apps, Power Automate, Power BI
- **Scalability:** Handles 1000s of records easily
- **APIs:** Auto-generated REST API for external integration

#### Disadvantages ❌
- **Cost:** $40/10GB after 3GB included (but 1000 employees = ~5GB, so $40-80/month)
- **Complexity:** Requires understanding Dataverse concepts (tables, relationships, security roles)
- **Licensing:** Requires Power Apps per-app or per-user license

#### When to Choose Dataverse
- ✅ Need row-level security (divisions can't see other divisions)
- ✅ Need complex relationships (manager hierarchy, division hierarchy)
- ✅ Need audit trail (compliance requirement)
- ✅ Building multiple apps on same data
- ✅ Need offline access (Power Apps can cache Dataverse data)

---

### Option 2: SharePoint Lists ⚠️ VIABLE ALTERNATIVE

**What it is:** Structured data storage in SharePoint, accessible via Power Platform

#### Data Model

```
List: Employees
├── ID (Auto-number)
├── Email (Person field) - links to Azure AD
├── DisplayName (Single line text)
├── JobTitle (Single line text)
├── Division (Lookup to Divisions list)
├── Manager (Person field) - links to Azure AD
├── Department (Single line text)
├── Location (Choice field: HQ, Remote, Office A, Office B...)
├── Status (Choice: Active, On Leave, Departed)
├── ApprovalStatus (Choice: Draft, Pending, Approved, Rejected)
├── LastReviewDate (Date)
└── Notes (Multiple lines text)

List: Divisions
├── ID (Auto-number)
├── DivisionName (Single line text)
├── ContactPerson (Person field)
├── ParentDivision (Lookup to self)
├── DivisionHead (Lookup to Employees list)
└── LastReviewDate (Date)

List: ApprovalHistory
├── ID (Auto-number)
├── Employee (Lookup to Employees list)
├── Reviewer (Person field)
├── ReviewDate (Date)
├── Action (Choice: Approved, Rejected, Requested Changes)
└── Comments (Multiple lines text)
```

#### Advantages ✅
- **Cost:** Free (included with Microsoft 365)
- **Familiarity:** Most enterprises already use SharePoint
- **Permissions:** SharePoint groups for access control (easier for IT to understand)
- **Excel integration:** Can export to Excel, edit, re-import
- **Quick setup:** Create lists in 30 minutes
- **Version history:** Built-in versioning on list items
- **No special licensing:** Works with standard Microsoft 365

#### Disadvantages ❌
- **5000 item view threshold:** List views limited to 5000 items (1000 employees OK, but hits limit with growth)
- **Performance:** Slower than Dataverse for complex queries
- **Relationships:** Lookup fields less robust than Dataverse relationships
- **No offline:** Power Apps can't cache SharePoint data for offline use
- **Limited validation:** Can't enforce complex business rules at database level
- **Security:** Harder to implement row-level security (need complex permissions)

#### When to Choose SharePoint Lists
- ✅ Already using SharePoint heavily
- ✅ Budget-constrained (need free option)
- ✅ Simple access control OK (division contacts can see all data)
- ✅ <5000 employees (won't hit threshold)
- ✅ Excel export/import important (users comfortable with Excel)

---

### Option 3: Excel (Current Source) ❌ NOT RECOMMENDED

**What it is:** Excel file stored in SharePoint/OneDrive, connected to Power Platform

#### Data Model

```
Sheet: Employees
├── Column A: Email
├── Column B: Display Name
├── Column C: Job Title
├── Column D: Division
├── Column E: Manager Email
├── Column F: Department
├── Column G: Status
└── Column H: Last Updated

Sheet: Divisions
├── Column A: Division Name
├── Column B: Contact Email
└── Column C: Parent Division
```

#### Advantages ✅
- **Familiarity:** Everyone knows Excel
- **Easy editing:** Can bulk-edit in Excel
- **No licensing:** Free with Microsoft 365
- **Quick start:** Already have the data in Excel

#### Disadvantages ❌
- **Concurrency:** Can't have multiple people editing simultaneously
- **No relationships:** Can't enforce referential integrity (manager must exist)
- **No validation:** Can enter invalid data (circular reporting, missing required fields)
- **No audit:** Can't see who changed what, when
- **No security:** Can't restrict row-level access
- **Performance:** Power Apps slow when connecting to Excel (must load entire table)
- **Approval workflow:** Can't easily track approval status in Excel

#### When to Choose Excel
- ⚠️ Only as **import source** for one-time migration
- ⚠️ NOT for production data storage

---

## Recommendation: Dataverse vs SharePoint

### Decision Matrix

| Factor | Dataverse | SharePoint Lists |
|--------|-----------|------------------|
| **Cost** | $40-80/month | Free |
| **Performance** | Excellent | Good |
| **Security** | Row-level (advanced) | List-level (basic) |
| **Relationships** | Native, enforced | Lookups (not enforced) |
| **Audit trail** | Built-in | Version history only |
| **Scalability** | 100K+ records | <5000 per view |
| **Offline support** | Yes (Power Apps) | No |
| **Setup complexity** | Medium | Low |
| **Excel integration** | Export only | Export + re-import |

### Recommended Choice: **Dataverse** ⭐

**Why:**
1. **Row-level security critical:** Divisions should only edit their employees
2. **Relationship enforcement:** Can't have orphaned managers, circular reporting
3. **Audit requirement:** HR needs to see change history for compliance
4. **Future growth:** 1000 employees → 2000 employees = SharePoint hits threshold
5. **Cost justified:** $40-80/month saved by eliminating 25 hours/month manual work ($1250/month value)

**Only choose SharePoint Lists if:**
- Budget absolutely can't afford $40-80/month
- Security requirement relaxed (all division contacts can see all data)
- <1000 employees, no growth expected

---

## Approval Workflow Design

### Workflow Overview

```
1. Division Contact edits employees
   ↓
2. Division Contact clicks "Submit for Review"
   ↓
3. Power Automate triggered
   ↓
4. Email sent to Division Head for approval
   ↓
5. Division Head approves/rejects (via email or Power App)
   ↓
6. If approved → Status = "Approved", HR notified
   If rejected → Status = "Draft", Division Contact notified
   ↓
7. HR can see all approved data
   ↓
8. Quarterly: Power Automate reminds Division Contacts to review
```

### Power Automate Flow: "Division Review Submission"

**Trigger:** When Employee record ApprovalStatus changes to "Pending Review"

**Actions:**
1. **Get Division record** (from DivisionID lookup)
2. **Get Division Head** (from Division.DivisionHeadID)
3. **Create approval request**
   - Approver: Division Head email
   - Title: "Review org chart updates for [Division Name]"
   - Details:
     - Number of changes: [count of Pending Review records]
     - Link to Power App: [deep link to division view]
4. **Wait for approval response**
5. **Condition: If approved**
   - **Update Employee records** → ApprovalStatus = "Approved"
   - **Create ApprovalHistory record** (snapshot of data)
   - **Send email to HR** → "Division [Name] org chart approved, [N] changes"
6. **Condition: If rejected**
   - **Update Employee records** → ApprovalStatus = "Draft"
   - **Send email to Division Contact** → "Changes rejected by [Division Head], comments: [X]"

### Power Automate Flow: "Quarterly Review Reminder"

**Trigger:** Recurrence (every 3 months)

**Actions:**
1. **Get Divisions** where LastReviewDate < 90 days ago
2. **For each Division:**
   - **Send email to Contact Person**
     - Subject: "Time to review [Division Name] org chart"
     - Body: "Please review your division's org chart and submit any updates. Last review: [Date]"
     - Button: "Open Org Chart App" (deep link to Power App)
3. **Log reminder sent** (update Division.LastReviewDate)

### Power Automate Flow: "New Employee Auto-Add"

**Trigger:** When new user added to Azure AD (optional, if AD is source of truth)

**Actions:**
1. **Get user details from AD** (name, email, job title, manager)
2. **Check if employee exists** in Employee table
3. **If not exists:**
   - **Create Employee record**
     - Status = "Draft"
     - Manager = lookup from AD manager
     - Division = [TBD - needs manual assignment]
   - **Send email to HR** → "New employee [Name] added, needs division assignment"

---

## Power Apps Design

### App 1: "Division Org Chart Manager" (Canvas App)

**Users:** Division Contacts (50 users)

**Screens:**

#### Screen 1: Division Overview
- **My Division:** [Division Name]
- **Total Employees:** [Count]
- **Pending Changes:** [Count where Status = "Draft"]
- **Last Review:** [Date]
- **Buttons:**
  - "View Org Chart" → Screen 2
  - "Edit Employees" → Screen 3
  - "Submit for Review" → Trigger workflow

#### Screen 2: Visual Org Chart
- **Control:** Organization Chart visual (custom PCF component or SVG)
- **Display:** Hierarchical tree (Division Head at top, reports below)
- **Interaction:** Click employee → See details
- **Filter:** Only show my division
- **Export:** Button to download as PNG/PDF

#### Screen 3: Employee List (Editable)
- **Gallery:** List of employees in my division
- **Columns:** Name, Job Title, Manager, Status
- **Actions:**
  - Click row → Edit form (Screen 4)
  - "Add New Employee" → Edit form (Screen 4)
  - "Delete" → Mark as Departed
- **Filter:** Only my division (RLS enforced by Dataverse)

#### Screen 4: Edit Employee
- **Form fields:**
  - Display Name (text)
  - Email (text, validated)
  - Job Title (text)
  - Manager (dropdown, filtered to my division)
  - Department (text)
  - Location (dropdown)
  - Status (dropdown)
  - Notes (text area)
- **Validation:**
  - Manager can't be self
  - Email must be unique
  - Required fields: Name, Email, Manager
- **Buttons:**
  - "Save" → Update record, Status = "Draft"
  - "Cancel" → Return to Screen 3

### App 2: "HR Org Chart Viewer" (Canvas App)

**Users:** HR Admins (5 users)

**Screens:**

#### Screen 1: Company-Wide Org Chart
- **Display:** Full organization hierarchy (CEO at top)
- **Filter:** By division, by location, by status
- **Search:** Find employee by name/email
- **Export:** Download full org chart as Visio/PDF

#### Screen 2: Division Status Dashboard
- **Table:**
  - Division Name | Contact | Last Review | Pending Changes | Status
- **Actions:**
  - Click division → View division org chart
  - Click "Pending Changes" → See what's changed
- **Alerts:** Highlight divisions not reviewed in 90+ days

#### Screen 3: Change History
- **Timeline:** Show all approval actions
- **Filters:** By division, by date range, by reviewer
- **Details:** Before/after comparison for each change

---

## Generating Visio from Data

### Challenge: Power Automate → Visio Export

**Problem:** Power Automate doesn't have native "Create Visio file" action.

### Solution Options

#### Option 1: Use Microsoft Graph API ⭐ RECOMMENDED

**Approach:** Power Automate HTTP action to Microsoft Graph API

**Power Automate Flow:**
1. **Get Employee records** from Dataverse (all approved records)
2. **Transform to JSON** (prepare hierarchical structure)
3. **HTTP request to Graph API:**
   - **Endpoint:** POST /drives/{drive-id}/items/{parent-id}/children
   - **Action:** Create Visio file from template
   - **Body:** XML in Visio format (VDX or VSDX structure)
4. **Upload generated file** to SharePoint document library
5. **Send email with link** to file

**Visio XML Structure (simplified):**
```xml
<VisioDocument>
  <Pages>
    <Page Name="Org Chart">
      <Shapes>
        <Shape ID="1" Type="Executive">
          <Text>CEO Name</Text>
          <Position X="5" Y="1"/>
        </Shape>
        <Shape ID="2" Type="Manager">
          <Text>Division Head Name</Text>
          <Position X="2" Y="3"/>
        </Shape>
        <!-- ... more shapes ... -->
      </Shapes>
      <Connects>
        <Connect FromSheet="1" ToSheet="2"/> <!-- CEO to Division Head -->
        <!-- ... more connections ... -->
      </Connects>
    </Page>
  </Pages>
</VisioDocument>
```

**Complexity:** High (requires understanding Visio XML format, Graph API)

**Development time:** 20-30 hours

---

#### Option 2: Use Power Automate + Excel + Manual Import to Visio ⚠️ PRAGMATIC

**Approach:** Export to Excel format that Visio can import

**Power Automate Flow:**
1. **Get Employee records** from Dataverse
2. **Create Excel file** in SharePoint
   - **Sheet 1:** Employee data (Name, Title, Manager, Reports To)
   - **Sheet 2:** Connection data (Employee ID, Manager ID)
3. **Save to SharePoint document library**
4. **Send email to user:** "Your org chart data is ready. Download Excel and import to Visio."

**User manual step:**
1. Download Excel file
2. Open Visio → New → Organization Chart
3. Click "Import" → Select Excel file
4. Visio auto-generates org chart from data
5. Customize layout, styling as needed

**Complexity:** Low (built-in Visio feature)

**Development time:** 4-8 hours

**Trade-off:** Requires manual step, but Visio import is fast (30 seconds)

---

#### Option 3: Use OrgChart.js + Export to Image/PDF ⭐ MODERN ALTERNATIVE

**Approach:** Generate interactive org chart in web browser, export as image/PDF

**Implementation:**
1. **Power Apps Component Framework (PCF):**
   - Build custom component using OrgChart.js library
   - Fetch data from Dataverse
   - Render interactive org chart in canvas app
2. **Export options:**
   - PNG: Use html2canvas library to capture as image
   - PDF: Use jsPDF library to generate PDF
   - SVG: OrgChart.js native export

**Advantages:**
- ✅ Interactive org chart in Power Apps (click to expand, zoom, pan)
- ✅ Modern look (better than Visio default templates)
- ✅ Multiple export formats (PNG, PDF, SVG)
- ✅ Can style with CSS (match corporate branding)

**Disadvantages:**
- ❌ Not native Visio format (users can't edit in Visio)
- ❌ Requires PCF development (advanced Power Platform skill)

**Complexity:** Medium (requires PCF development, JavaScript)

**Development time:** 30-40 hours

---

### Recommendation: Phased Approach

**Phase 1 (MVP - 4 weeks):**
- Use **Option 2: Excel export + manual Visio import**
- Fast to build, uses existing Visio feature
- HR users comfortable with Excel + Visio workflow

**Phase 2 (Enhancement - if needed):**
- Evaluate demand: Do users want fully automated Visio generation?
- If yes → Invest in **Option 1: Graph API automation** (20-30 hours)
- If no (Excel + Visio workflow is fine) → Stay with Phase 1

**Phase 3 (Future - optional):**
- Build **Option 3: OrgChart.js PCF component** for interactive web view
- Modern, shareable org charts (embed in SharePoint, Teams)
- Complement to Visio (not replacement)

---

## Complete Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                         Azure AD                            │
│  (Source of truth for employees, managers, emails)          │
└───────────────────┬─────────────────────────────────────────┘
                    │ Sync
                    ↓
┌─────────────────────────────────────────────────────────────┐
│                       Dataverse                             │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────────┐   │
│  │  Employee   │  │  Division    │  │ ApprovalHistory  │   │
│  │  Table      │  │  Table       │  │  Table           │   │
│  └─────────────┘  └──────────────┘  └──────────────────┘   │
│                                                              │
│  Row-level security: Divisions see only their data          │
└────────┬───────────────────┬─────────────────────┬──────────┘
         │                   │                     │
         │                   │                     │
    ┌────▼─────┐      ┌──────▼──────┐      ┌──────▼─────┐
    │  Power   │      │   Power     │      │  Power BI  │
    │  Apps    │      │  Automate   │      │  Dashboard │
    │          │      │             │      │            │
    │ • Division│     │ • Approval  │      │ • Org      │
    │   Manager│      │   workflow  │      │   chart    │
    │ • HR     │      │ • Quarterly │      │   visual   │
    │   Viewer │      │   reminders │      │ • Metrics  │
    └────┬─────┘      │ • Email     │      └────────────┘
         │            │   notify    │
         │            └──────┬──────┘
         │                   │
         │                   ↓
         │            ┌──────────────┐
         │            │  Outlook /   │
         │            │  Teams       │
         │            │              │
         │            │ • Approval   │
         │            │   emails     │
         │            │ • Reminders  │
         └────────────┤ • Deep links │
                      └──────┬───────┘
                             │
                      ┌──────▼────────┐
                      │  SharePoint   │
                      │               │
                      │ • Exported    │
                      │   Excel files │
                      │ • Exported    │
                      │   Visio files │
                      │ • Snapshots   │
                      └───────────────┘
```

---

## Implementation Roadmap

### Week 1-2: Setup & Data Model
- [ ] Create Dataverse environment
- [ ] Define Employee, Division, ApprovalHistory tables
- [ ] Configure relationships and security roles
- [ ] Import existing Excel data (one-time migration)
- [ ] Set up Azure AD sync (if needed)

### Week 3-4: Power Apps Development
- [ ] Build Division Org Chart Manager app
  - [ ] Division Overview screen
  - [ ] Employee list screen
  - [ ] Edit employee form
- [ ] Build HR Org Chart Viewer app
  - [ ] Company-wide view
  - [ ] Division status dashboard
- [ ] Test with 2-3 pilot divisions

### Week 5-6: Power Automate Workflows
- [ ] Build approval workflow (submit → approve/reject)
- [ ] Build quarterly reminder workflow
- [ ] Build Excel export workflow (for Visio import)
- [ ] Test end-to-end workflow

### Week 7-8: Testing & Training
- [ ] UAT with HR and 5 division contacts
- [ ] Refinements based on feedback
- [ ] Create user documentation
- [ ] Training sessions (1 hour per group)
- [ ] Launch to all divisions

### Week 9-10: Monitoring & Support
- [ ] Monitor adoption (Power BI usage dashboard)
- [ ] Address support questions
- [ ] Collect feedback for Phase 2 enhancements

---

## Cost Breakdown

### Licensing (Monthly)
- **Dataverse:** $40-80/month (5-10GB storage)
- **Power Apps:** $250/month (50 division contacts × $5 per-app license)
- **Power Automate:** Included in Power Apps licenses
- **Power BI:** $500/month (Premium capacity for 1000 viewers) OR $0 (if viewers have Pro licenses)

**Total: $290-830/month** (depending on Power BI licensing)

### Development (One-Time)
- **Dataverse setup:** 8 hours × $100/hour = $800
- **Power Apps development:** 40 hours × $100/hour = $4,000
- **Power Automate workflows:** 20 hours × $100/hour = $2,000
- **Testing & training:** 16 hours × $100/hour = $1,600
- **Documentation:** 8 hours × $100/hour = $800

**Total: $9,200** (internal IT) or **$12,000-15,000** (external contractor)

### ROI
- **Monthly savings:** $1,250 (25 hours labor eliminated)
- **Break-even:** 10-15 months
- **3-year ROI:** $45,000 savings - $19,200 cost = **$25,800 net benefit**

---

## Alternatives & Trade-offs

### If Budget Constrained: SharePoint Lists

**Savings:**
- **Licensing:** $250/month (only Power Apps licenses, no Dataverse)
- **Development:** Same ($9,200)

**Trade-offs:**
- No row-level security (divisions can see all data) → mitigate with separate lists per division
- Performance slower for complex queries
- 5000 item view limit (OK for 1000 employees, but constrains growth)

**Verdict:** Acceptable for <1000 employees, tight budget, relaxed security

---

### If Timeline Critical: Packaged Software

**Re-evaluate:**
- **Lucidchart:** $6-8/user × 50 = $300-400/month (compare to $290-830 Power Platform)
- **Pingboard:** $150-300/month flat (better pricing!)
- **ChartHop:** $500-1000/month (enterprise-grade)

**If Pingboard fits workflow ($150-300/month):**
- **Cost:** Lower than Power Platform
- **Development:** Zero (packaged software)
- **Time-to-launch:** 2-4 weeks (vs 8 weeks for Power Platform)

**Action:** Trial Pingboard → If fits → Buy instead of build!

---

## Conclusion

**Recommended Implementation:**

1. **Data Storage:** Dataverse (row-level security, scalability, audit trail)
2. **Approval Workflow:** Power Automate with email approvals
3. **Visio Generation:** Phase 1 = Excel export + manual import (fast), Phase 2 = Graph API automation (if demand)
4. **Apps:** Two canvas apps (Division Manager, HR Viewer)
5. **Timeline:** 8 weeks development, 2 weeks training
6. **Cost:** $9,200 development + $290-830/month ongoing
7. **ROI:** Break-even in 10-15 months

**Critical validation step:** Trial Pingboard before building! If it has approval workflow + Visio export, buy instead of build.

---

**Document Version:** 1.0
**Date:** October 13, 2025
**Status:** Design phase - awaiting license verification and packaged software trial
