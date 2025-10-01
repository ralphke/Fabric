# Architecture Overview

## Microsoft Fabric Agentic Workloads Lab - System Architecture

This document provides a comprehensive overview of the architecture patterns and design principles used throughout the lab.

## Architectural Layers

### Layer 1: Data Foundation
```
┌─────────────────────────────────────────────────────────────┐
│                    DATA FOUNDATION LAYER                     │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  OneLake (Unified Data Lake)                                │
│  ├── Lakehouses (Delta Lake)                                │
│  │   ├── Bronze Layer (Raw data)                            │
│  │   ├── Silver Layer (Cleaned data)                        │
│  │   └── Gold Layer (Aggregated data)                       │
│  │                                                           │
│  ├── Data Warehouses (SQL)                                  │
│  │   ├── Fact tables                                        │
│  │   └── Dimension tables                                   │
│  │                                                           │
│  └── KQL Databases (Real-time)                              │
│      └── Time-series data                                   │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

### Layer 2: Data Processing
```
┌─────────────────────────────────────────────────────────────┐
│                  DATA PROCESSING LAYER                       │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  Data Factory Pipelines                                      │
│  ├── Copy activities                                         │
│  ├── Dataflows                                               │
│  └── Orchestration workflows                                 │
│                                                               │
│  Spark Notebooks                                             │
│  ├── PySpark transformations                                 │
│  ├── SQL queries                                             │
│  └── ML data preparation                                     │
│                                                               │
│  Event Streams                                               │
│  ├── Event capture                                           │
│  ├── Stream processing                                       │
│  └── Event routing                                           │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

### Layer 3: Intelligence
```
┌─────────────────────────────────────────────────────────────┐
│                    INTELLIGENCE LAYER                        │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ML Models (MLflow)                                          │
│  ├── Training pipelines                                      │
│  ├── Model registry                                          │
│  └── Inference endpoints                                     │
│                                                               │
│  Azure OpenAI Service                                        │
│  ├── GPT-4 (reasoning)                                       │
│  ├── GPT-3.5-turbo (fast tasks)                             │
│  └── Embeddings (semantic search)                           │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

### Layer 4: Agentic Layer (Core)
```
┌─────────────────────────────────────────────────────────────┐
│                     AGENTIC LAYER ⭐                         │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  Orchestration Agents                                        │
│  ├── Coordinator Agent (task distribution)                  │
│  ├── Planner Agent (strategy)                               │
│  └── Monitor Agent (oversight)                              │
│                                                               │
│  Specialized Agents                                          │
│  ├── Data Analyst Agent                                     │
│  ├── ML Engineer Agent                                      │
│  ├── Pipeline Operator Agent                                │
│  └── Security Agent                                         │
│                                                               │
│  Agent Infrastructure                                        │
│  ├── Memory System (short/long term)                        │
│  ├── Tool Registry (available functions)                    │
│  ├── Message Bus (inter-agent comm)                         │
│  └── State Manager (agent state)                            │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

### Layer 5: Presentation
```
┌─────────────────────────────────────────────────────────────┐
│                   PRESENTATION LAYER                         │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  Power BI Reports                                            │
│  ├── Agent performance dashboards                           │
│  ├── Business metrics                                       │
│  └── Real-time monitoring                                   │
│                                                               │
│  APIs and Integrations                                      │
│  ├── REST APIs                                              │
│  ├── Webhooks                                               │
│  └── Event notifications                                    │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

## Agent Architecture Patterns

### Pattern 1: Simple Autonomous Agent
```python
class SimpleAgent:
    def run(self, task):
        # Perceive: Gather context
        context = self.perceive(task)
        
        # Reason: Use LLM to decide
        decision = self.reason(context)
        
        # Act: Execute action
        result = self.act(decision)
        
        return result
```

**Use Cases**:
- Single-purpose tasks
- Quick decisions
- Isolated operations

### Pattern 2: Tool-Using Agent
```python
class ToolAgent:
    def run(self, task):
        # Agent can call multiple tools
        tools = [query_db, run_notebook, send_alert]
        
        # LLM decides which tools to use
        response = llm.chat(task, tools=tools)
        
        # Execute tool calls
        results = execute_tool_calls(response)
        
        return results
```

**Use Cases**:
- Complex workflows
- Multi-step operations
- API orchestration

### Pattern 3: Multi-Agent System
```python
class MultiAgentSystem:
    def run(self, task):
        # Coordinator breaks down task
        plan = coordinator.plan(task)
        
        # Specialized agents execute subtasks
        results = []
        for subtask in plan:
            agent = self.get_agent(subtask.type)
            result = agent.execute(subtask)
            results.append(result)
        
        # Coordinator synthesizes results
        return coordinator.synthesize(results)
```

**Use Cases**:
- Complex problem solving
- Collaborative tasks
- Domain expertise needed

### Pattern 4: Reactive Agent
```python
class ReactiveAgent:
    def run(self, task):
        # ReAct loop: Reason + Act
        observation = self.observe()
        
        for step in range(max_steps):
            # Think
            thought = self.reason(observation)
            
            # Act
            action = self.plan_action(thought)
            observation = self.execute(action)
            
            if self.is_complete(observation):
                break
        
        return observation
```

**Use Cases**:
- Iterative problem solving
- Trial and error scenarios
- Dynamic environments

## Data Flow Architecture

```
External Data → Data Factory Pipeline → Lakehouse (Bronze)
                                            ↓
                                    Spark Processing
                                            ↓
                                    Lakehouse (Silver)
                                            ↓
                                    Aggregation
                                            ↓
                           ┌────────────────┴────────────────┐
                           ↓                                  ↓
                    Lakehouse (Gold)                  Data Warehouse
                           ↓                                  ↓
                      ML Training                        SQL Analytics
                           ↓                                  ↓
                      ML Models                         Semantic Models
                           ↓                                  ↓
                           └────────────────┬────────────────┘
                                           ↓
                                    AGENTIC LAYER
                                  (Intelligent Agents)
                                           ↓
                                    ┌──────┴──────┐
                                    ↓             ↓
                              Actions       Power BI Reports
                              (Automated)   (Visualizations)
```

## Security Architecture

### Authentication Flow
```
User/Agent → Azure AD → Managed Identity → Fabric Workspace
                              ↓
                      Service Principal
                              ↓
                    Azure OpenAI Service
```

### Authorization Layers
1. **Workspace Level**: Admin, Member, Contributor, Viewer
2. **Item Level**: Read, Write, Execute permissions
3. **Row Level**: RLS on data
4. **API Level**: OAuth scopes

### Security Best Practices
- ✅ Use Managed Identities (not service principals with keys)
- ✅ Implement Row-Level Security (RLS)
- ✅ Encrypt data at rest and in transit
- ✅ Audit all agent actions
- ✅ Rate limiting on API calls
- ✅ Never commit credentials to source control

## Scalability Patterns

### Horizontal Scaling
```
Task Queue → [Agent 1] → Results
          → [Agent 2] →
          → [Agent 3] →
```

### Vertical Scaling
```
Complex Task → Powerful Agent (GPT-4, more memory)
Simple Task  → Efficient Agent (GPT-3.5, less memory)
```

### Hybrid Scaling
```
Coordinator
    ├── Parallel Agent Pool (horizontal)
    └── Specialized Agents (vertical)
```

## Monitoring Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    MONITORING SYSTEM                         │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  Agent Metrics                                               │
│  ├── Task success rate                                      │
│  ├── Latency (p50, p95, p99)                                │
│  ├── Token usage and cost                                   │
│  └── Error rates                                            │
│                                                               │
│  System Metrics                                              │
│  ├── Resource utilization                                   │
│  ├── API rate limits                                        │
│  └── Queue depths                                           │
│                                                               │
│  Business Metrics                                            │
│  ├── Tasks automated                                        │
│  ├── Time saved                                             │
│  └── ROI calculations                                       │
│                                                               │
│  Outputs                                                     │
│  ├── Real-time dashboards (Power BI)                        │
│  ├── Alerts (critical events)                               │
│  └── Historical reports                                     │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

## Deployment Architecture

### Development Environment
```
Local Development
    ├── Python virtual environment
    ├── Local Spark (optional)
    ├── Jupyter notebooks
    └── Git version control
```

### Staging Environment
```
Fabric Workspace (Staging)
    ├── Test data
    ├── Agent prototypes
    ├── Integration tests
    └── Performance benchmarks
```

### Production Environment
```
Fabric Workspace (Production)
    ├── Production data
    ├── Deployed agents
    ├── Monitoring enabled
    ├── Backup and recovery
    └── Disaster recovery plan
```

## Technology Stack

| Layer | Technologies |
|-------|-------------|
| Data Storage | OneLake, Delta Lake, SQL |
| Data Processing | Apache Spark, Data Factory |
| ML/AI | MLflow, Azure OpenAI, Semantic Kernel |
| Real-Time | Event Streams, KQL |
| Visualization | Power BI |
| Development | Python, VS Code, Git |
| Orchestration | Data Factory, Agent frameworks |
| Monitoring | Azure Monitor, Application Insights |

## Design Principles

### 1. Modular Design
- Separate concerns (data, logic, presentation)
- Reusable components
- Clear interfaces

### 2. Fail-Safe Operations
- Graceful degradation
- Error handling and retries
- Circuit breakers

### 3. Observability
- Comprehensive logging
- Metrics collection
- Distributed tracing

### 4. Cost Optimization
- Right-size resources
- Use appropriate models (GPT-3.5 vs GPT-4)
- Cache when possible
- Batch operations

### 5. Security First
- Zero trust architecture
- Principle of least privilege
- Data encryption
- Regular audits

## Integration Points

### Fabric REST API
```python
headers = {"Authorization": f"Bearer {token}"}
response = requests.get(
    "https://api.fabric.microsoft.com/v1/workspaces",
    headers=headers
)
```

### Azure OpenAI API
```python
client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)
response = client.chat.completions.create(...)
```

### Event Streams
```python
client = EventHubConsumerClient.from_connection_string(...)
client.receive(on_event=process_event)
```

## Future Extensions

Potential areas for expansion:
1. **Advanced Agent Types**
   - Reasoning agents with chain-of-thought
   - Self-improving agents
   - Swarm intelligence

2. **Enhanced Integration**
   - Azure Logic Apps
   - Azure Functions
   - Power Automate

3. **Advanced Analytics**
   - Agent behavior analytics
   - Cost prediction models
   - Performance optimization

4. **Industry Solutions**
   - Financial services templates
   - Healthcare compliance
   - Retail optimization

---

This architecture supports the entire lab journey from basic data ingestion to sophisticated multi-agent systems, all within the Microsoft Fabric ecosystem.

For implementation details, see the individual module READMEs in the labs/ directory.
