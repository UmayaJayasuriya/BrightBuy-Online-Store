/**
 * Bestseller Page Component
 * Displays bestselling products
 */
import React from 'react';
import { Link } from 'react-router-dom';
import ProductCard from '../components/common/ProductCard';
import { getFeaturedProducts } from '../data/products';
import './Bestseller.css';

const Bestseller = () => {
  const bestsellerProducts = getFeaturedProducts();

  return (
    <div className="bestseller-page">
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
          <h1 className="display-4 text-white mb-3" style={{ fontWeight: '700' }}>Bestsellers</h1>
          <nav aria-label="breadcrumb">
            <ol className="breadcrumb justify-content-center mb-0">
              <li className="breadcrumb-item"><Link to="/">Home</Link></li>
              <li className="breadcrumb-item active text-white">Bestsellers</li>
            </ol>
          </nav>
        </div>
      </div>

      {/* Bestseller Content */}
      <div className="container-fluid py-5">
        <div className="container py-5">
          <div className="section-title text-center mb-5">
            <h2 className="display-6 mb-3">Our Top Selling Products</h2>
            <p className="text-muted">
              Discover our most popular electronics chosen by thousands of satisfied customers
            </p>
          </div>

          <div className="row g-4">
            {bestsellerProducts.map((product) => (
              <div key={product.id} className="col-md-6 col-lg-4 col-xl-3">
                <ProductCard product={product} />
              </div>
            ))}
          </div>

          {/* Call to Action */}
          <div className="text-center mt-5">
            <Link to="/shop" className="btn btn-primary rounded-pill py-3 px-5">
              View All Products
            </Link>
          </div>
        </div>
      </div>

      {/* Why Choose Us Section */}
      <div className="container-fluid bg-light py-5">
        <div className="container py-5">
          <h2 className="text-center mb-5">Why Choose Our Bestsellers?</h2>
          <div className="row g-4">
            <div className="col-md-6 col-lg-3">
              <div className="text-center">
                <i className="fas fa-star fa-3x text-primary mb-3"></i>
                <h5>Top Rated</h5>
                <p className="text-muted">All products rated 4.5+ stars</p>
              </div>
            </div>
            <div className="col-md-6 col-lg-3">
              <div className="text-center">
                <i className="fas fa-certificate fa-3x text-primary mb-3"></i>
                <h5>Quality Assured</h5>
                <p className="text-muted">100% authentic products</p>
              </div>
            </div>
            <div className="col-md-6 col-lg-3">
              <div className="text-center">
                <i className="fas fa-shipping-fast fa-3x text-primary mb-3"></i>
                <h5>Fast Delivery</h5>
                <p className="text-muted">Express shipping available</p>
              </div>
            </div>
            <div className="col-md-6 col-lg-3">
              <div className="text-center">
                <i className="fas fa-headset fa-3x text-primary mb-3"></i>
                <h5>24/7 Support</h5>
                <p className="text-muted">Always here to help</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Bestseller;
