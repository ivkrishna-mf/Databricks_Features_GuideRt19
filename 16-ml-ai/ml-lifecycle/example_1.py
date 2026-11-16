# Train with autologging
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
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
