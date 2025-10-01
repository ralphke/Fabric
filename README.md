# Microsoft Fabric Learning Content

This repository contains comprehensive Jupyter notebooks showcasing the key capabilities of Microsoft Fabric, a unified analytics platform that brings together data engineering, data science, real-time analytics, and business intelligence.

## 📚 Notebooks

### 1. [OneLake Introduction](./notebooks/01_OneLake_Introduction.ipynb)
Learn about OneLake, Microsoft Fabric's unified data lake that provides a single storage location for all your analytics data.

**Topics covered:**
- OneLake architecture and benefits
- Reading and writing data in multiple formats (CSV, Parquet, Delta)
- Creating and managing Delta tables
- Data transformations and SQL queries
- OneLake shortcuts for external data access
- Delta Lake advanced features (time travel, history)
- Best practices for storage and performance
- Data governance capabilities

### 2. [Real-Time Intelligence](./notebooks/02_RealTime_Intelligence.ipynb)
Explore Real-Time Intelligence capabilities for streaming data analytics and event-driven architectures.

**Topics covered:**
- Event Streams for data ingestion
- KQL (Kusto Query Language) basics and patterns
- Real-time analytics scenarios
- Simulating IoT sensor data
- Real-Time Dashboards for visualization
- Activator for event-driven actions
- Integration with other Fabric services
- Best practices for streaming analytics

### 3. [Power BI Semantic Models](./notebooks/03_PowerBI_Semantic_Models.ipynb)
Understand how to build and manage Power BI semantic models (formerly datasets) for enterprise analytics.

**Topics covered:**
- Semantic model concepts and architecture
- Star schema design with fact and dimension tables
- Creating sample business data
- Common DAX measures and calculations
- Time intelligence and advanced analytics
- Row-level security (RLS) implementation
- Querying semantic models programmatically
- Refresh strategies and automation
- Best practices for performance

### 4. [Data Pipelines](./notebooks/04_Data_Pipelines.ipynb)
Master data pipeline orchestration and workflow automation in Microsoft Fabric.

**Topics covered:**
- Pipeline architecture patterns (ETL, ELT, Medallion)
- Key pipeline activities and components
- Building multi-layer transformations (Bronze, Silver, Gold)
- Incremental loading patterns
- Error handling and monitoring
- Pipeline parameters and variables
- Scheduling and trigger configuration
- Data quality validation
- Best practices for production pipelines

### 5. [CI/CD Pipelines](./notebooks/05_CICD_Pipelines.ipynb)
Implement DevOps practices for Microsoft Fabric with continuous integration and deployment.

**Topics covered:**
- Git integration with Fabric workspaces
- Environment configuration management
- Azure DevOps pipeline setup
- GitHub Actions workflow configuration
- Validation scripts for notebooks and pipelines
- Deployment automation using REST API
- Testing strategies (unit, integration, smoke tests)
- Security and credential management
- Monitoring and alerting

## 🚀 Getting Started

### Prerequisites
- A Microsoft Fabric workspace
- Appropriate Fabric capacity (F2 or higher recommended)
- Basic knowledge of Python and SQL
- (Optional) Git repository for CI/CD examples

### Running the Notebooks

1. **In Microsoft Fabric:**
   - Upload notebooks to your Fabric workspace
   - Attach to a lakehouse
   - Run cells sequentially

2. **Locally with Jupyter:**
   - Clone this repository
   - Install required packages: `pip install pandas numpy pyspark`
   - Open notebooks in Jupyter Lab/Notebook

## 📖 Learning Path

For a structured learning experience, we recommend following the notebooks in this order:

1. **Start with OneLake** to understand the foundational storage layer
2. **Explore Real-Time Intelligence** for streaming scenarios
3. **Learn Power BI Semantic Models** for reporting and analytics
4. **Master Data Pipelines** for orchestration and automation
5. **Implement CI/CD** to operationalize your solutions

## 🔗 Additional Resources

- [Microsoft Fabric Documentation](https://learn.microsoft.com/fabric/)
- [Fabric Community](https://community.fabric.microsoft.com/)
- [Fabric Blog](https://blog.fabric.microsoft.com/)
- [Power BI Community](https://community.powerbi.com/)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues or pull requests to improve these learning materials.

## 📝 License

This project is licensed under the GPL-3.0 License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

These notebooks are provided as educational content. Always test thoroughly before using any code in production environments. The examples use simulated data and may need adaptation for real-world scenarios.

---

**Last Updated:** October 2025 
