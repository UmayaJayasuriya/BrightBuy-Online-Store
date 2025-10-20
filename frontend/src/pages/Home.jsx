
import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import ProductCard from '../components/common/ProductCard';
import Spinner from '../components/common/Spinner';
import './Home.css';

const Home = () => {
  const [currentSlide, setCurrentSlide] = useState(0);
  const [featuredProducts, setFeaturedProducts] = useState([]);
  const [loading, setLoading] = useState(true);

  // Fetch featured products from different categories
  useEffect(() => {
    const fetchFeaturedProducts = async () => {
      setLoading(true);
      try {
        // Fetch all categories
        const categoriesResponse = await axios.get('http://127.0.0.1:8020/categories/');
        const categories = categoriesResponse.data;

        // Take first 6 categories
        const selectedCategories = categories.slice(0, 6);

        // Fetch one product from each category
        const productsPromises = selectedCategories.map(async (category) => {
          const response = await axios.get(
            `http://127.0.0.1:8020/products/?category_name=${encodeURIComponent(category.category_name)}`
          );
          // Return the first product from this category
          return response.data[0];
        });

        const products = await Promise.all(productsPromises);
        // Filter out any undefined products (categories with no products)
        setFeaturedProducts(products.filter(p => p));
      } catch (error) {
        console.error('Error fetching featured products:', error);
        setFeaturedProducts([]);
      } finally {
        setLoading(false);
      }
    };

    fetchFeaturedProducts();
  }, []);

  const carouselSlides = [
    {
      image: '/img/carousel-1.png',
      title: 'Save Up To A $400',
      subtitle: 'On Selected Laptops & Desktop Or Smartphone',
      description: 'Terms and Condition Apply'
    },
    {
      image: '/img/carousel-2.png',
      title: 'Save Up To A $200',
      subtitle: 'On Selected Laptops & Desktop Or Smartphone',
      description: 'Terms and Condition Apply'
    }
  ];

  // Auto-advance carousel
  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentSlide((prev) => (prev + 1) % carouselSlides.length);
    }, 5000);

    return () => clearInterval(interval);
  }, [carouselSlides.length]);

  const services = [
    { icon: 'fa-shipping-fast', title: 'Free Shipping', description: 'Free shipping on orders over $50' },
    { icon: 'fa-undo', title: 'Easy Returns', description: '30-day return policy' },
    { icon: 'fa-lock', title: 'Secure Payment', description: '100% secure payment' },
    { icon: 'fa-headset', title: '24/7 Support', description: 'Dedicated support team' },
    { icon: 'fa-gift', title: 'Gift Cards', description: 'Perfect gift options' },
    { icon: 'fa-percent', title: 'Best Deals', description: 'Up to 70% off' }
  ];

  return (
    <div className="home-page">
      {/* Hero Carousel Section */}
      <div className="container-fluid carousel px-0">
        <div className="row g-0" style={{ minHeight: '500px' }}>
          {/* Main Carousel Content */}
          <div className="col-12 col-lg-7 col-xl-9">
            <div className="header-carousel bg-light h-100">
              <div className="row g-0 align-items-center h-100">
                {/* Left - Product Image */}
                <div className="col-xl-6 carousel-img">
                  {carouselSlides.map((slide, index) => (
                    <div
                      key={index}
                      className={`carousel-image ${index === currentSlide ? 'active' : 'd-none'}`}
                    >
                      <img src={slide.image} className="img-fluid w-100" alt="Carousel" />
                    </div>
                  ))}
                </div>
                
                {/* Right - Text Content */}
                <div className="col-xl-6 carousel-content p-4">
                  {carouselSlides.map((slide, index) => (
                    <div
                      key={index}
                      className={`carousel-text-content ${index === currentSlide ? 'active' : 'd-none'}`}
                    >
                      <h4 className="text-uppercase fw-bold mb-4" style={{ letterSpacing: '3px', color: '#666' }}>
                        {(index === 0 || index === 1) ? <strong>{slide.title}</strong> : slide.title}
                      </h4>
                      <h1 className="display-3 text-capitalize mb-4" style={{ color: '#333' }}>
                        {(index === 0 || index === 1) ? <strong>{slide.subtitle}</strong> : slide.subtitle}
                      </h1>
                      <p className="text-muted mb-4">{slide.description}</p>
                      <Link className="btn btn-primary rounded-pill py-3 px-5" to="/shop">
                        Shop Now
                      </Link>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>

          {/* Side Banner */}
          <div className="col-12 col-lg-5 col-xl-3">
            <div className="carousel-header-banner h-100 position-relative" style={{ background: 'none' }}>
              <img
                src="https://i.pinimg.com/736x/19/87/f3/1987f35dbba2d94da2e3b142fe2234b9.jpg"
                loading="lazy"
                className="img-fluid w-100 h-100"
                style={{ objectFit: 'cover', position: 'absolute', top: 0, left: 0, zIndex: 0 }}
                alt="Woman holding a smartphone with shopping cart on screen"
              />
              {/* Banner overlays removed - only the image will display here */}
            </div>
          </div>
        </div>
      </div>

      {/* Services Section */}
      <div className="container-fluid px-0">
        <div className="row g-0">
          {services.map((service, index) => (
            <div
              key={index}
              className="col-6 col-md-4 col-lg-2 border-start border-end wow fadeInUp"
              data-wow-delay={`${0.1 * (index + 1)}s`}
            >
              <div className="p-4 text-center">
                <i className={`fas ${service.icon} fa-3x text-primary mb-3`}></i>
                <h5 className="mb-2">{service.title}</h5>
                <p className="mb-0 text-muted small">{service.description}</p>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Featured Products */}
      <div className="container-fluid product py-5">
        <div className="container py-5">
          <div className="section-title text-center mb-5 wow fadeInUp" data-wow-delay="0.1s">
            <h1 className="display-5 mb-3"><strong>Featured Products</strong></h1>
            <p className="text-muted">Check out our best-selling electronics from different categories</p>
          </div>

          {loading ? (
            <div className="text-center py-5">
              <Spinner />
            </div>
          ) : (
            <div className="row g-4">
              {featuredProducts.map((product, index) => (
                <div
                  key={product.product_id}
                  className="col-md-6 col-lg-4 col-xl-4 wow fadeInUp"
                  data-wow-delay={`${index * 0.1}s`}
                >
                  <ProductCard product={product} />
                </div>
              ))}
            </div>
          )}

          <div className="text-center mt-5">
            <Link to="/shop" className="btn btn-primary rounded-pill py-3 px-5">
              View All Products
            </Link>
          </div>
        </div>
      </div>    
    </div>
  );
};

export default Home;
