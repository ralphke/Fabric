# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "5d7986b2-2b35-42e0-851c-fe114ac8a3b9",
# META       "default_lakehouse_name": "Zava_Lakehouse",
# META       "default_lakehouse_workspace_id": "7a2d7ac6-d893-474a-881a-f90969e809ea",
# META       "known_lakehouses": [
# META         {
# META           "id": "5d7986b2-2b35-42e0-851c-fe114ac8a3b9"
# META         }
# META       ]
# META     }
# META   }
# META }

# MARKDOWN ********************

# # OneLake Introduction and Capabilities
# 
# This notebook demonstrates the key capabilities of Microsoft Fabric OneLake - the unified data lake for the entire organization.
# 
# ## What is OneLake?
# 
# OneLake is a unified, logical data lake for your entire organization. It provides:
# - **Single storage location** for all your analytics data
# - **Automatic integration** with all Fabric workloads
# - **Delta Parquet format** for efficient storage and querying
# - **Lakehouse architecture** combining data lake and data warehouse capabilities
# - **Shortcuts** to external data sources without data movement

# MARKDOWN ********************

# ## Prerequisites
# 
# To run this notebook, you need:
# - A Microsoft Fabric workspace
# - A Lakehouse created in your workspace
# - Appropriate permissions to read/write data

# MARKDOWN ********************

# ## 1. Connecting to OneLake
# 
# In Fabric notebooks, you're automatically connected to OneLake. Let's verify the connection and explore the environment.

# CELL ********************

# Import necessary libraries
import pandas as pd
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *

# Display Spark configuration
print(f"Spark Version: {spark.version}")
print(f"Application Name: {spark.sparkContext.appName}")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## 2. Reading Data from OneLake
# 
# OneLake supports multiple file formats. Let's demonstrate reading different formats:

# CELL ********************

# Example: Reading CSV data from OneLake
# Replace with your actual path
# csv_path = "Files/sample_data.csv"
# df_csv = spark.read.csv(csv_path, header=True, inferSchema=True)
# display(df_csv.limit(10))

print("To read CSV files, use: spark.read.csv(path, header=True, inferSchema=True)")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC SHOW DATABASES

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC -- Validate if any tables are already in existance
# MAGIC SHOW TABLES

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC select * from Zava_Lakehouse.customers LIMIT 10

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Example: Reading Parquet data from OneLake
parquet_path = "Files/sales_parquet"
df_parquet = spark.read.parquet(parquet_path)
df_parquet.printSchema()
display(df_parquet.limit(10))

print("To read Parquet files, use: spark.read.parquet(path)")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Example: Reading Delta tables from OneLake
delta_table_path = "Tables/customers"
df_delta = spark.read.format("delta").load(delta_table_path)
display(df_delta.limit(10))

print("To read Delta tables, use: spark.read.format('delta').load(path)")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## 3. Creating Sample Data
# 
# Let's create some sample data to demonstrate OneLake capabilities:

# CELL ********************

# Create sample sales data
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType, DateType
from datetime import datetime, timedelta
import random



# Generate sample data
sample_data = []
start_date = datetime(2025, 1, 1)
products = ['Laptop', 'Phone', 'Tablet', 'Monitor', 'Keyboard']
regions = ['North', 'South', 'East', 'West']

for i in range(100):
    sample_data.append((
        i + 1,
        random.choice(products),
        random.choice(regions),
        random.randint(1, 10),
        round(random.uniform(100, 2000), 2),
        start_date + timedelta(days=random.randint(0, 365))
    ))

# Define schema
schema = StructType([
    StructField("OrderID", IntegerType(), False),
    StructField("Product", StringType(), False),
    StructField("Region", StringType(), False),
    StructField("Quantity", IntegerType(), False),
    StructField("Amount", DoubleType(), False),
    StructField("OrderDate", DateType(), False)
])

# Create DataFrame
df_sales = spark.createDataFrame(sample_data, schema)
display(df_sales.limit(10))
print(f"Total records: {df_sales.count()}")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## 4. Writing Data to OneLake
# 
# Demonstrate different ways to write data to OneLake:

# CELL ********************

# Write as Delta table (recommended for OneLake)
# This provides ACID transactions, time travel, and optimal performance
delta_table_name = "sales_demo"

# Write to Delta table
df_sales.write.format("delta") \
    .mode("overwrite") \
    .save(f"Tables/{delta_table_name}")

print(f"Data written to Delta table: {delta_table_name}")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Write as Parquet files
df_sales.write.mode("overwrite") \
    .parquet("Files/sales_parquet")

print("Data written to Parquet format")
display(df_sales)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## 5. Querying Data with SQL
# 
# OneLake supports SQL queries through Spark SQL:

# CELL ********************

# Register DataFrame as temp view
df_sales.createOrReplaceTempView("sales")

# Run SQL query
result = spark.sql("""
    SELECT 
        Region,
        Product,
        COUNT(*) as OrderCount,
        SUM(Quantity) as TotalQuantity,
        ROUND(SUM(Amount), 2) as TotalRevenue
    FROM sales
    GROUP BY Region, Product
    ORDER BY TotalRevenue DESC
""")

display(result)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## 6. Data Transformations
# 
# Demonstrate common data transformation operations:

# CELL ********************

from pyspark.sql.functions import round, year, month, quarter, col
# Add calculated columns
df_enriched = df_sales \
    .withColumn("UnitPrice", round(col("Amount") / col("Quantity"), 2)) \
    .withColumn("Year", year(col("OrderDate"))) \
    .withColumn("Month", month(col("OrderDate"))) \
    .withColumn("Quarter", quarter(col("OrderDate")))

display(df_enriched.limit(10))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

from pyspark.sql.functions import count,avg, sum
# Aggregations
monthly_summary = df_enriched \
    .groupBy("Year", "Month", "Region") \
    .agg(
        count("*").alias("OrderCount"),
        sum("Quantity").alias("TotalQuantity"),
        round(sum("Amount"), 2).alias("TotalRevenue"),
        round(avg("Amount"), 2).alias("AvgOrderValue")
    ) \
    .orderBy("Year", "Month", "Region")

display(monthly_summary)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## 7. Working with OneLake Shortcuts
# 
# OneLake shortcuts allow you to reference data from external sources without copying it:
# 
# ### Types of Shortcuts:
# - **OneLake shortcuts**: Reference data in other OneLake locations
# - **ADLS Gen2 shortcuts**: Reference Azure Data Lake Storage
# - **S3 shortcuts**: Reference AWS S3 buckets
# 
# Shortcuts are created through the Fabric UI:
# 1. Navigate to your Lakehouse
# 2. Right-click on Files or Tables
# 3. Select "New shortcut"
# 4. Choose the source type and configure connection

# CELL ********************

# Once shortcuts are created, they appear as regular folders/tables
# Example: reading from a shortcut
df_shortcut = spark.read.format("delta").load("Tables/sales_performance")
display(df_shortcut.limit(10))

print("Shortcuts provide seamless access to external data without data movement")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## 8. Delta Lake Features
# 
# OneLake uses Delta Lake format which provides advanced capabilities:

# CELL ********************

delta_table_name = "sales_demo"

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Time Travel - Query historical versions of data
df_version = spark.read.format("delta") \
     .option("versionAsOf", 0) \
     .load(f"Tables/{delta_table_name}")
display(df_version)

print("Delta Lake supports time travel to query historical data versions")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Get table history
from delta.tables import DeltaTable

dt = DeltaTable.forPath(spark, f"Tables/{delta_table_name}")
history_df = dt.history()
display(history_df)

print("Delta tables maintain complete history of all operations")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## 9. Best Practices for OneLake
# 
# ### Storage Best Practices:
# 1. **Use Delta tables** for structured data
# 2. **Partition large tables** by frequently filtered columns (e.g., date)
# 3. **Use appropriate file sizes** (128MB-1GB per file)
# 4. **Leverage shortcuts** to avoid data duplication
# 
# ### Performance Best Practices:
# 1. **Use Z-ORDER** for multi-dimensional clustering
# 2. **Optimize file layout** with OPTIMIZE command
# 3. **Cache frequently accessed data**
# 4. **Use broadcast joins** for small dimension tables

# CELL ********************

# Example: Optimize Delta table
spark.sql(f"OPTIMIZE delta.`Tables/{delta_table_name}`")
spark.sql(f"OPTIMIZE delta.`Tables/{delta_table_name}` ZORDER BY (Region, Product)")

print("OPTIMIZE command compacts small files and improves query performance")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## 10. Data Governance in OneLake
# 
# OneLake integrates with Microsoft Purview for comprehensive data governance:
# 
# - **Data lineage**: Track data flow across your organization
# - **Data classification**: Automatically classify sensitive data
# - **Access control**: Manage permissions at workspace and item level
# - **Data discovery**: Find and understand available datasets
# 
# These features are configured through the Fabric portal and Purview governance center.

# MARKDOWN ********************

# ## Summary
# 
# In this notebook, we covered:
# - ✅ OneLake architecture and benefits
# - ✅ Reading and writing data in multiple formats
# - ✅ Creating and querying Delta tables
# - ✅ Data transformations and aggregations
# - ✅ OneLake shortcuts for external data
# - ✅ Delta Lake advanced features
# - ✅ Best practices for storage and performance
# - ✅ Data governance capabilities
# 
# ## Next Steps
# - Explore Real-Time Intelligence for streaming data
# - Learn about Power BI semantic models
# - Implement data pipelines for orchestration
# - Set up CI/CD for your Fabric solutions
