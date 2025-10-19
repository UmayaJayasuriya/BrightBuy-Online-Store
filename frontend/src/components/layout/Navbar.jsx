/**
 * Navbar Component
 * Main navigation menu with category dropdown
 */
import React, { useState, useRef, useEffect } from 'react';
import { Link, NavLink } from 'react-router-dom';
import axios from 'axios';
import './Navbar.css';

const Navbar = () => {
  const [isNavOpen, setIsNavOpen] = useState(false);
  const [isCategoryOpen, setIsCategoryOpen] = useState(false);
  const [categories, setCategories] = useState([]);

  const navRef = useRef(null);

  // Fetch categories from backend
  useEffect(() => {
    const fetchCategories = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:8020/categories/');
        console.log('Categories fetched:', response.data);
        setCategories(response.data);
      } catch (error) {
        console.error('Error fetching categories:', error);
      }
    };
    fetchCategories();
  }, []);

  useEffect(() => {
    const handleClickOutside = (e) => {
      if (isCategoryOpen && navRef.current && !navRef.current.contains(e.target)) {
        setIsCategoryOpen(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, [isCategoryOpen]);

  return (
    <div className="container-fluid nav-bar p-0">
      <div className="row gx-0 bg-primary px-5 align-items-center">
        {/* Categories Sidebar */}
        <div className="col-lg-3 d-none d-lg-block">
          <nav ref={navRef} className="navbar navbar-light position-relative" style={{ width: '250px' }}>
            <button
              className="navbar-toggler border-0 fs-4 w-100 px-0 text-start"
              type="button"
              onClick={() => setIsCategoryOpen(!isCategoryOpen)}
            >
              <h4 className="m-0">
                <i className="fa fa-bars me-2"></i>All Categories
              </h4>
            </button>
            <div className={`collapse navbar-collapse rounded-bottom categories-collapse ${isCategoryOpen ? 'show' : ''}`}>
              <div className="navbar-nav ms-auto py-0">
                <ul className="list-unstyled categories-bars">
                  {categories.map((category) => (
                    <li key={category.category_id}>
                      <div className="categories-bars-item">
                        <Link to={`/shop?category=${encodeURIComponent(category.category_name)}`}>
                          {category.category_name}
                        </Link>
                      </div>
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          </nav>
        </div>

        {/* Main Navigation */}
        <div className="col-12 col-lg-9">
          <nav className="navbar navbar-expand-lg navbar-light bg-primary">
            {/* Mobile Logo */}
            <Link to="/" className="navbar-brand d-block d-lg-none">
              <h1 className="display-5 text-secondary m-0">
                <i className="fas fa-shopping-bag text-white me-2"></i>Electro
              </h1>
            </Link>

            {/* Mobile Toggle */}
            <button
              className="navbar-toggler ms-auto"
              type="button"
              onClick={() => setIsNavOpen(!isNavOpen)}
            >
              <span className="fa fa-bars fa-1x"></span>
            </button>

            {/* Navigation Links */}
            <div className={`collapse navbar-collapse ${isNavOpen ? 'show' : ''}`}>
              <div className="navbar-nav ms-auto py-0">
                <NavLink to="/" className="nav-item nav-link">
                  Home
                </NavLink>
                <NavLink to="/shop" className="nav-item nav-link">
                  Shop
                </NavLink>

                <NavLink to="/favorites" className="nav-item nav-link">
                  Favorites
                </NavLink>

                {/* Pages Dropdown */}
                <div className="nav-item dropdown">
                  <a
                    href="#pages"
                    className="nav-link dropdown-toggle"
                    data-bs-toggle="dropdown"
                  >
                    Pages
                  </a>
                  <div className="dropdown-menu m-0">
                    <Link to="/bestseller" className="dropdown-item">
                      Bestseller
                    </Link>
                    <Link to="/cart" className="dropdown-item">
                      Cart Page
                    </Link>
                    <Link to="/checkout" className="dropdown-item">
                      Checkout
                    </Link>
                    <Link to="/favorites" className="dropdown-item">
                      My Favorites
                    </Link>
                  </div>
                </div>

                <NavLink to="/contact" className="nav-item nav-link me-2">
                  Contact
                </NavLink>

                {/* Mobile Category Dropdown */}
                <div className="nav-item dropdown d-block d-lg-none mb-3">
                  <a
                    href="#category"
                    className="nav-link dropdown-toggle"
                    data-bs-toggle="dropdown"
                  >
                    All Category
                  </a>
                  <div className="dropdown-menu m-0">
                    <ul className="list-unstyled categories-bars">
                      {categories.map((category) => (
                        <li key={category.category_id}>
                          <div className="categories-bars-item">
                            <Link to={`/shop?category=${encodeURIComponent(category.category_name)}`}>
                              {category.category_name}
                            </Link>
                          </div>
                        </li>
                      ))}
                    </ul>
                  </div>
                </div>
              </div>

              {/* Call Button */}
              <a
                href="tel:+01234567890"
                className="btn btn-secondary rounded-pill py-2 px-4 px-lg-3 mb-3 mb-md-3 mb-lg-0"
              >
                <i className="fa fa-mobile-alt me-2"></i> +0123 456 7890
              </a>
            </div>
          </nav>
        </div>
      </div>
    </div>
  );
};

export default Navbar;
