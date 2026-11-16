# Window functions, joins and aggregations

**Major feature** · Available since ~2015 · DE Professional exam: S3

## What it is

The daily tools of transformation. Window functions compute over a group of rows without collapsing them. Join strategy (broadcast, sort-merge, shuffle hash) decides most of the runtime. Aggregations shuffle by the grouping keys.

## How it flows

1. **Scan**: Read only needed columns and files.
2. **Shuffle or broadcast**: Small side is broadcast; otherwise both sides shuffle by key.
3. **Join or aggregate**: Per partition.
4. **Window**: Sort within partition, compute ranking or running values.
5. **Result**: AQE may re-plan between stages using real sizes.

```
[Scan] --> [Shuffle or broadcast] --> [Join or aggregate] --> [Window] --> [Result]
```

## When to choose it

**Choose it when**

- `row_number` to deduplicate or pick the latest row.
- `lag` and `lead` for change detection.
- Broadcast when one side fits comfortably in memory.

**Pick something else when**

- A window with no `partitionBy` on a large table: everything moves to one partition.
- Python UDFs where a built-in function exists.

## Senior engineer verdict

> Before tuning anything I check three things in the plan: is the small table being broadcast, is one key skewed, and is the filter being applied before the join. Those explain most slow jobs.

## Examples

### 1. Latest record per key and change detection

File: [`example_1.py`](example_1.py)

```python
from pyspark.sql import functions as F, Window
w = Window.partitionBy("customer_id").orderBy(F.col("updated_at").desc())
latest = df.withColumn("rn", F.row_number().over(w)).where("rn = 1").drop("rn")

w2 = Window.partitionBy("sku").orderBy("price_date")
moves = (prices.withColumn("prev_price", F.lag("price").over(w2))
    .where("prev_price IS NOT NULL AND price <> prev_price"))
```

### 2. Broadcast join and a running total

File: [`example_2.py`](example_2.py)

```python
from pyspark.sql import functions as F, Window
sales = spark.table("main.silver.sales")
stores = spark.table("main.silver.stores")
joined = sales.join(F.broadcast(stores), "store_id")

w = (Window.partitionBy("store_id").orderBy("sale_date")
    .rowsBetween(Window.unboundedPreceding, Window.currentRow))
daily = (joined.groupBy("store_id", "sale_date").agg(F.sum("amount").alias("revenue"))
    .withColumn("running_revenue", F.sum("revenue").over(w)))
```

## Traps and gotchas

- `rank` leaves gaps after ties, `dense_rank` does not, `row_number` is always unique.
- Default window frame with ORDER BY is range from unbounded preceding to current row, which treats ties as one group.
- A left join followed by a filter on the right table's column becomes an inner join.
