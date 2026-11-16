# Libraries and dependency troubleshooting

Available since ~2015 · DE Professional exam: S1

## What it is

Where a library is declared depends on the compute. Serverless jobs and notebooks use an environment with a dependency list. Pipelines declare dependencies in the pipeline environment. Classic clusters use cluster or task libraries. Notebook-scoped `%pip` installs apply to one session.

## How it flows

1. **Import fails or wrong version**: Read the error: not found, conflict, or build failure.
2. **Find the scope**: Serverless environment, pipeline environment, cluster library or notebook.
3. **Pin**: Exact versions; build your own code as a wheel.
4. **Rebuild the environment**: Redeploy the bundle or restart Python.
5. **Verify**: Print the version in the task.

```
[Import fails or wrong version] --> [Find the scope] --> [Pin] --> [Rebuild the environment] --> [Verify]
```

## When to choose it

**Choose it when**

- Wheels for your own code.
- Pinned PyPI versions for everything else.

**Pick something else when**

- Unpinned installs in production.
- Installing over packages the runtime depends on, such as pyspark or numpy, without checking compatibility.

## Senior engineer verdict

> Most dependency incidents are one of three: a package the runtime no longer ships, two libraries pinning different versions of a shared dependency, or a source build that needs a compiler the image lacks. The fix is always the same discipline: one lock file, wheels built in CI, and the same environment spec in every target.

## Examples

### 1. Install a library on a classic cluster

File: [`example_1.py`](example_1.py)

```python
from databricks.sdk import WorkspaceClient
from databricks.sdk.service import compute
w = WorkspaceClient()
w.libraries.install(cluster_id="0123-456789-abc", libraries=[
    compute.Library(pypi=compute.PythonPyPiLibrary(package="rapidfuzz==3.9.7")),
    compute.Library(whl="/Volumes/main/ops/libs/orders_lib-1.4.0-py3-none-any.whl")])
for s in w.libraries.cluster_status(cluster_id="0123-456789-abc"):
    print(s.library, s.status)
```

### 2. Pipeline environment with dependencies

File: [`example_2.yml`](example_2.yml)

```yaml
resources:
  pipelines:
    orders:
      serverless: true
      environment:
        dependencies:
          - ../dist/orders_lib-1.4.0-py3-none-any.whl
          - pydantic==2.9.2
      libraries:
        - glob: { include: ../src/pipelines/** }
```

### 3. Diagnose a version conflict in a notebook

File: [`example_3.py`](example_3.py)

```python
%pip install rapidfuzz==3.9.7 "pydantic>=2.8,<3"
dbutils.library.restartPython()

import importlib.metadata as md
for pkg in ["pydantic", "rapidfuzz", "pyarrow"]:
    print(pkg, md.version(pkg))
```

## Traps and gotchas

- After `%pip install` you must restart Python for already-imported modules.
- `%pip` does not work in pipeline source files; declare dependencies in the pipeline environment.
- A wheel built for a different Python version fails to install on a newer runtime.
