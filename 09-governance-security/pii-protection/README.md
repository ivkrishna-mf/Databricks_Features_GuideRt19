# Pseudonymization, anonymization and PII pipelines

Available since ~2022 · DE Professional exam: S6

## What it is

Pseudonymization replaces identifiers with a stand-in that can be linked back with extra information (salted hash, token from a vault table). Anonymization removes the link for good (suppression, generalization into ranges, aggregation). Pseudonymized data is still personal data.

## How it flows

1. **Raw PII in bronze**: Restricted schema, short retention.
2. **Detect and tag**: Data classification or explicit tags.
3. **Transform in silver**: Hash or tokenize identifiers, generalize quasi-identifiers.
4. **Mask at read**: Column masks for anything still sensitive.
5. **Analytics**: Consumers work on pseudonymized or aggregated data.

```
[Raw PII in bronze] --> [Detect and tag] --> [Transform in silver] --> [Mask at read] --> [Analytics]
```

## When to choose it

**Choose it when**

- Any table that leaves the restricted zone.

**Pick something else when**

- Unsalted hashes of low-entropy values such as phone numbers: they can be reversed by brute force.

## Methods

| Method | Reversible | Example | Use |
|---|---|---|---|
| Hashing with salt | No, but linkable | `sha2(concat(salt, email), 256)` | Join keys without exposing the value |
| Tokenization | Yes, through a vault table | Random token per customer id | Need to re-identify under control |
| Suppression | No | Drop or null the column | Field not needed |
| Generalization | No | Age 37 becomes 30 to 39; zip to first 3 digits | Keep analytic value, reduce uniqueness |

## Senior engineer verdict

> I separate identity from behavior early: one small, locked-down table maps real identifiers to tokens, and every other table carries only the token. A deletion request then touches one row in the mapping table and the rest of the lake is no longer linkable.

## Examples

### 1. Salted hash and generalization in a streaming silver table

File: [`example_1.py`](example_1.py)

```python
from pyspark.sql import functions as F
salt = dbutils.secrets.get("privacy", "email_salt")
silver = (spark.readStream.table("main.bronze.signups")
    .withColumn("email_key", F.sha2(F.concat(F.lit(salt), F.lower("email")), 256))
    .withColumn("age_band", F.concat((F.floor(F.col("age") / 10) * 10).cast("string"), F.lit("s")))
    .withColumn("zip3", F.substring("zip", 1, 3))
    .drop("email", "age", "zip", "full_name"))
```

### 2. Tokenization with a vault table

File: [`example_2.py`](example_2.py)

```python
from pyspark.sql import functions as F
new_ids = (spark.table("main.bronze.customers").select("customer_id").distinct()
    .join(spark.table("main.vault.customer_tokens"), "customer_id", "left_anti")
    .withColumn("token", F.expr("uuid()")))
new_ids.write.mode("append").saveAsTable("main.vault.customer_tokens")     # restricted schema

tokenized = (spark.table("main.bronze.orders")
    .join(spark.table("main.vault.customer_tokens"), "customer_id")
    .drop("customer_id"))
```

## Traps and gotchas

- Hashing is pseudonymization, not anonymization.
- `ai_mask` and data classification help detect and redact PII in free text.
