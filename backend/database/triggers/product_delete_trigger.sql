DELIMITER $$

CREATE TRIGGER prevent_product_delete_if_in_order
BEFORE DELETE ON product
FOR EACH ROW
BEGIN
    /* Prevent deleting a product if any order_item references one of its variants */
    IF EXISTS (
        SELECT 1
        FROM variant v
        JOIN order_item oi ON oi.variant_id = v.variant_id
        WHERE v.product_id = OLD.product_id
    ) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Cannot delete product: it is referenced in an order.';
    END IF;
END$$

DELIMITER ;
