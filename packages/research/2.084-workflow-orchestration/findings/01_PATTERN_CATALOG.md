# Workflow Orchestration Pattern Catalog

Research across Temporal, Apache Airflow, Prefect, and Dagster to extract patterns
for lightweight MCP workflow orchestration (Judith/SMCP).

---

## 1. DAG Definition Patterns

### 1.1 Code-First (Temporal, Prefect)

**Pattern**: Workflows defined as native code with decorators/annotations.

```python
# Prefect style
@flow
def my_workflow():
    result = task_a()
    return task_b(result)

@task
def task_a():
    return fetch_data()
```

**Characteristics**:
- Full language expressiveness (loops, conditionals, error handling)
- IDE support, type checking, testing with standard tools
- Dependencies implicit from data flow
- Dynamic task generation at runtime

**Temporal's Philosophy**: Argues against static DAGs for complex scenarios.
Dynamic error paths in a static DAG become unwieldy; same logic is ~20 lines of code.
Workflows are "code-native durable execution" not "DAG engines."

### 1.2 Declarative DAG (Airflow, Dagster, Kestra)

**Pattern**: Explicit DAG structure with operators/ops connected by dependencies.

```python
# Airflow style
with DAG("my_dag") as dag:
    t1 = PythonOperator(task_id="extract", python_callable=extract)
    t2 = PythonOperator(task_id="transform", python_callable=transform)
    t3 = PythonOperator(task_id="load", python_callable=load)
    t1 >> t2 >> t3
```

**Characteristics**:
- Visual representation in UI
- Clear dependency declaration
- Static analysis possible
- Separation between DAG definition and task logic

### 1.3 Asset-Centric (Dagster)

**Pattern**: Define what data assets should exist; system infers execution.

```python
@asset
def raw_data():
    return fetch_from_api()

@asset
def processed_data(raw_data):
    return transform(raw_data)
```

**Characteristics**:
- Declarative: define "what" not "how"
- Automatic lineage tracking
- Built-in data quality integration
- Dependencies inferred from function signatures

### 1.4 Hybrid: Graph-Backed Assets

**Pattern**: Wrap existing op graphs as assets for lineage benefits without rewrite.

**Use Case**: Migration path from task-based to asset-based thinking.

---

## 2. Task State Machine Patterns

### 2.1 Minimal State Set (Recommended for Lightweight)

| State | Description | Terminal? |
|-------|-------------|-----------|
| PENDING | Awaiting execution | No |
| RUNNING | Currently executing | No |
| COMPLETED | Finished successfully | Yes |
| FAILED | Execution error | Yes |

### 2.2 Extended State Set (Full Orchestrators)

| State | Description | Terminal? | Need for SMCP? |
|-------|-------------|-----------|----------------|
| SCHEDULED | Waiting for trigger time | No | Maybe |
| QUEUED | Waiting for worker slot | No | Skip |
| RUNNING | Executing | No | Yes |
| RETRYING | Retry in progress | No | Yes (as RUNNING) |
| AWAITING_RETRY | Waiting before retry | No | Skip (use delay) |
| PAUSED | User paused | No | Skip |
| CANCELLED | User cancelled | Yes | Maybe |
| COMPLETED | Success | Yes | Yes |
| FAILED | Error after all retries | Yes | Yes |
| CRASHED | Infrastructure failure | Yes | Skip (treat as FAILED) |

### 2.3 State Transition Diagram (Airflow)

```
none -> SCHEDULED -> QUEUED -> RUNNING -> SUCCESS
                                      \-> FAILED -> (retry?) -> RUNNING
```

### 2.4 Prefect State Philosophy

- **State Type**: Drives orchestration logic (RUNNING, COMPLETED, FAILED)
- **State Name**: Visual bookkeeping ("Running", "Retrying", "Crashed")

A retrying task has type=RUNNING but name="Retrying" for UI clarity.

---

## 3. Retry and Backoff Patterns

### 3.1 Exponential Backoff (Temporal Default)

```
next_delay = min(initial_interval * (backoff_coefficient ^ attempt), max_interval)
```

**Default Configuration**:
- `initial_interval`: 1 second
- `backoff_coefficient`: 2.0
- `max_interval`: 100 seconds (100x initial)
- `max_attempts`: unlimited (until timeout)

### 3.2 Retry Policy Components

| Component | Purpose | SMCP Recommendation |
|-----------|---------|---------------------|
| Initial Interval | First retry delay | Yes (e.g., 1s) |
| Backoff Coefficient | Delay multiplier | Yes (e.g., 2.0) |
| Max Interval | Cap on delay | Yes (e.g., 60s) |
| Max Attempts | Hard limit on retries | Yes (e.g., 3) |
| Non-Retryable Errors | Skip retry for specific errors | Yes |
| Timeout | Total time budget | Maybe |

### 3.3 Non-Retryable Error Classification

```python
# Temporal pattern
non_retryable_errors = [
    "InsufficientFundsError",    # Business logic failure
    "InvalidInputError",         # Bad request
    "AuthenticationError",       # Won't succeed with retry
]
```

**Principle**: Only retry transient failures (network, temporary unavailability).
Don't retry deterministic failures.

### 3.4 Activity vs Workflow Retry (Temporal)

- **Activities**: Default retry policy (operations may fail)
- **Workflows**: No default retry (deterministic, shouldn't fail randomly)

---

## 4. Trigger Patterns

### 4.1 Schedule-Based (Cron)

**Pattern**: Run at fixed times using cron syntax.

```python
# Airflow
schedule="0 9 * * MON"  # Every Monday at 9 AM UTC

# Prefect
@flow
def my_flow():
    ...
my_flow.serve(cron="0 9 * * MON")
```

**Use Cases**: Regular ETL, reports, batch processing.

### 4.2 Event-Driven

**Patterns by Source**:

| Source | Example | Implementation |
|--------|---------|----------------|
| File Arrival | S3 object created | Sensor polling or webhook |
| Message Queue | Kafka/SQS message | Consumer integration |
| HTTP Webhook | External API call | Webhook endpoint |
| Database Change | CDC event | Debezium + webhook |
| Asset Update | Upstream data changed | Asset sensor (Dagster) |

**Airflow Evolution**: Sensors (polling) -> Deferrable operators -> Event triggers (push).

**Prefect**: Native webhook support, automations system for event-to-action mapping.

### 4.3 Manual/API Trigger

**Pattern**: Start workflow via API call or UI button.

```bash
# Temporal CLI
temporal workflow start --task-queue my-queue --workflow-type MyWorkflow

# Airflow API
curl -X POST /api/v1/dags/{dag_id}/dagRuns
```

### 4.4 Signal-Based (Temporal)

**Pattern**: Send data to running workflow, optionally starting it.

```go
// Signal-With-Start: start if not running, then signal
client.SignalWithStartWorkflow(ctx, workflowID, signalName, signalArg, options, workflow)
```

**Use Cases**: User actions, external events that should update workflow state.

### 4.5 Dependency/Data-Driven (Dagster)

**Pattern**: Run when upstream assets are materialized.

```python
@asset_sensor(asset_key=AssetKey("upstream_data"), job=downstream_job)
def my_sensor(context, asset_event):
    return RunRequest()
```

---

## 5. Workflow Composition Patterns

### 5.1 Monoflow (Prefect)

**Pattern**: Single flow with linear task chain.

```python
@flow
def etl_pipeline():
    raw = extract()
    clean = transform(raw)
    load(clean)
```

**When**: Simple, straightforward pipelines.

### 5.2 Subflows (Prefect)

**Pattern**: Flows calling other flows for modularity.

```python
@flow
def main_flow():
    result_a = subflow_a()  # Another @flow
    result_b = subflow_b(result_a)
```

**When**: Large flows needing logical decomposition or team ownership boundaries.

### 5.3 Orchestrator Pattern (Prefect)

**Pattern**: Flow triggers deployed flows on separate infrastructure.

```python
@flow
def orchestrator():
    run_deployment("heavy-compute/gpu-flow")  # Runs elsewhere
    # Can wait or fire-and-forget
```

**When**: Different infrastructure requirements per step.

### 5.4 Child Workflows (Temporal)

**Pattern**: Workflows spawning other workflows with lifecycle control.

**Options**:
- ABANDON: Parent completion doesn't affect child
- TERMINATE: Parent termination terminates child
- REQUEST_CANCEL: Parent cancellation requests child cancel

### 5.5 Saga Pattern (Temporal)

**Pattern**: Compensating transactions for distributed operations.

```python
def transfer_saga():
    try:
        debit(source_account)
        credit(target_account)
    except Exception:
        # Compensate
        refund(source_account)
        raise
```

**When**: Multi-step operations needing atomic-like guarantees.

---

## 6. Durability and Persistence Patterns

### 6.1 Event Sourcing (Temporal)

**Pattern**: All workflow state changes persisted as events.

- Every activity result, timer, signal persisted
- Workflow can replay from any point
- Survives worker crashes, server restarts

### 6.2 Checkpointing (Prefect, Airflow)

**Pattern**: Task results cached, retry resumes from last checkpoint.

```python
@task(cache_key_fn=task_input_hash, cache_expiration=timedelta(hours=1))
def expensive_computation(data):
    ...
```

### 6.3 Durable Timers (Temporal)

**Pattern**: Sleep survives infrastructure failures.

```python
await workflow.sleep(timedelta(days=7))  # Persisted, survives crash
```

**Characteristic**: Single worker can await millions of timers (no resource consumption while waiting).

---

## 7. Error Handling Patterns

### 7.1 Structured Error Classification

| Category | Retry? | Example |
|----------|--------|---------|
| Transient | Yes | Network timeout, rate limit |
| Infrastructure | Maybe | Worker OOM, container eviction |
| Application | No | Validation error, bad input |
| Timeout | Maybe | Operation took too long |

### 7.2 Fallback Chains

**Pattern**: Try operations in order until one succeeds.

```python
def fetch_with_fallback():
    try:
        return primary_api()
    except Exception:
        return fallback_api()
```

### 7.3 Dead Letter Queue

**Pattern**: After all retries exhausted, send to DLQ for manual review.

**Implementation**: Final catch sends to queue/table for operator investigation.

---

## 8. Observability Patterns

### 8.1 Structured Logging

**Pattern**: Emit logs with workflow/task context.

```python
logger.info("Processing", extra={"workflow_id": wf_id, "task": "transform"})
```

### 8.2 Metrics

**Essential Metrics**:
- Task duration
- Success/failure rate
- Queue depth (if using)
- Retry count distribution

### 8.3 Lineage/Provenance

**Pattern**: Track what data produced what outputs.

**Dagster**: Native asset lineage
**Others**: Custom metadata propagation

---

## Sources

- [Temporal Workflow Documentation](https://docs.temporal.io/workflows)
- [Temporal Retry Policies](https://docs.temporal.io/encyclopedia/retry-policies)
- [The Fallacy of the Graph (Temporal Blog)](https://temporal.io/blog/the-fallacy-of-the-graph-why-your-next-workflow-should-be-code-not-a-diagram)
- [Apache Airflow DAGs](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/dags.html)
- [Airflow Tasks](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/tasks.html)
- [Airflow Event-Driven Scheduling](https://airflow.apache.org/docs/apache-airflow/stable/authoring-and-scheduling/event-scheduling.html)
- [Prefect Documentation](https://docs.prefect.io/)
- [Prefect Workflow Design Patterns](https://www.prefect.io/blog/workflow-design-patterns)
- [Prefect States](https://docs.prefect.io/v3/concepts/states)
- [Prefect Event-Driven Workflows](https://www.prefect.io/blog/building-real-time-data-pipelines-a-guide-to-event-driven-workflows-in-prefect)
- [Dagster Software-Defined Assets](https://dagster.io/blog/software-defined-assets)
- [Dagster Ops and Jobs](https://docs.dagster.io/guides/build/ops)
- [Dagster Schedules and Sensors](https://docs.dagster.io/api/dagster/schedules-sensors)
- [Kestra States](https://kestra.io/docs/workflow-components/states)
- [Flyte State Machine](https://docs.flyte.org/en/latest/user_guide/concepts/main_concepts/state_machine.html)
