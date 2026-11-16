# SDP or Structured Streaming

**Major feature** · Available since ~2025 · DE Professional exam: S1

## What it is

Both run on the same engine. The question is who owns the operational work. SDP is declarative: you state the tables and the framework runs them. Structured Streaming is imperative: you own triggers, checkpoints, sinks, retries and deployment.

## How it flows

1. **Requirement**: Read the constraint in the scenario first.
2. **Standard medallion, CDC, quality rules?**: SDP.
3. **Custom state, per-batch side effects, unusual sink?**: Structured Streaming.
4. **Mixed**: SDP for the tables, a job task with Structured Streaming for the special flow.

```
[Requirement] --> [Standard medallion, CDC, quality rules?] --> [Custom state, per-batch side effects, unusual sink?] --> [Mixed]
```

## Decision table

| Constraint | SDP | Structured Streaming |
|---|---|---|
| Checkpoints and restarts | Managed | You manage paths and recovery |
| CDC and SCD2 | AUTO CDC | MERGE in `foreachBatch`, ordering is your problem |
| Data quality | Expectations with metrics | Your own filters and logging |
| Arbitrary stateful logic (`transformWithState`) | Limited | Full control |
| Write to several sinks per batch, call APIs | Not the model | `foreachBatch` |
| Lineage, monitoring | Event log and UI built in | StreamingQueryListener, your dashboards |
| Team skill | SQL or simple Python | Engineers comfortable with streaming internals |

## Senior engineer verdict

> I choose SDP by default and write down the reason whenever I do not. The reasons that hold up: custom state machines, per-batch transactional writes to several targets, or a need to control the exact trigger and cluster. 'We already know Structured Streaming' is not one of them.

## Examples

### 1. Deduplicated silver table in SDP

File: [`example_1.py`](example_1.py)

```python
from pyspark import pipelines as dp

@dp.table(name="silver_payments")
def silver_payments():
    return (spark.readStream.table("bronze_payments")
        .withWatermark("paid_at", "2 hours")
        .dropDuplicatesWithinWatermark(["payment_id"]))
```

### 2. The same in Structured Streaming: you own the plumbing

File: [`example_2.py`](example_2.py)

```python
q = (spark.readStream.table("main.bronze.payments")
    .withWatermark("paid_at", "2 hours")
    .dropDuplicatesWithinWatermark(["payment_id"])
    .writeStream
    .option("checkpointLocation", "/Volumes/main/ops/chk/silver_payments")
    .trigger(processingTime="1 minute")
    .toTable("main.silver.payments"))
```

## Traps and gotchas

- 'Minimal operational overhead' or 'automatic dependency management' in a question points to SDP.
- 'Custom logic applied to each micro-batch' points to `foreachBatch` in Structured Streaming.
