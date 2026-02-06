# Command-Line and Data Processing Scenarios

## Scenario 1: Build Tool File Matching (glob patterns)

### Problem
Match files for compilation, testing, linting based on patterns like `src/**/*.rs` or `*.{js,ts}`

### Constraints
- Cross-platform (Windows, Linux, macOS)
- Respect .gitignore
- Fast for large codebases
- Support complex glob patterns

### Solution
**Language-appropriate glob library**

Rust (globset):
```rust
use globset::{Glob, GlobSetBuilder};

let mut builder = GlobSetBuilder::new();
builder.add(Glob::new("src/**/*.rs")?);
builder.add(Glob::new("tests/**/*.rs")?);
let set = builder.build()?;

for entry in walkdir::WalkDir::new(".") {
    let entry = entry?;
    if set.is_match(entry.path()) {
        // Process file
    }
}
```

Python (pathlib + fnmatch):
```python
from pathlib import Path
import fnmatch

def glob_recursive(pattern, root="."):
    root_path = Path(root)
    for path in root_path.rglob('*'):
        if fnmatch.fnmatch(str(path), pattern):
            yield path
```

**Rationale**:
- Compiled glob patterns (globset) faster than repeated matches
- Respects .gitignore with ignore crate
- Cross-platform path handling

**Alternatives**:
- **Shell expansion**: For simple CLI usage
- **regex**: For complex patterns beyond glob syntax
- **walk + filter**: For simple directory traversal

### Pitfalls
- ❌ Not handling dotfiles/hidden files consistently
- ❌ Following symlinks (potential infinite loops)
- ❌ Case sensitivity differences (Windows vs Unix)

## Scenario 2: CSV Parsing with Special Cases

### Problem
Parse CSV files with embedded commas, quotes, newlines in fields.

### Constraints
- RFC 4180 compliant
- Handle large files (streaming)
- Unicode support
- Error recovery (skip bad rows)

### Solution
**Dedicated CSV library**

Python (csv module):
```python
import csv

with open('data.csv', encoding='utf-8', newline='') as f:
    reader = csv.DictReader(f)
    for row in reader:
        try:
            process(row)
        except ValueError as e:
            print(f"Skipping row {reader.line_num}: {e}")
```

Rust (csv crate):
```rust
use csv::ReaderBuilder;

let mut rdr = ReaderBuilder::new()
    .flexible(true)  // Allow variable column counts
    .from_path("data.csv")?;

for result in rdr.records() {
    match result {
        Ok(record) => process(&record),
        Err(e) => eprintln!("Skip: {}", e),
    }
}
```

**Rationale**:
- Handles quoting, escaping, line breaks correctly
- Streaming for memory efficiency
- Error recovery without crashing

**Alternatives**:
- **Pandas**: For in-memory data analysis (Python)
- **polars**: High-performance DataFrame library (Rust/Python)
- **xsv**: CLI tool for CSV operations

### Pitfalls
- ❌ Splitting on commas with `str.split(',')` (breaks on quoted fields)
- ❌ Not specifying encoding (UTF-8 vs Latin-1)
- ❌ Accumulating all rows in memory

## Scenario 3: Log Colorization and Formatting

### Problem
Add colors to log output for better readability in terminal.

### Constraints
- Detect terminal capabilities (color support)
- No-color mode for pipes/files
- Cross-platform (ANSI codes)

### Solution
**Terminal color library**

Python (rich):
```python
from rich.console import Console
from rich.syntax import Syntax

console = Console()

# Auto-detects terminal capabilities
console.print("[bold red]ERROR[/] Connection failed", style="red")

# Syntax highlighting
code = Syntax(source, "python", theme="monokai")
console.print(code)
```

Rust (colored):
```rust
use colored::*;

if atty::is(atty::Stream::Stdout) {
    println!("{} Connection failed", "ERROR".red().bold());
} else {
    println!("ERROR Connection failed");  // Plain text
}
```

**Rationale**:
- Auto-detects color support (no-color when piped)
- Cross-platform ANSI codes
- Rich formatting (bold, italic, underline)

**Alternatives**:
- **Raw ANSI codes**: For minimal dependencies
- **termcolor**: Rust alternative with Windows support
- **chalk**: JavaScript terminal colors

### Pitfalls
- ❌ Hardcoding ANSI codes (breaks in non-terminal)
- ❌ Not respecting NO_COLOR environment variable
- ❌ Color spam (use sparingly for emphasis)

## Scenario 4: Configuration File Parsing

### Problem
Parse configuration from TOML/YAML/JSON files with validation.

### Constraints
- Type-safe deserialization
- Clear error messages for syntax errors
- Support comments (TOML/YAML)
- Schema validation

### Solution
**Serde (Rust) or pydantic (Python)**

Rust:
```rust
use serde::Deserialize;

#[derive(Deserialize)]
struct Config {
    database: DatabaseConfig,
    server: ServerConfig,
}

let config: Config = toml::from_str(&contents)?;
// Type errors caught at deserialization
```

Python:
```python
from pydantic import BaseModel, validator
import tomllib

class DatabaseConfig(BaseModel):
    host: str
    port: int = 5432

    @validator('port')
    def port_range(cls, v):
        if not (1024 <= v <= 65535):
            raise ValueError('Port out of range')
        return v

class Config(BaseModel):
    database: DatabaseConfig
    server: ServerConfig

with open('config.toml', 'rb') as f:
    data = tomllib.load(f)
    config = Config(**data)  # Validates on construction
```

**Rationale**:
- Type safety prevents runtime errors
- Validation at load time
- Clear error messages with field paths

**Alternatives**:
- **JSON Schema**: For JSON configuration
- **dataclasses**: Simpler Python validation
- **configparser**: For INI-style configs

### Pitfalls
- ❌ Silently using defaults for missing required fields
- ❌ No validation (accepting any values)
- ❌ Exposing secrets in config files (use environment variables)

## Scenario 5: String Template Expansion

### Problem
Expand templates like "Hello, {name}! You have {count} messages."

### Constraints
- Safe against injection
- Support conditionals and loops
- Clear syntax
- Good error messages

### Solution
**Template engine appropriate to use case**

Simple (Python str.format):
```python
template = "Hello, {name}! You have {count} messages."
output = template.format(name=user.name, count=len(messages))
```

Medium (Jinja2):
```python
from jinja2 import Template

template = Template("""
Hello, {{ name }}!
{% if count > 0 %}
  You have {{ count }} new messages.
{% else %}
  No new messages.
{% endif %}
""")

output = template.render(name=user.name, count=len(messages))
```

Complex (Tera/Handlebars):
```rust
use tera::Tera;

let mut tera = Tera::default();
tera.add_raw_template("email", template)?;

let context = tera::Context::from_serialize(&data)?;
let output = tera.render("email", &context)?;
```

**Rationale**:
- str.format: Simple placeholders, no logic
- Jinja2/Tera: Conditionals, loops, filters
- Auto-escaping prevents injection

**Alternatives**:
- **f-strings**: Python inline formatting
- **format!**: Rust macro for simple cases
- **Mustache**: Logic-less templates (language-agnostic)

### Pitfalls
- ❌ Using eval() for templating (security nightmare)
- ❌ Complex logic in templates (belongs in code)
- ❌ Not escaping when rendering HTML

## Scenario 6: Text Diff and Patching

### Problem
Show differences between text files, apply patches.

### Constraints
- Line-based diff
- Human-readable output
- Patch application with conflict detection

### Solution
**Difflib or dedicated diff library**

Python (difflib):
```python
import difflib

def show_diff(old_text, new_text):
    old_lines = old_text.splitlines(keepends=True)
    new_lines = new_text.splitlines(keepends=True)

    diff = difflib.unified_diff(
        old_lines, new_lines,
        fromfile='old.txt',
        tofile='new.txt',
        lineterm=''
    )

    return ''.join(diff)

# Highlight differences in terminal
def html_diff(old_text, new_text):
    differ = difflib.HtmlDiff()
    return differ.make_file(
        old_text.splitlines(),
        new_text.splitlines()
    )
```

Rust (similar):
```rust
use similar::{ChangeTag, TextDiff};

let diff = TextDiff::from_lines(old, new);

for change in diff.iter_all_changes() {
    let sign = match change.tag() {
        ChangeTag::Delete => "-",
        ChangeTag::Insert => "+",
        ChangeTag::Equal => " ",
    };
    print!("{}{}", sign, change);
}
```

**Rationale**:
- Standard unified diff format
- Efficient algorithms (Myers diff)
- HTML output for web display

**Alternatives**:
- **git diff**: For version-controlled files
- **patience diff**: Better heuristics for code
- **semantic diff**: For AST-based code comparison

### Pitfalls
- ❌ Not normalizing line endings (CRLF vs LF)
- ❌ Large diffs overwhelming output (paginate or summarize)
- ❌ No conflict detection when applying patches

## Scenario 7: Progress Bar with ETA

### Problem
Show progress for long-running operations (file processing, downloads).

### Constraints
- Real-time updates
- ETA calculation
- Works in terminal and logs
- Minimal overhead

### Solution
**Progress bar library with smart terminal detection**

Python (tqdm):
```python
from tqdm import tqdm

for item in tqdm(items, desc="Processing"):
    process(item)

# With custom metrics
with tqdm(total=file_size, unit='B', unit_scale=True) as pbar:
    for chunk in download():
        pbar.update(len(chunk))
```

Rust (indicatif):
```rust
use indicatif::ProgressBar;

let pb = ProgressBar::new(items.len() as u64);
pb.set_style(
    indicatif::ProgressStyle::default_bar()
        .template("{msg} [{bar:40}] {pos}/{len} (ETA: {eta})")
);

for item in items {
    process(item);
    pb.inc(1);
}

pb.finish_with_message("Done");
```

**Rationale**:
- Auto-hides in non-terminal output
- Accurate ETA based on historical rate
- Minimal performance impact

**Alternatives**:
- **Simple print statements**: For basic logging
- **Logging framework**: For structured logs

### Pitfalls
- ❌ Progress bar in logs/files (use isatty check)
- ❌ Updating too frequently (thrashing terminal)
- ❌ Not finalizing progress bar (leaves partial state)
