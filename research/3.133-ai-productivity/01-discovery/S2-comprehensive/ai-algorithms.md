# S2: AI Algorithms Deep-Dive

**Methodology**: MPSE v3.0 - S2 (Comprehensive Analysis)
**Focus**: How each tool's AI scheduling actually works
**Date**: 2025-11-09

---

## Executive Summary

**Key Finding**: AI sophistication varies dramatically across providers - from rule-based "AI" (Trevor) to true constraint-solver optimization (Motion).

**Sophistication Spectrum**:
1. **Most Advanced**: Motion (constraint solver + dependency graph + deadline propagation)
2. **Advanced**: Reclaim.ai (habit optimization + calendar analysis + pattern learning)
3. **Intermediate**: Akiflow (time estimation + priority scoring)
4. **Basic**: Trevor AI (rule-based suggestions, mostly manual)
5. **Minimal**: Sunsama (guided planning, human-driven)

**What Makes AI "Sophisticated"**:
- ✅ **Constraint solving**: Optimizes across multiple conflicting requirements
- ✅ **Dependency awareness**: Understands task relationships (A blocks B)
- ✅ **Pattern learning**: Adapts to user behavior over time
- ✅ **Proactive rescheduling**: Automatically adjusts when calendar changes
- ✅ **Context-awareness**: Understands meeting types, energy levels, focus needs

---

## 1. Motion: "Project Manager AI"

### Algorithm Architecture

**Core Technology**: Constraint satisfaction solver + directed acyclic graph (DAG) scheduler

**Components**:
1. **Task Graph Builder**: Constructs dependency graph from project structure
2. **Constraint Solver**: Optimizes task placement given multiple constraints
3. **Priority Scorer**: Ranks tasks by urgency, deadline, dependencies
4. **Calendar Optimizer**: Finds best time slots for each task
5. **Real-time Rescheduler**: Cascades changes when calendar updates

---

### How It Works: Step-by-Step

**Input**: Project "Launch Website" (Due: Nov 15, 20 hours total)
- Task A: "Design mockups" (6 hours, no dependencies)
- Task B: "Develop site" (10 hours, depends on A)
- Task C: "User testing" (4 hours, depends on B)

**Step 1: Build Dependency Graph**
```
A (Design) → B (Develop) → C (Testing) → [Nov 15 Deadline]
```

**Step 2: Deadline Propagation (Work Backwards)**
- Nov 15: Deadline
- Nov 14: C must finish (4 hours before deadline)
- Nov 12: B must finish (10 hours before C starts)
- Nov 10: A must finish (6 hours before B starts)
- **Conclusion**: Must start A by Nov 8 (2 days buffer)

**Step 3: Constraint Collection**
- Work hours: 9 AM - 6 PM (9 hours/day max)
- Existing meetings: Tue 2-3 PM, Wed 10-11 AM, Thu 3-5 PM
- Focus time preference: Morning (9-12 AM best for deep work)
- No-meeting days: Friday (prefer focus work)

**Step 4: Optimization (Constraint Solver)**

Motion solves: **Minimize deadline risk + Maximize focus time quality**

**Variables**:
- `start_time_A`, `start_time_B`, `start_time_C`

**Constraints**:
1. `start_time_B >= end_time_A` (dependency)
2. `start_time_C >= end_time_B` (dependency)
3. `end_time_C <= Nov 15` (deadline)
4. Tasks only in 9 AM - 6 PM blocks
5. Avoid scheduled meetings
6. Prefer mornings for focus work

**Solution** (simplified):
- Mon Nov 8, 9 AM - 12 PM: Task A (3h)
- Mon Nov 8, 1 PM - 4 PM: Task A (3h) ✅ Complete
- Tue Nov 9, 9 AM - 12 PM: Task B (3h)
- Tue Nov 9, 3 PM - 6 PM: Task B (3h)
- Wed Nov 10, 9 AM - 10 AM: (meeting conflict)
- Wed Nov 10, 11 AM - 2 PM: Task B (3h)
- Wed Nov 10, 2 PM - 3 PM: Task B (1h) ✅ Complete
- Thu Nov 11, 9 AM - 12 PM: Task C (3h)
- Thu Nov 11, 3 PM - 4 PM: (meeting conflict)
- Fri Nov 12, 9 AM - 10 AM: Task C (1h) ✅ Complete

**Step 5: Proactive Rescheduling**

**Scenario**: Wed 9 AM meeting added (blocks 3 hours of Task B)

**Motion's response** (automatic, no user action):
1. Detect conflict: Wed 9 AM slot now unavailable
2. Re-run solver with updated constraints
3. Push Task B completion → Thu morning
4. Push Task C start → Thu afternoon
5. Update calendar instantly

**User sees**: Tasks automatically shift, no manual work needed

---

### Sophistication Analysis

**What Makes Motion Advanced**:

1. **Dependency-Aware Scheduling**
   - Most tools schedule tasks independently
   - Motion understands "Task B can't start until Task A completes"
   - Optimizes entire project timeline, not just individual tasks

2. **Deadline Propagation**
   - Works backwards from final deadline
   - Calculates "latest start time" for each task
   - Flags projects at risk (impossible to meet deadline)

3. **Constraint Satisfaction Solving**
   - Juggles 10-20 constraints simultaneously (work hours, meetings, preferences, deadlines)
   - Finds optimal solution across all constraints
   - Similar to Google Calendar's "Find a Time" but for tasks, not meetings

4. **Real-Time Rescheduling**
   - Calendar change → automatic cascade adjustment
   - No "stale schedule" problem (always current)
   - Handles 50+ tasks rescheduling in <1 second

5. **Pattern Learning** (Over 2-4 Weeks)
   - "User always marks design tasks as taking 2× estimated time" → inflate estimates
   - "User most productive 9-11 AM" → prioritize important tasks then
   - "User takes 30 min to context-switch after meetings" → add buffer

---

### Technical Limitations

**What Motion AI Can't Do**:

1. **No Multi-Person Optimization** (Individual Plan)
   - Can't optimize across team calendars
   - Team plan improves this, but still limited

2. **No Energy-Level Awareness**
   - Knows time-of-day patterns, but not daily energy fluctuations
   - Doesn't understand "low-energy day = avoid hard tasks"

3. **No True LLM Integration** (Yet)
   - Uses custom ML models, not GPT-4/Claude
   - Can't understand natural language nuance ("do this when you feel creative")

4. **Overfits to Urgency**
   - Heavily weights deadlines
   - Can under-prioritize important-but-not-urgent work (Eisenhower matrix blind spot)

5. **Limited Task Complexity Modeling**
   - Task = duration + deadline + dependencies
   - Doesn't understand "this task requires deep focus" vs "mindless admin"

---

## 2. Reclaim.ai: "Habit AI"

### Algorithm Architecture

**Core Technology**: Calendar pattern analyzer + recurring task optimizer + conflict resolver

**Components**:
1. **Habit Scheduler**: Optimizes recurring commitments (e.g., "Exercise 3×/week")
2. **Calendar Analyzer**: Learns when you have meetings, focus time, free slots
3. **Priority Ranker**: Scores habits/tasks by flexibility, importance
4. **Buffer Time Calculator**: Adds recovery time after meetings
5. **Conflict Resolver**: Moves tasks when calendar conflicts arise

---

### How It Works: Step-by-Step

**Input**: "Deep Work" habit (4 hours/day, Mon-Fri)

**Step 1: Analyze Historical Calendar Patterns**

Reclaim looks at past 2-4 weeks:
- **Mon**: Meetings 10 AM, 2 PM, 4 PM (6 hours free)
- **Tue**: Meetings 11 AM, 3 PM (7 hours free)
- **Wed**: Meetings all afternoon (4 hours free AM only)
- **Thu**: Meetings morning (5 hours free PM)
- **Fri**: Few meetings (8 hours free)

**Insights**:
- Best focus time: **Mornings (Mon, Wed, Fri)** - least meetings
- Avoid: **Wed/Thu afternoons** - meeting-heavy
- Friday = best day for deep work (fewest interruptions)

**Step 2: Define "Good Slot" Criteria**

For "Deep Work" (4-hour habit):
- ✅ **Long blocks**: Need 2-4 hour contiguous slots
- ✅ **Morning preferred**: 9 AM - 12 PM optimal
- ✅ **Low meeting density**: Days with <3 meetings
- ❌ **Avoid post-lunch**: 1-2 PM = low energy
- ❌ **Avoid Fridays before 3-day weekend**: Motivation low

**Step 3: Optimal Scheduling**

**Week 1**:
- **Mon 9 AM - 1 PM**: Deep Work (4h) - morning block, no conflicts
- **Tue 9 AM - 11 AM**: Deep Work (2h) - meeting at 11, partial slot
- **Wed 9 AM - 1 PM**: Deep Work (4h) - morning block before afternoon meetings
- **Thu**: Skip (meeting-heavy)
- **Fri 9 AM - 1 PM**: Deep Work (4h) - best day

**Total**: 14 hours scheduled (target: 20 hours/week = 4h/day × 5 days)
**Shortfall**: 6 hours → Reclaim suggests "reduce to 3h/day" or "work some afternoons"

**Step 4: Adaptive Rescheduling**

**Scenario**: Wed 10 AM meeting added

**Reclaim's response**:
1. **Detect conflict**: Wed 10 AM meeting blocks 1 hour of Deep Work
2. **Check flexibility**: Deep Work = habit (flexible, can move)
3. **Find alternative**: Tue 2-4 PM slot available
4. **Move**: Wed Deep Work → Tue 2-5 PM (split across two days)
5. **Notify user**: "Deep Work moved to Tue due to Wed meeting"

**User sees**: Habit automatically adjusts, maintains weekly target

---

### Sophistication Analysis

**What Makes Reclaim Advanced**:

1. **Habit Optimization**
   - Understands "3×/week for 1 hour each" ≠ "3 consecutive hours"
   - Distributes across week to balance workload
   - Adapts to calendar density (meeting-heavy week = reduce habits)

2. **Calendar Pattern Learning**
   - "Tuesdays always have afternoon meetings" → schedule habits in AM
   - "User declines 8 AM meetings" → avoid early scheduling
   - Learns over 4-8 weeks, improves accuracy

3. **Buffer Time Intelligence**
   - After 1-hour meeting → add 10-min buffer
   - After 3-hour meeting → add 30-min buffer (decompression)
   - Before important meetings → add 15-min prep time

4. **Flexibility Scoring**
   - Hard deadline task = inflexible (schedule first)
   - Habit = flexible (fill gaps)
   - Meeting = immovable (work around)

5. **Team Coordination** (Business Plan)
   - Smart 1:1s: Finds mutual availability for recurring meetings
   - Team calendar: Shows who's available for ad-hoc sync
   - No-meeting days: Entire team blocks Fridays for focus

---

### Technical Limitations

**What Reclaim AI Can't Do**:

1. **No Dependency Understanding**
   - Task A doesn't "block" Task B
   - Schedules tasks independently (no project-level optimization)

2. **Simpler Task Model**
   - Task = duration + deadline + priority
   - No subtasks, no complex project structure

3. **Less Aggressive Rescheduling**
   - Requires user confirmation for some changes
   - Motion more autonomous (reschedules without asking)

4. **Habit-Centric, Not Project-Centric**
   - Excellent for recurring work (exercise, deep work, admin)
   - Weaker for one-off projects with dependencies

5. **No Multi-Calendar Optimization** (Free Tier)
   - Can sync work + personal calendars, but scheduling priority unclear
   - Business plan improves this

---

## 3. Trevor AI: "Hybrid AI + Manual"

### Algorithm Architecture

**Core Technology**: Rule-based suggestions + manual drag-drop time blocking

**Components**:
1. **Task Duration Estimator**: Suggests how long task will take
2. **Priority Suggester**: Recommends "do this today" tasks
3. **Time Block Generator**: Creates calendar blocks (user places them)
4. **Schedule Optimizer**: Suggests best times (user confirms)

---

### How It Works

**Input**: 10 tasks in to-do list

**Step 1: Duration Estimation**

Trevor analyzes:
- Task title: "Write blog post" → suggests 2 hours
- Historical data: User's past "write" tasks took 1.5-3 hours
- **Suggestion**: 2 hours

**User**: Adjusts to 3 hours (Trevor learns for next time)

**Step 2: Priority Scoring** (Rule-Based)

**Rules**:
1. Deadline today = highest priority
2. Deadline this week = high priority
3. No deadline = low priority
4. User-set priority overrides

**Example**:
- "Submit report" (due today) → Priority 1
- "Review slides" (due Friday) → Priority 2
- "Brainstorm ideas" (no deadline) → Priority 3

**Step 3: AI Suggestions**

Trevor suggests:
- "Work on 'Submit report' first (due today, 2 hours)"
- "Best time: 9-11 AM (your most productive hours)"

**Step 4: Manual Placement**

**User action required**: Drag "Submit report" task to calendar (9-11 AM block)

**Trevor**: Creates 9-11 AM calendar event, marks task in progress

**Step 5: Adaptive Learning** (Weak)

Trevor notices:
- User always schedules "writing" tasks in AM
- User often extends 2-hour tasks to 3 hours

**Next time**: Suggests 3 hours for writing, recommends AM slot

---

### Sophistication Analysis

**What Makes Trevor "AI"**:

1. **Time Estimation**: Uses historical data to suggest durations
2. **Priority Suggestions**: Rule-based, but learns from overrides
3. **Optimal Time Suggestions**: Analyzes when you schedule similar tasks

**What's NOT AI**:

1. **Manual Placement**: User drags tasks to calendar (no auto-scheduling)
2. **No Rescheduling**: Calendar change → user manually adjusts
3. **No Dependency Awareness**: Can't understand task relationships
4. **Rule-Based Logic**: "If deadline today, priority = high" (not learned)

**Verdict**: Trevor AI = "AI-assisted manual planning" (not fully autonomous AI scheduling)

---

## 4. Akiflow: "Task Aggregation + Light AI"

### Algorithm Architecture

**Core Technology**: Universal inbox + time blocking + basic AI suggestions

**Components**:
1. **Task Aggregator**: Pulls from Todoist, Asana, Gmail, Slack
2. **Duration Estimator**: Suggests task lengths
3. **Time Blocker**: Creates calendar events for tasks
4. **Priority Ranker**: Sorts tasks by importance

---

### How It Works

**Input**: Tasks from 5 sources (Todoist, Gmail, Slack, Linear, Asana)

**Step 1: Aggregation**

Akiflow pulls:
- Todoist: 15 tasks
- Gmail: 3 "follow-up" emails
- Slack: 2 action items from messages
- Linear: 5 engineering issues
- Asana: 7 project tasks

**Total**: 32 tasks in "universal inbox"

**Step 2: Deduplication**

Akiflow detects:
- "Fix login bug" (Linear) = "Login issue" (Slack) → merge

**Step 3: Priority Scoring** (AI-Based)

**Factors**:
1. Deadline proximity (due today = +50 points)
2. Source priority (Linear P0 = +30 points)
3. Mentioned in multiple places (+20 points)
4. User historically completes similar tasks first (+10 points)

**Ranked List**:
1. "Submit expense report" (due today, 85 pts)
2. "Fix login bug" (P0, mentioned in Slack, 80 pts)
3. "Review PR" (due tomorrow, 60 pts)
...

**Step 4: Time Blocking Suggestions**

Akiflow suggests:
- "Submit expense report" → 30 min, schedule 9-9:30 AM
- "Fix login bug" → 2 hours, schedule 9:30-11:30 AM
- "Review PR" → 45 min, schedule 2-2:45 PM

**User**: Confirms or adjusts, Akiflow creates calendar blocks

---

### Sophistication Analysis

**What Makes Akiflow AI**:

1. **Universal Inbox Aggregation**: Pulls tasks from everywhere (reduces context-switching)
2. **Deduplication**: Uses fuzzy matching to detect duplicate tasks
3. **Priority Scoring**: Learns from user behavior (which tasks you complete first)

**Limitations**:

1. **No Auto-Scheduling**: Suggests times, user must confirm
2. **No Dependency Awareness**: Tasks scheduled independently
3. **Simple Time Blocking**: Duration + time slot (no optimization)
4. **Less Learning**: Primarily rule-based with light ML

**Verdict**: Akiflow = "Smart task aggregation + manual time blocking" (AI for organization, not scheduling)

---

## 5. Sunsama: "Guided Planning AI"

### Algorithm Architecture

**Core Technology**: Daily planning ritual + light AI suggestions + human-driven workflow

**Components**:
1. **Daily Review Workflow**: Guides user through planning process
2. **Task Import Suggestions**: Recommends tasks to pull from integrations
3. **Time Estimate Prompts**: Asks user to estimate durations
4. **Reflection Prompts**: End-of-day review (what got done?)

---

### How It Works

**Daily Planning Flow** (10-15 minutes):

**Step 1: Import Tasks**

Sunsama suggests:
- "Pull in 3 overdue tasks from Todoist"
- "Import 2 Asana tasks due this week"
- "Add follow-up from yesterday's meeting notes"

**User**: Reviews, selects which to add

**Step 2: Set Intentions**

Sunsama asks: "What are your top 3 priorities today?"

**User**: "1. Submit report, 2. Fix bug, 3. Team sync"

**Step 3: Time Estimation**

For each task, Sunsama prompts: "How long will this take?"

**User**:
- "Submit report" → 2 hours
- "Fix bug" → 3 hours
- "Team sync" → 1 hour

**Step 4: Capacity Check**

Sunsama calculates:
- Total planned: 6 hours
- Calendar free time: 5 hours (after meetings)
- **Warning**: "You've planned 6 hours, but only have 5 hours free. Consider deferring a task."

**Step 5: Time Blocking** (Manual)

**User**: Drags tasks to calendar (Sunsama creates events)

**Step 6: End-of-Day Reflection**

Sunsama prompts: "What did you accomplish today? What's rolling over to tomorrow?"

**User**: Reviews, moves incomplete tasks to next day

---

### Sophistication Analysis

**What Makes Sunsama "AI"**:

1. **Task Suggestions**: Recommends which tasks to import based on deadlines
2. **Capacity Warnings**: Flags over-commitment (planned > available time)
3. **Pattern Recognition**: Learns which task sources you prioritize

**What's NOT AI**:

1. **Human-Driven Workflow**: User makes all decisions (AI just guides)
2. **No Auto-Scheduling**: User manually places tasks on calendar
3. **No Rescheduling**: Calendar change → user adjusts manually
4. **Minimal Learning**: Doesn't deeply adapt to user behavior

**Verdict**: Sunsama = "Mindful planning tool with AI suggestions" (focus on intentionality, not automation)

---

## Sophistication Comparison Table

| Feature | Motion | Reclaim.ai | Trevor AI | Akiflow | Sunsama |
|---------|--------|-----------|-----------|---------|---------|
| **Auto-Scheduling** | ✅ Full | ✅ Full | ❌ Manual | ⚠️ Suggests | ❌ Manual |
| **Dependency Awareness** | ✅ Yes | ❌ No | ❌ No | ❌ No | ❌ No |
| **Deadline Propagation** | ✅ Yes | ❌ No | ❌ No | ❌ No | ❌ No |
| **Pattern Learning** | ✅ Deep | ✅ Moderate | ⚠️ Light | ⚠️ Light | ⚠️ Minimal |
| **Proactive Rescheduling** | ✅ Automatic | ✅ Automatic | ❌ Manual | ❌ Manual | ❌ Manual |
| **Constraint Solving** | ✅ Yes | ⚠️ Basic | ❌ No | ❌ No | ❌ No |
| **Habit Optimization** | ⚠️ Basic | ✅ Advanced | ❌ No | ❌ No | ❌ No |
| **AI Sophistication** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐½ | ⭐½ |

---

## What Makes AI "Sophisticated" vs "Basic"?

### Sophisticated AI Characteristics:

1. **Autonomous Decision-Making**
   - AI makes scheduling decisions without user input
   - Automatically reschedules when calendar changes
   - **Example**: Motion, Reclaim

2. **Multi-Constraint Optimization**
   - Balances 10+ constraints simultaneously (deadlines, meetings, preferences, energy levels)
   - Finds optimal solution, not just "good enough"
   - **Example**: Motion's constraint solver

3. **Context Awareness**
   - Understands task relationships (dependencies, priorities)
   - Knows meeting types, user patterns, energy levels
   - **Example**: Motion's project dependencies

4. **Deep Learning & Adaptation**
   - Improves accuracy over weeks/months
   - Learns from corrections ("user always extends estimates")
   - **Example**: Motion, Reclaim pattern learning

5. **Proactive, Not Reactive**
   - AI reschedules before you notice a problem
   - Flags risks (project won't meet deadline)
   - **Example**: Motion's deadline warnings

---

### Basic "AI" Characteristics:

1. **Rule-Based Logic**
   - "If deadline today, priority = high" (static rules)
   - No learning or adaptation
   - **Example**: Trevor AI priority scoring

2. **Suggestion, Not Decision**
   - AI suggests, user must confirm/place
   - No autonomous scheduling
   - **Example**: Akiflow time blocking

3. **Single-Constraint Focus**
   - Optimizes for one thing (e.g., deadlines only)
   - Doesn't balance multiple factors
   - **Example**: Sunsama capacity warnings

4. **Minimal Learning**
   - Static behavior, doesn't improve over time
   - No pattern recognition
   - **Example**: Sunsama daily planning

5. **Reactive, Not Proactive**
   - User must initiate actions
   - No automatic rescheduling
   - **Example**: Trevor, Sunsama

---

## Technical Deep-Dive: Motion's Constraint Solver

### Simplified Pseudocode

```python
def schedule_tasks(tasks, calendar, user_preferences):
    # Step 1: Build dependency graph
    task_graph = build_dependency_graph(tasks)

    # Step 2: Propagate deadlines backwards
    for task in reversed(topological_sort(task_graph)):
        task.latest_start = task.deadline - task.duration
        for dependent in task.dependents:
            dependent.latest_start = min(dependent.latest_start, task.latest_start - dependent.duration)

    # Step 3: Define constraints
    constraints = [
        # Time constraints
        lambda slot: slot.start >= work_hours.start and slot.end <= work_hours.end,

        # Meeting conflicts
        lambda slot: not overlaps(slot, calendar.meetings),

        # Dependencies
        lambda task: all(d.end_time < task.start_time for d in task.dependencies),

        # Deadlines
        lambda task: task.end_time <= task.deadline,

        # Preferences
        lambda slot: prefer_morning_for_focus_work(slot, task),
    ]

    # Step 4: Optimize (constraint satisfaction problem)
    solution = constraint_solver.solve(
        variables=[(task, start_time) for task in tasks],
        constraints=constraints,
        objective=minimize(deadline_risk) + maximize(focus_time_quality)
    )

    # Step 5: Place tasks on calendar
    for task, start_time in solution:
        calendar.add_event(task, start_time, start_time + task.duration)

    return calendar
```

**Complexity**: NP-hard problem (similar to job-shop scheduling)
**Motion's approach**: Heuristic solver + branch-and-bound (finds good solution in <1 second)

---

## Verdict: AI Sophistication Rankings

### Tier 1: Advanced AI (Fully Autonomous)
1. **Motion** (⭐⭐⭐⭐⭐): Constraint solving, dependency-aware, deadline propagation
2. **Reclaim.ai** (⭐⭐⭐⭐): Habit optimization, pattern learning, auto-rescheduling

### Tier 2: Intermediate AI (Assisted Automation)
3. **Akiflow** (⭐⭐½): Task aggregation, priority scoring, light learning

### Tier 3: Basic AI (Suggestions Only)
4. **Trevor AI** (⭐⭐): Rule-based suggestions, manual placement
5. **Sunsama** (⭐½): Guided workflow, minimal AI

---

## Key Insights

1. **"AI" is a spectrum**: From fully autonomous (Motion) to glorified rules (Sunsama)

2. **Sophistication ≠ Better for everyone**: Some users prefer manual control (Trevor, Sunsama)

3. **Dependency awareness = game-changer**: Only Motion handles project-level scheduling

4. **Pattern learning takes time**: 2-4 weeks minimum (don't judge AI in first week)

5. **Trade-off: Automation vs Control**: Motion = hands-off, Trevor = hands-on

**Recommendation**:
- Need autonomous scheduling → **Motion or Reclaim**
- Prefer manual control → **Trevor or Sunsama**
- Task aggregation focus → **Akiflow**
