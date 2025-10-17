-- ============================================
-- Brightbuy Stored Procedures Export
-- Generated: 2025-10-16 16:54:00
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

DELIMITER ;
