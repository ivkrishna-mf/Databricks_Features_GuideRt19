# Define jobs in Python for a bundle
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
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
