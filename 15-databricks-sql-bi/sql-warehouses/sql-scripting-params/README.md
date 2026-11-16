# Parameterized SQL and SQL scripting

Available since ~2025 · Part of [SQL warehouses](../README.md)

## What it is

Named parameter markers (`:name`) keep values out of the SQL text, which prevents injection and enables plan reuse. `IDENTIFIER()` safely parameterizes table and column names. SQL scripting adds variables, IF, loops and exception handlers so procedural logic can run as SQL.

## How it flows

1. **Parameters**: Values bound at execution.
2. **IDENTIFIER**: Turns a string parameter into a validated object name.
3. **Script block**: BEGIN ... END with DECLARE, IF, FOR, WHILE.
4. **Run**: From the SQL editor, a notebook, a job SQL task or the API.

```
[Parameters] --> [IDENTIFIER] --> [Script block] --> [Run]
```

## When to choose it

**Choose it when**

- Any SQL built from user input.
- SQL-first teams that need loops or conditional logic without Python.

**Pick something else when**

- String formatting values into SQL with f-strings.

## Senior engineer verdict

> I treat an f-string with a user value inside `spark.sql` as a security bug in review. Named parameters plus IDENTIFIER cover every case I have needed.

## Examples

### 1. Safe parameters from Python

File: [`example_1.py`](example_1.py)

```python
tbl = "main.gold.fact_orders"
df = spark.sql(
    "SELECT region, SUM(amount) AS revenue FROM IDENTIFIER(:tbl) WHERE order_date >= :d GROUP BY region",
    args={"tbl": tbl, "d": "2026-11-01"})
```

### 2. Pass DataFrames and values into SQL safely

File: [`example_2.py`](example_2.py)

```python
recent = spark.table("main.silver.orders").where("order_date >= '2026-11-01'")
top = spark.sql("""
SELECT customer_id, SUM(amount) AS spend
FROM {orders} WHERE amount > {min_amount}
GROUP BY customer_id ORDER BY spend DESC LIMIT 10""", orders=recent, min_amount=50)
top.show()
```

### 3. SQL script with a loop and a condition

File: [`example_3.sql`](example_3.sql)

```sql
BEGIN
  DECLARE total BIGINT DEFAULT 0;
  FOR t AS SELECT table_name FROM main.information_schema.tables WHERE table_schema = 'bronze' DO
    EXECUTE IMMEDIATE 'OPTIMIZE main.bronze.' || t.table_name;
    SET total = total + 1;
  END FOR;
  IF total = 0 THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'No bronze tables found';
  END IF;
  SELECT total AS optimized_tables;
END;
```

## Traps and gotchas

- Parameter markers stand for values, not identifiers; use IDENTIFIER for names.
- Positional (`?`) and named markers cannot be mixed in one statement.
