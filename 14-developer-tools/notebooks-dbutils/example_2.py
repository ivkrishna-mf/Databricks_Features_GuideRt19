# Run child notebooks in parallel and collect results
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
from concurrent.futures import ThreadPoolExecutor
regions = ["emea", "amer", "apac"]

def run(region):
    return dbutils.notebook.run("./load_region", 3600, {"region": region, "run_date": run_date})

with ThreadPoolExecutor(max_workers=3) as pool:
    results = list(pool.map(run, regions))
print(results)        # each child ends with dbutils.notebook.exit("ok:<rows>")
