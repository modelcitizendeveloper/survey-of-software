# fs-train Phase 1: Core Engine - COMPLETE ✓

**Completed:** 2025-11-18
**Status:** All Phase 1 features implemented and tested

## Implemented Features

### 1. Interactive Terminal UI (blessed)
- Fullscreen terminal interface with centered layout
- Real-time score display with LLM status indicator
- Safe terminal formatting (handles missing capabilities)
- 7 financial views with instant switching
- Observation entry mode with live feedback
- Results screen with back-to-session capability

### 2. Scenario Loading System
- YAML-based scenario definitions
- Smart scenario finder (by number, name, or partial match)
- Bash tab completion for quick access
- `./run-fs-train 002` or `./run-fs-train margin` or `./run-fs-train <TAB>`

### 3. Seven Financial Views

#### View 1: Default (Absolute Values)
- Revenue, COGS, Gross Margin
- OpEx categories (salaries, marketing, R&D, etc.)
- Operating Income, Net Income
- Key: `d` or `1`

#### View 2: Percentage of Revenue
- All metrics as % of revenue
- Spot margin compression or expense bloat
- Key: `%` or `2`

#### View 3: Month-over-Month Growth
- Growth rates for all metrics
- Chronologically ordered (jan→feb, feb→mar)
- Key: `m` or `3`

#### View 4: Margin Analysis
- Gross Margin, Operating Margin, Net Margin
- Track profitability trends
- Key: `g` or `4`

#### View 5: Detailed Breakdown
- Full OpEx breakdown by category
- Shows cost structure evolution
- Key: `e` or `5`

#### View 6: Cash Flow
- Starting cash, operating cash flow, ending cash
- Track runway and burn rate
- Key: `c` or `6`

#### View 7: Balance Sheet ⭐ NEW
- Cash, Accounts Receivable, Accounts Payable
- DSO (Days Sales Outstanding)
- AR/Revenue ratio (working capital health)
- Key: `b` or `7`

### 4. Scoring System (Hybrid Approach)

#### Primary: Keyword Matching
- Fast, deterministic scoring
- Teaches financial jargon
- Shows which keywords matched
- Example: "revenue flat" matches keywords ["revenue", "flat"]

#### Secondary: Near-Miss Detection
- Synonym matching for common terms
- Guides toward proper terminology
- Example: "operating expenses" suggests "Try using: opex"

#### Tertiary: LLM Validation (Optional)
- Ollama integration (local, no API costs)
- Validates ALL observations (matched or not)
- Teaches jargon: "Good catch! In finance we call this 'OpEx growth'"
- Scores 0-10 based on insight depth
- Visible status indicator: 🤖 LLM: Active/Error

**User Philosophy Applied:**
> "Getting it right intuitively is fine, but we should guide towards financial terminology as widely understood (i.e. jargon)"

### 5. Session Logging
- All observations saved to `training_sessions.jsonl`
- Includes matched/missed insights
- Timestamps and scenario IDs
- Git-friendly format (one JSON object per line)

### 6. User Experience Features

#### Results Screen
- Shows score, depth level, time spent
- Lists caught insights (with keywords that matched)
- Lists missed insights (with keywords to try)
- Explains non-matches (if only 1-3)
- **[b] Back to session** - continue exploring
- **[Any key] Exit** - finish session

#### Smart Scenario Access
```bash
./run-fs-train 001              # By number
./run-fs-train margin           # By keyword
./run-fs-train 003_growth       # Full name
./run-fs-train <TAB>            # Show all scenarios
```

#### Keyboard Shortcuts
- `d/1` - Default view
- `%/2` - Percent of revenue
- `m/3` - Month-over-month
- `g/4` - Margin analysis
- `e/5` - Detailed breakdown
- `c/6` - Cash flow
- `b/7` - Balance sheet
- `o/Enter` - Make observation
- `?` - Show hint
- `f` - Finish and see results
- `q` - Quit (or cancel observation)

## Scenarios Included

1. **001_simple_growth.yaml** (Beginner)
   - Basic revenue growth
   - Healthy margins
   - Learn to spot trends

2. **002_margin_compression.yaml** (Intermediate)
   - Flat revenue
   - Rising COGS (nested structure: server_costs, support)
   - Declining gross margin
   - Moving from profitable to break-even

3. **003_growth_hiring.yaml** (Intermediate)
   - Consistent revenue growth (9-10% MoM)
   - New hire in March (+$5K salary)
   - Marketing acceleration (50% vs 10% revenue growth)
   - Profitability trade-offs

4. **004_cash_crunch.yaml** (Advanced)
   - Growing revenue and profitable
   - AR building up ($300K-$340K)
   - Cash declining despite profitability
   - Classic "profitable but broke" scenario
   - **Requires Balance Sheet view to diagnose**

## Technical Stack

- **Python 3** - Core language
- **blessed** - Terminal UI (fullscreen, colors, input)
- **PyYAML** - Scenario file parsing
- **requests** - Ollama API calls
- **Ollama** - Local LLM (llama3 default)
- **uv** - Fast package management

## Installation & Usage

```bash
# 1. Create virtual environment and install dependencies
uv venv
uv pip install -r requirements.txt

# 2. Enable tab completion (optional)
source fs-train-completion.bash

# 3. Run a scenario
./run-fs-train 002              # By number
./run-fs-train margin           # By keyword
./run-fs-train --llm 004        # With LLM scoring

# 4. Start Ollama for LLM scoring (optional)
ollama serve                    # In separate terminal
```

## Key Implementation Details

### Nested COGS Support
Handles both flat and nested COGS structures:
```yaml
# Flat (001, 003)
cogs:
  jan: 30000
  feb: 32000

# Nested (002)
cogs:
  server_costs:
    jan: 35000
    feb: 40000
  support:
    jan: 5000
    feb: 6000
```

### Month Ordering
All views show months chronologically (not alphabetically):
```python
month_order = ['jan', 'feb', 'mar', 'apr', 'may', 'jun',
              'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
```

### Safe Terminal Formatting
Handles terminals with missing capabilities:
```python
def _fmt(self, text, *attrs):
    """Safely apply terminal formatting, falling back to plain text."""
    result = text
    for attr in attrs:
        formatter = getattr(self.term, attr, None)
        if formatter and callable(formatter):
            try:
                result = formatter(result)
            except (TypeError, AttributeError):
                pass  # Terminal doesn't support this capability
    return result
```

## Bugs Fixed During Development

1. ✓ Terminal capabilities missing (dim, reverse) on WSL
2. ✓ "Total OpEx" repeated between characters (`replace("", ...)` bug)
3. ✓ Column spacing missing (values running together)
4. ✓ MoM columns in alphabetical order (should be chronological)
5. ✓ COGS showing $0 in nested scenarios
6. ✓ "Press any key" only accepting Enter (cbreak context)
7. ✓ Keyword matching too narrow (missed valid observations)
8. ✓ LLM errors silent (no visibility into failures)
9. ✓ Can't return to session after viewing results
10. ✓ No Balance Sheet view (couldn't see AR in scenario 004)

## Testing Evidence

From `training_sessions.jsonl`:
- Scenario 002: 84% score (Advanced depth)
- Scenario 003: 77% score (Intermediate depth) - 9 observations
- Scenario 004: 64% score (Intermediate depth) - 8 observations

## Phase 2: Enhancements (Future)

Potential future additions:
- [ ] More scenarios (hardware, marketplace, subscription)
- [ ] Multi-provider LLM support (OpenAI, Claude)
- [ ] Progress tracking across sessions
- [ ] Difficulty progression system
- [ ] Export session analysis
- [ ] Scenario editor/validator

## Success Metrics

✅ **User can complete scenario in < 5 minutes**
✅ **Keyword matching provides instant feedback**
✅ **LLM provides jargon coaching**
✅ **Near-miss detection guides learning**
✅ **Can return to session after viewing results**
✅ **All financial views display correctly**
✅ **Balance Sheet shows working capital metrics**
✅ **Session logs capture learning journey**

---

**Phase 1 Status: COMPLETE** 🎉

All core engine features implemented, tested, and documented.
Ready for real-world usage and Phase 2 enhancements.
