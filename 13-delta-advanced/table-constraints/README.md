# Constraints, generated, identity and default columns

**Major feature** · Available since ~2020

## What it is

Delta enforces NOT NULL and CHECK constraints on every write. Generated columns compute their value from other columns. Identity columns assign unique increasing numbers, useful as surrogate keys. Default values fill columns that a write leaves out. Primary and foreign keys are informational: documented and used by tools, not enforced.

## How it flows

1. **Write arrives**: INSERT, MERGE, append or streaming batch.
2. **Defaults and generated values**: Filled in by Delta.
3. **Identity**: A new unique value per inserted row.
4. **Constraint check**: Any violating row fails the whole transaction.
5. **Commit**: Only valid data becomes visible.

```
[Write arrives] --> [Defaults and generated values] --> [Identity] --> [Constraint check] --> [Commit]
```

## When to choose it

**Choose it when**

- Rules that must never be broken, enforced at the storage layer regardless of which tool writes.
- Surrogate keys for dimensions.

**Pick something else when**

- Using CHECK constraints for soft quality rules: one bad row fails the whole write. Use pipeline expectations for those.

## Senior engineer verdict

> Constraints are my last line of defense, not my quality strategy. I put a handful of hard invariants on gold tables (non-null keys, non-negative amounts) and declare primary and foreign keys so BI tools and the optimizer understand the model. Identity columns are unique but not gap-free, so never use them as a business sequence.

## Examples

### 1. Create a dimension with identity, generated and default columns

File: [`example_1.py`](example_1.py)

```python
spark.sql("""
CREATE TABLE main.gold.dim_customer (
  customer_sk  BIGINT GENERATED ALWAYS AS IDENTITY,
  customer_id  STRING NOT NULL,
  signup_ts    TIMESTAMP,
  signup_date  DATE GENERATED ALWAYS AS (CAST(signup_ts AS DATE)),
  status       STRING DEFAULT 'active',
  CONSTRAINT dim_customer_pk PRIMARY KEY (customer_sk)
) TBLPROPERTIES ('delta.feature.allowColumnDefaults' = 'supported')""")
```

### 2. Add a CHECK constraint and a foreign key

File: [`example_2.py`](example_2.py)

```python
spark.sql("ALTER TABLE main.gold.fact_orders ADD CONSTRAINT positive_amount CHECK (amount >= 0)")
spark.sql("""
ALTER TABLE main.gold.fact_orders ADD CONSTRAINT fk_customer
FOREIGN KEY (customer_sk) REFERENCES main.gold.dim_customer""")
spark.sql("SHOW TBLPROPERTIES main.gold.fact_orders").where("key LIKE 'delta.constraints%'").show(truncate=False)
```

## Traps and gotchas

- Adding a CHECK constraint fails if existing rows violate it.
- Primary and foreign keys in Unity Catalog are not enforced.
- With GENERATED ALWAYS AS IDENTITY you cannot insert your own values.

## Sub-features

- [Renames, drops and type widening](column-mapping-type-widening/README.md)
