# AUTO CDC FROM SNAPSHOT

Available since ~2024 · DE Professional exam: S1, S2 · Part of [Lakeflow Spark Declarative Pipelines (SDP)](../README.md)

## What it is

When a source gives only full snapshots, this API compares each snapshot with the previous state of the target and works out the inserts, updates and deletes itself. Python only.

## How it flows

1. **Snapshot N**: A full copy of the source table or a dated extract.
2. **Diff**: Compared with the current target by key.
3. **Derived changes**: Inserted, changed and missing keys.
4. **Target**: Applied as SCD type 1 or type 2.

```
[Snapshot N] --> [Diff] --> [Derived changes] --> [Target]
```

## When to choose it

**Choose it when**

- Nightly full extracts from a system with no change log.
- Backfilling history from a folder of dated snapshots.

**Pick something else when**

- A CDC feed exists: AUTO CDC is cheaper and keeps intra-day changes.

## Senior engineer verdict

> Snapshots lose every change that happened between two extracts, so SCD2 from snapshots has the granularity of the extract schedule. I say that out loud to stakeholders before they assume it is a full audit trail.

## Examples

### 1. Periodic snapshot: read the latest table state each update

File: [`example_1.py`](example_1.py)

```python
from pyspark import pipelines as dp

@dp.temporary_view
def products_snapshot():
    return spark.read.table("main.staging.products_full")

dp.create_streaming_table("dim_product")
dp.create_auto_cdc_from_snapshot_flow(
    target="dim_product",
    source="products_snapshot",
    keys=["sku"],
    stored_as_scd_type=2)
```

### 2. Historical snapshots: process dated folders in order

File: [`example_2.py`](example_2.py)

```python
from pyspark import pipelines as dp

def next_snapshot(latest_version):
    days = sorted(int(f.name.strip("/")) for f in dbutils.fs.ls("/Volumes/main/landing/products/"))
    todo = [d for d in days if latest_version is None or d > latest_version]
    if not todo:
        return None                       # nothing new: stop
    d = todo[0]
    return (spark.read.parquet("/Volumes/main/landing/products/" + str(d)), d)

dp.create_streaming_table("dim_product_hist")
dp.create_auto_cdc_from_snapshot_flow(
    target="dim_product_hist", source=next_snapshot,
    keys=["sku"], stored_as_scd_type=2)
```

## Traps and gotchas

- One target cannot be fed by both AUTO CDC and AUTO CDC FROM SNAPSHOT.
- No SQL syntax for the snapshot variant.
