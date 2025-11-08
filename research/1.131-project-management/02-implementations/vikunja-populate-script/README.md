# Vikunja Population Script

**Generic script to populate Vikunja from YAML/JSON files**

Part of 1.131 Project Management research - "hardware store model" tool for automating Vikunja project/task creation.

---

## Features

✅ **Flexible input**: YAML or JSON format
✅ **Comprehensive validation**: Schema validation before API calls
✅ **Dry-run mode**: Validate without creating resources
✅ **Error handling**: Clear error messages for debugging
✅ **HTML formatting**: Support for formatted task descriptions
✅ **Label management**: Automatic label creation and attachment

---

## Quick Start

### 1. Prerequisites

- Vikunja Cloud account: https://app.vikunja.cloud/
- API token configured (see [vikunja-api-wrapper/QUICK_START.md](../vikunja-api-wrapper/QUICK_START.md))
- Python 3.8+
- `.env` file at repo root with `VIKUNJA_API_TOKEN`

### 2. Basic Usage

```bash
# Navigate to src directory
cd research/1.131-project-management/02-implementations/vikunja-populate-script/src

# Dry run (validate only, no API calls)
python populate_vikunja.py --dry-run ../examples/simple-example.yaml

# Create resources
python populate_vikunja.py ../examples/simple-example.yaml

# Verbose output
python populate_vikunja.py --verbose ../examples/sea-week1-3.yaml
```

---

## Input Format

See [src/SCHEMA.md](src/SCHEMA.md) for complete documentation.

**Minimal example:**

```yaml
project:
  title: "My Project"

tasks:
  - title: "My Task"
```

**Full example:**

```yaml
project:
  title: "Schema Evolution Automation"
  description: "12-week implementation plan"
  color: "4287f5"

labels:
  - title: "Week 1"
    description: "Foundation tasks"
    color: "ff6b6b"

tasks:
  - title: "Week 1: Project Foundation"
    description: |
      <strong>Goal:</strong> Set up environment<br><br>
      <strong>Tasks:</strong><br>
      - Init git repo<br>
      - Configure CI/CD
    due_date: "2025-11-14"
    priority: 0
    labels:
      - "Week 1"
```

---

## Examples

### Simple Project

```bash
python populate_vikunja.py ../examples/simple-example.yaml
```

Creates a project with 2 labels (Bug, Feature) and 3 tasks.

### SEA Implementation Plan

```bash
python populate_vikunja.py ../examples/sea-week1-3.yaml
```

Creates Schema Evolution Automation project with weekly milestones.

---

## Development

**Built with Method 4 (Adaptive TDD):**

- ✅ 43 validation tests + 21 bug injection tests
- ✅ 17 parsing tests
- ✅ 15 population tests
- ✅ 100% bug detection rate (21/21 bugs caught)

**Run tests:**

```bash
# All tests
python -m pytest -v

# Specific module
python -m pytest test_validation.py -v
python -m pytest test_parsing.py -v
python -m pytest test_population.py -v

# Test the tests (Adaptive TDD)
python test_the_tests.py
```

---

## Files

```
vikunja-populate-script/
├── README.md                      # This file
├── examples/
│   ├── simple-example.yaml        # Minimal example
│   └── sea-week1-3.yaml           # SEA implementation plan
└── src/
    ├── SCHEMA.md                  # Input format documentation
    ├── populate_vikunja.py        # CLI script (Method 1)
    ├── validation.py              # Schema validation
    ├── parsing.py                 # YAML/JSON parsing
    ├── population.py              # Vikunja API population logic
    ├── requirements.txt           # Dependencies
    ├── test_validation.py         # Validation tests
    ├── test_parsing.py            # Parsing tests
    ├── test_population.py         # Population tests
    └── test_the_tests.py          # Bug injection tests
```

---

## CLI Options

```
usage: populate_vikunja.py [-h] [--dry-run] [-v] input_file

positional arguments:
  input_file     Path to YAML or JSON input file

options:
  -h, --help     show this help message and exit
  --dry-run      Validate schema without creating resources (no API calls)
  -v, --verbose  Verbose output (show all API calls)
```

---

## Error Handling

**Schema validation errors:**
- Missing required fields → Clear error with field name
- Invalid data types → Type mismatch error
- Invalid formats (dates, colors) → Format validation error
- Label references → Reference error if label doesn't exist

**API errors:**
- 401 Unauthorized → Token invalid/expired
- 403 Forbidden → Insufficient permissions
- 422 Validation Error → Vikunja rejected data

**Use dry-run mode to catch errors before API calls:**

```bash
python populate_vikunja.py --dry-run my-tasks.yaml
```

---

## Methodology

**TDD Process:**

1. **Tests first**: Written before implementation
2. **Implementation**: Make tests pass
3. **Adaptive TDD**: Inject bugs to verify tests catch them

**Method selection:**

- `validation.py`, `parsing.py`, `population.py`: **Method 4** (Adaptive TDD)
- `populate_vikunja.py` (CLI): **Method 1** (Direct implementation)

**Rationale**: CLI is thin orchestration layer; real logic is tested in underlying modules.

---

## Integration

**Works with:**

- [vikunja-api-wrapper](../vikunja-api-wrapper/) - Python API client (Method 4)
- `.env` configuration at repo root
- Any Vikunja Cloud or self-hosted instance

**Use cases:**

- Automate sprint planning (SEA 12-week plan)
- Content calendars (cookbooks conversion schedule)
- Bug tracking (qrcards maintenance tasks)
- Project templates (reusable task structures)

---

## Related Documentation

- **Setup**: [../vikunja-api-wrapper/QUICK_START.md](../vikunja-api-wrapper/QUICK_START.md)
- **Testing**: [../vikunja-api-wrapper/src/TESTING.md](../vikunja-api-wrapper/src/TESTING.md)
- **Schema**: [src/SCHEMA.md](src/SCHEMA.md)
- **Research**: [../../01-discovery/](../../01-discovery/) (1.131 PM platforms)

---

**Hardware Store Model**: Generic tool, not user-specific. Adapt YAML files to your needs.
