# Create a feature table and a training set
# Runs in a Databricks notebook or job (spark and dbutils are predefined).
from databricks.feature_engineering import FeatureEngineeringClient, FeatureLookup
fe = FeatureEngineeringClient()
fe.create_table(name="main.ml.customer_features", primary_keys=["customer_id"],
                timestamp_keys=["as_of"], df=features_df,
                description="Rolling 30-day spend and visit counts")

training_set = fe.create_training_set(
    df=spark.table("main.ml.churn_labels"),          # customer_id, label_ts, churned
    feature_lookups=[FeatureLookup(table_name="main.ml.customer_features",
                                   lookup_key="customer_id", timestamp_lookup_key="label_ts")],
    label="churned")
train_pdf = training_set.load_df().toPandas()
