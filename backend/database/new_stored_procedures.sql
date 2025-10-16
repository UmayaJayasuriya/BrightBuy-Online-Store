-- ============================================
-- BrightBuy Additional Stored Procedures
-- Created: 2025-10-16
-- Description: Enhanced procedures for cart, products, inventory, sales, and order management
-- ============================================

USE `brightbuy`;

DELIMITER $$

-- ============================================
-- Procedure 1: GetUserCart
-- Description: Fetch complete cart details for a user
-- Parameters: p_user_id (INT) - User ID
-- Returns: Cart items with product details and totals
-- ============================================
DROP PROCEDURE IF EXISTS `GetUserCart`$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `GetUserCart`(
    IN p_user_id INT
)
BEGIN
    SELECT 
        c.cart_id,
        c.user_id,
        c.total_amount as cart_total,
        ci.cart_item_id,
        ci.variant_id,
        ci.quantity,
        v.variant_name,
        v.price,
        v.SKU,
        v.quantity as stock_available,
        p.product_id,
        p.product_name,
        p.description,
        cat.category_name,
        (ci.quantity * v.price) as item_total,
        CASE 
            WHEN v.quantity >= ci.quantity THEN 'In Stock'
            WHEN v.quantity > 0 THEN 'Limited Stock'
            ELSE 'Out of Stock'
        END as stock_status
    FROM cart c
    LEFT JOIN cart_item ci ON c.cart_id = ci.cart_id
    LEFT JOIN variant v ON ci.variant_id = v.variant_id
    LEFT JOIN product p ON v.product_id = p.product_id
    LEFT JOIN category cat ON p.category_id = cat.category_id
    WHERE c.user_id = p_user_id
    ORDER BY ci.cart_item_id DESC;
END$$

-- ============================================
-- Procedure 2: GetProductsByCategory
-- Description: Get all products in a category with variant info
-- Parameters: p_category_id (INT) - Category ID (NULL for all products)
-- Returns: Products with price range and variant count
-- ============================================
DROP PROCEDURE IF EXISTS `GetProductsByCategory`$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `GetProductsByCategory`(
    IN p_category_id INT
)
BEGIN
    IF p_category_id IS NULL THEN
        -- Get all products
        SELECT 
            p.product_id,
            p.product_name,
            p.description,
            p.category_id,
            c.category_name,
            COUNT(DISTINCT v.variant_id) as variant_count,
            MIN(v.price) as min_price,
            MAX(v.price) as max_price,
            SUM(v.quantity) as total_stock,
            CASE 
                WHEN SUM(v.quantity) > 0 THEN 'Available'
                ELSE 'Out of Stock'
            END as availability_status
        FROM product p
        LEFT JOIN category c ON p.category_id = c.category_id
        LEFT JOIN variant v ON p.product_id = v.product_id
        GROUP BY p.product_id, p.product_name, p.description, p.category_id, c.category_name
        ORDER BY p.product_name;
    ELSE
        -- Get products by category
        SELECT 
            p.product_id,
            p.product_name,
            p.description,
            p.category_id,
            c.category_name,
            COUNT(DISTINCT v.variant_id) as variant_count,
            MIN(v.price) as min_price,
            MAX(v.price) as max_price,
            SUM(v.quantity) as total_stock,
            CASE 
                WHEN SUM(v.quantity) > 0 THEN 'Available'
                ELSE 'Out of Stock'
            END as availability_status
        FROM product p
        LEFT JOIN category c ON p.category_id = c.category_id
        LEFT JOIN variant v ON p.product_id = v.product_id
        WHERE p.category_id = p_category_id
        GROUP BY p.product_id, p.product_name, p.description, p.category_id, c.category_name
        ORDER BY p.product_name;
    END IF;
END$$

-- ============================================
-- Procedure 3: GetLowStockVariants
-- Description: Get variants with stock below threshold
-- Parameters: p_threshold (INT) - Stock level threshold (default 10)
-- Returns: Low stock variants with product details
-- ============================================
DROP PROCEDURE IF EXISTS `GetLowStockVariants`$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `GetLowStockVariants`(
    IN p_threshold INT
)
BEGIN
    -- Set default threshold if NULL
    IF p_threshold IS NULL THEN
        SET p_threshold = 10;
    END IF;
    
    SELECT 
        v.variant_id,
        v.variant_name,
        v.quantity as current_stock,
        v.price,
        v.SKU,
        p.product_id,
        p.product_name,
        c.category_id,
        c.category_name,
        p_threshold as threshold,
        CASE 
            WHEN v.quantity = 0 THEN 'OUT OF STOCK'
            WHEN v.quantity < (p_threshold / 2) THEN 'CRITICAL'
            ELSE 'LOW'
        END as stock_alert_level,
        -- Calculate recent sales (last 30 days)
        COALESCE(
            (SELECT SUM(oi.quantity) 
             FROM order_item oi 
             JOIN orders o ON oi.order_id = o.order_id
             WHERE oi.variant_id = v.variant_id 
             AND o.order_date >= DATE_SUB(NOW(), INTERVAL 30 DAY)
            ), 0
        ) as sold_last_30_days
    FROM variant v
    JOIN product p ON v.product_id = p.product_id
    JOIN category c ON p.category_id = c.category_id
    WHERE v.quantity < p_threshold
    ORDER BY v.quantity ASC, sold_last_30_days DESC;
END$$

-- ============================================
-- Procedure 4: GetSalesReport
-- Description: Generate sales report for a date range
-- Parameters: 
--   p_start_date (DATE) - Start date
--   p_end_date (DATE) - End date
-- Returns: Daily sales summary with revenue and order metrics
-- ============================================
DROP PROCEDURE IF EXISTS `GetSalesReport`$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `GetSalesReport`(
    IN p_start_date DATE,
    IN p_end_date DATE
)
BEGIN
    -- Set default dates if NULL (last 30 days)
    IF p_start_date IS NULL THEN
        SET p_start_date = DATE_SUB(CURDATE(), INTERVAL 30 DAY);
    END IF;
    
    IF p_end_date IS NULL THEN
        SET p_end_date = CURDATE();
    END IF;
    
    SELECT 
        DATE(o.order_date) as sale_date,
        COUNT(DISTINCT o.order_id) as total_orders,
        COUNT(DISTINCT o.user_id) as unique_customers,
        SUM(o.total_amount) as total_revenue,
        AVG(o.total_amount) as average_order_value,
        SUM(oi.quantity) as total_items_sold,
        -- Most popular product of the day
        (SELECT p.product_name 
         FROM order_item oi2
         JOIN variant v ON oi2.variant_id = v.variant_id
         JOIN product p ON v.product_id = p.product_id
         JOIN orders o2 ON oi2.order_id = o2.order_id
         WHERE DATE(o2.order_date) = DATE(o.order_date)
         GROUP BY p.product_id, p.product_name
         ORDER BY SUM(oi2.quantity) DESC
         LIMIT 1
        ) as top_product,
        -- Revenue by payment method
        SUM(CASE WHEN pm.payment_method = 'card' THEN o.total_amount ELSE 0 END) as card_revenue,
        SUM(CASE WHEN pm.payment_method = 'cash' THEN o.total_amount ELSE 0 END) as cash_revenue
    FROM orders o
    JOIN order_item oi ON o.order_id = oi.order_id
    LEFT JOIN payment pm ON o.order_id = pm.order_id
    WHERE DATE(o.order_date) BETWEEN p_start_date AND p_end_date
    GROUP BY DATE(o.order_date)
    ORDER BY sale_date DESC;
END$$

-- ============================================
-- Procedure 5: UpdateOrderStatus
-- Description: Update delivery status for an order
-- Parameters: 
--   p_order_id (INT) - Order ID
--   p_new_status (VARCHAR) - New delivery status
-- Returns: Success/failure message
-- ============================================
DROP PROCEDURE IF EXISTS `UpdateOrderStatus`$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `UpdateOrderStatus`(
    IN p_order_id INT,
    IN p_new_status VARCHAR(50)
)
BEGIN
    DECLARE order_exists INT;
    DECLARE delivery_exists INT;
    
    -- Check if order exists
    SELECT COUNT(*) INTO order_exists 
    FROM orders 
    WHERE order_id = p_order_id;
    
    IF order_exists = 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Order not found';
    END IF;
    
    -- Check if delivery record exists
    SELECT COUNT(*) INTO delivery_exists 
    FROM delivery 
    WHERE order_id = p_order_id;
    
    IF delivery_exists > 0 THEN
        -- Update existing delivery record
        UPDATE delivery
        SET delivery_status = p_new_status,
            delivery_date = CASE 
                WHEN p_new_status = 'Delivered' THEN NOW()
                ELSE delivery_date
            END
        WHERE order_id = p_order_id;
        
        SELECT 
            'Status updated successfully' as message,
            p_order_id as order_id,
            p_new_status as new_status,
            NOW() as updated_at;
    ELSE
        -- Create new delivery record if it doesn't exist
        INSERT INTO delivery (order_id, delivery_status, delivery_date)
        VALUES (
            p_order_id, 
            p_new_status,
            CASE WHEN p_new_status = 'Delivered' THEN NOW() ELSE NULL END
        );
        
        SELECT 
            'Delivery record created and status set' as message,
            p_order_id as order_id,
            p_new_status as new_status,
            NOW() as created_at;
    END IF;
END$$

-- ============================================
-- BONUS Procedure: GetTopSellingProducts
-- Description: Get best-selling products by quantity or revenue
-- Parameters: 
--   p_limit (INT) - Number of products to return (default 10)
--   p_days (INT) - Number of days to look back (default 30)
-- Returns: Top selling products with sales metrics
-- ============================================
DROP PROCEDURE IF EXISTS `GetTopSellingProducts`$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `GetTopSellingProducts`(
    IN p_limit INT,
    IN p_days INT
)
BEGIN
    -- Set defaults
    IF p_limit IS NULL THEN
        SET p_limit = 10;
    END IF;
    
    IF p_days IS NULL THEN
        SET p_days = 30;
    END IF;
    
    SELECT 
        p.product_id,
        p.product_name,
        c.category_name,
        COUNT(DISTINCT o.order_id) as times_ordered,
        SUM(oi.quantity) as total_quantity_sold,
        SUM(oi.quantity * oi.price) as total_revenue,
        AVG(oi.price) as average_price,
        MIN(v.quantity) as lowest_variant_stock
    FROM order_item oi
    JOIN orders o ON oi.order_id = o.order_id
    JOIN variant v ON oi.variant_id = v.variant_id
    JOIN product p ON v.product_id = p.product_id
    JOIN category c ON p.category_id = c.category_id
    WHERE o.order_date >= DATE_SUB(NOW(), INTERVAL p_days DAY)
    GROUP BY p.product_id, p.product_name, c.category_name
    ORDER BY total_quantity_sold DESC
    LIMIT p_limit;
END$$

-- ============================================
-- BONUS Procedure: GetCustomerOrderHistory
-- Description: Get complete order history for a customer with details
-- Parameters: p_user_id (INT) - User ID
-- Returns: All orders with items, delivery status, and payment info
-- ============================================
DROP PROCEDURE IF EXISTS `GetCustomerOrderHistory`$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `GetCustomerOrderHistory`(
    IN p_user_id INT
)
BEGIN
    SELECT 
        o.order_id,
        o.order_date,
        o.total_amount,
        d.delivery_status,
        d.delivery_date,
        pm.payment_method,
        COUNT(DISTINCT oi.order_item_id) as total_items,
        SUM(oi.quantity) as total_quantity,
        GROUP_CONCAT(
            CONCAT(p.product_name, ' (', v.variant_name, ') x', oi.quantity)
            SEPARATOR ', '
        ) as order_items,
        DATEDIFF(COALESCE(d.delivery_date, NOW()), o.order_date) as days_since_order
    FROM orders o
    LEFT JOIN order_item oi ON o.order_id = oi.order_id
    LEFT JOIN variant v ON oi.variant_id = v.variant_id
    LEFT JOIN product p ON v.product_id = p.product_id
    LEFT JOIN delivery d ON o.order_id = d.order_id
    LEFT JOIN payment pm ON o.order_id = pm.order_id
    WHERE o.user_id = p_user_id
    GROUP BY o.order_id, o.order_date, o.total_amount, d.delivery_status, 
             d.delivery_date, pm.payment_method
    ORDER BY o.order_date DESC;
END$$

DELIMITER ;

-- ============================================
-- Installation Complete
-- ============================================
-- The following stored procedures have been created:
-- 1. GetUserCart - Fetch user's cart with full details
-- 2. GetProductsByCategory - Get products by category with pricing
-- 3. GetLowStockVariants - Inventory management alerts
-- 4. GetSalesReport - Sales analytics by date range
-- 5. UpdateOrderStatus - Update order delivery status
-- 6. GetTopSellingProducts - Best sellers analysis (BONUS)
-- 7. GetCustomerOrderHistory - Complete customer order history (BONUS)
-- ============================================
