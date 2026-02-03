# Latin Training Utilities - Test Suite

Comprehensive test suite for Latin grammar training utilities using pytest.

## Test Organization

### Test Files

- **test_form_generator.py**: Unit tests for FormGenerator class
  - Stem extraction for all 5 declensions
  - Form generation (regular and irregular)
  - Ambiguous form detection
  - Neuter noun handling
  - Irregular vocative patterns

- **test_exercise_builder.py**: Unit tests for ExerciseBuilder class
  - Single declension exercises (01-05)
  - Single case exercises (06-11)
  - Single number exercises (12-13)
  - Integration exercises (14-15)
  - Word rotation and selection

- **test_latin_trainer.py**: Unit tests for LatinTrainer class
  - Interpretation checking (simple and ambiguous)
  - Vocabulary extraction from exercises
  - POS/case/number/declension validation

- **test_integration.py**: Integration tests for complete workflows
  - End-to-end exercise generation
  - JSONL file structure validation
  - Series metadata validation
  - Real series validation (model-nouns, common-nouns)

- **test_data_validation.py**: Data validation tests
  - JSONL format compliance
  - Required field presence
  - Valid value constraints
  - Ambiguous form correctness
  - Sentence structure integrity

## Running Tests

### Install Test Dependencies

```bash
# Using uv (recommended)
uv pip install -r requirements-test.txt

# Using pip
pip install -r requirements-test.txt
```

### Run All Tests

```bash
pytest
```

### Run Specific Test Categories

```bash
# Unit tests only
pytest -m unit

# Integration tests only
pytest -m integration

# Data validation tests only
pytest -m data

# Generator tests only
pytest -m generator

# Trainer tests only
pytest -m trainer

# Skip slow tests
pytest -m "not slow"
```

### Run Specific Test Files

```bash
# Test form generation
pytest tests/test_form_generator.py

# Test exercise building
pytest tests/test_exercise_builder.py

# Test latin trainer
pytest tests/test_latin_trainer.py
```

### Run with Coverage

```bash
pytest --cov=exercises --cov=bin --cov-report=html
```

### Run in Parallel

```bash
pytest -n auto  # Use all available CPUs
pytest -n 4     # Use 4 workers
```

### Verbose Output

```bash
pytest -v               # Verbose
pytest -vv              # Extra verbose
pytest -v --tb=short    # Short traceback
```

## Test Markers

Tests are categorized with pytest markers:

- `@pytest.mark.unit`: Unit tests for individual functions/classes
- `@pytest.mark.integration`: Integration tests across components
- `@pytest.mark.data`: Data validation tests for JSONL files
- `@pytest.mark.slow`: Tests that take more than 1 second
- `@pytest.mark.generator`: Tests for vocabulary exercise generator
- `@pytest.mark.trainer`: Tests for latin-train interactive trainer

## Test Coverage

Current test coverage:

### FormGenerator
- ✅ Stem extraction (all 5 declensions)
- ✅ Regular form generation
- ✅ Irregular forms (vir, filius, homo, nomen)
- ✅ Neuter nouns (nom = acc)
- ✅ Ambiguous forms (gen/dat, dat/abl, nom/acc/voc)

### ExerciseBuilder
- ✅ Single declension exercises
- ✅ Single case exercises
- ✅ Single number exercises
- ✅ Integration exercises
- ✅ Word selection and rotation
- ✅ Word data structure

### LatinTrainer
- ✅ Interpretation checking
- ✅ Ambiguous case handling
- ✅ Vocabulary extraction
- ✅ Multiple word handling

### Integration
- ✅ End-to-end generation
- ✅ File structure validation
- ✅ Metadata correctness
- ✅ Exercise type validation

### Data Validation
- ✅ JSONL format compliance
- ✅ Required fields
- ✅ Valid value constraints
- ✅ Ambiguous form correctness
- ✅ Sentence structure

## Fixtures

Reusable test fixtures defined in `conftest.py`:

- `declension_templates`: Loaded declension templates JSON
- `sample_vocabulary`: Sample vocabulary data for testing
- `sample_exercise_line`: Sample exercise line in JSONL format
- `model_nouns_vocab`: Vocabulary for model nouns series
- `temp_exercise_dir`: Temporary directory for testing file operations

## TDD Workflow

### Writing New Features

1. **Write test first** (Red)
   ```python
   def test_new_feature():
       # Arrange
       generator = FormGenerator(templates)

       # Act
       result = generator.new_feature()

       # Assert
       assert result == expected
   ```

2. **Run test (should fail)**
   ```bash
   pytest tests/test_new_feature.py::test_new_feature -v
   ```

3. **Implement feature** (Green)
   - Write minimal code to pass test

4. **Run test (should pass)**
   ```bash
   pytest tests/test_new_feature.py::test_new_feature -v
   ```

5. **Refactor** (Refactor)
   - Improve code quality
   - Run tests to ensure no regression

### Example TDD Cycle

```bash
# 1. Write failing test
vim tests/test_form_generator.py

# 2. Run test (should fail)
pytest tests/test_form_generator.py::TestFormGenerator::test_handle_defective_nouns -v

# 3. Implement feature
vim exercises/generate-vocabulary-exercises.py

# 4. Run test (should pass)
pytest tests/test_form_generator.py::TestFormGenerator::test_handle_defective_nouns -v

# 5. Run all tests to ensure no regression
pytest
```

## Continuous Testing

### Watch Mode (requires pytest-watch)

```bash
pip install pytest-watch
ptw -- -v
```

### Pre-commit Hook

Add to `.git/hooks/pre-commit`:

```bash
#!/bin/bash
pytest -m "not slow" --tb=short
```

## Troubleshooting

### Import Errors

If you get import errors, ensure the project paths are correct in `conftest.py`:

```python
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT / 'exercises'))
```

### Failed Data Validation Tests

If data validation tests fail, check:
1. JSONL files are properly formatted (one JSON object per line)
2. Metadata line is first in each file
3. All required fields are present in word data
4. Case values are valid (string or list of strings)

### Slow Tests

To skip slow tests during development:

```bash
pytest -m "not slow"
```

## Adding New Tests

### Template for New Test Class

```python
import pytest

@pytest.mark.unit
@pytest.mark.generator
class TestNewFeature:
    """Test description."""

    def test_basic_functionality(self):
        """Test basic functionality."""
        # Arrange
        setup_data = prepare_test_data()

        # Act
        result = function_under_test(setup_data)

        # Assert
        assert result == expected_value

    def test_edge_case(self):
        """Test edge case handling."""
        # Test edge case
        pass

    def test_error_handling(self):
        """Test error handling."""
        with pytest.raises(ExpectedException):
            function_that_should_fail()
```

## Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [Pytest Best Practices](https://docs.pytest.org/en/stable/goodpractices.html)
- [Test-Driven Development](https://en.wikipedia.org/wiki/Test-driven_development)
