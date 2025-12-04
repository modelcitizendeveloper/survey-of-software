# Use Case: CI/CD Pipeline Optimization

## Scenario Overview

Optimizing code formatting checks in continuous integration pipelines to minimize CI time, reduce resource usage, and provide fast feedback without sacrificing code quality.

## Primary Requirements

### Performance
- Sub-30 second formatting checks
- Efficient file parsing and processing
- Minimal memory footprint
- Parallel execution support

### Caching
- Effective cache invalidation
- Cross-run cache reuse
- Minimal cache storage requirements
- Fast cache restoration

### Resource Efficiency
- Low CPU usage
- Minimal network dependencies
- Small tool installation size
- Optimized for CI runners

### Developer Experience
- Fast feedback on PRs
- Clear error messages
- Actionable failure reports
- Automatic fix suggestions

## Recommended Toolchain

### Python: Ruff Format
Rust-based formatter with exceptional speed

**Performance Profile:**
- 10-100x faster than Black
- ~5MB binary size
- Near-zero dependencies
- Excellent caching

### JavaScript/TypeScript: Biome
Modern formatter built for performance

**Performance Profile:**
- 10-35x faster than Prettier
- Single binary distribution
- Built-in caching
- Integrated linting + formatting

### Alternative JavaScript: Prettier (with caching)
Mature ecosystem with good optimization options

**Performance Profile:**
- Well-optimized for typical codebases
- Excellent cache support
- Widespread CI integration examples

## Configuration Approach

### Ruff CI Configuration

`pyproject.toml`:
```toml
[tool.ruff]
line-length = 100
target-version = "py311"
cache-dir = ".ruff_cache"  # Explicit cache location for CI

[tool.ruff.format]
# Minimal config for fastest execution
quote-style = "double"

# Exclude paths that don't need checking
extend-exclude = [
    "tests/fixtures/",
    "benchmarks/generated/",
    "docs/examples/",
]
```

### Biome CI Configuration

`biome.json`:
```json
{
  "$schema": "https://biomejs.dev/schemas/1.9.4/schema.json",
  "vcs": {
    "enabled": true,
    "clientKind": "git",
    "useIgnoreFile": true
  },
  "formatter": {
    "enabled": true,
    "indentStyle": "space",
    "lineWidth": 100
  },
  "linter": {
    "enabled": true,
    "rules": {
      "recommended": true
    }
  }
}
```

### Prettier with Caching

`.prettierrc`:
```json
{
  "printWidth": 100,
  "cache": true,
  "cacheStrategy": "metadata"
}
```

## CI/CD Integration Patterns

### GitHub Actions: Optimized Ruff

```yaml
name: Format Check
on: [pull_request]

jobs:
  format-python:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Ruff cache
        uses: actions/cache@v4
        with:
          path: .ruff_cache
          key: ruff-${{ runner.os }}-${{ hashFiles('pyproject.toml') }}

      - name: Install Ruff
        run: pip install ruff

      - name: Check formatting
        run: ruff format --check .
```

### GitHub Actions: Optimized Biome

```yaml
name: Format Check
on: [pull_request]

jobs:
  format-js:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0  # For git-based change detection

      - name: Install Biome
        run: npm install -g @biomejs/biome

      - name: Check formatting
        run: biome ci .
```

### GitHub Actions: Changed Files Only

```yaml
name: Format Check (Changed Files)
on: [pull_request]

jobs:
  format:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Get changed files
        id: changed-files
        uses: tj-actions/changed-files@v44
        with:
          files: |
            **/*.py
            **/*.js
            **/*.ts

      - name: Check formatting (Python)
        if: steps.changed-files.outputs.any_changed == 'true'
        run: |
          pip install ruff
          echo "${{ steps.changed-files.outputs.all_changed_files }}" | \
            xargs ruff format --check

      - name: Check formatting (JavaScript)
        if: steps.changed-files.outputs.any_changed == 'true'
        run: |
          npm install -g @biomejs/biome
          echo "${{ steps.changed-files.outputs.all_changed_files }}" | \
            xargs biome format --check
```

### GitLab CI: Optimized Pipeline

```yaml
format-check:
  stage: lint
  image: python:3.11-slim
  cache:
    key: ruff-cache
    paths:
      - .ruff_cache
  before_script:
    - pip install ruff
  script:
    - ruff format --check .
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
      changes:
        - "**/*.py"
```

### CircleCI: Parallel Execution

```yaml
version: 2.1

jobs:
  format-check:
    docker:
      - image: cimg/python:3.11
    steps:
      - checkout
      - restore_cache:
          keys:
            - ruff-v1-{{ checksum "pyproject.toml" }}
      - run:
          name: Install Ruff
          command: pip install ruff
      - run:
          name: Check formatting
          command: ruff format --check .
      - save_cache:
          key: ruff-v1-{{ checksum "pyproject.toml" }}
          paths:
            - .ruff_cache

workflows:
  check:
    jobs:
      - format-check
```

## Performance Optimization Strategies

### Strategy 1: Tool Selection
Choose fastest tool for your ecosystem:
- Python: Ruff (10-100x faster than Black)
- JavaScript: Biome (10-35x faster than Prettier)
- Multi-language: Separate optimized tools per language

### Strategy 2: Intelligent Caching

**File Content Caching:**
```yaml
- uses: actions/cache@v4
  with:
    path: |
      .ruff_cache
      node_modules/.cache/prettier
    key: format-${{ runner.os }}-${{ hashFiles('**/*.py', '**/*.js') }}
```

**Tool Installation Caching:**
```yaml
- uses: actions/cache@v4
  with:
    path: ~/.local/bin/ruff
    key: ruff-${{ runner.os }}-0.7.4
```

### Strategy 3: Changed Files Only

**Using Git Diff:**
```bash
git diff --name-only origin/main...HEAD -- '*.py' | xargs ruff format --check
```

**Advantages:**
- 90%+ reduction in files checked
- Sub-5 second checks for typical PRs
- Scales with change size, not codebase size

**Considerations:**
- Must have full git history (`fetch-depth: 0`)
- Base branch must be available
- Handle empty file list edge case

### Strategy 4: Parallel Execution

**Language-Based Parallelism:**
```yaml
jobs:
  format-python:
    runs-on: ubuntu-latest
    steps:
      - run: ruff format --check backend/

  format-javascript:
    runs-on: ubuntu-latest
    steps:
      - run: biome format --check frontend/
```

**Directory-Based Parallelism:**
```yaml
strategy:
  matrix:
    path: [backend/api, backend/workers, backend/shared]
steps:
  - run: ruff format --check ${{ matrix.path }}
```

### Strategy 5: Fail-Fast Configuration

```yaml
jobs:
  format-check:
    steps:
      - name: Quick format check
        run: ruff format --check .
        timeout-minutes: 2  # Fail if takes too long

  test:
    needs: format-check  # Don't run tests if formatting fails
    steps:
      - run: pytest
```

## Common Pitfalls

### Pitfall 1: No Caching
**Problem:** Installing tools and parsing files on every run wastes 30-60 seconds

**Solution:** Implement comprehensive caching strategy:
```yaml
- uses: actions/cache@v4
  with:
    path: |
      ~/.cache/pip
      .ruff_cache
    key: ${{ runner.os }}-${{ hashFiles('**/pyproject.toml') }}
```

### Pitfall 2: Checking Generated Files
**Problem:** Formatting checks on `dist/`, `build/`, or generated code waste time

**Solution:** Explicit exclusions in tool config:
```toml
[tool.ruff]
extend-exclude = ["dist", "build", "*.generated.py"]
```

### Pitfall 3: Running All Checks on Every Commit
**Problem:** Full codebase checks when only 3 files changed

**Solution:** Use changed files detection:
```yaml
- uses: tj-actions/changed-files@v44
  id: changed
- run: ruff format --check ${{ steps.changed.outputs.all_changed_files }}
```

### Pitfall 4: Slow Tool Installation
**Problem:** `npm install` for Prettier takes 20+ seconds

**Solution:** Use pre-installed binaries or direct downloads:
```yaml
- run: |
    curl -LO https://github.com/astral-sh/ruff/releases/download/v0.7.4/ruff-x86_64-unknown-linux-gnu.tar.gz
    tar xzf ruff-x86_64-unknown-linux-gnu.tar.gz
    ./ruff format --check .
```

### Pitfall 5: Inadequate Error Reporting
**Problem:** "Formatting failed" without showing which files or why

**Solution:** Enhanced output and annotations:
```yaml
- name: Check formatting
  run: |
    ruff format --check . --diff | tee format-diff.txt
    if [ ${PIPESTATUS[0]} -ne 0 ]; then
      echo "::error::Formatting check failed. See diff above."
      exit 1
    fi
```

## Performance Benchmarks

### Tool Performance Comparison (1000 Python files)

| Tool | Cold Run | Cached Run | Binary Size |
|------|----------|------------|-------------|
| Ruff | 0.8s | 0.2s | 5MB |
| Black | 22s | 18s | 1MB + deps |
| YAPF | 45s | 40s | 2MB + deps |

### CI Pipeline Time Comparison

| Approach | Time | Cache Hit Rate |
|----------|------|----------------|
| Ruff (all files) | 3s | 95% |
| Black (all files) | 35s | 80% |
| Ruff (changed only) | 0.5s | 98% |
| Black (changed only) | 8s | 85% |

### Cost Optimization

**GitHub Actions (billed minutes):**
- Old pipeline (Black, no cache): ~1 min/run × 100 runs/day = 100 min/day
- Optimized (Ruff, cached, changed files): ~5s/run × 100 runs/day = 8.3 min/day
- **Savings: 91% reduction in CI time**

## Success Metrics

- Formatting check completes in < 10 seconds for typical PRs
- 95%+ cache hit rate
- < 1% of CI runs timeout on formatting
- Zero false positives from formatting checks
- Developer feedback time < 2 minutes total

## Advanced Optimizations

### Pre-commit.ci Integration
Offload formatting checks to specialized service:

`.pre-commit-config.yaml`:
```yaml
ci:
  autofix_prs: true
  autoupdate_schedule: monthly

repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.7.4
    hooks:
      - id: ruff-format
```

Benefits:
- Zero CI configuration needed
- Automatic PR fixes
- Free for open source

### Docker Layer Caching

```dockerfile
FROM python:3.11-slim

# Cache this layer (changes infrequently)
RUN pip install ruff==0.7.4

# Copy code (changes frequently)
COPY . /app
WORKDIR /app

CMD ["ruff", "format", "--check", "."]
```

### Monorepo Path Filtering

```yaml
- uses: dorny/paths-filter@v2
  id: filter
  with:
    filters: |
      backend:
        - 'backend/**'
      frontend:
        - 'frontend/**'

- if: steps.filter.outputs.backend == 'true'
  run: ruff format --check backend/

- if: steps.filter.outputs.frontend == 'true'
  run: biome check frontend/
```

## Date Compiled
December 4, 2025
