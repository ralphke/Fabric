# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   }
# META }

# MARKDOWN ********************

# # CI/CD for Microsoft Fabric
# 
# This notebook demonstrates implementing Continuous Integration and Continuous Deployment (CI/CD) practices for Microsoft Fabric solutions.
# 
# ## What is CI/CD for Fabric?
# 
# CI/CD for Fabric enables:
# - **Version Control**: Track changes to Fabric items using Git
# - **Automated Testing**: Validate changes before deployment
# - **Deployment Automation**: Push changes across environments
# - **Collaboration**: Enable team-based development
# - **Rollback Capabilities**: Quickly revert problematic changes

# MARKDOWN ********************

# ## Prerequisites
# 
# To implement CI/CD for Fabric, you need:
# - Azure DevOps or GitHub repository
# - Multiple Fabric workspaces (Dev, Test, Prod)
# - Fabric capacity with Git integration enabled
# - Service Principal or managed identity
# - Appropriate permissions

# MARKDOWN ********************

# ## 1. Git Integration Setup
# 
# ### Connecting Fabric to Git:
# 1. Navigate to Workspace settings
# 2. Select "Git integration"
# 3. Connect to Azure DevOps or GitHub
# 4. Select repository and branch
# 5. Configure folder structure
# 
# ### Supported Items:
# - Notebooks
# - Lakehouses
# - Data Pipelines
# - Semantic Models
# - Reports
# - Dataflows

# MARKDOWN ********************

# ## 2. Fabric Item Structure in Git
# 
# Understanding how Fabric items are stored in Git:

# CELL ********************

import os
import json

# Example folder structure for Fabric items in Git
fabric_git_structure = """
Repository/
├── .fabric/
│   └── config.json
├── Notebooks/
│   ├── DataTransform.Notebook/
│   │   ├── notebook-content.py
│   │   └── .platform
│   └── Analysis.Notebook/
│       ├── notebook-content.py
│       └── .platform
├── DataPipelines/
│   └── ETL_Pipeline.DataPipeline/
│       ├── pipeline-content.json
│       └── .platform
├── Lakehouses/
│   └── SalesLakehouse.Lakehouse/
│       ├── lakehouse-content.json
│       └── .platform
├── SemanticModels/
│   └── SalesModel.SemanticModel/
│       ├── model.bim
│       └── .platform
└── Reports/
    └── SalesDashboard.Report/
        ├── report.json
        └── .platform
"""

print("Fabric Git Repository Structure:")
print(fabric_git_structure)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## 3. Environment Configuration
# 
# Managing different environments (Dev, Test, Prod):

# CELL ********************

# Environment configuration file example
environments = {
    "development": {
        "workspace_id": "dev-workspace-guid",
        "capacity_name": "dev-capacity",
        "lakehouse_name": "dev_lakehouse",
        "storage_account": "devstorageaccount",
        "key_vault": "dev-keyvault",
        "service_principal_id": "dev-sp-id",
        "tenant_id": "your-tenant-id"
    },
    "test": {
        "workspace_id": "test-workspace-guid",
        "capacity_name": "test-capacity",
        "lakehouse_name": "test_lakehouse",
        "storage_account": "teststorageaccount",
        "key_vault": "test-keyvault",
        "service_principal_id": "test-sp-id",
        "tenant_id": "your-tenant-id"
    },
    "production": {
        "workspace_id": "prod-workspace-guid",
        "capacity_name": "prod-capacity",
        "lakehouse_name": "prod_lakehouse",
        "storage_account": "prodstorageaccount",
        "key_vault": "prod-keyvault",
        "service_principal_id": "prod-sp-id",
        "tenant_id": "your-tenant-id"
    }
}

print("Environment Configurations:")
print(json.dumps(environments, indent=2))

# Save as JSON file
os.makedirs('/tmp/cicd_config', exist_ok=True)
with open('/tmp/cicd_config/environments.json', 'w') as f:
    json.dump(environments, f, indent=2)
print("\n✓ Configuration saved to /tmp/cicd_config/environments.json")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## 4. Azure DevOps Pipeline (YAML)
# 
# Example CI/CD pipeline using Azure DevOps:

# CELL ********************

# Azure DevOps Pipeline YAML
azure_devops_pipeline = """
# azure-pipelines.yml
trigger:
  branches:
    include:
    - main
    - develop
  paths:
    include:
    - Notebooks/*
    - DataPipelines/*
    - SemanticModels/*

variables:
  - group: fabric-dev-variables
  - name: pythonVersion
    value: '3.10'

stages:
- stage: Build
  displayName: 'Build and Validate'
  jobs:
  - job: Validate
    displayName: 'Validate Fabric Items'
    pool:
      vmImage: 'ubuntu-latest'
    steps:
    - task: UsePythonVersion@0
      inputs:
        versionSpec: $(pythonVersion)
      displayName: 'Use Python $(pythonVersion)'
    
    - script: |
        pip install pytest nbformat nbconvert semantic-link-labs
      displayName: 'Install dependencies'
    
    - script: |
        python scripts/validate_notebooks.py
      displayName: 'Validate Notebooks'
    
    - script: |
        python scripts/validate_pipelines.py
      displayName: 'Validate Pipelines'
    
    - task: PublishTestResults@2
      inputs:
        testResultsFiles: '**/test-results.xml'
      displayName: 'Publish Test Results'

- stage: DeployDev
  displayName: 'Deploy to Dev'
  dependsOn: Build
  condition: and(succeeded(), eq(variables['Build.SourceBranch'], 'refs/heads/develop'))
  jobs:
  - deployment: DeployToDev
    displayName: 'Deploy to Dev Workspace'
    environment: 'fabric-dev'
    pool:
      vmImage: 'ubuntu-latest'
    strategy:
      runOnce:
        deploy:
          steps:
          - checkout: self
          
          - task: AzureCLI@2
            inputs:
              azureSubscription: 'fabric-service-connection'
              scriptType: 'bash'
              scriptLocation: 'inlineScript'
              inlineScript: |
                echo "Deploying to Dev workspace..."
                python scripts/deploy_to_fabric.py --environment dev
            displayName: 'Deploy to Dev'

- stage: DeployProd
  displayName: 'Deploy to Production'
  dependsOn: DeployDev
  condition: and(succeeded(), eq(variables['Build.SourceBranch'], 'refs/heads/main'))
  jobs:
  - deployment: DeployToProd
    displayName: 'Deploy to Prod Workspace'
    environment: 'fabric-prod'
    pool:
      vmImage: 'ubuntu-latest'
    strategy:
      runOnce:
        deploy:
          steps:
          - checkout: self
          
          - task: AzureCLI@2
            inputs:
              azureSubscription: 'fabric-service-connection'
              scriptType: 'bash'
              scriptLocation: 'inlineScript'
              inlineScript: |
                echo "Deploying to Production workspace..."
                python scripts/deploy_to_fabric.py --environment prod
            displayName: 'Deploy to Production'
          
          - script: |
              python scripts/run_smoke_tests.py
            displayName: 'Run Smoke Tests'
"""

print("Azure DevOps Pipeline YAML:")
print(azure_devops_pipeline)

# Save to file
with open('/tmp/cicd_config/azure-pipelines.yml', 'w') as f:
    f.write(azure_devops_pipeline)
print("\n✓ Pipeline saved to /tmp/cicd_config/azure-pipelines.yml")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## 5. GitHub Actions Workflow
# 
# Alternative CI/CD using GitHub Actions:

# CELL ********************

# GitHub Actions workflow
github_actions_workflow = """
# .github/workflows/fabric-cicd.yml
name: Fabric CI/CD

on:
  push:
    branches:
      - main
      - develop
    paths:
      - 'Notebooks/**'
      - 'DataPipelines/**'
      - 'SemanticModels/**'
  pull_request:
    branches:
      - main

env:
  PYTHON_VERSION: '3.10'

jobs:
  validate:
    name: Validate Fabric Items
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: ${{ env.PYTHON_VERSION }}
      
      - name: Install dependencies
        run: |
          pip install pytest nbformat nbconvert semantic-link-labs
      
      - name: Validate notebooks
        run: |
          python scripts/validate_notebooks.py
      
      - name: Validate pipelines
        run: |
          python scripts/validate_pipelines.py
      
      - name: Run unit tests
        run: |
          pytest tests/ --junitxml=test-results.xml
      
      - name: Publish test results
        uses: EnricoMi/publish-unit-test-result-action@v2
        if: always()
        with:
          files: test-results.xml

  deploy-dev:
    name: Deploy to Dev
    needs: validate
    if: github.ref == 'refs/heads/develop'
    runs-on: ubuntu-latest
    environment:
      name: development
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: ${{ env.PYTHON_VERSION }}
      
      - name: Azure Login
        uses: azure/login@v1
        with:
          creds: ${{ secrets.AZURE_CREDENTIALS }}
      
      - name: Deploy to Dev workspace
        run: |
          python scripts/deploy_to_fabric.py --environment dev
        env:
          WORKSPACE_ID: ${{ secrets.DEV_WORKSPACE_ID }}
          CLIENT_ID: ${{ secrets.DEV_CLIENT_ID }}
          CLIENT_SECRET: ${{ secrets.DEV_CLIENT_SECRET }}
          TENANT_ID: ${{ secrets.TENANT_ID }}

  deploy-prod:
    name: Deploy to Production
    needs: validate
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    environment:
      name: production
      url: https://app.fabric.microsoft.com
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: ${{ env.PYTHON_VERSION }}
      
      - name: Azure Login
        uses: azure/login@v1
        with:
          creds: ${{ secrets.AZURE_CREDENTIALS }}
      
      - name: Deploy to Production workspace
        run: |
          python scripts/deploy_to_fabric.py --environment prod
        env:
          WORKSPACE_ID: ${{ secrets.PROD_WORKSPACE_ID }}
          CLIENT_ID: ${{ secrets.PROD_CLIENT_ID }}
          CLIENT_SECRET: ${{ secrets.PROD_CLIENT_SECRET }}
          TENANT_ID: ${{ secrets.TENANT_ID }}
      
      - name: Run smoke tests
        run: |
          python scripts/run_smoke_tests.py
"""

print("GitHub Actions Workflow:")
print(github_actions_workflow)

# Save to file
with open('/tmp/cicd_config/fabric-cicd.yml', 'w') as f:
    f.write(github_actions_workflow)
print("\n✓ Workflow saved to /tmp/cicd_config/fabric-cicd.yml")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## 6. Validation Scripts
# 
# Scripts to validate Fabric items before deployment:

# CELL ********************

# Notebook validation script
notebook_validator = '''
#!/usr/bin/env python3
"""Validate Fabric notebooks"""

import os
import sys
import json
import nbformat
from pathlib import Path

def validate_notebook(notebook_path):
    """Validate a single notebook"""
    errors = []
    
    try:
        # Read notebook
        with open(notebook_path, 'r', encoding='utf-8') as f:
            nb = nbformat.read(f, as_version=4)
        
        # Check 1: Has cells
        if len(nb.cells) == 0:
            errors.append("Notebook has no cells")
        
        # Check 2: Has markdown documentation
        markdown_cells = [c for c in nb.cells if c.cell_type == 'markdown']
        if len(markdown_cells) == 0:
            errors.append("No documentation found")
        
        # Check 3: No output in cells (clean notebook)
        for i, cell in enumerate(nb.cells):
            if cell.cell_type == 'code' and cell.get('outputs'):
                errors.append(f"Cell {i} has output (should be cleared)")
        
        # Check 4: No hardcoded credentials
        dangerous_strings = ['password', 'secret', 'key=', 'token=']
        for i, cell in enumerate(nb.cells):
            if cell.cell_type == 'code':
                source = cell.source.lower()
                for danger in dangerous_strings:
                    if danger in source and '#' not in source[:source.index(danger)]:
                        errors.append(f"Cell {i} may contain credentials")
        
        return len(errors) == 0, errors
    
    except Exception as e:
        return False, [f"Error reading notebook: {str(e)}"]

def main():
    """Validate all notebooks"""
    notebook_dir = Path("Notebooks")
    
    if not notebook_dir.exists():
        print("No Notebooks directory found")
        return 0
    
    all_valid = True
    notebooks = list(notebook_dir.rglob("*.ipynb"))
    
    print(f"Validating {len(notebooks)} notebooks...\\n")
    
    for nb_path in notebooks:
        valid, errors = validate_notebook(nb_path)
        
        if valid:
            print(f"✓ {nb_path.name}")
        else:
            print(f"✗ {nb_path.name}")
            for error in errors:
                print(f"  - {error}")
            all_valid = False
    
    return 0 if all_valid else 1

if __name__ == "__main__":
    sys.exit(main())
'''

print("Notebook Validation Script:")
print(notebook_validator)

# Save to file
with open('/tmp/cicd_config/validate_notebooks.py', 'w') as f:
    f.write(notebook_validator)
print("\n✓ Script saved to /tmp/cicd_config/validate_notebooks.py")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Pipeline validation script
pipeline_validator = '''
#!/usr/bin/env python3
"""Validate Fabric data pipelines"""

import os
import sys
import json
from pathlib import Path

def validate_pipeline(pipeline_path):
    """Validate a single pipeline definition"""
    errors = []
    
    try:
        with open(pipeline_path, 'r', encoding='utf-8') as f:
            pipeline = json.load(f)
        
        # Check 1: Has activities
        if 'properties' not in pipeline or 'activities' not in pipeline['properties']:
            errors.append("Pipeline has no activities")
        else:
            activities = pipeline['properties']['activities']
            
            # Check 2: All activities have names
            for i, activity in enumerate(activities):
                if 'name' not in activity:
                    errors.append(f"Activity {i} has no name")
                if 'type' not in activity:
                    errors.append(f"Activity {i} has no type")
        
        # Check 3: No hardcoded connections
        pipeline_str = json.dumps(pipeline)
        if 'AccountKey' in pipeline_str or 'Password' in pipeline_str:
            errors.append("Pipeline may contain hardcoded credentials")
        
        return len(errors) == 0, errors
    
    except Exception as e:
        return False, [f"Error reading pipeline: {str(e)}"]

def main():
    """Validate all pipelines"""
    pipeline_dir = Path("DataPipelines")
    
    if not pipeline_dir.exists():
        print("No DataPipelines directory found")
        return 0
    
    all_valid = True
    pipelines = list(pipeline_dir.rglob("pipeline-content.json"))
    
    print(f"Validating {len(pipelines)} pipelines...\\n")
    
    for pipeline_path in pipelines:
        valid, errors = validate_pipeline(pipeline_path)
        
        if valid:
            print(f"✓ {pipeline_path.parent.name}")
        else:
            print(f"✗ {pipeline_path.parent.name}")
            for error in errors:
                print(f"  - {error}")
            all_valid = False
    
    return 0 if all_valid else 1

if __name__ == "__main__":
    sys.exit(main())
'''

print("Pipeline Validation Script:")
print(pipeline_validator)

# Save to file
with open('/tmp/cicd_config/validate_pipelines.py', 'w') as f:
    f.write(pipeline_validator)
print("\n✓ Script saved to /tmp/cicd_config/validate_pipelines.py")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## 7. Deployment Script
# 
# Script to deploy Fabric items using REST API:

# CELL ********************

# Deployment script
deployment_script = '''
#!/usr/bin/env python3
"""Deploy Fabric items to workspace"""

import os
import sys
import json
import argparse
import requests
from pathlib import Path
from azure.identity import DefaultAzureCredential, ClientSecretCredential

class FabricDeployer:
    """Deploy Fabric items using REST API"""
    
    def __init__(self, workspace_id, credential):
        self.workspace_id = workspace_id
        self.credential = credential
        self.base_url = "https://api.fabric.microsoft.com/v1"
        self.token = None
    
    def get_token(self):
        """Get access token"""
        if not self.token:
            self.token = self.credential.get_token(
                "https://api.fabric.microsoft.com/.default"
            ).token
        return self.token
    
    def deploy_notebook(self, notebook_path, notebook_name):
        """Deploy a notebook"""
        print(f"Deploying notebook: {notebook_name}")
        
        with open(notebook_path, 'r') as f:
            notebook_content = f.read()
        
        url = f"{self.base_url}/workspaces/{self.workspace_id}/notebooks"
        headers = {
            "Authorization": f"Bearer {self.get_token()}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "displayName": notebook_name,
            "definition": {
                "parts": [{
                    "path": "notebook-content.py",
                    "payload": notebook_content,
                    "payloadType": "InlineBase64"
                }]
            }
        }
        
        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code in [200, 201]:
            print(f"  ✓ Successfully deployed {notebook_name}")
            return True
        else:
            print(f"  ✗ Failed to deploy {notebook_name}: {response.text}")
            return False
    
    def deploy_pipeline(self, pipeline_path, pipeline_name):
        """Deploy a data pipeline"""
        print(f"Deploying pipeline: {pipeline_name}")
        
        with open(pipeline_path, 'r') as f:
            pipeline_content = json.load(f)
        
        url = f"{self.base_url}/workspaces/{self.workspace_id}/dataPipelines"
        headers = {
            "Authorization": f"Bearer {self.get_token()}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "displayName": pipeline_name,
            "definition": pipeline_content
        }
        
        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code in [200, 201]:
            print(f"  ✓ Successfully deployed {pipeline_name}")
            return True
        else:
            print(f"  ✗ Failed to deploy {pipeline_name}: {response.text}")
            return False

def main():
    parser = argparse.ArgumentParser(description='Deploy Fabric items')
    parser.add_argument('--environment', required=True, choices=['dev', 'test', 'prod'])
    args = parser.parse_args()
    
    # Load environment config
    with open('config/environments.json', 'r') as f:
        envs = json.load(f)
    
    env_config = envs.get(args.environment)
    if not env_config:
        print(f"Environment {args.environment} not found")
        return 1
    
    # Create credential
    if os.getenv('CLIENT_ID') and os.getenv('CLIENT_SECRET'):
        credential = ClientSecretCredential(
            tenant_id=env_config['tenant_id'],
            client_id=os.getenv('CLIENT_ID'),
            client_secret=os.getenv('CLIENT_SECRET')
        )
    else:
        credential = DefaultAzureCredential()
    
    deployer = FabricDeployer(env_config['workspace_id'], credential)
    
    print(f"\\nDeploying to {args.environment} environment...\\n")
    
    success = True
    
    # Deploy notebooks
    notebook_dir = Path("Notebooks")
    if notebook_dir.exists():
        for nb_path in notebook_dir.rglob("*.ipynb"):
            if not deployer.deploy_notebook(nb_path, nb_path.stem):
                success = False
    
    # Deploy pipelines
    pipeline_dir = Path("DataPipelines")
    if pipeline_dir.exists():
        for pipeline_path in pipeline_dir.rglob("pipeline-content.json"):
            pipeline_name = pipeline_path.parent.name.replace('.DataPipeline', '')
            if not deployer.deploy_pipeline(pipeline_path, pipeline_name):
                success = False
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
'''

print("Deployment Script:")
print(deployment_script)

# Save to file
with open('/tmp/cicd_config/deploy_to_fabric.py', 'w') as f:
    f.write(deployment_script)
print("\n✓ Script saved to /tmp/cicd_config/deploy_to_fabric.py")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## 8. Testing Strategy
# 
# Implement different types of tests:

# CELL ********************

# Unit test example for data transformation
unit_test_example = '''
# tests/test_transformations.py
import pytest
import pandas as pd
from pyspark.sql import SparkSession

# Import your transformation functions
# from notebooks.transformations import clean_data, aggregate_sales

@pytest.fixture
def spark():
    """Create Spark session for testing"""
    return SparkSession.builder \\
        .appName("unit-tests") \\
        .master("local[*]") \\
        .getOrCreate()

@pytest.fixture
def sample_data():
    """Create sample test data"""
    return pd.DataFrame({
        'id': [1, 2, 3, 4, 5],
        'value': [100, 200, None, 400, 500],
        'category': ['A', 'B', 'A', 'B', 'C']
    })

def test_data_cleaning(sample_data):
    """Test data cleaning removes null values"""
    # cleaned = clean_data(sample_data)
    # assert cleaned['value'].isnull().sum() == 0
    assert True  # Placeholder

def test_aggregation(sample_data):
    """Test aggregation produces correct results"""
    result = sample_data.groupby('category')['value'].sum()
    assert result['A'] == 100  # First value (null excluded)
    assert result['B'] == 600  # 200 + 400

def test_spark_transformation(spark, sample_data):
    """Test Spark transformation"""
    df = spark.createDataFrame(sample_data)
    assert df.count() == 5
    assert len(df.columns) == 3
'''

print("Unit Test Example:")
print(unit_test_example)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## 9. Best Practices
# 
# ### Version Control:
# 1. **Commit frequently** with meaningful messages
# 2. **Use branches** for features and fixes
# 3. **Code review** through pull requests
# 4. **Tag releases** for production deployments
# 
# ### Testing:
# 1. **Unit tests** for transformation logic
# 2. **Integration tests** for pipelines
# 3. **Smoke tests** after deployment
# 4. **Data quality tests** in pipelines
# 
# ### Security:
# 1. **Use Key Vault** for secrets
# 2. **Service Principals** for authentication
# 3. **Never commit credentials** to Git
# 4. **Implement RBAC** for workspaces
# 
# ### Deployment:
# 1. **Automated deployments** for consistency
# 2. **Environment parity** - keep configs similar
# 3. **Rollback plan** for failures
# 4. **Gradual rollout** for major changes

# MARKDOWN ********************

# ## 10. Monitoring and Alerting
# 
# Monitor your CI/CD pipeline:

# CELL ********************

# Monitoring configuration
monitoring_config = {
    "metrics_to_track": [
        "Deployment success rate",
        "Deployment duration",
        "Test pass rate",
        "Pipeline run frequency",
        "Failed deployment count"
    ],
    "alerts": [
        {
            "name": "Deployment Failure",
            "condition": "deployment_status == 'failed'",
            "action": "Send email to data-team@company.com",
            "severity": "High"
        },
        {
            "name": "Test Failure",
            "condition": "test_pass_rate < 95%",
            "action": "Send Teams notification",
            "severity": "Medium"
        },
        {
            "name": "Long Deployment",
            "condition": "deployment_duration > 30 minutes",
            "action": "Create incident ticket",
            "severity": "Low"
        }
    ],
    "dashboards": [
        {
            "name": "CI/CD Overview",
            "tiles": [
                "Recent deployments",
                "Success rate trend",
                "Average deployment time",
                "Active branches"
            ]
        }
    ]
}

print("Monitoring Configuration:")
print(json.dumps(monitoring_config, indent=2))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## Summary
# 
# In this notebook, we covered:
# - ✅ Git integration with Fabric workspaces
# - ✅ Environment configuration management
# - ✅ Azure DevOps pipeline setup
# - ✅ GitHub Actions workflow configuration
# - ✅ Validation scripts for notebooks and pipelines
# - ✅ Deployment automation using REST API
# - ✅ Testing strategies and examples
# - ✅ Best practices for CI/CD
# - ✅ Monitoring and alerting setup
# 
# ## Next Steps
# - Set up your Git repository
# - Configure service principals
# - Implement automated tests
# - Create deployment pipelines
# - Monitor and iterate
