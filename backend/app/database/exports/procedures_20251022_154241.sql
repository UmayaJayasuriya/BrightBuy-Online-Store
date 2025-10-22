-- ============================================
-- BrightBuy Stored Procedures Export
-- Generated: 2025-10-22 15:42:41
-- ============================================

USE `brightbuy`;

DELIMITER $$

-- Procedure: AddUserWithAddress
DROP PROCEDURE IF EXISTS `AddUserWithAddress`$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `AddUserWithAddress`(
    IN p_user_id INT,
    IN p_user_name VARCHAR(50),
    IN p_email VARCHAR(100),
    IN p_name VARCHAR(50),
    IN p_password_hash VARCHAR(100),
    IN p_user_type VARCHAR(30),
    
    -- Address fields
    IN p_city_id INT,
    IN p_house_number INT,
    IN p_street VARCHAR(100),
    IN p_city VARCHAR(100),
    IN p_state VARCHAR(100)
)
BEGIN
    DECLARE new_address_id INT;

    -- Step 1: Insert address
    INSERT INTO Address (
        address_id, city_id, house_number, street, city, state
    )
    VALUES (
        NULL, p_city_id, p_house_number, p_street, p_city, p_state
    );

    -- Step 2: Get the newly inserted address_id
    SET new_address_id = LAST_INSERT_ID();

    -- Step 3: Insert user with the new address_id
    INSERT INTO User (
        user_id, user_name, email, name, password_hash, user_type, address_id
    )
    VALUES (
        p_user_id, p_user_name, p_email, p_name, p_password_hash, p_user_type, new_address_id
    );
END$$

-- Procedure: GetOrderSummary
DROP PROCEDURE IF EXISTS `GetOrderSummary`$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `GetOrderSummary`(
    IN p_user_id INT
)
BEGIN
    SELECT 
        o.order_id,
        o.order_date,
        o.total_amount,
        oi.quantity,
        oi.price,
        p.product_name,
        v.variant_name,
        d.delivery_status
    FROM orders o
    JOIN order_item oi ON o.order_id = oi.order_id
    LEFT JOIN variant v ON oi.variant_id = v.variant_id  
    LEFT JOIN product p ON v.product_id = p.product_id
    LEFT JOIN delivery d ON o.order_id = d.order_id
    WHERE o.user_id = p_user_id
    ORDER BY o.order_date DESC;
END$$

-- Procedure: GetUserCart
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

-- Procedure: GetProductsByCategory
DROP PROCEDURE IF EXISTS `GetProductsByCategory`$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `GetProductsByCategory`(
    IN p_category_id INT
)
BEGIN
    SELECT 
        p.product_id,
        p.product_name,
        p.description,
        p.category_id,
        c.category_name,
        COUNT(v.variant_id) as variant_count,
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
    WHERE p_category_id IS NULL OR p.category_id = p_category_id
    GROUP BY p.product_id, p.product_name, p.description, p.category_id, c.category_name
    ORDER BY p.product_name;
END$$

-- Procedure: GetLowStockVariants
DROP PROCEDURE IF EXISTS `GetLowStockVariants`$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `GetLowStockVariants`(
    IN p_threshold INT
)
BEGIN
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
            WHEN v.quantity <= (p_threshold * 0.3) THEN 'CRITICAL'
            ELSE 'LOW'
        END as stock_alert_level,
        COALESCE(
            (SELECT SUM(oi.quantity) 
             FROM order_item oi 
             JOIN orders o ON oi.order_id = o.order_id 
             WHERE oi.variant_id = v.variant_id 
             AND o.order_date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)),
            0
        ) as sold_last_30_days
    FROM variant v
    JOIN product p ON v.product_id = p.product_id
    LEFT JOIN category c ON p.category_id = c.category_id
    WHERE v.quantity <= p_threshold
    ORDER BY v.quantity ASC, sold_last_30_days DESC;
END$$

-- Procedure: GetSalesReport
DROP PROCEDURE IF EXISTS `GetSalesReport`$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `GetSalesReport`(
    IN p_start_date DATE,
    IN p_end_date DATE
)
BEGIN
    SELECT 
        DATE(o.order_date) as sale_date,
        COUNT(DISTINCT o.order_id) as total_orders,
        COUNT(DISTINCT o.user_id) as unique_customers,
        SUM(o.total_amount) as total_revenue,
        AVG(o.total_amount) as average_order_value,
        SUM(oi.quantity) as total_items_sold,
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
        SUM(CASE WHEN pay.payment_method = 'card' THEN o.total_amount ELSE 0 END) as card_revenue,
        SUM(CASE WHEN pay.payment_method = 'cash' THEN o.total_amount ELSE 0 END) as cash_revenue
    FROM orders o
    LEFT JOIN order_item oi ON o.order_id = oi.order_id
    LEFT JOIN payment pay ON o.order_id = pay.order_id
    WHERE DATE(o.order_date) BETWEEN p_start_date AND p_end_date
    GROUP BY DATE(o.order_date)
    ORDER BY sale_date DESC;
END$$

-- Procedure: UpdateOrderStatus
DROP PROCEDURE IF EXISTS `UpdateOrderStatus`$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `UpdateOrderStatus`(
    IN p_order_id INT,
    IN p_status VARCHAR(50)
)
BEGIN
    DECLARE v_delivery_id INT;
    
    -- Check if order exists
    SELECT delivery_id INTO v_delivery_id
    FROM delivery
    WHERE order_id = p_order_id;
    
    IF v_delivery_id IS NULL THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Order not found';
    END IF;
    
    -- Update delivery status
    UPDATE delivery
    SET delivery_status = p_status,
        delivery_date = CASE WHEN p_status = 'Delivered' THEN CURDATE() ELSE delivery_date END
    WHERE order_id = p_order_id;
    
    -- Return success message
    SELECT 
        'Status updated successfully' as message,
        NOW() as updated_at,
        p_order_id as order_id,
        p_status as new_status;
END$$

-- Procedure: GetTopSellingProducts
DROP PROCEDURE IF EXISTS `GetTopSellingProducts`$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `GetTopSellingProducts`(
    IN p_limit INT,
    IN p_days INT
)
BEGIN
    SELECT 
        p.product_id,
        p.product_name,
        c.category_name,
        COUNT(DISTINCT oi.order_id) as times_ordered,
        SUM(oi.quantity) as total_quantity_sold,
        SUM(oi.quantity * oi.price) as total_revenue,
        AVG(oi.price) as average_price,
        MIN(v.quantity) as lowest_variant_stock
    FROM order_item oi
    JOIN variant v ON oi.variant_id = v.variant_id
    JOIN product p ON v.product_id = p.product_id
    LEFT JOIN category c ON p.category_id = c.category_id
    JOIN orders o ON oi.order_id = o.order_id
    WHERE o.order_date >= DATE_SUB(CURDATE(), INTERVAL p_days DAY)
    GROUP BY p.product_id, p.product_name, c.category_name
    ORDER BY total_quantity_sold DESC
    LIMIT p_limit;
END$$

-- Procedure: GetCustomerOrderHistory
DROP PROCEDURE IF EXISTS `GetCustomerOrderHistory`$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `GetCustomerOrderHistory`(
    IN p_user_id INT
)
BEGIN
    SELECT 
        o.order_id,
        DATE(o.order_date) as order_date,
        o.total_amount,
        d.delivery_status,
        d.delivery_date,
        p.payment_method,
        COUNT(oi.order_item_id) as total_items,
        SUM(oi.quantity) as total_quantity,
        GROUP_CONCAT(
            CONCAT(prod.product_name, ' (', v.variant_name, ') x', oi.quantity)
            SEPARATOR ', '
        ) as order_items,
        DATEDIFF(CURDATE(), o.order_date) as days_since_order
    FROM orders o
    LEFT JOIN delivery d ON o.order_id = d.order_id
    LEFT JOIN payment p ON o.order_id = p.order_id
    LEFT JOIN order_item oi ON o.order_id = oi.order_id
    LEFT JOIN variant v ON oi.variant_id = v.variant_id
    LEFT JOIN product prod ON v.product_id = prod.product_id
    WHERE o.user_id = p_user_id
    GROUP BY o.order_id, o.order_date, o.total_amount, d.delivery_status, 
             d.delivery_date, p.payment_method
    ORDER BY o.order_date DESC;
END$$

DELIMITER ;
