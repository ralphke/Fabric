# Module 4: Data Science and ML Models

## Overview
Build machine learning models in Microsoft Fabric that agents can use for predictions and decision-making.

## Duration
⏱️ Estimated time: 2 hours

## Learning Objectives
- Create ML experiments in Fabric
- Train models with MLflow
- Deploy models for inference
- Integrate models with agents

## Key Topics

### 1. ML in Fabric
- Data Science workspace
- Notebooks for ML
- MLflow integration

### 2. Model Training
- Data preparation
- Model selection
- Hyperparameter tuning
- Evaluation metrics

### 3. Model Deployment
- Registering models
- Creating endpoints
- Batch vs. real-time inference

### 4. Models for Agents
- Prediction APIs
- Model metadata
- Agent-model integration patterns

## Hands-On Exercises

### Exercise 1: Train a Classification Model
Build a customer churn prediction model.

### Exercise 2: Deploy Model Endpoint
Create an inference endpoint agents can call.

### Exercise 3: Agent-Model Integration
Build an agent that uses ML models for decisions.

## Sample Code

```python
# Train and register a model
import mlflow
from sklearn.ensemble import RandomForestClassifier

# Train model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Log with MLflow
with mlflow.start_run():
    mlflow.sklearn.log_model(model, "churn_model")
    mlflow.log_metrics({"accuracy": 0.92})

# Agent can now call this model
def agent_predict(customer_id):
    model = mlflow.sklearn.load_model("models:/churn_model/latest")
    customer_data = get_customer_features(customer_id)
    prediction = model.predict([customer_data])
    return prediction
```

## Assessment
- Train a production-ready model
- Create inference endpoint
- Integrate model with an agent

---

[← Back to Module 3](../03-data-engineering/README.md) | [Next: Module 5 →](../05-data-warehouse/README.md)
