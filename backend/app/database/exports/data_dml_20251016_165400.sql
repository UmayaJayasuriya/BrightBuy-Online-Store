-- ============================================
-- Brightbuy Data (DML) Export
-- Generated: 2025-10-16 16:54:00
-- ============================================

USE `brightbuy`;

SET FOREIGN_KEY_CHECKS=0;

-- ============================================
-- Data for table: address (7 rows)
-- ============================================

INSERT INTO `address` (`address_id`, `city_id`, `house_number`, `street`, `city`, `state`) VALUES
  (18, 1, 26, 'Main street', 'Dallas', 'Texas'),
  (19, 5, 6, 'Hill street', 'Austin', 'Texas'),
  (21, 2, 22, 'Green street', 'Austin', 'Texas'),
  (25, 2, 22, 'Bean Street', 'Houston', 'Texas'),
  (26, 5, 42, 'Maple Avenue', 'Austin', 'Illinois'),
  (27, 5, 44, 'jj', 'Austin', 'Texas'),
  (29, 2, 11, 'colombo street', 'Houston', 'Texas');

-- ============================================
-- Data for table: card (2 rows)
-- ============================================

INSERT INTO `card` (`card_id`, `order_id`, `card_number`, `card_name`, `expiry_date`, `CVV`) VALUES
  (1, 5, '3846 0634 0875 6340', 'Hima', '12/26', '333'),
  (2, 7, '7890 6976 3562 7768', 'Hima', '05/27', '666');

-- ============================================
-- Data for table: cart (2 rows)
-- ============================================

INSERT INTO `cart` (`cart_id`, `user_id`, `created_date`, `total_amount`) VALUES
  (1, 10, '2025-10-11 10:39:11', '0.00'),
  (2, 11, '2025-10-11 13:03:09', '0.00');

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
-- Data for table: contact (2 rows)
-- ============================================

INSERT INTO `contact` (`contact_id`, `customer_name`, `email`, `subject_name`, `message`) VALUES
  (1, 'John Doe', 'a@b.com', 'Test', 'This is a test message'),
  (2, 'Hima', 'himak@gmail.com', 'is', 'hmfj');

-- ============================================
-- Data for table: delivery (6 rows)
-- ============================================

INSERT INTO `delivery` (`delivery_id`, `order_id`, `delivery_method`, `address_id`, `estimated_delivery_date`, `delivery_status`) VALUES
  (1, 2, 'home_delivery', 29, '2025-10-18', 'pending'),
  (2, 3, 'store_pickup', NULL, '2025-10-15', 'pending'),
  (3, 4, 'store_pickup', NULL, '2025-10-15', 'pending'),
  (4, 5, 'store_pickup', NULL, '2025-10-16', 'pending'),
  (5, 6, 'store_pickup', NULL, '2025-10-16', 'pending'),
  (6, 7, 'store_pickup', NULL, '2025-10-18', 'pending');

-- ============================================
-- Data for table: location (10 rows)
-- ============================================

INSERT INTO `location` (`city_id`, `city`, `zip_code`, `Is_main_city`) VALUES
  (1, 'Dallas', 120, 1),
  (2, 'Houston', 121, 1),
  (3, 'San Antonio', 122, 1),
  (4, 'Fort Worth', 123, 1),
  (5, 'Austin', 124, 1),
  (6, 'New Orleans', 124, 0),
  (7, 'Jackson', 124, 0),
  (8, 'Memphis', 124, 0),
  (9, 'Tulsa', 124, 0),
  (10, 'Norman', 124, 0);

-- ============================================
-- Data for table: order_item (13 rows)
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
  (13, 7, 7, 2, '59.00');

-- ============================================
-- Data for table: orders (6 rows)
-- ============================================

INSERT INTO `orders` (`order_id`, `cart_id`, `user_id`, `order_date`, `total_amount`) VALUES
  (2, 2, 11, '2025-10-13 10:05:21', '5397.48'),
  (3, 2, 11, '2025-10-13 10:19:54', '1099.00'),
  (4, 2, 11, '2025-10-13 10:34:12', '486.96'),
  (5, 1, 10, '2025-10-14 15:54:57', '183.50'),
  (6, 1, 10, '2025-10-14 16:31:32', '2198.00'),
  (7, 1, 10, '2025-10-16 10:19:21', '7674.97');

-- ============================================
-- Data for table: payment (6 rows)
-- ============================================

INSERT INTO `payment` (`payment_id`, `order_id`, `payment_method`, `payment_status`, `payment_date`) VALUES
  (1, 2, 'card', 'completed', '2025-10-13 10:05:21'),
  (2, 3, 'cod', 'pending', '2025-10-13 10:19:54'),
  (3, 4, 'card', 'completed', '2025-10-13 10:34:12'),
  (4, 5, 'card', 'completed', '2025-10-14 15:54:57'),
  (5, 6, 'cod', 'pending', '2025-10-14 16:31:32'),
  (6, 7, 'card', 'completed', '2025-10-16 10:19:21');

-- ============================================
-- Data for table: product (41 rows)
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
  (41, 'Lenovo ThinkPlus K3 speaker', 13, 'Portable Bluetooth speaker with 360° sound.');

-- ============================================
-- Data for table: user (6 rows)
-- ============================================

INSERT INTO `user` (`user_id`, `user_name`, `email`, `name`, `password_hash`, `user_type`, `address_id`) VALUES
  (10, 'himak', 'himanndhikuruppu@gmail.com', 'Himandhi K', '$2b$12$zk9EitI7xHFkEp9dZ/kmM.K0uw4E8yN843tFtlkZDU37kTRvZf8VG', 'customer', 18),
  (11, 'hima2', 'himanndhik@gmail.com', 'Himandhi K', '$2b$12$XSWYbOY2s2SaNYWc/LBbtuSyVZ7UXdTSiltXrS9Bae/ZZLIr1mAq6', 'customer', 19),
  (13, 'admin1', 'himandhik.23@cse.mrt.ac.lk', 'Admin 1', '$2b$12$4RnaCpSEVnamV6w2Bsy/f.ZJS.loj.Tv1t7gKrIiOjRYzua/qR4XO', 'admin', 21),
  (17, 'Senilka1', 'senilkat@gmail.com', 'Senilka M T', '$2b$12$eFQdv8vTHilP8I2bAGfgC.10g/pUxE.mu4o8W/FCJx7RtOXctcxLq', 'customer', 25),
  (18, 'johndoe92', 'john.doe@example.com', 'John Doe', '$2b$12$FHTfkGXEeUeL2sj66wQDk.msyZsJhW2NuWuV8sBZYUWCwjgEyEffS', 'customer', 26),
  (19, 'test1', 'test1@gmail.com', 'Test 1', '$2b$12$.HzxpfP1qtX4mD8ATT.m3ukr1gQRziAjDS4zq5EUQXFcl.2Y.YK2S', 'customer', 27);

-- ============================================
-- Data for table: variant (82 rows)
-- ============================================

INSERT INTO `variant` (`variant_id`, `variant_name`, `product_id`, `price`, `quantity`, `SKU`) VALUES
  (1, 'iPhine 17 Pro', 1, '1099.00', 45, 'SKU001'),
  (2, 'iPhone 17 Pro Max', 1, '1199.00', 50, 'SKU002'),
  (3, 'Galaxy S25 Ultra', 2, '1419.99', 47, 'SKU003'),
  (4, 'Galaxy S25', 2, '799.99', 50, 'SKU004'),
  (5, 'Pixel 10', 3, '799.00', 50, 'SKU005'),
  (6, 'Pixel 10 Pro', 3, '999.00', 50, 'SKU006'),
  (7, 'USB-C to Lightning', 4, '59.00', 48, 'SKU007'),
  (8, 'USB-C to USB-C', 4, '75.99', 50, 'SKU008'),
  (9, '10000 mAh ', 5, '85.94', 50, 'SKU009'),
  (10, '20000 mAh', 5, '149.99', 50, 'SKU010'),
  (11, '18W USB-C Fast Charger', 6, '122.29', 50, 'SKU011'),
  (12, '30W USB-C Charger', 6, '139.00', 50, 'SKU012'),
  (13, '128GB', 7, '126.49', 50, 'SKU013'),
  (14, '256GB', 7, '130.99', 50, 'SKU014'),
  (15, 'iPhone 17 Pro Max Silicone ', 8, '116.99', 50, 'SKU015'),
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
  (27, 'Kindle Oasis 32 GB Wi-Fi', 13, '299.00', 40, 'SKU027'),
  (28, 'Lenovo Tab P12 Pro 6 GB RAM / 128 GB', 14, '649.00', 50, 'SKU028'),
  (29, 'Lenovo Tab P12 Pro 8 GB RAM / 256 GB', 14, '749.00', 40, 'SKU029'),
  (30, 'MacBook Air M3 13-inch 256 GB', 15, '1199.00', 50, 'SKU030'),
  (31, 'MacBook Air M3 15-inch 512 GB', 15, '1599.00', 40, 'SKU031'),
  (32, 'MacBook Pro M3 Pro 14-inch 512 GB', 16, '1999.00', 40, 'SKU032'),
  (33, 'MacBook Pro M3 Pro 16-inch 1 TB', 16, '2499.00', 30, 'SKU033'),
  (34, 'Dell XPS 13 Plus 16GB RAM / 512GB SSD', 17, '1499.00', 40, 'SKU034'),
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
  (59, 'Google Nest Hub 2nd Gen Chalk', 30, '99.00', 50, 'SKU059'),
  (60, 'Google Nest Hub 2nd Gen Charcoal', 30, '99.00', 50, 'SKU060'),
  (61, 'Philips Hue White Ambiance', 31, '79.00', 50, 'SKU061'),
  (62, 'Philips Hue Color Ambiance', 31, '129.00', 50, 'SKU062'),
  (63, 'Ring Video Doorbell Standard', 32, '59.00', 50, 'SKU063'),
  (64, 'Ring Video Doorbell With Chime', 32, '79.00', 50, 'SKU064'),
  (65, 'TP-Link Kasa Single Plug', 33, '19.00', 50, 'SKU065'),
  (66, 'TP-Link Kasa 2-Pack', 33, '29.00', 50, 'SKU066'),
  (67, 'Plasma Ball Sphere 1.0', 34, '259.00', 50, 'SKU067'),
  (68, 'Plasma Ball Sphere 2.0', 34, '159.00', 50, 'SKU068'),
  (69, 'Laser Keyboard Projector 1.0', 35, '199.00', 50, 'SKU069'),
  (70, 'Laser Keyboard Projector 2.0.0', 35, '220.00', 50, 'SKU070'),
  (71, 'RoboPet X1', 36, '350.00', 50, 'SKU071'),
  (72, 'RoboPetX2', 36, '499.00', 50, 'SKU072'),
  (73, 'Fan Clock White', 37, '85.00', 50, 'SKU073'),
  (74, 'Fan Clock Pink', 37, '100.00', 50, 'SKU074'),
  (75, 'JBL Mini Speaker 1.0', 38, '190.00', 50, 'SKU075'),
  (76, 'JBL Mini Speaker 2.0', 38, '150.00', 50, 'SKU076'),
  (77, 'Cobble Speaker 2.0', 39, '140.00', 50, 'SKU077'),
  (78, 'Cobble Speaker 3.0', 39, '249.00', 50, 'SKU078'),
  (79, 'EchoDot 1.0', 40, '199.00', 50, 'SKU079'),
  (80, 'EchoDot 2.0', 40, '149.00', 50, 'SKU080'),
  (81, 'Lenovo ThinkPlus 1.8', 41, '180.00', 50, 'SKU081'),
  (82, 'Lenovo ThinkPlus 1.8', 41, '199.00', 50, 'SKU082');

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
