-- ============================================
-- BrightBuy Triggers Export
-- Generated: 2025-10-22 15:42:41
-- ============================================

USE `brightbuy`;

DELIMITER $$

-- Trigger: check_cvv_length
DROP TRIGGER IF EXISTS `check_cvv_length`$$

CREATE DEFINER=`himak`@`%` TRIGGER `check_cvv_length` BEFORE INSERT ON `card` FOR EACH ROW BEGIN
    IF LENGTH(NEW.CVV) != 3 OR NEW.CVV REGEXP '[^0-9]' THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'CVV must be exactly 3 digits';
    END IF;
END$$

-- Trigger: set_default_delivery_status
DROP TRIGGER IF EXISTS `set_default_delivery_status`$$

CREATE DEFINER=`himak`@`%` TRIGGER `set_default_delivery_status` BEFORE INSERT ON `delivery` FOR EACH ROW BEGIN
    IF NEW.delivery_status IS NULL THEN
        SET NEW.delivery_status = 'Pending';
    END IF;
END$$

-- Trigger: trg_check_email_before_insert
DROP TRIGGER IF EXISTS `trg_check_email_before_insert`$$

CREATE DEFINER=`himak`@`%` TRIGGER `trg_check_email_before_insert` BEFORE INSERT ON `user` FOR EACH ROW BEGIN
    IF NEW.email NOT LIKE '%@%' THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Please enter a valid email address. It must include the "@" symbol (e.g., name@example.com).';
    END IF;
END$$

-- Trigger: check_variant_quantity
DROP TRIGGER IF EXISTS `check_variant_quantity`$$

CREATE DEFINER=`himak`@`%` TRIGGER `check_variant_quantity` BEFORE UPDATE ON `variant` FOR EACH ROW BEGIN
    IF NEW.quantity < 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Quantity cannot be negative';
    END IF;
END$$

-- Trigger: prevent_negative_stock
DROP TRIGGER IF EXISTS `prevent_negative_stock`$$

CREATE DEFINER=`root`@`localhost` TRIGGER `prevent_negative_stock` BEFORE UPDATE ON `variant` FOR EACH ROW BEGIN
    IF NEW.quantity < 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Stock cannot be negative';
    END IF;
END$$

-- Trigger: prevent_variant_delete_if_in_order
DROP TRIGGER IF EXISTS `prevent_variant_delete_if_in_order`$$

CREATE DEFINER=`root`@`localhost` TRIGGER `prevent_variant_delete_if_in_order` BEFORE DELETE ON `variant` FOR EACH ROW BEGIN
            -- Check if this variant is referenced in any order_item
            IF EXISTS (
                SELECT 1
                FROM order_item
                WHERE variant_id = OLD.variant_id
            ) THEN
                SIGNAL SQLSTATE '45000'
                SET MESSAGE_TEXT = 'Cannot delete variant: This variant is part of existing orders and cannot be removed.';
            END IF;
        END$$

DELIMITER ;
