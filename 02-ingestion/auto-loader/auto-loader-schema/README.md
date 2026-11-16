# Schema inference, evolution and rescued data

Available since ~2021 · DE Professional exam: S1, S2 · Part of [Auto Loader](../README.md)

## What it is

Auto Loader samples files to infer a schema and stores it at the schema location. When new columns appear, `cloudFiles.schemaEvolutionMode` decides what happens. Data that does not fit the schema goes to the `_rescued_data` column instead of being lost.

## How it flows

1. **New column appears**: A file contains `discount_code`.
2. **Mode check**: addNewColumns: the stream stops with an unknown field error after updating the stored schema.
3. **Restart**: The job retry starts the stream with the new schema.
4. **Write**: With `mergeSchema` on the sink, the Delta table gains the column.

```
[New column appears] --> [Mode check] --> [Restart] --> [Write]
```

## Evolution modes

| Mode | Behavior on a new column | Choose when |
|---|---|---|
| `addNewColumns` (default with no schema given) | Stream fails once, schema is updated, restart continues | You want new fields automatically; set job retries |
| `rescue` | Schema never changes; new fields go to `_rescued_data` | Stable contract, but nothing may be lost |
| `failOnNewColumns` | Stream fails until you update the schema or hints | Strict contracts where a human must approve changes |
| `none` (default when you supply a schema) | New columns are ignored | You only want the declared columns |

## Senior engineer verdict

> For bronze I run addNewColumns with job retries, plus schema hints for the columns whose types I care about. When the payload is truly unpredictable I stop fighting it and load the whole record into one VARIANT column.

## Examples

### 1. Rescue mode with type hints

File: [`example_1.py`](example_1.py)

```python
df = (spark.readStream.format("cloudFiles")
    .option("cloudFiles.format", "json")
    .option("cloudFiles.schemaLocation", "/Volumes/main/ops/chk/pay/_schema")
    .option("cloudFiles.schemaEvolutionMode", "rescue")
    .option("cloudFiles.schemaHints", "amount DECIMAL(18,2), paid_at TIMESTAMP")
    .load("/Volumes/main/landing/payments/"))
bad = df.where("_rescued_data IS NOT NULL")     # route these to a quarantine table
```

### 2. Whole record as VARIANT

File: [`example_2.py`](example_2.py)

```python
df = (spark.readStream.format("cloudFiles")
    .option("cloudFiles.format", "json")
    .option("singleVariantColumn", "payload")
    .option("cloudFiles.schemaLocation", "/Volumes/main/ops/chk/events/_schema")
    .load("/Volumes/main/landing/events/"))
typed = df.selectExpr("payload:user.id::string AS user_id", "payload:ts::timestamp AS ts")
```

## Traps and gotchas

- With addNewColumns the first failure is expected behavior. The fix is a retry policy, not a different mode.
- Type mismatches go to rescued data; they do not evolve the column type.
