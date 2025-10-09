/**
 * Shop Page Component
 * Product listing page with filters and sorting
 */
import React, { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import ProductCard from '../components/common/ProductCard';
import { products, getProductsByCategory } from '../data/products';
import './Shop.css';

const Shop = () => {
  const [searchParams] = useSearchParams();
  const [filteredProducts, setFilteredProducts] = useState(products);
  const [selectedCategory, setSelectedCategory] = useState('All Category');
  const [sortBy, setSortBy] = useState('default');
  const [priceRange, setPriceRange] = useState([0, 3000]);

  const categories = ['All Category', 'SmartPhone', 'Tablets', 'Laptops & Desktops', 'Accessories', 'Mobiles & Tablets', 'SmartPhone & Smart TV'];

  useEffect(() => {
    const category = searchParams.get('category');
    if (category) {
      setSelectedCategory(category);
    }
  }, [searchParams]);

  useEffect(() => {
    let filtered = getProductsByCategory(selectedCategory);

    // Apply price filter
    filtered = filtered.filter(
      (product) => product.price >= priceRange[0] && product.price <= priceRange[1]
    );

    // Apply sorting
    if (sortBy === 'price-low') {
      filtered.sort((a, b) => a.price - b.price);
    } else if (sortBy === 'price-high') {
      filtered.sort((a, b) => b.price - a.price);
    } else if (sortBy === 'name') {
      filtered.sort((a, b) => a.name.localeCompare(b.name));
    } else if (sortBy === 'rating') {
      filtered.sort((a, b) => b.rating - a.rating);
    }

    setFilteredProducts(filtered);
  }, [selectedCategory, sortBy, priceRange]);

  return (
    <div className="shop-page">
      {/* Page Header */}
      <div className="container-fluid page-header py-5" style={{
        backgroundImage: 'url(/img/carousel-1.jpg)',
        backgroundSize: '200%',
        backgroundPosition: 'center 15%',
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
                    {categories.map((category) => (
                      <li key={category} className="mb-2">
                        <button
                          className={`btn btn-link text-decoration-none ${
                            selectedCategory === category ? 'text-primary fw-bold' : 'text-dark'
                          }`}
                          onClick={() => setSelectedCategory(category)}
                        >
                          {category}
                        </button>
                      </li>
                    ))}
                  </ul>
                </div>

                {/* Price Filter */}
                <div className="sidebar-widget mb-4">
                  <h4 className="mb-3">Price Range</h4>
                  <div className="price-range">
                    <input
                      type="range"
                      className="form-range"
                      min="0"
                      max="3000"
                      step="50"
                      value={priceRange[1]}
                      onChange={(e) => setPriceRange([0, parseInt(e.target.value)])}
                    />
                    <div className="d-flex justify-content-between mt-2">
                      <span>${priceRange[0]}</span>
                      <span>${priceRange[1]}</span>
                    </div>
                  </div>
                </div>

                {/* Featured Product */}
                <div className="sidebar-widget">
                  <h4 className="mb-3">Featured</h4>
                  <div className="border rounded p-3">
                    <img src="/img/product-1.png" className="img-fluid mb-3" alt="Featured" />
                    <h6>Apple iPad Mini</h6>
                    <p className="text-primary mb-0">$1,050.00</p>
                  </div>
                </div>
              </div>
            </div>

            {/* Products Grid */}
            <div className="col-lg-9">
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
                    <option value="price-low">Price: Low to High</option>
                    <option value="price-high">Price: High to Low</option>
                    <option value="rating">Rating</option>
                  </select>
                </div>
              </div>

              {/* Products Grid */}
              <div className="row g-4">
                {filteredProducts.length > 0 ? (
                  filteredProducts.map((product) => (
                    <div key={product.id} className="col-md-6 col-xl-4">
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

              {/* Pagination */}
              {filteredProducts.length > 0 && (
                <nav className="mt-5">
                  <ul className="pagination justify-content-center">
                    <li className="page-item disabled">
                      <a className="page-link" href="#prev">Previous</a>
                    </li>
                    <li className="page-item active">
                      <a className="page-link" href="#1">1</a>
                    </li>
                    <li className="page-item">
                      <a className="page-link" href="#2">2</a>
                    </li>
                    <li className="page-item">
                      <a className="page-link" href="#3">3</a>
                    </li>
                    <li className="page-item">
                      <a className="page-link" href="#next">Next</a>
                    </li>
                  </ul>
                </nav>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Shop;
