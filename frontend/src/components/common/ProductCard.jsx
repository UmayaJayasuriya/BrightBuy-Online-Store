/**
 * ProductCard Component
 * Reusable product card for displaying product information
 */
import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useCart } from '../../context/CartContext';
import { useAuth } from '../../context/AuthContext';
import axios from 'axios';
import './ProductCard.css';

const ProductCard = ({ product }) => {
  const { addToWishlist } = useCart();
  const { isAdmin, isAuthenticated, user, openLoginModal } = useAuth();
  const navigate = useNavigate();
  const [isFavorite, setIsFavorite] = useState(false);
  const [favLoading, setFavLoading] = useState(false);

  // Check if product is in favorites on mount
  useEffect(() => {
    const checkFavoriteStatus = async () => {
      if (isAuthenticated && user) {
        try {
          const response = await axios.get(
            `http://127.0.0.1:8020/favorites/check/${user.user_id}/${product.product_id}`
          );
          setIsFavorite(response.data.is_favorite);
        } catch (error) {
          console.error('Error checking favorite status:', error);
        }
      }
    };

    checkFavoriteStatus();
  }, [isAuthenticated, user, product.product_id]);

  const handleViewProduct = (e) => {
    e.preventDefault();
    navigate(`/single/${product.product_id}`);
  };

  const handleAddToFavorite = async (e) => {
    e.preventDefault();
    
    // Check if user is logged in
    if (!isAuthenticated) {
      // Directly open login modal
      openLoginModal();
      return;
    }

    setFavLoading(true);
    try {
      if (isFavorite) {
        // Remove from favorites
        await axios.delete(`http://127.0.0.1:8020/favorites/${user.user_id}/${product.product_id}`);
        setIsFavorite(false);
        // small inline feedback instead of blocking alert
        console.info('Removed from favorites');
      } else {
        // Add to favorites
        await axios.post(`http://127.0.0.1:8020/favorites/${user.user_id}`, {
          product_id: product.product_id
        });
        setIsFavorite(true);
        console.info('Added to favorites');
      }

      // Also update local wishlist for backward compatibility
      addToWishlist(product);
    } catch (error) {
      // Prefer server-provided error message when available
      const serverMessage = error?.response?.data?.detail || error?.response?.data?.message;
      console.error('Error updating favorites:', error, serverMessage || 'no server message');
      // show short alert to user
      alert(serverMessage ? `Failed to update favorites: ${serverMessage}` : 'Failed to update favorites. Please try again.');
    } finally {
      setFavLoading(false);
    }
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
              onClick={handleAddToFavorite}
              className={`btn ${isFavorite ? 'btn-danger' : 'btn-outline-primary'} rounded-circle`}
              title={isFavorite ? 'Remove from Favorites' : 'Add to Favorites'}
              disabled={favLoading}
            >
              <i className={`fa${isFavorite ? 's' : 'r'} fa-heart`}></i>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProductCard;
