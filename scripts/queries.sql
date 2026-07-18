-- =========================================================
-- Task 2: SQL for Data Extraction
-- Database: apexplanet_analytics | Table: superstore
-- =========================================================

USE apexplanet_analytics;

-- ============================
-- PART 1: SQL FUNDAMENTALS
-- ============================

-- 1. Basic SELECT with WHERE
SELECT order_id, customer_name, sales
FROM superstore
WHERE sales > 500;

-- 2. ORDER BY + LIMIT
SELECT order_id, customer_name, sales
FROM superstore
ORDER BY sales DESC
LIMIT 10;

-- 3. GROUP BY + aggregate
SELECT category, ROUND(SUM(sales),2) AS total_sales
FROM superstore
GROUP BY category;

-- 4. GROUP BY + HAVING
SELECT sub_category, ROUND(SUM(sales),2) AS total_sales
FROM superstore
GROUP BY sub_category
HAVING SUM(sales) > 10000;

-- 5. JOIN example (only relevant if you split into multiple tables;
--    included here as a template in case you normalize customers into
--    a separate table later)
-- SELECT s.order_id, c.customer_name, s.sales
-- FROM superstore s
-- JOIN customers c ON s.customer_id = c.customer_id;


-- ============================
-- PART 2: ADVANCED SQL
-- ============================

-- 6. Subquery: orders above the overall average sales
SELECT order_id, sales
FROM superstore
WHERE sales > (SELECT AVG(sales) FROM superstore);

-- 7. CTE (WITH clause): regional sales summary
WITH region_totals AS (
    SELECT region, ROUND(SUM(sales),2) AS total_sales
    FROM superstore
    GROUP BY region
)
SELECT * FROM region_totals
ORDER BY total_sales DESC;

-- 8. Window function: rank products by sales within each category
SELECT
    category,
    product_name,
    sales,
    RANK() OVER (PARTITION BY category ORDER BY sales DESC) AS sales_rank
FROM superstore;

-- 9. Window function: running total of sales by date
SELECT
    order_date,
    sales,
    SUM(sales) OVER (ORDER BY order_date) AS running_total
FROM superstore
ORDER BY order_date;

-- 10. Create a reusable VIEW for category-level performance
CREATE OR REPLACE VIEW category_performance AS
SELECT
    category,
    COUNT(order_id) AS total_orders,
    SUM(sales) AS total_sales,
    AVG(sales) AS avg_sales
FROM superstore
GROUP BY category;

-- Use the view like a table:
-- category_performancecategorycategoryavg_salesSELECT * FROM category_performance;


-- ============================
-- PART 3: 10 BUSINESS QUESTIONS
-- ============================

-- Q1. Top 5 products by total sales
SELECT product_name, ROUND(SUM(sales),2) AS total_sales
FROM superstore
GROUP BY product_name
ORDER BY total_sales DESC
LIMIT 5;

-- Q2. Monthly sales trend
SELECT
    DATE_FORMAT(order_date, '%Y-%m') AS month,
    ROUND(SUM(sales),2) AS total_sales
FROM superstore
GROUP BY month
ORDER BY month;

-- Q3. Customer segmentation by total spend
SELECT
    customer_name,
    ROUND(SUM(sales),2) AS total_spend,
    CASE
        WHEN SUM(sales) >= 5000 THEN 'High Value'
        WHEN SUM(sales) >= 1000 THEN 'Medium Value'
        ELSE 'Low Value'
    END AS customer_segment
FROM superstore
GROUP BY customer_name
ORDER BY total_spend DESC;

-- Q4. Sales performance by region
SELECT region, ROUND(SUM(sales),2) AS total_sales, COUNT(order_id) AS total_orders
FROM superstore
GROUP BY region
ORDER BY total_sales DESC;

-- Q5. Best-selling sub-category by quantity
-- (remove this query if your table doesn't have a 'quantity' column)
SELECT sub_category, SUM(quantity) AS total_units
FROM superstore
GROUP BY sub_category
ORDER BY total_units DESC
LIMIT 5;

-- Q6. Average discount by category
-- (remove this query if your table doesn't have a 'discount' column)
SELECT category, AVG(discount) AS avg_discount
FROM superstore
GROUP BY category
ORDER BY avg_discount DESC;

-- Q7. Top 5 customers by number of orders
SELECT customer_name, COUNT(order_id) AS order_count
FROM superstore
GROUP BY customer_name
ORDER BY order_count DESC
LIMIT 5;

-- Q8. Sales by shipping mode
SELECT ship_mode, SUM(sales) AS total_sales, COUNT(order_id) AS total_orders
FROM superstore
GROUP BY ship_mode
ORDER BY total_sales DESC;

-- Q9. States with highest average order value
SELECT state, ROUND(AVG(sales),2) AS avg_order_value
FROM superstore
GROUP BY state
ORDER BY avg_order_value DESC
LIMIT 10;

-- Q10. Profit margin by category
-- (remove this query if your table doesn't have a 'profit' column)
SELECT
    category,
    ROUND(SUM(sales),2) AS total_sales,
  ROUND(SUM(profit),2)AS total_profit,
    ROUND(SUM(profit) / SUM(sales) * 100, 2) AS profit_margin_pct
FROM superstore
GROUP BY category
ORDER BY profit_margin_pct DESC;
