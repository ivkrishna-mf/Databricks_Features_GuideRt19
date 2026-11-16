# COPY INTO

Available since ~2020 · DE Professional exam: S2

## What it is

A SQL command that loads files from a path into a Delta table and remembers which files it already loaded, so rerunning it is safe.

## How it flows

1. **Files in a path**: Thousands, not millions.
2. **COPY INTO runs**: On a schedule from a SQL warehouse or job.
3. **Skip loaded files**: File load history lives in the table metadata.
4. **Append**: New rows land in the target table.

```
[Files in a path] --> [COPY INTO runs] --> [Skip loaded files] --> [Append]
```

## When to choose it

**Choose it when**

- SQL-first teams loading modest file counts on a schedule.
- Ad hoc or one-off loads that should be re-runnable.

**Pick something else when**

- Millions of files, complex nested data or schema drift: Auto Loader handles these better.

## Senior engineer verdict

> COPY INTO is fine where it already works. For anything new I reach for a streaming table with `read_files` or Auto Loader, because it scales further and I do not have to migrate later.

## Examples

### 1. Idempotent load with schema evolution

File: [`example_1.py`](example_1.py)

```python
spark.sql("""
COPY INTO main.bronze.invoices
FROM '/Volumes/main/landing/invoices/'
FILEFORMAT = CSV
FORMAT_OPTIONS ('header' = 'true', 'inferSchema' = 'true')
COPY_OPTIONS ('mergeSchema' = 'true')""")
```

### 2. Force a reload of all files

File: [`example_2.py`](example_2.py)

```python
spark.sql("""
COPY INTO main.bronze.invoices
FROM '/Volumes/main/landing/invoices/'
FILEFORMAT = CSV
FORMAT_OPTIONS ('header' = 'true')
COPY_OPTIONS ('force' = 'true')""")      # ignores load history: duplicates possible
```

## Traps and gotchas

- `force` = true disables idempotency.
- COPY INTO is batch only; there is no trigger or checkpoint.
