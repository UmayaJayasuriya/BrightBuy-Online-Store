/**
 * Footer Component
 * Site footer with contact info, newsletter signup, and links
 */
import React from 'react';
import { Link } from 'react-router-dom';
import './Footer.css';

const Footer = () => {
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
                  <p className="mb-2">123 Street Texas.USA</p>
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
                  <p className="mb-2">brightbuy@gmail.com</p>
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
        </div>
      </div>

      {/* Copyright */}
      <div className="container-fluid copyright py-4">
        <div className="container">
          <div className="row g-4 align-items-center">
            <div className="col-md-6 text-center text-md-start mb-md-0">
              <span className="text-white">
                <Link to="/" className="border-bottom text-white">
                  <i className="fas fa-copyright text-light me-2"></i>Brightbuy
                </Link>
                , All right reserved.
              </span>
            </div>
          
          </div>
        </div>
      </div>
    </>
  );
};

export default Footer;
