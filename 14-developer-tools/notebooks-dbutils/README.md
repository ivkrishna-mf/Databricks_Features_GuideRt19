# Notebooks, widgets and dbutils

**Major feature** · Available since ~2013

## What it is

Notebooks mix Python, SQL, Scala and Markdown cells, with real-time co-editing, comments, version history, Git folder integration and the Databricks Assistant. `dbutils` adds helpers for files, widgets (parameters), secrets, job task values and calling other notebooks.

## How it flows

1. **Write cells**: Python by default; `%sql`, `%md` and `%pip` switch mode.
2. **Parameters**: Widgets receive job or caller parameters.
3. **Reuse**: `%run` inlines another notebook; `dbutils.notebook.run` runs it as a child job.
4. **Assistant**: Generate, explain and fix code in context.
5. **Ship**: Move stable logic into Python files and a package.

```
[Write cells] --> [Parameters] --> [Reuse] --> [Assistant] --> [Ship]
```

## When to choose it

**Choose it when**

- Exploration, prototyping, teaching, demos and lightweight jobs.

**Pick something else when**

- Large production codebases kept only as notebooks: move logic to tested Python modules.

## %run or dbutils.notebook.run

|  | %run | dbutils.notebook.run |
|---|---|---|
| Execution | Same session, inline | Separate ephemeral run |
| Shares variables and functions | Yes | No; returns a string with `dbutils.notebook.exit` |
| Parameters | No | Yes, as widget values |
| Use for | Shared helper definitions | Parameterized child workflows, parallel runs |

## Senior engineer verdict

> Notebooks are a great front end and a weak place to keep business logic. My notebooks import from a package and contain orchestration and parameters only, which makes them testable and short. For parameters, widgets in development and job parameters in production share the same code.

## Examples

### 1. Widgets as parameters and files with dbutils

File: [`example_1.py`](example_1.py)

```python
dbutils.widgets.text("run_date", "2026-11-15", "Run date")
dbutils.widgets.dropdown("env", "dev", ["dev", "prod"])
run_date = dbutils.widgets.get("run_date")

for f in dbutils.fs.ls("/Volumes/main/landing/orders/")[:5]:
    print(f.name, f.size)
dbutils.fs.cp("/Volumes/main/landing/orders/a.json", "/Volumes/main/archive/orders/a.json")
```

### 2. Run child notebooks in parallel and collect results

File: [`example_2.py`](example_2.py)

```python
from concurrent.futures import ThreadPoolExecutor
regions = ["emea", "amer", "apac"]

def run(region):
    return dbutils.notebook.run("./load_region", 3600, {"region": region, "run_date": run_date})

with ThreadPoolExecutor(max_workers=3) as pool:
    results = list(pool.map(run, regions))
print(results)        # each child ends with dbutils.notebook.exit("ok:<rows>")
```

## Traps and gotchas

- `%run` must be alone in its cell.
- `dbutils.notebook.run` does not share state with the caller; pass values through parameters and the exit string.
- For new orchestration, a job with a For each task is usually cleaner than notebook.run loops.

## Sub-features

- [Secrets](secrets/README.md)
