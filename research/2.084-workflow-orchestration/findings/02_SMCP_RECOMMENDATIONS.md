# SMCP/Judith Workflow Orchestration Recommendations

Practical recommendations for implementing a lightweight workflow orchestrator
for MCP (Model Context Protocol) based on patterns extracted from Temporal,
Airflow, Prefect, and Dagster.

**Target Scale**: Single node to small cluster, NOT enterprise distributed systems.

---

## Executive Summary

| Category | Recommendation |
|----------|----------------|
| DAG Definition | ADOPT code-first with decorators |
| State Machine | SIMPLIFY to 4-5 states |
| Triggers | ADOPT manual + cron, SKIP event-driven |
| Retry/Backoff | ADOPT simple exponential backoff |
| Distributed | SKIP worker pools, K8s operators |
| Persistence | ADOPT file-based state, SKIP event sourcing |

---

## 1. DAG Definition: ADOPT Code-First

### Recommendation: Python decorators with implicit dependencies

```python
@judith.workflow
def mcp_pipeline(context):
    # MCP tool calls as tasks
    files = context.run(list_files, path="/data")
    for f in files:
        context.run(process_file, file=f)
    return context.run(summarize)

@judith.task
def list_files(path: str) -> list[str]:
    # Wraps MCP tool call
    ...
```

### Why Code-First for SMCP

1. **MCP tools are already Python callables** - decorators are natural
2. **Dynamic workflows matter** - file lists, conditional branches are common
3. **No DAG visualization needed** - SMCP is developer-facing, not BI-facing
4. **Testing is standard pytest** - no special test harness required

### Skip

- YAML/declarative DAG definitions (Kestra, Airflow 1.x style)
- Visual DAG builders
- Asset-centric model (Dagster) - overkill for MCP tool orchestration

### Simplification from Prefect/Temporal

- No need for deployment specs (single node)
- No infrastructure abstraction (work pools, executors)
- No UI for DAG editing

---

## 2. Task State Machine: SIMPLIFY

### Recommendation: 5 Essential States

```
PENDING -> RUNNING -> COMPLETED
              |
              v
           FAILED <-> RETRYING
```

| State | When | Terminal |
|-------|------|----------|
| PENDING | Task created, waiting to start | No |
| RUNNING | Currently executing | No |
| RETRYING | Failed, waiting for retry attempt | No |
| COMPLETED | Success | Yes |
| FAILED | All retries exhausted | Yes |

### Skip These States

| State | Why Skip |
|-------|----------|
| SCHEDULED | Use PENDING + trigger time field |
| QUEUED | No worker pool, no queuing needed |
| AWAITING_RETRY | Merge into RETRYING with delay field |
| PAUSED | Not needed for MCP automation |
| CANCELLED | Add later if needed |
| CRASHED | Treat as FAILED with error type |

### Implementation

```python
class TaskState(Enum):
    PENDING = "pending"
    RUNNING = "running"
    RETRYING = "retrying"
    COMPLETED = "completed"
    FAILED = "failed"

@dataclass
class TaskRun:
    state: TaskState
    attempt: int = 0
    error: Optional[str] = None
    result: Optional[Any] = None
    next_retry_at: Optional[datetime] = None
```

---

## 3. Retry Strategy: ADOPT Simple Exponential

### Recommendation: Temporal-inspired defaults

```python
@dataclass
class RetryPolicy:
    max_attempts: int = 3
    initial_interval: float = 1.0  # seconds
    backoff_coefficient: float = 2.0
    max_interval: float = 60.0  # seconds
    non_retryable_errors: list[type] = field(default_factory=list)
```

### Calculation

```python
def get_retry_delay(attempt: int, policy: RetryPolicy) -> float:
    delay = policy.initial_interval * (policy.backoff_coefficient ** attempt)
    return min(delay, policy.max_interval)
```

### Default Non-Retryable Errors

```python
NON_RETRYABLE = [
    ValueError,           # Bad input
    TypeError,            # Programming error
    PermissionError,      # Auth won't change with retry
    FileNotFoundError,    # Resource doesn't exist
]
```

### Skip

- Jitter (random delay variance) - adds complexity, marginal benefit
- Per-error-type retry policies - keep it simple
- Retry budgets/circuit breakers - enterprise pattern

---

## 4. Triggers: ADOPT Manual + Cron

### Recommendation: Start simple, add event-driven later

**Phase 1 (MVP)**:
- Manual: `judith.run(workflow, inputs)`
- Cron: `judith.schedule(workflow, cron="0 * * * *")`

**Phase 2 (If Needed)**:
- Webhook trigger endpoint
- File watcher (simple polling, not sensors)

### Implementation

```python
# Manual trigger
result = judith.run(my_workflow, {"input": "value"})

# Scheduled
judith.schedule(
    my_workflow,
    cron="0 9 * * *",  # Daily at 9 AM
    inputs={"mode": "daily"}
)

# Or simple interval
judith.schedule(my_workflow, every=timedelta(hours=1))
```

### Skip

- Complex sensor system (Airflow)
- Asset materialization triggers (Dagster)
- Event bus / automation rules (Prefect Cloud)
- Message queue integration (Kafka, SQS)
- Signal-with-start patterns (Temporal)

These are enterprise patterns for multi-system coordination. SMCP targets
single-node MCP tool orchestration.

---

## 5. Persistence: ADOPT File-Based

### Recommendation: JSON/SQLite state, not event sourcing

```python
# Simple state file per workflow run
{
    "workflow_id": "wf_abc123",
    "status": "running",
    "started_at": "2025-01-08T10:00:00Z",
    "tasks": [
        {
            "task_id": "t_001",
            "name": "list_files",
            "state": "completed",
            "result": ["/data/a.txt", "/data/b.txt"],
            "duration_ms": 150
        },
        {
            "task_id": "t_002",
            "name": "process_file",
            "state": "running",
            "attempt": 1
        }
    ]
}
```

### Why Not Event Sourcing (Temporal-style)

1. **Complexity**: Replay logic is hard to get right
2. **Overkill**: SMCP workflows are short-lived, not month-long sagas
3. **Dependencies**: Requires event store infrastructure

### Skip

- Workflow replay from events
- Durable timers (just use cron + state check)
- Event history UI

### Simple Recovery Strategy

```python
def recover_workflow(workflow_id: str):
    state = load_state(workflow_id)
    # Find last completed task
    # Resume from next pending task
    # Re-run failed tasks with retry count
```

---

## 6. Distributed Execution: SKIP

### What to Skip Entirely

| Feature | Why Skip |
|---------|----------|
| Worker pools | Single process is fine for MCP |
| Task queues | No concurrent workers |
| Kubernetes operators | Wrong scale |
| Container-per-task | Overhead for MCP tools |
| Celery/Redis brokers | Infrastructure complexity |
| Multi-region failover | Enterprise pattern |

### Simple Concurrency Model

```python
# Use asyncio for concurrent MCP tool calls
async def run_parallel_tasks(tasks):
    return await asyncio.gather(*[run_task(t) for t in tasks])
```

### If You Need More Later

- Add subprocess workers (not containers)
- Use `multiprocessing` for CPU-bound tasks
- Consider Dask for data-heavy workflows

---

## 7. Workflow Composition: SIMPLIFY

### Recommendation: Functions calling functions

```python
@judith.workflow
def main_workflow(ctx):
    # Just call other workflows as functions
    intermediate = sub_workflow_a(ctx)
    return sub_workflow_b(ctx, intermediate)

@judith.workflow
def sub_workflow_a(ctx):
    return ctx.run(task_a)
```

### Skip

- Deployment-based composition (Prefect orchestrator pattern)
- Child workflow lifecycle management (Temporal)
- Saga compensation patterns (unless doing financial txns)

### Error Propagation

```python
# Simple: let errors bubble up
@judith.workflow
def composed(ctx):
    try:
        result = risky_sub_workflow(ctx)
    except WorkflowError as e:
        ctx.run(send_alert, message=str(e))
        raise
```

---

## 8. Observability: ADOPT Minimal

### Recommendation: Structured logs + basic metrics

```python
# Logging with context
logger.info("task_completed", extra={
    "workflow_id": ctx.workflow_id,
    "task": "process_file",
    "duration_ms": 150,
    "attempt": 1
})
```

### Essential Metrics (if any)

- Workflow run count (success/failure)
- Task duration histogram
- Retry count per workflow

### Skip

- OpenTelemetry integration (add later if needed)
- Distributed tracing
- Custom metrics backends
- Lineage tracking (Dagster-style)

---

## 9. API Design Recommendations

### Workflow Definition

```python
from judith import workflow, task, RetryPolicy

@workflow
def my_pipeline(ctx):
    """Top-level workflow."""
    data = ctx.run(fetch_data)
    return ctx.run(process, data)

@task(retry=RetryPolicy(max_attempts=3))
def fetch_data():
    """Individual task with retry."""
    return mcp_tool_call("read_file", path="/data")
```

### Running Workflows

```python
from judith import Judith

j = Judith()

# Synchronous
result = j.run(my_pipeline, inputs={"key": "value"})

# Async
result = await j.run_async(my_pipeline, inputs={})

# Scheduled
j.schedule(my_pipeline, cron="0 * * * *")

# Background (returns immediately)
run_id = j.submit(my_pipeline, inputs={})
status = j.get_status(run_id)
```

### Configuration

```python
judith = Judith(
    state_dir="~/.judith/state",
    log_level="INFO",
    default_retry=RetryPolicy(max_attempts=3),
    max_concurrent_tasks=10,
)
```

---

## 10. Migration Path

### Phase 1: MVP (Week 1-2)

- Task/workflow decorators
- 5-state machine
- Manual triggers only
- JSON file state
- Basic retry with backoff

### Phase 2: Scheduling (Week 3-4)

- Cron scheduler
- Simple interval scheduling
- Workflow history/log viewer

### Phase 3: Polish (Week 5-6)

- Better error messages
- Timeout support
- CLI tools
- Optional: webhook triggers

### Future (If Needed)

- Async task execution
- Simple job queue
- Web UI for status

---

## Summary Table

| Pattern | ADOPT | SIMPLIFY | SKIP |
|---------|-------|----------|------|
| Code-first DAG | X | | |
| YAML DAG | | | X |
| Asset-centric | | | X |
| 5-state machine | | X | |
| Full state machine | | | X |
| Exponential backoff | X | | |
| Circuit breakers | | | X |
| Manual trigger | X | | |
| Cron trigger | X | | |
| Event sensors | | | X |
| Message queues | | | X |
| File-based state | X | | |
| Event sourcing | | | X |
| Worker pools | | | X |
| K8s operators | | | X |
| Subworkflows | | X | |
| Saga pattern | | | X |
| Structured logs | X | | |
| Distributed tracing | | | X |

---

## Sources

- [Temporal Documentation](https://docs.temporal.io/)
- [Prefect Documentation](https://docs.prefect.io/)
- [Apache Airflow Documentation](https://airflow.apache.org/docs/)
- [Dagster Documentation](https://docs.dagster.io/)
- [Dagu - Lightweight Alternative](https://dagu.io/)
- [State of Workflow Orchestration 2025](https://www.pracdata.io/p/state-of-workflow-orchestration-ecosystem-2025)
- [Workflow Orchestration Platforms Comparison 2025](https://procycons.com/en/blogs/workflow-orchestration-platforms-comparison-2025/)
