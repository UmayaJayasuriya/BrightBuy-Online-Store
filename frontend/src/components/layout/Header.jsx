/**
 * Header Component
 * Displays the main site logo, search bar, and cart/wishlist icons
 */
import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import axios from 'axios';
import { useAuth } from '../../context/AuthContext';
import Login from '../common/Login';
import SignUp from '../common/SignUp';
import './Header.css';

const Header = () => {
  const { isAuthenticated, user, isAdmin, login, logout, registerLoginModalHandler } = useAuth();
  const navigate = useNavigate();
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('All Categories');
  const [categories, setCategories] = useState([]);
  const [isLoginOpen, setIsLoginOpen] = useState(false);
  const [isSignUpOpen, setIsSignUpOpen] = useState(false);
  const [cartCount, setCartCount] = useState(0);
  const [cartTotal, setCartTotal] = useState(0);

  // Register login modal handler on mount
  useEffect(() => {
    registerLoginModalHandler(() => setIsLoginOpen(true));
  }, [registerLoginModalHandler]);

  // Fetch categories from backend
  useEffect(() => {
    const fetchCategories = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:8020/categories/');
        setCategories(response.data);
      } catch (error) {
        console.error('Error fetching categories:', error);
      }
    };
    fetchCategories();
  }, []);

  // Fetch cart data from backend
  useEffect(() => {
    const fetchCart = async () => {
      if (!isAuthenticated || !user) {
        setCartCount(0);
        setCartTotal(0);
        return;
      }

      try {
        const response = await axios.get(`http://127.0.0.1:8020/cart/${user.user_id}`);
        const cartData = response.data;
        if (cartData && cartData.cart_items) {
          // Calculate total count
          const count = cartData.cart_items.reduce((sum, item) => sum + item.quantity, 0);
          setCartCount(count);
          setCartTotal(parseFloat(cartData.total_amount || 0));
        } else {
          setCartCount(0);
          setCartTotal(0);
        }
      } catch (error) {
        console.error('Error fetching cart:', error);
        setCartCount(0);
        setCartTotal(0);
      }
    };

    fetchCart();
    
    // Refresh cart every 5 seconds if user is authenticated
    const interval = setInterval(() => {
      if (isAuthenticated && user) {
        fetchCart();
      }
    }, 5000);

    return () => clearInterval(interval);
  }, [isAuthenticated, user]);

  const handleSearch = (e) => {
    e.preventDefault();
    // Navigate to shop page with search query and category filter
    if (searchQuery.trim()) {
      const params = new URLSearchParams();
      params.append('search', searchQuery);
      if (selectedCategory && selectedCategory !== 'All Categories') {
        params.append('category', selectedCategory);
      }
      navigate(`/shop?${params.toString()}`);
    } else if (selectedCategory && selectedCategory !== 'All Categories') {
      // If no search query but category is selected, navigate to that category
      navigate(`/shop?category=${encodeURIComponent(selectedCategory)}`);
    } else {
      // If neither search nor category, just go to shop
      navigate('/shop');
    }
  };

  const handleCategoryChange = (e) => {
    const category = e.target.value;
    setSelectedCategory(category);
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
                BrightBuy
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
                onChange={handleCategoryChange}
              >
                <option value="All Categories">All Categories</option>
                {categories.map((category) => (
                  <option key={category.category_id} value={category.category_name}>
                    {category.category_name}
                  </option>
                ))}
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

            {/* Login Oval Button */}
            <button
              onClick={handleWishlistClick}
              className="login-oval me-3"
              title="Login"
              aria-label="Login"
            >
              Login
            </button>

            {/* Sign-up Oval Button */}
            <button
              onClick={() => setIsSignUpOpen(true)}
              className="signup-oval me-3"
              title="Sign up"
              aria-label="Sign up"
            >
              Sign-up
            </button>

            {/* Cart Icon */}
            <Link
              to="/cart"
              className="text-muted d-flex align-items-center justify-content-center"
            >
              <span className="rounded-circle btn-md-square border position-relative d-flex align-items-center justify-content-center" style={{ width: '45px', height: '45px' }}>
                <i className="fa-solid fa-shopping-cart"></i>
                {cartCount > 0 && (
                  <span className="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger">
                    {cartCount}
                  </span>
                )}
              </span>
              <span className="text-dark ms-2">${cartTotal.toFixed(2)}</span>
            </Link>
          </div>
        </div>
      </div>

      {/* User Greeting */}
      {isAuthenticated && (
        <div className="container-fluid px-5 py-2 header-greeting">
          <div className="row">
            <div className="col-12 text-end">
              <small className="text-muted">
                <span className="user-greeting">
                  <span>
                    Welcome back, <Link to="/profile" className="text-decoration-none fw-bolder text-primary">{user.user_name}</Link>!
                    {isAdmin && (
                      <> | <Link to="/admin" className="text-decoration-none text-danger fw-bold">Admin Dashboard</Link></>
                    )}
                  </span>
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
        onSwitchToSignUp={() => {
          setIsLoginOpen(false);
          setIsSignUpOpen(true);
        }}
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
        onSwitchToLogin={() => {
          setIsSignUpOpen(false);
          setIsLoginOpen(true);
        }}
      />
    </div>
  );
};

export default Header;
