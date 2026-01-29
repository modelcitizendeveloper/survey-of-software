# Scenario: Legacy Taiwan Banking System Integration

## Context

**Business**: Taiwan bank with 30-year-old core banking system
**Current state**: Exports Big5-encoded CSV files for reports/integrations
**Goal**: Integrate with modern UTF-8 REST API for mobile banking
**Volume**: 10,000 files/day, 50KB-5MB each
**Data type**: Customer names, transactions, account statements (financial data)

## Requirements Analysis

| Requirement | Priority | Constraint |
|-------------|----------|------------|
| **Accuracy** | CRITICAL | Financial data, 100% fidelity required |
| **Performance** | HIGH | Must complete nightly batch (8 hours) |
| **Reversibility** | MEDIUM | May need to trace back to original |
| **Error handling** | CRITICAL | Must detect/log any conversion issues |
| **Compliance** | HIGH | Banking regulations, audit trail |

### Pain Points

1. **Big5-HKSCS characters**: 8% of files have Hong Kong customer names
2. **Private Use Area (PUA)**: Legacy system uses vendor-specific characters
3. **Corrupted files**: Occasional file truncation/corruption
4. **Validation**: Need to prove conversion was lossless

## Library Selection

### Detection: **Skip** (Encoding is known)
- Files are guaranteed Big5 or Big5-HKSCS
- No need for charset-normalizer/cchardet
- Use file metadata/header to determine variant

### Transcoding: **Python codecs** with `big5hkscs`
- Use `big5hkscs` codec (superset of Big5)
- Handles Hong Kong characters correctly
- Fast C implementation

### Repair: **Skip** (Files are not mojibake)
- ftfy not needed (files are cleanly encoded)
- If corruption, reject file (don't repair)

### CJK Conversion: **Not needed**
- Keep Traditional Chinese (Taiwan customer base)
- No Simplified conversion required

## Integration Pattern

```python
import csv
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

def convert_big5_csv_to_utf8(input_file, output_file):
    """
    Convert Big5 CSV to UTF-8 with validation

    Returns:
        dict: {
            'success': bool,
            'rows_converted': int,
            'errors': list,
        }
    """
    errors = []
    rows_converted = 0

    try:
        # Step 1: Read as Big5-HKSCS (handles both Big5 and HKSCS)
        with open(input_file, 'r', encoding='big5hkscs', errors='strict') as f_in:
            reader = csv.DictReader(f_in)
            rows = list(reader)

        # Step 2: Validate (check for replacement characters)
        for i, row in enumerate(rows):
            for key, value in row.items():
                if '�' in value:
                    errors.append({
                        'row': i,
                        'column': key,
                        'error': 'Replacement character found',
                    })

        # Step 3: Write as UTF-8
        if not errors:
            with open(output_file, 'w', encoding='utf-8', newline='') as f_out:
                if rows:
                    writer = csv.DictWriter(f_out, fieldnames=rows[0].keys())
                    writer.writeheader()
                    writer.writerows(rows)
                    rows_converted = len(rows)

        return {
            'success': len(errors) == 0,
            'rows_converted': rows_converted,
            'errors': errors,
        }

    except UnicodeDecodeError as e:
        logger.error(f"Encoding error in {input_file}: {e}")
        return {
            'success': False,
            'rows_converted': 0,
            'errors': [{'error': str(e)}],
        }
    except Exception as e:
        logger.error(f"Unexpected error in {input_file}: {e}")
        return {
            'success': False,
            'rows_converted': 0,
            'errors': [{'error': str(e)}],
        }
```

## Error Handling Strategy

### 1. Strict Mode with Logging
```python
# Use errors='strict' to catch any invalid sequences
# Don't silently replace (� characters in financial data is unacceptable)
try:
    text = big5_bytes.decode('big5hkscs', errors='strict')
except UnicodeDecodeError as e:
    # Log exact position of error
    logger.error(f"Decode error at byte {e.start}: {e.reason}")
    # Quarantine file for manual review
    quarantine_file(input_file)
    raise
```

### 2. Validate After Conversion
```python
def validate_conversion(original_file, converted_file):
    """
    Verify no data loss in conversion
    """
    # Count rows
    with open(original_file, 'r', encoding='big5hkscs') as f:
        original_rows = sum(1 for _ in f) - 1  # -1 for header

    with open(converted_file, 'r', encoding='utf-8') as f:
        converted_rows = sum(1 for _ in f) - 1

    assert original_rows == converted_rows, "Row count mismatch"

    # Check for replacement characters
    with open(converted_file, 'r', encoding='utf-8') as f:
        content = f.read()
        assert '�' not in content, "Replacement characters found"

    return True
```

### 3. Audit Trail
```python
import hashlib
import json

def log_conversion(input_file, output_file, result):
    """
    Create audit record for compliance
    """
    audit_record = {
        'timestamp': datetime.now().isoformat(),
        'input_file': str(input_file),
        'output_file': str(output_file),
        'input_size': input_file.stat().st_size,
        'output_size': output_file.stat().st_size,
        'input_hash': hashlib.sha256(input_file.read_bytes()).hexdigest(),
        'output_hash': hashlib.sha256(output_file.read_bytes()).hexdigest(),
        'rows_converted': result['rows_converted'],
        'success': result['success'],
        'errors': result['errors'],
    }

    # Append to audit log
    with open('conversion_audit.jsonl', 'a') as f:
        f.write(json.dumps(audit_record) + '\n')
```

## Performance Optimization

### Batch Processing with Parallelization

```python
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

def process_batch(input_dir, output_dir, max_workers=8):
    """
    Process entire directory in parallel
    """
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)

    # Collect all files
    files = list(input_path.glob('*.csv'))

    def process_one(input_file):
        output_file = output_path / input_file.name
        result = convert_big5_csv_to_utf8(input_file, output_file)

        # Validate
        if result['success']:
            validate_conversion(input_file, output_file)

        # Audit log
        log_conversion(input_file, output_file, result)

        return result

    # Process in parallel
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        results = list(executor.map(process_one, files))

    # Summary
    total = len(results)
    successful = sum(1 for r in results if r['success'])
    failed = total - successful

    return {
        'total': total,
        'successful': successful,
        'failed': failed,
        'results': results,
    }
```

**Performance estimate**:
- Single file (1MB): 45ms (transcoding) + 10ms (validation) = 55ms
- 10,000 files: 550s (sequential) / 70s (8 workers) = ~1 minute with parallelization

## Testing Strategy

### Unit Tests
```python
def test_basic_conversion():
    """Test simple Big5 → UTF-8"""
    input_data = "客戶,金額\n王小明,1000\n".encode('big5')
    # ... test conversion

def test_hkscs_characters():
    """Test Hong Kong supplementary characters"""
    # Use actual HKSCS characters in test
    input_data = "姓名,地址\n陳大文,香港\n".encode('big5hkscs')
    # ... verify no data loss

def test_corrupted_file():
    """Test error handling for corrupted files"""
    corrupted = b'\xa4\xa4\xff\xfe'  # Invalid Big5 sequence
    # ... should raise UnicodeDecodeError

def test_private_use_area():
    """Test PUA characters (vendor-specific)"""
    # These may not convert cleanly
    # Should be logged for manual review
```

### Integration Tests
```python
def test_end_to_end_batch():
    """Test full batch processing"""
    # Create test directory with 100 files
    # Run batch processor
    # Verify:
    # - All files converted
    # - No errors
    # - Audit log created
    # - Row counts match
```

### Smoke Tests on Production Data
```python
def test_sample_production_files():
    """Run on 1% sample of real data"""
    # Pick 100 random files from production
    # Convert
    # Manual review of random samples
    # Build confidence before full migration
```

## Trade-offs & Decisions

| Decision | Chosen | Alternative | Rationale |
|----------|--------|-------------|-----------|
| **Encoding codec** | big5hkscs | big5 | Superset, handles Hong Kong clients |
| **Error mode** | strict | replace | Financial data, can't accept loss |
| **Validation** | Always | Spot-check | Compliance requirement |
| **Repair** | No ftfy | Use ftfy | Files are clean, not mojibake |
| **Parallelization** | 8 workers | Sequential | 8x speedup, easily meets SLA |

## Rollout Plan

### Phase 1: Validation (Week 1)
- Convert 100 sample files
- Manual review of output
- Audit trail verification
- Performance testing

### Phase 2: Pilot (Week 2)
- Convert 1 day's worth of files
- Run in shadow mode (parallel to legacy)
- Compare outputs
- Fix any edge cases

### Phase 3: Staged Rollout (Week 3-4)
- Process 10% of files through new pipeline
- Increase to 50%, then 100%
- Monitor error rates
- Keep audit logs for 90 days

### Phase 4: Decommission (Week 5)
- Fully migrate to UTF-8 pipeline
- Archive Big5 conversion scripts
- Document for future reference

## Monitoring & Alerting

```python
# Key metrics to track
metrics = {
    'files_processed': Counter(),
    'files_failed': Counter(),
    'processing_time_ms': Histogram(),
    'rows_converted': Counter(),
}

# Alerts
if failure_rate > 0.1%:  # SLO: <0.1% errors
    alert('High conversion error rate')

if processing_time > 2 * expected:
    alert('Processing time degradation')
```

## Success Criteria

- [ ] 100% of files converted with no data loss
- [ ] Processing completes within 8-hour batch window
- [ ] Audit trail for all conversions
- [ ] Error rate < 0.1%
- [ ] Manual spot-check of 1% sample passes
- [ ] Compliance sign-off from audit team

## Estimated Effort

- Development: 2-3 days (conversion + validation + audit)
- Testing: 3-4 days (unit + integration + production samples)
- Rollout: 2-3 weeks (phased approach)
- **Total**: 1 month from start to full production
