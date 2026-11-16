# What is new in Runtime 19

Available since ~2026 · DBR 19

## What it is

Runtime 19 is built on Apache Spark 4.x with Java 21, Scala 2.13 and Python 3.12. The exam guide does not name a runtime version, so treat this page as context for your project and for spotting behavior changes, not as a list of exam objectives.

## How it flows

1. **Inventory**: List jobs and the packages and Spark configs they rely on.
2. **Test on 19**: Run the test suite on a Runtime 19 job cluster or the matching serverless environment.
3. **Fix dependencies**: Declare removed packages; drop blocked configs and the JDK 17 pin.
4. **Compare output**: Check UDF results and late-data counts against the old runtime.
5. **Roll out**: Switch targets in the bundle, dev first, then prod.

```
[Inventory] --> [Test on 19] --> [Fix dependencies] --> [Compare output] --> [Roll out]
```

## Changes a data engineer will notice

| Area | Change | What to do |
|---|---|---|
| Delta | Automatic change data feed: row-level changes computed at query time from row tracking | You no longer need `delta.enableChangeDataFeed` on every table; row tracking must be on |
| Delta | `INSERT INTO ... REPLACE ON / USING` and `withSchemaEvolution()` on the DataFrame writer | Simpler upsert-style and evolving writes |
| Python | Arrow-optimized Python UDFs are on by default | Faster UDFs; type coercion can differ, config exists to revert |
| Python | About 90 packages removed from the base image (plotly, seaborn, pyodbc, psycopg2 and others) | Declare them explicitly in the environment or cluster libraries |
| Java | JDK 17 fallback removed | Unset `JNAME` if a cluster pins zulu17 |
| Streaming | Kinesis polling in real-time mode GA; watermark boundary records retained | Re-check tests that assert on exact late-data counts |
| SQL | `SET PATH` and `CURRENT_PATH()`; new functions such as `trim_array`, `variant_strip_nulls` | Shorter function references across schemas |
| Governance | Atomic `CREATE OR REPLACE VIEW` keeps grants and tags; policy details hidden in plans; stricter Spark configs in standard access mode | Remove blocked configs such as `spark.jars` from shared clusters |
| Shuffle | Auto-optimized shuffle is the default when no fixed partition count is set | Stop hard-coding `spark.sql.shuffle.partitions` unless you measured |

## Senior engineer verdict

> The upgrade risk is not Spark, it is the removed Python packages and the Arrow UDF default. Run your test suite on a Runtime 19 job cluster before switching production, and pin dependencies in the bundle rather than relying on what the image happens to include.

## Examples

### 1. Read row-level changes without enabling CDF per table

File: [`example_1.py`](example_1.py)

```python
# Runtime 19+: row tracking on, changes are computed at query time
spark.sql("ALTER TABLE main.silver.orders SET TBLPROPERTIES ('delta.enableRowTracking' = 'true')")

changes = (spark.read
    .option("readChangeFeed", "true")
    .option("startingVersion", 120)
    .table("main.silver.orders"))
changes.groupBy("_change_type").count().show()
```

### 2. INSERT REPLACE for idempotent reprocessing

File: [`example_2.py`](example_2.py)

```python
spark.table("main.staging.events_fix").createOrReplaceTempView("fix")
spark.sql("INSERT INTO main.silver.events REPLACE USING (event_date) SELECT * FROM fix")
spark.sql("DESCRIBE HISTORY main.silver.events").select("version", "operation").show(3)
```

### 3. Declare packages that Runtime 19 no longer ships

File: [`example_3.yml`](example_3.yml)

```yaml
# resources/job.yml (serverless environment for a job task)
environments:
  - environment_key: default
    spec:
      environment_version: "4"     # use the version your workspace offers
      dependencies:
        - plotly==5.24.1
        - psycopg2-binary==2.9.10
        - ./dist/*.whl
```

## Traps and gotchas

- A question that says 'the notebook worked on Runtime 18 and fails with ModuleNotFoundError on 19' is about removed packages, not about a broken cluster.
- Automatic change data feed needs row tracking. Without it you still need the table property.
