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

