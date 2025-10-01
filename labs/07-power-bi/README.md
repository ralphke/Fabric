# Module 7: Power BI Integration

## Overview
Connect Power BI to Fabric data sources and create interactive reports for monitoring agents.

## Duration
⏱️ Estimated time: 1.5 hours

## Learning Objectives
- Connect Power BI to Fabric
- Create semantic models
- Build interactive reports
- Visualize agent performance
- Enable agents to update reports

## Key Topics

### 1. Power BI Fundamentals
- Connecting to Fabric data
- Direct Lake mode
- Report design basics

### 2. Semantic Models
- Creating models from Lakehouse/Warehouse
- Relationships and hierarchies
- Measures and calculated columns

### 3. Visualizations
- Common chart types
- Interactive filters
- Drill-through capabilities

### 4. Agent Monitoring Dashboards
- Visualizing agent metrics
- Real-time performance tracking
- Cost and usage reports

## Hands-On Exercises

### Exercise 1: Connect to Fabric Data
Create a semantic model from your Lakehouse.

### Exercise 2: Build Agent Dashboard
Create a dashboard showing agent performance.

### Exercise 3: Automated Report Updates
Enable agents to trigger report refreshes.

## Sample Code

```python
# Agent updates Power BI dataset
from powerbi import PowerBIClient
from azure.identity import DefaultAzureCredential

class ReportingAgent:
    def __init__(self):
        credential = DefaultAzureCredential()
        self.client = PowerBIClient(credential)
    
    def update_dashboard(self, dataset_id):
        # Trigger dataset refresh
        self.client.datasets.refresh_dataset(
            workspace_id, 
            dataset_id
        )
        
        print("Dashboard updated with latest agent metrics")
    
    def get_report_insights(self, report_id):
        # Agents can query reports for insights
        data = self.client.reports.export_to_file(
            workspace_id,
            report_id,
            "JSON"
        )
        return data
```

## Dashboard Examples

### Agent Performance Dashboard
- Tasks completed vs. failed
- Average latency trends
- Token usage and costs
- Error rates by agent type

### Data Quality Dashboard
- Data freshness metrics
- Pipeline success rates
- Data volume trends

### Business Impact Dashboard
- Business metrics affected by agents
- ROI calculations
- Time saved through automation

## Assessment
- Create a complete Power BI report
- Build agent performance dashboard
- Implement automated updates

---

[← Back to Module 6](../06-real-time-analytics/README.md) | [Next: Module 8 - Agentic Workloads →](../08-agentic-workloads/README.md)
