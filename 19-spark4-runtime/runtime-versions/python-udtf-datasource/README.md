# Python UDTFs and the Python Data Source API

Available since ~2023 · Part of [Databricks Runtime versions from the beginning to 19](../README.md)

## What it is

A Python user-defined table function (UDTF) returns zero or more rows per input row, so it can explode, parse or call an API and return a table. The Python Data Source API lets you write a custom batch or streaming source or sink in pure Python and use it with `spark.read.format(...)`.

## How it flows

1. **Define class**: eval yields rows (UDTF) or read yields rows (data source).
2. **Register**: spark.udtf.register or spark.dataSource.register.
3. **Use**: In SQL or DataFrame code like a built-in.
4. **Distribute**: Partitions run in parallel on executors.

```
[Define class] --> [Register] --> [Use] --> [Distribute]
```

## When to choose it

**Choose it when**

- UDTF: one input expands into many rows with custom logic.
- Data source: an internal API or file format with no connector.

**Pick something else when**

- Sources that already have a supported connector or Lakeflow Connect integration.

## Senior engineer verdict

> The Python data source API replaced the 'call an API in a loop on the driver' pattern for me. Partition the reads properly and Spark parallelizes them for you.

## Examples

### 1. Python UDTF that splits text into words

File: [`example_1.py`](example_1.py)

```python
from pyspark.sql.functions import udtf

@udtf(returnType="word string, position int")
class SplitWords:
    def eval(self, text: str):
        for i, w in enumerate((text or "").split()):
            yield w.lower(), i

spark.udtf.register("split_words", SplitWords)
spark.sql("SELECT * FROM split_words('Delta Lake on Databricks')").show()
from pyspark.sql.functions import lit
SplitWords(lit("one two")).show()          # DataFrame API
```

### 2. Custom batch data source

File: [`example_2.py`](example_2.py)

```python
from pyspark.sql.datasource import DataSource, DataSourceReader, InputPartition

class RangeReader(DataSourceReader):
    def __init__(self, options):
        self.n = int(options.get("rows", "10"))
    def partitions(self):
        return [InputPartition(i) for i in range(4)]
    def read(self, partition):
        for i in range(partition.value, self.n, 4):
            yield (i, i * i)

class SquaresSource(DataSource):
    @classmethod
    def name(cls):
        return "squares"
    def schema(self):
        return "n int, sq int"
    def reader(self, schema):
        return RangeReader(self.options)

spark.dataSource.register(SquaresSource)
spark.read.format("squares").option("rows", "20").load().show()
```

## Traps and gotchas

- UDTF eval must yield tuples matching returnType.
- Data source classes must be importable on executors; keep them in a module or define them in the notebook before registering.
