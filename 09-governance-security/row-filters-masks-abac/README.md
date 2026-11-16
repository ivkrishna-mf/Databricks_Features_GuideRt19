# Row filters, column masks and ABAC

**Major feature** · Available since ~2023 · DE Professional exam: S6

## What it is

A row filter is a SQL function that returns true for rows a user may see. A column mask is a function that returns the value a user may see. You can attach them table by table, or define an ABAC policy once on a catalog or schema that applies to every column carrying a governed tag.

## How it flows

1. **Tag data**: Governed tag such as pii = email on columns.
2. **Write a function**: Returns the masked value or a boolean, based on group membership.
3. **Create a policy**: On a catalog or schema: which principals, which tag.
4. **New table appears**: Tagged columns are covered automatically.
5. **Query**: Filters and masks are applied at run time for every access path.

```
[Tag data] --> [Write a function] --> [Create a policy] --> [New table appears] --> [Query]
```

## When to choose it

**Choose it when**

- Different audiences need different slices of the same table.
- PII must be masked consistently everywhere.

**Pick something else when**

- Copying tables per audience.
- Heavy logic in the function: it runs for every query.

## Options

| Approach | Scope | Choose when |
|---|---|---|
| Dynamic view | One view | Legacy pattern, or sharing a restricted projection |
| Row filter / column mask on a table | One table | A few sensitive tables |
| ABAC policy with governed tags | Catalog or schema | Many tables; rules must follow the data classification |

## Senior engineer verdict

> Table-level masks do not scale past a handful of tables, because every new table needs someone to remember. With ABAC the rule is attached to the classification, so tagging a column is all a producer has to do. I keep the functions simple, deterministic SQL in a governance schema.

## Examples

### 1. Row filter and column mask on one table

File: [`example_1.py`](example_1.py)

```python
spark.sql("""
CREATE OR REPLACE FUNCTION main.gov.region_filter(region STRING) RETURNS BOOLEAN
RETURN is_account_group_member('global_admins') OR region = 'EMEA'""")
spark.sql("ALTER TABLE main.gold.sales SET ROW FILTER main.gov.region_filter ON (region)")

spark.sql("""
CREATE OR REPLACE FUNCTION main.gov.mask_email(email STRING) RETURNS STRING
RETURN CASE WHEN is_account_group_member('pii_readers') THEN email
            ELSE concat('***@', split_part(email, '@', 2)) END""")
spark.sql("ALTER TABLE main.gold.customers ALTER COLUMN email SET MASK main.gov.mask_email")
```

### 2. ABAC: one policy for every column tagged as email

File: [`example_2.py`](example_2.py)

```python
spark.sql("ALTER TABLE main.gold.customers ALTER COLUMN email SET TAGS ('pii' = 'email')")
spark.sql("""
CREATE OR REPLACE FUNCTION main.gov.redact(v STRING) RETURNS STRING RETURN '[redacted]'""")
spark.sql("""
CREATE POLICY mask_pii_email ON CATALOG main
COMMENT 'Mask email columns for everyone except pii_readers'
COLUMN MASK main.gov.redact
TO `account users` EXCEPT `pii_readers`
FOR TABLES
MATCH COLUMNS hasTagValue('pii', 'email') AS c
ON COLUMN c""")
```

## Traps and gotchas

- Row filters and masks need standard access mode or serverless (or dedicated compute with fine-grained access control).
- A table can have one row filter; a column can have one mask.
- ABAC policies are inherited by child objects.
