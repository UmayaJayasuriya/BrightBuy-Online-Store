/**
 * NotFound (404) Page Component
 * Displayed when user navigates to non-existent route
 */
import React from 'react';
import { Link } from 'react-router-dom';
import './NotFound.css';

const NotFound = () => {
  return (
    <div className="notfound-page">
      <div className="container py-5">
        <div className="row justify-content-center">
          <div className="col-lg-8 text-center">
            <div className="error-content">
              <h1 className="display-1 fw-bold text-primary mb-4">404</h1>
              <h2 className="mb-4">Oops! Page Not Found</h2>
              <p className="text-muted mb-5">
                The page you are looking for might have been removed, had its name changed,
                or is temporarily unavailable.
              </p>
              
              <div className="d-flex flex-column flex-sm-row gap-3 justify-content-center mb-5">
                <Link to="/" className="btn btn-primary rounded-pill py-3 px-5">
                  <i className="fas fa-home me-2"></i>
                  Go to Homepage
                </Link>
                <Link to="/shop" className="btn btn-outline-primary rounded-pill py-3 px-5">
                  <i className="fas fa-shopping-bag me-2"></i>
                  Continue Shopping
                </Link>
              </div>

              {/* Search Box */}
              <div className="search-box mx-auto" style={{ maxWidth: '500px' }}>
                <h5 className="mb-3">Or search for what you need:</h5>
                <form className="d-flex">
                  <input
                    type="text"
                    className="form-control rounded-pill me-2"
                    placeholder="Search products..."
                  />
                  <button type="submit" className="btn btn-primary rounded-pill px-4">
                    Search
                  </button>
                </form>
              </div>

              {/* Helpful Links */}
              <div className="helpful-links mt-5">
                <h6 className="mb-3">You might be interested in:</h6>
                <div className="d-flex flex-wrap gap-2 justify-content-center">
                  <Link to="/shop" className="badge bg-light text-dark p-2">
                    Shop
                  </Link>
                  <Link to="/bestseller" className="badge bg-light text-dark p-2">
                    Bestsellers
                  </Link>
                  <Link to="/contact" className="badge bg-light text-dark p-2">
                    Contact Us
                  </Link>
                  <Link to="/cart" className="badge bg-light text-dark p-2">
                    Shopping Cart
                  </Link>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default NotFound;
