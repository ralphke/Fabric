# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {}
# META }

# CELL ********************

from azure.identity import DefaultAzureCredential
from azure.storage.filedatalake import DataLakeServiceClient

# Replace with your actual workspace and lakehouse names
workspace_name = "Learning-Fabric-Workspace"
lakehouse_name = "Zava_Lakehouse"
file_path_local = "customers.parquet"
file_path_onelake = "Files/customers.parquet"

# Authenticate using DefaultAzureCredential (requires az login)
credential = DefaultAzureCredential()

# Construct OneLake URL
account_url = f"https://onelake.dfs.fabric.microsoft.com"
filesystem_name = workspace_name
directory_name = f"{lakehouse_name}.lakehouse"

# Create service client
service_client = DataLakeServiceClient(account_url=account_url, credential=credential)

# Get filesystem and directory clients
filesystem_client = service_client.get_file_system_client(filesystem_name)
directory_client = filesystem_client.get_directory_client(directory_name)





# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Import necessary libraries
import pandas as pd
import requests 
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
customers_path = source_dir + "customers.parquet"
response = requests.get(customers_path) #, stream=True)
response.raise_for_status()
if response.status_code == 200:
    content = response.content  # For binary files
    # print(content)
else:
    print(f"Failed to fetch file: {response.status_code}")

# Upload the file
file_client = directory_client.create_file(file_path_onelake)
file_client.append_data(data=content, offset=0, length=len(content))
file_client.flush_data(len(content))

print("✅ File uploaded to OneLake successfully!")


df_customers = spark.read.parquet(tmp_path)

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
