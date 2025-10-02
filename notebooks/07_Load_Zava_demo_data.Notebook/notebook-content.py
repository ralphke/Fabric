# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {}
# META }

# CELL ********************

# Welcome to your new notebook
# Type here in the cell editor to add code!


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Import necessary libraries
import pandas as pd
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
import os

# Display Spark configuration
print(f"Spark Version: {spark.version}")
print(f"Application Name: {spark.sparkContext.appName}")
print("\nEnvironment ready for data upload!")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Define the source directory containing the parquet files
# Note: In Fabric, you would typically upload these files first or reference them from a Git repo
source_dir = "https://github.com/ralphke/Fabric/raw/refs/heads/main/sample-data/zava-demo/"
# Alternative: If running locally with the repo, use:
# source_dir = "../sample-data/zava-demo/"

# Define the files we want to upload
files_to_upload = [
    "customers.parquet",
    "products.parquet",
    "orders.parquet",
    "order_items.parquet",
    "sales_performance.parquet"
]

print(f"Source directory: {source_dir}")
print(f"Files to upload: {len(files_to_upload)}")
for f in files_to_upload:
    print(f"  - {f}")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Read customers parquet file
customers_path = os.path.join(source_dir, "customers.parquet")
df_customers = spark.read.parquet(customers_path)

print("Customers Schema:")
df_customers.printSchema()

print(f"\nTotal Customers: {df_customers.count()}")
print("\nSample Data:")
display(df_customers.limit(5))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
