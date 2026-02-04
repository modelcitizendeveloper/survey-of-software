# fs-train: Financial Analysis Fluency Trainer

Interactive CLI tool for learning financial statement analysis through hands-on practice.

## Quick Start

```bash
# One-time setup
uv venv
uv pip install blessed PyYAML requests

# List scenarios
./run-fs-train --list

# Run by number (easiest!)
./run-fs-train 001
./run-fs-train 002

# Or by partial name
./run-fs-train margin
./run-fs-train cash

# Or full filename
./run-fs-train 001_simple_growth.yaml

# With LLM scoring (requires Ollama)
./run-fs-train 002 --llm

# Optional: Enable bash tab completion
source fs-train-completion.bash
./run-fs-train <TAB>  # Shows all scenarios
```

## Features

- **6 Pre-Calculated Views**: Default, %, MoM, Margin, Detail, Cash
- **Keyword-Based Scoring**: Instant feedback on observations
- **LLM Scoring** (optional): Deep evaluation with Ollama (local models)
- **Progressive Difficulty**: Beginner → Intermediate → Advanced
- **Vim-Like Interface**: Keyboard-driven, fast navigation

## Usage

### Interactive Session

Once in a training session:

**View Commands:**
- `d` or `1` - Default view (absolute values)
- `%` or `2` - Percentage of revenue
- `m` or `3` - Month-over-month growth
- `g` or `4` - Margin analysis
- `e` or `5` - Detailed breakdown
- `c` or `6` - Cash flow

**Actions:**
- `o` or `Enter` - Add observation
- `?` - Show hint
- `f` or `Esc` - Finish session
- `q` - Quit (or cancel observation)

### LLM Scoring with Ollama

For enhanced evaluation with local LLMs:

```bash
# Ensure Ollama is running
ollama serve

# Run with LLM scoring
./fs-train 001_simple_growth.yaml --llm
```

Supported local models (via Ollama):
- llama3 (default)
- mistral
- phi
- Any model available in your Ollama installation

## Scenario Structure

Scenarios are YAML files in `scenarios/`:

```yaml
scenario_id: 001_simple_growth
name: "TechStart - Simple Growth"
difficulty: beginner

financial_data:
  revenue: { jan: 50000, feb: 55000, mar: 60000 }
  cogs: { jan: 15000, feb: 16500, mar: 18000 }
  opex:
    salaries: { jan: 30000, feb: 30000, mar: 30000 }
    # ...

key_insights:
  - id: steady_growth
    description: "Revenue growing steadily at 10% MoM"
    points: 20
    keywords: ["revenue", "grow", "10%"]
```

## Architecture

```
fs-train (main CLI)
├── scenario_loader.py   - Load YAML scenarios
├── view_engine.py       - Pre-calculate financial views
└── scorer.py            - Keyword + LLM scoring
```

## Educational Progression

1. **Week 1**: Fundamentals (growth, margins, profitability)
2. **Week 2**: Complexity (investments, trade-offs, seasonality)
3. **Week 3**: Nuance (multi-issue analysis, strategic thinking)
4. **Week 4**: Real-world application

## Pattern

Based on `latin-train` methodology:
- **Pre-parsing**: Calculate all views upfront
- **Rapid feedback**: Instant scoring
- **Pattern recognition**: Learn through repetition
- **Fluency over perfection**: Build intuition

## Design Philosophy

- **NOT** a spreadsheet replacement
- **NOT** automated analysis
- **IS** interactive exploration with intelligent feedback
- **IS** fluency training through guided practice

## Implementation Status

✅ Phase 1: Core Engine
- [x] View Engine (6 standard views)
- [x] Keyword-based scoring
- [x] Terminal UI with blessed
- [x] 5 training scenarios

⏳ Phase 2: LLM Integration
- [x] Ollama support for local models
- [ ] OpenAI/Claude support
- [ ] Advanced feedback generation
- [ ] 10+ scenarios

🔮 Phase 3: Polish
- [ ] Progress tracking
- [ ] Statistics over time
- [ ] Custom scenario creation

## Related Tools

- **fs-parse**: Parse financial statements → canonical format
- **fs-scenario**: Apply scenarios to financial models
- **fs-train**: Learn financial analysis (this tool)

---

**Status**: Core implementation complete, tested with Scenario 001
**Next**: Run full test suite, expand scenario library
