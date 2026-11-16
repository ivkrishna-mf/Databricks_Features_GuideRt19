# Update a Git folder to a branch with the SDK
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
from databricks.sdk import WorkspaceClient
w = WorkspaceClient()
repo = next(r for r in w.repos.list(path_prefix="/Repos/release/orders"))
w.repos.update(repo_id=repo.id, branch="release")      # pull latest of the branch
