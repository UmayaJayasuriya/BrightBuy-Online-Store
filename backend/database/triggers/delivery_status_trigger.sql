-- Trigger to set default delivery_status to 'Pending' on INSERT
DELIMITER $$

CREATE TRIGGER set_default_delivery_status
BEFORE INSERT ON Delivery
FOR EACH ROW
BEGIN
    IF NEW.delivery_status IS NULL THEN
        SET NEW.delivery_status = 'Pending';
    END IF;
END$$

DELIMITER ;
