"""
Setup script for Microsoft Fabric workspace
Automates the initial workspace configuration
"""

import os
import sys
from azure.identity import DefaultAzureCredential
import requests
import json

def setup_fabric_workspace():
    """Create and configure a Fabric workspace for the lab."""
    
    print("=" * 60)
    print("Microsoft Fabric Workspace Setup")
    print("=" * 60)
    
    # Authenticate
    print("\n1. Authenticating with Azure...")
    try:
        credential = DefaultAzureCredential()
        token = credential.get_token("https://analysis.windows.net/powerbi/api/.default")
        print("   ✅ Authentication successful")
    except Exception as e:
        print(f"   ❌ Authentication failed: {e}")
        return False
    
    # Setup headers
    headers = {
        "Authorization": f"Bearer {token.token}",
        "Content-Type": "application/json"
    }
    
    # Create workspace
    print("\n2. Creating workspace 'fabric-agentic-lab'...")
    workspace_data = {
        "name": "fabric-agentic-lab",
        "description": "Workspace for Fabric Agentic Workloads Lab"
    }
    
    try:
        response = requests.post(
            "https://api.fabric.microsoft.com/v1/workspaces",
            headers=headers,
            json=workspace_data
        )
        
        if response.status_code in [200, 201]:
            workspace = response.json()
            workspace_id = workspace.get('id')
            print(f"   ✅ Workspace created: {workspace_id}")
        elif response.status_code == 409:
            print("   ℹ️  Workspace already exists")
            # Get existing workspace
            response = requests.get(
                "https://api.fabric.microsoft.com/v1/workspaces",
                headers=headers
            )
            workspaces = response.json().get('value', [])
            workspace_id = next(
                (w['id'] for w in workspaces if w['name'] == 'fabric-agentic-lab'),
                None
            )
        else:
            print(f"   ❌ Failed to create workspace: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    # Create Lakehouse
    print("\n3. Creating Lakehouse 'agents_lakehouse'...")
    lakehouse_data = {
        "displayName": "agents_lakehouse",
        "description": "Lakehouse for agent data"
    }
    
    try:
        response = requests.post(
            f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/lakehouses",
            headers=headers,
            json=lakehouse_data
        )
        
        if response.status_code in [200, 201]:
            print("   ✅ Lakehouse created")
        else:
            print(f"   ℹ️  Lakehouse may already exist or creation pending")
    except Exception as e:
        print(f"   ⚠️  Lakehouse creation: {e}")
    
    # Save configuration
    print("\n4. Saving configuration...")
    config = {
        "workspace_id": workspace_id,
        "workspace_name": "fabric-agentic-lab",
        "lakehouse_name": "agents_lakehouse",
        "created_at": str(datetime.now())
    }
    
    with open("fabric_config.json", "w") as f:
        json.dump(config, f, indent=2)
    
    print("   ✅ Configuration saved to fabric_config.json")
    
    print("\n" + "=" * 60)
    print("✅ Setup Complete!")
    print("=" * 60)
    print(f"\nWorkspace ID: {workspace_id}")
    print("\nNext steps:")
    print("1. Navigate to https://app.fabric.microsoft.com")
    print("2. Open the 'fabric-agentic-lab' workspace")
    print("3. Continue with Module 1 exercises")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    from datetime import datetime
    
    success = setup_fabric_workspace()
    sys.exit(0 if success else 1)
