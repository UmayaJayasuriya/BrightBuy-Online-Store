-- Trigger to prevent negative quantity on variant table
DELIMITER $$

CREATE TRIGGER check_variant_quantity
BEFORE UPDATE ON variant
FOR EACH ROW
BEGIN
    IF NEW.quantity < 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Quantity cannot be negative';
    END IF;
END$$

DELIMITER ;
