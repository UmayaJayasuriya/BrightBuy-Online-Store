-- ============================================
-- Fix PreventProductDeletion Trigger
-- This script fixes the trigger that references
-- the non-existent 'OrderDetails' table
-- ============================================

USE `brightbuy`;

DELIMITER $$

-- Drop the existing broken trigger
DROP TRIGGER IF EXISTS `PreventProductDeletion`$$

-- Create the corrected trigger
CREATE DEFINER=`root`@`localhost` TRIGGER `PreventProductDeletion` 
BEFORE DELETE ON `product` 
FOR EACH ROW 
BEGIN
    -- Check if product variants exist in order_item table
    IF EXISTS (
        SELECT 1 FROM order_item oi
        JOIN variant v ON oi.variant_id = v.variant_id
        WHERE v.product_id = OLD.product_id
    ) THEN
        SIGNAL SQLSTATE '45000' 
        SET MESSAGE_TEXT = 'Cannot delete product with existing orders';
    END IF;
END$$

DELIMITER ;

-- Verify the trigger was created
SHOW TRIGGERS WHERE `Trigger` = 'PreventProductDeletion';
