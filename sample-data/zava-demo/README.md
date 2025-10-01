# Zava Demo Database - Sample Parquet Files

This directory contains sample data files in Apache Parquet format, representing a typical e-commerce database structure. These files can be used for testing, learning, and demonstration purposes with Microsoft Fabric and other data platforms.

## Files Overview

### 1. customers.parquet
Customer information table containing 100 sample customer records.

**Schema:**
- `customer_id` (int64): Unique customer identifier
- `first_name` (string): Customer's first name
- `last_name` (string): Customer's last name
- `email` (string): Customer's email address
- `phone` (string): Customer's phone number
- `city` (string): Customer's city
- `state` (string): Customer's state code
- `country` (string): Customer's country
- `registration_date` (string): Date when customer registered

**Record Count:** 100 customers

### 2. products.parquet
Product catalog containing 50 sample products across various categories.

**Schema:**
- `product_id` (int64): Unique product identifier
- `product_name` (string): Name of the product
- `category` (string): Product category (Electronics, Clothing, Home & Garden, Sports, Books, Toys, Food & Beverage)
- `price` (float64): Product price
- `stock_quantity` (int64): Available stock quantity
- `supplier` (string): Supplier name
- `created_date` (string): Date when product was added

**Record Count:** 50 products

### 3. orders.parquet
Order transactions containing 500 sample order records.

**Schema:**
- `order_id` (int64): Unique order identifier
- `customer_id` (int64): Customer who placed the order (foreign key to customers)
- `order_date` (string): Date when order was placed
- `order_status` (string): Current status (Pending, Processing, Shipped, Delivered, Cancelled)
- `total_amount` (float64): Total order amount
- `shipping_address` (string): Delivery address
- `payment_method` (string): Payment method used

**Record Count:** 500 orders

### 4. order_items.parquet
Individual items within orders, representing a many-to-many relationship between orders and products.

**Schema:**
- `order_item_id` (int64): Unique order item identifier
- `order_id` (int64): Order this item belongs to (foreign key to orders)
- `product_id` (int64): Product ordered (foreign key to products)
- `quantity` (int64): Quantity ordered
- `unit_price` (float64): Price per unit at time of order
- `discount` (float64): Discount applied (0.00 to 0.30)

**Record Count:** 1000 order items

### 5. sales_performance.parquet
Aggregated sales metrics by category and month.

**Schema:**
- `year_month` (string): Year and month (YYYY-MM format)
- `category` (string): Product category
- `total_sales` (float64): Total sales amount for the period
- `total_orders` (int64): Number of orders in the period
- `avg_order_value` (float64): Average order value
- `units_sold` (int64): Total units sold

**Record Count:** 84 records (12 months × 7 categories)

## Data Relationships

```
customers (1) ----< orders (M)
                      |
                      | (1)
                      |
                      < (M) order_items (M) >---- (1) products
```

## Usage Examples

### Reading with Python (pandas)
```python
import pandas as pd

# Read customers data
customers_df = pd.read_parquet('customers.parquet')
print(customers_df.head())

# Read all tables
tables = {
    'customers': pd.read_parquet('customers.parquet'),
    'products': pd.read_parquet('products.parquet'),
    'orders': pd.read_parquet('orders.parquet'),
    'order_items': pd.read_parquet('order_items.parquet'),
    'sales_performance': pd.read_parquet('sales_performance.parquet')
}
```

### Reading with Python (pyarrow)
```python
import pyarrow.parquet as pq

# Read customers data
table = pq.read_table('customers.parquet')
print(table.schema)
df = table.to_pandas()
```

### Using in Microsoft Fabric
1. Upload these parquet files to your Fabric Lakehouse
2. Create shortcuts or copy files to the Files section
3. Use Notebooks or SQL to query the data
4. Build reports and dashboards in Power BI

### Sample Queries

**Get top 10 customers by total spending:**
```sql
SELECT 
    c.customer_id,
    c.first_name,
    c.last_name,
    SUM(o.total_amount) as total_spent
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.first_name, c.last_name
ORDER BY total_spent DESC
LIMIT 10
```

**Get sales by category:**
```sql
SELECT 
    p.category,
    COUNT(DISTINCT o.order_id) as order_count,
    SUM(oi.quantity * oi.unit_price * (1 - oi.discount)) as revenue
FROM products p
JOIN order_items oi ON p.product_id = oi.product_id
JOIN orders o ON oi.order_id = o.order_id
GROUP BY p.category
ORDER BY revenue DESC
```

## Notes

- All data is randomly generated for demonstration purposes
- Date ranges: 2023-01-01 to 2023-12-31 for orders and 2022-2024 for products
- Data includes realistic relationships between tables
- Parquet format provides efficient storage and fast query performance
- Files are compressed and optimized for analytical workloads

## License

This sample data is provided under the same license as the repository (GPL v3).
