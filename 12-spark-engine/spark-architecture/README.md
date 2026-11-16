# How Spark executes your code

**Major feature** · Available since ~2013

## What it is

Every Databricks workload, whether SQL, Python, a pipeline or ML training on tables, ends up as Spark (or Photon) work. The driver turns your DataFrame or SQL code into a plan. When an action runs, the plan becomes a job, the job splits into stages at each shuffle, and each stage runs one task per partition on the executors.

Transformations are lazy: `filter`, `select` and `join` only build the plan. Actions such as `count`, `write` and `collect` execute it. Catalyst optimizes the logical plan (pushes filters down, prunes columns). Adaptive Query Execution (AQE) re-plans at runtime using real sizes. Photon runs the physical operators in vectorized native code.

## How it flows

1. **Your code**: DataFrame, SQL or pipeline definition.
2. **Logical plan**: Catalyst resolves names and applies rules such as predicate pushdown.
3. **Physical plan**: Join strategies and exchanges (shuffles) are chosen.
4. **Job, stages, tasks**: An action creates a job; each shuffle boundary starts a new stage; one task per partition.
5. **AQE**: After each stage, real statistics can coalesce partitions, switch to a broadcast join or split skew.

```
[Your code] --> [Logical plan] --> [Physical plan] --> [Job, stages, tasks] --> [AQE]
```

## When to choose it

**Choose it when**

- Use this mental model whenever you read a Spark UI, a query profile or an explain plan.

**Pick something else when**

- Calling actions in a loop (`count` for every step). Each one runs the whole plan again.

## Narrow and wide transformations

| Kind | Examples | Shuffle? | Cost |
|---|---|---|---|
| Narrow | `select`, `filter`, `withColumn`, `union`, map-side work | No | Cheap, pipelined in one stage |
| Wide | `groupBy`, `join` (non-broadcast), `distinct`, `orderBy`, `repartition`, window with partitionBy | Yes | Network, disk, a new stage |

## Senior engineer verdict

> Most performance work is reducing shuffles and the bytes in each one. Read less (filters and clustering), shuffle less (broadcast small tables, aggregate before joining), and let AQE handle partition counts. I almost never set `spark.sql.shuffle.partitions` by hand any more.

## Examples

### 1. Lazy plan, one action, read the plan

File: [`example_1.py`](example_1.py)

```python
from pyspark.sql import functions as F
orders = spark.table("main.silver.orders")             # nothing runs yet
big = (orders.where("order_date >= '2026-10-01'")       # narrow
    .groupBy("customer_id")                              # wide: shuffle
    .agg(F.sum("amount").alias("spend")))
big.explain("formatted")       # Exchange = shuffle; PushedFilters = file skipping
big.write.mode("overwrite").saveAsTable("main.gold.spend_oct")   # the action
```

### 2. repartition, coalesce and AQE

File: [`example_2.py`](example_2.py)

```python
spark.conf.set("spark.sql.adaptive.enabled", "true")                 # default on Databricks
spark.conf.set("spark.sql.adaptive.coalescePartitions.enabled", "true")

wide = df.repartition(200, "customer_id")   # full shuffle, even distribution by key
narrow = df.coalesce(8)                     # merges partitions, no shuffle, can be uneven
print(df.rdd.getNumPartitions(), wide.rdd.getNumPartitions(), narrow.rdd.getNumPartitions())
```

## Traps and gotchas

- `coalesce` can only reduce partitions and avoids a shuffle; `repartition` can go up or down and always shuffles.
- `collect` and `toPandas` pull the whole result to the driver.
- A cached DataFrame is materialized only when an action runs.

## Sub-features

- [Spark Connect and Databricks Connect](databricks-connect/README.md)
- [pandas API on Spark and pandas functions](pandas-on-spark/README.md)
