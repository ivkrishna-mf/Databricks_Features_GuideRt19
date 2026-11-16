# Git folders and CI/CD

Available since ~2020 · DE Professional exam: S8

## What it is

Git folders (formerly Repos) connect a workspace folder to a Git repository so you can branch, commit, pull and review. In CI/CD, a pipeline runs tests on pull requests and deploys the bundle on merge.

## How it flows

1. **Feature branch**: Develop in a Git folder or locally.
2. **Pull request**: CI runs unit tests and `bundle validate`.
3. **Merge to main**: CI deploys to staging and runs integration tests.
4. **Release**: CI deploys to prod as a service principal.
5. **Run**: Jobs run the deployed, versioned code.

```
[Feature branch] --> [Pull request] --> [Merge to main] --> [Release] --> [Run]
```

## When to choose it

**Choose it when**

- Team development with reviews.
- Promotion across environments.

**Pick something else when**

- Production jobs pointing at a user's Git folder or a moving branch that anyone can change.

## Senior engineer verdict

> Production runs deployed artifacts from a bundle, never a personal folder. If a job must read from Git directly, it points at a tag or release branch. Authentication in CI is OAuth for a service principal, ideally with workload identity federation so there is no stored secret.

## Examples

### 1. Create a Git folder and check out a tag

File: [`example_1.py`](example_1.py)

```python
from databricks.sdk import WorkspaceClient
w = WorkspaceClient()
repo = w.repos.create(url="https://github.com/acme/orders-platform.git", provider="gitHub",
                      path="/Workspace/Users/de@acme.com/orders-platform")
w.repos.update(repo_id=repo.id, tag="v1.4.0")        # detached at a release tag
```

### 2. CI workflow: test, validate, deploy

File: [`example_2.yml`](example_2.yml)

```yaml
# .github/workflows/deploy.yml
on:
  push: { branches: [main] }
jobs:
  deploy:
    runs-on: ubuntu-latest
    env:
      DATABRICKS_HOST: ${{ vars.DATABRICKS_HOST }}
      DATABRICKS_CLIENT_ID: ${{ secrets.SP_CLIENT_ID }}
      DATABRICKS_CLIENT_SECRET: ${{ secrets.SP_CLIENT_SECRET }}
    steps:
      - uses: actions/checkout@v4
      - uses: databricks/setup-cli@main
      - run: pip install -e ".[dev]" && pytest tests/unit
      - run: databricks bundle validate -t prod
      - run: databricks bundle deploy -t prod
```

### 3. Update a Git folder to a branch with the SDK

File: [`example_3.py`](example_3.py)

```python
from databricks.sdk import WorkspaceClient
w = WorkspaceClient()
repo = next(r for r in w.repos.list(path_prefix="/Repos/release/orders"))
w.repos.update(repo_id=repo.id, branch="release")      # pull latest of the branch
```

## Traps and gotchas

- Git folders version files, not jobs or clusters. Bundles deploy resources.
- Notebook outputs are not committed by default.
