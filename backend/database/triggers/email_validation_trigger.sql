"""
SQL Trigger: Email Validation
This trigger validates email addresses before inserting into the User table
"""

-- Trigger to validate email format before user insertion
DELIMITER $$

CREATE TRIGGER trg_check_email_before_insert
BEFORE INSERT ON User
FOR EACH ROW
BEGIN
    -- Check if email contains '@'
    IF NEW.email NOT LIKE '%@%' THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Please enter a valid email address. It must include the "@" symbol (e.g., name@example.com).';
    END IF;
END$$

DELIMITER ;
