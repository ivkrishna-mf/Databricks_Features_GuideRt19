# Tags, comments and lineage

Available since ~2023 · DE Professional exam: S7

## What it is

Comments describe objects in plain language. Tags are key and value pairs for classification and search; governed tags have controlled values and can drive ABAC. Lineage is captured automatically for queries that run through Unity Catalog, down to column level.

## How it flows

1. **Create object**: Table lands in a schema.
2. **Describe**: Comment on table and columns.
3. **Classify**: Tags such as domain, pii, retention.
4. **Discover**: Search by tag or text in Catalog Explorer.
5. **Trace**: Lineage shows upstream and downstream tables, jobs and dashboards.

```
[Create object] --> [Describe] --> [Classify] --> [Discover] --> [Trace]
```

## When to choose it

**Choose it when**

- Every published table. Good metadata also improves AI assistants and Genie answers.

**Pick something else when**

- Putting secrets or personal data in tags or comments.

## Senior engineer verdict

> I set comments and tags in the pipeline code so they are versioned and never drift. Before changing a column I check column lineage to see who consumes it.

## Examples

### 1. Comments and tags

File: [`example_1.py`](example_1.py)

```python
spark.sql("COMMENT ON TABLE main.gold.daily_revenue IS 'Net revenue per day and store, refreshed hourly'")
spark.sql("ALTER TABLE main.gold.daily_revenue ALTER COLUMN revenue COMMENT 'Net of tax, in EUR'")
spark.sql("ALTER TABLE main.gold.daily_revenue SET TAGS ('domain' = 'finance', 'tier' = 'gold')")
spark.sql("SELECT * FROM main.information_schema.table_tags WHERE tag_name = 'domain'").show()
```

### 2. Who reads this table? Lineage from system tables

File: [`example_2.py`](example_2.py)

```python
spark.sql("""
SELECT DISTINCT target_table_full_name, entity_type, created_by
FROM system.access.table_lineage
WHERE source_table_full_name = 'main.silver.orders'
  AND event_time >= current_date() - INTERVAL 30 DAYS""").show(truncate=False)
```

## Traps and gotchas

- Tags are not access control by themselves; ABAC policies make them enforce something.
- Applying a tag needs APPLY TAG on the object (and ASSIGN on a governed tag).
