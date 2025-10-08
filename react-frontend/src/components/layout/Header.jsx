/**
 * Header Component
 * Displays the main site logo, search bar, and cart/wishlist icons
 */
import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { useCart } from '../../context/CartContext';
import './Header.css';

const Header = () => {
  const { getCartTotal, getCartItemsCount } = useCart();
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('All Category');

  const handleSearch = (e) => {
    e.preventDefault();
    // Implement search functionality
    console.log('Searching for:', searchQuery, 'in category:', selectedCategory);
  };

  return (
    <div className="container-fluid px-5 py-4 d-none d-lg-block">
      <div className="row gx-0 align-items-center text-center">
        {/* Logo Section */}
        <div className="col-md-4 col-lg-3 text-center text-lg-start">
          <div className="d-inline-flex align-items-center">
            <Link to="/" className="navbar-brand p-0">
              <h1 className="display-5 text-primary m-0">
                <i className="fas fa-shopping-bag text-secondary me-2"></i>
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
                <i className="fas fa-search"></i>
              </button>
            </form>
          </div>
        </div>

        {/* Icons Section - Compare, Wishlist, Cart */}
        <div className="col-md-4 col-lg-3 text-center text-lg-end">
          <div className="d-inline-flex align-items-center">
            {/* Compare Icon */}
            <Link
              to="#compare"
              className="text-muted d-flex align-items-center justify-content-center me-3"
            >
              <span className="rounded-circle btn-md-square border">
                <i className="fas fa-random"></i>
              </span>
            </Link>

            {/* Wishlist Icon */}
            <Link
              to="#wishlist"
              className="text-muted d-flex align-items-center justify-content-center me-3"
            >
              <span className="rounded-circle btn-md-square border">
                <i className="fas fa-heart"></i>
              </span>
            </Link>

            {/* Cart Icon */}
            <Link
              to="/cart"
              className="text-muted d-flex align-items-center justify-content-center"
            >
              <span className="rounded-circle btn-md-square border position-relative">
                <i className="fas fa-shopping-cart"></i>
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
    </div>
  );
};

export default Header;
