/**
 * Topbar Component
 * Displays top navigation with help links, phone number, currency, language, and dashboard options
 */
import React from 'react';
import './Topbar.css';

const Topbar = () => {
  return (
    <div className="container-fluid px-5 d-none border-bottom d-lg-block">
      <div className="row gx-0 align-items-center">
        {/* Left section - Help links */}
        <div className="col-lg-4 text-center text-lg-start mb-lg-0">
          <div className="d-inline-flex align-items-center" style={{ height: '45px' }}>
            <a href="#help" className="text-muted me-2"> Help</a>
            <small> / </small>
            <a href="#support" className="text-muted mx-2"> Support</a>
            <small> / </small>
            <a href="#contact" className="text-muted ms-2"> Contact</a>
          </div>
        </div>

        {/* Center section - Phone number */}
        <div className="col-lg-4 text-center d-flex align-items-center justify-content-center">
          <small className="text-dark">Call Us:</small>
          <a href="tel:+0121234567890" className="text-muted">(+012) 1234 567890</a>
        </div>

        {/* Right section - Currency, Language, Dashboard */}
        <div className="col-lg-4 text-center text-lg-end">
          <div className="d-inline-flex align-items-center" style={{ height: '45px' }}>
            {/* Currency Dropdown */}
            <div className="dropdown">
              <a 
                href="#currency" 
                className="dropdown-toggle text-muted me-2" 
                data-bs-toggle="dropdown"
              >
                <small> USD</small>
              </a>
              <div className="dropdown-menu rounded">
                <a href="#euro" className="dropdown-item"> Euro</a>
                <a href="#dollar" className="dropdown-item"> Dollar</a>
              </div>
            </div>

            {/* Language Dropdown */}
            <div className="dropdown">
              <a 
                href="#language" 
                className="dropdown-toggle text-muted mx-2" 
                data-bs-toggle="dropdown"
              >
                <small> English</small>
              </a>
              <div className="dropdown-menu rounded">
                <a href="#english" className="dropdown-item"> English</a>
                <a href="#turkish" className="dropdown-item"> Turkish</a>
                <a href="#spanish" className="dropdown-item"> Spanish</a>
                <a href="#italian" className="dropdown-item"> Italian</a>
              </div>
            </div>

            {/* Dashboard Dropdown */}
            <div className="dropdown">
              <a 
                href="#dashboard" 
                className="dropdown-toggle text-muted ms-2" 
                data-bs-toggle="dropdown"
              >
                <small>
                  <i className="fa-solid fa-house me-2"></i> My Dashboard
                </small>
              </a>
              <div className="dropdown-menu rounded">
                <a href="#login" className="dropdown-item"> Login</a>
                <a href="#wishlist" className="dropdown-item"> Wishlist</a>
                <a href="#card" className="dropdown-item"> My Card</a>
                <a href="#notifications" className="dropdown-item"> Notifications</a>
                <a href="#settings" className="dropdown-item"> Account Settings</a>
                <a href="#account" className="dropdown-item"> My Account</a>
                <a href="#logout" className="dropdown-item"> Log Out</a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Topbar;
