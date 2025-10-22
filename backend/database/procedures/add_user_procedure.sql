-- User Registration Stored Procedure
DELIMITER $$

CREATE PROCEDURE AddUserWithAddress(
    IN p_username VARCHAR(50),
    IN p_email VARCHAR(100),
    IN p_password_hash VARCHAR(255),
    IN p_street VARCHAR(255),
    IN p_city VARCHAR(100),
    IN p_state VARCHAR(100),
    IN p_postal_code VARCHAR(20),
    IN p_country VARCHAR(100)
)
BEGIN
    DECLARE v_user_id INT;
    DECLARE v_address_id INT;
    
    -- Start transaction
    START TRANSACTION;
    
    -- Insert into user table
    INSERT INTO user (username, email, password_hash, created_at)
    VALUES (p_username, p_email, p_password_hash, NOW());
    
    -- Get the new user_id
    SET v_user_id = LAST_INSERT_ID();
    
    -- Insert into address table
    INSERT INTO address (street, city, state, postal_code, country)
    VALUES (p_street, p_city, p_state, p_postal_code, p_country);
    
    -- Get the new address_id
    SET v_address_id = LAST_INSERT_ID();
    
    -- Link user and address in user_address table
    INSERT INTO user_address (user_id, address_id, is_default)
    VALUES (v_user_id, v_address_id, TRUE);
    
    -- Commit transaction
    COMMIT;
    
    -- Return the new user_id
    SELECT v_user_id AS user_id;
    
END$$

DELIMITER ;