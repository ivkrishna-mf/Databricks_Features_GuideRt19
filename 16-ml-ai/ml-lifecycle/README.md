# Machine learning lifecycle on Databricks

**Major feature** · Available since ~2018

## What it is

Databricks runs the whole ML loop on the same governed data: features from Delta tables, experiments tracked in MLflow, models registered in Unity Catalog, deployment to Model Serving or batch scoring with Spark, and monitoring of inference tables. Mosaic AI is the umbrella name for the AI side: serving, vector search, agents, evaluation and the AI Gateway.

## How it flows

1. **Data and features**: Gold tables and feature tables in Unity Catalog.
2. **Train and track**: Notebooks or jobs; MLflow logs params, metrics and models.
3. **Register**: Model versions in Unity Catalog with aliases such as champion.
4. **Serve**: Real-time endpoint or batch scoring with spark_udf or ai_query.
5. **Monitor**: Inference tables, data profiling and drift; retrain on a schedule.

```
[Data and features] --> [Train and track] --> [Register] --> [Serve] --> [Monitor]
```

## Pieces and when to use them

| Need | Feature |
|---|---|
| Track experiments and compare runs | MLflow tracking |
| Version, approve and govern models | Models in Unity Catalog |
| Reusable, point-in-time correct features | Feature engineering in Unity Catalog |
| Low-latency predictions over HTTP | Model Serving |
| Score millions of rows | Batch inference with `mlflow.pyfunc.spark_udf` or `ai_query` |
| Use or govern LLMs | Foundation Model APIs and AI Gateway |
| Retrieval for RAG | Vector Search |
| Build and evaluate agents | Agent Bricks, Agent Framework, MLflow 3 tracing and evaluation |

## Senior engineer verdict

> Batch first. Most 'real-time ML' requests are satisfied by scoring every hour into a table that the app reads. I go to a serving endpoint when the input only exists at request time. Either way, the model goes through Unity Catalog with an alias so promotion is a pointer change, not a redeploy.

## Examples

### 1. Train with autologging

File: [`example_1.py`](example_1.py)

```python
import mlflow
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

mlflow.set_registry_uri("databricks-uc")
mlflow.sklearn.autolog()
pdf = spark.table("main.ml.churn_training").toPandas()
X, y = pdf.drop(columns=["churned"]), pdf["churned"]
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=7)

with mlflow.start_run(run_name="rf_baseline") as run:
    model = RandomForestClassifier(n_estimators=300, max_depth=8).fit(X_tr, y_tr)
    mlflow.log_metric("test_accuracy", model.score(X_te, y_te))
```

### 2. Batch scoring with the champion model

File: [`example_2.py`](example_2.py)

```python
import mlflow
from pyspark.sql import functions as F
mlflow.set_registry_uri("databricks-uc")
predict = mlflow.pyfunc.spark_udf(spark, "models:/main.ml.churn_model@champion", result_type="double")

scored = (spark.table("main.ml.churn_features_today")
    .withColumn("churn_score", predict(*[c for c in feature_cols])))
scored.write.mode("overwrite").saveAsTable("main.ml.churn_scores")
```

## Traps and gotchas

- Unity Catalog models use three-level names and aliases; workspace registry stages (Staging, Production) are legacy.
- spark_udf needs the same Python dependencies as training; MLflow records them with the model.

## Sub-features

- [MLflow tracking and models in Unity Catalog](mlflow-uc-models/README.md)
- [Feature engineering and online features](feature-engineering/README.md)
- [Distributed training and Spark ML](distributed-ml/README.md)
