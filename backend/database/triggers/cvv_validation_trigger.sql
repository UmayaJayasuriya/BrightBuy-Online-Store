-- Trigger to validate CVV length and digits for Card table
DELIMITER $$

CREATE TRIGGER check_cvv_length
BEFORE INSERT ON card
FOR EACH ROW
BEGIN
    -- Ensure CVV is 3 characters AND only contains digits
    IF LENGTH(NEW.CVV) != 3 OR NEW.CVV REGEXP '[^0-9]' THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'CVV must be exactly 3 digits';
    END IF;
END$$

DELIMITER ;
