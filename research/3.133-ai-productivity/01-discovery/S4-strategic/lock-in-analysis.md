# S4: Lock-In Analysis & Data Portability

**Focus**: How hard to switch if vendor dies? Migration effort, data loss
**Date**: 2025-11-09

---

## Executive Summary

**Lock-In Levels**:
- **Reclaim**: VERY LOW (tasks stay in Todoist/Asana, 30-60 min migration)
- **Trevor**: LOW (CSV export, 1-2 hour migration)
- **Todoist**: VERY LOW (API + CSV export, used by many integrations)
- **Motion**: MODERATE (all-in-one system, 2-4 hour migration, lose project structure)
- **Akiflow**: MODERATE (universal inbox, 2-3 hour migration)
- **Sunsama**: LOW (tasks in source systems, 1-2 hour migration)

**Comparison**: AI productivity lock-in < CRM (high lock-in) but > object storage (very low lock-in)

**Worst-case migration**: Motion → Reclaim = 2-4 hours (lose project dependencies, AI training data)

---

## Data Portability Analysis

### Motion: Moderate Lock-In

**What's portable**:
- ✅ Tasks (title, description, deadline): CSV export
- ✅ Calendar events: Stay in Google/Outlook (not Motion-specific)
- ✅ Projects (basic structure): CSV with parent-child relationships

**What's locked**:
- ❌ AI training data: Motion's AI learned your patterns (2-4 weeks to retrain elsewhere)
- ❌ Project dependencies: "Task A blocks Task B" (most tools don't support)
- ❌ Time estimates: Motion's learned estimates (1-2 weeks to recalibrate)
- ❌ Workload balancing: Team features (Motion-specific)

**Migration effort**: 2-4 hours
1. Export tasks to CSV (30 min)
2. Import to new tool (Reclaim, Trevor, Todoist) (1-2 hours)
3. Recreate project structure (1-2 hours if complex)

**AI recalibration**: 2-4 weeks (new tool learns your patterns)

**Lock-in level**: MODERATE (2-4 hour migration, lose advanced features)

---

### Reclaim: Very Low Lock-In

**What's portable**:
- ✅ Tasks: Already in Todoist/Asana (no migration needed, just disconnect Reclaim)
- ✅ Calendar events: Stay in Google/Outlook
- ✅ Habits: Exportable (CSV), but re-create in new tool

**What's locked**:
- ❌ Habit history: Reclaim-specific (which weeks you exercised, focus time achieved)
- ❌ AI patterns: Reclaim's learned preferences (1-2 weeks to retrain)

**Migration effort**: 30-60 min
1. Disconnect Reclaim from Todoist/Asana (5 min)
2. Connect new tool (Motion, Trevor) to Todoist/Asana (15-30 min)
3. Recreate habits in new tool (10-20 min)

**AI recalibration**: 1-2 weeks (faster than Motion, simpler AI)

**Lock-in level**: VERY LOW (tasks stay in source system, 30-60 min migration)

---

### Trevor AI: Low Lock-In

**What's portable**:
- ✅ Tasks: CSV export or bidirectional Todoist sync
- ✅ Calendar events: Stay in Google/Outlook
- ✅ Time blocks: Exportable (if needed)

**What's locked**:
- ❌ Time block history: Trevor-specific (visual placement data)
- ❌ AI duration estimates: Trevor's learned estimates (minimal, AI is light)

**Migration effort**: 1-2 hours
1. Export tasks from Trevor (CSV) OR keep in Todoist (30 min)
2. Import to new tool (30-60 min)

**AI recalibration**: <1 week (Trevor AI is light, minimal learning)

**Lock-in level**: LOW (1-2 hour migration, minimal AI to retrain)

---

### Akiflow: Moderate Lock-In

**What's portable**:
- ✅ Tasks: Bidirectional sync with Todoist/Asana/Linear (stay in source systems)
- ✅ Calendar events: Stay in Google/Outlook
- ⚠️ Universal inbox tasks: Tasks created in Akiflow (from Gmail/Slack) need export

**What's locked**:
- ❌ Universal inbox history: Akiflow-specific (which emails became tasks)
- ❌ AI deduplication: Akiflow's learned patterns (fuzzy matching)

**Migration effort**: 2-3 hours
1. Export Akiflow-specific tasks (CSV) (1 hour)
2. Import to new tool (1-2 hours)
3. Re-sync source systems (Todoist, Asana, Linear) with new tool (30 min)

**Lock-in level**: MODERATE (2-3 hour migration, lose universal inbox history)

---

### Todoist: Very Low Lock-In

**What's portable**:
- ✅ Tasks: Full API + CSV export (used by 100+ integrations)
- ✅ Projects: Hierarchical structure exportable
- ✅ Labels, priorities, filters: Exportable

**What's locked**:
- ❌ Karma points: Todoist-specific gamification
- ❌ Productivity trends: Todoist analytics (not critical)

**Migration effort**: 30-60 min
1. Export via API or CSV (10 min)
2. Import to new tool (20-50 min, depending on complexity)

**Lock-in level**: VERY LOW (industry-standard task format, many integrations)

---

### Sunsama: Low Lock-In

**What's portable**:
- ✅ Tasks: Already in Todoist/Asana (no migration needed)
- ✅ Calendar events: Stay in Google/Outlook
- ⚠️ Daily planning notes: Exportable (CSV), but Sunsama-specific

**What's locked**:
- ❌ Reflection history: Sunsama-specific (daily/weekly reflections)
- ❌ Planning ritual: Workflow (not data)

**Migration effort**: 1-2 hours
1. Export planning notes (if needed) (30 min)
2. Disconnect Sunsama, connect new tool to task sources (30-60 min)

**Lock-in level**: LOW (tasks stay in source systems, 1-2 hour migration)

---

## Lock-In Comparison Table

| Provider | Data Export | Migration Effort | AI Recalibration | **Lock-In Level** |
|----------|-------------|------------------|------------------|-------------------|
| **Reclaim** | CSV + tasks in source systems | 30-60 min | 1-2 weeks | VERY LOW |
| **Todoist** | Full API + CSV | 30-60 min | N/A (no AI) | VERY LOW |
| **Trevor** | CSV + Todoist sync | 1-2 hours | <1 week | LOW |
| **Sunsama** | CSV + tasks in source systems | 1-2 hours | N/A (minimal AI) | LOW |
| **Motion** | CSV | 2-4 hours | 2-4 weeks | MODERATE |
| **Akiflow** | CSV + source system sync | 2-3 hours | 1-2 weeks | MODERATE |

---

## Lock-In Benchmarks (Cross-Industry)

### Very Low Lock-In (Easy Switch):
- **Object storage** (S3, GCS): Standard API (s3cmd, gsutil), migrate in hours
- **Email** (Gmail, Outlook): IMAP/POP3 export, migrate in 1-2 hours
- **Todoist, Reclaim**: Standard task format, 30-60 min migration

### Low Lock-In (1-2 Day Migration):
- **CMS** (WordPress, Drupal): Content exportable, 1-2 days to migrate
- **Trevor, Sunsama**: CSV export, 1-2 hours migration

### Moderate Lock-In (1-2 Week Migration):
- **Motion, Akiflow**: Custom features (dependencies, universal inbox), 2-4 hours + 2-4 weeks AI recalibration
- **Project management** (Asana, Linear): Task export, lose workflow automation

### High Lock-In (Multi-Month Migration):
- **CRM** (Salesforce): Custom objects, workflows, integrations = 1-3 months migration
- **ERP** (SAP, Oracle): Business logic embedded, 6-12 months migration

**Verdict**: AI productivity tools = LOW to MODERATE lock-in (closer to email than CRM)

---

## Mitigation Strategies

### 1. Choose Low Lock-In Providers
- **Reclaim + Todoist**: Tasks stay in Todoist (if Reclaim dies, keep Todoist)
- **Avoid**: Motion all-in-one (higher lock-in, but justified if need advanced AI)

### 2. Export Data Regularly (Quarterly)
- Motion: Export tasks to CSV (every 3 months)
- Akiflow: Export universal inbox tasks (every 3 months)
- **Effort**: 15 min/quarter
- **Benefit**: If vendor dies, recent backup available

### 3. Use Standard Formats (Calendar, Task APIs)
- Google Calendar, Outlook: Industry-standard calendar APIs (portable)
- Todoist: Industry-standard task format (many integrations)
- **Avoid**: Proprietary task systems (Motion's all-in-one)

### 4. Have Migration Plan Ready
- Identify backup tool (if Motion dies → migrate to Reclaim)
- Test export/import (verify CSV export works)
- **Effort**: 1-2 hours (one-time)
- **Benefit**: If vendor dies, execute migration in <1 day

### 5. Diversify Tools (Reduce Single-Vendor Risk)
- Use Reclaim (calendar optimization) + Todoist (task management)
- If Reclaim dies → keep Todoist, switch to Motion
- **Trade-off**: Two tools vs one, but lower risk

---

## Worst-Case Migration Scenarios

### Scenario 1: Motion Dies (Moderate Impact)

**Timeline**:
- Day 1: Motion announces shutdown (30-60 day notice typical)
- Week 1: Export tasks to CSV (2 hours)
- Week 2: Choose new tool (Reclaim or Trevor), import tasks (2 hours)
- Week 3-6: AI recalibration (new tool learns patterns)

**Data loss**:
- ❌ Project dependencies (Reclaim/Trevor don't support)
- ❌ AI training data (2-4 weeks to retrain)
- ✅ Tasks, deadlines, descriptions preserved

**Total cost**: 4 hours migration + 2-4 weeks recalibration = $200-400 (@ $50/hour equivalent)

---

### Scenario 2: Reclaim Dies (Low Impact)

**Timeline**:
- Day 1: Reclaim announces shutdown
- Week 1: Disconnect Reclaim from Todoist/Asana (5 min)
- Week 1: Connect new tool (Motion or Trevor) to Todoist/Asana (30 min)
- Week 2-3: AI recalibration (if Motion), or manual time blocking (if Trevor)

**Data loss**:
- ❌ Habit history (Reclaim-specific)
- ✅ Tasks, projects preserved (in Todoist/Asana)

**Total cost**: 1 hour migration + 1-2 weeks recalibration = $50-100

---

### Scenario 3: Todoist Dies (Very Low Impact)

**Timeline**:
- Day 1: Todoist announces shutdown (unlikely, but hypothetically)
- Week 1: Export tasks via API or CSV (30 min)
- Week 1: Import to new tool (Motion, Reclaim, Things, Asana) (1 hour)

**Data loss**:
- ❌ Karma points (gamification)
- ✅ Tasks, projects, labels, priorities preserved

**Total cost**: 1.5 hours migration = $75

---

## Key Insights

1. **Reclaim = lowest lock-in**: Tasks stay in Todoist/Asana (30-60 min migration if dies)
2. **Motion = moderate lock-in**: All-in-one (2-4 hour migration, lose dependencies)
3. **AI recalibration = hidden cost**: 1-4 weeks for new tool to learn patterns
4. **Lock-in < CRM**: AI productivity = 2-4 hour migration vs CRM = 1-3 months
5. **Mitigation easy**: Quarterly CSV export (15 min) + migration plan (1-2 hours)

**Recommendation**:
- **Risk-averse**: Use Reclaim + Todoist (very low lock-in)
- **Advanced AI needs**: Use Motion (accept moderate lock-in for capabilities)
- **Mitigation**: Export CSV quarterly, have backup tool identified
