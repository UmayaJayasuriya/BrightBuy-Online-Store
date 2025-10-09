/**
 * Footer Component
 * Site footer with contact info, newsletter signup, and links
 */
import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import './Footer.css';

const Footer = () => {
  const [email, setEmail] = useState('');

  const handleNewsletterSubmit = (e) => {
    e.preventDefault();
    // Handle newsletter subscription
    console.log('Newsletter signup:', email);
    setEmail('');
  };

  return (
    <>
      {/* Footer Start */}
      <div className="container-fluid footer py-5 wow fadeIn" data-wow-delay="0.2s">
        <div className="container py-5">
          {/* Contact Info Cards */}
          <div className="row g-4 rounded mb-5" style={{ background: 'rgba(255, 255, 255, .03)' }}>
            <div className="col-md-6 col-lg-6 col-xl-3">
              <div className="rounded p-4">
                <div
                  className="rounded-circle bg-secondary d-flex align-items-center justify-content-center mb-4"
                  style={{ width: '70px', height: '70px' }}
                >
                  <i className="fas fa-map-marker-alt fa-2x text-primary"></i>
                </div>
                <div>
                  <h4 className="text-white">Address</h4>
                  <p className="mb-2">123 Street New York.USA</p>
                </div>
              </div>
            </div>

            <div className="col-md-6 col-lg-6 col-xl-3">
              <div className="rounded p-4">
                <div
                  className="rounded-circle bg-secondary d-flex align-items-center justify-content-center mb-4"
                  style={{ width: '70px', height: '70px' }}
                >
                  <i className="fas fa-envelope fa-2x text-primary"></i>
                </div>
                <div>
                  <h4 className="text-white">Mail Us</h4>
                  <p className="mb-2">info@example.com</p>
                </div>
              </div>
            </div>

            <div className="col-md-6 col-lg-6 col-xl-3">
              <div className="rounded p-4">
                <div
                  className="rounded-circle bg-secondary d-flex align-items-center justify-content-center mb-4"
                  style={{ width: '70px', height: '70px' }}
                >
                  <i className="fa fa-phone-alt fa-2x text-primary"></i>
                </div>
                <div>
                  <h4 className="text-white">Telephone</h4>
                  <p className="mb-2">(+012) 3456 7890</p>
                </div>
              </div>
            </div>

            <div className="col-md-6 col-lg-6 col-xl-3">
              <div className="rounded p-4">
                <div
                  className="rounded-circle bg-secondary d-flex align-items-center justify-content-center mb-4"
                  style={{ width: '70px', height: '70px' }}
                >
                  <i className="fab fa-firefox-browser fa-2x text-primary"></i>
                </div>
                <div>
                  <h4 className="text-white">Yoursite@ex.com</h4>
                  <p className="mb-2">(+012) 3456 7890</p>
                </div>
              </div>
            </div>
          </div>

          {/* Footer Links */}
          <div className="row g-5">
            {/* Newsletter */}
            <div className="col-md-6 col-lg-6 col-xl-3">
              <div className="footer-item d-flex flex-column">
                <h4 className="text-primary mb-4">Newsletter</h4>
                <p className="mb-3">
                  Dolor amet sit justo amet elitr clita ipsum elitr est. Lorem ipsum dolor sit amet, 
                  consectetur adipiscing elit.
                </p>
                <form onSubmit={handleNewsletterSubmit} className="position-relative mx-auto rounded-pill">
                  <input
                    className="form-control rounded-pill w-100 py-3 ps-4 pe-5"
                    type="email"
                    placeholder="Enter your email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                  />
                  <button
                    type="submit"
                    className="btn btn-primary rounded-pill position-absolute top-0 end-0 py-2 mt-2 me-2"
                  >
                    SignUp
                  </button>
                </form>
              </div>
            </div>

            {/* Customer Service Links */}
            <div className="col-md-6 col-lg-6 col-xl-3">
              <div className="footer-item d-flex flex-column">
                <h4 className="text-primary mb-4">Customer Service</h4>
                <Link to="/contact" className="">
                  <i className="fas fa-angle-right me-2"></i> Contact Us
                </Link>
                <Link to="#" className="">
                  <i className="fas fa-angle-right me-2"></i> Returns
                </Link>
                <Link to="#" className="">
                  <i className="fas fa-angle-right me-2"></i> Order History
                </Link>
                <Link to="#" className="">
                  <i className="fas fa-angle-right me-2"></i> Site Map
                </Link>
                <Link to="#" className="">
                  <i className="fas fa-angle-right me-2"></i> Testimonials
                </Link>
                <Link to="#" className="">
                  <i className="fas fa-angle-right me-2"></i> My Account
                </Link>
                <Link to="#" className="">
                  <i className="fas fa-angle-right me-2"></i> Unsubscribe Notification
                </Link>
              </div>
            </div>

            {/* Information Links */}
            <div className="col-md-6 col-lg-6 col-xl-3">
              <div className="footer-item d-flex flex-column">
                <h4 className="text-primary mb-4">Information</h4>
                <Link to="#" className="">
                  <i className="fas fa-angle-right me-2"></i> About Us
                </Link>
                <Link to="#" className="">
                  <i className="fas fa-angle-right me-2"></i> Delivery Information
                </Link>
                <Link to="#" className="">
                  <i className="fas fa-angle-right me-2"></i> Privacy Policy
                </Link>
                <Link to="#" className="">
                  <i className="fas fa-angle-right me-2"></i> Terms & Conditions
                </Link>
                <Link to="#" className="">
                  <i className="fas fa-angle-right me-2"></i> Warranty
                </Link>
                <Link to="#" className="">
                  <i className="fas fa-angle-right me-2"></i> FAQ
                </Link>
                <Link to="#" className="">
                  <i className="fas fa-angle-right me-2"></i> Seller Login
                </Link>
              </div>
            </div>

            {/* Extras Links */}
            <div className="col-md-6 col-lg-6 col-xl-3">
              <div className="footer-item d-flex flex-column">
                <h4 className="text-primary mb-4">Extras</h4>
                <Link to="#" className="">
                  <i className="fas fa-angle-right me-2"></i> Brands
                </Link>
                <Link to="#" className="">
                  <i className="fas fa-angle-right me-2"></i> Gift Vouchers
                </Link>
                <Link to="#" className="">
                  <i className="fas fa-angle-right me-2"></i> Affiliates
                </Link>
                <Link to="#" className="">
                  <i className="fas fa-angle-right me-2"></i> Wishlist
                </Link>
                <Link to="#" className="">
                  <i className="fas fa-angle-right me-2"></i> Order History
                </Link>
                <Link to="#" className="">
                  <i className="fas fa-angle-right me-2"></i> Track Your Order
                </Link>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Copyright */}
      <div className="container-fluid copyright py-4">
        <div className="container">
          <div className="row g-4 align-items-center">
            <div className="col-md-6 text-center text-md-start mb-md-0">
              <span className="text-white">
                <Link to="/" className="border-bottom text-white">
                  <i className="fas fa-copyright text-light me-2"></i>Your Site Name
                </Link>
                , All right reserved.
              </span>
            </div>
            <div className="col-md-6 text-center text-md-end text-white">
              Designed By{' '}
              <a className="border-bottom text-white" href="https://htmlcodex.com">
                HTML Codex
              </a>
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default Footer;
