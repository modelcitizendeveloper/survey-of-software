# Use Case: Translation Agencies (LSPs)

**Experiment**: 1.172 Translation Memory
**Pass**: S3 - Need-Driven Discovery
**Date**: 2026-01-29

## Use Case Overview

**WHO**: Language Service Providers (LSPs) managing 10-100+ translators across multiple client projects

**WHY**: Scale team capacity without quality loss, isolate client data for confidentiality, maintain consistent terminology across translators

**Context**: LSP handles 50+ simultaneous projects, needs to prevent Client A's TM from leaking into Client B's translations, enable real-time collaboration among distributed team

**Requirements**:
- Central TM server (multiple translators access shared TM)
- Client-specific TM isolation (data confidentiality)
- Role-based access control (PMs, translators, reviewers)
- Real-time updates (Translator B sees Translator A's work immediately)
- QA automation (terminology consistency, number formatting)
- Project package distribution (send work to freelancers)

**Volume**:
- Translation volume: 1M-10M words/year
- Concurrent projects: 50-200
- Team size: 10-100+ translators (in-house + freelance)
- Languages: 20-50 pairs

## Recommended Tool: MemoQ Server

**Rationale**:
1. **Real-time collaboration**: Multiple translators work on same project simultaneously
2. **Client isolation**: Separate TM per client workspace (prevent data leakage)
3. **Access control**: Granular permissions (PM, translator, reviewer roles)
4. **Performance**: Handles 50+ concurrent users on single server
5. **Freelance friendly**: Distributes project packages to external translators

### Real-Time Collaboration Advantage

**Scenario**: 5 translators working on 50,000-word manual

**Without TM server** (isolated work):
- Each translator gets 10,000 words
- Translator A translates "Error: Invalid input" → "Erreur : Saisie invalide"
- Translator B encounters same string → Retranslates (wastes time, may use different term)
- Result: Inconsistency, wasted effort

**With MemoQ Server** (real-time TM sync):
- All 5 translators share live TM
- Translator A translates "Error: Invalid input" at 10:00 AM
- Translator B sees same string at 10:05 AM → Auto-populated from A's translation
- Result: Consistency, 5x speedup on repeated segments

## Implementation Guidance

### 1. Server Setup

**Hardware requirements**:
```
MemoQ Server (50 concurrent users):
- CPU: 8 cores
- RAM: 32 GB
- Disk: 500 GB SSD
- Network: 1 Gbps

Estimated cost: $300-500/month (AWS r5.2xlarge or equivalent)
```

**Installation**:
```powershell
# Windows Server 2019/2022
# Download from https://www.memoq.com/server

# Run installer
memoq-server-setup-10.0.exe

# Configure database (SQL Server or PostgreSQL)
New-MemoQDatabase -DatabaseType SQLServer -Server localhost -Name MemoQDB

# Create admin user
New-MemoQUser -Username admin@lsp.com -Role Administrator
```

### 2. Client Workspace Setup

**Create isolated workspace per client**:
```csharp
// MemoQ API (C# SDK)
using MemoQ.ServerAPI;

var api = new MemoQServerApi("https://memoq.lsp.com:8080");
api.Login("pm@lsp.com", "password");

// Create client-specific workspace
var clientWorkspace = api.CreateWorkspace(new Workspace
{
    Name = "Client A - Legal Contracts",
    Description = "All translation work for Client A",
    IsolationLevel = IsolationLevel.Strict  // No TM sharing with other workspaces
});

// Import client TM
api.ImportTranslationMemory(clientWorkspace.Id, "client-a-legal-tm.tmx");

// Set access permissions
api.GrantAccess(clientWorkspace.Id, "translator-legal@lsp.com", Role.Translator);
api.GrantAccess(clientWorkspace.Id, "reviewer-legal@lsp.com", Role.Reviewer);
```

**Result**: Client A's TM isolated from Client B, Client C, etc.

### 3. Project Manager Workflow

**Create translation project**:
```csharp
// PM creates project via web UI or API
var project = api.CreateProject(new Project
{
    Name = "Client A - Product Manual v2.0",
    WorkspaceId = clientWorkspace.Id,
    SourceLanguage = "en",
    TargetLanguages = new[] { "fr", "de", "es", "ja" },
    Deadline = DateTime.Parse("2026-02-15"),
    AssignmentStrategy = AssignmentStrategy.AutoAssign  // Distribute by language pair
});

// Upload source files
api.UploadDocument(project.Id, "product-manual.docx");

// Assign translators
api.AssignTranslator(project.Id, "fr", "translator-fr@lsp.com");
api.AssignTranslator(project.Id, "de", "translator-de@lsp.com");
api.AssignReviewer(project.Id, "fr", "reviewer-fr@lsp.com");
```

**PM dashboard shows**:
- Progress: FR 45%, DE 30%, ES 10%, JA 0%
- Translators assigned: 4
- Deadline: 15 days remaining
- QA issues: 12 terminology errors, 3 number formatting

### 4. Translator Workflow (In-House)

**Translator opens MemoQ client**:
```csharp
// Auto-download assigned projects
var myProjects = api.GetAssignedProjects("translator-fr@lsp.com");

// Open project in MemoQ Editor
memoq.OpenProject(myProjects[0].Id);
```

**MemoQ Editor UI**:
```
Source (EN): "The system will restart automatically."
TM Match (95%): "The application will restart automatically." → "L'application redémarrera automatiquement."
Term base: "system" → "système" (approved)
Target (FR): [Translator types] "Le système redémarrera automatiquement."

[Save] → Syncs to server immediately
```

**Translator B (working on same project, different segment)**:
```
Source (EN): "The system will restart automatically."
TM Match (100%): [Auto-populated from Translator A's work 5 minutes ago]
Target (FR): "Le système redémarrera automatiquement." [Confirmed]
```

**Real-time sync**: Sub-second latency on LAN, <5 seconds over VPN

### 5. Freelance Translator Workflow

**PM exports project package**:
```csharp
// Create .mqout package for freelancer
var package = api.ExportProjectPackage(project.Id, "fr");
// File: client-a-manual-fr.mqout (includes source, TM, term base)

// Send via email/FTP to freelancer
SendToFreelancer("freelance-fr@example.com", package);
```

**Freelancer works offline**:
```powershell
# Freelancer has MemoQ installed (no server access needed)
# Opens .mqout package
memoq.exe client-a-manual-fr.mqout

# Translates offline (on airplane, coffee shop, etc.)
# TM updates saved in .mqout package

# Delivers .mqback package when done
```

**PM imports completed work**:
```csharp
// Import .mqback package
api.ImportProjectPackage(project.Id, "client-a-manual-fr.mqback");

// Freelancer's translations merge into server TM
// Other translators immediately see updated TM
```

## Alternative Options

### Option 2: SDL Trados Studio + GroupShare

**When to use**:
- Industry standard (most freelancers already own Trados)
- Need for offline work (Trados Studio works without server)
- Hybrid in-house/freelance team

**Trade-off**:
- More expensive (~$1,200/user for Studio + $500/user/year for GroupShare)
- Less real-time (GroupShare batch updates, not instant like MemoQ)

**Implementation**:
```csharp
// SDL GroupShare API
var gs = new GroupShareApi("https://groupshare.lsp.com");
gs.Login("pm@lsp.com", "password");

// Create project
var project = gs.CreateProject(new ProjectRequest
{
    Name = "Client A Manual",
    SourceLanguage = "en-US",
    TargetLanguages = new[] { "fr-FR", "de-DE" },
    TranslationMemory = "client-a-legal-tm",
    Workflow = new[] {
        new WorkflowStep { Name = "Translation", DueDate = "2026-02-10" },
        new WorkflowStep { Name = "Review", DueDate = "2026-02-15" }
    }
});

// Assign translator
gs.AssignUser(project.Id, "translator-fr@lsp.com", WorkflowStep.Translation);
```

**Freelancer downloads project package**:
```powershell
# SDL Studio Project Package (.sdlppx)
gs.ExportProjectPackage(project.Id, "fr-FR", "client-a-fr.sdlppx")

# Freelancer opens in SDL Trados Studio
SDL.TradosStudio.exe client-a-fr.sdlppx

# Translates offline, returns .sdlrpx package
gs.ImportCompletedPackage(project.Id, "client-a-fr.sdlrpx")
```

**Best for**: Large freelance network (most translators have Trados), need for offline work

## Common Pitfalls

### 1. Mixing Client TMs

**Problem**: Translator accidentally uses Client A's TM for Client B's project

**Scenario**:
```
Translator logs in, sees 2 projects:
- Client A (pharmaceutical) - TM has "patient" → "patient" (medical context)
- Client B (software) - TM should have "patient" → "tolérant" (software tolerant)

Translator uses wrong TM → Client B gets medical terminology in software docs
```

**Solution**: MemoQ workspace isolation
```csharp
// Strict isolation: Translator can only see assigned workspace
var workspace = api.CreateWorkspace(new Workspace
{
    IsolationLevel = IsolationLevel.Strict,
    AllowCrossWorkspaceTM = false  // Prevent TM leakage
});
```

### 2. Not Managing Freelance Packages

**Problem**: Freelancer never returns .mqback package, PM has no visibility

**Scenario**:
```
PM sends 10 projects to freelancer
Freelancer completes 8, abandons 2
PM doesn't know which are done until freelancer responds
```

**Solution**: Package expiration + automated reminders
```csharp
// Set package expiration (auto-lock after 7 days)
var package = api.ExportProjectPackage(project.Id, "fr", new PackageOptions
{
    ExpirationDate = DateTime.Now.AddDays(7),
    ReminderEmails = new[] { "freelancer@example.com" },
    ReminderSchedule = new[] { 5, 3, 1 }  // Days before deadline
});
```

### 3. Over-Segmenting Large Projects

**Problem**: Splitting 100,000-word project across 20 translators

**Scenario**:
```
PM: "Let's finish fast! Assign 5,000 words to each of 20 translators"
Result:
- Each translator gets random segments (no context)
- Terminology inconsistency (20 different people translating "system")
- Wasted time on coordination (merging 20 people's work)
```

**Solution**: Assign by logical units (chapters, modules)
```csharp
// Assign by document structure, not arbitrary word count
api.AssignTranslator(project.Id, "Chapter1-Introduction.docx", "translator-1@lsp.com");
api.AssignTranslator(project.Id, "Chapter2-Installation.docx", "translator-2@lsp.com");
// Each translator gets full chapter (better context, less coordination)
```

### 4. Ignoring QA Automation

**Problem**: Manual QA catches errors after delivery to client

**Scenario**:
```
Client receives translation:
- "The price is 1000.50 EUR" → "Le prix est 1000.50 EUR" (French uses comma: 1000,50 EUR)
- Client complains: "Why didn't you catch this?"
```

**Solution**: MemoQ QA automation
```csharp
// Configure QA rules
var qaRules = new QASettings
{
    NumberFormatChecks = true,  // Detect 1000.50 vs. 1000,50
    TerminologyChecks = true,   // Enforce approved terms
    ConsistencyChecks = true,   // Flag inconsistent translations
    TagChecks = true            // Ensure XML/HTML tags match
};

api.RunQA(project.Id, qaRules);

// Returns QA report
QAReport:
- 12 number formatting errors
- 8 unapproved terminology uses
- 3 tag mismatches
```

**PM fixes before delivery**, client satisfaction improves

## Performance Tuning

### 1. TM Optimization (Large TMs)

**Problem**: 10M segment TM → Slow lookups (5-10 seconds)

**Solution**: TM indexing + caching
```sql
-- MemoQ Server database optimization
CREATE INDEX idx_tm_source ON TranslationMemory(SourceSegment);
CREATE INDEX idx_tm_target ON TranslationMemory(TargetSegment);

-- Enable TM caching (server config)
<TMCache>
    <MaxCacheSizeGB>8</MaxCacheSizeGB>
    <PreloadTopClients>Client-A, Client-B</PreloadTopClients>
</TMCache>
```

**Result**: Lookup time: 5 seconds → 200ms

### 2. Concurrent User Scaling

**MemoQ Server performance**:
```
10 users: 4 CPU cores, 8 GB RAM → <100ms latency
50 users: 8 CPU cores, 32 GB RAM → <200ms latency
100 users: 16 CPU cores, 64 GB RAM → <500ms latency
```

**Load balancing** (>100 users):
```yaml
# Kubernetes deployment (2 MemoQ servers)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: memoq-server
spec:
  replicas: 2  # 2 server instances
  template:
    spec:
      containers:
      - name: memoq
        image: memoq/server:10.0
        resources:
          requests:
            cpu: 8
            memory: 32Gi
---
apiVersion: v1
kind: Service
metadata:
  name: memoq-lb
spec:
  type: LoadBalancer
  ports:
  - port: 8080
  selector:
    app: memoq-server
```

**Capacity**: 2 instances × 50 users = 100 concurrent users

## Success Metrics

### TM Leverage Rates

**Targets**:
- New client (first project): 0-20% (building TM from scratch)
- Returning client (6 months): 50-70%
- Long-term client (2+ years): 75-90%

**Measure per client**:
```sql
-- Query MemoQ database
SELECT
    Client,
    AVG(MatchRate) AS AvgLeverage
FROM ProjectStatistics
WHERE CreatedDate > '2025-01-01'
GROUP BY Client;

Results:
| Client   | AvgLeverage |
|----------|-------------|
| Client A | 82%         | (long-term)
| Client B | 55%         | (6 months)
| Client C | 15%         | (new)
```

### Translator Productivity

**Targets**:
- Without TM: 2,000 words/day
- With mature client TM (70%+ leverage): 3,500-4,500 words/day

**Measure**:
```sql
-- Translator productivity report
SELECT
    TranslatorEmail,
    SUM(WordCount) / COUNT(DISTINCT WorkDate) AS AvgWordsPerDay
FROM TranslatorActivity
WHERE Month = '2026-01'
GROUP BY TranslatorEmail;

Results:
| Translator           | AvgWordsPerDay |
|----------------------|----------------|
| translator-1@lsp.com | 4,200          | (experienced)
| translator-2@lsp.com | 3,800          |
| translator-3@lsp.com | 2,500          | (new hire)
```

### Quality (Revision Rate)

**Target**: <10% revision rate

**Measure**:
```sql
-- Percentage of segments revised after initial translation
SELECT
    AVG(RevisedSegments / TotalSegments * 100) AS RevisionRate
FROM Projects
WHERE Status = 'Completed';

Result: 8.5% revision rate (below 10% target)
```

## Cost Analysis

### Software Costs

**MemoQ Server**:
- License: $3,000-5,000/year (50 CAL - concurrent active users)
- Infrastructure: $300-500/month (cloud server)
- Total: ~$8,000-11,000/year

**SDL Trados Studio + GroupShare** (alternative):
- Studio licenses: $900/user × 20 users = $18,000 (one-time)
- GroupShare: $500/user/year × 20 users = $10,000/year
- Total: $18,000 setup + $10,000/year

**MemoQ advantage**: Lower cost for large teams (50 CAL cheaper than 50 Trados licenses)

### Translation Cost Savings

**Scenario**: LSP translates 5M words/year across 10 clients

**Without TM**:
```python
cost_without_tm = 5_000_000 * 0.12  # $0.12/word
# = $600,000/year
```

**With TM** (60% average leverage):
```python
cost_with_tm = (
    2_000_000 * 0.12 +  # 40% new @ $0.12
    2_000_000 * 0.05 +  # 40% fuzzy @ $0.05
    1_000_000 * 0.01    # 20% exact @ $0.01
)
# = $240,000 + $100,000 + $10,000 = $350,000/year
```

**Savings**: $250,000/year (42% reduction)

**ROI**:
```python
software_cost = 11_000  # MemoQ Server
savings = 250_000
roi = savings / software_cost
# = 22.7x ROI (payback in <3 weeks)
```

### Margin Improvement

**LSP pricing model**:
```python
# Charge clients by word count
client_rate = 0.15  # $/word (market rate)
revenue = 5_000_000 * 0.15  # $750,000

# Pay translators by TM leverage
translator_cost = 350_000  # (with TM savings)

margin = (revenue - translator_cost) / revenue * 100
# = 53.3% margin (vs. 20% without TM)
```

**Business impact**: TM enables 2.6x higher margins

## Real-World Examples

### Case Study: RWS (SDL Acquisition)

**Scale**: 10,000+ translators, 500+ languages
**Tool**: SDL Trados Studio + WorldServer (enterprise TM)
**Volume**: 1B+ words/year

**Key insights**:
- Largest LSP globally, relies entirely on SDL ecosystem
- Client-specific TMs with 80-90% leverage (long-term clients)
- Hybrid: In-house (WorldServer) + freelance (Trados Studio packages)

### Case Study: Lionbridge

**Scale**: 5,000+ translators, 350+ languages
**Tool**: Custom TM platform (proprietary) + integrations
**Volume**: 500M+ words/year

**Key insights**:
- Built custom TM server (outgrew commercial tools)
- API integrations with client systems (SAP, Salesforce, Adobe)
- Real-time TM sync across global offices (US, EU, APAC)

## Summary

**Recommended Tool**: MemoQ Server

**Key strengths**:
- ✅ Real-time collaboration (multiple translators, instant TM sync)
- ✅ Client isolation (strict workspace separation)
- ✅ Cost-effective (50 CAL cheaper than 50 Trados licenses)
- ✅ Freelance support (offline project packages)
- ✅ QA automation (catch errors before delivery)

**When to use SDL Trados instead**:
- Large freelance network (most translators own Trados already)
- Need for offline-first workflow (Studio works without server)
- Client requires SDL format (.sdlppx packages)

**Savings**: 40-60% translation cost reduction, 22x ROI on software

## Cross-References

- **S1 Rapid Discovery**: [memoq.md](../S1-rapid/memoq.md), [sdl-trados.md](../S1-rapid/sdl-trados.md)
- **S2 Comprehensive**: [memoq.md](../S2-comprehensive/memoq.md), [sdl-trados.md](../S2-comprehensive/sdl-trados.md)
- **S3 Other Use Cases**: [use-case-software-localization.md](use-case-software-localization.md), [use-case-freelance-translators.md](use-case-freelance-translators.md)
- **S4 Strategic**: Build vs. buy, TM governance
