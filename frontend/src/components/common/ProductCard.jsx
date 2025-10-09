/**
 * ProductCard Component
 * Reusable product card for displaying product information
 */
import React from 'react';
import { Link } from 'react-router-dom';
import { useCart } from '../../context/CartContext';
import './ProductCard.css';

const ProductCard = ({ product }) => {
  const { addToCart, addToWishlist } = useCart();

  const handleAddToCart = (e) => {
    e.preventDefault();
    addToCart(product);
  };

  const handleAddToWishlist = (e) => {
    e.preventDefault();
    addToWishlist(product);
  };

  return (
    <div className="product-card">
      <div className="product-item border h-100">
        <div className="position-relative">
          <img
            src={product.image || '/img/product-1.png'}
            className="img-fluid w-100"
            alt={product.name}
          />
          {product.discount && (
            <div className="product-badge">
              <span className="badge bg-danger">{product.discount}% OFF</span>
            </div>
          )}
          <div className="product-overlay">
            <Link
              to={`/single/${product.id}`}
              className="btn btn-sm btn-primary rounded-circle"
            >
              <i className="fa fa-eye"></i>
            </Link>
          </div>
        </div>

        <div className="product-content p-4">
          <Link to={`/shop?category=${product.category}`} className="d-block mb-2 text-muted">
            {product.category}
          </Link>
          <Link to={`/single/${product.id}`} className="h5 d-block mb-3">
            {product.name}
          </Link>

          <div className="d-flex align-items-center mb-3">
            <div className="text-warning me-2">
              {'★'.repeat(Math.floor(product.rating || 5))}
              {'☆'.repeat(5 - Math.floor(product.rating || 5))}
            </div>
            <small className="text-muted">({product.reviews || 0} reviews)</small>
          </div>

          <div className="d-flex justify-content-between align-items-center mb-3">
            <div>
              {product.oldPrice && (
                <del className="me-2 text-muted">${product.oldPrice.toFixed(2)}</del>
              )}
              <span className="text-primary fw-bold fs-5">
                ${product.price.toFixed(2)}
              </span>
            </div>
          </div>

          <div className="d-flex gap-2">
            <button
              onClick={handleAddToCart}
              className="btn btn-primary rounded-pill flex-grow-1"
            >
              <i className="fas fa-shopping-cart me-2"></i>
              Add to Cart
            </button>
            <button
              onClick={handleAddToWishlist}
              className="btn btn-outline-primary rounded-circle"
              title="Add to Wishlist"
            >
              <i className="fas fa-heart"></i>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProductCard;
