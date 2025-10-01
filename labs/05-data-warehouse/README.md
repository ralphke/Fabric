# Module 5: Data Warehouse and SQL Analytics

## Overview
Learn to create and query data warehouses in Microsoft Fabric for structured analytics.

## Duration
⏱️ Estimated time: 1.5 hours

## Learning Objectives
- Create a Fabric Data Warehouse
- Design star schemas
- Write optimized T-SQL queries
- Enable agent SQL access

## Key Topics

### 1. Warehouse Fundamentals
- Creating a warehouse
- Tables and schemas
- Loading data

### 2. SQL Optimization
- Indexing strategies
- Query performance
- Statistics management

### 3. Semantic Models
- Creating semantic layers
- Relationships and measures
- DAX basics

### 4. Agent-Warehouse Integration
- SQL query generation by agents
- Secure access patterns
- Query result handling

## Hands-On Exercises

### Exercise 1: Create Star Schema
Build a dimensional model for sales data.

### Exercise 2: Complex Queries
Write analytical queries for common business questions.

### Exercise 3: Agent SQL Interface
Enable agents to query the warehouse.

## Sample Code

```sql
-- Create a warehouse table
CREATE TABLE sales_fact (
    sale_id INT PRIMARY KEY,
    date_key INT,
    customer_key INT,
    product_key INT,
    amount DECIMAL(10,2)
);

-- Agent can query this
-- Python agent code:
import pyodbc

class WarehouseAgent:
    def query_sales(self, filter_condition):
        query = f"""
        SELECT 
            SUM(amount) as total_sales,
            COUNT(*) as transaction_count
        FROM sales_fact
        WHERE {filter_condition}
        """
        return self.execute_query(query)
```

## Assessment
- Design and implement a dimensional model
- Create optimized queries
- Build agent with SQL capabilities

---

[← Back to Module 4](../04-data-science/README.md) | [Next: Module 6 →](../06-real-time-analytics/README.md)
