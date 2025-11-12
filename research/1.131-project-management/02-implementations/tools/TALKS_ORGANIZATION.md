# Talks Organization System

Complete system for managing speaking opportunities and topic development in Vikunja.

## Project Structure

```
Talks (Parent Project 14153)
│
├── Opportunities (Project 13481) - formerly "Talks"
│   └── Speaking events, conferences, and engagement opportunities
│       ├── 💡 Ideas - New opportunities to consider
│       ├── 📝 Proposal Writing - Actively drafting submissions
│       ├── 📤 Submitted - Waiting for response
│       ├── ✅ Accepted - Confirmed speaking engagements
│       ├── 🎯 Preparing - Slides, demos, rehearsal
│       └── 🎤 Delivered - Completed talks
│
└── Topics (Project 14154)
    └── Talk content, abstracts, and intellectual property
        ├── 💡 Ideas - Raw concepts, brainstorming
        ├── 📐 Prepare - Research, outline, draft
        ├── ✅ Ready - Polished, submittable abstracts
        └── 🔧 Refinement - Post-delivery improvements
```

## Topic Labels

Use labels to categorize topics by domain/audience:

| Label | ID | Color | Description |
|-------|------|-------|-------------|
| Events | 7021 | Purple (#9B59B6) | Event tech, conferences, hospitality |
| Finance | 7022 | Orange (#F39C12) | CFO advisory, FP&A, financial planning |
| Marketing | 7023 | Pink (#E91E63) | Marketing operations, growth, strategy |
| Operations | 7024 | Blue Grey (#607D8B) | Process optimization, efficiency |
| Leadership | 7025 | Dark Purple (#8E44AD) | Management, team building, strategy |
| Technology | 7026 | Blue (#3498DB) | Software architecture, development |
| Academic | 7027 | Green (#2ECC71) | Research, education, scholarship |
| Arts & Culture | 7028 | Red (#E74C3C) | Creative industries, cultural work |

**Note:** Topics can have multiple labels (e.g., "Anticipatory Experience Design" = Events + Technology)

## Workflow: From Idea to Delivery

### 1. Opportunity Arrives
**Example:** Email about inControl Summit 2026

**Action:**
```bash
# Use add_talk.py to quickly capture
cd /home/ivanadmin/spawn-solutions/research/1.131-project-management/02-implementations/tools
uv run python add_talk.py \
  --title "inControl Summit 2026 - Düsseldorf" \
  --event-date 2026-06-02 \
  --location "Düsseldorf, Germany" \
  --focus "AI-focused event industry conference"
```

**Result:** Task created in `Opportunities → 💡 Ideas`

### 2. Match with Topic
**Action:** Filter Topics by label (Events, Technology)

**Find:** "Anticipatory Experience Design" in `✅ Ready` bucket

### 3. Customize & Submit
**Action:**
- Update opportunity with specific abstract for event
- Link opportunity to topic (manually note in description)
- Move to `📝 Proposal Writing` → `📤 Submitted`

### 4. Track & Prepare
**If accepted:**
- Move to `✅ Accepted` → `🎯 Preparing`
- Create slides, demos, rehearsal plan

### 5. Deliver & Refine
**After talk:**
- Move opportunity to `🎤 Delivered`
- Move topic to `🔧 Refinement`
- Update based on audience feedback
- When polished, move back to `✅ Ready`

## Seeded Topics

### 1. Anticipatory Experience Design
**Status:** ✅ Ready
**Labels:** Events, Technology
**ID:** 220228

Philosophy and architecture for creating event experiences that anticipate needs.

**Key Points:**
- One card → infinite personalized experiences
- Database-driven routing
- Live demo: qrcard.conventioncityseattle.com

**Use For:** Event tech conferences, hospitality events, UX/experience design talks

---

### 2. Database-Driven Routing: Multi-Tenant Architecture
**Status:** ✅ Ready
**Labels:** Technology
**ID:** 220230

Novel architecture pattern where routes are resolved through database queries.

**Key Points:**
- Traditional @app.route vs database-driven
- Multi-tenant data isolation
- Framework-agnostic pattern

**Use For:** Software architecture conferences, technical deep-dives, platform engineering talks

---

### 3. Privacy-First AI: Local Personalization with MCP
**Status:** 📐 Prepare
**Labels:** Technology, Events
**ID:** 220231

AI-powered personalization without surveillance capitalism using MCP + SmolLM.

**Key Points:**
- GDPR-compliant AI
- Local processing, no external API calls
- Model Context Protocol architecture

**Use For:** European conferences, privacy-focused events, AI ethics discussions

## Quick Commands

### Add New Opportunity
```bash
# Quick shell function
vikunja-add-talk "Conference Name" "2026-08-15" "Location"

# Full featured
cd /home/ivanadmin/spawn-solutions/research/1.131-project-management/02-implementations/tools
uv run python add_talk.py --title "..." --event-date "..." --location "..."
```

### Add New Topic
```bash
cd /home/ivanadmin/spawn-solutions/research/1.131-project-management/02-implementations/tools

# Simple topic
uv run python create_task.py \
  --project-id 14154 \
  --title "Topic Name" \
  --bucket 1 \
  --description "<h3>Overview</h3><p>...</p>"

# With labels (requires manual addition via UI or API)
```

### View All Topics
```bash
# Via export script
cd /home/ivanadmin/spawn-solutions/research/1.131-project-management/02-implementations/vikunja-export-script
uv run python src/export_vikunja.py --project-id 14154
```

### View All Opportunities
```bash
# Via check_talks script (update to use project 13481)
cd /home/ivanadmin/spawn-solutions/research/1.131-project-management/02-implementations/vikunja-export-script
uv run python src/check_talks.py
```

## Design Rationale

### Why Separate Opportunities from Topics?

**Before:** Mixed event opportunities with content topics
- "PyCon 2026" task contained abstract for that specific event
- Hard to reuse content across events
- No clear view of intellectual property

**After:** Clear separation of concerns
- **Opportunities** = when/where to speak (temporal, event-specific)
- **Topics** = what to speak about (evergreen, reusable)

**Benefits:**
1. Reuse polished topics across multiple events
2. Track intellectual property development
3. See which topics are ready vs need refinement
4. Build speaker portfolio (all ready topics = your offerings)

### Why Labels Instead of Sub-Projects?

**Labels are more flexible:**
- Topics often span multiple domains (e.g., Events + Technology)
- Filter/search by multiple labels simultaneously
- Less hierarchy = less maintenance overhead
- Easier to add new categories (just create label)

**Sub-projects would be rigid:**
- "Database-Driven Routing" fits Technology AND Architecture
- Where does it go? Need to pick one or duplicate
- More navigation clicks to see overview

## URLs

- **Parent Project:** https://app.vikunja.cloud/projects/14153
- **Opportunities:** https://app.vikunja.cloud/projects/13481
- **Topics:** https://app.vikunja.cloud/projects/14154

## Future Enhancements

### Potential Additions
1. **Slides tracking** - Link to slide decks for each delivered talk
2. **Recording links** - YouTube/Vimeo URLs for recorded talks
3. **Audience feedback** - Ratings, comments from attendees
4. **Talk variants** - Short (20min), Medium (45min), Long (90min) versions
5. **Co-speaker tracking** - When collaborating with others

### Automation Opportunities
1. **Auto-link opportunities → topics** when keywords match
2. **Deadline reminders** for proposal submissions
3. **Preparation checklist** auto-created when moved to Preparing
4. **Post-delivery survey** sent to audience for feedback

---

**Created:** November 11, 2025
**Last Updated:** November 11, 2025
**Vikunja Instance:** https://app.vikunja.cloud
