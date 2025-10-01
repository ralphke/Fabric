# Module 1: Environment Setup

## Overview

In this module, you'll set up your Microsoft Fabric workspace and prepare your environment for building agentic workloads. This foundational setup is crucial for all subsequent modules.

## Duration
⏱️ Estimated time: 1 hour

## Learning Objectives

By the end of this module, you will:
- Understand Microsoft Fabric licensing and capacity
- Create and configure a Fabric workspace
- Set up security and access controls
- Install necessary development tools
- Validate your environment setup

## Prerequisites

- Active Azure subscription
- Admin or contributor access to create resources
- Microsoft 365 account (for Power BI)

## Lab Steps

### Step 1: Enable Microsoft Fabric

1. **Activate Fabric Trial** (if you don't have a paid capacity)
   - Navigate to [Microsoft Fabric](https://app.fabric.microsoft.com)
   - Sign in with your Microsoft 365 account
   - Click your profile icon → **Start trial**
   - Select **Fabric (Free)** trial
   - Complete the trial activation

2. **Verify Fabric Capacity**
   ```
   - Go to Settings (⚙️) → Admin portal
   - Navigate to Capacity settings
   - Verify you have at least F2 capacity for agent workloads
   ```

### Step 2: Create Your Workspace

1. **Create a new workspace**:
   - Click **Workspaces** → **+ New workspace**
   - Name: `fabric-agentic-lab`
   - Description: `Workspace for agentic workloads lab`
   - Advanced settings:
     - License mode: **Fabric capacity** or **Trial**
     - Default storage format: **Small dataset storage format**

2. **Configure workspace settings**:
   - Navigate to workspace settings (⚙️)
   - **OneLake settings**: 
     - Enable shortcuts to external data sources
   - **Git integration** (optional for version control):
     - Connect to your Git repository

### Step 3: Set Up Security and Permissions

1. **Workspace roles**:
   ```
   Admin    - Full control (assign to yourself)
   Member   - Create, edit, share content
   Contributor - Create and edit, limited sharing
   Viewer   - Read-only access
   ```

2. **Add users** (if working in a team):
   - Go to workspace → **Manage access**
   - Add users with appropriate roles
   - Configure Row-Level Security (RLS) as needed

3. **Enable Service Principal** (for automation):
   - Azure Portal → Azure Active Directory
   - App registrations → New registration
   - Name: `fabric-agent-sp`
   - Note the Application (client) ID and create a client secret
   - Grant API permissions for Fabric

### Step 4: Install Development Tools

#### A. Python Environment

```bash
# Install Python 3.9 or higher
python --version

# Create virtual environment
python -m venv fabric-lab-env

# Activate environment
# Windows:
fabric-lab-env\Scripts\activate
# Linux/Mac:
source fabric-lab-env/bin/activate

# Install core packages
pip install --upgrade pip
pip install fabric-sdk
pip install azure-identity
pip install semantic-kernel
pip install openai
pip install langchain
pip install pandas
pip install pyarrow
pip install delta-spark
```

#### B. Azure CLI

```bash
# Install Azure CLI
# Windows: Download from https://aka.ms/installazurecliwindows
# Linux:
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
# Mac:
brew install azure-cli

# Login to Azure
az login

# Verify installation
az account show
```

#### C. VS Code Extensions (Recommended)

Install these VS Code extensions:
- Python
- Jupyter
- Azure Account
- Power BI (Preview)
- GitHub Copilot (optional, helpful for development)

#### D. Fabric REST API Access

```python
# Test Fabric API connectivity
from azure.identity import DefaultAzureCredential
import requests

# Authenticate
credential = DefaultAzureCredential()
token = credential.get_token("https://analysis.windows.net/powerbi/api/.default")

# Test API call
headers = {
    "Authorization": f"Bearer {token.token}",
    "Content-Type": "application/json"
}

response = requests.get(
    "https://api.fabric.microsoft.com/v1/workspaces",
    headers=headers
)

print(f"API Status: {response.status_code}")
```

### Step 5: Configure Azure OpenAI Service

For agentic workloads, you'll need access to Azure OpenAI:

1. **Create Azure OpenAI Resource**:
   ```bash
   az cognitiveservices account create \
     --name fabric-openai-agents \
     --resource-group fabric-lab-rg \
     --kind OpenAI \
     --sku S0 \
     --location eastus \
     --yes
   ```

2. **Deploy Models**:
   - Navigate to Azure OpenAI Studio
   - Deploy these models (minimum):
     - **gpt-4** or **gpt-4-turbo** (for agent reasoning)
     - **gpt-35-turbo** (for faster, cost-effective tasks)
     - **text-embedding-ada-002** (for semantic search)

3. **Store credentials**:
   ```python
   # Create .env file (DO NOT commit to Git)
   AZURE_OPENAI_ENDPOINT=https://fabric-openai-agents.openai.azure.com/
   AZURE_OPENAI_API_KEY=your_api_key_here
   AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4
   AZURE_OPENAI_EMBEDDING_DEPLOYMENT=text-embedding-ada-002
   ```

### Step 6: Create Sample Data Sources

1. **Upload sample data to OneLake**:
   - In your workspace, create a new **Lakehouse**: `agents_lakehouse`
   - Upload sample datasets:
     - Customer data
     - Sales transactions
     - Product catalog
     - Event logs

2. **Create connection to external sources** (optional):
   - Azure Data Lake Gen2
   - Azure SQL Database
   - Azure Cosmos DB
   - API endpoints

### Step 7: Validate Your Setup

Run this validation script to ensure everything is configured:

```python
"""
Fabric Environment Validation Script
Save as: validate_setup.py
"""

import os
import sys
from azure.identity import DefaultAzureCredential
import requests

def check_python_version():
    version = sys.version_info
    if version.major >= 3 and version.minor >= 9:
        print("✅ Python version OK:", sys.version.split()[0])
        return True
    else:
        print("❌ Python 3.9+ required. Current:", sys.version.split()[0])
        return False

def check_packages():
    required = ['fabric-sdk', 'azure-identity', 'semantic-kernel', 
                'openai', 'langchain', 'pandas']
    missing = []
    
    for package in required:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package} installed")
        except ImportError:
            missing.append(package)
            print(f"❌ {package} missing")
    
    return len(missing) == 0

def check_azure_auth():
    try:
        credential = DefaultAzureCredential()
        token = credential.get_token("https://management.azure.com/.default")
        print("✅ Azure authentication successful")
        return True
    except Exception as e:
        print(f"❌ Azure authentication failed: {e}")
        return False

def check_fabric_api():
    try:
        credential = DefaultAzureCredential()
        token = credential.get_token("https://analysis.windows.net/powerbi/api/.default")
        
        headers = {
            "Authorization": f"Bearer {token.token}",
            "Content-Type": "application/json"
        }
        
        response = requests.get(
            "https://api.fabric.microsoft.com/v1/workspaces",
            headers=headers
        )
        
        if response.status_code == 200:
            workspaces = response.json()
            print(f"✅ Fabric API accessible. Found {len(workspaces.get('value', []))} workspaces")
            return True
        else:
            print(f"❌ Fabric API error: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Fabric API connection failed: {e}")
        return False

def check_openai_config():
    endpoint = os.getenv('AZURE_OPENAI_ENDPOINT')
    api_key = os.getenv('AZURE_OPENAI_API_KEY')
    
    if endpoint and api_key:
        print("✅ Azure OpenAI configuration found")
        return True
    else:
        print("❌ Azure OpenAI configuration missing. Check .env file")
        return False

def main():
    print("=" * 50)
    print("Microsoft Fabric Environment Validation")
    print("=" * 50)
    
    checks = [
        ("Python Version", check_python_version),
        ("Required Packages", check_packages),
        ("Azure Authentication", check_azure_auth),
        ("Fabric API Access", check_fabric_api),
        ("OpenAI Configuration", check_openai_config)
    ]
    
    results = []
    for name, check_func in checks:
        print(f"\n🔍 Checking {name}...")
        results.append(check_func())
    
    print("\n" + "=" * 50)
    if all(results):
        print("🎉 All checks passed! Your environment is ready.")
        return 0
    else:
        print("⚠️  Some checks failed. Please review the output above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
```

Run the validation:
```bash
python validate_setup.py
```

## Configuration Files

Create these configuration files in your project root:

### config.yaml
```yaml
workspace:
  name: fabric-agentic-lab
  id: your-workspace-id
  capacity: F2

storage:
  lakehouse: agents_lakehouse
  warehouse: agents_warehouse

security:
  service_principal_id: your-sp-id
  tenant_id: your-tenant-id

agent_config:
  default_model: gpt-4
  temperature: 0.7
  max_tokens: 2000
  timeout_seconds: 120
```

### .env (DO NOT commit to Git)
```bash
# Azure credentials
AZURE_TENANT_ID=your-tenant-id
AZURE_CLIENT_ID=your-client-id
AZURE_CLIENT_SECRET=your-client-secret

# Fabric workspace
FABRIC_WORKSPACE_ID=your-workspace-id
FABRIC_CAPACITY_ID=your-capacity-id

# Azure OpenAI
AZURE_OPENAI_ENDPOINT=https://your-endpoint.openai.azure.com/
AZURE_OPENAI_API_KEY=your-api-key
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4
AZURE_OPENAI_EMBEDDING_DEPLOYMENT=text-embedding-ada-002
```

## Common Issues and Troubleshooting

### Issue 1: Fabric Trial Not Available
**Solution**: Check if your organization has disabled trial features. Contact your admin or use a personal Microsoft account.

### Issue 2: Permission Denied
**Solution**: Ensure you have at least Member role in the workspace and Contributor role in Azure subscription.

### Issue 3: API Authentication Fails
**Solution**: 
- Verify Azure CLI is logged in: `az account show`
- Check service principal permissions
- Regenerate authentication tokens

### Issue 4: Package Installation Errors
**Solution**:
```bash
# Use pip with --upgrade and --user flags
pip install --upgrade --user package-name

# Or try with conda
conda install -c conda-forge package-name
```

## Next Steps

Once your environment is set up and validated:
1. Review the [Architecture Overview](../assets/architecture.md)
2. Proceed to [Module 2: Data Factory](../02-data-factory/README.md)
3. Or jump directly to [Module 8: Agentic Workloads](../08-agentic-workloads/README.md) if you have prior Fabric experience

## Additional Resources

- [Microsoft Fabric Setup Guide](https://learn.microsoft.com/fabric/get-started/)
- [Azure OpenAI Service Documentation](https://learn.microsoft.com/azure/ai-services/openai/)
- [Fabric REST API Reference](https://learn.microsoft.com/rest/api/fabric/)
- [Python SDK for Fabric](https://pypi.org/project/fabric-sdk/)

## Checklist

Before moving to the next module, ensure you have:

- [ ] Activated Fabric capacity (trial or paid)
- [ ] Created `fabric-agentic-lab` workspace
- [ ] Configured workspace permissions
- [ ] Installed Python 3.9+ and required packages
- [ ] Set up Azure CLI and authenticated
- [ ] Deployed Azure OpenAI models
- [ ] Created .env file with credentials
- [ ] Run validation script successfully
- [ ] Created sample lakehouse

**Congratulations! Your environment is ready for building agentic workloads! 🎉**

[← Back to Lab Home](../README.md) | [Next: Module 2 - Data Factory →](../02-data-factory/README.md)
