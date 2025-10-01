# Quick Start Guide

Get started with the Microsoft Fabric Agentic Workloads Lab in minutes!

## 🚀 Fast Track (5 minutes)

### 1. Clone the Repository
```bash
git clone https://github.com/ralphke/Fabric.git
cd Fabric
```

### 2. Set Up Python Environment
```bash
# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Azure OpenAI
Create a `.env` file in the root directory:
```bash
AZURE_OPENAI_ENDPOINT=https://your-endpoint.openai.azure.com/
AZURE_OPENAI_API_KEY=your-api-key-here
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4
AZURE_OPENAI_EMBEDDING_DEPLOYMENT=text-embedding-ada-002
```

### 4. Start Learning!

**Option A - Full Lab (16-20 hours)**
```bash
cd labs/01-setup
# Follow the README.md
```

**Option B - Jump to Agents (Quick)**
```bash
cd labs/08-agentic-workloads
# Run the first exercise
python exercise1_simple_agent.py
```

## 📚 Learning Paths

### Path 1: Complete Learning Journey
Best for comprehensive understanding:
1. Module 1: Setup → 1 hour
2. Module 2: Data Factory → 1.5 hours
3. Module 3: Data Engineering → 2 hours
4. Module 4: Data Science → 2 hours
5. Module 5: Data Warehouse → 1.5 hours
6. Module 6: Real-Time Analytics → 1.5 hours
7. Module 7: Power BI → 1.5 hours
8. **Module 8: Agentic Workloads** → 4-6 hours ⭐
9. Module 9: Advanced Scenarios → 2-3 hours

### Path 2: Agentic-Focused (Recommended)
For those who want to focus on building agents:
1. Module 1: Setup → 1 hour
2. Module 3: Data Engineering basics → 1 hour
3. Module 4: ML Models → 1 hour
4. **Module 8: Agentic Workloads** → 4-6 hours ⭐

### Path 3: Quick Prototype (2-3 hours)
Jump right into building:
1. Set up environment (above) → 30 min
2. Module 8, Exercise 1: Simple Agent → 45 min
3. Module 8, Exercise 2: Tool-Using Agent → 60 min
4. Experiment and extend! → ∞

## 🎯 Key Exercises

### Must-Try Exercises:
1. **Simple Data Agent** (`labs/08-agentic-workloads/exercise1_simple_agent.py`)
   - Build your first autonomous agent
   - Learn the perceive-reason-act loop

2. **Tool-Using Agent** (`labs/08-agentic-workloads/exercise2_tool_agent.py`)
   - Function calling and tool use
   - Real-world agent capabilities

3. **Multi-Agent System** (`labs/08-agentic-workloads/exercise3_multi_agent.py`)
   - Agent collaboration
   - Complex problem solving

4. **Agent Memory** (`labs/08-agentic-workloads/exercise4_agent_memory.py`)
   - Persistent context
   - Learning from interactions

5. **Agent Monitoring** (`labs/08-agentic-workloads/exercise5_agent_monitoring.py`)
   - Production monitoring
   - Performance evaluation

## 💡 Tips for Success

### Do:
✅ Start with simple agents before complex systems
✅ Read the module documentation before coding
✅ Experiment and modify the sample code
✅ Use the validation scripts to check your setup
✅ Join the community discussions

### Don't:
❌ Skip Module 1 setup - it's crucial
❌ Commit your .env file with credentials
❌ Use production API keys for testing
❌ Forget to set token limits on agents

## 🆘 Common Issues

### "Module not found" errors
```bash
# Ensure virtual environment is activated
pip install -r requirements.txt
```

### "Azure authentication failed"
```bash
# Login to Azure CLI
az login
az account show
```

### "OpenAI API key invalid"
- Double-check your .env file
- Ensure no extra spaces in the API key
- Verify the endpoint URL is correct

### "Fabric workspace not found"
- Complete Module 1 setup first
- Check workspace permissions in Azure Portal

## 📖 Documentation Structure

```
Fabric/
├── README.md                    ← You are here
├── QUICK_START.md              ← This guide
├── requirements.txt            ← Python dependencies
├── labs/
│   ├── README.md               ← Complete lab overview
│   ├── 01-setup/               ← Start here
│   ├── 02-data-factory/        
│   ├── 03-data-engineering/    
│   ├── 04-data-science/        
│   ├── 05-data-warehouse/      
│   ├── 06-real-time-analytics/ 
│   ├── 07-power-bi/            
│   ├── 08-agentic-workloads/   ← Core module ⭐
│   ├── 09-advanced-scenarios/  
│   └── assets/                 ← Sample data & scripts
└── LICENSE
```

## 🎓 What You'll Learn

By the end of this lab:
- ✅ Build autonomous AI agents
- ✅ Integrate agents with Fabric data platform
- ✅ Create multi-agent systems
- ✅ Implement production monitoring
- ✅ Deploy agents at scale

## 🌟 Showcase Your Work

Built something cool? Share it!
1. Create a GitHub Gist with your agent
2. Post in [Discussions](https://github.com/ralphke/Fabric/discussions)
3. Tag it with #FabricAgents

## 📞 Get Help

- **Issues**: [GitHub Issues](https://github.com/ralphke/Fabric/issues)
- **Questions**: [GitHub Discussions](https://github.com/ralphke/Fabric/discussions)
- **Docs**: [Microsoft Fabric Docs](https://learn.microsoft.com/fabric/)

## 🚀 Ready?

Choose your path and start building!

```bash
# Full experience
cd labs/01-setup

# Jump to agents
cd labs/08-agentic-workloads

# Let's go! 🎉
```

---

**Happy Learning!** 🤖💙
