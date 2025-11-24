# S1: Rapid Discovery - Approach

**Methodology**: Rapid Library Search (speed-focused)
**Time Box**: 60-90 minutes maximum
**Goal**: Identify viable Anki integration libraries and custom system patterns

## Core Philosophy

Quickly map the solution space:
- What Anki integration libraries exist?
- How mature/popular are they?
- Is building custom flashcard system feasible?
- What's the 80/20 answer?

## Discovery Process

### 1. Anki Integration Landscape (25 min)
- **genanki**: Programmatic deck generation
- **ankipandas**: Database analysis
- **AnkiConnect**: Live API integration
- **Anki pylib**: Direct database access
- Check: PyPI downloads, GitHub stars, maintenance status

### 2. Custom Flashcard System Patterns (20 min)
- FSRS + SQLite (simplest DIY)
- Web frameworks (React + FSRS)
- Existing open-source flashcard apps
- Implementation complexity estimate

### 3. Anki Ecosystem Assessment (15 min)
- Anki user base size (adoption risk)
- .apkg format stability (future-proofing)
- Mobile sync options (AnkiWeb vs self-hosted)
- Community momentum (growing vs declining)

### 4. Quick Comparison (15 min)
- Anki export: Pros/cons, implementation hours
- Custom system: Pros/cons, implementation hours
- Hybrid approach: Feasibility assessment

### 5. Initial Recommendation (10 min)
- Default path for language learning app
- When to consider alternatives
- Signal for S3 scenario analysis

## Evaluation Criteria

**Primary**:
- Implementation effort (hours to working flashcard delivery)
- User adoption friction (installation, learning curve)

**Secondary**:
- Data portability (can users export/migrate?)
- Long-term maintenance burden

**Tertiary**:
- UX control vs ecosystem benefits trade-off

## Output Files

- `approach.md` (this file)
- `genanki.md` - Programmatic deck generation
- `ankiconnect.md` - Live Anki integration
- `ankipandas.md` - Database analysis
- `custom-system.md` - Build-your-own patterns
- `recommendation.md` - Initial path forward

## Success Criteria

- Understand Anki integration options (3-4 viable libraries)
- Estimate custom system complexity (rough hours)
- Identify which path minimizes friction for users
- Provide input for S3 scenario analysis
- Total time: <90 minutes

## Note for S3

S3 will do heavy lifting on **scenario comparison**:
- Scenario 1: Anki export (existing Anki users)
- Scenario 2: Custom interface (dedicated app users)

S1 just maps what's possible - S3 determines which scenario wins.
