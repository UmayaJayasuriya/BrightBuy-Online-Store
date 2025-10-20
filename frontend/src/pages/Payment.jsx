/**
 * Payment Page Component
 * Credit/Debit Card Payment Form
 */
import React, { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import axios from 'axios';
import { useAuth } from '../context/AuthContext';
import Spinner from '../components/common/Spinner';
import './Payment.css';

const Payment = () => {
  const { user } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const orderData = location.state?.orderData;

  const [processing, setProcessing] = useState(false);
  const [cardData, setCardData] = useState({
    cardNumber: '',
    nameOnCard: '',
    expiryDate: '',
    cvv: ''
  });

  // Redirect if no order data
  React.useEffect(() => {
    if (!orderData) {
      navigate('/cart');
    }
  }, [orderData, navigate]);

  const handleInputChange = (e) => {
    let { name, value } = e.target;

    // Format card number with spaces
    if (name === 'cardNumber') {
      value = value.replace(/\s/g, '').replace(/(\d{4})/g, '$1 ').trim();
      if (value.length > 19) return; // Max 16 digits + 3 spaces
    }

    // Format expiry date as MM/YY
    if (name === 'expiryDate') {
      value = value.replace(/\D/g, '');
      if (value.length >= 2) {
        value = value.slice(0, 2) + '/' + value.slice(2, 4);
      }
      if (value.length > 5) return;
    }

    // Limit CVV to 3-4 digits
    if (name === 'cvv') {
      value = value.replace(/\D/g, '');
      if (value.length > 4) return;
    }

    setCardData({
      ...cardData,
      [name]: value
    });
  };

  const validateCardNumber = (number) => {
    const cleaned = number.replace(/\s/g, '');
    return cleaned.length === 16 && /^\d+$/.test(cleaned);
  };

  const validateExpiryDate = (date) => {
    if (!/^\d{2}\/\d{2}$/.test(date)) return false;
    
    const [month, year] = date.split('/').map(Number);
    if (month < 1 || month > 12) return false;
    
    const currentDate = new Date();
    const currentYear = currentDate.getFullYear() % 100;
    const currentMonth = currentDate.getMonth() + 1;
    
    if (year < currentYear) return false;
    if (year === currentYear && month < currentMonth) return false;
    
    return true;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Validate card details
    if (!validateCardNumber(cardData.cardNumber)) {
      alert('Please enter a valid 16-digit card number');
      return;
    }

    if (!validateExpiryDate(cardData.expiryDate)) {
      alert('Please enter a valid expiry date (MM/YY)');
      return;
    }

    if (cardData.cvv.length < 3) {
      alert('Please enter a valid CVV');
      return;
    }

    if (!cardData.nameOnCard.trim()) {
      alert('Please enter the name on card');
      return;
    }

    setProcessing(true);

    try {
      // Add card details to order data
      const orderWithCard = {
        ...orderData,
        card_details: {
          card_number: cardData.cardNumber,
          card_name: cardData.nameOnCard,
          expiry_date: cardData.expiryDate,
          cvv: cardData.cvv
        }
      };

      // Submit the order to backend
      const response = await axios.post('http://127.0.0.1:8020/orders/checkout', orderWithCard);
      
      if (response.data.order_id) {
        alert(`Payment successful! Your order #${response.data.order_id} has been placed.\nTotal: $${parseFloat(response.data.total_amount).toFixed(2)}`);
        navigate('/');
      }
    } catch (error) {
      console.error('Payment error:', error);
      alert(error.response?.data?.detail || 'Payment failed. Please try again.');
    } finally {
      setProcessing(false);
    }
  };

  if (!orderData) {
    return (
      <div className="container py-5">
        <Spinner />
      </div>
    );
  }

  return (
    <div className="payment-page">
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
          <h1 className="display-4 text-white mb-3 fw-bolder">Payment</h1>
          <p className="text-white fw-semibold">Secure Card Payment</p>
        </div>
      </div>

      <div className="container py-5">
        <div className="row justify-content-center">
          <div className="col-lg-6 col-md-8">
            <div className="card shadow-lg border-0">
              <div className="card-body p-5">
                <div className="text-center mb-4">
                  <div className="payment-icons mb-3">
                    <i className="fab fa-cc-visa fa-3x text-primary me-3"></i>
                    <i className="fab fa-cc-mastercard fa-3x text-primary me-3"></i>
                    <i className="fab fa-cc-amex fa-3x text-primary"></i>
                  </div>
                  <h3 className="mb-2">Enter Card Details</h3>
                  <p className="text-muted">Your payment information is secure</p>
                </div>

                <form onSubmit={handleSubmit}>
                  {/* Card Number */}
                  <div className="mb-4">
                    <label className="form-label">Card Number *</label>
                    <div className="input-group">
                      <span className="input-group-text">
                        <i className="fas fa-credit-card"></i>
                      </span>
                      <input
                        type="text"
                        className="form-control form-control-lg"
                        name="cardNumber"
                        value={cardData.cardNumber}
                        onChange={handleInputChange}
                        placeholder=""
                        required
                      />
                    </div>
                  </div>

                  {/* Name on Card */}
                  <div className="mb-4">
                    <label className="form-label">Name on Card *</label>
                    <div className="input-group">
                      <span className="input-group-text">
                        <i className="fas fa-user"></i>
                      </span>
                      <input
                        type="text"
                        className="form-control form-control-lg"
                        name="nameOnCard"
                        value={cardData.nameOnCard}
                        onChange={handleInputChange}
                        placeholder=""
                        style={{ textTransform: 'uppercase' }}
                        required
                      />
                    </div>
                  </div>

                  {/* Expiry Date and CVV */}
                  <div className="row">
                    <div className="col-md-6 mb-4">
                      <label className="form-label">Expiry Date *</label>
                      <div className="input-group">
                        <span className="input-group-text">
                          <i className="fas fa-calendar"></i>
                        </span>
                        <input
                          type="text"
                          className="form-control form-control-lg"
                          name="expiryDate"
                          value={cardData.expiryDate}
                          onChange={handleInputChange}
                          placeholder=""
                          required
                        />
                      </div>
                    </div>

                    <div className="col-md-6 mb-4">
                      <label className="form-label">CVV *</label>
                      <div className="input-group">
                        <span className="input-group-text">
                          <i className="fas fa-lock"></i>
                        </span>
                        <input
                          type="text"
                          className="form-control form-control-lg"
                          name="cvv"
                          value={cardData.cvv}
                          onChange={handleInputChange}
                          placeholder=""
                          required
                        />
                      </div>
                    </div>
                  </div>

                  {/* Order Amount */}
                  <div className="alert alert-info mb-4">
                    <div className="d-flex justify-content-between align-items-center">
                      <span><i className="fas fa-info-circle me-2"></i>Total Amount:</span>
                      <strong className="fs-4">${orderData.total_amount || '0.00'}</strong>
                    </div>
                  </div>

                  {/* Submit Button */}
                  <button
                    type="submit"
                    className="btn btn-primary btn-lg w-100 rounded-pill py-3"
                    disabled={processing}
                  >
                    {processing ? (
                      <>
                        <i className="fas fa-spinner fa-spin me-2"></i>
                        Processing Payment...
                      </>
                    ) : (
                      <>
                        <i className="fas fa-lock me-2"></i>
                        Pay ${orderData.total_amount || '0.00'}
                      </>
                    )}
                  </button>

                  {/* Security Notice */}
                  <div className="text-center mt-4">
                    <small className="text-muted">
                      <i className="fas fa-shield-alt me-1"></i>
                      Your payment information is encrypted and secure
                    </small>
                  </div>
                </form>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Payment;
