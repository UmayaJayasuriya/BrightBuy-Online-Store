-- ============================================
-- BrightBuy Report Views
-- Database views for generating PDF reports
-- ============================================

USE `brightbuy`;

-- ============================================
-- View 1: Quarterly Sales Report
-- Sales data grouped by quarter and year
-- ============================================
DROP VIEW IF EXISTS quarterly_sales_report;

CREATE VIEW quarterly_sales_report AS
SELECT 
    y AS year,
    q AS quarter,
    CONCAT('Q', q, ' ', y) AS quarter_label,
    total_orders,
    unique_customers,
    total_revenue,
    average_order_value,
    total_items_sold
FROM (
    SELECT 
        YEAR(o.order_date) AS y,
        QUARTER(o.order_date) AS q,
        COUNT(DISTINCT o.order_id) AS total_orders,
        COUNT(DISTINCT o.user_id) AS unique_customers,
        SUM(o.total_amount) AS total_revenue,
        AVG(o.total_amount) AS average_order_value,
        COALESCE(SUM(oi.quantity), 0) AS total_items_sold
    FROM orders o
    LEFT JOIN order_item oi ON o.order_id = oi.order_id
    GROUP BY YEAR(o.order_date), QUARTER(o.order_date)
) AS subquery
ORDER BY year DESC, quarter DESC;


-- ============================================
-- View 2: Top Selling Products
-- Products ranked by quantity sold
-- ============================================
DROP VIEW IF EXISTS top_selling_products;

CREATE VIEW top_selling_products AS
SELECT 
    p.product_id,
    p.product_name,
    c.category_name,
    v.variant_id,
    v.variant_name,
    v.SKU,
    SUM(oi.quantity) AS total_quantity_sold,
    SUM(oi.quantity * oi.price) AS total_revenue,
    AVG(oi.price) AS average_price,
    COUNT(DISTINCT oi.order_id) AS number_of_orders,
    MIN(o.order_date) AS first_sale_date,
    MAX(o.order_date) AS last_sale_date
FROM order_item oi
JOIN variant v ON oi.variant_id = v.variant_id
JOIN product p ON v.product_id = p.product_id
LEFT JOIN category c ON p.category_id = c.category_id
JOIN orders o ON oi.order_id = o.order_id
GROUP BY p.product_id, p.product_name, c.category_name, v.variant_id, v.variant_name, v.SKU
ORDER BY total_quantity_sold DESC;


-- ============================================
-- View 3: Category-wise Order Summary
-- Total orders and revenue by category
-- ============================================
DROP VIEW IF EXISTS category_order_summary;

CREATE VIEW category_order_summary AS
SELECT 
    COALESCE(c.category_name, 'Uncategorized') AS category_name,
    c.category_id,
    COUNT(DISTINCT o.order_id) AS total_orders,
    SUM(oi.quantity) AS total_items_sold,
    SUM(oi.quantity * oi.price) AS total_revenue,
    AVG(oi.quantity * oi.price) AS average_order_value,
    COUNT(DISTINCT p.product_id) AS unique_products,
    MIN(o.order_date) AS first_order_date,
    MAX(o.order_date) AS last_order_date
FROM order_item oi
JOIN orders o ON oi.order_id = o.order_id
JOIN variant v ON oi.variant_id = v.variant_id
JOIN product p ON v.product_id = p.product_id
LEFT JOIN category c ON p.category_id = c.category_id
GROUP BY c.category_id, category_name
ORDER BY total_revenue DESC;


-- ============================================
-- View 4: Customer Order and Payment Summary
-- Detailed customer order history with payment status
-- ============================================
DROP VIEW IF EXISTS customer_order_payment_summary;

CREATE VIEW customer_order_payment_summary AS
SELECT 
    u.user_id,
    u.user_name,
    u.email,
    u.name AS full_name,
    o.order_id,
    o.order_date,
    o.total_amount,
    p.payment_method,
    p.payment_status,
    p.payment_date,
    d.delivery_status,
    d.delivery_method,
    d.estimated_delivery_date,
    COUNT(oi.order_item_id) AS items_in_order,
    SUM(oi.quantity) AS total_quantity
FROM user u
LEFT JOIN orders o ON u.user_id = o.user_id
LEFT JOIN payment p ON o.order_id = p.order_id
LEFT JOIN delivery d ON o.order_id = d.order_id
LEFT JOIN order_item oi ON o.order_id = oi.order_id
GROUP BY 
    u.user_id, u.user_name, u.email, u.name,
    o.order_id, o.order_date, o.total_amount,
    p.payment_method, p.payment_status, p.payment_date,
    d.delivery_status, d.delivery_method, d.estimated_delivery_date
ORDER BY u.user_id, o.order_date DESC;


-- ============================================
-- View 5: Customer Summary Statistics
-- Aggregate statistics per customer
-- ============================================
DROP VIEW IF EXISTS customer_summary_statistics;

CREATE VIEW customer_summary_statistics AS
SELECT 
    u.user_id,
    u.user_name,
    u.email,
    u.name AS full_name,
    COUNT(DISTINCT o.order_id) AS total_orders,
    COALESCE(SUM(o.total_amount), 0) AS total_spent,
    AVG(o.total_amount) AS average_order_value,
    MIN(o.order_date) AS first_order_date,
    MAX(o.order_date) AS last_order_date,
    SUM(CASE WHEN p.payment_status = 'completed' THEN 1 ELSE 0 END) AS completed_payments,
    SUM(CASE WHEN p.payment_status = 'pending' THEN 1 ELSE 0 END) AS pending_payments,
    SUM(CASE WHEN d.delivery_status = 'delivered' THEN 1 ELSE 0 END) AS delivered_orders,
    SUM(CASE WHEN d.delivery_status = 'pending' THEN 1 ELSE 0 END) AS pending_deliveries
FROM user u
LEFT JOIN orders o ON u.user_id = o.user_id
LEFT JOIN payment p ON o.order_id = p.order_id
LEFT JOIN delivery d ON o.order_id = d.order_id
GROUP BY u.user_id, u.user_name, u.email, full_name
HAVING total_orders > 0
ORDER BY total_spent DESC;


-- ============================================
-- Verification Queries
-- Run these to test the views
-- ============================================

-- Test quarterly sales
-- SELECT * FROM quarterly_sales_report WHERE year = 2025;

-- Test top selling products
-- SELECT * FROM top_selling_products LIMIT 10;

-- Test category summary
-- SELECT * FROM category_order_summary;

-- Test customer order payment summary
-- SELECT * FROM customer_order_payment_summary WHERE user_id = 10 LIMIT 5;

-- Test customer statistics
-- SELECT * FROM customer_summary_statistics LIMIT 10;
