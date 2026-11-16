# UDFs: Python, pandas and Unity Catalog functions

Available since ~2017 · DE Professional exam: S1

## What it is

When built-in functions are not enough you can write your own. A Python UDF runs row by row. A pandas UDF receives Arrow batches as pandas Series and is vectorized. A Unity Catalog function (SQL or Python) is a governed, shareable object that can be called from any SQL or pipeline.

## How it flows

1. **Need custom logic**: Check for a built-in first.
2. **SQL expression possible?**: Use a SQL UDF: the optimizer can inline it.
3. **Vectorizable in Python?**: pandas UDF.
4. **Row logic only**: Python UDF.
5. **Shared across teams?**: Register in Unity Catalog and grant EXECUTE.

```
[Need custom logic] --> [SQL expression possible?] --> [Vectorizable in Python?] --> [Row logic only] --> [Shared across teams?]
```

## Choosing a UDF type

| Type | Speed | Choose when |
|---|---|---|
| Built-in function | Fastest, Photon | Always first |
| SQL UDF in Unity Catalog | Fast, inlined | Reusable business rules, row filters, column masks |
| pandas UDF | Vectorized through Arrow | Numeric or library logic over batches |
| Python UDF | Row by row; Arrow-optimized by default on Runtime 19 | Simple custom logic with no vector form |
| `applyInPandas` / `mapInPandas` | Per group or per batch | Model scoring, per-group algorithms |

## Senior engineer verdict

> Every UDF is a black box to the optimizer: no predicate pushdown through it, no Photon inside it. My order is built-ins, SQL UDF, pandas UDF, Python UDF. Governance rules such as masks belong in Unity Catalog SQL functions so they are defined once.

## Examples

### 1. pandas UDF and a plain Python UDF

File: [`example_1.py`](example_1.py)

```python
import pandas as pd
from pyspark.sql import functions as F

@F.pandas_udf("double")
def net_amount(gross: pd.Series, tax_rate: pd.Series) -> pd.Series:
    return gross / (1 + tax_rate)

@F.udf("string")
def initials(name):
    return "".join(p[0].upper() for p in name.split()) if name else None

df = orders.select("order_id", net_amount("gross", "tax_rate").alias("net"), initials("customer_name"))
```

### 2. Unity Catalog SQL and Python functions

File: [`example_2.py`](example_2.py)

```python
spark.sql("""
CREATE OR REPLACE FUNCTION main.fn.fiscal_quarter(d DATE) RETURNS STRING
RETURN concat('FY', year(add_months(d, 6)), '-Q', quarter(add_months(d, 6)))""")

spark.sql("""
CREATE OR REPLACE FUNCTION main.fn.clean_phone(p STRING) RETURNS STRING
LANGUAGE PYTHON AS $$
import re
return re.sub(r'[^0-9+]', '', p) if p else None
$$""")
spark.sql("GRANT EXECUTE ON FUNCTION main.fn.fiscal_quarter TO `analysts`")
```

## Traps and gotchas

- Calling a UC function needs EXECUTE on it plus USE CATALOG and USE SCHEMA.
- A filter on a UDF result cannot be pushed to the files.
- Python UDFs are not accelerated by Photon.
