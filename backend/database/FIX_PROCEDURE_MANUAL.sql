-- Fix GetOrderSummary Stored Procedure
-- Run this SQL in MySQL Workbench or your MySQL client

-- Step 1: Drop the existing procedure
DROP PROCEDURE IF EXISTS GetOrderSummary;

-- Step 2: Create the corrected procedure
DELIMITER $$

CREATE PROCEDURE GetOrderSummary(
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
    LEFT JOIN variant v ON oi.variant_id = v.variant_id  -- ✅ FIXED: Was oi.order_id = o.order_id
    LEFT JOIN product p ON v.product_id = p.product_id
    LEFT JOIN delivery d ON o.order_id = d.order_id
    WHERE o.user_id = p_user_id
    ORDER BY o.order_date DESC;
END$$

DELIMITER ;

-- Test the procedure
CALL GetOrderSummary(10);
