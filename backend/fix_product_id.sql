-- Fix product_id AUTO_INCREMENT issue
-- This will modify the product table to automatically generate product_id values

ALTER TABLE product 
MODIFY COLUMN product_id INT NOT NULL AUTO_INCREMENT;
