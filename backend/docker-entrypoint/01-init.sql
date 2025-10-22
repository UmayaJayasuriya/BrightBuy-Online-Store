-- ============================================
-- MedSync Complete Database Backup
-- Generated: 2025-10-22 15:42:41
-- ============================================

-- ============================================
-- MedSync Schema (DDL) Export
-- Generated: 2025-10-22 15:42:41
-- ============================================

CREATE DATABASE IF NOT EXISTS `brightbuy`;
USE `brightbuy`;

-- ============================================
-- Table: address
-- ============================================
DROP TABLE IF EXISTS `address`;

CREATE TABLE `address` (
  `address_id` int NOT NULL AUTO_INCREMENT,
  `city_id` int DEFAULT NULL,
  `house_number` int DEFAULT NULL,
  `street` varchar(100) DEFAULT NULL,
  `city` varchar(100) DEFAULT NULL,
  `state` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`address_id`),
  KEY `city_id` (`city_id`),
  CONSTRAINT `address_ibfk_1` FOREIGN KEY (`city_id`) REFERENCES `location` (`city_id`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=39 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ============================================
-- Table: admin_verification_codes
-- ============================================
DROP TABLE IF EXISTS `admin_verification_codes`;

CREATE TABLE `admin_verification_codes` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `verification_code` varchar(6) NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `expires_at` timestamp NOT NULL,
  `is_used` tinyint(1) DEFAULT '0',
  `attempts` int DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `idx_user_code` (`user_id`,`verification_code`),
  KEY `idx_expires` (`expires_at`),
  CONSTRAINT `admin_verification_codes_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ============================================
-- Table: card
-- ============================================
DROP TABLE IF EXISTS `card`;

CREATE TABLE `card` (
  `card_id` int NOT NULL AUTO_INCREMENT,
  `order_id` int DEFAULT NULL,
  `card_number` varchar(50) DEFAULT NULL,
  `card_name` varchar(50) DEFAULT NULL,
  `expiry_date` varchar(50) DEFAULT NULL,
  `CVV` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`card_id`),
  KEY `order_id` (`order_id`),
  CONSTRAINT `card_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `orders` (`order_id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ============================================
-- Table: cart
-- ============================================
DROP TABLE IF EXISTS `cart`;

CREATE TABLE `cart` (
  `cart_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `created_date` datetime DEFAULT NULL,
  `total_amount` decimal(10,2) DEFAULT NULL,
  PRIMARY KEY (`cart_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `cart_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ============================================
-- Table: cart_item
-- ============================================
DROP TABLE IF EXISTS `cart_item`;

CREATE TABLE `cart_item` (
  `cart_item_id` int NOT NULL AUTO_INCREMENT,
  `cart_id` int DEFAULT NULL,
  `variant_id` int DEFAULT NULL,
  `quantity` int DEFAULT NULL,
  PRIMARY KEY (`cart_item_id`),
  KEY `variant_id` (`variant_id`),
  KEY `cart_item_ibfk_1` (`cart_id`),
  CONSTRAINT `cart_item_ibfk_1` FOREIGN KEY (`cart_id`) REFERENCES `cart` (`cart_id`) ON DELETE CASCADE,
  CONSTRAINT `cart_item_ibfk_2` FOREIGN KEY (`variant_id`) REFERENCES `variant` (`variant_id`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=36 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ============================================
-- Table: category
-- ============================================
DROP TABLE IF EXISTS `category`;

CREATE TABLE `category` (
  `category_id` int NOT NULL AUTO_INCREMENT,
  `category_name` varchar(100) DEFAULT NULL,
  `parent_category_id` int DEFAULT NULL,
  PRIMARY KEY (`category_id`),
  KEY `parent_category_id` (`parent_category_id`),
  CONSTRAINT `category_ibfk_1` FOREIGN KEY (`parent_category_id`) REFERENCES `category` (`category_id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ============================================
-- Table: category_order_summary
-- ============================================
DROP TABLE IF EXISTS `category_order_summary`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `category_order_summary` AS select coalesce(`c`.`category_name`,'Uncategorized') AS `category_name`,`c`.`category_id` AS `category_id`,count(distinct `o`.`order_id`) AS `total_orders`,sum(`oi`.`quantity`) AS `total_items_sold`,sum((`oi`.`quantity` * `oi`.`price`)) AS `total_revenue`,avg((`oi`.`quantity` * `oi`.`price`)) AS `average_order_value`,count(distinct `p`.`product_id`) AS `unique_products`,min(`o`.`order_date`) AS `first_order_date`,max(`o`.`order_date`) AS `last_order_date` from ((((`order_item` `oi` join `orders` `o` on((`oi`.`order_id` = `o`.`order_id`))) join `variant` `v` on((`oi`.`variant_id` = `v`.`variant_id`))) join `product` `p` on((`v`.`product_id` = `p`.`product_id`))) left join `category` `c` on((`p`.`category_id` = `c`.`category_id`))) group by `c`.`category_id`,`c`.`category_name` order by `total_revenue` desc;

-- ============================================
-- Table: contact
-- ============================================
DROP TABLE IF EXISTS `contact`;

CREATE TABLE `contact` (
  `contact_id` int NOT NULL AUTO_INCREMENT,
  `customer_name` varchar(50) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  `subject_name` varchar(50) DEFAULT NULL,
  `message` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`contact_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ============================================
-- Table: customer_order_payment_summary
-- ============================================
DROP TABLE IF EXISTS `customer_order_payment_summary`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `customer_order_payment_summary` AS select `u`.`user_id` AS `user_id`,`u`.`user_name` AS `user_name`,`u`.`email` AS `email`,`u`.`name` AS `full_name`,`o`.`order_id` AS `order_id`,`o`.`order_date` AS `order_date`,`o`.`total_amount` AS `total_amount`,`p`.`payment_method` AS `payment_method`,`p`.`payment_status` AS `payment_status`,`p`.`payment_date` AS `payment_date`,`d`.`delivery_status` AS `delivery_status`,`d`.`delivery_method` AS `delivery_method`,`d`.`estimated_delivery_date` AS `estimated_delivery_date`,count(`oi`.`order_item_id`) AS `items_in_order`,sum(`oi`.`quantity`) AS `total_quantity` from ((((`user` `u` left join `orders` `o` on((`u`.`user_id` = `o`.`user_id`))) left join `payment` `p` on((`o`.`order_id` = `p`.`order_id`))) left join `delivery` `d` on((`o`.`order_id` = `d`.`order_id`))) left join `order_item` `oi` on((`o`.`order_id` = `oi`.`order_id`))) group by `u`.`user_id`,`u`.`user_name`,`u`.`email`,`u`.`name`,`o`.`order_id`,`o`.`order_date`,`o`.`total_amount`,`p`.`payment_method`,`p`.`payment_status`,`p`.`payment_date`,`d`.`delivery_status`,`d`.`delivery_method`,`d`.`estimated_delivery_date` order by `u`.`user_id`,`o`.`order_date` desc;

-- ============================================
-- Table: customer_summary_statistics
-- ============================================
DROP TABLE IF EXISTS `customer_summary_statistics`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `customer_summary_statistics` AS select `u`.`user_id` AS `user_id`,`u`.`user_name` AS `user_name`,`u`.`email` AS `email`,`u`.`name` AS `full_name`,count(distinct `o`.`order_id`) AS `total_orders`,sum(`o`.`total_amount`) AS `total_spent`,avg(`o`.`total_amount`) AS `average_order_value`,min(`o`.`order_date`) AS `first_order_date`,max(`o`.`order_date`) AS `last_order_date`,sum((case when (`p`.`payment_status` = 'completed') then 1 else 0 end)) AS `completed_payments`,sum((case when (`p`.`payment_status` = 'pending') then 1 else 0 end)) AS `pending_payments`,sum((case when (`d`.`delivery_status` = 'delivered') then 1 else 0 end)) AS `delivered_orders`,sum((case when (`d`.`delivery_status` = 'pending') then 1 else 0 end)) AS `pending_deliveries` from (((`user` `u` left join `orders` `o` on((`u`.`user_id` = `o`.`user_id`))) left join `payment` `p` on((`o`.`order_id` = `p`.`order_id`))) left join `delivery` `d` on((`o`.`order_id` = `d`.`order_id`))) group by `u`.`user_id`,`u`.`user_name`,`u`.`email`,`u`.`name` having (`total_orders` > 0) order by `total_spent` desc;

-- ============================================
-- Table: delivery
-- ============================================
DROP TABLE IF EXISTS `delivery`;

CREATE TABLE `delivery` (
  `delivery_id` int NOT NULL AUTO_INCREMENT,
  `order_id` int DEFAULT NULL,
  `delivery_method` varchar(50) DEFAULT NULL,
  `address_id` int DEFAULT NULL,
  `estimated_delivery_date` date DEFAULT NULL,
  `delivery_status` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`delivery_id`),
  KEY `order_id` (`order_id`),
  KEY `delivery_ibfk_2` (`address_id`),
  CONSTRAINT `delivery_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `orders` (`order_id`) ON DELETE CASCADE,
  CONSTRAINT `delivery_ibfk_2` FOREIGN KEY (`address_id`) REFERENCES `address` (`address_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ============================================
-- Table: favorite_product
-- ============================================
DROP TABLE IF EXISTS `favorite_product`;

CREATE TABLE `favorite_product` (
  `favorite_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `product_id` int NOT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`favorite_id`),
  UNIQUE KEY `unique_user_product` (`user_id`,`product_id`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_product_id` (`product_id`),
  CONSTRAINT `favorite_product_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`) ON DELETE CASCADE,
  CONSTRAINT `favorite_product_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `product` (`product_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ============================================
-- Table: location
-- ============================================
DROP TABLE IF EXISTS `location`;

CREATE TABLE `location` (
  `city_id` int NOT NULL,
  `city` varchar(100) DEFAULT NULL,
  `zip_code` int DEFAULT NULL,
  `Is_main_city` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`city_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ============================================
-- Table: order_item
-- ============================================
DROP TABLE IF EXISTS `order_item`;

CREATE TABLE `order_item` (
  `order_item_id` int NOT NULL AUTO_INCREMENT,
  `order_id` int NOT NULL,
  `variant_id` int DEFAULT NULL,
  `quantity` int NOT NULL,
  `price` decimal(10,2) NOT NULL,
  PRIMARY KEY (`order_item_id`),
  KEY `order_id` (`order_id`),
  KEY `order_item_ibfk_2` (`variant_id`),
  CONSTRAINT `order_item_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `orders` (`order_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `order_item_ibfk_2` FOREIGN KEY (`variant_id`) REFERENCES `variant` (`variant_id`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ============================================
-- Table: orders
-- ============================================
DROP TABLE IF EXISTS `orders`;

CREATE TABLE `orders` (
  `order_id` int NOT NULL AUTO_INCREMENT,
  `cart_id` int NOT NULL,
  `user_id` int NOT NULL,
  `order_date` datetime NOT NULL,
  `total_amount` decimal(10,2) NOT NULL,
  PRIMARY KEY (`order_id`),
  KEY `cart_id` (`cart_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`cart_id`) REFERENCES `cart` (`cart_id`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `orders_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ============================================
-- Table: payment
-- ============================================
DROP TABLE IF EXISTS `payment`;

CREATE TABLE `payment` (
  `payment_id` int NOT NULL AUTO_INCREMENT,
  `order_id` int NOT NULL,
  `payment_method` varchar(30) NOT NULL,
  `payment_status` varchar(30) NOT NULL,
  `payment_date` datetime NOT NULL,
  PRIMARY KEY (`payment_id`),
  KEY `order_id` (`order_id`),
  CONSTRAINT `payment_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `orders` (`order_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ============================================
-- Table: product
-- ============================================
DROP TABLE IF EXISTS `product`;

CREATE TABLE `product` (
  `product_id` int NOT NULL AUTO_INCREMENT,
  `product_name` varchar(100) DEFAULT NULL,
  `category_id` int DEFAULT NULL,
  `description` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`product_id`),
  KEY `category_id` (`category_id`),
  CONSTRAINT `product_ibfk_1` FOREIGN KEY (`category_id`) REFERENCES `category` (`category_id`)
) ENGINE=InnoDB AUTO_INCREMENT=47 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ============================================
-- Table: quarterly_sales_report
-- ============================================
DROP TABLE IF EXISTS `quarterly_sales_report`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `quarterly_sales_report` AS select `quarterly_data`.`year` AS `year`,`quarterly_data`.`quarter` AS `quarter`,concat('Q',`quarterly_data`.`quarter`,' ',`quarterly_data`.`year`) AS `quarter_label`,`quarterly_data`.`total_orders` AS `total_orders`,`quarterly_data`.`unique_customers` AS `unique_customers`,`quarterly_data`.`total_revenue` AS `total_revenue`,`quarterly_data`.`average_order_value` AS `average_order_value`,`quarterly_data`.`total_items_sold` AS `total_items_sold` from (select year(`o`.`order_date`) AS `year`,quarter(`o`.`order_date`) AS `quarter`,count(distinct `o`.`order_id`) AS `total_orders`,count(distinct `o`.`user_id`) AS `unique_customers`,sum(`o`.`total_amount`) AS `total_revenue`,avg(`o`.`total_amount`) AS `average_order_value`,sum(`oi`.`quantity`) AS `total_items_sold` from (`orders` `o` left join `order_item` `oi` on((`o`.`order_id` = `oi`.`order_id`))) group by year(`o`.`order_date`),quarter(`o`.`order_date`)) `quarterly_data` order by `quarterly_data`.`year` desc,`quarterly_data`.`quarter` desc;

-- ============================================
-- Table: top_selling_products
-- ============================================
DROP TABLE IF EXISTS `top_selling_products`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `top_selling_products` AS select `p`.`product_id` AS `product_id`,`p`.`product_name` AS `product_name`,`c`.`category_name` AS `category_name`,`v`.`variant_id` AS `variant_id`,`v`.`variant_name` AS `variant_name`,`v`.`SKU` AS `SKU`,sum(`oi`.`quantity`) AS `total_quantity_sold`,sum((`oi`.`quantity` * `oi`.`price`)) AS `total_revenue`,avg(`oi`.`price`) AS `average_price`,count(distinct `oi`.`order_id`) AS `number_of_orders`,min(`o`.`order_date`) AS `first_sale_date`,max(`o`.`order_date`) AS `last_sale_date` from ((((`order_item` `oi` join `variant` `v` on((`oi`.`variant_id` = `v`.`variant_id`))) join `product` `p` on((`v`.`product_id` = `p`.`product_id`))) left join `category` `c` on((`p`.`category_id` = `c`.`category_id`))) join `orders` `o` on((`oi`.`order_id` = `o`.`order_id`))) group by `p`.`product_id`,`p`.`product_name`,`c`.`category_name`,`v`.`variant_id`,`v`.`variant_name`,`v`.`SKU` order by `total_quantity_sold` desc;

-- ============================================
-- Table: user
-- ============================================
DROP TABLE IF EXISTS `user`;

CREATE TABLE `user` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `user_name` varchar(50) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `name` varchar(50) DEFAULT NULL,
  `password_hash` varchar(100) DEFAULT NULL,
  `user_type` varchar(30) DEFAULT NULL,
  `address_id` int DEFAULT NULL,
  PRIMARY KEY (`user_id`),
  KEY `user_ibfk_1` (`address_id`),
  CONSTRAINT `user_ibfk_1` FOREIGN KEY (`address_id`) REFERENCES `address` (`address_id`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ============================================
-- Table: variant
-- ============================================
DROP TABLE IF EXISTS `variant`;

CREATE TABLE `variant` (
  `variant_id` int NOT NULL AUTO_INCREMENT,
  `variant_name` varchar(50) NOT NULL,
  `product_id` int DEFAULT NULL,
  `price` decimal(10,2) DEFAULT NULL,
  `quantity` int DEFAULT NULL,
  `SKU` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`variant_id`),
  KEY `product_id` (`product_id`),
  CONSTRAINT `variant_ibfk_1` FOREIGN KEY (`product_id`) REFERENCES `product` (`product_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=89 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ============================================
-- Table: variant_attribute
-- ============================================
DROP TABLE IF EXISTS `variant_attribute`;

CREATE TABLE `variant_attribute` (
  `attribute_id` int NOT NULL,
  `attribute_name` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`attribute_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ============================================
-- Table: variant_attribute_value
-- ============================================
DROP TABLE IF EXISTS `variant_attribute_value`;

CREATE TABLE `variant_attribute_value` (
  `id` int NOT NULL,
  `variant_id` int DEFAULT NULL,
  `attribute_id` int NOT NULL,
  `value` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `variant_id` (`variant_id`),
  KEY `attribute_id` (`attribute_id`),
  CONSTRAINT `variant_attribute_value_ibfk_1` FOREIGN KEY (`variant_id`) REFERENCES `variant` (`variant_id`) ON DELETE CASCADE,
  CONSTRAINT `variant_attribute_value_ibfk_2` FOREIGN KEY (`attribute_id`) REFERENCES `variant_attribute` (`attribute_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;



-- ============================================
-- MedSync Stored Procedures Export
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

DELIMITER ;


-- ============================================
-- MedSync Functions Export
-- Generated: 2025-10-22 15:42:41
-- ============================================

USE `brightbuy`;

DELIMITER $$

-- No functions found

DELIMITER ;


-- ============================================
-- MedSync Triggers Export
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


-- ============================================
-- MedSync Views Export
-- Generated: 2025-10-22 15:42:41
-- ============================================

USE `brightbuy`;

-- View: category_order_summary
DROP VIEW IF EXISTS `category_order_summary`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `category_order_summary` AS select coalesce(`c`.`category_name`,'Uncategorized') AS `category_name`,`c`.`category_id` AS `category_id`,count(distinct `o`.`order_id`) AS `total_orders`,sum(`oi`.`quantity`) AS `total_items_sold`,sum((`oi`.`quantity` * `oi`.`price`)) AS `total_revenue`,avg((`oi`.`quantity` * `oi`.`price`)) AS `average_order_value`,count(distinct `p`.`product_id`) AS `unique_products`,min(`o`.`order_date`) AS `first_order_date`,max(`o`.`order_date`) AS `last_order_date` from ((((`order_item` `oi` join `orders` `o` on((`oi`.`order_id` = `o`.`order_id`))) join `variant` `v` on((`oi`.`variant_id` = `v`.`variant_id`))) join `product` `p` on((`v`.`product_id` = `p`.`product_id`))) left join `category` `c` on((`p`.`category_id` = `c`.`category_id`))) group by `c`.`category_id`,`c`.`category_name` order by `total_revenue` desc;

-- View: customer_order_payment_summary
DROP VIEW IF EXISTS `customer_order_payment_summary`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `customer_order_payment_summary` AS select `u`.`user_id` AS `user_id`,`u`.`user_name` AS `user_name`,`u`.`email` AS `email`,`u`.`name` AS `full_name`,`o`.`order_id` AS `order_id`,`o`.`order_date` AS `order_date`,`o`.`total_amount` AS `total_amount`,`p`.`payment_method` AS `payment_method`,`p`.`payment_status` AS `payment_status`,`p`.`payment_date` AS `payment_date`,`d`.`delivery_status` AS `delivery_status`,`d`.`delivery_method` AS `delivery_method`,`d`.`estimated_delivery_date` AS `estimated_delivery_date`,count(`oi`.`order_item_id`) AS `items_in_order`,sum(`oi`.`quantity`) AS `total_quantity` from ((((`user` `u` left join `orders` `o` on((`u`.`user_id` = `o`.`user_id`))) left join `payment` `p` on((`o`.`order_id` = `p`.`order_id`))) left join `delivery` `d` on((`o`.`order_id` = `d`.`order_id`))) left join `order_item` `oi` on((`o`.`order_id` = `oi`.`order_id`))) group by `u`.`user_id`,`u`.`user_name`,`u`.`email`,`u`.`name`,`o`.`order_id`,`o`.`order_date`,`o`.`total_amount`,`p`.`payment_method`,`p`.`payment_status`,`p`.`payment_date`,`d`.`delivery_status`,`d`.`delivery_method`,`d`.`estimated_delivery_date` order by `u`.`user_id`,`o`.`order_date` desc;

-- View: customer_summary_statistics
DROP VIEW IF EXISTS `customer_summary_statistics`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `customer_summary_statistics` AS select `u`.`user_id` AS `user_id`,`u`.`user_name` AS `user_name`,`u`.`email` AS `email`,`u`.`name` AS `full_name`,count(distinct `o`.`order_id`) AS `total_orders`,sum(`o`.`total_amount`) AS `total_spent`,avg(`o`.`total_amount`) AS `average_order_value`,min(`o`.`order_date`) AS `first_order_date`,max(`o`.`order_date`) AS `last_order_date`,sum((case when (`p`.`payment_status` = 'completed') then 1 else 0 end)) AS `completed_payments`,sum((case when (`p`.`payment_status` = 'pending') then 1 else 0 end)) AS `pending_payments`,sum((case when (`d`.`delivery_status` = 'delivered') then 1 else 0 end)) AS `delivered_orders`,sum((case when (`d`.`delivery_status` = 'pending') then 1 else 0 end)) AS `pending_deliveries` from (((`user` `u` left join `orders` `o` on((`u`.`user_id` = `o`.`user_id`))) left join `payment` `p` on((`o`.`order_id` = `p`.`order_id`))) left join `delivery` `d` on((`o`.`order_id` = `d`.`order_id`))) group by `u`.`user_id`,`u`.`user_name`,`u`.`email`,`u`.`name` having (`total_orders` > 0) order by `total_spent` desc;

-- View: quarterly_sales_report
DROP VIEW IF EXISTS `quarterly_sales_report`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `quarterly_sales_report` AS select `quarterly_data`.`year` AS `year`,`quarterly_data`.`quarter` AS `quarter`,concat('Q',`quarterly_data`.`quarter`,' ',`quarterly_data`.`year`) AS `quarter_label`,`quarterly_data`.`total_orders` AS `total_orders`,`quarterly_data`.`unique_customers` AS `unique_customers`,`quarterly_data`.`total_revenue` AS `total_revenue`,`quarterly_data`.`average_order_value` AS `average_order_value`,`quarterly_data`.`total_items_sold` AS `total_items_sold` from (select year(`o`.`order_date`) AS `year`,quarter(`o`.`order_date`) AS `quarter`,count(distinct `o`.`order_id`) AS `total_orders`,count(distinct `o`.`user_id`) AS `unique_customers`,sum(`o`.`total_amount`) AS `total_revenue`,avg(`o`.`total_amount`) AS `average_order_value`,sum(`oi`.`quantity`) AS `total_items_sold` from (`orders` `o` left join `order_item` `oi` on((`o`.`order_id` = `oi`.`order_id`))) group by year(`o`.`order_date`),quarter(`o`.`order_date`)) `quarterly_data` order by `quarterly_data`.`year` desc,`quarterly_data`.`quarter` desc;

-- View: top_selling_products
DROP VIEW IF EXISTS `top_selling_products`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `top_selling_products` AS select `p`.`product_id` AS `product_id`,`p`.`product_name` AS `product_name`,`c`.`category_name` AS `category_name`,`v`.`variant_id` AS `variant_id`,`v`.`variant_name` AS `variant_name`,`v`.`SKU` AS `SKU`,sum(`oi`.`quantity`) AS `total_quantity_sold`,sum((`oi`.`quantity` * `oi`.`price`)) AS `total_revenue`,avg(`oi`.`price`) AS `average_price`,count(distinct `oi`.`order_id`) AS `number_of_orders`,min(`o`.`order_date`) AS `first_sale_date`,max(`o`.`order_date`) AS `last_sale_date` from ((((`order_item` `oi` join `variant` `v` on((`oi`.`variant_id` = `v`.`variant_id`))) join `product` `p` on((`v`.`product_id` = `p`.`product_id`))) left join `category` `c` on((`p`.`category_id` = `c`.`category_id`))) join `orders` `o` on((`oi`.`order_id` = `o`.`order_id`))) group by `p`.`product_id`,`p`.`product_name`,`c`.`category_name`,`v`.`variant_id`,`v`.`variant_name`,`v`.`SKU` order by `total_quantity_sold` desc;



-- ============================================
-- MedSync Data (DML) Export
-- Generated: 2025-10-22 15:42:41
-- ============================================

USE `brightbuy`;

SET FOREIGN_KEY_CHECKS=0;

-- ============================================
-- Data for table: address (14 rows)
-- ============================================

INSERT INTO `address` (`address_id`, `city_id`, `house_number`, `street`, `city`, `state`) VALUES
  (18, 1, 26, 'Main street', 'Dallas', 'Texas'),
  (19, 5, 6, 'Hill street', 'Austin', 'Texas'),
  (21, 5, 22, 'Green street', 'Austin', 'Texas'),
  (25, 2, 22, 'Bean Street', 'Houston', 'Texas'),
  (26, 5, 42, 'Maple Avenue', 'Austin', 'Illinois'),
  (27, 5, 44, 'jj', 'Austin', 'Texas'),
  (29, 2, 11, 'colombo street', 'Houston', 'Texas'),
  (31, 1, 22, 'colombo street', 'Dallas', 'Texas'),
  (33, 3, 23, 'hill street', 'San Antonio', 'Texas'),
  (34, 2, 34, '23 street', 'Houston', 'Texas'),
  (35, 2, 22, 'Bean Street', 'Houston', 'Texas'),
  (36, 1, 35, 'kkk', 'Dallas', 'Texas'),
  (37, 3, 98, 'hh', 'San Antonio', 'Texas'),
  (38, 4, 33, 'bean street', 'Fort Worth', 'Texas');

-- ============================================
-- Data for table: admin_verification_codes (9 rows)
-- ============================================

INSERT INTO `admin_verification_codes` (`id`, `user_id`, `verification_code`, `created_at`, `expires_at`, `is_used`, `attempts`) VALUES
  (3, 13, '629660', '2025-10-21 14:35:11', '2025-10-21 14:45:12', 1, 0),
  (4, 13, '201277', '2025-10-21 14:35:41', '2025-10-21 14:45:42', 1, 0),
  (5, 13, '418803', '2025-10-21 14:52:20', '2025-10-21 15:02:21', 1, 0),
  (6, 13, '204965', '2025-10-21 14:52:53', '2025-10-21 15:02:54', 1, 2),
  (7, 13, '715269', '2025-10-21 18:27:28', '2025-10-21 18:37:29', 1, 1),
  (8, 13, '157224', '2025-10-21 19:41:46', '2025-10-21 19:51:47', 1, 0),
  (9, 13, '424791', '2025-10-21 20:07:34', '2025-10-21 20:17:34', 1, 1),
  (10, 13, '882913', '2025-10-21 20:34:50', '2025-10-21 20:44:50', 1, 0),
  (11, 13, '068378', '2025-10-22 10:35:26', '2025-10-22 10:45:27', 1, 0);

-- ============================================
-- Data for table: card (6 rows)
-- ============================================

INSERT INTO `card` (`card_id`, `order_id`, `card_number`, `card_name`, `expiry_date`, `CVV`) VALUES
  (1, 5, '3846 0634 0875 6340', 'Hima', '12/26', '333'),
  (2, 7, '7890 6976 3562 7768', 'Hima', '05/27', '666'),
  (3, 9, '6275 1694 3914 0121', 'jsbcksdc', '06/29', '222'),
  (4, 11, '9673 5426 6763 4345', 'kchjgc', '12/34', '586'),
  (5, 12, '3262 7356 9845 2374', 'shamila', '04/26', '678'),
  (6, 13, '6324 5932 3022 4454', 'jdlksjhfls', '06/29', '367');

-- ============================================
-- Data for table: cart (5 rows)
-- ============================================

INSERT INTO `cart` (`cart_id`, `user_id`, `created_date`, `total_amount`) VALUES
  (1, 10, '2025-10-11 10:39:11', '0.00'),
  (2, 11, '2025-10-11 13:03:09', '0.00'),
  (3, 13, NULL, '0.00'),
  (4, 20, NULL, '59.00'),
  (5, 22, NULL, '0.00');

-- ============================================
-- Data for table: cart_item (1 rows)
-- ============================================

INSERT INTO `cart_item` (`cart_item_id`, `cart_id`, `variant_id`, `quantity`) VALUES
  (27, 4, 7, 1);

-- ============================================
-- Data for table: category (13 rows)
-- ============================================

INSERT INTO `category` (`category_id`, `category_name`, `parent_category_id`) VALUES
  (1, 'Mobile & Accessories', NULL),
  (2, 'Computers & Gaming', NULL),
  (3, 'Smart Tech & Lifestyle', NULL),
  (4, 'Smartphones', 1),
  (5, 'Mobile Accessories', 1),
  (6, 'Tablets & E-Readers', 1),
  (7, 'Laptops', 2),
  (8, 'Mouse & Keyboards', 2),
  (9, 'Gaming Consoles', 2),
  (10, 'Smart Watches & Wearables', 3),
  (11, 'Smart Home Devices', 3),
  (12, 'Toys & Gadgets', 3),
  (13, 'Bluetooth Speakers', 3);

-- ============================================
-- Data for table: category_order_summary (8 rows)
-- ============================================

INSERT INTO `category_order_summary` (`category_name`, `category_id`, `total_orders`, `total_items_sold`, `total_revenue`, `average_order_value`, `unique_products`, `first_order_date`, `last_order_date`) VALUES
  ('Smartphones', 4, 8, '22', '22950.92', '1912.576667', 4, '2025-10-13 10:05:21', '2025-10-21 14:19:57'),
  ('Laptops', 7, 2, '5', '6895.00', '3447.500000', 2, '2025-10-13 10:05:21', '2025-10-16 18:06:29'),
  ('Tablets & E-Readers', 6, 2, '2', '1398.00', '699.000000', 2, '2025-10-21 10:25:08', '2025-10-21 10:29:10'),
  ('Mobile Accessories', 5, 5, '10', '956.94', '159.490000', 3, '2025-10-13 10:05:21', '2025-10-20 06:54:56'),
  ('Toys & Gadgets', 12, 1, '1', '199.00', '199.000000', 1, '2025-10-21 10:25:08', '2025-10-21 10:25:08'),
  ('Mouse & Keyboards', 8, 1, '3', '183.50', '91.750000', 2, '2025-10-14 15:54:57', '2025-10-14 15:54:57'),
  ('Gaming Consoles', 9, 1, '1', '100.50', '100.500000', 1, '2025-10-13 10:05:21', '2025-10-13 10:05:21'),
  ('Smart Home Devices', 11, 1, '1', '99.00', '99.000000', 1, '2025-10-18 13:18:52', '2025-10-18 13:18:52');

-- ============================================
-- Data for table: contact (3 rows)
-- ============================================

INSERT INTO `contact` (`contact_id`, `customer_name`, `email`, `subject_name`, `message`) VALUES
  (1, 'John Doe', 'a@b.com', 'Test', 'This is a test message'),
  (2, 'Hima', 'himak@gmail.com', 'is', 'hmfj'),
  (3, 'Himandi', 'fernandoshamila@gmail.com', 'Testtt', 'hiiiiii');

-- ============================================
-- Data for table: customer_order_payment_summary (21 rows)
-- ============================================

INSERT INTO `customer_order_payment_summary` (`user_id`, `user_name`, `email`, `full_name`, `order_id`, `order_date`, `total_amount`, `payment_method`, `payment_status`, `payment_date`, `delivery_status`, `delivery_method`, `estimated_delivery_date`, `items_in_order`, `total_quantity`) VALUES
  (10, 'himak', 'himanndhikuruppu@gmail.com', 'Himandhi K', 14, '2025-10-20 10:00:10', '4150.99', 'cod', 'pending', '2025-10-20 10:00:10', 'pending', 'store_pickup', '2025-10-22', 4, '5'),
  (10, 'himak', 'himanndhikuruppu@gmail.com', 'Himandhi K', 9, '2025-10-16 18:06:29', '6695.00', 'card', 'completed', '2025-10-16 18:06:29', 'Delivered', 'home_delivery', '2025-10-21', 2, '5'),
  (10, 'himak', 'himanndhikuruppu@gmail.com', 'Himandhi K', 7, '2025-10-16 10:19:21', '7674.97', 'card', 'completed', '2025-10-16 10:19:21', 'Delivered', 'store_pickup', '2025-10-18', 3, '8'),
  (10, 'himak', 'himanndhikuruppu@gmail.com', 'Himandhi K', 6, '2025-10-14 16:31:32', '2198.00', 'cod', 'pending', '2025-10-14 16:31:32', 'pending', 'store_pickup', '2025-10-16', 1, '2'),
  (10, 'himak', 'himanndhikuruppu@gmail.com', 'Himandhi K', 5, '2025-10-14 15:54:57', '183.50', 'card', 'completed', '2025-10-14 15:54:57', 'pending', 'store_pickup', '2025-10-16', 2, '3'),
  (11, 'hima2', 'himanndhik@gmail.com', 'Himandhi K', 15, '2025-10-21 10:25:08', '498.00', 'cod', 'pending', '2025-10-21 10:25:08', 'pending', 'store_pickup', '2025-10-23', 2, '2'),
  (11, 'hima2', 'himanndhik@gmail.com', 'Himandhi K', 13, '2025-10-20 06:54:56', '59.00', 'card', 'completed', '2025-10-20 06:54:56', 'pending', 'store_pickup', '2025-10-22', 1, '1'),
  (11, 'hima2', 'himanndhik@gmail.com', 'Himandhi K', 12, '2025-10-18 15:51:56', '2839.98', 'card', 'completed', '2025-10-18 15:51:56', 'pending', 'store_pickup', '2025-10-20', 1, '2'),
  (11, 'hima2', 'himanndhik@gmail.com', 'Himandhi K', 11, '2025-10-18 13:18:52', '332.98', 'card', 'completed', '2025-10-18 13:18:52', 'Delivered', 'home_delivery', '2025-10-23', 2, '3'),
  (11, 'hima2', 'himanndhik@gmail.com', 'Himandhi K', 4, '2025-10-13 10:34:12', '486.96', 'card', 'completed', '2025-10-13 10:34:12', 'pending', 'store_pickup', '2025-10-15', 2, '4'),
  (11, 'hima2', 'himanndhik@gmail.com', 'Himandhi K', 3, '2025-10-13 10:19:54', '1099.00', 'cod', 'completed', '2025-10-13 10:19:54', 'pending', 'store_pickup', '2025-10-15', 1, '1'),
  (11, 'hima2', 'himanndhik@gmail.com', 'Himandhi K', 2, '2025-10-13 10:05:21', '5397.48', 'card', 'completed', '2025-10-13 10:05:21', 'Delivered', 'home_delivery', '2025-10-18', 4, '6'),
  (13, 'admin1', 'himandhik.23@cse.mrt.ac.lk', 'Admin 1', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL),
  (17, 'Senilka1', 'senilkat@gmail.com', 'Senilka M T', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL),
  (18, 'johndoe92', 'john.doe@example.com', 'John Doe', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL),
  (19, 'test1', 'test1@gmail.com', 'Test 1', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL),
  (20, 'thira1', 'thirani@gmail.com', 'Thirani Kuruppu', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL),
  (21, 'hasini123', 'hasini@gmail.com', 'Hasini Lawanya', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL),
  (22, 'hima6', 'fernandoshamila@gmail.com', 'Shamila Fernando', 17, '2025-10-21 14:19:57', '68.00', 'cod', 'pending', '2025-10-21 14:19:57', 'pending', 'home_delivery', '2025-10-29', 1, '2'),
  (22, 'hima6', 'fernandoshamila@gmail.com', 'Shamila Fernando', 16, '2025-10-21 10:29:10', '1099.00', 'cod', 'pending', '2025-10-21 10:29:10', 'pending', 'store_pickup', '2025-10-23', 1, '1'),
  (23, 'hima7', 'himandhikuruppu@gmail.com', 'Himandhi Kururppu', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL);

-- ============================================
-- Data for table: customer_summary_statistics (3 rows)
-- ============================================

INSERT INTO `customer_summary_statistics` (`user_id`, `user_name`, `email`, `full_name`, `total_orders`, `total_spent`, `average_order_value`, `first_order_date`, `last_order_date`, `completed_payments`, `pending_payments`, `delivered_orders`, `pending_deliveries`) VALUES
  (10, 'himak', 'himanndhikuruppu@gmail.com', 'Himandhi K', 5, '20902.46', '4180.492000', '2025-10-14 15:54:57', '2025-10-20 10:00:10', '3', '2', '2', '3'),
  (11, 'hima2', 'himanndhik@gmail.com', 'Himandhi K', 7, '10713.40', '1530.485714', '2025-10-13 10:05:21', '2025-10-21 10:25:08', '6', '1', '2', '5'),
  (22, 'hima6', 'fernandoshamila@gmail.com', 'Shamila Fernando', 2, '1167.00', '583.500000', '2025-10-21 10:29:10', '2025-10-21 14:19:57', '0', '2', '0', '2');

-- ============================================
-- Data for table: delivery (14 rows)
-- ============================================

INSERT INTO `delivery` (`delivery_id`, `order_id`, `delivery_method`, `address_id`, `estimated_delivery_date`, `delivery_status`) VALUES
  (1, 2, 'home_delivery', 29, '2025-10-18', 'Delivered'),
  (2, 3, 'store_pickup', NULL, '2025-10-15', 'pending'),
  (3, 4, 'store_pickup', NULL, '2025-10-15', 'pending'),
  (4, 5, 'store_pickup', NULL, '2025-10-16', 'pending'),
  (5, 6, 'store_pickup', NULL, '2025-10-16', 'pending'),
  (6, 7, 'store_pickup', NULL, '2025-10-18', 'Delivered'),
  (7, 9, 'home_delivery', 31, '2025-10-21', 'Delivered'),
  (8, 11, 'home_delivery', 33, '2025-10-23', 'Delivered'),
  (9, 12, 'store_pickup', NULL, '2025-10-20', 'pending'),
  (10, 13, 'store_pickup', NULL, '2025-10-22', 'pending'),
  (11, 14, 'store_pickup', NULL, '2025-10-22', 'pending'),
  (12, 15, 'store_pickup', NULL, '2025-10-23', 'pending'),
  (13, 16, 'store_pickup', NULL, '2025-10-23', 'pending'),
  (14, 17, 'home_delivery', 37, '2025-10-29', 'pending');

-- ============================================
-- Data for table: favorite_product (5 rows)
-- ============================================

INSERT INTO `favorite_product` (`favorite_id`, `user_id`, `product_id`, `created_at`) VALUES
  (2, 11, 4, '2025-10-19 08:12:46'),
  (3, 11, 18, '2025-10-19 08:12:50'),
  (4, 10, 4, '2025-10-20 11:30:38'),
  (5, 21, 33, '2025-10-20 17:10:31'),
  (6, 21, 30, '2025-10-20 17:10:32');

-- ============================================
-- Data for table: location (11 rows)
-- ============================================

INSERT INTO `location` (`city_id`, `city`, `zip_code`, `Is_main_city`) VALUES
  (1, 'Dallas', 120, 1),
  (2, 'Houston', 121, 1),
  (3, 'San Antonio', 122, 1),
  (4, 'Fort Worth', 123, 1),
  (5, 'Austin', 124, 1),
  (6, 'El Paso', 125, 1),
  (7, 'Arlington', 126, 0),
  (8, 'Corpus Christi', 127, 0),
  (9, 'Plano', 128, 0),
  (10, 'Lubbock', 129, 0),
  (11, 'Irving', 130, 0);

-- ============================================
-- Data for table: order_item (27 rows)
-- ============================================

INSERT INTO `order_item` (`order_item_id`, `order_id`, `variant_id`, `quantity`, `price`) VALUES
  (1, 2, 47, 1, '100.50'),
  (2, 2, 3, 2, '1419.99'),
  (3, 2, 7, 1, '59.00'),
  (4, 2, 30, 2, '1199.00'),
  (5, 3, 1, 1, '1099.00'),
  (6, 4, 15, 2, '116.99'),
  (7, 4, 13, 2, '126.49'),
  (8, 5, 35, 1, '42.50'),
  (9, 5, 39, 2, '70.50'),
  (10, 6, 1, 2, '1099.00'),
  (11, 7, 3, 3, '1419.99'),
  (12, 7, 1, 3, '1099.00'),
  (13, 7, 7, 2, '59.00'),
  (16, 9, 1, 2, '1099.00'),
  (17, 9, 34, 3, '1499.00'),
  (20, 11, 15, 2, '116.99'),
  (21, 11, 59, 1, '99.00'),
  (22, 12, 3, 2, '1419.99'),
  (23, 13, 7, 1, '59.00'),
  (24, 14, 3, 1, '1419.99'),
  (25, 14, 1, 1, '1099.00'),
  (26, 14, 86, 1, '34.00'),
  (27, 14, 5, 2, '799.00'),
  (28, 15, 27, 1, '299.00'),
  (29, 15, 69, 1, '199.00'),
  (30, 16, 19, 1, '1099.00'),
  (31, 17, 86, 2, '34.00');

-- ============================================
-- Data for table: orders (14 rows)
-- ============================================

INSERT INTO `orders` (`order_id`, `cart_id`, `user_id`, `order_date`, `total_amount`) VALUES
  (2, 2, 11, '2025-10-13 10:05:21', '5397.48'),
  (3, 2, 11, '2025-10-13 10:19:54', '1099.00'),
  (4, 2, 11, '2025-10-13 10:34:12', '486.96'),
  (5, 1, 10, '2025-10-14 15:54:57', '183.50'),
  (6, 1, 10, '2025-10-14 16:31:32', '2198.00'),
  (7, 1, 10, '2025-10-16 10:19:21', '7674.97'),
  (9, 1, 10, '2025-10-16 18:06:29', '6695.00'),
  (11, 2, 11, '2025-10-18 13:18:52', '332.98'),
  (12, 2, 11, '2025-10-18 15:51:56', '2839.98'),
  (13, 2, 11, '2025-10-20 06:54:56', '59.00'),
  (14, 1, 10, '2025-10-20 10:00:10', '4150.99'),
  (15, 2, 11, '2025-10-21 10:25:08', '498.00'),
  (16, 5, 22, '2025-10-21 10:29:10', '1099.00'),
  (17, 5, 22, '2025-10-21 14:19:57', '68.00');

-- ============================================
-- Data for table: payment (14 rows)
-- ============================================

INSERT INTO `payment` (`payment_id`, `order_id`, `payment_method`, `payment_status`, `payment_date`) VALUES
  (1, 2, 'card', 'completed', '2025-10-13 10:05:21'),
  (2, 3, 'cod', 'completed', '2025-10-13 10:19:54'),
  (3, 4, 'card', 'completed', '2025-10-13 10:34:12'),
  (4, 5, 'card', 'completed', '2025-10-14 15:54:57'),
  (5, 6, 'cod', 'pending', '2025-10-14 16:31:32'),
  (6, 7, 'card', 'completed', '2025-10-16 10:19:21'),
  (8, 9, 'card', 'completed', '2025-10-16 18:06:29'),
  (10, 11, 'card', 'completed', '2025-10-18 13:18:52'),
  (11, 12, 'card', 'completed', '2025-10-18 15:51:56'),
  (12, 13, 'card', 'completed', '2025-10-20 06:54:56'),
  (13, 14, 'cod', 'pending', '2025-10-20 10:00:10'),
  (14, 15, 'cod', 'pending', '2025-10-21 10:25:08'),
  (15, 16, 'cod', 'pending', '2025-10-21 10:29:10'),
  (16, 17, 'cod', 'pending', '2025-10-21 14:19:57');

-- ============================================
-- Data for table: product (42 rows)
-- ============================================

INSERT INTO `product` (`product_id`, `product_name`, `category_id`, `description`) VALUES
  (1, 'Apple Phones', 4, 'A premium technology brand known for its innovative smartphones, laptops, and ecosystem of devices.'),
  (2, 'Samsung Phones', 4, 'A global electronics giant producing smartphones, TVs, home appliances, and cutting-edge technology solutions.'),
  (3, 'Google Phones', 4, 'A leading tech company specializing in internet services, AI solutions, and the Android operating system.'),
  (4, 'USB Cables', 5, 'A reliable cable for data transfer and charging devices quickly.'),
  (5, 'Power Bank', 5, 'A portable battery to charge your devices on the go.'),
  (6, 'Charging Adaptors', 5, 'A compact adapter for safe and efficient device charging.'),
  (7, 'SD Cards', 5, 'A memory card for storing photos, videos, and files.'),
  (8, 'Phone Cases', 5, 'A protective case to keep your phone safe from drops and scratches.'),
  (9, 'Screen Protectors', 5, 'A durable film to protect your phone screen from scratches and cracks.'),
  (10, 'Apple iPad Pro (M4)', 6, 'Latest generation iPad Pro with powerful M4 chip, available in multiple sizes and storage options.'),
  (11, 'Samsung Galaxy Tab S9+', 6, 'Premium Android tablet with high-resolution AMOLED display and multitasking support.'),
  (12, 'Amazon Kindle Paperwhite', 6, 'Lightweight e-reader with glare-free screen and adjustable warm light.'),
  (13, 'Amazon Kindle Oasis', 6, 'Premium Kindle with ergonomic design and page-turn buttons.'),
  (14, 'Lenovo Tab P12 Pro', 6, 'High-performance Lenovo tablet with vivid OLED display and stylus support.'),
  (15, 'Apple MacBook Air M3', 7, 'Ultra-thin and lightweight MacBook powered by Apple’s M3 chip.'),
  (16, 'Apple MacBook Pro M3 Pro', 7, 'Professional-grade MacBook with M3 Pro chip and stunning Liquid Retina XDR display.'),
  (17, 'Dell XPS 13 Plus', 7, 'Compact premium ultrabook with InfinityEdge display and powerful performance.'),
  (18, 'Logitech MX Keys Wireless Keyboard', 8, 'A premium wireless keyboard available in Graphite and Pale Gray, designed for productivity and comfort.'),
  (19, 'Razer BlackWidow V4 Pro Mechanical Keyboard', 8, 'A mechanical gaming keyboard with Green, Yellow, or Orange switches for customizable performance.'),
  (20, 'Logitech G Pro X Superlight Gaming Mouse', 8, 'An ultra-lightweight wireless gaming mouse, available in Black, White, and Pink.'),
  (21, 'Corsair K100 RGB Mechanical Keyboard', 8, 'A high-performance keyboard with OPX optical or Cherry MX Speed switches and dynamic RGB lighting.'),
  (22, 'PlayStation 5', 9, 'Sony\'s flagship gaming console, available in Standard Disc, Digital Edition, and Spider-Man 2 Bundle.'),
  (23, 'Xbox Series X', 9, 'Microsoft’s most powerful console, offered in 1TB Standard, Diablo IV, and Forza Horizon 5 bundles.'),
  (24, 'Nintendo Switch OLED Model', 9, 'A hybrid gaming console with a vibrant OLED display, available in White, Neon Red/Blue, and Zelda Edition.'),
  (25, 'Steam Deck', 9, 'A portable handheld gaming PC, available in 64GB LCD, 256GB SSD, and 512GB OLED versions.'),
  (26, 'Apple Watch Series 9', 10, 'A premium smartwatch offering advanced health, fitness, and connectivity features.'),
  (27, 'Samsung Galaxy Watch 6', 10, 'A versatile smartwatch with sleek design, fitness tracking, and smart connectivity.'),
  (28, 'Fitbit Versa 4', 10, 'A fitness-focused smartwatch with health tracking and personalized insights.'),
  (29, 'Garmin Forerunner 265', 10, 'A performance smartwatch designed for athletes with GPS and training features.'),
  (30, 'Google Nest Hub (2nd Gen)', 11, 'A smart display with Google Assistant for entertainment, control, and information.'),
  (31, 'Philips Hue Smart Bulb Starter Kit', 11, 'A smart lighting system with customizable ambiance and easy app control.'),
  (32, 'Ring Video Doorbell (Wired)', 11, 'A smart video doorbell with HD video, motion detection, and two-way talk.'),
  (33, 'TP-Link Kasa Smart Plug', 11, 'A smart plug that allows remote control of devices and energy monitoring.'),
  (34, 'USM Plasma Ball Sphere', 12, 'Touch-activated interactive lightning ball with USB power'),
  (35, 'Laser keyboard projector', 12, 'Portable Bluetooth laser keyboard for phones and tablets'),
  (36, 'Voice controlled robot pet', 12, 'Interactive toy robot that responds to commands and dances.'),
  (37, 'USB fan clock', 12, 'Flexible LED fan displaying real-time clock.'),
  (38, 'JBL mini speaker', 13, 'Mini speaker with an iconic design, rugged build, and rich sound.'),
  (39, 'Realme cobble speaker', 13, 'Compact, bass-boosted speaker with gaming mode.'),
  (40, 'EchoDot 5th gen speaker', 13, 'Alexa smart speaker with Bluetooth streaming.'),
  (41, 'Lenovo ThinkPlus K3 speaker', 13, 'Portable Bluetooth speaker with 360° sound.'),
  (46, 'Phone1', 4, 'test phone category');

-- ============================================
-- Data for table: quarterly_sales_report (1 rows)
-- ============================================

INSERT INTO `quarterly_sales_report` (`year`, `quarter`, `quarter_label`, `total_orders`, `unique_customers`, `total_revenue`, `average_order_value`, `total_items_sold`) VALUES
  (2025, 4, 'Q4 2025', 14, 3, '84974.65', '3147.209259', '45');

-- ============================================
-- Data for table: top_selling_products (16 rows)
-- ============================================

INSERT INTO `top_selling_products` (`product_id`, `product_name`, `category_name`, `variant_id`, `variant_name`, `SKU`, `total_quantity_sold`, `total_revenue`, `average_price`, `number_of_orders`, `first_sale_date`, `last_sale_date`) VALUES
  (1, 'Apple Phones', 'Smartphones', 1, 'iPhine 17 Pro', 'SKU001', '9', '9891.00', '1099.000000', 5, '2025-10-13 10:19:54', '2025-10-20 10:00:10'),
  (2, 'Samsung Phones', 'Smartphones', 3, 'Galaxy S25 Ultra', 'SKU003', '8', '11359.92', '1419.990000', 4, '2025-10-13 10:05:21', '2025-10-20 10:00:10'),
  (4, 'USB Cables', 'Mobile Accessories', 7, 'USB-C to Lightning', 'SKU007', '4', '236.00', '59.000000', 3, '2025-10-13 10:05:21', '2025-10-20 06:54:56'),
  (8, 'Phone Cases', 'Mobile Accessories', 15, 'iPhone 17 Pro Max Silicone ', 'SKU015', '4', '467.96', '116.990000', 2, '2025-10-13 10:34:12', '2025-10-18 13:18:52'),
  (17, 'Dell XPS 13 Plus', 'Laptops', 34, 'Dell XPS 13 Plus 16GB RAM / 512GB SSD', 'SKU034', '3', '4497.00', '1499.000000', 1, '2025-10-16 18:06:29', '2025-10-16 18:06:29'),
  (46, 'Phone1', 'Smartphones', 86, 'testphone1', 'sku100', '3', '102.00', '34.000000', 2, '2025-10-20 10:00:10', '2025-10-21 14:19:57'),
  (3, 'Google Phones', 'Smartphones', 5, 'Pixel 10', 'SKU005', '2', '1598.00', '799.000000', 1, '2025-10-20 10:00:10', '2025-10-20 10:00:10'),
  (7, 'SD Cards', 'Mobile Accessories', 13, '128GB', 'SKU013', '2', '252.98', '126.490000', 1, '2025-10-13 10:34:12', '2025-10-13 10:34:12'),
  (15, 'Apple MacBook Air M3', 'Laptops', 30, 'MacBook Air M3 13-inch 256 GB', 'SKU030', '2', '2398.00', '1199.000000', 1, '2025-10-13 10:05:21', '2025-10-13 10:05:21'),
  (20, 'Logitech G Pro X Superlight Gaming Mouse', 'Mouse & Keyboards', 39, 'Logitech G Pro X Superlight (Black)', 'SKU039', '2', '141.00', '70.500000', 1, '2025-10-14 15:54:57', '2025-10-14 15:54:57'),
  (10, 'Apple iPad Pro (M4)', 'Tablets & E-Readers', 19, 'iPad Pro M4 11-inch 256 GB Wi-Fi', 'SKU019', '1', '1099.00', '1099.000000', 1, '2025-10-21 10:29:10', '2025-10-21 10:29:10'),
  (13, 'Amazon Kindle Oasis', 'Tablets & E-Readers', 27, 'Kindle Oasis 32 GB Wi-Fi', 'SKU027', '1', '299.00', '299.000000', 1, '2025-10-21 10:25:08', '2025-10-21 10:25:08'),
  (18, 'Logitech MX Keys Wireless Keyboard', 'Mouse & Keyboards', 35, 'Logitech MX Keys (Graphite)', 'SKU035', '1', '42.50', '42.500000', 1, '2025-10-14 15:54:57', '2025-10-14 15:54:57'),
  (24, 'Nintendo Switch OLED Model', 'Gaming Consoles', 47, 'Nintendo Switch OLED White', 'SKU047', '1', '100.50', '100.500000', 1, '2025-10-13 10:05:21', '2025-10-13 10:05:21'),
  (30, 'Google Nest Hub (2nd Gen)', 'Smart Home Devices', 59, 'Google Nest Hub 2nd Gen Chalk', 'SKU059', '1', '99.00', '99.000000', 1, '2025-10-18 13:18:52', '2025-10-18 13:18:52'),
  (35, 'Laser keyboard projector', 'Toys & Gadgets', 69, 'Laser Keyboard Projector 1.0', 'SKU069', '1', '199.00', '199.000000', 1, '2025-10-21 10:25:08', '2025-10-21 10:25:08');

-- ============================================
-- Data for table: user (10 rows)
-- ============================================

INSERT INTO `user` (`user_id`, `user_name`, `email`, `name`, `password_hash`, `user_type`, `address_id`) VALUES
  (10, 'himak', 'himanndhikuruppu@gmail.com', 'Himandhi K', '$2b$12$zk9EitI7xHFkEp9dZ/kmM.K0uw4E8yN843tFtlkZDU37kTRvZf8VG', 'customer', 18),
  (11, 'hima2', 'himanndhik@gmail.com', 'Himandhi K', '$2b$12$XSWYbOY2s2SaNYWc/LBbtuSyVZ7UXdTSiltXrS9Bae/ZZLIr1mAq6', 'customer', 19),
  (13, 'admin1', 'himandhik.23@cse.mrt.ac.lk', 'Admin 1', '$2b$12$4RnaCpSEVnamV6w2Bsy/f.ZJS.loj.Tv1t7gKrIiOjRYzua/qR4XO', 'admin', 21),
  (17, 'Senilka1', 'senilkat@gmail.com', 'Senilka M T', '$2b$12$eFQdv8vTHilP8I2bAGfgC.10g/pUxE.mu4o8W/FCJx7RtOXctcxLq', 'customer', 25),
  (18, 'johndoe92', 'john.doe@example.com', 'John Doe', '$2b$12$FHTfkGXEeUeL2sj66wQDk.msyZsJhW2NuWuV8sBZYUWCwjgEyEffS', 'customer', 26),
  (19, 'test1', 'test1@gmail.com', 'Test 1', '$2b$12$.HzxpfP1qtX4mD8ATT.m3ukr1gQRziAjDS4zq5EUQXFcl.2Y.YK2S', 'customer', 27),
  (20, 'thira1', 'thirani@gmail.com', 'Thirani Kuruppu', '$2b$12$T684tfqZ.k4lvShbYiQ5G.qinZgKw3h.bafrdQRj/b4PMytcnzS3y', 'customer', 34),
  (21, 'hasini123', 'hasini@gmail.com', 'Hasini Lawanya', '$2b$12$GY87jJfzvSNokK4UHVKYnevilgeJYceUQgJ5c.AyNetpqjM60COE2', 'customer', 35),
  (22, 'hima6', 'fernandoshamila@gmail.com', 'Shamila Fernando', '$2b$12$zk0OqonZydH1Mo3Cm1sR6Og8eU1uXjHrqvTCxYX6xTL0t2I7DP42K', 'customer', 36),
  (23, 'hima7', 'himandhikuruppu@gmail.com', 'Himandhi Kururppu', '$2b$12$bHsgfibZrvjZXfw8Kz.4UOIYZLX/xzsrJB/toselr/BIiHHEbCquW', 'customer', 38);

-- ============================================
-- Data for table: variant (83 rows)
-- ============================================

INSERT INTO `variant` (`variant_id`, `variant_name`, `product_id`, `price`, `quantity`, `SKU`) VALUES
  (1, 'iPhine 17 Pro', 1, '1099.00', 40, 'SKU001'),
  (2, 'iPhone 17 Pro Max', 1, '1199.00', 50, 'SKU002'),
  (3, 'Galaxy S25 Ultra', 2, '1419.99', 42, 'SKU003'),
  (4, 'Galaxy S25', 2, '799.99', 50, 'SKU004'),
  (5, 'Pixel 10', 3, '799.00', 48, 'SKU005'),
  (6, 'Pixel 10 Pro', 3, '999.00', 50, 'SKU006'),
  (7, 'USB-C to Lightning', 4, '59.00', 47, 'SKU007'),
  (8, 'USB-C to USB-C', 4, '75.99', 50, 'SKU008'),
  (9, '10000 mAh ', 5, '85.94', 50, 'SKU009'),
  (10, '20000 mAh', 5, '149.99', 50, 'SKU010'),
  (11, '18W USB-C Fast Charger', 6, '122.29', 50, 'SKU011'),
  (12, '30W USB-C Charger', 6, '139.00', 50, 'SKU012'),
  (13, '128GB', 7, '126.49', 50, 'SKU013'),
  (14, '256GB', 7, '130.99', 50, 'SKU014'),
  (15, 'iPhone 17 Pro Max Silicone ', 8, '116.99', 48, 'SKU015'),
  (16, 'Galaxy S25 Ultra Leather ', 8, '114.29', 50, 'SKU016'),
  (17, 'iPhone 17 Pro Max Tempered Glass', 9, '80.35', 50, 'SKU017'),
  (18, 'Pixel 10 Pro Anti-Glare Glass', 9, '150.00', 50, 'SKU018'),
  (19, 'iPad Pro M4 11-inch 256 GB Wi-Fi', 10, '1099.00', 50, 'SKU019'),
  (20, 'iPad Pro M4 11-inch 512 GB Wi-Fi + Cellular', 10, '1399.00', 40, 'SKU020'),
  (21, 'iPad Pro M4 13-inch 1 TB Wi-Fi + Cellular', 10, '1899.00', 30, 'SKU021'),
  (22, 'Galaxy Tab S9+ Graphite 256 GB', 11, '999.00', 50, 'SKU022'),
  (23, 'Galaxy Tab S9+ Beige 512 GB', 11, '1199.00', 40, 'SKU023'),
  (24, 'Kindle Paperwhite 8 GB Standard', 12, '139.00', 50, 'SKU024'),
  (25, 'Kindle Paperwhite 16 GB Signature Edition', 12, '169.00', 40, 'SKU025'),
  (26, 'Kindle Oasis 8 GB Wi-Fi', 13, '249.00', 50, 'SKU026'),
  (27, 'Kindle Oasis 32 GB Wi-Fi', 13, '299.00', 39, 'SKU027'),
  (28, 'Lenovo Tab P12 Pro 6 GB RAM / 128 GB', 14, '649.00', 50, 'SKU028'),
  (29, 'Lenovo Tab P12 Pro 8 GB RAM / 256 GB', 14, '749.00', 40, 'SKU029'),
  (30, 'MacBook Air M3 13-inch 256 GB', 15, '1199.00', 50, 'SKU030'),
  (31, 'MacBook Air M3 15-inch 512 GB', 15, '1599.00', 40, 'SKU031'),
  (32, 'MacBook Pro M3 Pro 14-inch 512 GB', 16, '1999.00', 40, 'SKU032'),
  (33, 'MacBook Pro M3 Pro 16-inch 1 TB', 16, '2499.00', 30, 'SKU033'),
  (34, 'Dell XPS 13 Plus 16GB RAM / 512GB SSD', 17, '1499.00', 37, 'SKU034'),
  (35, 'Logitech MX Keys (Graphite)', 18, '42.50', 50, 'SKU035'),
  (36, 'Logitech MX Keys (Pale Gray)', 18, '54.50', 50, 'SKU036'),
  (37, 'Razer BlackWidow V4 Pro (Green Switch)', 19, '52.00', 50, 'SKU037'),
  (38, 'Razer BlackWidow V4 Pro (Yellow Switch)', 19, '67.90', 50, 'SKU038'),
  (39, 'Logitech G Pro X Superlight (Black)', 20, '70.50', 50, 'SKU039'),
  (40, 'Logitech G Pro X Superlight (White)', 20, '72.50', 50, 'SKU040'),
  (41, 'Corsair K100 RGB (OPX Switch)', 21, '120.50', 50, 'SKU041'),
  (42, 'Corsair K100 RGB (Cherry MX Speed)', 21, '95.50', 50, 'SKU042'),
  (43, 'PlayStation 5 Standard Edition', 22, '150.00', 50, 'SKU043'),
  (44, 'PlayStation 5 Digital Edition', 22, '140.00', 50, 'SKU044'),
  (45, 'Xbox Series X 1TB Standard', 23, '120.00', 50, 'SKU045'),
  (46, 'Xbox Series X Diablo IV Bundle', 23, '130.50', 50, 'SKU046'),
  (47, 'Nintendo Switch OLED White', 24, '100.50', 50, 'SKU047'),
  (48, 'Nintendo Switch OLED Zelda Edition', 24, '120.00', 50, 'SKU048'),
  (49, 'Steam Deck 256GB SSD', 25, '220.00', 50, 'SKU049'),
  (50, 'Steam Deck 512GB OLED', 25, '190.50', 50, 'SKU050'),
  (51, 'Apple Watch Series 9 GPS', 26, '399.00', 50, 'SKU051'),
  (52, 'Apple Watch Series 9 Cellular', 26, '499.00', 50, 'SKU052'),
  (53, 'Samsung Galaxy Watch 6 Bluetooth', 27, '299.00', 50, 'SKU053'),
  (54, 'Samsung Galaxy Watch 6 LTE', 27, '349.00', 50, 'SKU054'),
  (55, 'Fitbit Versa 4 Standard', 28, '229.00', 50, 'SKU055'),
  (56, 'Fitbit Versa 4 Premium', 28, '249.00', 50, 'SKU056'),
  (57, 'Garmin Forerunner 265 42mm', 29, '449.00', 50, 'SKU057'),
  (58, 'Garmin Forerunner 265 46mm', 29, '479.00', 50, 'SKU058'),
  (59, 'Google Nest Hub 2nd Gen Chalk', 30, '99.00', 49, 'SKU059'),
  (60, 'Google Nest Hub 2nd Gen Charcoal', 30, '99.00', 50, 'SKU060'),
  (61, 'Philips Hue White Ambiance', 31, '79.00', 50, 'SKU061'),
  (62, 'Philips Hue Color Ambiance', 31, '129.00', 50, 'SKU062'),
  (63, 'Ring Video Doorbell Standard', 32, '59.00', 50, 'SKU063'),
  (64, 'Ring Video Doorbell With Chime', 32, '79.00', 50, 'SKU064'),
  (65, 'TP-Link Kasa Single Plug', 33, '19.00', 50, 'SKU065'),
  (66, 'TP-Link Kasa 2-Pack', 33, '29.00', 50, 'SKU066'),
  (67, 'Plasma Ball Sphere 1.0', 34, '259.00', 50, 'SKU067'),
  (68, 'Plasma Ball Sphere 2.0', 34, '159.00', 50, 'SKU068'),
  (69, 'Laser Keyboard Projector 1.0', 35, '199.00', 49, 'SKU069'),
  (70, 'Laser Keyboard Projector 2.0.0', 35, '220.00', 50, 'SKU070'),
  (71, 'RoboPet X1', 36, '350.00', 50, 'SKU071'),
  (72, 'RoboPetX2', 36, '499.00', 50, 'SKU072'),
  (73, 'Fan Clock White', 37, '85.00', 50, 'SKU073'),
  (74, 'Fan Clock Pink', 37, '100.00', 33, 'SKU074'),
  (75, 'JBL Mini Speaker 1.0', 38, '190.00', 50, 'SKU075'),
  (76, 'JBL Mini Speaker 2.0', 38, '150.00', 50, 'SKU076'),
  (77, 'Cobble Speaker 2.0', 39, '140.00', 50, 'SKU077'),
  (78, 'Cobble Speaker 3.0', 39, '249.00', 50, 'SKU078'),
  (79, 'EchoDot 1.0', 40, '199.00', 50, 'SKU079'),
  (80, 'EchoDot 2.0', 40, '149.00', 50, 'SKU080'),
  (81, 'Lenovo ThinkPlus 1.8', 41, '180.00', 50, 'SKU081'),
  (82, 'Lenovo ThinkPlus 1.8', 41, '199.00', 50, 'SKU082'),
  (86, 'testphone1', 46, '34.00', 15, 'sku100');

-- ============================================
-- Data for table: variant_attribute (4 rows)
-- ============================================

INSERT INTO `variant_attribute` (`attribute_id`, `attribute_name`) VALUES
  (1, 'Model'),
  (2, 'Colour'),
  (3, 'Released Year'),
  (4, 'Warranty');

-- ============================================
-- Data for table: variant_attribute_value (264 rows)
-- ============================================

INSERT INTO `variant_attribute_value` (`id`, `variant_id`, `attribute_id`, `value`) VALUES
  (1, 1, 1, '17'),
  (2, 1, 2, 'Black'),
  (3, 1, 3, '2025'),
  (4, 1, 4, '12 months'),
  (5, 2, 1, '17 Pro'),
  (6, 2, 2, 'Silver'),
  (7, 2, 3, '2025'),
  (8, 2, 4, '12 months'),
  (9, 3, 1, 'S25 Ultra'),
  (10, 3, 2, 'Phantom Black'),
  (11, 3, 3, '2025'),
  (12, 3, 4, '12 months'),
  (13, 4, 1, 'S25'),
  (14, 4, 2, 'White'),
  (15, 4, 3, '2025'),
  (16, 4, 4, '12 months'),
  (17, 5, 1, '10'),
  (18, 5, 2, 'Just Black'),
  (19, 5, 3, '2025'),
  (20, 5, 4, '12 months'),
  (21, 6, 1, '10 Pro'),
  (22, 6, 2, 'Cloudy White'),
  (23, 6, 3, '2025'),
  (24, 6, 4, '12 months'),
  (25, 7, 1, NULL),
  (26, 7, 2, 'White'),
  (27, 7, 3, '2025'),
  (28, 7, 4, '6 months'),
  (29, 8, 1, NULL),
  (30, 8, 2, 'Black'),
  (31, 8, 3, '2025'),
  (32, 8, 4, '6 months'),
  (33, 9, 1, NULL),
  (34, 9, 2, 'Black'),
  (35, 9, 3, '2025'),
  (36, 9, 4, '12 months'),
  (37, 10, 1, NULL),
  (38, 10, 2, 'White'),
  (39, 10, 3, '2025'),
  (40, 10, 4, '12 months'),
  (41, 11, 1, NULL),
  (42, 11, 2, 'White'),
  (43, 11, 3, '2025'),
  (44, 11, 4, '6 months'),
  (45, 12, 1, NULL),
  (46, 12, 2, 'Black'),
  (47, 12, 3, '2025'),
  (48, 12, 4, '6 months'),
  (49, 13, 1, NULL),
  (50, 13, 2, 'Red'),
  (51, 13, 3, '2025'),
  (52, 13, 4, '12 months'),
  (53, 14, 1, NULL),
  (54, 14, 2, 'Blue'),
  (55, 14, 3, '2025'),
  (56, 14, 4, '12 months'),
  (57, 15, 1, NULL),
  (58, 15, 2, 'Black'),
  (59, 15, 3, '2025'),
  (60, 15, 4, '6 months'),
  (61, 16, 1, NULL),
  (62, 16, 2, 'Brown'),
  (63, 16, 3, '2025'),
  (64, 16, 4, '6 months'),
  (65, 17, 1, NULL),
  (66, 17, 2, 'Transparent'),
  (67, 17, 3, '2025'),
  (68, 17, 4, '6 months'),
  (69, 18, 1, NULL),
  (70, 18, 2, 'Transparent'),
  (71, 18, 3, '2025'),
  (72, 18, 4, '6 months'),
  (73, 19, 1, 'iPad Pro M4'),
  (74, 19, 2, 'Silver'),
  (75, 19, 3, '2025'),
  (76, 19, 4, '12 months'),
  (77, 20, 1, 'iPad Pro M4'),
  (78, 20, 2, 'Space Gray'),
  (79, 20, 3, '2025'),
  (80, 20, 4, '12 months'),
  (81, 21, 1, 'iPad Pro M4'),
  (82, 21, 2, 'Silver'),
  (83, 21, 3, '2025'),
  (84, 21, 4, '12 months'),
  (85, 22, 1, 'Galaxy Tab S9+'),
  (86, 22, 2, 'Graphite'),
  (87, 22, 3, '2024'),
  (88, 22, 4, '12 months'),
  (89, 23, 1, 'Galaxy Tab S9+'),
  (90, 23, 2, 'Beige'),
  (91, 23, 3, '2024'),
  (92, 23, 4, '12 months'),
  (93, 24, 1, 'Kindle Paperwhite'),
  (94, 24, 2, 'Black'),
  (95, 24, 3, '2023'),
  (96, 24, 4, '12 months'),
  (97, 25, 1, 'Kindle Paperwhite Signature Edition'),
  (98, 25, 2, 'Black'),
  (99, 25, 3, '2024'),
  (100, 25, 4, '12 months');

INSERT INTO `variant_attribute_value` (`id`, `variant_id`, `attribute_id`, `value`) VALUES
  (101, 26, 1, 'Kindle Oasis'),
  (102, 26, 2, 'Graphite'),
  (103, 26, 3, '2022'),
  (104, 26, 4, '12 months'),
  (105, 27, 1, 'Kindle Oasis'),
  (106, 27, 2, 'Graphite'),
  (107, 27, 3, '2022'),
  (108, 27, 4, '12 months'),
  (109, 28, 1, 'Lenovo Tab P12 Pro'),
  (110, 28, 2, 'Storm Grey'),
  (111, 28, 3, '2023'),
  (112, 28, 4, '12 months'),
  (113, 29, 1, 'Lenovo Tab P12 Pro'),
  (114, 29, 2, 'Aurora Black'),
  (115, 29, 3, '2023'),
  (116, 29, 4, '12 months'),
  (117, 30, 1, 'MacBook Air M3'),
  (118, 30, 2, 'Silver'),
  (119, 30, 3, '2024'),
  (120, 30, 4, '12 months'),
  (121, 31, 1, 'MacBook Air M3'),
  (122, 31, 2, 'Space Gray'),
  (123, 31, 3, '2024'),
  (124, 31, 4, '12 months'),
  (125, 32, 1, 'MacBook Air M3'),
  (126, 32, 2, 'Silver'),
  (127, 32, 3, '2024'),
  (128, 32, 4, '12 months'),
  (129, 33, 1, 'MacBook Pro M3 Pro'),
  (130, 33, 2, 'Space Gray'),
  (131, 33, 3, '2024'),
  (132, 33, 4, '12 months'),
  (133, 34, 1, 'MacBook Pro M3 Pro'),
  (134, 34, 2, 'Silver'),
  (135, 34, 3, '2024'),
  (136, 34, 4, '12 months'),
  (137, 35, 1, 'Advanced Wireless (PC layout)'),
  (138, 35, 2, 'Graphite'),
  (139, 35, 3, '2019'),
  (140, 35, 4, '6 months'),
  (141, 36, 1, 'Advanced Wireless (Mac layout)'),
  (142, 36, 2, 'Pale Gray'),
  (143, 36, 3, '2019'),
  (144, 36, 4, '6 months'),
  (145, 37, 1, 'Green Clicky Switches'),
  (146, 37, 2, 'Black'),
  (147, 37, 3, '2023'),
  (148, 37, 4, '6 months'),
  (149, 38, 1, 'Yellow Linear Switches'),
  (150, 38, 2, 'Black'),
  (151, 38, 3, '2023'),
  (152, 38, 4, '6 months'),
  (153, 39, 1, 'Superlight Wireless'),
  (154, 39, 2, 'Black'),
  (155, 39, 3, '2020'),
  (156, 39, 4, '4 months'),
  (157, 40, 1, 'Superlight Wireless'),
  (158, 40, 2, 'White'),
  (159, 40, 3, '2020'),
  (160, 40, 4, '4 months'),
  (161, 41, 1, 'OPX Optical Switches'),
  (162, 41, 2, 'Black'),
  (163, 41, 3, '2020'),
  (164, 41, 4, '4 months'),
  (165, 42, 1, 'Cherry MX Speed Switches'),
  (166, 42, 2, 'Black'),
  (167, 42, 3, '2020'),
  (168, 42, 4, '4 months'),
  (169, 43, 1, 'Standard Edition (Disc Drive)'),
  (170, 43, 2, 'White'),
  (171, 43, 3, '2020'),
  (172, 43, 4, '6 months'),
  (173, 44, 1, 'Digital Edition'),
  (174, 44, 2, 'Black'),
  (175, 44, 3, '2020'),
  (176, 44, 4, '6 months'),
  (177, 45, 1, '1TB Standard'),
  (178, 45, 2, 'Black'),
  (179, 45, 3, '2020'),
  (180, 45, 4, '6 months'),
  (181, 46, 1, 'Diablo IV Bundle'),
  (182, 46, 2, 'Black'),
  (183, 46, 3, '2020'),
  (184, 46, 4, '6 months'),
  (185, 47, 1, 'OLED Model'),
  (186, 47, 2, 'White'),
  (187, 47, 3, '2021'),
  (188, 47, 4, '6 months'),
  (189, 48, 1, 'OLED Zelda Edition'),
  (190, 48, 2, 'Custom Zelda Design'),
  (191, 48, 3, '2021'),
  (192, 48, 4, '4 months'),
  (193, 49, 1, '256GB SSD'),
  (194, 49, 2, 'Black'),
  (195, 49, 3, '2022'),
  (196, 49, 4, '6 months'),
  (197, 50, 1, '512GB OLED'),
  (198, 50, 2, 'Black'),
  (199, 50, 3, '2023'),
  (200, 50, 4, '6 months');

INSERT INTO `variant_attribute_value` (`id`, `variant_id`, `attribute_id`, `value`) VALUES
  (265, 67, 1, 'X1'),
  (266, 67, 2, 'Blue'),
  (267, 67, 3, '2024'),
  (268, 67, 4, '12 months'),
  (269, 68, 1, 'X2'),
  (270, 68, 2, 'Black'),
  (271, 68, 3, '2025'),
  (272, 68, 4, '12 months'),
  (273, 69, 1, '1.0'),
  (274, 69, 2, 'White'),
  (275, 69, 3, '2023'),
  (276, 69, 4, '9 months'),
  (277, 70, 1, '2.0'),
  (278, 70, 2, 'Red'),
  (279, 70, 3, '2024'),
  (280, 70, 4, '12 months'),
  (281, 71, 1, '1.0'),
  (282, 71, 2, 'White'),
  (283, 71, 3, '2022'),
  (284, 71, 4, '12 months'),
  (285, 72, 1, '2.0'),
  (286, 72, 2, 'Red'),
  (287, 72, 3, '2025'),
  (288, 72, 4, '12 months'),
  (289, 73, 1, '2.0'),
  (290, 73, 2, 'White'),
  (291, 73, 3, '2024'),
  (292, 73, 4, '8 months'),
  (293, 74, 1, '2.0'),
  (294, 74, 2, 'Blue'),
  (295, 74, 3, '2024'),
  (296, 74, 4, '8 months'),
  (297, 75, 1, '1.0'),
  (298, 75, 2, 'Black'),
  (299, 75, 3, '2023'),
  (300, 75, 4, '12 months'),
  (301, 76, 1, '2.0'),
  (302, 76, 2, 'Purple'),
  (303, 76, 3, '2025'),
  (304, 76, 4, '15 months'),
  (305, 77, 1, '2.0'),
  (306, 77, 2, 'Red'),
  (307, 77, 3, '2022'),
  (308, 77, 4, '12 months'),
  (309, 78, 1, '3.0'),
  (310, 78, 2, 'Black'),
  (311, 78, 3, '2024'),
  (312, 78, 4, '12 months'),
  (313, 79, 1, '1.0'),
  (314, 79, 2, 'White'),
  (315, 79, 3, '2023'),
  (316, 79, 4, '9 months'),
  (317, 80, 1, '2.0'),
  (318, 80, 2, 'Black'),
  (319, 80, 3, '2024'),
  (320, 80, 4, '12 months'),
  (321, 81, 1, '1.8'),
  (322, 81, 2, 'Blue'),
  (323, 81, 3, '2023'),
  (324, 81, 4, '12 months'),
  (325, 82, 1, '2.0'),
  (326, 82, 2, 'Black'),
  (327, 82, 3, '2025'),
  (328, 82, 4, '15 months');

SET FOREIGN_KEY_CHECKS=1;


