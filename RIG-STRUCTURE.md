# Research Rig Structure

## Current Structure (Simple, Recommended for Learning)

```
research/
├── .repo.git/                      ← Canonical clone (bare repo) of SoS
├── crew/ivan/                      ← Worktree: SoS workspace (YOU ARE HERE)
│   ├── packages/research/          ← 1.xxx public research
│   ├── docs/survey/
│   ├── scripts/
│   └── RIG-STRUCTURE.md            ← This file
│
├── dev/                            ← Experiments & private research
│   ├── recipe-embeddings/          ← Separate repo (experiment)
│   ├── library-embeddings/         ← Separate repo (experiment)
│   └── private-research/           ← Future: 2.xxx, 3.xxx (not public)
│
├── polecats/                       ← Autonomous workers (worktrees)
│   ├── ace/
│   │   └── research/               ← Worktree → ../../.repo.git
│   └── ...
│
├── mayor/                          ← Mayor's coordination space
├── refinery/                       ← Merge queue processor
└── witness/                        ← Worker lifecycle manager
```

## How This Works

### crew/ivan (Current Workspace)
- **Purpose**: Main workspace for Survey of Software (SoS) development
- **Git**: Worktree pointing to `.repo.git` on `main` branch
- **Content**: 1.xxx public research, survey docs, automation scripts
- **Navigation**: `dev re` or `gas re`

### dev/ (Experiments & Private Work)
- **Purpose**: Side projects, experiments, private research
- **Git**: Each subdirectory is its own independent repo (or not versioned)
- **Content**:
  - recipe-embeddings, library-embeddings (experiments)
  - private-research (future: 2.xxx, 3.xxx unpublished research)
- **Navigation**: `cd ~/gt/research/dev/`

### polecats/ (Autonomous Workers)
- **Purpose**: Autonomous agents working on research tasks
- **Git**: Each polecat has worktrees pointing to `.repo.git` (different branches)
- **Content**: Same as crew/ivan but on feature branches
- **Coordination**: Assigned work via beads system

## Navigation Quick Reference

```bash
# Work on SoS (published research)
dev re                      # → crew/ivan (SoS workspace)
gas re                      # → crew/ivan + launch Claude

# Work on experiments
cd ~/gt/research/dev/recipe-embeddings
cd ~/gt/research/dev/library-embeddings

# Work on private research (future)
cd ~/gt/research/dev/private-research

# Check polecat status
cd ~/gt && gt polecat list research
```

## Research Type Routing

| Type | Code | Location | Published? |
|------|------|----------|------------|
| **Public research** | 1.xxx | `crew/ivan/packages/research/` | ✅ Yes (SoS) |
| **Private research** | 2.xxx, 3.xxx | `dev/private-research/` | ❌ No |
| **Experiments** | N/A | `dev/recipe-embeddings/`, etc. | ❌ No |

## Alternatives (Future Considerations)

### Alternative A: Multi-Project Workspace

**Structure:**
```
research/
├── .repo.git/                      ← SoS canonical clone
├── repos/                          ← Other canonical clones
│   ├── private-research/
│   └── experiments/
├── crew/ivan/                      ← Flexible workspace (NOT a worktree)
│   └── projects/
│       ├── sos/                    ← Worktree → ../../.repo.git
│       ├── private-research/       ← Worktree → ../../repos/private-research
│       └── experiments/            ← Worktrees to experiment repos
└── polecats/ace/
    └── projects/
        ├── sos/
        └── private-research/
```

**Pros:**
- crew/ivan is truly flexible - not locked to one repo
- Can work on multiple projects without leaving workspace
- Polecats mirror the same structure
- Clean separation of concerns

**Cons:**
- More complex directory structure
- Requires restructuring existing setup
- Navigation becomes more nested
- Need to update all scripts/tools

**When to use:**
- You frequently switch between multiple unrelated repos
- Projects have equal importance (not one "main" project)
- You want polecats to work on multiple projects simultaneously

### Alternative B: Single Repo, Multiple Branches

**Structure:**
```
research/
├── .repo.git/                      ← One repo for ALL research
│   ├── main branch                 ← 1.xxx (public)
│   ├── private branch              ← 2.xxx, 3.xxx (private)
│   └── experiment/* branches       ← Experiments
├── crew/ivan/                      ← Worktree (main branch)
└── polecats/ace/                   ← Worktree (feature branches)
```

**Pros:**
- Simplest structure
- All research in one repo
- Easy to share code/utils between projects
- Git handles everything

**Cons:**
- Private and public research mixed in one repo
- Risk of accidentally publishing private work
- Large repo with unrelated content
- Can't easily have separate remotes (e.g., different GitHub repos)

**When to use:**
- Research types are closely related
- You trust branch-based access control
- You want minimal directory complexity

### Alternative C: Monorepo with Workspaces

**Structure:**
```
research/
├── .repo.git/                      ← Monorepo
│   ├── projects/
│   │   ├── sos/                    ← Published research
│   │   ├── private-research/       ← Private research
│   │   └── experiments/            ← Experiments
│   └── shared/                     ← Shared utilities
├── crew/ivan/                      ← Worktree (entire monorepo)
└── polecats/ace/                   ← Worktree (entire monorepo)
```

**Pros:**
- All projects in one repo, clearly organized
- Shared tooling and utilities
- Single dependency management
- Can use monorepo tools (Nx, Turborepo, etc.)

**Cons:**
- Still risk of publishing private content
- Complex .gitignore for selective publishing
- Need monorepo tooling
- Large repo size

**When to use:**
- Projects share significant code/dependencies
- You want centralized tooling
- You're comfortable with monorepo patterns

## Decision Criteria

**Stick with Current (Recommended for now):**
- ✅ You're still learning Gas Town
- ✅ SoS is your primary focus
- ✅ Private research is occasional/experimental
- ✅ You want simplicity

**Consider Alternative A (Multi-Project Workspace):**
- You work on 3+ unrelated repos daily
- Private research becomes equally important as SoS
- You want polecats working on multiple projects
- You're comfortable with complexity

**Consider Alternative B (Single Repo):**
- Research types are closely related
- You never want them published separately
- You trust branch-based separation
- You want minimal structure

**Consider Alternative C (Monorepo):**
- Projects share significant code
- You want centralized tooling
- You're experienced with monorepo patterns
- You can manage publishing workflows

## Migration Path (If Needed Later)

If you decide to restructure to Alternative A:

```bash
# 1. Create new structure
cd ~/gt/research
mkdir -p crew/ivan/projects repos

# 2. Move SoS worktree
mv crew/ivan crew/ivan-old
mkdir -p crew/ivan/projects
cd crew/ivan/projects
git worktree add sos ../../.repo.git main

# 3. Set up private research
git clone <private-repo-url> ../../repos/private-research
git worktree add private-research ../../repos/private-research main

# 4. Update navigation scripts
# Edit ~/gt/scripts/gas-town-init.sh

# 5. Verify and clean up
rm -rf crew/ivan-old
```

## Notes

- This structure was documented on 2026-02-03 while learning Gas Town
- Current setup works well for SoS-focused development
- Re-evaluate if workflow changes significantly
- See `CLAUDE.md` for Gas Town best practices
- See `NAVIGATION-QUICKREF.md` for navigation shortcuts

## Questions?

If you're unsure which structure to use, ask yourself:

1. **How often do I switch between projects?**
   - Rarely → Current (simple)
   - Often → Alternative A (multi-project)

2. **Are projects related or independent?**
   - Related → Alternative B or C (shared repo)
   - Independent → Current or Alternative A (separate repos)

3. **Do I need polecats on multiple projects?**
   - No → Current (simple)
   - Yes → Alternative A (multi-project)

4. **Am I comfortable with complexity?**
   - No → Current (simple)
   - Yes → Any alternative

**Default recommendation: Keep it simple until you have a clear reason to change.**
