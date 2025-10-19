-- Create favorite_product table
-- Run this SQL in your MySQL database

CREATE TABLE IF NOT EXISTS favorite_product (
    favorite_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    product_id INT NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    -- Foreign keys
    FOREIGN KEY (user_id) REFERENCES user(user_id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES product(product_id) ON DELETE CASCADE,
    
    -- Ensure a user can't favorite the same product twice
    UNIQUE KEY unique_user_product (user_id, product_id),
    
    -- Index for faster queries
    INDEX idx_user_id (user_id),
    INDEX idx_product_id (product_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Optional: Add some sample data
-- INSERT INTO favorite_product (user_id, product_id) VALUES (10, 1);
-- INSERT INTO favorite_product (user_id, product_id) VALUES (10, 5);
