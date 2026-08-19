# SQL Concepts — Practice Log

Week 1, Core Data Analytics Foundation. Practice queries run against `sql_practice.db` (tables: `customers`, `products`, `orders`, `order_items`) to learn each core SQL concept before applying them to the business task.

---

## 1. SELECT + WHERE

**Concept:** SELECT chooses which columns to return; WHERE filters which rows qualify.

```sql
SELECT customer_name, city, customer_type
FROM customers
WHERE state = 'Karnataka';
```

| customer_name | city | customer_type |
|---|---|---|
| Kavya Gupta | Bengaluru | Online |
| Rahul Reddy | Bengaluru | Retail |
| Vikram Kapoor | Bengaluru | Retail |
| Rohit Verma | Bengaluru | Wholesale |

**Combining conditions with AND:**

```sql
SELECT * FROM products WHERE category = 'Electronics' AND unit_price > 1000;
```

| product_id | product_name | category | unit_price |
|---|---|---|---|
| 2 | Bluetooth Speaker | Electronics | 1899.0 |
| 10 | Ergonomic Keyboard | Electronics | 2299.0 |
| 11 | Webcam HD | Electronics | 3499.0 |

**Filtering with not-equal:**

```sql
SELECT * FROM customers WHERE customer_type != 'Retail';
```
Returned 27 rows (all non-Retail customers — Online and Wholesale) — output omitted here for brevity, full result set verified during practice.

---

## 2. ORDER BY

**Concept:** sorts result rows; `DESC` = highest first, `ASC` = lowest first (default).

```sql
SELECT product_name, unit_price
FROM products
ORDER BY unit_price DESC;
```

| product_name | unit_price |
|---|---|
| Standing Desk | 12999.0 |
| Office Chair | 6499.0 |
| Filing Cabinet | 5999.0 |
| Webcam HD | 3499.0 |
| Whiteboard | 2499.0 |
| Ergonomic Keyboard | 2299.0 |
| Bluetooth Speaker | 1899.0 |
| Laptop Stand | 1299.0 |
| LED Desk Lamp | 899.0 |
| Wireless Mouse | 799.0 |
| USB-C Cable | 299.0 |
| Notebook Set | 199.0 |

---

## 3. Aggregate Functions

**Concept:** collapse a column into one summary value — SUM, AVG, COUNT, MAX, MIN.

```sql
SELECT SUM(quantity) FROM order_items;
```
Result: **1200**

```sql
SELECT AVG(unit_price) FROM products;
```
Result: **3265.67**

```sql
SELECT COUNT(*) FROM orders;
```
Result: **220**

```sql
SELECT MAX(unit_price), MIN(unit_price) FROM products;
```
Result: **Max 12999.0, Min 199.0**

---

## 4. GROUP BY

**Concept:** buckets rows by a shared value; aggregate functions then run separately per bucket instead of across the whole table.

```sql
SELECT category, COUNT(*) AS num_products, AVG(unit_price) AS avg_price
FROM products
GROUP BY category;
```

| category | num_products | avg_price |
|---|---|---|
| Electronics | 5 | 1759.00 |
| Furniture | 3 | 8499.00 |
| Office | 3 | 1565.67 |
| Stationery | 1 | 199.00 |

---

## 5. HAVING

**Concept:** filters *after* grouping, on the aggregated result — unlike WHERE, which filters raw rows before grouping.

```sql
SELECT category, COUNT(*) AS num_products
FROM products
GROUP BY category
HAVING COUNT(*) >= 3;
```

| category | num_products |
|---|---|
| Electronics | 5 |
| Furniture | 3 |
| Office | 3 |

(Stationery correctly dropped — only 1 product, below the threshold.)

---

## 6. JOINs

**Concept:** combines related rows across tables using a shared key column.

**INNER JOIN** — orders matched to their customer:

```sql
SELECT o.order_id, c.customer_name, o.order_date
FROM orders o
INNER JOIN customers c ON o.customer_id = c.customer_id
LIMIT 10;
```

| order_id | customer_name | order_date |
|---|---|---|
| 1 | Sneha Singh | 2025-01-03 |
| 2 | Vikram Reddy | 2025-08-22 |
| 3 | Sneha Singh | 2025-02-26 |
| 4 | Divya Nair | 2025-10-02 |
| 5 | Divya Rao | 2025-11-05 |

**Chained JOIN across 3 tables**, computing line-level revenue with the discount applied:

```sql
SELECT
    o.order_id,
    c.customer_name,
    p.product_name,
    oi.quantity,
    p.unit_price,
    ROUND(oi.quantity * p.unit_price * (1 - oi.discount_pct/100.0), 2) AS line_revenue
FROM order_items oi
JOIN orders o ON oi.order_id = o.order_id
JOIN customers c ON o.customer_id = c.customer_id
JOIN products p ON oi.product_id = p.product_id
LIMIT 10;
```

| order_id | customer_name | product_name | quantity | unit_price | line_revenue |
|---|---|---|---|---|---|
| 1 | Sneha Singh | LED Desk Lamp | 2 | 899.0 | 1618.20 |
| 1 | Sneha Singh | Ergonomic Keyboard | 2 | 2299.0 | 4598.00 |
| 1 | Sneha Singh | Filing Cabinet | 3 | 5999.0 | 16197.30 |
| 1 | Sneha Singh | Webcam HD | 5 | 3499.0 | 14870.75 |
| 2 | Vikram Reddy | Notebook Set | 2 | 199.0 | 378.10 |

**LEFT JOIN** — every customer kept, even with zero orders:

```sql
SELECT c.customer_name, COUNT(o.order_id) AS num_orders
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_name;
```

| customer_name | num_orders |
|---|---|
| Amit Gupta | 15 |
| Amit Singh | 10 |
| Ananya Gupta | 3 |
| Arjun Gupta | 1 |
| ... | ... |

(38 rows returned in total, one per customer.)

---

## 7. Subqueries

**Concept:** a query nested inside another; the inner query resolves first and its result feeds the outer query.

```sql
SELECT product_name, unit_price
FROM products
WHERE unit_price > (SELECT AVG(unit_price) FROM products);
```

| product_name | unit_price |
|---|---|
| Office Chair | 6499.0 |
| Standing Desk | 12999.0 |
| Webcam HD | 3499.0 |
| Filing Cabinet | 5999.0 |

Inner query computes the average price (3265.67) first; outer query returns only products priced above that.

---

## 8. Window Functions

**Concept:** compute an aggregate or ranking *without collapsing* individual rows — unlike GROUP BY, every original row stays visible alongside the calculated value.

**RANK()** — sequencing orders by date without merging rows:

```sql
SELECT
    order_id,
    customer_id,
    order_date,
    RANK() OVER (ORDER BY order_date) AS order_sequence
FROM orders
LIMIT 10;
```

| order_id | customer_id | order_date | order_sequence |
|---|---|---|---|
| 35 | 29 | 2025-01-02 | 1 |
| 1 | 19 | 2025-01-03 | 2 |
| 207 | 25 | 2025-01-12 | 3 |
| 111 | 9 | 2025-01-14 | 4 |
| 209 | 10 | 2025-01-14 | 4 |

(Tied dates correctly receive the same rank — 111 and 209 both rank 4.)

**Running total** — cumulative revenue over time:

```sql
SELECT
    o.order_id,
    o.order_date,
    SUM(oi.quantity * p.unit_price) OVER (ORDER BY o.order_date) AS running_revenue
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
JOIN products p ON oi.product_id = p.product_id
ORDER BY o.order_date
LIMIT 15;
```

| order_id | order_date | running_revenue |
|---|---|---|
| 35 | 2025-01-02 | 42894.0 |
| 1 | 2025-01-03 | 84782.0 |
| 207 | 2025-01-12 | 132773.0 |
| 111 | 2025-01-14 | 154568.0 |
| 209 | 2025-01-14 | 154568.0 |

Note: revenue here is `quantity × unit_price` without the discount applied, since the goal of this specific exercise was learning the window function mechanic, not final revenue accuracy. The discount-adjusted version was already demonstrated in the JOIN section above.

---

## Concept Coverage Checklist

| Concept | Practiced |
|---|---|
| SELECT | Yes |
| WHERE | Yes |
| ORDER BY | Yes |
| GROUP BY | Yes |
| HAVING | Yes |
| JOINs (INNER, LEFT) | Yes |
| Aggregate Functions | Yes |
| Subqueries | Yes |
| Basic Window Functions | Yes |

All 9 required concepts covered.

## Status

This document covers concept-level practice only. The Week 1 task deliverable — "Write SQL queries to analyse customer orders, revenue, and product performance" — requires a separate set of 10 business-question queries against this same database, tracked in `sql_practice_queries.sql`. That file is still in progress and is the actual graded task output.
