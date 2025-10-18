DELIMITER $$

CREATE TRIGGER prevent_product_delete_if_in_order
BEFORE DELETE ON Product
FOR EACH ROW
BEGIN
    IF EXISTS (
        SELECT 1
        FROM Variant v
        JOIN Cart_Item ci ON v.variant_id = ci.variant_id
        JOIN Cart c ON ci.cart_id = c.cart_id
        JOIN Orders o ON c.cart_id = o.cart_id
        WHERE v.product_id = OLD.product_id
    ) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Cannot delete product: it is referenced in an order.';
    END IF;
END$$

DELIMITER ;
