# Deployment Workflow

## Canonical Flow (Site 1: Public 1.xxx Research)

```
Source Research (4PS structure)
  packages/research/1.xxx-topic/
    ├── 01-discovery/
    │   ├── S1-rapid/
    │   ├── S2-comprehensive/
    │   ├── S3-need-driven/
    │   └── S4-strategic/
    ├── DOMAIN_EXPLAINER.md
    └── metadata.yaml
          ↓
    convert_research.py
          ↓
Converted Docusaurus MDX
  docs/survey/1-xxx.md
          ↓
    npm run build
          ↓
Build Artifact
  build/
          ↓
  GitHub Actions (.github/workflows/deploy.yml)
          ↓
Production Site
  https://research.modelcitizendeveloper.com/
```

## Local Development

### Staging Site (localhost)
```bash
npm start                    # http://localhost:3000
# OR
sos launch 1                 # Same thing
```

### Convert Research
```bash
python3 convert_research.py  # Converts packages/research/ → docs/survey/
```

### Build for Production
```bash
npm run build                # Creates build/ directory
```

## Git Workflow

**Branches:**
- `main` - Production (auto-deploys to research.modelcitizendeveloper.com)
- `draft` - Staging (for testing before promotion)

**What's Tracked:**
- ✅ `packages/research/` - Source research (4PS structure)
- ✅ `docs/survey/` - Converted MDX
- ✅ `docs/*.md` - Site pages (about, vision, etc.)
- ✅ `sidebars.ts`, `docusaurus.config.ts` - Site config
- ❌ `build/` - Deployment artifact (gitignored)
- ❌ `node_modules/` - Dependencies (gitignored)

**Creating New Research:**
1. Create research in `packages/research/<code>-<topic>/` following 4PS template
2. Run `python3 convert_research.py` to generate `docs/survey/<code>.md`
3. Update `docs/survey/index.md` (add to catalog)
4. Update `sidebars.ts` (add to navigation)
5. Commit source (`packages/research/`) and output (`docs/survey/`)
6. Push to main → auto-deploys

## Other Staging Sites (Private, Not Deployed)

Access via `sos launch <n>`:

| Site | Content | Port | Command |
|------|---------|------|---------|
| 1/public | 1.xxx | 3000 | `sos launch 1` |
| 2/standards | 2.xxx | 3001 | `sos launch 2` |
| 3/core | 3.00-3.03 | 3002 | `sos launch 3` |
| 4/data | 3.04-3.07 | 3003 | `sos launch 4` |
| 5/platforms | 3.10+ | 3004 | `sos launch 5` |

Only Site 1 (public 1.xxx) deploys to production.

## Deployment Trigger

GitHub Actions workflow (`.github/workflows/deploy.yml`) triggers on:
- Push to `main` branch
- Manual workflow dispatch

The workflow:
1. Checks out main
2. Installs dependencies (`npm ci`)
3. Builds site (`npm run build`)
4. Uploads `build/` to GitHub Pages
5. Deploys to https://research.modelcitizendeveloper.com/

## Troubleshooting

### Conversion issues
```bash
cd ~/gt/research/crew/ivan
python3 convert_research.py 2>&1 | less
```

### Build errors
```bash
npm run build 2>&1 | less
```

### Check what's deployed
- Local: http://localhost:3000
- Production: https://research.modelcitizendeveloper.com/
- GitHub repo: https://github.com/modelcitizendeveloper/survey-of-software
