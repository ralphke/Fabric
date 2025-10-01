# Module 3: Data Engineering with Apache Spark

## Overview
Master data engineering on Microsoft Fabric using Apache Spark and Delta Lake.

## Duration
⏱️ Estimated time: 2 hours

## Learning Objectives
- Create and manage Lakehouses
- Work with Delta Lake tables
- Write Spark transformations
- Implement medallion architecture
- Prepare data for agent consumption

## Key Topics

### 1. Lakehouse Fundamentals
- Creating a Lakehouse
- Tables, files, and folders
- OneLake integration

### 2. Delta Lake
- ACID transactions
- Time travel
- Schema evolution

### 3. Spark Notebooks
- DataFrame operations
- SQL queries
- PySpark transformations

### 4. Data for Agents
- Structuring data for easy agent access
- Creating data views
- Metadata management

## Hands-On Exercises

### Exercise 1: Create a Lakehouse
Set up your first Lakehouse with sample data.

### Exercise 2: Data Transformations
Build bronze, silver, and gold layers.

### Exercise 3: Agent-Ready Data
Prepare data tables that agents can query.

## Sample Code

```python
# Create a Delta table that agents can query
from pyspark.sql import SparkSession

spark = SparkSession.builder.getOrCreate()

# Read raw data
df = spark.read.csv("Files/raw/sales.csv", header=True)

# Transform
df_clean = df.dropna().distinct()

# Write as Delta
df_clean.write.format("delta").mode("overwrite").saveAsTable("gold_sales")
```

## Assessment
- Build a complete medallion architecture
- Create agent-queryable tables
- Implement data quality checks

---

[← Back to Module 2](../02-data-factory/README.md) | [Next: Module 4 →](../04-data-science/README.md)
