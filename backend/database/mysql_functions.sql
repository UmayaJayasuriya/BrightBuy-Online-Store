-- ============================================
-- BrightBuy MySQL Functions
-- Created: 2025-10-18
-- Description: Reusable functions for calculations, validations, and data transformations
-- ============================================

USE `brightbuy`;

DELIMITER $$

-- ============================================
-- Function 1: CalculateCartTotal
-- Description: Calculate total amount for a cart
-- Parameters: p_cart_id (INT) - Cart ID
-- Returns: DECIMAL(10,2) - Total cart amount
-- ============================================
DROP FUNCTION IF EXISTS `CalculateCartTotal`$$

CREATE FUNCTION `CalculateCartTotal`(
    p_cart_id INT
)
RETURNS DECIMAL(10,2)
DETERMINISTIC
READS SQL DATA
BEGIN
    DECLARE total DECIMAL(10,2);
    
    SELECT COALESCE(SUM(ci.quantity * v.price), 0.00)
    INTO total
    FROM cart_item ci
    JOIN variant v ON ci.variant_id = v.variant_id
    WHERE ci.cart_id = p_cart_id;
    
    RETURN total;
END$$

-- ============================================
-- Function 2: GetProductStockStatus
-- Description: Get stock status for a product (all variants combined)
-- Parameters: p_product_id (INT) - Product ID
-- Returns: VARCHAR(20) - 'In Stock', 'Low Stock', or 'Out of Stock'
-- ============================================
DROP FUNCTION IF EXISTS `GetProductStockStatus`$$

CREATE FUNCTION `GetProductStockStatus`(
    p_product_id INT
)
RETURNS VARCHAR(20)
DETERMINISTIC
READS SQL DATA
BEGIN
    DECLARE total_stock INT;
    DECLARE status VARCHAR(20);
    
    SELECT COALESCE(SUM(quantity), 0)
    INTO total_stock
    FROM variant
    WHERE product_id = p_product_id;
    
    IF total_stock = 0 THEN
        SET status = 'Out of Stock';
    ELSEIF total_stock < 20 THEN
        SET status = 'Low Stock';
    ELSE
        SET status = 'In Stock';
    END IF;
    
    RETURN status;
END$$

-- ============================================
-- Function 3: CalculateOrderItemTotal
-- Description: Calculate total for a specific order item
-- Parameters: 
--   p_order_item_id (INT) - Order Item ID
-- Returns: DECIMAL(10,2) - Item total (quantity × price)
-- ============================================
DROP FUNCTION IF EXISTS `CalculateOrderItemTotal`$$

CREATE FUNCTION `CalculateOrderItemTotal`(
    p_order_item_id INT
)
RETURNS DECIMAL(10,2)
DETERMINISTIC
READS SQL DATA
BEGIN
    DECLARE item_total DECIMAL(10,2);
    
    SELECT (quantity * price)
    INTO item_total
    FROM order_item
    WHERE order_item_id = p_order_item_id;
    
    RETURN COALESCE(item_total, 0.00);
END$$

-- ============================================
-- Function 4: GetCustomerLifetimeValue
-- Description: Calculate total amount spent by a customer
-- Parameters: p_user_id (INT) - User ID
-- Returns: DECIMAL(10,2) - Total lifetime spending
-- ============================================
DROP FUNCTION IF EXISTS `GetCustomerLifetimeValue`$$

CREATE FUNCTION `GetCustomerLifetimeValue`(
    p_user_id INT
)
RETURNS DECIMAL(10,2)
DETERMINISTIC
READS SQL DATA
BEGIN
    DECLARE lifetime_value DECIMAL(10,2);
    
    SELECT COALESCE(SUM(total_amount), 0.00)
    INTO lifetime_value
    FROM orders
    WHERE user_id = p_user_id;
    
    RETURN lifetime_value;
END$$

-- ============================================
-- Function 5: GetProductAverageRating
-- Description: Calculate average rating for a product (placeholder for future ratings feature)
-- Parameters: p_product_id (INT) - Product ID
-- Returns: DECIMAL(3,2) - Average rating (0.00 if no ratings)
-- Note: Returns 0.00 for now; update when ratings table is added
-- ============================================
DROP FUNCTION IF EXISTS `GetProductAverageRating`$$

CREATE FUNCTION `GetProductAverageRating`(
    p_product_id INT
)
RETURNS DECIMAL(3,2)
DETERMINISTIC
READS SQL DATA
BEGIN
    -- Placeholder: Return 0.00 until ratings table is implemented
    -- Future implementation:
    -- SELECT COALESCE(AVG(rating), 0.00)
    -- FROM product_ratings
    -- WHERE product_id = p_product_id;
    
    RETURN 0.00;
END$$

-- ============================================
-- Function 6: IsVariantAvailable
-- Description: Check if a variant has sufficient stock
-- Parameters: 
--   p_variant_id (INT) - Variant ID
--   p_quantity (INT) - Requested quantity
-- Returns: BOOLEAN (1 = available, 0 = not available)
-- ============================================
DROP FUNCTION IF EXISTS `IsVariantAvailable`$$

CREATE FUNCTION `IsVariantAvailable`(
    p_variant_id INT,
    p_quantity INT
)
RETURNS BOOLEAN
DETERMINISTIC
READS SQL DATA
BEGIN
    DECLARE available_stock INT;
    
    SELECT quantity
    INTO available_stock
    FROM variant
    WHERE variant_id = p_variant_id;
    
    IF available_stock >= p_quantity THEN
        RETURN TRUE;
    ELSE
        RETURN FALSE;
    END IF;
END$$

-- ============================================
-- Function 7: GetProductPriceRange
-- Description: Get price range for a product as formatted string
-- Parameters: p_product_id (INT) - Product ID
-- Returns: VARCHAR(50) - Price range (e.g., "$10.00 - $50.00" or "$25.00")
-- ============================================
DROP FUNCTION IF EXISTS `GetProductPriceRange`$$

CREATE FUNCTION `GetProductPriceRange`(
    p_product_id INT
)
RETURNS VARCHAR(50)
DETERMINISTIC
READS SQL DATA
BEGIN
    DECLARE min_price DECIMAL(10,2);
    DECLARE max_price DECIMAL(10,2);
    DECLARE price_range VARCHAR(50);
    
    SELECT MIN(price), MAX(price)
    INTO min_price, max_price
    FROM variant
    WHERE product_id = p_product_id;
    
    IF min_price IS NULL THEN
        RETURN 'N/A';
    ELSEIF min_price = max_price THEN
        RETURN CONCAT('$', FORMAT(min_price, 2));
    ELSE
        RETURN CONCAT('$', FORMAT(min_price, 2), ' - $', FORMAT(max_price, 2));
    END IF;
END$$

-- ============================================
-- Function 8: CalculateDeliveryDays
-- Description: Calculate estimated delivery days based on city
-- Parameters: p_city_id (INT) - City ID
-- Returns: INT - Estimated delivery days
-- ============================================
DROP FUNCTION IF EXISTS `CalculateDeliveryDays`$$

CREATE FUNCTION `CalculateDeliveryDays`(
    p_city_id INT
)
RETURNS INT
DETERMINISTIC
READS SQL DATA
BEGIN
    DECLARE delivery_days INT;
    
    -- Get delivery time from location table
    SELECT delivery_time
    INTO delivery_days
    FROM location
    WHERE city_id = p_city_id;
    
    -- Default to 7 days if city not found
    RETURN COALESCE(delivery_days, 7);
END$$

-- ============================================
-- Function 9: GetOrderStatus
-- Description: Get comprehensive order status (delivery + payment)
-- Parameters: p_order_id (INT) - Order ID
-- Returns: VARCHAR(100) - Combined status message
-- ============================================
DROP FUNCTION IF EXISTS `GetOrderStatus`$$

CREATE FUNCTION `GetOrderStatus`(
    p_order_id INT
)
RETURNS VARCHAR(100)
DETERMINISTIC
READS SQL DATA
BEGIN
    DECLARE delivery_status VARCHAR(50);
    DECLARE payment_method VARCHAR(50);
    DECLARE status_message VARCHAR(100);
    
    SELECT d.delivery_status, p.payment_method
    INTO delivery_status, payment_method
    FROM orders o
    LEFT JOIN delivery d ON o.order_id = d.order_id
    LEFT JOIN payment p ON o.order_id = p.order_id
    WHERE o.order_id = p_order_id;
    
    IF delivery_status IS NULL THEN
        SET status_message = 'Order Placed';
    ELSE
        SET status_message = CONCAT(delivery_status, ' (', COALESCE(payment_method, 'N/A'), ')');
    END IF;
    
    RETURN status_message;
END$$

-- ============================================
-- Function 10: ValidateEmail
-- Description: Basic email validation
-- Parameters: p_email (VARCHAR) - Email address
-- Returns: BOOLEAN (1 = valid, 0 = invalid)
-- ============================================
DROP FUNCTION IF EXISTS `ValidateEmail`$$

CREATE FUNCTION `ValidateEmail`(
    p_email VARCHAR(255)
)
RETURNS BOOLEAN
DETERMINISTIC
NO SQL
BEGIN
    -- Check if email contains @ and . and has valid format
    IF p_email REGEXP '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$' THEN
        RETURN TRUE;
    ELSE
        RETURN FALSE;
    END IF;
END$$

-- ============================================
-- Function 11: GetDiscountedPrice
-- Description: Calculate discounted price (for future discount feature)
-- Parameters: 
--   p_price (DECIMAL) - Original price
--   p_discount_percent (DECIMAL) - Discount percentage
-- Returns: DECIMAL(10,2) - Discounted price
-- ============================================
DROP FUNCTION IF EXISTS `GetDiscountedPrice`$$

CREATE FUNCTION `GetDiscountedPrice`(
    p_price DECIMAL(10,2),
    p_discount_percent DECIMAL(5,2)
)
RETURNS DECIMAL(10,2)
DETERMINISTIC
NO SQL
BEGIN
    DECLARE discounted_price DECIMAL(10,2);
    
    IF p_discount_percent < 0 OR p_discount_percent > 100 THEN
        RETURN p_price;
    END IF;
    
    SET discounted_price = p_price - (p_price * p_discount_percent / 100);
    
    RETURN ROUND(discounted_price, 2);
END$$

-- ============================================
-- Function 12: GetCategoryPath
-- Description: Get full category path (e.g., "Electronics > Laptops")
-- Parameters: p_category_id (INT) - Category ID
-- Returns: VARCHAR(500) - Category path
-- ============================================
DROP FUNCTION IF EXISTS `GetCategoryPath`$$

CREATE FUNCTION `GetCategoryPath`(
    p_category_id INT
)
RETURNS VARCHAR(500)
DETERMINISTIC
READS SQL DATA
BEGIN
    DECLARE category_path VARCHAR(500);
    DECLARE current_name VARCHAR(100);
    DECLARE parent_id INT;
    
    -- Get current category name
    SELECT category_name, parent_category_id
    INTO current_name, parent_id
    FROM category
    WHERE category_id = p_category_id;
    
    SET category_path = current_name;
    
    -- Build path by traversing parent categories
    WHILE parent_id IS NOT NULL DO
        SELECT category_name, parent_category_id
        INTO current_name, parent_id
        FROM category
        WHERE category_id = parent_id;
        
        SET category_path = CONCAT(current_name, ' > ', category_path);
    END WHILE;
    
    RETURN category_path;
END$$

DELIMITER ;

-- ============================================
-- Installation Complete
-- ============================================
-- The following MySQL functions have been created:
-- 1. CalculateCartTotal - Calculate cart total amount
-- 2. GetProductStockStatus - Get product stock status
-- 3. CalculateOrderItemTotal - Calculate order item total
-- 4. GetCustomerLifetimeValue - Calculate customer lifetime value
-- 5. GetProductAverageRating - Get product rating (placeholder)
-- 6. IsVariantAvailable - Check variant availability
-- 7. GetProductPriceRange - Get formatted price range
-- 8. CalculateDeliveryDays - Calculate delivery estimate
-- 9. GetOrderStatus - Get comprehensive order status
-- 10. ValidateEmail - Email validation
-- 11. GetDiscountedPrice - Calculate discounted price
-- 12. GetCategoryPath - Get full category path
-- ============================================
