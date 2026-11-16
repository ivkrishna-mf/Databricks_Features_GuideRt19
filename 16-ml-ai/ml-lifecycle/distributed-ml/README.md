# Distributed training and Spark ML

Available since ~2016 · Part of [Machine learning lifecycle on Databricks](../README.md)

## What it is

For large tabular data, Spark MLlib trains pipelines (feature transformers plus estimators) across the cluster. For deep learning, TorchDistributor runs PyTorch training across GPUs and nodes. Many small models train in parallel with applyInPandas. Hyperparameter search parallelizes with Optuna or Ray.

## How it flows

1. **Data in Delta**: Features prepared with Spark.
2. **Choose strategy**: Spark ML, single-node with more memory, distributed deep learning or many models.
3. **Train**: With MLflow autologging.
4. **Register and score**: Same path as any model.

```
[Data in Delta] --> [Choose strategy] --> [Train] --> [Register and score]
```

## When to choose it

**Choose it when**

- Spark ML: data too large for one machine and classical algorithms suffice.
- TorchDistributor: deep learning across GPUs.

**Pick something else when**

- Distributing a training job that fits on one large node: single-node is usually faster and simpler.

## Senior engineer verdict

> Try one big node first. Distributed training adds communication cost and failure modes, so I reach for it only when data or model size forces it.

## Examples

### 1. Spark ML pipeline

File: [`example_1.py`](example_1.py)

```python
from pyspark.ml import Pipeline
from pyspark.ml.feature import StringIndexer, VectorAssembler
from pyspark.ml.classification import GBTClassifier
import mlflow
mlflow.pyspark.ml.autolog()

df = spark.table("main.ml.churn_training")
pipe = Pipeline(stages=[
    StringIndexer(inputCol="plan", outputCol="plan_idx", handleInvalid="keep"),
    VectorAssembler(inputCols=["plan_idx", "tenure", "monthly_spend"], outputCol="features"),
    GBTClassifier(labelCol="churned", featuresCol="features", maxIter=50)])
train, test = df.randomSplit([0.8, 0.2], seed=7)
model = pipe.fit(train)
model.transform(test).select("churned", "prediction").show(5)
```

### 2. Distributed PyTorch with TorchDistributor

File: [`example_2.py`](example_2.py)

```python
from pyspark.ml.torch.distributor import TorchDistributor

def train_fn(epochs: int):
    import torch, torch.distributed as dist
    dist.init_process_group("nccl")
    model = torch.nn.parallel.DistributedDataParallel(build_model().cuda())
    for _ in range(epochs):
        train_one_epoch(model)          # your loop; each rank reads its shard
    dist.destroy_process_group()

TorchDistributor(num_processes=8, local_mode=False, use_gpu=True).run(train_fn, 5)
```

## Traps and gotchas

- Spark ML needs features in a single vector column.
- GPU clusters need an ML runtime (or serverless GPU compute).
