# Declarative Automation Bundles

**Major feature** · Available since ~2023 · DE Professional exam: S1, S8

## What it is

Bundles (formerly Databricks Asset Bundles) describe a project as code: source files plus YAML or Python definitions of jobs, pipelines, schemas, volumes, dashboards and more. The CLI validates and deploys the same definition to each target, such as dev, staging and prod.

## How it flows

1. **databricks bundle init**: Start from a template.
2. **Edit databricks.yml**: Bundle name, includes, variables, resources, targets.
3. **bundle validate**: Checks the configuration.
4. **bundle deploy -t dev**: Uploads files and creates or updates resources.
5. **bundle run**: Runs a job or pipeline. CI repeats this for prod with a service principal.

```
[databricks bundle init] --> [Edit databricks.yml] --> [bundle validate] --> [bundle deploy -t dev] --> [bundle run]
```

## When to choose it

**Choose it when**

- Any project that will be deployed to more than one environment.
- You want reviews and rollbacks for jobs and pipelines, not only for code.

**Pick something else when**

- Managing workspaces, networks and account-level setup: that is Terraform territory.

## Senior engineer verdict

> The structure I use: `src/` for a Python package with pure transformation functions, `resources/` with one YAML per job or pipeline, `tests/`, and a short `databricks.yml` with variables and targets. Development mode gives every engineer an isolated, prefixed copy; production mode deploys from CI as a service principal and nobody deploys by hand.

## Examples

### 1. Define jobs in Python for a bundle

File: [`example_1.py`](example_1.py)

```python
# resources/__init__.py  (databricks.yml: python: { resources: ["resources:load_resources"] })
from databricks.bundles.core import Bundle, Resources
from databricks.bundles.jobs import Job

def load_resources(bundle: Bundle) -> Resources:
    resources = Resources()
    for table in ["orders", "customers", "products"]:
        resources.add_job(f"load_{table}", Job.from_dict({
            "name": f"load_{table}_{bundle.target}",
            "tasks": [{"task_key": "load",
                       "notebook_task": {"notebook_path": "src/load_table.py",
                                         "base_parameters": {"table": table}}}]}))
    return resources
```

### 2. Package code the bundle deploys as a wheel

File: [`example_2.py`](example_2.py)

```python
# src/orders/main.py  (entry point "orders-main" in pyproject.toml, task: python_wheel_task)
import argparse
from pyspark.sql import SparkSession, functions as F

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--catalog", default="dev")
    args = p.parse_args()
    spark = SparkSession.builder.getOrCreate()
    (spark.table(f"{args.catalog}.bronze.orders")
        .where("order_id IS NOT NULL")
        .withColumn("loaded_at", F.current_timestamp())
        .write.mode("overwrite").saveAsTable(f"{args.catalog}.silver.orders"))

if __name__ == "__main__":
    main()
```

### 3. databricks.yml with two targets

File: [`example_3.yml`](example_3.yml)

```yaml
bundle:
  name: orders_platform

include:
  - resources/*.yml

variables:
  catalog:
    default: dev

artifacts:
  orders_lib:
    type: whl
    path: .

targets:
  dev:
    mode: development          # prefixes names, pauses schedules
    default: true
    workspace: { host: https://dev.cloud.databricks.com }
  prod:
    mode: production
    workspace: { host: https://prod.cloud.databricks.com, root_path: /Workspace/Shared/.bundle/orders }
    variables: { catalog: main }
    run_as: { service_principal_name: "sp-orders-deploy" }
```

### 4. A pipeline resource and the deploy commands

File: [`example_4.yml`](example_4.yml)

```yaml
# resources/orders_pipeline.yml
resources:
  pipelines:
    orders:
      name: orders_${bundle.target}
      catalog: ${var.catalog}
      schema: orders
      serverless: true
      libraries:
        - glob: { include: ../src/pipelines/** }

# Shell:
#   databricks bundle validate -t prod
#   databricks bundle deploy   -t prod
#   databricks bundle run orders -t prod
```

## Traps and gotchas

- Development mode prefixes resources with the user name and pauses triggers; production mode validates that you are not deploying from a personal path.
- The rename is non-breaking: the command is still `databricks bundle`.
- `bundle deployment bind` links an existing job or pipeline to a bundle resource.
