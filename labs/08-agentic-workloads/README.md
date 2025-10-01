# Module 8: Agentic Workloads ⭐

## Overview

Welcome to the core module of this lab! Here you'll learn to build autonomous AI agents that can perceive, reason, act, and learn within the Microsoft Fabric ecosystem. Agentic workloads represent the cutting edge of AI-powered data analytics and automation.

## Duration
⏱️ Estimated time: 4-6 hours

## What Makes a Workload "Agentic"?

Traditional AI systems are reactive - they respond to direct inputs. Agentic AI systems are **proactive** and **autonomous**:

- **Perception**: Agents observe their environment (data, events, metrics)
- **Reasoning**: Agents use LLMs to understand context and make decisions
- **Action**: Agents execute tasks through tools and APIs
- **Learning**: Agents improve from feedback and experience
- **Autonomy**: Agents operate with minimal human intervention

## Learning Objectives

By completing this module, you will:
1. Understand agentic AI architecture patterns
2. Build single-purpose autonomous agents
3. Implement tool-using agents with function calling
4. Create multi-agent systems with orchestration
5. Manage agent memory and state
6. Monitor and evaluate agent performance
7. Deploy production-ready agents on Fabric

## Prerequisites

- Completed Module 1 (Environment Setup)
- Basic understanding of:
  - LLMs and prompt engineering
  - Python programming
  - REST APIs
- Modules 3-4 recommended (but not required)

## Lab Architecture

```
┌────────────────────────────────────────────────────────────────┐
│                    Agentic Workload System                      │
├────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              ORCHESTRATION LAYER                          │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │  │
│  │  │ Coordinator  │  │  Planner     │  │  Monitor     │  │  │
│  │  │   Agent      │──│   Agent      │──│   Agent      │  │  │
│  │  └──────────────┘  └──────────────┘  └──────────────┘  │  │
│  └────────────────────────┬─────────────────────────────────┘  │
│                           │                                     │
│  ┌────────────────────────▼─────────────────────────────────┐  │
│  │              EXECUTION AGENTS LAYER                       │  │
│  │  ┌────────────┐  ┌────────────┐  ┌─────────────────┐   │  │
│  │  │ Data Query │  │ Transform  │  │ ML Inference    │   │  │
│  │  │   Agent    │  │   Agent    │  │   Agent         │   │  │
│  │  └────────────┘  └────────────┘  └─────────────────┘   │  │
│  └────────────────────────┬─────────────────────────────────┘  │
│                           │                                     │
│  ┌────────────────────────▼─────────────────────────────────┐  │
│  │                  TOOLS & APIs LAYER                       │  │
│  │  ┌──────────┐  ┌──────────┐  ┌───────────┐  ┌────────┐ │  │
│  │  │ Fabric   │  │ SQL      │  │ Spark     │  │ OpenAI │ │  │
│  │  │ REST API │  │ Endpoint │  │ Notebooks │  │ Models │ │  │
│  │  └──────────┘  └──────────┘  └───────────┘  └────────┘ │  │
│  └──────────────────────────────────────────────────────────┘  │
│                           │                                     │
│  ┌────────────────────────▼─────────────────────────────────┐  │
│  │                  FABRIC DATA LAYER                        │  │
│  │        Lakehouse │ Warehouse │ Real-Time Analytics       │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────┘
```

## Lab Exercises

### Exercise 1: Building Your First Agent (45 minutes)

Create a simple data query agent that can answer questions about data in Fabric.

**File**: `exercise1_simple_agent.py`

```python
"""
Exercise 1: Simple Data Query Agent
A basic agent that can query Fabric lakehouse and answer questions about data.
"""

from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential
import os
import json

class SimpleDataAgent:
    """A simple agent that queries data and answers questions."""
    
    def __init__(self):
        self.client = AzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            api_version="2024-02-01",
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
        )
        self.deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
        self.conversation_history = []
    
    def query_fabric_data(self, table_name, filter_condition=None):
        """
        Simulates querying data from Fabric lakehouse.
        In production, this would use Fabric REST API or SQL endpoint.
        """
        # Mock data for demonstration
        mock_data = {
            "sales": [
                {"date": "2024-01-01", "product": "Widget A", "amount": 1500, "region": "East"},
                {"date": "2024-01-02", "product": "Widget B", "amount": 2300, "region": "West"},
                {"date": "2024-01-03", "product": "Widget A", "amount": 1800, "region": "East"},
            ],
            "customers": [
                {"id": 1, "name": "Acme Corp", "segment": "Enterprise"},
                {"id": 2, "name": "Tech Start", "segment": "SMB"},
            ]
        }
        return mock_data.get(table_name, [])
    
    def perceive(self, user_question):
        """Agent perceives the user's question and environment."""
        print(f"👀 Agent perceiving: '{user_question}'")
        
        # Get relevant context from data
        sales_data = self.query_fabric_data("sales")
        
        context = {
            "user_question": user_question,
            "available_data": {
                "sales": sales_data,
                "total_records": len(sales_data)
            }
        }
        return context
    
    def reason(self, context):
        """Agent reasons about the question using LLM."""
        print("🧠 Agent reasoning...")
        
        system_prompt = """You are a data analysis agent working with Microsoft Fabric.
        You have access to sales data and can answer questions about it.
        Analyze the data provided and give accurate, concise answers.
        If you need more data, say what you need."""
        
        user_prompt = f"""
        Question: {context['user_question']}
        
        Available data:
        {json.dumps(context['available_data'], indent=2)}
        
        Provide a clear answer based on this data.
        """
        
        response = self.client.chat.completions.create(
            model=self.deployment,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )
        
        return response.choices[0].message.content
    
    def act(self, reasoning_result):
        """Agent acts by providing the answer."""
        print("✅ Agent responding...")
        return reasoning_result
    
    def run(self, user_question):
        """Main agent loop: perceive -> reason -> act."""
        print("\n" + "="*60)
        print("🤖 Simple Data Agent")
        print("="*60)
        
        # Perceive
        context = self.perceive(user_question)
        
        # Reason
        answer = self.reason(context)
        
        # Act
        result = self.act(answer)
        
        print(f"\n💬 Answer: {result}\n")
        return result

# Demo usage
if __name__ == "__main__":
    agent = SimpleDataAgent()
    
    # Test questions
    questions = [
        "What was the total sales amount?",
        "Which product had the highest sales?",
        "How many transactions were in the East region?"
    ]
    
    for question in questions:
        agent.run(question)
        print()
```

**Tasks**:
1. Run the simple agent with sample questions
2. Modify it to query actual Fabric data sources
3. Add error handling and logging
4. Experiment with different prompts

---

### Exercise 2: Tool-Using Agent with Function Calling (60 minutes)

Build an agent that can use multiple tools to accomplish complex tasks.

**File**: `exercise2_tool_agent.py`

```python
"""
Exercise 2: Tool-Using Agent with Function Calling
An agent that can call multiple tools/functions to accomplish tasks.
"""

from openai import AzureOpenAI
import os
import json
import requests
from typing import Dict, List, Any

class ToolUsingAgent:
    """An agent that can use multiple tools via function calling."""
    
    def __init__(self):
        self.client = AzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            api_version="2024-02-01",
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
        )
        self.deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
        
        # Define available tools
        self.tools = [
            {
                "type": "function",
                "function": {
                    "name": "query_lakehouse",
                    "description": "Query data from Fabric lakehouse using SQL",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "sql_query": {
                                "type": "string",
                                "description": "The SQL query to execute"
                            },
                            "lakehouse_name": {
                                "type": "string",
                                "description": "Name of the lakehouse"
                            }
                        },
                        "required": ["sql_query", "lakehouse_name"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "run_spark_notebook",
                    "description": "Execute a Spark notebook for data transformation",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "notebook_name": {
                                "type": "string",
                                "description": "Name of the notebook to run"
                            },
                            "parameters": {
                                "type": "object",
                                "description": "Parameters to pass to the notebook"
                            }
                        },
                        "required": ["notebook_name"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "trigger_pipeline",
                    "description": "Trigger a Data Factory pipeline",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "pipeline_name": {
                                "type": "string",
                                "description": "Name of the pipeline to trigger"
                            },
                            "parameters": {
                                "type": "object",
                                "description": "Pipeline parameters"
                            }
                        },
                        "required": ["pipeline_name"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "send_alert",
                    "description": "Send an alert notification",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "message": {
                                "type": "string",
                                "description": "Alert message"
                            },
                            "severity": {
                                "type": "string",
                                "enum": ["info", "warning", "error"],
                                "description": "Alert severity level"
                            }
                        },
                        "required": ["message", "severity"]
                    }
                }
            }
        ]
    
    def query_lakehouse(self, sql_query: str, lakehouse_name: str) -> Dict:
        """Execute SQL query on lakehouse."""
        print(f"🔍 Querying lakehouse '{lakehouse_name}': {sql_query}")
        
        # Mock implementation - replace with actual Fabric API call
        return {
            "status": "success",
            "rows_returned": 42,
            "data": [{"sample": "data"}]
        }
    
    def run_spark_notebook(self, notebook_name: str, parameters: Dict = None) -> Dict:
        """Run a Spark notebook."""
        print(f"📓 Running notebook '{notebook_name}' with params: {parameters}")
        
        # Mock implementation
        return {
            "status": "success",
            "run_id": "run_12345",
            "output": "Notebook executed successfully"
        }
    
    def trigger_pipeline(self, pipeline_name: str, parameters: Dict = None) -> Dict:
        """Trigger a Data Factory pipeline."""
        print(f"🚀 Triggering pipeline '{pipeline_name}' with params: {parameters}")
        
        # Mock implementation
        return {
            "status": "success",
            "run_id": "pipeline_run_67890",
            "message": "Pipeline triggered successfully"
        }
    
    def send_alert(self, message: str, severity: str) -> Dict:
        """Send an alert notification."""
        print(f"🚨 Sending {severity} alert: {message}")
        
        # Mock implementation
        return {
            "status": "sent",
            "timestamp": "2024-01-01T12:00:00Z"
        }
    
    def execute_tool(self, tool_name: str, arguments: Dict) -> Any:
        """Execute a tool based on its name."""
        tool_map = {
            "query_lakehouse": self.query_lakehouse,
            "run_spark_notebook": self.run_spark_notebook,
            "trigger_pipeline": self.trigger_pipeline,
            "send_alert": self.send_alert
        }
        
        if tool_name not in tool_map:
            return {"error": f"Unknown tool: {tool_name}"}
        
        return tool_map[tool_name](**arguments)
    
    def run(self, task: str, max_iterations: int = 5):
        """Run the agent with a given task."""
        print("\n" + "="*60)
        print(f"🤖 Tool-Using Agent - Task: {task}")
        print("="*60 + "\n")
        
        messages = [
            {
                "role": "system",
                "content": """You are an autonomous agent working with Microsoft Fabric.
                You can query data, run notebooks, trigger pipelines, and send alerts.
                Use the available tools to accomplish the user's task.
                Think step-by-step and use tools as needed."""
            },
            {
                "role": "user",
                "content": task
            }
        ]
        
        for iteration in range(max_iterations):
            print(f"\n--- Iteration {iteration + 1} ---")
            
            # Call LLM with function calling
            response = self.client.chat.completions.create(
                model=self.deployment,
                messages=messages,
                tools=self.tools,
                tool_choice="auto",
                temperature=0.7
            )
            
            response_message = response.choices[0].message
            
            # Check if LLM wants to call a tool
            if response_message.tool_calls:
                messages.append(response_message)
                
                # Execute each tool call
                for tool_call in response_message.tool_calls:
                    function_name = tool_call.function.name
                    arguments = json.loads(tool_call.function.arguments)
                    
                    print(f"🔧 Calling tool: {function_name}")
                    print(f"   Arguments: {json.dumps(arguments, indent=2)}")
                    
                    # Execute the tool
                    result = self.execute_tool(function_name, arguments)
                    
                    # Add tool result to messages
                    messages.append({
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": function_name,
                        "content": json.dumps(result)
                    })
                
            else:
                # No more tool calls, agent is done
                final_response = response_message.content
                print(f"\n✅ Agent completed task!")
                print(f"📝 Final response: {final_response}\n")
                return final_response
        
        print("\n⚠️  Max iterations reached")
        return "Task incomplete - max iterations reached"

# Demo usage
if __name__ == "__main__":
    agent = ToolUsingAgent()
    
    # Test scenarios
    tasks = [
        "Query the sales data for Q1 2024 and if revenue is below $50k, send a warning alert",
        "Run the data transformation notebook and then trigger the analytics pipeline",
        "Check the latest customer data and create a summary report"
    ]
    
    for task in tasks:
        agent.run(task)
        print("\n" + "="*80 + "\n")
```

**Tasks**:
1. Run the agent with different complex tasks
2. Add new tools (e.g., send_email, update_dashboard)
3. Implement actual Fabric API calls instead of mocks
4. Add retry logic and error handling

---

### Exercise 3: Multi-Agent System (90 minutes)

Create a system where multiple specialized agents collaborate to solve complex problems.

**File**: `exercise3_multi_agent.py`

```python
"""
Exercise 3: Multi-Agent System
A system with multiple specialized agents that collaborate to solve complex tasks.
"""

from openai import AzureOpenAI
import os
import json
from typing import List, Dict, Any
from enum import Enum

class AgentRole(Enum):
    """Define different agent roles."""
    COORDINATOR = "coordinator"
    DATA_ANALYST = "data_analyst"
    ML_ENGINEER = "ml_engineer"
    PIPELINE_OPERATOR = "pipeline_operator"

class Message:
    """Message passed between agents."""
    def __init__(self, sender: str, receiver: str, content: str, metadata: Dict = None):
        self.sender = sender
        self.receiver = receiver
        self.content = content
        self.metadata = metadata or {}
    
    def to_dict(self):
        return {
            "sender": self.sender,
            "receiver": self.receiver,
            "content": self.content,
            "metadata": self.metadata
        }

class BaseAgent:
    """Base class for all agents."""
    
    def __init__(self, name: str, role: AgentRole, system_prompt: str):
        self.name = name
        self.role = role
        self.system_prompt = system_prompt
        self.message_history: List[Message] = []
        
        self.client = AzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            api_version="2024-02-01",
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
        )
        self.deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
    
    def receive_message(self, message: Message):
        """Receive a message from another agent."""
        self.message_history.append(message)
        print(f"📨 {self.name} received message from {message.sender}")
    
    def process(self, input_data: str) -> str:
        """Process input and generate response."""
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": input_data}
        ]
        
        response = self.client.chat.completions.create(
            model=self.deployment,
            messages=messages,
            temperature=0.7,
            max_tokens=1000
        )
        
        return response.choices[0].message.content
    
    def send_message(self, receiver: str, content: str, metadata: Dict = None) -> Message:
        """Send a message to another agent."""
        message = Message(self.name, receiver, content, metadata)
        print(f"📤 {self.name} sending message to {receiver}")
        return message

class CoordinatorAgent(BaseAgent):
    """Orchestrates other agents to accomplish complex tasks."""
    
    def __init__(self):
        super().__init__(
            name="Coordinator",
            role=AgentRole.COORDINATOR,
            system_prompt="""You are a coordinator agent managing a team of specialized agents.
            You have access to:
            - Data Analyst: Can query and analyze data
            - ML Engineer: Can train and deploy ML models
            - Pipeline Operator: Can manage data pipelines
            
            Break down complex tasks into subtasks and assign them to appropriate agents.
            Coordinate their work and synthesize the final result."""
        )
    
    def plan_task(self, task: str) -> List[Dict]:
        """Break down a complex task into subtasks."""
        planning_prompt = f"""
        Task: {task}
        
        Break this down into specific subtasks for the specialist agents.
        Return a JSON list of subtasks with format:
        [{{"agent": "agent_name", "subtask": "description", "dependencies": []}}]
        """
        
        plan_text = self.process(planning_prompt)
        
        # Parse the plan (simplified - add better parsing in production)
        try:
            # Extract JSON from response
            start = plan_text.find('[')
            end = plan_text.rfind(']') + 1
            plan = json.loads(plan_text[start:end])
            return plan
        except:
            # Fallback simple plan
            return [
                {"agent": "DataAnalyst", "subtask": "Analyze the data", "dependencies": []},
                {"agent": "MLEngineer", "subtask": "Build model if needed", "dependencies": ["DataAnalyst"]},
                {"agent": "PipelineOperator", "subtask": "Deploy solution", "dependencies": ["MLEngineer"]}
            ]

class DataAnalystAgent(BaseAgent):
    """Specialized agent for data analysis."""
    
    def __init__(self):
        super().__init__(
            name="DataAnalyst",
            role=AgentRole.DATA_ANALYST,
            system_prompt="""You are a data analyst agent working with Microsoft Fabric.
            You can query lakehouses, warehouses, and perform statistical analysis.
            Provide clear, data-driven insights."""
        )
    
    def analyze_data(self, query: str) -> Dict:
        """Analyze data based on a query."""
        analysis_prompt = f"""
        Analyze: {query}
        
        Provide:
        1. Key findings
        2. Statistical summary
        3. Recommended next steps
        """
        
        result = self.process(analysis_prompt)
        return {
            "analysis": result,
            "status": "complete",
            "agent": self.name
        }

class MLEngineerAgent(BaseAgent):
    """Specialized agent for ML tasks."""
    
    def __init__(self):
        super().__init__(
            name="MLEngineer",
            role=AgentRole.ML_ENGINEER,
            system_prompt="""You are an ML engineer agent working with Microsoft Fabric.
            You can design, train, and deploy machine learning models.
            Focus on practical, production-ready solutions."""
        )
    
    def design_model(self, requirements: str) -> Dict:
        """Design an ML model based on requirements."""
        design_prompt = f"""
        Requirements: {requirements}
        
        Design an ML model including:
        1. Model architecture
        2. Training approach
        3. Evaluation metrics
        4. Deployment strategy
        """
        
        result = self.process(design_prompt)
        return {
            "design": result,
            "status": "complete",
            "agent": self.name
        }

class PipelineOperatorAgent(BaseAgent):
    """Specialized agent for pipeline operations."""
    
    def __init__(self):
        super().__init__(
            name="PipelineOperator",
            role=AgentRole.PIPELINE_OPERATOR,
            system_prompt="""You are a pipeline operator agent managing data workflows.
            You can create, trigger, and monitor Data Factory pipelines.
            Ensure reliability and efficiency."""
        )
    
    def deploy_pipeline(self, specifications: str) -> Dict:
        """Deploy a data pipeline."""
        deploy_prompt = f"""
        Specifications: {specifications}
        
        Plan pipeline deployment including:
        1. Pipeline activities
        2. Schedule and triggers
        3. Monitoring strategy
        4. Error handling
        """
        
        result = self.process(deploy_prompt)
        return {
            "deployment_plan": result,
            "status": "complete",
            "agent": self.name
        }

class MultiAgentSystem:
    """Orchestrates multiple agents to solve complex tasks."""
    
    def __init__(self):
        self.coordinator = CoordinatorAgent()
        self.agents = {
            "DataAnalyst": DataAnalystAgent(),
            "MLEngineer": MLEngineerAgent(),
            "PipelineOperator": PipelineOperatorAgent()
        }
        self.message_bus: List[Message] = []
    
    def route_message(self, message: Message):
        """Route a message to the appropriate agent."""
        if message.receiver in self.agents:
            self.agents[message.receiver].receive_message(message)
        self.message_bus.append(message)
    
    def execute_task(self, task: str) -> Dict:
        """Execute a complex task using multiple agents."""
        print("\n" + "="*70)
        print(f"🎯 Multi-Agent System - Task: {task}")
        print("="*70 + "\n")
        
        # Step 1: Coordinator plans the task
        print("📋 Coordinator creating execution plan...")
        plan = self.coordinator.plan_task(task)
        print(f"Plan created with {len(plan)} subtasks\n")
        
        results = {}
        
        # Step 2: Execute subtasks in order
        for i, subtask in enumerate(plan):
            agent_name = subtask["agent"]
            subtask_desc = subtask["subtask"]
            
            print(f"🔄 Executing subtask {i+1}/{len(plan)}")
            print(f"   Agent: {agent_name}")
            print(f"   Task: {subtask_desc}\n")
            
            if agent_name in self.agents:
                agent = self.agents[agent_name]
                
                # Different agents have different methods
                if isinstance(agent, DataAnalystAgent):
                    result = agent.analyze_data(subtask_desc)
                elif isinstance(agent, MLEngineerAgent):
                    result = agent.design_model(subtask_desc)
                elif isinstance(agent, PipelineOperatorAgent):
                    result = agent.deploy_pipeline(subtask_desc)
                else:
                    result = {"status": "unknown agent type"}
                
                results[agent_name] = result
                print(f"   ✅ Completed\n")
        
        # Step 3: Coordinator synthesizes final result
        print("🔄 Coordinator synthesizing results...")
        synthesis_prompt = f"""
        Task: {task}
        
        Agent Results:
        {json.dumps(results, indent=2)}
        
        Provide a final summary and recommendations.
        """
        
        final_result = self.coordinator.process(synthesis_prompt)
        
        print("\n" + "="*70)
        print("✅ Multi-Agent Task Complete")
        print("="*70)
        print(f"\n{final_result}\n")
        
        return {
            "task": task,
            "plan": plan,
            "agent_results": results,
            "final_result": final_result
        }

# Demo usage
if __name__ == "__main__":
    system = MultiAgentSystem()
    
    # Complex task requiring multiple agents
    tasks = [
        """Analyze customer churn data in the lakehouse, build a predictive model,
        and deploy an automated pipeline that scores new customers daily.""",
        
        """Investigate anomalies in the sales data from the past week,
        determine if a model update is needed, and set up monitoring."""
    ]
    
    for task in tasks:
        result = system.execute_task(task)
        print("\n" + "="*80 + "\n")
```

**Tasks**:
1. Run the multi-agent system with sample tasks
2. Add a new specialized agent (e.g., Security Agent, Cost Optimizer)
3. Implement agent-to-agent direct communication
4. Add a shared memory system for agents
5. Implement parallel execution of independent subtasks

---

### Exercise 4: Agent Memory and State Management (60 minutes)

Implement persistent memory so agents can remember past interactions and learn over time.

**File**: `exercise4_agent_memory.py`

```python
"""
Exercise 4: Agent Memory and State Management
Implement memory systems for agents to maintain context and learn from interactions.
"""

import os
import json
from datetime import datetime
from typing import List, Dict, Optional
from openai import AzureOpenAI
from dataclasses import dataclass, asdict
import hashlib

@dataclass
class MemoryEntry:
    """A single memory entry."""
    timestamp: str
    type: str  # "conversation", "action", "observation", "learning"
    content: str
    metadata: Dict
    embedding: Optional[List[float]] = None
    importance: float = 0.5
    
    def to_dict(self):
        return asdict(self)

class MemorySystem:
    """Manages agent memory with different memory types."""
    
    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.short_term_memory: List[MemoryEntry] = []  # Recent interactions
        self.long_term_memory: List[MemoryEntry] = []   # Important memories
        self.working_memory: Dict[str, any] = {}         # Current context
        
        self.client = AzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            api_version="2024-02-01",
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
        )
    
    def add_memory(self, memory_type: str, content: str, metadata: Dict = None):
        """Add a new memory entry."""
        memory = MemoryEntry(
            timestamp=datetime.now().isoformat(),
            type=memory_type,
            content=content,
            metadata=metadata or {},
            importance=self._calculate_importance(content)
        )
        
        # Generate embedding for semantic search
        memory.embedding = self._generate_embedding(content)
        
        # Add to short-term memory
        self.short_term_memory.append(memory)
        
        # Consolidate if short-term memory is full
        if len(self.short_term_memory) > 20:
            self._consolidate_memory()
    
    def _generate_embedding(self, text: str) -> List[float]:
        """Generate embedding for semantic search."""
        try:
            response = self.client.embeddings.create(
                model=os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT", "text-embedding-ada-002"),
                input=text
            )
            return response.data[0].embedding
        except Exception as e:
            print(f"Warning: Could not generate embedding: {e}")
            return []
    
    def _calculate_importance(self, content: str) -> float:
        """Calculate importance score of a memory (simplified)."""
        # In production, use more sophisticated methods
        keywords = ["error", "critical", "success", "failure", "learned"]
        importance = 0.5
        
        for keyword in keywords:
            if keyword.lower() in content.lower():
                importance += 0.1
        
        return min(importance, 1.0)
    
    def _consolidate_memory(self):
        """Move important short-term memories to long-term."""
        # Sort by importance
        self.short_term_memory.sort(key=lambda m: m.importance, reverse=True)
        
        # Move top 5 most important to long-term
        to_promote = self.short_term_memory[:5]
        self.long_term_memory.extend(to_promote)
        
        # Keep only recent 10 in short-term
        self.short_term_memory = self.short_term_memory[5:15]
        
        print(f"💾 Consolidated memory: {len(to_promote)} moved to long-term")
    
    def retrieve_relevant_memories(self, query: str, top_k: int = 5) -> List[MemoryEntry]:
        """Retrieve memories relevant to a query using semantic search."""
        query_embedding = self._generate_embedding(query)
        
        if not query_embedding:
            # Fallback to recent memories
            all_memories = self.short_term_memory + self.long_term_memory
            return all_memories[-top_k:]
        
        # Calculate similarity scores
        all_memories = self.short_term_memory + self.long_term_memory
        scored_memories = []
        
        for memory in all_memories:
            if memory.embedding:
                similarity = self._cosine_similarity(query_embedding, memory.embedding)
                scored_memories.append((similarity, memory))
        
        # Sort by similarity and return top_k
        scored_memories.sort(reverse=True, key=lambda x: x[0])
        return [memory for _, memory in scored_memories[:top_k]]
    
    def _cosine_similarity(self, a: List[float], b: List[float]) -> float:
        """Calculate cosine similarity between two vectors."""
        if not a or not b or len(a) != len(b):
            return 0.0
        
        dot_product = sum(x * y for x, y in zip(a, b))
        magnitude_a = sum(x * x for x in a) ** 0.5
        magnitude_b = sum(x * x for x in b) ** 0.5
        
        if magnitude_a == 0 or magnitude_b == 0:
            return 0.0
        
        return dot_product / (magnitude_a * magnitude_b)
    
    def save_to_fabric(self, lakehouse_path: str):
        """Save memory to Fabric lakehouse for persistence."""
        memory_data = {
            "agent_id": self.agent_id,
            "short_term": [m.to_dict() for m in self.short_term_memory],
            "long_term": [m.to_dict() for m in self.long_term_memory],
            "working": self.working_memory,
            "saved_at": datetime.now().isoformat()
        }
        
        # In production, save to actual Fabric lakehouse
        filename = f"/tmp/{self.agent_id}_memory.json"
        with open(filename, 'w') as f:
            json.dump(memory_data, f, indent=2)
        
        print(f"💾 Memory saved to {filename}")
    
    def load_from_fabric(self, lakehouse_path: str):
        """Load memory from Fabric lakehouse."""
        filename = f"/tmp/{self.agent_id}_memory.json"
        
        try:
            with open(filename, 'r') as f:
                memory_data = json.load(f)
            
            # Restore memories (without embeddings for simplicity)
            self.short_term_memory = [
                MemoryEntry(**m) for m in memory_data.get("short_term", [])
            ]
            self.long_term_memory = [
                MemoryEntry(**m) for m in memory_data.get("long_term", [])
            ]
            self.working_memory = memory_data.get("working", {})
            
            print(f"💾 Memory loaded: {len(self.short_term_memory)} short-term, {len(self.long_term_memory)} long-term")
        except FileNotFoundError:
            print("💾 No saved memory found, starting fresh")

class MemoryEnabledAgent:
    """An agent with memory capabilities."""
    
    def __init__(self, name: str):
        self.name = name
        self.memory = MemorySystem(name)
        
        self.client = AzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            api_version="2024-02-01",
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
        )
        self.deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
    
    def process_with_memory(self, user_input: str) -> str:
        """Process user input with memory context."""
        print(f"\n{'='*60}")
        print(f"🤖 {self.name} processing with memory")
        print(f"{'='*60}\n")
        
        # Retrieve relevant memories
        relevant_memories = self.memory.retrieve_relevant_memories(user_input)
        
        memory_context = "\n".join([
            f"- [{m.type}] {m.content}" for m in relevant_memories
        ])
        
        print(f"🧠 Retrieved {len(relevant_memories)} relevant memories\n")
        
        # Build prompt with memory context
        system_prompt = f"""You are {self.name}, an AI agent with memory.
        
        Here are relevant memories from past interactions:
        {memory_context}
        
        Use these memories to provide more contextual and personalized responses."""
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ]
        
        response = self.client.chat.completions.create(
            model=self.deployment,
            messages=messages,
            temperature=0.7
        )
        
        agent_response = response.choices[0].message.content
        
        # Store this interaction in memory
        self.memory.add_memory(
            "conversation",
            f"User: {user_input} | Agent: {agent_response}",
            {"user_input": user_input, "response": agent_response}
        )
        
        print(f"💬 Response: {agent_response}\n")
        return agent_response
    
    def learn_from_feedback(self, feedback: str):
        """Learn from user feedback."""
        print(f"📚 Learning from feedback: {feedback}")
        
        self.memory.add_memory(
            "learning",
            f"Feedback received: {feedback}",
            {"type": "user_feedback"}
        )
        
        # In production, use this to fine-tune models or update behavior

# Demo usage
if __name__ == "__main__":
    agent = MemoryEnabledAgent("MemoryBot")
    
    # Simulate a conversation with memory
    interactions = [
        "My name is Alice and I work in sales analytics",
        "What's the best way to analyze customer churn?",
        "Remember my department?",  # Testing memory recall
        "Create a dashboard for my team"  # Testing context awareness
    ]
    
    for user_input in interactions:
        print(f"\n👤 User: {user_input}")
        agent.process_with_memory(user_input)
    
    # Provide feedback
    agent.learn_from_feedback("The churn analysis suggestions were very helpful!")
    
    # Save memory
    agent.memory.save_to_fabric("lakehouse_path")
    
    print("\n" + "="*60)
    print("Memory System Demo Complete")
    print("="*60)
```

**Tasks**:
1. Run the memory-enabled agent with sample conversations
2. Test memory retrieval across multiple sessions
3. Implement episodic memory (specific events)
4. Add semantic memory (facts and knowledge)
5. Create memory pruning strategies for efficiency

---

### Exercise 5: Agent Monitoring and Evaluation (45 minutes)

Build monitoring and evaluation systems to track agent performance and reliability.

**File**: `exercise5_agent_monitoring.py`

```python
"""
Exercise 5: Agent Monitoring and Evaluation
Monitor agent performance, track metrics, and evaluate agent behavior.
"""

import os
import json
import time
from datetime import datetime
from typing import Dict, List
from dataclasses import dataclass, asdict
from enum import Enum

class AgentStatus(Enum):
    IDLE = "idle"
    PROCESSING = "processing"
    ERROR = "error"
    COMPLETED = "completed"

@dataclass
class AgentMetrics:
    """Metrics for agent performance."""
    agent_name: str
    total_tasks: int = 0
    successful_tasks: int = 0
    failed_tasks: int = 0
    total_tokens_used: int = 0
    total_cost_usd: float = 0.0
    average_latency_seconds: float = 0.0
    error_rate: float = 0.0
    
    def to_dict(self):
        return asdict(self)

@dataclass
class TaskLog:
    """Log entry for a task execution."""
    task_id: str
    agent_name: str
    timestamp: str
    task_description: str
    status: AgentStatus
    latency_seconds: float
    tokens_used: int
    cost_usd: float
    error_message: str = ""
    result_quality_score: float = 0.0
    
    def to_dict(self):
        return {
            **asdict(self),
            "status": self.status.value
        }

class AgentMonitor:
    """Monitors agent performance and collects metrics."""
    
    def __init__(self):
        self.metrics: Dict[str, AgentMetrics] = {}
        self.task_logs: List[TaskLog] = []
        self.start_time = datetime.now()
    
    def start_task(self, agent_name: str, task_id: str, task_description: str):
        """Log the start of a task."""
        if agent_name not in self.metrics:
            self.metrics[agent_name] = AgentMetrics(agent_name=agent_name)
        
        return {
            "task_id": task_id,
            "start_time": time.time()
        }
    
    def end_task(self, agent_name: str, task_id: str, task_description: str,
                 status: AgentStatus, start_time: float, tokens_used: int = 0,
                 error_message: str = ""):
        """Log the completion of a task."""
        end_time = time.time()
        latency = end_time - start_time
        
        # Calculate cost (simplified - adjust for actual pricing)
        cost_per_1k_tokens = 0.002  # GPT-4 pricing
        cost = (tokens_used / 1000) * cost_per_1k_tokens
        
        # Create task log
        log = TaskLog(
            task_id=task_id,
            agent_name=agent_name,
            timestamp=datetime.now().isoformat(),
            task_description=task_description,
            status=status,
            latency_seconds=latency,
            tokens_used=tokens_used,
            cost_usd=cost,
            error_message=error_message
        )
        
        self.task_logs.append(log)
        
        # Update metrics
        metrics = self.metrics[agent_name]
        metrics.total_tasks += 1
        
        if status == AgentStatus.COMPLETED:
            metrics.successful_tasks += 1
        elif status == AgentStatus.ERROR:
            metrics.failed_tasks += 1
        
        metrics.total_tokens_used += tokens_used
        metrics.total_cost_usd += cost
        
        # Update average latency
        total_latency = metrics.average_latency_seconds * (metrics.total_tasks - 1) + latency
        metrics.average_latency_seconds = total_latency / metrics.total_tasks
        
        # Update error rate
        metrics.error_rate = metrics.failed_tasks / metrics.total_tasks
        
        print(f"📊 Task {task_id} logged: {status.value} ({latency:.2f}s, {tokens_used} tokens)")
    
    def get_agent_metrics(self, agent_name: str) -> Dict:
        """Get metrics for a specific agent."""
        if agent_name not in self.metrics:
            return {}
        return self.metrics[agent_name].to_dict()
    
    def get_all_metrics(self) -> Dict:
        """Get metrics for all agents."""
        return {
            name: metrics.to_dict()
            for name, metrics in self.metrics.items()
        }
    
    def generate_report(self) -> str:
        """Generate a comprehensive monitoring report."""
        report = []
        report.append("=" * 70)
        report.append("AGENT MONITORING REPORT")
        report.append("=" * 70)
        report.append(f"Report Time: {datetime.now().isoformat()}")
        report.append(f"Monitoring Since: {self.start_time.isoformat()}")
        report.append("")
        
        for agent_name, metrics in self.metrics.items():
            report.append(f"\n📊 Agent: {agent_name}")
            report.append("-" * 70)
            report.append(f"Total Tasks: {metrics.total_tasks}")
            report.append(f"Successful: {metrics.successful_tasks} ({metrics.successful_tasks/max(metrics.total_tasks,1)*100:.1f}%)")
            report.append(f"Failed: {metrics.failed_tasks} ({metrics.error_rate*100:.1f}%)")
            report.append(f"Avg Latency: {metrics.average_latency_seconds:.2f}s")
            report.append(f"Total Tokens: {metrics.total_tokens_used:,}")
            report.append(f"Total Cost: ${metrics.total_cost_usd:.4f}")
        
        report.append("\n" + "=" * 70)
        return "\n".join(report)
    
    def export_to_fabric(self, workspace_id: str):
        """Export metrics to Fabric for visualization."""
        export_data = {
            "timestamp": datetime.now().isoformat(),
            "metrics": self.get_all_metrics(),
            "task_logs": [log.to_dict() for log in self.task_logs]
        }
        
        # In production, write to Fabric lakehouse or warehouse
        filename = f"/tmp/agent_metrics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w') as f:
            json.dump(export_data, f, indent=2)
        
        print(f"📊 Metrics exported to {filename}")
        return export_data

class AgentEvaluator:
    """Evaluates agent behavior and output quality."""
    
    def __init__(self):
        from openai import AzureOpenAI
        self.client = AzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            api_version="2024-02-01",
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
        )
        self.deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
    
    def evaluate_response(self, task: str, agent_response: str, expected_output: str = None) -> Dict:
        """Evaluate the quality of an agent's response."""
        print(f"\n🔍 Evaluating agent response...")
        
        eval_prompt = f"""
        Task: {task}
        Agent Response: {agent_response}
        {f"Expected Output: {expected_output}" if expected_output else ""}
        
        Evaluate the agent's response on these criteria (score 0-10 each):
        1. Correctness: Is the response factually correct?
        2. Completeness: Does it fully address the task?
        3. Clarity: Is it clear and well-structured?
        4. Relevance: Is it relevant to the task?
        
        Return a JSON object with scores and overall feedback.
        Format: {{"correctness": X, "completeness": X, "clarity": X, "relevance": X, "feedback": "..."}}
        """
        
        response = self.client.chat.completions.create(
            model=self.deployment,
            messages=[
                {"role": "system", "content": "You are an expert evaluator of AI agent performance."},
                {"role": "user", "content": eval_prompt}
            ],
            temperature=0.3
        )
        
        eval_text = response.choices[0].message.content
        
        # Parse evaluation (simplified)
        try:
            start = eval_text.find('{')
            end = eval_text.rfind('}') + 1
            evaluation = json.loads(eval_text[start:end])
        except:
            evaluation = {
                "correctness": 7,
                "completeness": 7,
                "clarity": 7,
                "relevance": 7,
                "feedback": "Could not parse evaluation"
            }
        
        # Calculate overall score
        scores = [evaluation.get(k, 0) for k in ["correctness", "completeness", "clarity", "relevance"]]
        evaluation["overall_score"] = sum(scores) / len(scores)
        
        print(f"✅ Overall Score: {evaluation['overall_score']:.1f}/10")
        print(f"   Feedback: {evaluation.get('feedback', 'N/A')}")
        
        return evaluation

# Demo usage
if __name__ == "__main__":
    monitor = AgentMonitor()
    evaluator = AgentEvaluator()
    
    # Simulate agent tasks
    agents = ["DataAgent", "MLAgent", "PipelineAgent"]
    
    for i in range(10):
        agent = agents[i % len(agents)]
        task_id = f"task_{i+1}"
        task_desc = f"Process data batch {i+1}"
        
        # Start task
        task_context = monitor.start_task(agent, task_id, task_desc)
        
        # Simulate task execution
        time.sleep(0.1)  # Simulate work
        
        # Randomly succeed or fail
        import random
        status = AgentStatus.COMPLETED if random.random() > 0.2 else AgentStatus.ERROR
        tokens = random.randint(100, 500)
        error = "Connection timeout" if status == AgentStatus.ERROR else ""
        
        # End task
        monitor.end_task(
            agent, task_id, task_desc,
            status, task_context["start_time"],
            tokens, error
        )
    
    # Generate report
    print("\n")
    print(monitor.generate_report())
    
    # Export metrics
    monitor.export_to_fabric("workspace_id")
    
    # Evaluate a sample response
    print("\n" + "="*70)
    sample_evaluation = evaluator.evaluate_response(
        task="Analyze customer churn data",
        agent_response="Based on the analysis, churn rate is 15% with key factors being price sensitivity and lack of engagement.",
        expected_output="Analysis should include churn rate, key factors, and recommendations"
    )
    
    print("\n" + "="*70)
    print("Monitoring and Evaluation Demo Complete")
    print("="*70)
```

**Tasks**:
1. Run the monitoring system with sample agents
2. Create visualizations of metrics in Power BI
3. Implement alerting for high error rates
4. Add cost tracking and budget limits
5. Create automated evaluation pipelines

---

## Additional Resources

### Sample Data

Located in `../assets/data/`:
- `customer_data.csv` - Customer demographics and behavior
- `sales_transactions.parquet` - Sales data for analysis
- `product_catalog.json` - Product information
- `event_logs.json` - System event logs for monitoring

### Helper Scripts

Located in `../assets/scripts/`:
- `setup_fabric_workspace.py` - Automate workspace setup
- `deploy_agent.py` - Deploy agents to Fabric
- `test_agent_tools.py` - Test agent capabilities
- `monitor_dashboard.py` - Real-time monitoring dashboard

### Best Practices

1. **Start Simple**: Begin with single-agent systems before building multi-agent
2. **Test Thoroughly**: Use evaluation frameworks to validate agent behavior
3. **Monitor Costs**: Track token usage and set budgets
4. **Handle Errors**: Implement robust error handling and retries
5. **Security First**: Never expose credentials; use managed identities
6. **Iterate**: Continuously improve agents based on feedback
7. **Document**: Keep clear documentation of agent capabilities and limitations

## Assessment

To complete this module, demonstrate:

1. ✅ A working single-purpose agent
2. ✅ A tool-using agent with at least 3 functions
3. ✅ A multi-agent system solving a complex task
4. ✅ Agent memory persistence and retrieval
5. ✅ Comprehensive monitoring and evaluation

## Common Issues and Solutions

### Issue: Agent loops infinitely
**Solution**: Implement max iterations and timeout limits

### Issue: High token costs
**Solution**: Use prompt caching, smaller models for simple tasks, and set token limits

### Issue: Agents make incorrect decisions
**Solution**: Improve prompts, add validation steps, use chain-of-thought reasoning

### Issue: Memory grows too large
**Solution**: Implement memory consolidation and pruning strategies

## Next Steps

Congratulations on completing the Agentic Workloads module! Next:

1. Explore [Module 9: Advanced Scenarios](../09-advanced-scenarios/README.md)
2. Review [Best Practices Guide](../assets/best-practices.md)
3. Check out [Industry Use Cases](../assets/use-cases.md)
4. Join the [Community Forum](https://github.com/ralphke/Fabric/discussions)

## Certification

After completing all exercises, you can:
- Generate a completion certificate
- Share your agents in the community showcase
- Contribute your learnings back to the lab

---

[← Back to Lab Home](../README.md) | [Next: Module 9 - Advanced Scenarios →](../09-advanced-scenarios/README.md)
