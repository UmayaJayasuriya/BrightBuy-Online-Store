/**
 * Header Component
 * Displays the main site logo, search bar, and cart/wishlist icons
 */
import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { useCart } from '../../context/CartContext';
import { useAuth } from '../../context/AuthContext';
import Login from '../common/Login';
import SignUp from '../common/SignUp';
import './Header.css';

const Header = () => {
  const { getCartTotal, getCartItemsCount } = useCart();
  const { isAuthenticated, user, login, logout } = useAuth();
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('All Category');
  const [isLoginOpen, setIsLoginOpen] = useState(false);
  const [isSignUpOpen, setIsSignUpOpen] = useState(false);

  const handleSearch = (e) => {
    e.preventDefault();
    // Implement search functionality
    console.log('Searching for:', searchQuery, 'in category:', selectedCategory);
  };

  const handleWishlistClick = (e) => {
    e.preventDefault();
    if (isAuthenticated) {
      // User is logged in, navigate to wishlist
      console.log('Navigate to wishlist for user:', user.user_name);
      // TODO: Navigate to wishlist page
    } else {
      // User is not logged in, show login modal
      setIsLoginOpen(true);
    }
  };

  const handleLoginSuccess = (userData) => {
    login(userData);
    console.log('User logged in successfully:', userData.user_name);
  };

  const handleLogout = () => {
    logout();
    console.log('User logged out');
  };

  return (
    <div className="container-fluid px-5 py-4 d-none d-lg-block">
      <div className="row gx-0 align-items-center text-center">
        {/* Logo Section */}
        <div className="col-md-4 col-lg-3 text-center text-lg-start">
          <div className="d-inline-flex align-items-center">
            <Link to="/" className="navbar-brand p-0">
              <h1 className="display-5 text-primary m-0">
                <i className="fa-solid fa-shopping-bag text-secondary me-2"></i>
                Electro
              </h1>
            </Link>
          </div>
        </div>

        {/* Search Bar Section */}
        <div className="col-md-4 col-lg-6 text-center">
          <div className="position-relative ps-4">
            <form onSubmit={handleSearch} className="d-flex border rounded-pill">
              <input
                className="form-control border-0 rounded-pill w-100 py-3"
                type="text"
                placeholder="Search Looking For?"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
              />
              <select
                className="form-select text-dark border-0 border-start rounded-0 p-3"
                style={{ width: '200px' }}
                value={selectedCategory}
                onChange={(e) => setSelectedCategory(e.target.value)}
              >
                <option value="All Category">All Category</option>
                <option value="Category 1">Category 1</option>
                <option value="Category 2">Category 2</option>
                <option value="Category 3">Category 3</option>
                <option value="Category 4">Category 4</option>
              </select>
              <button
                type="submit"
                className="btn btn-primary rounded-pill py-3 px-5"
                style={{ border: 0 }}
              >
                <i className="fa-solid fa-magnifying-glass"></i>
              </button>
            </form>
          </div>
        </div>

        {/* Icons Section - Compare, Wishlist, Cart */}
        <div className="col-md-4 col-lg-3 text-center text-lg-end">
          <div className="d-inline-flex align-items-center">
            {/* (removed unused compare button) */}

            {/* Wishlist Icon */}
            <button
              onClick={handleWishlistClick}
              className="text-muted d-flex align-items-center justify-content-center me-3 bg-transparent border-0"
              title={isAuthenticated ? "Go to Wishlist" : "Login to access Wishlist"}
            >
              <span className="rounded-circle btn-md-square border d-flex align-items-center justify-content-center" style={{ width: '45px', height: '45px' }}>
                <i className={`fa-solid fa-heart ${isAuthenticated ? 'text-danger' : ''}`}></i>
              </span>
            </button>

            {/* Share/Sign Up Icon (moved between wishlist and cart) */}
            <button
              onClick={() => setIsSignUpOpen(true)}
              className="text-muted d-flex align-items-center justify-content-center me-3 bg-transparent border-0"
              title="Sign up"
            >
              <span className="rounded-circle btn-md-square border d-flex align-items-center justify-content-center" style={{ width: '45px', height: '45px' }}>
                <i className="fa-solid fa-share-nodes"></i>
              </span>
            </button>

            {/* Cart Icon */}
            <Link
              to="/cart"
              className="text-muted d-flex align-items-center justify-content-center"
            >
              <span className="rounded-circle btn-md-square border position-relative d-flex align-items-center justify-content-center" style={{ width: '45px', height: '45px' }}>
                <i className="fa-solid fa-shopping-cart"></i>
                {getCartItemsCount() > 0 && (
                  <span className="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger">
                    {getCartItemsCount()}
                  </span>
                )}
              </span>
              <span className="text-dark ms-2">${getCartTotal().toFixed(2)}</span>
            </Link>
          </div>
        </div>
      </div>

      {/* User Greeting */}
      {isAuthenticated && (
        <div className="container-fluid px-5 py-2 bg-light">
          <div className="row">
            <div className="col-12 text-end">
              <small className="text-muted">
                <span className="user-greeting">
                  <span>Welcome back, <strong className="text-primary">{user.user_name}</strong>!</span>
                  <button 
                    onClick={handleLogout} 
                    className="btn btn-link btn-sm text-danger logout-link"
                    aria-label="Logout"
                  >
                    Logout
                  </button>
                </span>
              </small>
            </div>
          </div>
        </div>
      )}

      {/* Login Modal */}
      <Login 
        isOpen={isLoginOpen}
        onClose={() => setIsLoginOpen(false)}
        onLoginSuccess={handleLoginSuccess}
      />

      {/* SignUp Modal */}
      <SignUp
        isOpen={isSignUpOpen}
        onClose={() => setIsSignUpOpen(false)}
        onSignUpSuccess={(createdUser) => {
          // createdUser is the UserOut returned by backend
          // set as authenticated user in context
          login(createdUser);
          setIsSignUpOpen(false);
        }}
      />
    </div>
  );
};

export default Header;
