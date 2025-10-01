# Microsoft Fabric Agentic Workloads Lab

## Overview

This comprehensive lab covers all aspects of Microsoft Fabric with a special focus on **Agentic AI workloads**. You'll learn how to build, deploy, and manage intelligent agents that can autonomously interact with data, make decisions, and orchestrate complex workflows across the Fabric platform.

## What is Microsoft Fabric?

Microsoft Fabric is an all-in-one analytics solution for enterprises that covers everything from data movement to data science, real-time analytics, and business intelligence. It brings together new and existing components from Power BI, Azure Synapse, and Azure Data Factory into a single integrated environment.

## What are Agentic Workloads?

Agentic workloads represent the next evolution in AI-powered data analytics. Instead of traditional reactive systems, agents are autonomous entities that can:
- **Perceive** their environment through data observation
- **Reason** about problems using AI models
- **Act** by executing tasks and workflows
- **Learn** from outcomes to improve over time
- **Collaborate** with other agents and humans

## Lab Objectives

By completing this lab, you will:
1. Understand the Microsoft Fabric architecture and components
2. Build end-to-end data pipelines using Data Factory
3. Perform data engineering with Apache Spark
4. Create machine learning models for agentic behavior
5. Implement real-time data streaming and analytics
6. Deploy autonomous AI agents on Fabric
7. Orchestrate multi-agent systems for complex scenarios
8. Monitor and optimize agent performance

## Prerequisites

- Azure subscription with Microsoft Fabric enabled
- Basic understanding of:
  - Python programming
  - SQL and data concepts
  - Machine learning fundamentals
  - RESTful APIs
- Familiarity with Azure services (helpful but not required)

## Lab Modules

### [Module 1: Environment Setup](./01-setup/README.md)
- Setting up your Fabric workspace
- Configuring permissions and security
- Installing required tools and SDKs
- Understanding Fabric capacity and compute

### [Module 2: Data Factory - Orchestration Foundations](./02-data-factory/README.md)
- Creating data pipelines
- Working with dataflows
- Implementing data movement patterns
- Scheduling and monitoring pipelines

### [Module 3: Data Engineering with Apache Spark](./03-data-engineering/README.md)
- Lakehouse architecture in Fabric
- Delta Lake and data management
- Spark notebooks and transformations
- Medallion architecture implementation

### [Module 4: Data Science and ML Models](./04-data-science/README.md)
- Building ML models in Fabric
- MLflow integration
- Model training and experimentation
- Deploying models for inference

### [Module 5: Data Warehouse and SQL Analytics](./05-data-warehouse/README.md)
- Creating data warehouses in Fabric
- T-SQL query optimization
- Serving data for analytics
- Integration with semantic models

### [Module 6: Real-Time Analytics](./06-real-time-analytics/README.md)
- Event streaming with Event Streams
- KQL (Kusto Query Language) databases
- Real-time dashboards
- Streaming data transformations

### [Module 7: Power BI Integration](./07-power-bi/README.md)
- Connecting Power BI to Fabric data
- Creating semantic models
- Building interactive reports
- Embedding analytics in applications

### [Module 8: Agentic Workloads ⭐](./08-agentic-workloads/README.md)
**The core module for AI agents**
- Introduction to agentic AI patterns
- Building autonomous data agents
- Agent communication protocols
- Tool-using agents with function calling
- Multi-agent orchestration
- Agent memory and state management
- Evaluation and monitoring of agents

### [Module 9: Advanced Scenarios](./09-advanced-scenarios/README.md)
- Industry-specific agent implementations
- Hybrid agent architectures
- Security and governance for agents
- Cost optimization strategies
- Best practices and design patterns

## Lab Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     Microsoft Fabric Workspace                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │ Data Factory │  │  Lakehouse   │  │   Data Warehouse     │  │
│  │  Pipelines   │──▶│ Delta Tables │──▶│   SQL Endpoint      │  │
│  └──────────────┘  └──────────────┘  └──────────────────────┘  │
│         │                  │                     │               │
│         │                  ▼                     │               │
│         │          ┌──────────────┐              │               │
│         │          │ ML Models    │              │               │
│         │          │ (MLflow)     │              │               │
│         │          └──────────────┘              │               │
│         │                  │                     │               │
│         │                  ▼                     │               │
│         │          ┌──────────────────────────────────────────┐ │
│         └─────────▶│      AI AGENTS (Agentic Layer)          │ │
│                    │  • Planning Agents                       │ │
│                    │  • Execution Agents                      │ │
│                    │  • Monitoring Agents                     │ │
│                    │  • Coordination Agents                   │ │
│                    └──────────────────────────────────────────┘ │
│                                    │                             │
│                                    ▼                             │
│                    ┌──────────────────────────┐                 │
│                    │  Real-Time Analytics     │                 │
│                    │  & Event Streams         │                 │
│                    └──────────────────────────┘                 │
│                                    │                             │
│                                    ▼                             │
│                    ┌──────────────────────────┐                 │
│                    │     Power BI Reports     │                 │
│                    └──────────────────────────┘                 │
└─────────────────────────────────────────────────────────────────┘
```

## Key Technologies

- **Microsoft Fabric**: Unified analytics platform
- **Azure OpenAI**: LLM models for agent reasoning
- **Apache Spark**: Distributed data processing
- **Delta Lake**: ACID transactions on data lakes
- **MLflow**: ML lifecycle management
- **KQL**: Real-time analytics queries
- **Power BI**: Business intelligence and visualization
- **Python**: Primary programming language for agents
- **Semantic Kernel / LangChain**: Agent frameworks

## Getting Started

1. Start with [Module 1: Environment Setup](./01-setup/README.md)
2. Complete modules sequentially for a structured learning path
3. Focus on Module 8 for deep-dive into Agentic workloads
4. Explore Module 9 for real-world applications

## Estimated Time

- **Full Lab**: 16-20 hours
- **Core Modules (1-7)**: 10-12 hours  
- **Agentic Workloads Focus (Module 8)**: 4-6 hours
- **Advanced Scenarios (Module 9)**: 2-3 hours

## Learning Paths

### Path 1: Quick Start (Agentic Focus)
For those who want to quickly get to agentic workloads:
1. Module 1 (Setup) - 1 hour
2. Module 3 (Data Engineering basics) - 1.5 hours
3. Module 4 (ML Models) - 1.5 hours
4. Module 8 (Agentic Workloads) - 4-6 hours

### Path 2: Comprehensive
For complete coverage of Fabric capabilities:
- Complete all modules sequentially - 16-20 hours

### Path 3: Data Engineer Focus
For data engineering professionals:
1. Modules 1-3, 5-6 - Data platform fundamentals
2. Module 8 - Agentic automation for data workflows

## Support and Resources

- [Microsoft Fabric Documentation](https://learn.microsoft.com/fabric/)
- [Azure OpenAI Service](https://learn.microsoft.com/azure/ai-services/openai/)
- [Community Discussions](https://github.com/ralphke/Fabric/discussions)
- [Issue Tracker](https://github.com/ralphke/Fabric/issues)

## Contributing

Contributions are welcome! Please see our contributing guidelines for more information.

## License

This project is licensed under the GPL-3.0 License - see the [LICENSE](../LICENSE) file for details.

---

**Ready to build intelligent, autonomous agents on Microsoft Fabric? Let's get started! 🚀**
