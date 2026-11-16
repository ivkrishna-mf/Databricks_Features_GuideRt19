# MLflow tracking and models in Unity Catalog

Available since ~2023 · Part of [Machine learning lifecycle on Databricks](../README.md)

## What it is

MLflow records runs (parameters, metrics, artifacts, models). Registering a model in Unity Catalog creates a governed, versioned object with lineage to the data and run that produced it. Aliases such as champion and challenger point to versions; code loads by alias.

## How it flows

1. **Run**: Log params, metrics, model with a signature.
2. **Register**: New version of catalog.schema.model.
3. **Validate**: Tests and evaluation on the new version.
4. **Set alias**: champion now points to the new version.
5. **Consumers**: Load models:/name@champion; no code change.

```
[Run] --> [Register] --> [Validate] --> [Set alias] --> [Consumers]
```

## When to choose it

**Choose it when**

- Every model that will be used by anything other than its author.

**Pick something else when**

- Hard-coding version numbers in scoring jobs.

## Senior engineer verdict

> I promote by moving an alias from a CI job after evaluation passes, and I keep the previous version as a fallback alias. Rollback is then one API call. Grants on the model (EXECUTE) control who can load it.

## Examples

### 1. Log with signature and register

File: [`example_1.py`](example_1.py)

```python
import mlflow
from mlflow.models import infer_signature
mlflow.set_registry_uri("databricks-uc")
with mlflow.start_run():
    sig = infer_signature(X_tr, model.predict(X_tr))
    mlflow.sklearn.log_model(model, name="model", signature=sig, input_example=X_tr.head(3),
                             registered_model_name="main.ml.churn_model")
```

### 2. Promote with aliases and load by alias

File: [`example_2.py`](example_2.py)

```python
from mlflow import MlflowClient
client = MlflowClient(registry_uri="databricks-uc")
latest = max(int(v.version) for v in client.search_model_versions("name='main.ml.churn_model'"))
current = client.get_model_version_by_alias("main.ml.churn_model", "champion")
client.set_registered_model_alias("main.ml.churn_model", "previous", current.version)
client.set_registered_model_alias("main.ml.churn_model", "champion", latest)

model = mlflow.pyfunc.load_model("models:/main.ml.churn_model@champion")
```

## Traps and gotchas

- Models in Unity Catalog require a signature.
- Reading a UC model needs EXECUTE on it plus USE CATALOG and USE SCHEMA.
