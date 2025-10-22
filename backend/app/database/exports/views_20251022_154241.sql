-- ============================================
-- BrightBuy Views Export
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

