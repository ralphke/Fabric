# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   }
# META }

# MARKDOWN ********************

# # Data Pipelines in Microsoft Fabric
# 
# This notebook demonstrates building and orchestrating data pipelines in Microsoft Fabric.
# 
# ## What are Data Pipelines?
# 
# Data Pipelines in Fabric provide:
# - **Visual orchestration** of data workflows
# - **150+ connectors** to various data sources
# - **Data transformation** using Copy, Dataflow, and Notebook activities
# - **Scheduling and triggers** for automation
# - **Monitoring and alerts** for reliability

# MARKDOWN ********************

# ## Prerequisites
# 
# To follow this notebook, you need:
# - A Microsoft Fabric workspace
# - Source data (can be files, databases, APIs)
# - Destination (Lakehouse, Warehouse, etc.)
# - Appropriate permissions

# MARKDOWN ********************

# ## 1. Pipeline Architecture Patterns
# 
# ### Common Pipeline Patterns:
# 1. **ETL (Extract, Transform, Load)**: Traditional data warehousing
# 2. **ELT (Extract, Load, Transform)**: Modern data lake approach
# 3. **Change Data Capture (CDC)**: Incremental updates
# 4. **Lambda Architecture**: Batch + Real-time processing
# 5. **Medallion Architecture**: Bronze, Silver, Gold layers

# CELL ********************

# Visualize pipeline patterns
pipeline_patterns = {
    "ETL Pattern": [
        "1. Extract data from sources",
        "2. Transform in staging area",
        "3. Load to target system",
        "Best for: Traditional DW, Small-medium data volumes"
    ],
    "ELT Pattern": [
        "1. Extract data from sources",
        "2. Load raw data to data lake",
        "3. Transform using compute engine",
        "Best for: Cloud platforms, Large data volumes"
    ],
    "Medallion Architecture": [
        "Bronze: Raw data ingestion (as-is)",
        "Silver: Cleaned and conformed data",
        "Gold: Business-level aggregations",
        "Best for: Data lakes, Multi-purpose analytics"
    ]
}

for pattern, steps in pipeline_patterns.items():
    print(f"\n{pattern}:")
    for step in steps:
        print(f"  {step}")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## 2. Creating Sample Source Data
# 
# Let's create sample data that we'll use in our pipeline examples:

# CELL ********************

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json

# Generate sample transaction data
np.random.seed(42)
n_records = 1000

transactions = pd.DataFrame({
    'transaction_id': [f'TXN{str(i).zfill(6)}' for i in range(1, n_records + 1)],
    'customer_id': [f'CUST{np.random.randint(1, 201):04d}' for _ in range(n_records)],
    'product_id': [f'PROD{np.random.randint(1, 51):03d}' for _ in range(n_records)],
    'transaction_date': [datetime.now() - timedelta(days=np.random.randint(0, 90)) for _ in range(n_records)],
    'quantity': np.random.randint(1, 11, n_records),
    'unit_price': np.round(np.random.uniform(10, 500, n_records), 2),
    'status': np.random.choice(['completed', 'pending', 'cancelled'], n_records, p=[0.85, 0.10, 0.05])
})

transactions['total_amount'] = (transactions['quantity'] * transactions['unit_price']).round(2)

print(f"Generated {len(transactions)} sample transactions")
print(f"Date range: {transactions['transaction_date'].min()} to {transactions['transaction_date'].max()}")
print(f"Total value: ${transactions['total_amount'].sum():,.2f}")
display(transactions.head())

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Save sample data to files (simulating source data)
import os

# Create temp directory for sample files
os.makedirs('/tmp/pipeline_data', exist_ok=True)

# Save as CSV
transactions.to_csv('/tmp/pipeline_data/transactions.csv', index=False)
print("✓ Saved transactions.csv")

# Save as JSON
transactions.to_json('/tmp/pipeline_data/transactions.json', orient='records', date_format='iso')
print("✓ Saved transactions.json")

# Save as Parquet
transactions.to_parquet('/tmp/pipeline_data/transactions.parquet', index=False)
print("✓ Saved transactions.parquet")

print("\nSample files created in /tmp/pipeline_data/")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## 3. Pipeline Activities
# 
# ### Key Activity Types:
# 1. **Copy Data**: Transfer data between sources and destinations
# 2. **Dataflow**: Transform data using Power Query
# 3. **Notebook**: Execute Python/Scala/R code
# 4. **Stored Procedure**: Run database procedures
# 5. **Script**: Execute custom scripts
# 6. **Control Flow**: If, ForEach, Until, Wait

# MARKDOWN ********************

# ## 4. Building a Pipeline (Conceptual)
# 
# ### Pipeline Creation Steps:
# 1. Navigate to Fabric workspace
# 2. Create New → Data Pipeline
# 3. Add activities from the toolbar
# 4. Configure activity properties
# 5. Connect activities (success/failure paths)
# 6. Set up parameters and variables
# 7. Test and debug
# 8. Schedule or trigger

# CELL ********************

# Example Pipeline Structure (JSON representation)
pipeline_definition = {
    "name": "Sales_Data_Pipeline",
    "properties": {
        "description": "Daily sales data processing pipeline",
        "activities": [
            {
                "name": "Copy_CSV_to_Bronze",
                "type": "Copy",
                "description": "Copy raw data to Bronze layer",
                "source": {
                    "type": "DelimitedText",
                    "location": "Files/source/transactions.csv"
                },
                "sink": {
                    "type": "DeltaTable",
                    "location": "Tables/Bronze_Transactions"
                }
            },
            {
                "name": "Transform_Bronze_to_Silver",
                "type": "Notebook",
                "description": "Clean and validate data",
                "notebookPath": "Notebooks/Transform_to_Silver",
                "dependsOn": ["Copy_CSV_to_Bronze"]
            },
            {
                "name": "Aggregate_Silver_to_Gold",
                "type": "Notebook",
                "description": "Create business aggregations",
                "notebookPath": "Notebooks/Aggregate_to_Gold",
                "dependsOn": ["Transform_Bronze_to_Silver"]
            },
            {
                "name": "Refresh_Semantic_Model",
                "type": "ExecuteDataflow",
                "description": "Refresh Power BI semantic model",
                "dependsOn": ["Aggregate_Silver_to_Gold"]
            }
        ],
        "parameters": {
            "ProcessDate": {
                "type": "String",
                "defaultValue": "@utcnow()"
            },
            "SourcePath": {
                "type": "String",
                "defaultValue": "Files/source/"
            }
        }
    }
}

print("Sample Pipeline Definition:")
print(json.dumps(pipeline_definition, indent=2))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## 5. Data Transformation Examples
# 
# Let's simulate the transformations that would happen in pipeline activities:

# CELL ********************

# Bronze Layer: Raw data ingestion (minimal processing)
def bronze_layer(df):
    """Bronze layer: Ingest raw data with metadata"""
    df_bronze = df.copy()
    df_bronze['_ingestion_timestamp'] = datetime.now()
    df_bronze['_source_file'] = 'transactions.csv'
    return df_bronze

bronze_transactions = bronze_layer(transactions)
print("Bronze Layer:")
print(f"  Records: {len(bronze_transactions)}")
print(f"  Columns: {list(bronze_transactions.columns)}")
display(bronze_transactions.head(3))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Silver Layer: Cleaned and validated data
def silver_layer(df_bronze):
    """Silver layer: Clean, validate, and standardize"""
    df_silver = df_bronze.copy()
    
    # Data quality checks
    # 1. Remove cancelled transactions
    df_silver = df_silver[df_silver['status'] != 'cancelled']
    
    # 2. Remove duplicates
    df_silver = df_silver.drop_duplicates(subset=['transaction_id'])
    
    # 3. Handle invalid values
    df_silver = df_silver[df_silver['quantity'] > 0]
    df_silver = df_silver[df_silver['unit_price'] > 0]
    
    # 4. Add calculated fields
    df_silver['transaction_year'] = df_silver['transaction_date'].dt.year
    df_silver['transaction_month'] = df_silver['transaction_date'].dt.month
    df_silver['transaction_quarter'] = df_silver['transaction_date'].dt.quarter
    
    # 5. Add data quality flag
    df_silver['data_quality_score'] = 100  # Could be more complex
    df_silver['_processing_timestamp'] = datetime.now()
    
    return df_silver

silver_transactions = silver_layer(bronze_transactions)
print("\nSilver Layer:")
print(f"  Records: {len(silver_transactions)} (removed {len(bronze_transactions) - len(silver_transactions)} invalid records)")
print(f"  Quality Score: {silver_transactions['data_quality_score'].mean():.1f}%")
display(silver_transactions.head(3))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Gold Layer: Business-level aggregations
def gold_layer(df_silver):
    """Gold layer: Create business aggregations"""
    
    # Daily aggregations
    gold_daily = df_silver.groupby(
        df_silver['transaction_date'].dt.date
    ).agg({
        'transaction_id': 'count',
        'total_amount': ['sum', 'mean'],
        'quantity': 'sum',
        'customer_id': 'nunique'
    }).round(2)
    
    gold_daily.columns = ['transaction_count', 'total_revenue', 'avg_order_value', 'total_units', 'unique_customers']
    gold_daily = gold_daily.reset_index()
    gold_daily.columns = ['date', 'transaction_count', 'total_revenue', 'avg_order_value', 'total_units', 'unique_customers']
    
    # Product aggregations
    gold_product = df_silver.groupby('product_id').agg({
        'transaction_id': 'count',
        'quantity': 'sum',
        'total_amount': 'sum'
    }).round(2)
    
    gold_product.columns = ['order_count', 'units_sold', 'revenue']
    gold_product = gold_product.sort_values('revenue', ascending=False).reset_index()
    
    # Customer aggregations
    gold_customer = df_silver.groupby('customer_id').agg({
        'transaction_id': 'count',
        'total_amount': ['sum', 'mean'],
        'transaction_date': ['min', 'max']
    }).round(2)
    
    gold_customer.columns = ['purchase_count', 'total_spent', 'avg_order_value', 'first_purchase', 'last_purchase']
    gold_customer = gold_customer.reset_index()
    
    return {
        'daily_metrics': gold_daily,
        'product_metrics': gold_product,
        'customer_metrics': gold_customer
    }

gold_tables = gold_layer(silver_transactions)

print("\nGold Layer - Daily Metrics:")
display(gold_tables['daily_metrics'].tail(10))

print("\nGold Layer - Top Products:")
display(gold_tables['product_metrics'].head(10))

print("\nGold Layer - Top Customers:")
top_customers = gold_tables['customer_metrics'].sort_values('total_spent', ascending=False).head(10)
display(top_customers)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## 6. Incremental Loading Pattern
# 
# Incremental loading processes only new or changed data:

# CELL ********************

def incremental_load(df_source, df_target, key_column, timestamp_column):
    """
    Implement incremental load logic
    
    Args:
        df_source: New data from source
        df_target: Existing data in target
        key_column: Unique identifier column
        timestamp_column: Column to track changes
    """
    if df_target is None or len(df_target) == 0:
        # First load - load all data
        print("Initial load: Loading all records")
        return df_source, len(df_source), 0, 0
    
    # Get max timestamp from target
    max_timestamp = df_target[timestamp_column].max()
    
    # Get new records
    df_new = df_source[df_source[timestamp_column] > max_timestamp]
    
    # Get updated records (exists in target but newer in source)
    existing_keys = set(df_target[key_column])
    source_keys = set(df_source[key_column])
    
    updated_keys = existing_keys.intersection(source_keys)
    df_updates = df_source[
        (df_source[key_column].isin(updated_keys)) & 
        (df_source[timestamp_column] > max_timestamp)
    ]
    
    # Combine new and updated records
    df_incremental = pd.concat([df_new, df_updates]).drop_duplicates(subset=[key_column])
    
    print(f"Incremental load:")
    print(f"  New records: {len(df_new)}")
    print(f"  Updated records: {len(df_updates)}")
    print(f"  Total to process: {len(df_incremental)}")
    
    return df_incremental, len(df_new), len(df_updates), len(df_target)

# Simulate incremental load
# First run - empty target
print("\n=== First Pipeline Run ===")
incremental_data, new_count, updated_count, existing_count = incremental_load(
    transactions, None, 'transaction_id', 'transaction_date'
)

# Second run - with new data
print("\n=== Second Pipeline Run (with new data) ===")
new_transactions = transactions.sample(n=50).copy()
new_transactions['transaction_date'] = datetime.now()

incremental_data, new_count, updated_count, existing_count = incremental_load(
    new_transactions, transactions, 'transaction_id', 'transaction_date'
)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## 7. Error Handling and Logging
# 
# Proper error handling is crucial for production pipelines:

# CELL ********************

import logging
from datetime import datetime

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('DataPipeline')

class PipelineMonitor:
    """Monitor pipeline execution"""
    
    def __init__(self, pipeline_name):
        self.pipeline_name = pipeline_name
        self.start_time = None
        self.metrics = {
            'records_processed': 0,
            'records_failed': 0,
            'errors': []
        }
    
    def start(self):
        """Start pipeline monitoring"""
        self.start_time = datetime.now()
        logger.info(f"Pipeline '{self.pipeline_name}' started at {self.start_time}")
    
    def log_activity(self, activity_name, status, records=0):
        """Log activity execution"""
        logger.info(f"Activity '{activity_name}': {status} - {records} records")
        if status == 'success':
            self.metrics['records_processed'] += records
        else:
            self.metrics['records_failed'] += records
    
    def log_error(self, activity_name, error):
        """Log error"""
        error_msg = f"{activity_name}: {str(error)}"
        logger.error(error_msg)
        self.metrics['errors'].append(error_msg)
    
    def complete(self):
        """Complete pipeline monitoring"""
        duration = (datetime.now() - self.start_time).total_seconds()
        logger.info(f"Pipeline '{self.pipeline_name}' completed in {duration:.2f} seconds")
        logger.info(f"Metrics: {self.metrics}")
        return self.metrics

# Example usage
monitor = PipelineMonitor("Sales_ETL_Pipeline")
monitor.start()

try:
    # Simulate activities
    monitor.log_activity("Copy_to_Bronze", "success", len(transactions))
    monitor.log_activity("Transform_to_Silver", "success", len(silver_transactions))
    monitor.log_activity("Aggregate_to_Gold", "success", len(gold_tables['daily_metrics']))
except Exception as e:
    monitor.log_error("Pipeline_Execution", e)
finally:
    final_metrics = monitor.complete()
    print("\nPipeline Metrics:")
    print(json.dumps(final_metrics, indent=2))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## 8. Pipeline Parameters and Variables
# 
# Parameters make pipelines flexible and reusable:

# CELL ********************

# Example pipeline parameters
pipeline_parameters = {
    # Static parameters (set at pipeline creation)
    "source_container": "raw-data",
    "target_lakehouse": "enterprise_lakehouse",
    "email_notifications": "data-team@company.com",
    
    # Dynamic parameters (can be passed at runtime)
    "process_date": "@formatDateTime(utcnow(), 'yyyy-MM-dd')",
    "batch_size": 10000,
    "retry_count": 3,
    
    # Environment-specific parameters
    "environment": "production",
    "logging_level": "INFO"
}

# Pipeline variables (set during execution)
pipeline_variables = {
    "records_processed": 0,
    "last_success_time": None,
    "retry_attempt": 0,
    "error_message": ""
}

print("Pipeline Parameters:")
print(json.dumps(pipeline_parameters, indent=2))

print("\nPipeline Variables:")
print(json.dumps(pipeline_variables, indent=2))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## 9. Scheduling and Triggers
# 
# ### Trigger Types:
# 1. **Schedule Trigger**: Run on a schedule (cron expression)
# 2. **Event Trigger**: Run when a file arrives or event occurs
# 3. **Manual Trigger**: Run on-demand
# 4. **Tumbling Window**: Fixed-size, non-overlapping time windows

# CELL ********************

# Example trigger configurations
trigger_examples = {
    "daily_schedule": {
        "type": "ScheduleTrigger",
        "properties": {
            "recurrence": {
                "frequency": "Day",
                "interval": 1,
                "startTime": "2024-01-01T02:00:00Z",
                "timeZone": "UTC"
            }
        }
    },
    "hourly_schedule": {
        "type": "ScheduleTrigger",
        "properties": {
            "recurrence": {
                "frequency": "Hour",
                "interval": 1
            }
        }
    },
    "file_arrival": {
        "type": "BlobEventsTrigger",
        "properties": {
            "events": ["Microsoft.Storage.BlobCreated"],
            "scope": "/subscriptions/{subscription}/resourceGroups/{rg}/providers/Microsoft.Storage/storageAccounts/{account}",
            "blobPathBeginsWith": "/raw-data/transactions/",
            "blobPathEndsWith": ".csv"
        }
    },
    "tumbling_window": {
        "type": "TumblingWindowTrigger",
        "properties": {
            "frequency": "Hour",
            "interval": 1,
            "startTime": "2024-01-01T00:00:00Z",
            "delay": "00:15:00",  # 15-minute delay
            "maxConcurrency": 1,
            "retryPolicy": {
                "count": 3,
                "intervalInSeconds": 30
            }
        }
    }
}

print("Trigger Configuration Examples:")
for trigger_name, config in trigger_examples.items():
    print(f"\n{trigger_name}:")
    print(json.dumps(config, indent=2))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## 10. Best Practices
# 
# ### Design Principles:
# 1. **Idempotency**: Pipelines should produce same result when run multiple times
# 2. **Modularity**: Break complex logic into reusable components
# 3. **Error Handling**: Implement retry logic and failure notifications
# 4. **Logging**: Comprehensive logging for debugging
# 5. **Testing**: Test with sample data before production
# 
# ### Performance:
# 1. **Parallel Processing**: Use ForEach activities with concurrency
# 2. **Partitioning**: Process data in chunks
# 3. **Compression**: Use compressed formats (Parquet, Avro)
# 4. **Incremental Loads**: Process only new/changed data
# 
# ### Monitoring:
# 1. **Pipeline Runs**: Monitor success/failure rates
# 2. **Duration Tracking**: Alert on long-running pipelines
# 3. **Data Quality**: Implement quality checks
# 4. **Alerting**: Configure notifications for failures

# CELL ********************

# Data quality checks example
def data_quality_checks(df, table_name):
    """Run data quality validations"""
    checks = []
    
    # Check 1: No null values in key columns
    key_columns = ['transaction_id', 'customer_id', 'product_id']
    for col in key_columns:
        null_count = df[col].isnull().sum()
        checks.append({
            'check': f'No nulls in {col}',
            'passed': null_count == 0,
            'details': f'{null_count} null values found'
        })
    
    # Check 2: Positive values
    checks.append({
        'check': 'All quantities positive',
        'passed': (df['quantity'] > 0).all(),
        'details': f"{(df['quantity'] <= 0).sum()} negative/zero values"
    })
    
    # Check 3: Reasonable date range
    days_old = (datetime.now() - df['transaction_date'].min()).days
    checks.append({
        'check': 'Date range reasonable',
        'passed': days_old <= 365,
        'details': f'Oldest record: {days_old} days'
    })
    
    # Check 4: No duplicates
    duplicate_count = df.duplicated(subset=['transaction_id']).sum()
    checks.append({
        'check': 'No duplicate IDs',
        'passed': duplicate_count == 0,
        'details': f'{duplicate_count} duplicates found'
    })
    
    # Summary
    passed = sum(1 for c in checks if c['passed'])
    total = len(checks)
    
    print(f"\nData Quality Report - {table_name}")
    print(f"{'='*60}")
    for check in checks:
        status = '✓' if check['passed'] else '✗'
        print(f"{status} {check['check']}: {check['details']}")
    print(f"{'='*60}")
    print(f"Passed: {passed}/{total} checks ({passed/total*100:.1f}%)")
    
    return passed == total

# Run quality checks
quality_passed = data_quality_checks(transactions, 'Transactions')

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## Summary
# 
# In this notebook, we covered:
# - ✅ Pipeline architecture patterns (ETL, ELT, Medallion)
# - ✅ Key pipeline activities and components
# - ✅ Building multi-layer data transformations
# - ✅ Implementing incremental loading
# - ✅ Error handling and monitoring
# - ✅ Pipeline parameters and variables
# - ✅ Scheduling and trigger configuration
# - ✅ Data quality validation
# - ✅ Best practices for production pipelines
# 
# ## Next Steps
# - Implement CI/CD for pipelines
# - Integrate with DevOps practices
# - Build real-time streaming pipelines
# - Explore advanced orchestration patterns
