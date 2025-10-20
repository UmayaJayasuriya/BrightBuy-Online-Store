/**
 * Contact Page Component
 * Contact form and company information
 */
import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import './Contact.css';

const Contact = () => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    subject: '',
    message: ''
  });

  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitStatus, setSubmitStatus] = useState({ type: '', message: '' });

  const handleInputChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);
    setSubmitStatus({ type: '', message: '' });

    try {
      console.log('📤 Submitting contact form:', {
        customer_name: formData.name,
        email: formData.email,
        subject_name: formData.subject,
        message: formData.message
      });

      const response = await axios.post('http://127.0.0.1:8020/contact/', {
        customer_name: formData.name,
        email: formData.email,
        subject_name: formData.subject,
        message: formData.message
      });

      console.log('✅ Response:', response);

      if (response.status === 201) {
        setSubmitStatus({
          type: 'success',
          message: 'Thank you for your message! We will get back to you soon.'
        });
        setFormData({ name: '', email: '', subject: '', message: '' });
      }
    } catch (error) {
      console.error('❌ Error submitting contact form:', error);
      console.error('Error response:', error.response);
      console.error('Error details:', error.response?.data);
      
      let errorMessage = 'Failed to send message. Please try again later.';
      if (error.response?.data?.detail) {
        errorMessage = error.response.data.detail;
      } else if (error.message) {
        errorMessage = `Error: ${error.message}`;
      }
      
      setSubmitStatus({
        type: 'error',
        message: errorMessage
      });
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="contact-page">
      {/* Page Header */}
      <div className="container-fluid page-header py-5" style={{
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
          <h1 className="display-4 text-white mb-3" style={{ fontWeight: '700' }}>Contact Us</h1>
          <nav aria-label="breadcrumb">
            <ol className="breadcrumb justify-content-center mb-0">
              <li className="breadcrumb-item"><Link to="/">Home</Link></li>
              <li className="breadcrumb-item active text-white">Contact</li>
            </ol>
          </nav>
        </div>
      </div>

      {/* Contact Info Cards */}
      <div className="container-fluid py-5">
        <div className="container py-5">
          <div className="row g-4 mb-5">
            <div className="col-md-6 col-lg-3">
              <div className="contact-info-card text-center p-4 rounded">
                <div className="icon-circle mb-3">
                  <i className="fas fa-map-marker-alt fa-2x text-primary"></i>
                </div>
                <h5>Address</h5>
                <p className="text-muted">123 Street, Texas, USA</p>
              </div>
            </div>
            <div className="col-md-6 col-lg-3">
              <div className="contact-info-card text-center p-4 rounded">
                <div className="icon-circle mb-3">
                  <i className="fas fa-envelope fa-2x text-primary"></i>
                </div>
                <h5>Email</h5>
                <p className="text-muted">brightbuy@gmail.com</p>
              </div>
            </div>
            <div className="col-md-6 col-lg-3">
              <div className="contact-info-card text-center p-4 rounded">
                <div className="icon-circle mb-3">
                  <i className="fas fa-phone-alt fa-2x text-primary"></i>
                </div>
                <h5>Phone</h5>
                <p className="text-muted">(+012) 3456 7890</p>
              </div>
            </div>
            <div className="col-md-6 col-lg-3">
              <div className="contact-info-card text-center p-4 rounded">
                <div className="icon-circle mb-3">
                  <i className="fas fa-clock fa-2x text-primary"></i>
                </div>
                <h5>Working Hours</h5>
                <p className="text-muted">Mon - Fri: 9AM - 6PM</p>
              </div>
            </div>
          </div>

          {/* Contact Form */}
          <div className="row g-5">
            <div className="col-lg-6">
              <h2 className="mb-4">Get In Touch</h2>
              <p className="mb-4">
                Have a question or feedback? Fill out the form below and we'll get back to you as soon as possible.
              </p>
              
              {/* Success/Error Messages */}
              {submitStatus.message && (
                <div className={`alert ${submitStatus.type === 'success' ? 'alert-success' : 'alert-danger'} alert-dismissible fade show`} role="alert">
                  {submitStatus.message}
                  <button 
                    type="button" 
                    className="btn-close" 
                    onClick={() => setSubmitStatus({ type: '', message: '' })}
                    aria-label="Close"
                  ></button>
                </div>
              )}

              <form onSubmit={handleSubmit}>
                <div className="row g-3">
                  <div className="col-md-6">
                    <div className="form-floating">
                      <input
                        type="text"
                        className="form-control"
                        id="name"
                        name="name"
                        placeholder="Your Name"
                        value={formData.name}
                        onChange={handleInputChange}
                        maxLength={100}
                        required
                      />
                      <label htmlFor="name">Your Name</label>
                    </div>
                  </div>
                  <div className="col-md-6">
                    <div className="form-floating">
                      <input
                        type="email"
                        className="form-control"
                        id="email"
                        name="email"
                        placeholder="Your Email"
                        value={formData.email}
                        onChange={handleInputChange}
                        maxLength={100}
                        required
                      />
                      <label htmlFor="email">Your Email</label>
                    </div>
                  </div>
                  <div className="col-12">
                    <div className="form-floating">
                      <input
                        type="text"
                        className="form-control"
                        id="subject"
                        name="subject"
                        placeholder="Subject"
                        value={formData.subject}
                        onChange={handleInputChange}
                        maxLength={200}
                        required
                      />
                      <label htmlFor="subject">Subject</label>
                    </div>
                  </div>
                  <div className="col-12">
                    <div className="form-floating">
                      <textarea
                        className="form-control"
                        id="message"
                        name="message"
                        placeholder="Message"
                        style={{ height: '150px' }}
                        value={formData.message}
                        onChange={handleInputChange}
                        maxLength={2000}
                        required
                      ></textarea>
                      <label htmlFor="message">Message</label>
                    </div>
                  </div>
                  <div className="col-12">
                    <button 
                      className="btn btn-primary rounded-pill py-3 px-5" 
                      type="submit"
                      disabled={isSubmitting}
                    >
                      {isSubmitting ? 'Sending...' : 'Send Message'}
                    </button>
                  </div>
                </div>
              </form>
            </div>

            {/* Map */}
            <div className="col-lg-6">
              <h2 className="mb-4">Our Location</h2>
              <div className="map-container rounded overflow-hidden">
                <iframe
                  title="Google Map"
                  src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d107194.85104867952!2d-96.87195344453126!3d32.82058395937124!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x864e992e2d4d4f59%3A0x93c6c11bac9c8e4a!2sDallas%2C%20TX!5e0!3m2!1sen!2sus!4v1728568890123!5m2!1sen!2sus"
                  width="100%"
                  height="450"
                  style={{ border: 0 }}
                  allowFullScreen=""
                  loading="lazy"
                  referrerPolicy="no-referrer-when-downgrade"
                ></iframe>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Contact;
