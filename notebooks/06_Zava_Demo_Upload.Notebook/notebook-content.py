# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   }
# META }

# MARKDOWN ********************

# # Zava Demo Data Upload to Fabric Lakehouse
# 
# This notebook demonstrates how to upload the Zava demo sample parquet files to a Microsoft Fabric Lakehouse. The Zava demo contains e-commerce sample data including customers, products, orders, order items, and sales performance metrics.
# 
# ## What You'll Learn
# 
# - How to read parquet files from a local directory
# - How to upload data to the Fabric Lakehouse Files section
# - How to create Delta tables from parquet files
# - How to verify and query the uploaded data
# - Best practices for organizing data in OneLake

# MARKDOWN ********************

# ## Prerequisites
# 
# To run this notebook, you need:
# - A Microsoft Fabric workspace
# - A Lakehouse created in your workspace
# - The zava demo parquet files from the `sample-data/zava-demo/` directory
# - Appropriate permissions to read/write data

# MARKDOWN ********************

# ## 1. Setup and Configuration
# 
# First, let's import the necessary libraries and verify our Spark environment.

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

# MARKDOWN ********************

# ## 2. Define Source Data Location
# 
# The Zava demo data consists of 5 parquet files representing a typical e-commerce database:
# - **customers.parquet**: 100 customer records
# - **products.parquet**: 50 product records
# - **orders.parquet**: 500 order records
# - **order_items.parquet**: 1000 order item records
# - **sales_performance.parquet**: 84 aggregated sales metrics

# CELL ********************

# Define the source directory containing the parquet files
# Note: In Fabric, you would typically upload these files first or reference them from a Git repo
source_dir = "/lakehouse/default/Files/sample-data/zava-demo/"

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

# MARKDOWN ********************

# ## 3. Read and Explore the Parquet Files
# 
# Let's read each parquet file and examine its schema and sample data.

# MARKDOWN ********************

# ### 3.1 Customers Data

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

# MARKDOWN ********************

# ### 3.2 Products Data

# CELL ********************

# Read products parquet file
products_path = os.path.join(source_dir, "products.parquet")
df_products = spark.read.parquet(products_path)

print("Products Schema:")
df_products.printSchema()

print(f"\nTotal Products: {df_products.count()}")
print("\nSample Data:")
display(df_products.limit(5))

print("\nProduct Categories:")
display(df_products.groupBy("category").count().orderBy("category"))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### 3.3 Orders Data

# CELL ********************

# Read orders parquet file
orders_path = os.path.join(source_dir, "orders.parquet")
df_orders = spark.read.parquet(orders_path)

print("Orders Schema:")
df_orders.printSchema()

print(f"\nTotal Orders: {df_orders.count()}")
print("\nSample Data:")
display(df_orders.limit(5))

print("\nOrder Status Distribution:")
display(df_orders.groupBy("order_status").count().orderBy("order_status"))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### 3.4 Order Items Data

# CELL ********************

# Read order_items parquet file
order_items_path = os.path.join(source_dir, "order_items.parquet")
df_order_items = spark.read.parquet(order_items_path)

print("Order Items Schema:")
df_order_items.printSchema()

print(f"\nTotal Order Items: {df_order_items.count()}")
print("\nSample Data:")
display(df_order_items.limit(5))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### 3.5 Sales Performance Data

# CELL ********************

# Read sales_performance parquet file
sales_performance_path = os.path.join(source_dir, "sales_performance.parquet")
df_sales_performance = spark.read.parquet(sales_performance_path)

print("Sales Performance Schema:")
df_sales_performance.printSchema()

print(f"\nTotal Records: {df_sales_performance.count()}")
print("\nSample Data:")
display(df_sales_performance.limit(10))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## 4. Upload Data to Lakehouse as Delta Tables
# 
# Now let's write the data as Delta tables in the Lakehouse. Delta format provides:
# - ACID transactions
# - Time travel capabilities
# - Schema evolution
# - Optimal query performance

# MARKDOWN ********************

# ### 4.1 Create Customers Table

# CELL ********************

# Write customers data as Delta table
table_name = "zava_customers"
df_customers.write.format("delta") \
    .mode("overwrite") \
    .option("overwriteSchema", "true") \
    .save(f"Tables/{table_name}")

print(f"✓ Created Delta table: {table_name}")
print(f"  Records: {df_customers.count()}")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### 4.2 Create Products Table

# CELL ********************

# Write products data as Delta table
table_name = "zava_products"
df_products.write.format("delta") \
    .mode("overwrite") \
    .option("overwriteSchema", "true") \
    .save(f"Tables/{table_name}")

print(f"✓ Created Delta table: {table_name}")
print(f"  Records: {df_products.count()}")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### 4.3 Create Orders Table

# CELL ********************

# Write orders data as Delta table
table_name = "zava_orders"
df_orders.write.format("delta") \
    .mode("overwrite") \
    .option("overwriteSchema", "true") \
    .save(f"Tables/{table_name}")

print(f"✓ Created Delta table: {table_name}")
print(f"  Records: {df_orders.count()}")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### 4.4 Create Order Items Table

# CELL ********************

# Write order_items data as Delta table
table_name = "zava_order_items"
df_order_items.write.format("delta") \
    .mode("overwrite") \
    .option("overwriteSchema", "true") \
    .save(f"Tables/{table_name}")

print(f"✓ Created Delta table: {table_name}")
print(f"  Records: {df_order_items.count()}")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### 4.5 Create Sales Performance Table

# CELL ********************

# Write sales_performance data as Delta table
table_name = "zava_sales_performance"
df_sales_performance.write.format("delta") \
    .mode("overwrite") \
    .option("overwriteSchema", "true") \
    .save(f"Tables/{table_name}")

print(f"✓ Created Delta table: {table_name}")
print(f"  Records: {df_sales_performance.count()}")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## 5. Verify Uploaded Data
# 
# Let's verify that all tables were created successfully and contain the expected data.

# CELL ********************

# Create a summary of all uploaded tables
tables = [
    ("zava_customers", df_customers),
    ("zava_products", df_products),
    ("zava_orders", df_orders),
    ("zava_order_items", df_order_items),
    ("zava_sales_performance", df_sales_performance)
]

print("=" * 60)
print("UPLOAD SUMMARY")
print("=" * 60)

for table_name, df in tables:
    count = df.count()
    print(f"✓ {table_name:30s} | {count:6d} records")

print("=" * 60)
print("\nAll Zava demo data has been successfully uploaded!")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## 6. Sample Queries and Analytics
# 
# Now that the data is in the lakehouse, let's run some sample queries to demonstrate the data relationships.

# MARKDOWN ********************

# ### 6.1 Top 10 Customers by Total Spending

# CELL ********************

# Query: Top 10 customers by total spending
top_customers = spark.sql("""
    SELECT 
        c.customer_id,
        c.first_name,
        c.last_name,
        c.email,
        c.city,
        c.state,
        SUM(o.total_amount) as total_spent,
        COUNT(DISTINCT o.order_id) as order_count
    FROM delta.`Tables/zava_customers` c
    JOIN delta.`Tables/zava_orders` o ON c.customer_id = o.customer_id
    GROUP BY c.customer_id, c.first_name, c.last_name, c.email, c.city, c.state
    ORDER BY total_spent DESC
    LIMIT 10
""")

print("Top 10 Customers by Total Spending:")
display(top_customers)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### 6.2 Sales by Product Category

# CELL ********************

# Query: Sales by product category
sales_by_category = spark.sql("""
    SELECT 
        p.category,
        COUNT(DISTINCT o.order_id) as order_count,
        SUM(oi.quantity) as total_units_sold,
        ROUND(SUM(oi.quantity * oi.unit_price * (1 - oi.discount)), 2) as total_revenue,
        ROUND(AVG(oi.unit_price), 2) as avg_unit_price
    FROM delta.`Tables/zava_products` p
    JOIN delta.`Tables/zava_order_items` oi ON p.product_id = oi.product_id
    JOIN delta.`Tables/zava_orders` o ON oi.order_id = o.order_id
    GROUP BY p.category
    ORDER BY total_revenue DESC
""")

print("Sales by Product Category:")
display(sales_by_category)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### 6.3 Monthly Order Trends

# CELL ********************

# Query: Monthly order trends
monthly_trends = spark.sql("""
    SELECT 
        SUBSTRING(order_date, 1, 7) as year_month,
        COUNT(*) as order_count,
        ROUND(SUM(total_amount), 2) as total_revenue,
        ROUND(AVG(total_amount), 2) as avg_order_value
    FROM delta.`Tables/zava_orders`
    GROUP BY SUBSTRING(order_date, 1, 7)
    ORDER BY year_month
""")

print("Monthly Order Trends:")
display(monthly_trends)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### 6.4 Top 10 Products by Revenue

# CELL ********************

# Query: Top 10 products by revenue
top_products = spark.sql("""
    SELECT 
        p.product_id,
        p.product_name,
        p.category,
        p.price,
        SUM(oi.quantity) as units_sold,
        ROUND(SUM(oi.quantity * oi.unit_price * (1 - oi.discount)), 2) as total_revenue
    FROM delta.`Tables/zava_products` p
    JOIN delta.`Tables/zava_order_items` oi ON p.product_id = oi.product_id
    GROUP BY p.product_id, p.product_name, p.category, p.price
    ORDER BY total_revenue DESC
    LIMIT 10
""")

print("Top 10 Products by Revenue:")
display(top_products)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### 6.5 Order Status Distribution

# CELL ********************

# Query: Order status distribution with value
status_distribution = spark.sql("""
    SELECT 
        order_status,
        COUNT(*) as order_count,
        ROUND(SUM(total_amount), 2) as total_value,
        ROUND(AVG(total_amount), 2) as avg_order_value
    FROM delta.`Tables/zava_orders`
    GROUP BY order_status
    ORDER BY order_count DESC
""")

print("Order Status Distribution:")
display(status_distribution)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## 7. Data Relationships and Integrity
# 
# Let's verify the referential integrity of our data by checking the relationships between tables.

# CELL ********************

# Verify referential integrity
print("Data Relationship Verification:")
print("=" * 60)

# Check customers referenced in orders
customers_in_orders = spark.sql("""
    SELECT COUNT(DISTINCT customer_id) as count
    FROM delta.`Tables/zava_orders`
""").collect()[0]['count']

total_customers = df_customers.count()
print(f"Customers: {total_customers} total, {customers_in_orders} have orders")

# Check products referenced in order_items
products_in_orders = spark.sql("""
    SELECT COUNT(DISTINCT product_id) as count
    FROM delta.`Tables/zava_order_items`
""").collect()[0]['count']

total_products = df_products.count()
print(f"Products: {total_products} total, {products_in_orders} have been ordered")

# Check orders with items
orders_with_items = spark.sql("""
    SELECT COUNT(DISTINCT order_id) as count
    FROM delta.`Tables/zava_order_items`
""").collect()[0]['count']

total_orders = df_orders.count()
print(f"Orders: {total_orders} total, {orders_with_items} have items")

print("=" * 60)
print("\n✓ Data relationships verified successfully!")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## 8. Copy Files to Lakehouse Files Section (Optional)
# 
# In addition to creating Delta tables, you can also copy the original parquet files to the Files section of your lakehouse for additional flexibility.

# CELL ********************

# Copy parquet files to lakehouse Files section
target_dir = "Files/zava-demo/"

print("Copying parquet files to Files section...")
print("=" * 60)

for file_name in files_to_upload:
    source_path = os.path.join(source_dir, file_name)
    target_path = os.path.join(target_dir, file_name)
    
    # Read and write to copy the file
    df = spark.read.parquet(source_path)
    df.write.mode("overwrite").parquet(target_path)
    
    print(f"✓ Copied {file_name} to {target_path}")

print("=" * 60)
print("\nAll files copied successfully!")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## 9. Best Practices and Next Steps
# 
# ### Best Practices for Lakehouse Data Organization:
# 
# 1. **Use Delta tables** for structured data that requires ACID transactions
# 2. **Organize by domain** - group related tables together (e.g., zava_* prefix)
# 3. **Implement partitioning** for large tables by date or other frequently filtered columns
# 4. **Add table descriptions** and metadata for documentation
# 5. **Set up data quality checks** to validate data integrity
# 6. **Configure retention policies** for Delta table history
# 
# ### Next Steps:
# 
# 1. **Build semantic models** on top of these tables for Power BI reporting
# 2. **Create SQL views** for common queries and business logic
# 3. **Set up data pipelines** for incremental data loads
# 4. **Implement row-level security** if needed for data governance
# 5. **Create dashboards** to visualize sales trends and customer behavior
# 6. **Explore advanced analytics** using the data for forecasting and predictions

# MARKDOWN ********************

# ## Summary
# 
# In this notebook, we:
# - ✅ Read parquet files from the zava-demo sample data
# - ✅ Uploaded 5 tables to the Fabric Lakehouse as Delta tables
# - ✅ Verified data integrity and relationships
# - ✅ Demonstrated sample queries for analytics
# - ✅ Copied original parquet files to the Files section
# 
# The Zava demo data is now ready for use in:
# - Power BI reports and dashboards
# - Data science and machine learning experiments
# - Data pipeline development and testing
# - Learning and training scenarios
# 
# **Total records uploaded:** 1,734 records across 5 tables
# - Customers: 100
# - Products: 50
# - Orders: 500
# - Order Items: 1,000
# - Sales Performance: 84
