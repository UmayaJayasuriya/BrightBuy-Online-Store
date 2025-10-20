/**
 * Bestseller Page Component
 * Displays bestselling products
 */
import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import ProductCard from '../components/common/ProductCard';
import Spinner from '../components/common/Spinner';
import './Bestseller.css';

const Bestseller = () => {
  const [bestsellerProducts, setBestsellerProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchBestsellerProducts = async () => {
      try {
        setLoading(true);
        // Fetch actual bestselling products from the backend
        // This endpoint returns top 10 products by total quantity sold
        const response = await axios.get('http://127.0.0.1:8020/products/bestsellers/');
        
        if (response.data && response.data.length > 0) {
          setBestsellerProducts(response.data);
          setError(null);
        } else {
          setBestsellerProducts([]);
          setError('No bestseller data available yet. Products will appear here once orders are placed.');
        }
      } catch (err) {
        console.error('Error fetching bestseller products:', err);
        setError('Failed to load bestseller products');
      } finally {
        setLoading(false);
      }
    };

    fetchBestsellerProducts();
  }, []);

  if (loading) {
    return <Spinner />;
  }

  if (error) {
    return (
      <div className="container py-5">
        <div className="alert alert-danger text-center">
          {error}
        </div>
      </div>
    );
  }

  return (
    <div className="bestseller-page">
      {/* Page Header */}
      <div className="container-fluid page-header py-5" style={{
        backgroundImage: 'url(/img/topbar.png)',
        backgroundSize: 'cover',
        backgroundPosition: 'center',
        backgroundRepeat: 'no-repeat',
        position: 'relative',
        minHeight: '260px'
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
            <h2 className="display-6 mb-3 fw-bolder">Our Top Selling Products</h2>
            <p className="text-muted fw-semibold">
              Discover our most popular electronics chosen by thousands of satisfied customers
            </p>
          </div>

          <div className="row g-4">
            {bestsellerProducts.length > 0 ? (
              bestsellerProducts.map((product) => (
                <div key={product.product_id} className="col-md-6 col-lg-4 col-xl-3">
                  <ProductCard product={product} />
                </div>
              ))
            ) : (
              <div className="col-12 text-center">
                <p className="text-muted">No bestseller products available at the moment.</p>
              </div>
            )}
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
