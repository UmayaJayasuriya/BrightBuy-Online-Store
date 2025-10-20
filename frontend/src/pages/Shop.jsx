/**
 * Shop Page Component
 * Product listing page with filters and sorting
 */
import React, { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import axios from 'axios';
import ProductCard from '../components/common/ProductCard';
import Spinner from '../components/common/Spinner';
import './Shop.css';

const Shop = () => {
  const [searchParams] = useSearchParams();
  const [products, setProducts] = useState([]);
  const [filteredProducts, setFilteredProducts] = useState([]);
  const [categories, setCategories] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState('All Category');
  const [searchQuery, setSearchQuery] = useState('');
  const [sortBy, setSortBy] = useState('default');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  // Handle category and search from URL params FIRST - runs on mount and when URL changes
  useEffect(() => {
    const category = searchParams.get('category');
    const search = searchParams.get('search');
    console.log('📍 Category from URL:', category);
    console.log('🔍 Search from URL:', search);
    if (category) {
      setSelectedCategory(category);
    } else {
      setSelectedCategory('All Category');
    }
    if (search) {
      setSearchQuery(search);
    } else {
      setSearchQuery('');
    }
  }, [searchParams]);

  // Fetch categories from backend
  useEffect(() => {
    const fetchCategories = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:8020/categories/');
        setCategories(response.data);
      } catch (err) {
        console.error('Error fetching categories:', err);
        setError('Failed to load categories');
      }
    };
    fetchCategories();
  }, []);

  // Fetch products when component mounts or category changes
  useEffect(() => {
    const fetchProducts = async () => {
      setLoading(true);
      setError('');
      try {
        let url = 'http://127.0.0.1:8020/products/';
        
        // Only filter by category if a specific category is selected (not "All Category")
        if (selectedCategory && selectedCategory !== 'All Category') {
          url += `?category_name=${encodeURIComponent(selectedCategory)}`;
        }
        
        console.log('🔍 Fetching products from:', url, '| Selected category:', selectedCategory);
        const response = await axios.get(url);
        console.log('✅ Products received:', response.data.length, 'products');
        setProducts(response.data);
        setFilteredProducts(response.data);
      } catch (err) {
        console.error('Error fetching products:', err);
        setError('Failed to load products');
        setProducts([]);
        setFilteredProducts([]);
      } finally {
        setLoading(false);
      }
    };
    
    fetchProducts();
  }, [selectedCategory]);

  // Apply filters and sorting to products
  useEffect(() => {
    let filtered = [...products];

    // Apply search filter
    if (searchQuery) {
      filtered = filtered.filter(product => {
        const query = searchQuery.toLowerCase();
        const productName = product.product_name.toLowerCase();
        const categoryName = product.category?.category_name?.toLowerCase() || '';
        
        // Search in product name and category name only (not description)
        return productName.includes(query) || categoryName.includes(query);
      });
    }

    // Apply sorting
    if (sortBy === 'name') {
      filtered.sort((a, b) => a.product_name.localeCompare(b.product_name));
    }

    setFilteredProducts(filtered);
  }, [products, searchQuery, sortBy]);

  return (
    <div className="shop-page">
      {/* Page Header */}
      <div className="container-fluid page-header py-5" style={{
        // Use the site's topbar image per user request
        backgroundImage: 'url(/img/topbar.png)',
        backgroundSize: 'cover',
        backgroundPosition: 'center',
        backgroundRepeat: 'no-repeat',
        position: 'relative'
      }}>
        <div style={{
          position: 'absolute',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          backgroundColor: 'rgba(0, 0, 0, 0.5)',
          zIndex: 1
        }}></div>
        <div className="container text-center py-5" style={{ position: 'relative', zIndex: 2 }}>
          <h1 className="display-4 text-white mb-3" style={{ fontWeight: '700' }}>Shop</h1>
          <nav aria-label="breadcrumb">
            <ol className="breadcrumb justify-content-center mb-0">
              <li className="breadcrumb-item"><a href="/">Home</a></li>
              <li className="breadcrumb-item active text-white">Shop</li>
            </ol>
          </nav>
        </div>
      </div>

      {/* Shop Content */}
      <div className="container-fluid py-5">
        <div className="container py-5">
          <div className="row g-4">
            {/* Sidebar Filters */}
            <div className="col-lg-3">
              <div className="shop-sidebar">
                {/* Categories */}
                <div className="sidebar-widget mb-4">
                  <h4 className="mb-3">Categories</h4>
                  <ul className="list-unstyled">
                    <li className="mb-2">
                      <button
                        className={`btn btn-link text-decoration-none ${
                          selectedCategory === 'All Category' ? 'text-primary fw-bold' : 'text-dark'
                        }`}
                        onClick={() => setSelectedCategory('All Category')}
                      >
                        All Category
                      </button>
                    </li>
                    {categories.map((category) => (
                      <li key={category.category_id} className="mb-2">
                        <button
                          className={`btn btn-link text-decoration-none ${
                            selectedCategory === category.category_name ? 'text-primary fw-bold' : 'text-dark'
                          }`}
                          onClick={() => setSelectedCategory(category.category_name)}
                        >
                          {category.category_name}
                        </button>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            </div>

            {/* Products Grid */}
            <div className="col-lg-9">
              {/* Search Query Display */}
              {searchQuery && (
                <div className="alert alert-info d-flex justify-content-between align-items-center mb-3">
                  <span>
                    Search results for: <strong>"{searchQuery}"</strong>
                  </span>
                  <button 
                    className="btn btn-sm btn-outline-secondary"
                    onClick={() => {
                      setSearchQuery('');
                      window.history.pushState({}, '', '/shop');
                    }}
                  >
                    Clear Search
                  </button>
                </div>
              )}

              {/* Toolbar */}
              <div className="shop-toolbar d-flex justify-content-between align-items-center mb-4 p-3 bg-light rounded">
                <div>
                  <span className="text-muted">
                    Showing {filteredProducts.length} products
                  </span>
                </div>
                <div className="d-flex align-items-center">
                  <label className="me-2 mb-0">Sort by:</label>
                  <select
                    className="form-select"
                    value={sortBy}
                    onChange={(e) => setSortBy(e.target.value)}
                    style={{ width: 'auto' }}
                  >
                    <option value="default">Default</option>
                    <option value="name">Name</option>
                  </select>
                </div>
              </div>

              {/* Loading State */}
              {loading && (
                <div className="text-center py-5">
                  <Spinner />
                </div>
              )}

              {/* Error State */}
              {error && (
                <div className="alert alert-danger">
                  {error}
                </div>
              )}

              {/* Products Grid */}
              {!loading && !error && (
                <div className="row g-4">
                  {filteredProducts.length > 0 ? (
                    filteredProducts.map((product) => (
                      <div key={product.product_id} className="col-md-6 col-xl-4">
                        <ProductCard product={product} />
                      </div>
                    ))
                  ) : (
                    <div className="col-12">
                      <div className="alert alert-info text-center">
                        No products found matching your criteria.
                      </div>
                    </div>
                  )}
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Shop;
