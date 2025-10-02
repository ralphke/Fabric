# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   }
# META }

# MARKDOWN ********************

# # Real-Time Intelligence in Microsoft Fabric
# 
# This notebook demonstrates the Real-Time Intelligence capabilities in Microsoft Fabric, including:
# - Event streams
# - Real-time analytics with KQL
# - Streaming data ingestion
# - Real-time dashboards
# 
# ## What is Real-Time Intelligence?
# 
# Real-Time Intelligence in Fabric provides:
# - **Event Streams**: Capture, transform, and route streaming data
# - **KQL Database**: Fast analytics on streaming and historical data
# - **Real-Time Dashboards**: Visualize streaming data with minimal latency
# - **Activator**: Trigger actions based on data patterns and conditions

# MARKDOWN ********************

# ## Prerequisites
# 
# To run this notebook, you need:
# - A Microsoft Fabric workspace with Real-Time Intelligence enabled
# - A KQL Database (optional)
# - An Event Stream (optional)
# - Appropriate permissions

# MARKDOWN ********************

# ## 1. Simulating Streaming Data
# 
# Let's create a simulator that generates real-time IoT sensor data:

# CELL ********************

import json
import random
import time
from datetime import datetime
import pandas as pd

# Define sensor locations
sensor_locations = [
    {"id": "sensor_001", "location": "Building A - Floor 1", "type": "temperature"},
    {"id": "sensor_002", "location": "Building A - Floor 2", "type": "temperature"},
    {"id": "sensor_003", "location": "Building B - Floor 1", "type": "humidity"},
    {"id": "sensor_004", "location": "Building B - Floor 2", "type": "humidity"},
    {"id": "sensor_005", "location": "Warehouse", "type": "pressure"},
]

def generate_sensor_reading(sensor):
    """Generate a single sensor reading"""
    base_values = {
        "temperature": 22.0,
        "humidity": 45.0,
        "pressure": 1013.25
    }
    
    variation = random.uniform(-5, 5)
    value = base_values.get(sensor["type"], 0) + variation
    
    return {
        "sensor_id": sensor["id"],
        "location": sensor["location"],
        "type": sensor["type"],
        "value": round(value, 2),
        "timestamp": datetime.utcnow().isoformat(),
        "status": "normal" if abs(variation) < 4 else "warning"
    }

# Generate sample batch of readings
sample_readings = [generate_sensor_reading(sensor) for sensor in sensor_locations for _ in range(5)]
df_readings = pd.DataFrame(sample_readings)
print("Sample Sensor Readings:")
display(df_readings.head(10))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## 2. Working with Event Streams
# 
# Event Streams in Fabric allow you to:
# - Ingest data from multiple sources (IoT Hub, Event Hub, Kafka, etc.)
# - Transform data in real-time
# - Route data to multiple destinations
# 
# ### Creating an Event Stream (via Fabric UI):
# 1. Navigate to your workspace
# 2. Click "New" → "Event Stream"
# 3. Configure source connection
# 4. Add transformations if needed
# 5. Configure destination (KQL Database, Lakehouse, etc.)

# CELL ********************

# Example: Publishing data to Event Stream using Azure Event Hub SDK
# Note: This requires azure-eventhub package and proper credentials

# from azure.eventhub import EventHubProducerClient, EventData
# 
# connection_string = "YOUR_EVENT_HUB_CONNECTION_STRING"
# event_hub_name = "YOUR_EVENT_HUB_NAME"
# 
# producer = EventHubProducerClient.from_connection_string(
#     connection_string, 
#     eventhub_name=event_hub_name
# )
# 
# # Send batch of events
# event_data_batch = producer.create_batch()
# for reading in sample_readings:
#     event_data_batch.add(EventData(json.dumps(reading)))
# 
# producer.send_batch(event_data_batch)
# producer.close()

print("Event Stream connections are typically configured through the Fabric portal")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## 3. KQL (Kusto Query Language) Basics
# 
# KQL is the query language for Real-Time Intelligence. Let's explore key concepts:

# CELL ********************

# Convert our sample data to demonstrate KQL-like operations in Python
from pyspark.sql import SparkSession
from pyspark.sql.functions import *

# Create Spark DataFrame
df_spark = spark.createDataFrame(df_readings)

# Display schema
print("Data Schema:")
df_spark.printSchema()

# Basic filtering (equivalent to KQL 'where')
print("\nWarning readings only:")
df_warnings = df_spark.filter(col("status") == "warning")
display(df_warnings)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## 4. Common KQL Query Patterns
# 
# Here are common query patterns you'll use in KQL Database:

# CELL ********************

# KQL Query Examples (to be run in KQL Database)
kql_examples = """
-- Example 1: Basic filtering and projection
SensorReadings
| where timestamp > ago(1h)
| where status == 'warning'
| project sensor_id, location, value, timestamp

-- Example 2: Aggregation over time windows
SensorReadings
| where timestamp > ago(24h)
| summarize 
    avg_value = avg(value),
    max_value = max(value),
    min_value = min(value),
    reading_count = count()
  by sensor_id, bin(timestamp, 1h)
| order by timestamp desc

-- Example 3: Anomaly detection
SensorReadings
| where timestamp > ago(7d)
| make-series avg_value = avg(value) on timestamp step 1h by sensor_id
| extend anomalies = series_decompose_anomalies(avg_value, 1.5)

-- Example 4: Windowed aggregation
SensorReadings
| where timestamp > ago(1d)
| partition by sensor_id
  (
    order by timestamp asc
    | extend moving_avg = row_avg(value, prev(value), prev(value, 2))
  )

-- Example 5: Join with dimension table
SensorReadings
| where timestamp > ago(1h)
| join kind=inner SensorMetadata on $left.sensor_id == $right.sensor_id
| project sensor_id, location, type, value, threshold = metadata_threshold
| where value > threshold
"""

print("Common KQL Query Patterns:")
print(kql_examples)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## 5. Real-Time Analytics Scenarios
# 
# Let's implement some common real-time analytics patterns:

# CELL ********************

# Scenario 1: Alert on threshold violations
def check_thresholds(df):
    """Check for threshold violations"""
    thresholds = {
        "temperature": {"min": 18, "max": 26},
        "humidity": {"min": 30, "max": 60},
        "pressure": {"min": 1000, "max": 1025}
    }
    
    alerts = []
    for _, row in df.iterrows():
        threshold = thresholds.get(row['type'], {})
        if threshold:
            if row['value'] < threshold['min'] or row['value'] > threshold['max']:
                alerts.append({
                    'sensor_id': row['sensor_id'],
                    'location': row['location'],
                    'type': row['type'],
                    'value': row['value'],
                    'threshold_min': threshold['min'],
                    'threshold_max': threshold['max'],
                    'timestamp': row['timestamp']
                })
    
    return pd.DataFrame(alerts)

alerts_df = check_thresholds(df_readings)
if not alerts_df.empty:
    print(f"Found {len(alerts_df)} threshold violations:")
    display(alerts_df)
else:
    print("No threshold violations detected")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Scenario 2: Calculate moving averages
def calculate_moving_average(df, window_size=3):
    """Calculate moving average for sensor readings"""
    result = df.sort_values('timestamp').copy()
    result['moving_avg'] = result.groupby('sensor_id')['value'].transform(
        lambda x: x.rolling(window=window_size, min_periods=1).mean()
    )
    return result

df_with_ma = calculate_moving_average(df_readings, window_size=3)
print("\nReadings with Moving Average:")
display(df_with_ma[['sensor_id', 'location', 'value', 'moving_avg', 'timestamp']].head(15))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Scenario 3: Aggregate by location and time window
df_readings_copy = df_readings.copy()
df_readings_copy['timestamp'] = pd.to_datetime(df_readings_copy['timestamp'])
df_readings_copy['time_bucket'] = df_readings_copy['timestamp'].dt.floor('5min')

aggregated = df_readings_copy.groupby(['location', 'type', 'time_bucket']).agg({
    'value': ['mean', 'min', 'max', 'std'],
    'sensor_id': 'count'
}).round(2)

aggregated.columns = ['avg_value', 'min_value', 'max_value', 'std_value', 'reading_count']
print("\nAggregated readings by location and time:")
display(aggregated.head(10))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## 6. Setting Up Real-Time Dashboards
# 
# Real-Time Dashboards in Fabric provide:
# - Live data visualization
# - Auto-refresh capabilities
# - KQL-based queries
# - Multiple visualization types
# 
# ### Creating a Real-Time Dashboard:
# 1. Navigate to your workspace
# 2. Click "New" → "Real-Time Dashboard"
# 3. Add tiles with KQL queries
# 4. Configure refresh intervals
# 5. Set up parameters for interactivity

# CELL ********************

# Sample KQL queries for dashboard tiles
dashboard_queries = """
-- Tile 1: Current Status Overview
SensorReadings
| where timestamp > ago(5m)
| summarize 
    latest_value = arg_max(timestamp, value),
    latest_status = arg_max(timestamp, status)
  by sensor_id, location
| project sensor_id, location, latest_value, latest_status

-- Tile 2: Time Series Chart
SensorReadings
| where timestamp > ago(1h)
| where type == 'temperature'
| summarize avg_temp = avg(value) by bin(timestamp, 5m), location
| render timechart

-- Tile 3: Alerts Summary
SensorReadings
| where timestamp > ago(1h)
| where status == 'warning'
| summarize alert_count = count() by location
| render columnchart

-- Tile 4: Real-time Metric
SensorReadings
| where timestamp > ago(1m)
| summarize current_avg = avg(value)
| project metric = current_avg
| render card
"""

print("Sample Dashboard Queries:")
print(dashboard_queries)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## 7. Activator - Event-Driven Actions
# 
# Activator enables you to trigger actions based on patterns in your data:
# 
# ### Common Use Cases:
# - Send email/Teams alerts on threshold violations
# - Trigger Power Automate flows
# - Call custom webhooks
# - Start data pipelines
# 
# ### Setting up Activator:
# 1. Create an Activator item in your workspace
# 2. Connect to your event stream or KQL database
# 3. Define trigger conditions
# 4. Configure actions to take
# 5. Test and activate

# CELL ********************

# Example: Simulating activator logic
def check_activator_conditions(reading):
    """Check if reading meets activator trigger conditions"""
    triggers = []
    
    # Condition 1: Temperature too high
    if reading['type'] == 'temperature' and reading['value'] > 26:
        triggers.append({
            'condition': 'High Temperature',
            'action': 'Send Alert to Facilities Team',
            'severity': 'High',
            'details': f"Temperature at {reading['location']} is {reading['value']}°C"
        })
    
    # Condition 2: Humidity out of range
    if reading['type'] == 'humidity' and (reading['value'] < 30 or reading['value'] > 60):
        triggers.append({
            'condition': 'Humidity Out of Range',
            'action': 'Trigger HVAC Adjustment',
            'severity': 'Medium',
            'details': f"Humidity at {reading['location']} is {reading['value']}%"
        })
    
    return triggers

# Check all readings for trigger conditions
all_triggers = []
for _, reading in df_readings.iterrows():
    triggers = check_activator_conditions(reading)
    all_triggers.extend(triggers)

if all_triggers:
    print(f"\nFound {len(all_triggers)} activator triggers:")
    display(pd.DataFrame(all_triggers))
else:
    print("\nNo activator triggers detected")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## 8. Best Practices for Real-Time Intelligence
# 
# ### Data Ingestion:
# 1. **Use batching** for high-volume streams
# 2. **Implement retry logic** for failed ingestions
# 3. **Monitor ingestion latency** and adjust buffer sizes
# 4. **Use partitioning** for scalability
# 
# ### Query Optimization:
# 1. **Filter early** in your KQL queries
# 2. **Use materialized views** for complex aggregations
# 3. **Implement data retention policies**
# 4. **Use appropriate time ranges** in queries
# 
# ### Monitoring:
# 1. **Set up alerts** for ingestion failures
# 2. **Monitor query performance**
# 3. **Track data freshness**
# 4. **Use capacity metrics** for scaling decisions

# CELL ********************

# Example: Data quality checks for streaming data
def validate_streaming_data(df):
    """Perform data quality checks"""
    issues = []
    
    # Check for null values
    null_counts = df.isnull().sum()
    if null_counts.any():
        issues.append(f"Found null values: {null_counts[null_counts > 0].to_dict()}")
    
    # Check for duplicate sensor readings
    duplicates = df.duplicated(subset=['sensor_id', 'timestamp']).sum()
    if duplicates > 0:
        issues.append(f"Found {duplicates} duplicate readings")
    
    # Check value ranges
    for sensor_type in df['type'].unique():
        type_df = df[df['type'] == sensor_type]
        if type_df['value'].std() > 10:  # High variance
            issues.append(f"High variance detected for {sensor_type} sensors")
    
    if issues:
        print("Data Quality Issues:")
        for issue in issues:
            print(f"  - {issue}")
    else:
        print("✓ All data quality checks passed")
    
    return len(issues) == 0

validate_streaming_data(df_readings)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## 9. Integration with Other Fabric Services
# 
# Real-Time Intelligence integrates seamlessly with:
# 
# ### OneLake:
# - Store historical streaming data in Delta tables
# - Combine real-time and batch analytics
# 
# ### Data Pipelines:
# - Trigger pipelines from events
# - Orchestrate data processing workflows
# 
# ### Power BI:
# - Create real-time reports
# - Use DirectQuery with KQL databases
# 
# ### Data Science:
# - Apply ML models to streaming data
# - Real-time predictions and scoring

# CELL ********************

# Example: Archiving streaming data to OneLake
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, TimestampType

# Convert to Spark DataFrame
schema = StructType([
    StructField("sensor_id", StringType(), False),
    StructField("location", StringType(), False),
    StructField("type", StringType(), False),
    StructField("value", DoubleType(), False),
    StructField("timestamp", StringType(), False),
    StructField("status", StringType(), False)
])

df_archive = spark.createDataFrame(df_readings.values.tolist(), schema)

# Write to OneLake (Delta format)
# df_archive.write.format("delta") \
#     .mode("append") \
#     .partitionBy("type") \
#     .save("Tables/sensor_archive")

print("Streaming data can be archived to OneLake for long-term storage and analysis")
print(f"Sample data shape: {df_archive.count()} rows")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## Summary
# 
# In this notebook, we covered:
# - ✅ Real-Time Intelligence architecture and components
# - ✅ Event Streams for data ingestion
# - ✅ KQL query language and patterns
# - ✅ Real-time analytics scenarios
# - ✅ Real-Time Dashboards for visualization
# - ✅ Activator for event-driven actions
# - ✅ Best practices for streaming analytics
# - ✅ Integration with other Fabric services
# 
# ## Next Steps
# - Explore Power BI semantic models for reporting
# - Learn about data pipeline orchestration
# - Implement CI/CD for Fabric solutions
# - Build end-to-end streaming applications
