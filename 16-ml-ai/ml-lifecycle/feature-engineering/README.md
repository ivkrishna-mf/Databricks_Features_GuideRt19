# Feature engineering and online features

Available since ~2021 · Part of [Machine learning lifecycle on Databricks](../README.md)

## What it is

Any Delta table with a primary key can be a feature table. The Feature Engineering client builds training sets by joining features to labels, with point-in-time lookups for time series keys so training never sees future values. Models logged with the client look up features automatically at scoring time, and features can be published to an online store (Lakebase) for low-latency serving.

## How it flows

1. **Feature table**: Primary key, optional timestamp key.
2. **Training set**: Labels plus FeatureLookups, joined point in time.
3. **Log model**: Feature metadata is packaged with the model.
4. **Batch score**: score_batch looks up features by key.
5. **Online**: Publish to an online store; serving endpoints look up features at request time.

```
[Feature table] --> [Training set] --> [Log model] --> [Batch score] --> [Online]
```

## When to choose it

**Choose it when**

- Features shared across models or teams.
- Time-dependent features where leakage is a risk.

**Pick something else when**

- One-off features used by a single notebook.

## Senior engineer verdict

> Point-in-time correctness is the reason to use this, not the catalog page. A naive join of 'latest customer features' to historical labels leaks the future and inflates offline metrics.

## Examples

### 1. Create a feature table and a training set

File: [`example_1.py`](example_1.py)

```python
from databricks.feature_engineering import FeatureEngineeringClient, FeatureLookup
fe = FeatureEngineeringClient()
fe.create_table(name="main.ml.customer_features", primary_keys=["customer_id"],
                timestamp_keys=["as_of"], df=features_df,
                description="Rolling 30-day spend and visit counts")

training_set = fe.create_training_set(
    df=spark.table("main.ml.churn_labels"),          # customer_id, label_ts, churned
    feature_lookups=[FeatureLookup(table_name="main.ml.customer_features",
                                   lookup_key="customer_id", timestamp_lookup_key="label_ts")],
    label="churned")
train_pdf = training_set.load_df().toPandas()
```

### 2. Log a feature-aware model and score by key

File: [`example_2.py`](example_2.py)

```python
import mlflow
fe.log_model(model=model, artifact_path="model", flavor=mlflow.sklearn,
             training_set=training_set, registered_model_name="main.ml.churn_fs_model")

scored = fe.score_batch(model_uri="models:/main.ml.churn_fs_model@champion",
                        df=spark.table("main.ml.customers_to_score"))   # only keys needed
```

## Traps and gotchas

- Feature tables need a primary key; time series feature tables also need a timestamp key.
