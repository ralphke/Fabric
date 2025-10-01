# Glossary of Terms

A comprehensive glossary of terms used throughout the Microsoft Fabric Agentic Workloads Lab.

## A

**Agentic AI**: Autonomous artificial intelligence systems that can perceive, reason, act, and learn to accomplish goals with minimal human intervention.

**Agent**: An autonomous software entity that can perceive its environment, make decisions, and take actions to achieve specific goals.

**Azure OpenAI**: Microsoft's Azure service providing access to OpenAI's GPT models and other AI capabilities.

## B

**Bronze Layer**: The raw data layer in a medallion architecture, containing unprocessed data as it arrives.

## C

**Chain-of-Thought (CoT)**: A prompting technique that encourages LLMs to show their reasoning step-by-step.

**Compute**: The processing resources (CPU, memory) used to run workloads in Fabric.

**Coordinator Agent**: An agent responsible for orchestrating multiple other agents to accomplish complex tasks.

## D

**Data Factory**: Microsoft Fabric's data integration service for creating data pipelines and orchestrating data movement.

**Dataflow**: A data transformation component in Data Factory using a visual interface.

**Delta Lake**: An open-source storage layer that provides ACID transactions on data lakes.

**Direct Lake Mode**: Power BI's ability to query data directly from OneLake without import or DirectQuery.

## E

**Embedding**: A numerical vector representation of text that captures semantic meaning, used for similarity search.

**Event Hub**: Azure's event streaming service for real-time data ingestion.

**Event Stream**: Fabric's real-time data streaming capability.

## F

**Fabric Capacity**: The compute and storage resources allocated to a Fabric workspace, measured in units (F2, F4, etc.).

**Function Calling**: The ability of LLMs to invoke specific functions or tools based on user requests.

## G

**Gold Layer**: The curated, business-ready data layer in medallion architecture.

**GPT (Generative Pre-trained Transformer)**: The family of large language models from OpenAI.

## K

**KQL (Kusto Query Language)**: The query language used for analyzing data in Azure Data Explorer and Fabric KQL databases.

**KQL Database**: A Fabric component for storing and querying real-time data using KQL.

## L

**Lakehouse**: A Fabric component combining data lake and data warehouse capabilities using Delta Lake.

**LangChain**: A framework for developing applications powered by language models.

**LLM (Large Language Model)**: A neural network trained on vast amounts of text data, capable of understanding and generating human-like text.

**Long-Term Memory**: In agent systems, persistent storage of important information for future recall.

## M

**Managed Identity**: An Azure identity that doesn't require managing credentials, used for secure authentication.

**Medallion Architecture**: A data design pattern with bronze (raw), silver (cleaned), and gold (curated) layers.

**Memory System**: The component managing an agent's ability to store and retrieve information.

**MLflow**: An open-source platform for managing the machine learning lifecycle.

**Multi-Agent System**: A system where multiple specialized agents collaborate to solve complex problems.

## O

**OneLake**: Microsoft Fabric's unified data lake, providing a single storage location for all data.

**Orchestration**: The coordination of multiple tasks, agents, or services to accomplish a goal.

## P

**Perceive**: The agent's ability to observe and understand its environment through data.

**Pipeline**: A series of connected data processing activities in Data Factory.

**Power BI**: Microsoft's business intelligence platform for data visualization and reporting.

**Prompt**: The input text given to an LLM to generate a response.

**Prompt Engineering**: The practice of crafting effective prompts to get desired outputs from LLMs.

## R

**RAG (Retrieval-Augmented Generation)**: A pattern where an LLM retrieves relevant information before generating a response.

**ReAct**: A prompting pattern combining Reasoning and Acting in iterative loops.

**Real-Time Analytics**: The ability to analyze and respond to data as it arrives.

**Reason**: The agent's ability to think about information and make decisions.

**REST API**: A web API using HTTP requests to interact with services.

**Row-Level Security (RLS)**: Security mechanism restricting data access at the row level based on user attributes.

## S

**Semantic Kernel**: Microsoft's SDK for integrating LLMs with conventional programming languages.

**Semantic Model**: Power BI's data model defining relationships, measures, and business logic.

**Service Principal**: An Azure AD identity for applications to access Azure resources.

**Short-Term Memory**: In agent systems, temporary storage of recent interactions.

**Silver Layer**: The cleaned and validated data layer in medallion architecture.

**Spark**: Apache Spark, a distributed data processing engine used in Fabric.

**State Management**: Tracking and maintaining the current state of agents and workflows.

## T

**T-SQL (Transact-SQL)**: Microsoft's extension of SQL used in SQL Server and Fabric Data Warehouse.

**Temperature**: A parameter controlling the randomness of LLM outputs (0 = deterministic, higher = more random).

**Token**: The basic unit of text processed by LLMs (roughly 3-4 characters).

**Tool-Using Agent**: An agent capable of calling external functions or APIs to accomplish tasks.

## W

**Warehouse**: Fabric's SQL-based data warehouse for structured analytical queries.

**Workspace**: A container for Fabric items (lakehouses, notebooks, pipelines, etc.).

**Working Memory**: The agent's current context and active information during task execution.

## Abbreviations

- **AI**: Artificial Intelligence
- **API**: Application Programming Interface
- **ACID**: Atomicity, Consistency, Isolation, Durability
- **CoT**: Chain-of-Thought
- **DAX**: Data Analysis Expressions (Power BI formula language)
- **ETL**: Extract, Transform, Load
- **GPT**: Generative Pre-trained Transformer
- **HTTP**: Hypertext Transfer Protocol
- **JSON**: JavaScript Object Notation
- **KQL**: Kusto Query Language
- **LLM**: Large Language Model
- **ML**: Machine Learning
- **RAG**: Retrieval-Augmented Generation
- **REST**: Representational State Transfer
- **RLS**: Row-Level Security
- **ROI**: Return on Investment
- **SDK**: Software Development Kit
- **SLA**: Service Level Agreement
- **SQL**: Structured Query Language
- **TTL**: Time to Live

## Key Concepts

### Agent Lifecycle
1. **Initialization**: Agent is created with configuration
2. **Perception**: Agent observes environment
3. **Reasoning**: Agent decides what to do
4. **Action**: Agent executes tasks
5. **Learning**: Agent updates its knowledge
6. **Termination**: Agent completes or shuts down

### Data Flow Patterns
- **Batch Processing**: Processing data in scheduled chunks
- **Stream Processing**: Processing data continuously as it arrives
- **Micro-batch**: Small batch processing at frequent intervals
- **Lambda Architecture**: Combining batch and stream processing
- **Kappa Architecture**: Stream-only architecture

### Agent Communication Patterns
- **Request-Response**: Agent sends request, waits for response
- **Publish-Subscribe**: Agents subscribe to event topics
- **Message Queue**: Asynchronous message passing
- **Direct Communication**: Point-to-point agent interaction

### Security Models
- **Zero Trust**: Verify every access request
- **Least Privilege**: Grant minimum necessary permissions
- **Defense in Depth**: Multiple layers of security
- **Separation of Duties**: Divide critical tasks among agents

---

**Need clarification on any term?** Open an issue or discussion on GitHub!
