# Spark Connect and Databricks Connect

Available since ~2019 · Part of [How Spark executes your code](../README.md)

## What it is

Spark Connect separates the client from the cluster: your code builds a plan locally and sends it over gRPC to remote compute. Databricks Connect is the Databricks client built on it, so you can run PySpark from your IDE, a script or a test suite against serverless or a cluster, with breakpoints and local tooling.

## How it flows

1. **IDE or script**: Your Python process with databricks-connect installed.
2. **Build plan**: DataFrame calls create an unresolved plan locally.
3. **Send**: The plan goes to Databricks compute, authenticated with your profile.
4. **Execute remotely**: Data never leaves Databricks unless you collect it.
5. **Results**: Only collected results come back.

```
[IDE or script] --> [Build plan] --> [Send] --> [Execute remotely] --> [Results]
```

## When to choose it

**Choose it when**

- Local development and debugging in VS Code or PyCharm.
- Integration tests in CI against real compute.
- Python applications that need Spark without running on a cluster.

**Pick something else when**

- Code that relies on the RDD API or `sparkContext`: those are not available through Spark Connect.
- Moving large data to the client.

## Senior engineer verdict

> Databricks Connect is how I test the transformations in my package: the same functions run in pytest locally and in the job. Standard access mode and serverless also run on Spark Connect, so code that avoids RDDs works everywhere.

## Examples

### 1. Session against serverless or a profile

File: [`example_1.py`](example_1.py)

```python
from databricks.connect import DatabricksSession

spark = DatabricksSession.builder.serverless().getOrCreate()
# or: DatabricksSession.builder.profile("dev").clusterId("0123-456789-abc").getOrCreate()

df = spark.table("samples.nyctaxi.trips").where("trip_distance > 10")
print(df.count())
```

### 2. pytest fixture shared by every test

File: [`example_2.py`](example_2.py)

```python
# tests/conftest.py
import pytest
from databricks.connect import DatabricksSession

@pytest.fixture(scope="session")
def spark():
    return DatabricksSession.builder.serverless().getOrCreate()
```

## Traps and gotchas

- The Databricks Connect version should match the runtime major and minor version you target.
- `spark.sparkContext` and RDD operations fail under Spark Connect.
