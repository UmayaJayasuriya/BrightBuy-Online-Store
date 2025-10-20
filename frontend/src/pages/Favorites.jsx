/**
 * Favorites Page Component
 * Display user's favorite products
 */
import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import axios from 'axios';
import { useAuth } from '../context/AuthContext';
import Spinner from '../components/common/Spinner';
import './Favorites.css';

const Favorites = () => {
  const { isAuthenticated, user, openLoginModal } = useAuth();
  const navigate = useNavigate();
  const [favorites, setFavorites] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    if (!isAuthenticated) {
      // Open login modal and redirect to home page
      openLoginModal();
      navigate('/');
      return;
    }

    fetchFavorites();
  }, [isAuthenticated, user, openLoginModal, navigate]);

  const fetchFavorites = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`http://127.0.0.1:8020/favorites/${user.user_id}`);
      setFavorites(response.data);
    } catch (err) {
      console.error('Error fetching favorites:', err);
      setError('Failed to load favorites');
    } finally {
      setLoading(false);
    }
  };

  const handleRemoveFavorite = async (productId) => {
    try {
      await axios.delete(`http://127.0.0.1:8020/favorites/${user.user_id}/${productId}`);
      setFavorites(favorites.filter(fav => fav.product_id !== productId));
      alert('Removed from favorites!');
    } catch (err) {
      console.error('Error removing favorite:', err);
      alert('Failed to remove from favorites');
    }
  };

  if (loading) return <Spinner />;

  return (
    <div className="container-fluid py-5">
      <div className="container py-5">
        {/* Page Header */}
        <div className="row mb-4">
          <div className="col-12">
            <h1 className="display-5 mb-0 fw-bolder">My Favorite Products</h1>
            <nav aria-label="breadcrumb">
              <ol className="breadcrumb">
                <li className="breadcrumb-item"><Link to="/">Home</Link></li>
                <li className="breadcrumb-item active">Favorites</li>
              </ol>
            </nav>
          </div>
        </div>

        {/* Error Message */}
        {error && (
          <div className="alert alert-danger" role="alert">
            <i className="fas fa-exclamation-circle me-2"></i>
            {error}
          </div>
        )}

        {/* Favorites Content */}
        {favorites.length === 0 ? (
          <div className="text-center py-5">
            <i className="fas fa-heart fa-5x text-muted mb-4"></i>
            <h3 className="mb-3">No Favorites Yet</h3>
            <p className="text-muted mb-4">
              Start adding products to your favorites by clicking the heart icon on products you love!
            </p>
            <Link to="/shop" className="btn btn-primary btn-lg rounded-pill px-5">
              <i className="fas fa-shopping-bag me-2"></i>
              Browse Products
            </Link>
          </div>
        ) : (
          <>
            <div className="row mb-4">
              <div className="col-12">
                <p className="text-muted">
                  <i className="fas fa-heart text-danger me-2"></i>
                  You have {favorites.length} favorite {favorites.length === 1 ? 'product' : 'products'}
                </p>
              </div>
            </div>

            <div className="row g-4">
              {favorites.map((favorite) => (
                <div key={favorite.favorite_id} className="col-md-6 col-lg-4 col-xl-3">
                  <div className="card h-100 shadow-sm border-0 favorite-card">
                    <div className="position-relative">
                      <img
                        src={`/img/products/${favorite.product_id}.png`}
                        className="card-img-top"
                        alt={favorite.product_name}
                        style={{ height: '250px', objectFit: 'cover', backgroundColor: '#f8f9fa' }}
                        onError={(e) => {
                          if (e.target.src.endsWith('.png')) {
                            e.target.src = `/img/products/${favorite.product_id}.jpg`;
                          } else if (e.target.src.endsWith('.jpg')) {
                            e.target.src = '/img/product-1.png';
                          }
                        }}
                      />
                      <button
                        onClick={() => handleRemoveFavorite(favorite.product_id)}
                        className="btn btn-danger btn-sm position-absolute top-0 end-0 m-2 rounded-circle"
                        title="Remove from Favorites"
                      >
                        <i className="fas fa-times"></i>
                      </button>
                    </div>
                    <div className="card-body">
                      {favorite.category_name && (
                        <span className="badge bg-secondary mb-2">{favorite.category_name}</span>
                      )}
                      <h5 className="card-title">
                        <Link 
                          to={`/single/${favorite.product_id}`}
                          className="text-dark text-decoration-none"
                        >
                          {favorite.product_name}
                        </Link>
                      </h5>
                      {favorite.description && (
                        <p className="card-text text-muted small" style={{
                          overflow: 'hidden',
                          textOverflow: 'ellipsis',
                          display: '-webkit-box',
                          WebkitLineClamp: 2,
                          WebkitBoxOrient: 'vertical',
                          minHeight: '40px'
                        }}>
                          {favorite.description}
                        </p>
                      )}
                      <div className="d-flex gap-2 mt-3">
                        <Link
                          to={`/single/${favorite.product_id}`}
                          className="btn btn-primary btn-sm rounded-pill flex-grow-1"
                        >
                          <i className="fas fa-eye me-2"></i>
                          View Product
                        </Link>
                        <button
                          onClick={() => handleRemoveFavorite(favorite.product_id)}
                          className="btn btn-outline-danger btn-sm rounded-circle"
                          title="Remove"
                        >
                          <i className="fas fa-heart-broken"></i>
                        </button>
                      </div>
                    </div>
                    <div className="card-footer bg-transparent border-top-0">
                      <small className="text-muted">
                        <i className="far fa-clock me-1"></i>
                        Added {new Date(favorite.created_at).toLocaleDateString()}
                      </small>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </>
        )}
      </div>
    </div>
  );
};

export default Favorites;
