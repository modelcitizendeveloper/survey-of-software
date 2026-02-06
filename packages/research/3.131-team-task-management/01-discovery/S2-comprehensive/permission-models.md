# S2 Comprehensive: Permission Models & Team Collaboration

**Date**: 2025-11-12
**Phase**: S2 Comprehensive
**Purpose**: Analysis of permission models, role-based access control, and team collaboration patterns across 6 platforms

---

## Executive Summary

**Key Findings**:
- **Role complexity spectrum**: Trello (2 roles) → Linear (4 roles) → Asana (5 roles) → ClickUp (7 roles)
- **Granularity leaders**: Airtable (field-level), ClickUp (task-level), Monday.com (board-level)
- **Guest access**: All platforms support guest/external collaborators, but with varying limitations
- **Custom roles**: Available only on Business/Enterprise tiers ($15-25/user/month+)
- **SSO/SAML**: Enterprise feature across all platforms (not available on free/team tiers)

**Permission Model Tiers**:
- **Tier 1 (Simple)**: Trello, Linear (2-4 roles, project-level permissions)
- **Tier 2 (Balanced)**: Asana, Monday.com (5 roles, workspace + project permissions)
- **Tier 3 (Complex)**: ClickUp, Airtable (7+ roles, field/task-level permissions, custom roles)

---

## Role Types Comparison

### Overview Table

| Platform | # of Roles | Role Granularity | Custom Roles | Guest Access | Field-Level Permissions |
|----------|------------|------------------|--------------|--------------|-------------------------|
| **Trello** | 2 | Board-level | ❌ No | ✅ Yes (invite to board) | ❌ No |
| **Linear** | 4 | Project/Team-level | ❌ No | ✅ Yes (limited view) | ❌ No |
| **Asana** | 5 | Workspace + Project | ✅ Business+ | ✅ Yes (project-specific) | ❌ No |
| **Monday.com** | 5 | Workspace + Board | ✅ Enterprise | ✅ Yes (board-level) | ✅ Enterprise |
| **ClickUp** | 7 | Workspace → Task | ✅ Business+ | ✅ Yes (granular) | ✅ Business+ |
| **Airtable** | 5 | Base + Table | ✅ Enterprise | ✅ Yes (base-level) | ✅ Yes (per field) |

---

## Platform-by-Platform Analysis

### **Trello** (Simplest: 2 Roles)

#### Available Roles

**1. Admin** (Board owner)
- Full control over board settings
- Add/remove members
- Delete board
- Change visibility (public, private, team)

**2. Member**
- Create cards
- Edit cards
- Comment, attach files
- Move cards between lists
- Cannot delete board or change settings

#### Granularity
- **Board-level only**: Permissions apply to entire board (cannot restrict per list or card)

#### Guest Access
- **Invite external users**: Add anyone with email to board (even if not in Trello organization)
- **Limitations**: Guests have same permissions as Members (cannot restrict to read-only at board level)
- **Workaround**: Use Workspace (paid tier) to manage guest permissions at organization level

#### Custom Roles
- **Not available**: Fixed 2-role model (Admin, Member)

#### Collaboration Patterns

**Best for**:
- Small teams (3-8 people) with flat hierarchy
- Everyone needs equal access (no sensitive data)
- External collaborators with full board access (clients, contractors)

**Not suitable for**:
- Large teams needing granular permissions
- Security-sensitive projects (no read-only at board level)
- Complex org structures (multiple teams, departments)

---

### **Linear** (Simple: 4 Roles)

#### Available Roles

**1. Owner**
- Full organization control
- Billing, delete workspace
- Manage members, teams, projects

**2. Admin**
- Manage teams and members
- Create projects, roadmaps
- Configure integrations
- Cannot delete workspace or change billing

**3. Member**
- Create issues, projects
- Edit assigned issues
- Comment, attach files
- View all teams (unless private)

**4. Guest**
- **Read-only** access to specific teams/projects
- Cannot create issues or edit
- Cannot see other teams

#### Granularity
- **Team-level**: Permissions can be set per team (not per project within team)
- **Private teams**: Teams can be marked private (only members can see)

#### Guest Access
- **Invite external users**: Add guests to specific teams
- **Limitations**: Read-only (cannot create issues, comment disabled by default)
- **Use case**: Clients reviewing project progress, stakeholders checking roadmaps

#### Custom Roles
- **Not available**: Fixed 4-role model

#### Collaboration Patterns

**Best for**:
- Engineering teams (5-15 people) with clear hierarchy (owner, engineers, stakeholders)
- External stakeholders needing read-only access (investors, clients)
- Teams with private projects (not all members should see everything)

**Not suitable for**:
- Complex permission needs (no per-project permissions within team)
- External collaborators needing write access (guests are read-only)

---

### **Asana** (Balanced: 5 Roles)

#### Available Roles

**1. Owner** (Organization/Workspace)
- Full control over organization
- Billing, security settings (SSO, SAML)
- Delete workspace

**2. Admin**
- Manage members, projects
- Configure integrations, custom fields
- Cannot change billing or delete workspace

**3. Member**
- Create tasks, projects
- Edit tasks in assigned projects
- Comment, attach files, collaborate

**4. Limited Access Member** (Business tier+)
- Access only to assigned projects (not all projects in workspace)
- Useful for contractors, external teams

**5. Guest**
- Access specific projects only (not entire workspace)
- Cannot create projects (only tasks within project)
- Cannot see other projects

#### Granularity
- **Workspace-level**: Owner, Admin control entire workspace
- **Project-level**: Members, Limited Access, Guests can be restricted to specific projects
- **Task-level**: Cannot restrict edit permissions per task (if you can see project, you can edit tasks)

#### Guest Access
- **Invite external users**: Add guests to specific projects
- **Limitations**:
  - Free tier: Unlimited guests (but limited to 15 total members)
  - Paid tiers: Unlimited guests
- **Use case**: Clients, contractors, external teams collaborating on specific projects

#### Custom Roles
- **Available**: Business tier ($25/user/month) and above
- **Custom role features**: Define custom permissions (e.g., "can view but not edit tasks", "can create but not delete")

#### Collaboration Patterns

**Best for**:
- Cross-functional teams (10-30 people) with multiple departments
- External collaborators on specific projects (agencies, contractors)
- Organizations needing project-level permissions (not everyone sees everything)

**Not suitable for**:
- Field-level permissions (cannot hide specific task fields from users)
- Very complex permission hierarchies (no task-level permissions)

---

### **Monday.com** (Balanced: 5 Roles)

#### Available Roles

**1. Owner** (Account)
- Full control over account
- Billing, security (SSO, SAML)
- Delete account

**2. Admin**
- Manage members, boards
- Configure automations, integrations
- Cannot change billing or delete account

**3. Member**
- Create boards, items
- Edit items in boards they have access to
- Comment, attach files

**4. Viewer** (Paid tiers)
- **Read-only** access to boards
- Cannot create or edit items
- Can comment (if enabled)

**5. Guest**
- Access specific boards only (not entire workspace)
- Can create items, edit (if permitted)
- Cannot see other boards

#### Granularity
- **Workspace-level**: Owner, Admin control entire workspace
- **Board-level**: Guests can be restricted to specific boards
- **Column-level**: Enterprise tier can hide specific columns from users
- **Item-level**: Cannot restrict per item (if you can see board, you see all items)

#### Guest Access
- **Invite external users**: Add guests to specific boards
- **Limitations**:
  - Free tier: 2 users total (no separate guest concept at free tier)
  - Standard tier: 2 guests max
  - Pro tier: Unlimited guests
- **Use case**: Clients reviewing project status, external partners collaborating

#### Custom Roles
- **Available**: Enterprise tier ($24+/user/month)
- **Custom role features**: Define custom permissions per board, column visibility

#### Collaboration Patterns

**Best for**:
- Sales/marketing teams (10-25 people) with client-facing boards
- Visual workflow teams (non-technical) needing simple permissions
- Teams with external collaborators (clients, vendors) on specific boards

**Not suitable for**:
- Item-level permissions (cannot restrict per item)
- Free/Standard tiers with many external collaborators (guest limits)

---

### **ClickUp** (Complex: 7 Roles + Custom)

#### Available Roles

**1. Owner** (Workspace)
- Full control over workspace
- Billing, security, integrations
- Delete workspace

**2. Admin**
- Manage members, spaces, folders
- Configure permissions, automations
- Cannot change billing or delete workspace

**3. Member**
- Create tasks, lists, folders (if permitted)
- Edit tasks in accessible spaces
- Comment, attach files

**4. Guest** (Limited Member)
- Access specific spaces/folders/lists only
- Can create tasks (if permitted)
- Cannot see other spaces

**5. Custom Roles** (Business tier+)
- Define custom permissions (e.g., "can edit but not delete tasks")
- Granular control: Workspace → Space → Folder → List → Task level

**6. View-Only** (Business tier+)
- **Read-only** access to specific spaces
- Cannot create or edit tasks
- Can comment (if enabled)

**7. Can Edit** (Business tier+)
- Edit tasks but not delete
- Cannot create new tasks (edit-only)

#### Granularity
- **Workspace-level**: Owner, Admin
- **Space-level**: Permissions per space (top-level container)
- **Folder-level**: Permissions per folder within space
- **List-level**: Permissions per list within folder
- **Task-level**: Individual tasks can have custom permissions (most granular)

#### Guest Access
- **Invite external users**: Add guests to specific spaces, folders, or lists
- **Limitations**: Free tier (2 guests max), Unlimited tier (5 guests), Business tier (unlimited guests)
- **Use case**: Clients, contractors with granular access (only specific lists, not entire space)

#### Custom Roles (Business tier+)
- **Most flexible custom roles** among all platforms
- Define permissions per action: Create, edit, delete, comment, attach files, manage settings
- Apply custom roles at any level (workspace, space, folder, list, task)

#### Collaboration Patterns

**Best for**:
- Large teams (20-50 people) with complex org structures (multiple departments, hierarchy)
- Teams needing task-level permissions (sensitive tasks hidden from some members)
- Agencies managing many clients (each client gets separate space with custom permissions)

**Not suitable for**:
- Small teams (3-8 people) — overkill, too complex
- Teams wanting simple permissions (7 roles + custom can overwhelm)

---

### **Airtable** (Complex: Field-Level Permissions)

#### Available Roles

**1. Owner** (Workspace)
- Full control over workspace
- Billing, security, integrations
- Delete workspace

**2. Creator**
- Create bases, tables
- Full edit permissions in bases they create
- Cannot change workspace billing

**3. Editor**
- Edit records, fields in bases with edit access
- Cannot create bases or change base structure

**4. Commenter**
- Add comments to records
- Cannot edit records or fields

**5. Read-only**
- View records, tables
- Cannot edit or comment

#### Granularity
- **Workspace-level**: Owner controls workspace
- **Base-level**: Permissions per base (different users can have different roles per base)
- **Table-level**: Enterprise tier can hide tables from users
- **Field-level**: **Most granular** — hide specific fields from users (Enterprise tier)
- **View-level**: Share specific views (filtered/sorted) with users (not entire table)

#### Guest Access
- **Invite external users**: Add collaborators to specific bases
- **Limitations**: Free tier (5 editors per base, unlimited commenters/read-only)
- **Use case**: Clients viewing project status, partners editing specific records

#### Custom Roles
- **Available**: Enterprise tier ($30+/user/month)
- **Custom role features**: Define permissions per base, field-level visibility

#### Field-Level Permissions (Unique to Airtable)
- **Hide fields**: Enterprise tier can hide specific fields from users (e.g., hide salary field from non-HR)
- **Most granular permissions** among all platforms
- **Use case**: CRM with sensitive data, HR databases, financial tracking

#### Collaboration Patterns

**Best for**:
- Teams managing structured data (CRM, inventory, HR databases)
- Organizations with sensitive data (field-level hiding critical)
- Cross-functional teams where different roles need different data visibility

**Not suitable for**:
- Field-level permissions require Enterprise tier ($30+/user/month, expensive)
- Small teams (overkill, too complex)

---

## Permission Complexity Ladder

### Simple → Complex Permission Needs

**If you need simple permissions** (everyone has equal access):
- **Trello** (2 roles, board-level)
- **Use case**: Small teams (3-8 people), flat hierarchy, no sensitive data

**If you need project-level permissions** (some users restricted to specific projects):
- **Linear** (4 roles, team-level) — for dev teams
- **Asana** (5 roles, project-level) — for cross-functional teams
- **Use case**: 10-25 people, external collaborators on specific projects

**If you need board/space-level permissions** (different boards for different teams):
- **Monday.com** (5 roles, board-level)
- **Use case**: 10-30 people, sales/marketing teams, client-facing boards

**If you need task-level permissions** (individual tasks with custom permissions):
- **ClickUp** (7 roles, task-level granularity)
- **Use case**: 20-50 people, agencies, complex org structures

**If you need field-level permissions** (hide specific data fields from users):
- **Airtable** (field-level hiding, Enterprise tier)
- **Use case**: CRM, HR databases, financial tracking, sensitive data

---

## Team Collaboration Scenarios

### Scenario 1: External Collaborators (Clients, Contractors)

**Need**: Invite clients/contractors to specific projects without seeing entire workspace

| Platform | Guest Access | Limitations | Cost |
|----------|--------------|-------------|------|
| **Asana** | ✅ Unlimited guests | Access specific projects only | Free tier: 15 total members (including guests) |
| **Linear** | ✅ Guest role | Read-only (cannot create issues) | All tiers: Unlimited guests (read-only) |
| **Monday.com** | ✅ Guests per board | Standard: 2 guests max, Pro: Unlimited | Pro tier: $12/user/month for unlimited guests |
| **ClickUp** | ✅ Guests per space | Free: 2 guests, Unlimited: 5 guests, Business: Unlimited | Business tier: $19/user/month for unlimited guests |
| **Trello** | ✅ Invite to board | Guests have full Member access (no read-only) | Free tier: Unlimited board invites |
| **Airtable** | ✅ Base collaborators | Free: 5 editors per base, unlimited commenters | Free tier: 5 editors per base |

**Best platform**: **Asana** (free tier unlimited guests, project-level access) or **Linear** (read-only guests for stakeholders)

---

### Scenario 2: Cross-Functional Teams (Marketing + Engineering + Ops)

**Need**: Different teams need access to different projects, some overlap

| Platform | Approach | Strengths | Weaknesses |
|----------|----------|-----------|------------|
| **Asana** | Project-level permissions | Cross-functional features, balanced | No task-level permissions |
| **ClickUp** | Space-level permissions | Most flexible (space → folder → list) | Complex, steep learning curve |
| **Monday.com** | Board-level permissions | Visual, easy to understand | Limited granularity (board-level only) |
| **Linear** | Team-level permissions | Works if teams are siloed (engineering only) | Not suitable for cross-functional |
| **Airtable** | Base-level permissions | Works if each function has separate base | Not optimized for task management |
| **Trello** | Board-level permissions | Simple, easy to set up | No workspace-level control |

**Best platform**: **Asana** (balanced, project-level, cross-functional features) or **ClickUp** (if team has complex needs)

---

### Scenario 3: Large Organizations (Multiple Teams, Departments)

**Need**: Workspace/organization structure with teams, departments, permissions hierarchy

| Platform | Org Structure | Team Management | Scalability |
|----------|---------------|-----------------|-------------|
| **Asana** | Workspace → Projects | Teams within workspace, project ownership | ⭐⭐⭐⭐⭐ Excellent (scales to 100s of users) |
| **ClickUp** | Workspace → Spaces → Folders → Lists | Hierarchical structure, most flexible | ⭐⭐⭐⭐⭐ Excellent (complex orgs) |
| **Monday.com** | Account → Workspaces → Boards | Multiple workspaces, board ownership | ⭐⭐⭐⭐ Very Good (scales to 50-100 users) |
| **Linear** | Organization → Teams → Projects | Team-based structure (engineering focus) | ⭐⭐⭐ Good (best for <50 engineers) |
| **Airtable** | Workspace → Bases → Tables | Database-centric structure | ⭐⭐⭐ Good (not optimized for large orgs) |
| **Trello** | Workspace → Boards | Flat structure (no hierarchy) | ⭐⭐ Fair (not suitable for large orgs) |

**Best platform**: **Asana** (enterprise-ready, scales to 100s of users) or **ClickUp** (for complex hierarchies)

---

### Scenario 4: Security-Sensitive (Finance, Legal, HR)

**Need**: Field-level permissions, hide sensitive data, audit logs

| Platform | Field-Level Permissions | Audit Logs | SSO/SAML | Cost |
|----------|-------------------------|------------|----------|------|
| **Airtable** | ✅ Yes (Enterprise) | ✅ Yes | ✅ Enterprise | $30+/user/month |
| **ClickUp** | ✅ Task-level (Business) | ✅ Business+ | ✅ Enterprise | $19/user/month (Business), $29/user (Enterprise) |
| **Monday.com** | ✅ Column-level (Enterprise) | ✅ Enterprise | ✅ Enterprise | $24+/user/month |
| **Asana** | ❌ No | ✅ Business+ | ✅ Enterprise | $25/user/month (Business) |
| **Linear** | ❌ No | ✅ Yes (all tiers) | ✅ Yes | $8/user/month+ |
| **Trello** | ❌ No | ✅ Enterprise | ✅ Enterprise | $17.50/user/month (Enterprise) |

**Best platform**: **Airtable** (field-level hiding, best for sensitive data) or **ClickUp** (task-level, cheaper than Airtable)

---

## SSO/SAML and Enterprise Security

### SSO/SAML Availability

| Platform | SSO/SAML | Tier | Cost | 2FA |
|----------|----------|------|------|-----|
| **Asana** | ✅ Yes | Enterprise | Custom quote | ✅ Free tier+ |
| **ClickUp** | ✅ Yes | Enterprise | $29/user/month | ✅ All tiers |
| **Linear** | ✅ Yes | Standard tier | $8/user/month | ✅ All tiers |
| **Monday.com** | ✅ Yes | Enterprise | $24+/user/month | ✅ Pro tier+ |
| **Airtable** | ✅ Yes | Enterprise | $30+/user/month | ✅ All tiers |
| **Trello** | ✅ Yes | Enterprise | $17.50/user/month | ✅ All tiers |

**Key insight**: SSO/SAML is **Enterprise-only** for most platforms, except **Linear** (available on Standard tier at $8/user/month — best value).

---

## Permission Model Rankings

### By Simplicity (Easiest → Most Complex)

1. **Trello** ⭐⭐⭐⭐⭐ (2 roles, board-level)
2. **Linear** ⭐⭐⭐⭐ (4 roles, team-level)
3. **Asana** ⭐⭐⭐⭐ (5 roles, project-level)
4. **Monday.com** ⭐⭐⭐ (5 roles, board-level)
5. **Airtable** ⭐⭐ (5 roles + field-level permissions)
6. **ClickUp** ⭐⭐ (7 roles + task-level permissions)

**Recommendation**: If team is small (3-10 people) and needs simple permissions, choose **Trello or Linear**.

---

### By Granularity (Least → Most Granular)

1. **Trello** (board-level only)
2. **Linear** (team-level)
3. **Asana** (project-level)
4. **Monday.com** (board-level, column-level at Enterprise)
5. **ClickUp** (workspace → space → folder → list → task)
6. **Airtable** (workspace → base → table → field-level)

**Recommendation**: If team needs granular permissions (task-level, field-level), choose **ClickUp or Airtable**.

---

### By Guest Access Flexibility

1. **Asana** ⭐⭐⭐⭐⭐ (unlimited guests at Free tier, project-level access)
2. **Linear** ⭐⭐⭐⭐⭐ (unlimited read-only guests, all tiers)
3. **Trello** ⭐⭐⭐⭐ (unlimited guests at Free tier, but no read-only)
4. **Airtable** ⭐⭐⭐⭐ (5 editors + unlimited commenters per base at Free tier)
5. **ClickUp** ⭐⭐⭐ (2 guests at Free, unlimited at Business $19/user/month)
6. **Monday.com** ⭐⭐ (2 guests at Standard, unlimited at Pro $12/user/month)

**Recommendation**: If team has many external collaborators (clients, contractors), choose **Asana or Linear**.

---

## Key Insights for Platform Selection

### If You Need Simple Permissions → **Trello or Linear**
Trello (2 roles) and Linear (4 roles) have the simplest permission models. Best for small teams (3-10 people) with flat hierarchy.

### If You Need Project-Level Permissions → **Asana**
Asana's project-level permissions are ideal for cross-functional teams (10-30 people) where different teams need access to different projects.

### If You Need Task-Level Permissions → **ClickUp**
ClickUp has the most granular task-level permissions. Best for agencies, large teams (20-50 people) with complex needs.

### If You Need Field-Level Permissions → **Airtable**
Airtable is the ONLY platform with field-level hiding (Enterprise tier). Essential for HR, finance, legal teams managing sensitive data.

### If You Have Many External Collaborators → **Asana or Linear**
Asana (unlimited guests at Free tier, project-level) and Linear (unlimited read-only guests) are best for teams with clients, contractors, external partners.

### If You Need Enterprise Security (SSO/SAML) → **Linear** (Best Value)
Linear offers SSO/SAML at Standard tier ($8/user/month), cheapest among all platforms. Others require Enterprise tier ($17.50-30/user/month).

---

## Recommendations by Team Size

### Small Teams (3-8 people)
- **Simple permissions**: **Trello** (free tier, 2 roles)
- **Dev teams**: **Linear** (free tier, 4 roles)

### Growing Teams (10-20 people)
- **Cross-functional**: **Asana** (project-level permissions)
- **Power users**: **ClickUp** (space-level permissions)

### Mid-Size Teams (20-50 people)
- **Complex orgs**: **ClickUp** (task-level granularity)
- **Enterprise security**: **Asana** (mature permissions, SSO/SAML)

### Large Teams (50+ people)
- **Enterprise-ready**: **Asana** (scales to 100s of users)
- **Sensitive data**: **Airtable** (field-level permissions)

---

## Next Steps

**Completed in S2**:
- ✅ Feature matrix (64 features, quantitative comparison)
- ✅ Pricing TCO analysis (4 scenarios, 1/3/5 year projections)
- ✅ Integrations ecosystem (native integrations, API quality, Zapier maturity)
- ✅ Permission models analysis (role-based access control, guest access, team collaboration patterns)

**Remaining S2 deliverables**:
- ⏳ Mobile experience analysis (iOS/Android feature parity, offline capabilities, UX evaluation)
- ⏳ Synthesis document (decision frameworks, cross-cutting insights)

---

**Last Updated**: 2025-11-12
**Phase**: S2 Comprehensive
**Document**: 3.131 Team Task Management - Permission Models & Team Collaboration
