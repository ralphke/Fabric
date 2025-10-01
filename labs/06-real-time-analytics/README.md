# Module 6: Real-Time Analytics

## Overview
Implement real-time data streaming and analytics for responsive agentic workloads.

## Duration
⏱️ Estimated time: 1.5 hours

## Learning Objectives
- Create Event Streams
- Work with KQL databases
- Build real-time dashboards
- Enable agents to react to events

## Key Topics

### 1. Event Streams
- Creating event streams
- Event sources (Event Hubs, IoT Hub)
- Event destinations
- Stream transformations

### 2. KQL Databases
- Kusto Query Language basics
- Time-series analysis
- Real-time aggregations

### 3. Real-Time Agents
- Event-driven agent triggers
- Streaming data processing
- Real-time decision making

## Hands-On Exercises

### Exercise 1: Create Event Stream
Set up streaming data ingestion.

### Exercise 2: KQL Queries
Write queries for real-time analysis.

### Exercise 3: Event-Driven Agent
Build an agent that reacts to stream events.

## Sample Code

```python
# Event-driven agent
from azure.eventhub import EventHubConsumerClient

class RealTimeAgent:
    def __init__(self):
        self.client = EventHubConsumerClient.from_connection_string(
            conn_str, consumer_group, eventhub_name
        )
    
    def on_event(self, partition_context, event):
        # Agent processes each event
        data = json.loads(event.body_as_str())
        
        # Detect anomalies
        if self.is_anomaly(data):
            self.take_action(data)
        
        partition_context.update_checkpoint(event)
    
    def start(self):
        self.client.receive(on_event=self.on_event)
```

```kusto
-- KQL query for real-time monitoring
Events
| where Timestamp > ago(5m)
| summarize Count=count(), AvgValue=avg(Value) by bin(Timestamp, 1m)
| where AvgValue > 100  // Alert threshold
```

## Assessment
- Set up end-to-end streaming pipeline
- Create KQL queries for monitoring
- Build real-time responsive agent

---

[← Back to Module 5](../05-data-warehouse/README.md) | [Next: Module 7 →](../07-power-bi/README.md)
