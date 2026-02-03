# Use Case: Python API Backends

## Context

Python backend APIs (Flask, FastAPI, Django REST Framework) require testing across:
- Individual function/method behavior (business logic)
- API endpoint contracts (request/response validation)
- Database operations and ORM queries
- Authentication and authorization
- External service integration (payment, email, etc.)
- Error handling and edge cases

Testing pyramid emphasis: **60% unit, 30% integration, 10% E2E**

## Requirements

### Must-Have Capabilities
1. Fast test execution for TDD workflows
2. Fixture management for test data
3. Database transaction rollback between tests
4. HTTP client for API testing
5. Mocking external dependencies
6. Parametrized tests for multiple scenarios
7. Coverage reporting
8. Async/await support (FastAPI)

### Nice-to-Have
- Test parallelization
- Property-based testing
- Load testing integration
- OpenAPI schema validation
- Mutation testing

## Primary Recommendation: pytest + pytest-flask/fastapi

### Rationale
**pytest** is the de facto standard for Python testing:
- Intuitive assert statements (no special assertions)
- Powerful fixture system
- Excellent plugin ecosystem
- Native async support
- Parametrization for data-driven tests

**Framework-specific plugins** provide essential helpers:
- `pytest-flask`: Test client, database fixtures
- `pytest-asyncio`: Async test support
- `pytest-cov`: Coverage reporting
- `pytest-mock`: Enhanced mocking

### Setup Complexity: Low
```python
# pyproject.toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_functions = ["test_*"]
addopts = [
    "--cov=app",
    "--cov-report=term-missing",
    "--cov-report=html",
    "-v"
]
asyncio_mode = "auto"
```

Time to first test: **~10 minutes**

### Sample Test Pattern

#### Unit Test: Business Logic
```python
import pytest
from app.services.pricing import calculate_total

@pytest.mark.parametrize("subtotal,tax_rate,expected", [
    (100.00, 0.08, 108.00),
    (50.00, 0.10, 55.00),
    (0.00, 0.08, 0.00),
])
def test_calculate_total(subtotal, tax_rate, expected):
    result = calculate_total(subtotal, tax_rate)
    assert result == expected
```

#### Integration Test: API Endpoint
```python
import pytest
from flask import Flask

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def auth_headers(create_user):
    # Fixture creates user and returns auth token
    token = create_user("test@example.com")
    return {"Authorization": f"Bearer {token}"}

def test_create_order(client, auth_headers, db_session):
    # Arrange
    payload = {
        "items": [{"product_id": "123", "quantity": 2}],
        "shipping_address": "123 Main St"
    }

    # Act
    response = client.post(
        "/api/orders",
        json=payload,
        headers=auth_headers
    )

    # Assert
    assert response.status_code == 201
    data = response.get_json()
    assert data["order_id"] is not None
    assert data["status"] == "pending"

    # Verify database state
    order = db_session.query(Order).get(data["order_id"])
    assert order.user_id == auth_headers["user_id"]
```

#### Mock External Service
```python
import pytest
from unittest.mock import patch

def test_send_confirmation_email(client, mocker):
    # Mock external email service
    mock_send = mocker.patch("app.services.email.send_email")

    response = client.post("/api/orders", json={...})

    mock_send.assert_called_once_with(
        to="customer@example.com",
        template="order_confirmation",
        context=mocker.ANY
    )
```

### CI/CD Integration
```yaml
# .github/workflows/test.yml
- name: Install dependencies
  run: |
    pip install -e ".[test]"

- name: Run tests
  run: pytest --cov --cov-report=xml

- name: Upload coverage
  uses: codecov/codecov-action@v3

- name: Run integration tests
  run: pytest tests/integration -v
  env:
    DATABASE_URL: postgresql://test:test@localhost/test_db
```

**Parallel execution**: Use `pytest-xdist` with `-n auto`
**Cache strategy**: Cache pip dependencies, pytest cache
**Typical runtime**: 1-3 minutes for 300+ tests

## Alternative Options

### Option B: unittest (Standard Library)

**When to choose**: Zero dependencies required, legacy codebases

**Advantages**:
- No external dependencies
- Familiar to Java/C# developers (xUnit style)
- Built into Python standard library

**Disadvantages**:
- Verbose test writing (setUp/tearDown)
- No fixture system
- Less readable assertions (assertEqual vs assert)
- Limited plugin ecosystem

**Setup complexity**: Minimal (no installation needed)

### Option C: pytest + hypothesis

**When to choose**: Complex business logic, edge case discovery

**Advantages**:
- Property-based testing finds unexpected bugs
- Automatic test case generation
- Shrinking to minimal failing examples

**Disadvantages**:
- Steeper learning curve
- Slower test execution
- Can produce flaky tests if not carefully designed

**Setup complexity**: Medium (requires understanding property-based testing)

## Implementation Strategy

### Phase 1: Foundation (Day 1)
1. Install pytest and essential plugins
2. Configure pytest.ini and coverage
3. Set up database fixtures (create/teardown)
4. Write first unit and integration tests

### Phase 2: Patterns (Week 1)
1. Create fixture library for common scenarios
2. Establish mocking patterns for external services
3. Document testing best practices
4. Set up pre-commit hooks (pytest + ruff)

### Phase 3: Coverage (Week 2-4)
1. Test critical business logic (unit tests)
2. Test all API endpoints (integration tests)
3. Add authentication/authorization tests
4. Achieve 85%+ coverage with quality gates

## Validation Results

### Speed Benchmarks
- **Initial test run**: 2.8s for 200 tests (unit only)
- **With database**: 12s for 200 tests (including setup/teardown)
- **Parallel execution**: 4s with `-n 4` flag
- **CI full suite**: 90s including linting and coverage

### Developer Experience Metrics
- Time to write first test: 5 minutes (experienced Python dev)
- Average test writing time: 2-4 minutes per function
- Debugging clarity: High (clear diffs, fixture inspection)

### Maintenance Burden
- **Low to Medium**: Tests break when API contracts change
- Unit tests are very stable
- Integration tests need updates with schema changes
- Mock assertions require maintenance when service contracts evolve

## Known Gaps

### What This Solution Cannot Handle
1. **Load testing** - Needs Locust or k6
2. **Contract testing** - Needs Pact or Postman
3. **Real browser testing** - Needs Selenium/Playwright
4. **Production monitoring** - Needs Sentry or Datadog

### Scenarios Requiring Additional Tools
- **API schema validation**: Add `pydantic` or `marshmallow`
- **Database migrations**: Add `alembic` testing
- **Message queue testing**: Add `pytest-celery` or similar
- **Multi-service integration**: Add Docker Compose for test environment

## Recommended Tool Stack

**Minimal viable testing**:
```
pytest
pytest-cov
pytest-mock
```

**Production-ready stack**:
```
pytest
pytest-cov
pytest-asyncio (for FastAPI)
pytest-xdist (parallelization)
pytest-mock
faker (test data generation)
```

**Enterprise stack**:
```
Above tools plus:
hypothesis (property-based testing)
pytest-django/flask/fastapi (framework integration)
pytest-postgresql (real database testing)
locust (load testing)
```

## Database Testing Strategy

### Approach 1: In-Memory SQLite (Fast)
```python
@pytest.fixture(scope="session")
def db_engine():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    return engine
```

**Pros**: Extremely fast, no cleanup needed
**Cons**: SQLite quirks differ from PostgreSQL/MySQL

### Approach 2: Transaction Rollback (Accurate)
```python
@pytest.fixture
def db_session(db_engine):
    connection = db_engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()
```

**Pros**: Tests real database, isolated tests
**Cons**: Slower than in-memory

### Approach 3: Docker Test Database (Production-like)
```python
@pytest.fixture(scope="session")
def db_container():
    container = start_postgres_container()
    yield container
    container.stop()
```

**Pros**: Exact production environment
**Cons**: Slowest, requires Docker

**Recommendation**: Use Approach 2 for local development, Approach 3 for CI

## Cost-Benefit Analysis

### Setup Investment
- **Time**: 1 day for full test infrastructure
- **Training**: 4 hours for team onboarding
- **Tooling cost**: Free (all open source)

### Ongoing Returns
- **Bug prevention**: Catch 80-90% of logic bugs before production
- **Refactoring confidence**: Safe database schema migrations
- **Development speed**: TDD often faster than manual testing
- **Documentation**: Tests document API behavior

## Migration Path

### From unittest
1. Install pytest (compatible with unittest tests)
2. Run existing tests with pytest
3. Gradually convert to pytest style
4. Add fixtures to replace setUp/tearDown

**Effort**: 1-2 weeks for gradual migration
**Risk**: Low (backward compatibility)

### From No Testing
1. Start with critical business logic (unit tests)
2. Add tests for new features first
3. Cover high-risk endpoints (authentication, payments)
4. Gradually increase coverage

**Effort**: Ongoing over 2-4 months
**Risk**: None (incremental adoption)

## FastAPI-Specific Considerations

### Async Test Support
```python
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_async_endpoint(async_client: AsyncClient):
    response = await async_client.get("/api/users/123")
    assert response.status_code == 200
```

### Dependency Injection Override
```python
from fastapi import Depends

def test_with_mock_dependency(client, app):
    def mock_get_db():
        # Return test database
        pass

    app.dependency_overrides[get_db] = mock_get_db
    response = client.get("/api/data")
    assert response.status_code == 200
```

### OpenAPI Schema Testing
```python
def test_openapi_schema(client):
    response = client.get("/openapi.json")
    schema = response.json()

    # Validate schema structure
    assert "paths" in schema
    assert "/api/users" in schema["paths"]
```
