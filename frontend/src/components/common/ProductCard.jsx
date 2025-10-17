/**
 * ProductCard Component
 * Reusable product card for displaying product information
 */
import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useCart } from '../../context/CartContext';
import { useAuth } from '../../context/AuthContext';
import './ProductCard.css';

const ProductCard = ({ product }) => {
  const { addToWishlist } = useCart();
  const { isAdmin } = useAuth();
  const navigate = useNavigate();

  const handleViewProduct = (e) => {
    e.preventDefault();
    navigate(`/single/${product.product_id}`);
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
            src={`/img/products/${product.product_id}.png`}
            className="img-fluid w-100"
            alt={product.product_name}
            style={{ height: '250px', objectFit: 'cover', backgroundColor: '#f8f9fa' }}
            onError={(e) => {
              // Fallback to .jpg if .png doesn't exist
              if (e.target.src.endsWith('.png')) {
                e.target.src = `/img/products/${product.product_id}.jpg`;
              } else if (e.target.src.endsWith('.jpg')) {
                // Fallback to placeholder if neither exists
                e.target.src = '/img/product-1.png';
              }
            }}
          />
          <div className="product-overlay">
            <Link
              to={`/single/${product.product_id}`}
              className="btn btn-sm btn-primary rounded-circle"
            >
              <i className="fa fa-eye"></i>
            </Link>
          </div>
        </div>

        <div className="product-content p-4">
          {product.category && (
            <Link to={`/shop?category=${encodeURIComponent(product.category.category_name)}`} className="d-block mb-2 text-muted small">
              {product.category.category_name}
            </Link>
          )}
          <Link to={`/single/${product.product_id}`} className="h6 d-block mb-3 text-dark">
            {product.product_name}
          </Link>

          {product.description && (
            <p className="text-muted small mb-3" style={{ 
              overflow: 'hidden', 
              textOverflow: 'ellipsis', 
              display: '-webkit-box', 
              WebkitLineClamp: 2, 
              WebkitBoxOrient: 'vertical',
              minHeight: '40px'
            }}>
              {product.description}
            </p>
          )}

          <div className="d-flex gap-2 mt-3">
            <button
              onClick={handleViewProduct}
              className="btn btn-primary rounded-pill flex-grow-1"
            >
              <i className={`fas ${isAdmin ? 'fa-edit' : 'fa-eye'} me-2`}></i>
              {isAdmin ? 'Edit Product' : 'View Product'}
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
