# Applications & Development Beads Design

## Confirmed Approach

Based on discussion:
- **Track all applications** (not just active)
- **Include individual tasks** within applications
- **Leave out analyses** until they generate actionable tasks
- **Track 02-implementations** - focused development in a single research area
- **Consider parallel folder structure** to separate dev from research data
- **ID scheme**: Structured for top-level apps, random for work items

## Proposed Structure

### ID Naming Convention

| Level | Format | Example |
|-------|--------|---------|
| Research | `solutions-xxx` (random) | `solutions-sjb` |
| Application (top-level) | `app-{name}` (structured) | `app-elevator`, `app-qrcards` |
| App work item | `app-{name}-xxx` (random suffix) | `app-elevator-a1b`, `app-qrcards-c2d` |
| Implementation | `impl-{research-id}` (structured) | `impl-1131` (for 1.131) |
| Impl work item | `impl-{research-id}-xxx` (random) | `impl-1131-xyz` |

### Folder Structure Option: Parallel Development Directory

Current:
```
spawn-solutions/
├── research/
│   ├── 1.131-project-management/
│   │   ├── 01-discovery/     # Research
│   │   └── 02-implementations/  # Development (mixed with research)
│   └── ...
└── applications/             # Mixed: analyses + working code
```

Proposed:
```
spawn-solutions/
├── research/                 # Pure research (01-discovery only)
│   ├── 1.131-project-management/
│   │   └── 01-discovery/
│   └── ...
├── development/              # All development work
│   ├── implementations/      # Research validation (was 02-implementations)
│   │   ├── 1131-vikunja-tools/
│   │   ├── 1140-latin-trainer/
│   │   └── 1104-ast-parser/
│   └── applications/         # Multi-topic or standalone apps
│       ├── elevator-project/
│       ├── language-learning/
│       └── qrcards/
└── applications/             # Strategic analyses only (or deprecate?)
```

**Alternative**: Keep current structure but clearly separate in beads:
- Research beads: `solutions-*`
- Development beads: `app-*`, `impl-*`

## Application Inventory

### Active Applications (in `applications/`)

| ID | Name | Type | Status | Description |
|----|------|------|--------|-------------|
| `app-elevator` | Elevator Scheduling | simulation | active | Monte Carlo elevator optimization |
| `app-language` | Language Learning | webapp | planning | Latin/Greek trainer platform |
| `app-qrcards` | QRCards | webapp | active | QR code card system |
| `app-schema` | Schema Evolution | library | active | Automated model migration |
| `app-inverse` | Inverse Fractional | analysis | planning | Investment strategy |
| `app-cookbooks` | Cookbooks | content | maintained | Recipe collection system |
| `app-lineage` | Research Lineage | system | planning | Data lineage tracking |
| `app-portal` | Intelligence Portal | webapp | planning | spawn-analysis frontend |

### Implementations (in `research/*/02-implementations/`)

| ID | Research | Name | Status |
|----|----------|------|--------|
| `impl-1131` | 1.131 Project Mgmt | Vikunja Tools | active |
| `impl-1140` | 1.140 Classical Lang | Latin Trainer | active |
| `impl-1104` | 1.104.1 AST Parsing | LibCST Examples | complete |
| `impl-1003` | 1.003 Full-Text Search | Search POC | complete |
| `impl-1049` | 1.049.1 Schema Inspect | Inspector Tool | complete |
| `impl-1100` | 1.100 Text Processing | Text Utils | complete |

## Label Taxonomy

### Status Labels
```yaml
dev-active:      "Currently being developed"
dev-maintained:  "Stable, occasional updates"
dev-complete:    "Implementation finished"
dev-planning:    "In design phase"
dev-archived:    "No longer maintained"
```

### Type Labels
```yaml
type-webapp:     "Web application"
type-cli:        "Command-line tool"
type-library:    "Reusable library/package"
type-simulation: "Simulation/modeling"
type-content:    "Content/documentation project"
type-system:     "Internal system/infrastructure"
```

### Research Link Labels
```yaml
validates-research:  "Validates research findings"
applies-research:    "Applies research to real problem"
extends-research:    "Extends beyond original research"
```

## Implementation Plan

### Phase 1: Create Labels
```bash
bd label create dev-active "Currently being developed"
bd label create dev-planning "In design phase"
bd label create dev-complete "Implementation finished"
bd label create type-webapp "Web application"
bd label create type-simulation "Simulation/modeling"
bd label create type-library "Reusable library"
bd label create impl "Implementation of research"
bd label create app "Standalone application"
```

### Phase 2: Create Application Issues
```bash
# Top-level applications (structured IDs)
bd create --id=app-elevator --title="Elevator Scheduling Simulation" \
  --labels="app,dev-active,type-simulation"
bd create --id=app-language --title="Language Learning Platform" \
  --labels="app,dev-planning,type-webapp"
bd create --id=app-qrcards --title="QRCards Modernization" \
  --labels="app,dev-active,type-webapp"
```

### Phase 3: Create Implementation Issues
```bash
# Implementations (structured IDs linking to research)
bd create --id=impl-1131 --title="Vikunja Integration Tools" \
  --labels="impl,dev-active,type-library,validates-research"
bd create --id=impl-1140 --title="Latin/Greek Trainer" \
  --labels="impl,dev-active,type-webapp,validates-research"
```

### Phase 4: Add Work Items (as needed)
```bash
# Random suffix for individual tasks
bd create --title="Implement voluntary floor strategy" \
  --labels="app" --parent=app-elevator
# Results in: app-elevator-a1b (or similar)
```

## Questions Remaining

1. **Folder restructure**: Move `02-implementations` to `development/implementations/`?
   - Pro: Clean separation of research data from code
   - Con: Breaks existing paths, migration effort

2. **applications/ folder**: Keep for analyses, or move working code out?
   - Option A: `applications/` = analyses only, code moves to `development/`
   - Option B: Keep mixed, just track differently in beads

3. **Parent-child in beads**: Does `bd` support parent relationships for app → work items?

## Recommended Next Steps

1. **Decision**: Confirm folder structure (restructure vs keep current)
2. **Labels**: Create the label taxonomy
3. **Pilot**: Create beads for 2-3 applications + implementations
4. **Work items**: Add tasks as actual development work arises
5. **Evaluate**: Assess structure after 2 weeks of use

---

**Created**: 2025-12-11
**Status**: Ready for implementation decision
