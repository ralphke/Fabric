# Fabric notebook source


# MARKDOWN ********************

# # Power BI Semantic Models in Microsoft Fabric
# 
# This notebook demonstrates working with Power BI semantic models (formerly known as datasets) in Microsoft Fabric.
# 
# ## What are Semantic Models?
# 
# Semantic models in Fabric provide:
# - **Business logic layer** between raw data and reports
# - **Centralized metrics** and calculations (DAX measures)
# - **Security and governance** through row-level security (RLS)
# - **Optimized query performance** with data modeling
# - **Reusability** across multiple reports and applications

# MARKDOWN ********************

# ## Prerequisites
# 
# To run this notebook, you need:
# - A Microsoft Fabric workspace
# - Power BI Premium or Fabric capacity
# - A lakehouse or warehouse with data
# - Appropriate permissions

# MARKDOWN ********************

# ## 1. Preparing Data for Semantic Models
# 
# Let's create sample data that we'll use to build a semantic model:

# CELL ********************

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *

# Create sample dimensions and facts for a sales scenario
print("Creating sample star schema data...")

# Date dimension
start_date = datetime(2023, 1, 1)
dates = [start_date + timedelta(days=x) for x in range(365 * 2)]
dim_date = pd.DataFrame({
    'DateKey': [d.strftime('%Y%m%d') for d in dates],
    'Date': dates,
    'Year': [d.year for d in dates],
    'Quarter': [(d.month - 1) // 3 + 1 for d in dates],
    'Month': [d.month for d in dates],
    'MonthName': [d.strftime('%B') for d in dates],
    'DayOfWeek': [d.weekday() + 1 for d in dates],
    'DayName': [d.strftime('%A') for d in dates],
    'IsWeekend': [d.weekday() >= 5 for d in dates]
})

print(f"✓ Created Date dimension: {len(dim_date)} rows")
display(dim_date.head())

# CELL ********************

# Product dimension
products = [
    ('P001', 'Laptop Pro 15', 'Electronics', 'Computers', 1299.99),
    ('P002', 'Laptop Pro 13', 'Electronics', 'Computers', 999.99),
    ('P003', 'Smartphone X', 'Electronics', 'Mobile Devices', 899.99),
    ('P004', 'Tablet Plus', 'Electronics', 'Mobile Devices', 599.99),
    ('P005', 'Wireless Mouse', 'Accessories', 'Input Devices', 29.99),
    ('P006', 'Mechanical Keyboard', 'Accessories', 'Input Devices', 149.99),
    ('P007', 'USB-C Hub', 'Accessories', 'Connectivity', 49.99),
    ('P008', '4K Monitor', 'Electronics', 'Displays', 449.99),
    ('P009', 'Wireless Headphones', 'Accessories', 'Audio', 199.99),
    ('P010', 'External SSD 1TB', 'Accessories', 'Storage', 129.99)
]

dim_product = pd.DataFrame(products, columns=[
    'ProductKey', 'ProductName', 'Category', 'SubCategory', 'ListPrice'
])

print(f"✓ Created Product dimension: {len(dim_product)} rows")
display(dim_product)

# CELL ********************

# Customer dimension
np.random.seed(42)
customer_ids = [f'C{str(i).zfill(4)}' for i in range(1, 101)]
cities = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 'Philadelphia', 'San Antonio', 'San Diego']
segments = ['Consumer', 'Corporate', 'Home Office']

dim_customer = pd.DataFrame({
    'CustomerKey': customer_ids,
    'CustomerName': [f'Customer {i}' for i in range(1, 101)],
    'City': np.random.choice(cities, 100),
    'Segment': np.random.choice(segments, 100),
    'JoinDate': [start_date + timedelta(days=np.random.randint(0, 365)) for _ in range(100)]
})

print(f"✓ Created Customer dimension: {len(dim_customer)} rows")
display(dim_customer.head())

# CELL ********************

# Sales fact table
np.random.seed(42)
n_transactions = 5000

fact_sales_data = []
for i in range(n_transactions):
    date_key = np.random.choice(dim_date['DateKey'].values)
    product_key = np.random.choice(dim_product['ProductKey'].values)
    customer_key = np.random.choice(dim_customer['CustomerKey'].values)
    
    product_price = dim_product[dim_product['ProductKey'] == product_key]['ListPrice'].values[0]
    quantity = np.random.randint(1, 6)
    discount_pct = np.random.choice([0, 0.05, 0.10, 0.15, 0.20], p=[0.5, 0.2, 0.15, 0.10, 0.05])
    
    sales_amount = product_price * quantity * (1 - discount_pct)
    cost_amount = sales_amount * np.random.uniform(0.5, 0.7)
    
    fact_sales_data.append((
        f'S{str(i+1).zfill(6)}',
        date_key,
        product_key,
        customer_key,
        quantity,
        sales_amount,
        cost_amount,
        discount_pct * 100
    ))

fact_sales = pd.DataFrame(fact_sales_data, columns=[
    'SalesKey', 'DateKey', 'ProductKey', 'CustomerKey', 
    'Quantity', 'SalesAmount', 'CostAmount', 'DiscountPercent'
])

print(f"✓ Created Sales fact table: {len(fact_sales)} rows")
print(f"\nSales Summary:")
print(f"  Total Sales: ${fact_sales['SalesAmount'].sum():,.2f}")
print(f"  Total Quantity: {fact_sales['Quantity'].sum():,}")
print(f"  Average Order Value: ${fact_sales['SalesAmount'].mean():,.2f}")
display(fact_sales.head())

# MARKDOWN ********************

# ## 2. Saving Data to OneLake
# 
# Save the star schema tables to OneLake for use in semantic models:

# CELL ********************

# Convert to Spark DataFrames and save as Delta tables
tables = {
    'DimDate': dim_date,
    'DimProduct': dim_product,
    'DimCustomer': dim_customer,
    'FactSales': fact_sales
}

for table_name, df_pandas in tables.items():
    # Convert to Spark DataFrame
    df_spark = spark.createDataFrame(df_pandas)
    
    # Save as Delta table
    # df_spark.write.format("delta") \
    #     .mode("overwrite") \
    #     .save(f"Tables/{table_name}")
    
    print(f"✓ {table_name} ready to save ({len(df_pandas)} rows)")

print("\n✓ All tables prepared for semantic model")

# MARKDOWN ********************

# ## 3. Semantic Model Design Principles
# 
# ### Star Schema Design:
# - **Fact tables**: Contain measures (numerical values)
# - **Dimension tables**: Contain attributes for filtering and grouping
# - **Relationships**: Connect facts to dimensions via keys
# 
# ### Best Practices:
# 1. Use **surrogate keys** for relationships
# 2. Keep dimension tables **denormalized**
# 3. Create **date/calendar** dimension
# 4. Define clear **relationships** (one-to-many)
# 5. Use **meaningful names** for columns

# MARKDOWN ********************

# ## 4. Creating a Semantic Model
# 
# ### Via Power BI Desktop:
# 1. Open Power BI Desktop
# 2. Get Data → Lakehouse or Warehouse
# 3. Select your tables
# 4. Model the data:
#    - Define relationships
#    - Create hierarchies
#    - Add DAX measures
#    - Configure table properties
# 5. Publish to Fabric workspace
# 
# ### Via Fabric Portal:
# 1. Navigate to workspace
# 2. Create "Semantic Model" from Lakehouse
# 3. Select tables to include
# 4. Configure relationships
# 5. Add measures using DAX

# MARKDOWN ********************

# ## 5. Common DAX Measures
# 
# DAX (Data Analysis Expressions) is used to create calculated measures:

# CELL ********************

# Common DAX patterns (to be created in Power BI)
dax_measures = """
-- Basic Aggregations
Total Sales = SUM(FactSales[SalesAmount])
Total Quantity = SUM(FactSales[Quantity])
Total Cost = SUM(FactSales[CostAmount])

-- Calculated Measures
Profit = [Total Sales] - [Total Cost]
Profit Margin = DIVIDE([Profit], [Total Sales], 0)
Average Order Value = DIVIDE([Total Sales], DISTINCTCOUNT(FactSales[SalesKey]), 0)

-- Time Intelligence
Sales YTD = TOTALYTD([Total Sales], DimDate[Date])
Sales Previous Year = CALCULATE([Total Sales], SAMEPERIODLASTYEAR(DimDate[Date]))
Sales YoY Growth = 
    DIVIDE(
        [Total Sales] - [Sales Previous Year],
        [Sales Previous Year],
        0
    )

-- Moving Averages
Sales 3M MA = 
    CALCULATE(
        [Total Sales],
        DATESINPERIOD(DimDate[Date], LASTDATE(DimDate[Date]), -3, MONTH)
    ) / 3

-- Ranking
Product Rank = 
    RANKX(
        ALL(DimProduct[ProductName]),
        [Total Sales],
        ,
        DESC,
        DENSE
    )

-- Conditional Logic
High Value Sales = 
    CALCULATE(
        [Total Sales],
        FactSales[SalesAmount] > 500
    )

-- Distinct Counts
Customer Count = DISTINCTCOUNT(FactSales[CustomerKey])
Product Count = DISTINCTCOUNT(FactSales[ProductKey])

-- Percentage Calculations
% of Total Sales = 
    DIVIDE(
        [Total Sales],
        CALCULATE([Total Sales], ALL(DimProduct)),
        0
    )

-- Running Totals
Running Total Sales = 
    CALCULATE(
        [Total Sales],
        FILTER(
            ALL(DimDate[Date]),
            DimDate[Date] <= MAX(DimDate[Date])
        )
    )
"""

print("Common DAX Measures for Sales Semantic Model:")
print(dax_measures)

# MARKDOWN ********************

# ## 6. Implementing Calculations in Python
# 
# Let's demonstrate equivalent calculations in Python:

# CELL ********************

# Create a combined view for analysis
df_analysis = fact_sales.merge(dim_product, on='ProductKey') \
                       .merge(dim_customer, on='CustomerKey') \
                       .merge(dim_date, on='DateKey')

# Calculate key metrics
df_analysis['Profit'] = df_analysis['SalesAmount'] - df_analysis['CostAmount']
df_analysis['ProfitMargin'] = df_analysis['Profit'] / df_analysis['SalesAmount']

print("\nKey Metrics:")
metrics = {
    'Total Sales': df_analysis['SalesAmount'].sum(),
    'Total Profit': df_analysis['Profit'].sum(),
    'Average Profit Margin': df_analysis['ProfitMargin'].mean(),
    'Total Quantity': df_analysis['Quantity'].sum(),
    'Unique Customers': df_analysis['CustomerKey'].nunique(),
    'Unique Products': df_analysis['ProductKey'].nunique(),
    'Average Order Value': df_analysis['SalesAmount'].mean()
}

for metric, value in metrics.items():
    if 'Margin' in metric:
        print(f"  {metric}: {value:.2%}")
    elif '$' in str(value) or 'Sales' in metric or 'Profit' in metric or 'Value' in metric:
        print(f"  {metric}: ${value:,.2f}")
    else:
        print(f"  {metric}: {value:,.0f}")

# CELL ********************

# Sales by Category
category_sales = df_analysis.groupby('Category').agg({
    'SalesAmount': 'sum',
    'Profit': 'sum',
    'Quantity': 'sum',
    'SalesKey': 'count'
}).round(2)

category_sales.columns = ['Total Sales', 'Total Profit', 'Units Sold', 'Order Count']
category_sales['Profit Margin %'] = (category_sales['Total Profit'] / category_sales['Total Sales'] * 100).round(2)
category_sales = category_sales.sort_values('Total Sales', ascending=False)

print("\nSales by Category:")
display(category_sales)

# CELL ********************

# Top 10 Products by Sales
product_sales = df_analysis.groupby('ProductName').agg({
    'SalesAmount': 'sum',
    'Profit': 'sum',
    'Quantity': 'sum'
}).round(2)

product_sales.columns = ['Total Sales', 'Total Profit', 'Units Sold']
product_sales['Profit Margin %'] = (product_sales['Total Profit'] / product_sales['Total Sales'] * 100).round(2)
top_products = product_sales.sort_values('Total Sales', ascending=False).head(10)

print("\nTop 10 Products by Sales:")
display(top_products)

# CELL ********************

# Monthly Sales Trend
df_analysis['YearMonth'] = df_analysis['Date'].dt.to_period('M')
monthly_trend = df_analysis.groupby('YearMonth').agg({
    'SalesAmount': 'sum',
    'Profit': 'sum',
    'SalesKey': 'count'
}).round(2)

monthly_trend.columns = ['Total Sales', 'Total Profit', 'Order Count']
monthly_trend['Moving Avg (3M)'] = monthly_trend['Total Sales'].rolling(window=3).mean().round(2)

print("\nMonthly Sales Trend (Last 12 months):")
display(monthly_trend.tail(12))

# MARKDOWN ********************

# ## 7. Row-Level Security (RLS)
# 
# RLS ensures users only see data they're authorized to access:

# CELL ********************

# Example RLS patterns (to be implemented in Power BI)
rls_examples = """
-- Role: Regional Managers (see only their region's data)
-- In DimCustomer table:
[City] = USERPRINCIPALNAME()

-- Role: Sales Reps (see only their customers)
-- In DimCustomer table:
[SalesRep] = USERPRINCIPALNAME()

-- Role: Category Managers (see specific categories)
-- In DimProduct table:
[Category] IN { "Electronics", "Accessories" }

-- Dynamic Security using security table
-- In fact table:
[Region] IN 
    VALUES(
        FILTER(
            SecurityTable,
            SecurityTable[UserEmail] = USERPRINCIPALNAME()
        ),
        SecurityTable[Region]
    )
"""

print("Row-Level Security Examples:")
print(rls_examples)

# MARKDOWN ********************

# ## 8. Querying Semantic Models
# 
# ### Using XMLA Endpoint:
# Semantic models can be queried programmatically using the XMLA endpoint:

# CELL ********************

# Example: Querying semantic model using DAX
# Requires: pip install adodbapi or pyodbc

dax_query_example = """
// DAX Query Example
EVALUATE
SUMMARIZECOLUMNS(
    DimProduct[Category],
    DimDate[Year],
    "Total Sales", [Total Sales],
    "Profit", [Profit],
    "Profit Margin", [Profit Margin]
)
ORDER BY DimDate[Year], [Total Sales] DESC
"""

print("DAX Query Example:")
print(dax_query_example)

# Python code to execute DAX query would look like:
python_code = """
import adodbapi

connection_string = (
    "Provider=MSOLAP;"
    "Data Source=powerbi://api.powerbi.com/v1.0/myorg/MyWorkspace;"
    "Initial Catalog=MySemanticModel;"
)

# Use Azure AD authentication
conn = adodbapi.connect(connection_string)
cursor = conn.cursor()

dax_query = '''EVALUATE TOPN(10, DimProduct, [Total Sales])'''
cursor.execute(dax_query)
results = cursor.fetchall()
"""

print("\nPython Code for Querying Semantic Model:")
print(python_code)

# MARKDOWN ********************

# ## 9. Semantic Model Refresh
# 
# ### Refresh Types:
# 1. **Import Mode**: Data is cached, requires scheduled refresh
# 2. **DirectQuery**: Queries sent to source in real-time
# 3. **Composite**: Combines import and DirectQuery
# 
# ### Refresh Configuration:
# - Configure in Fabric portal settings
# - Set up to 48 refreshes per day (Premium)
# - Use incremental refresh for large tables
# - Monitor refresh history

# CELL ********************

# Example: Triggering refresh programmatically using Power BI REST API
rest_api_example = """
# Using Power BI REST API to refresh semantic model

import requests
from azure.identity import DefaultAzureCredential

# Get access token
credential = DefaultAzureCredential()
token = credential.get_token("https://analysis.windows.net/powerbi/api/.default")

# Define parameters
workspace_id = "YOUR_WORKSPACE_ID"
dataset_id = "YOUR_DATASET_ID"

# Trigger refresh
url = f"https://api.powerbi.com/v1.0/myorg/groups/{workspace_id}/datasets/{dataset_id}/refreshes"
headers = {
    "Authorization": f"Bearer {token.token}",
    "Content-Type": "application/json"
}

# Full refresh
response = requests.post(url, headers=headers, json={
    "notifyOption": "MailOnFailure"
})

# Check refresh status
status_url = f"{url}?$top=1"
status_response = requests.get(status_url, headers=headers)
print(status_response.json())
"""

print("Semantic Model Refresh via REST API:")
print(rest_api_example)

# MARKDOWN ********************

# ## 10. Best Practices
# 
# ### Data Modeling:
# 1. **Use star schema** over snowflake
# 2. **Minimize table count** - consolidate where possible
# 3. **Remove unused columns** to reduce model size
# 4. **Use appropriate data types** (integer vs. text)
# 5. **Create calculated columns** only when necessary
# 
# ### DAX Optimization:
# 1. **Use measures** instead of calculated columns when possible
# 2. **Avoid complex calculated columns** - do in source
# 3. **Use CALCULATE** efficiently
# 4. **Leverage variables** (VAR) for complex calculations
# 5. **Test performance** with DAX Studio
# 
# ### Refresh Strategy:
# 1. **Use incremental refresh** for large tables
# 2. **Partition historical data** separately
# 3. **Schedule refreshes** during off-peak hours
# 4. **Monitor and alert** on failures
# 
# ### Security:
# 1. **Implement RLS** for multi-tenant scenarios
# 2. **Test RLS** thoroughly with different users
# 3. **Use dynamic security** with security tables
# 4. **Document security** requirements

# MARKDOWN ********************

# ## Summary
# 
# In this notebook, we covered:
# - ✅ Semantic model concepts and benefits
# - ✅ Star schema design for analytics
# - ✅ Creating dimension and fact tables
# - ✅ Common DAX measures and calculations
# - ✅ Implementing business logic
# - ✅ Row-level security patterns
# - ✅ Querying semantic models programmatically
# - ✅ Refresh strategies and automation
# - ✅ Best practices for performance and governance
# 
# ## Next Steps
# - Learn about data pipeline orchestration
# - Implement CI/CD for semantic models
# - Create Power BI reports using semantic models
# - Explore advanced DAX patterns
