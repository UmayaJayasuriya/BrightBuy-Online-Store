/**
 * Checkout Page Component
 * Order checkout with billing and payment information
 */
import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import axios from 'axios';
import { useAuth } from '../context/AuthContext';
import './Checkout.css';

const Checkout = () => {
  const { user, isAuthenticated } = useAuth();
  const navigate = useNavigate();
  const [cartData, setCartData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState('');
  
  const [formData, setFormData] = useState({
    firstName: '',
    lastName: '',
    email: '',
    phone: '',
    address: '',
    city: '',
    state: '',
    zipCode: '',
    country: '',
    paymentMethod: 'card'
  });

  // Fetch cart from backend
  useEffect(() => {
    const fetchCart = async () => {
      if (!isAuthenticated || !user) {
        setLoading(false);
        return;
      }
      try {
        const response = await axios.get(`http://127.0.0.1:8020/cart/${user.user_id}`);
        setCartData(response.data);
      } catch (err) {
        console.error('Error fetching cart:', err);
        setError('Failed to load cart');
      } finally {
        setLoading(false);
      }
    };
    fetchCart();
  }, [isAuthenticated, user]);

  const handleInputChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!cartData || !cartData.cart_id) {
      setError('No cart found');
      return;
    }
    setSubmitting(true);
    setError('');
    try {
      // Call backend checkout endpoint
      const payload = {
        user_id: user?.user_id,
        cart_id: cartData.cart_id,
        payment_method: formData.paymentMethod
      };
      const response = await axios.post('/cart/checkout', payload);
      alert(response.data.message || 'Order placed successfully!');
      navigate('/');
    } catch (err) {
      console.error('Checkout error:', err);
      setError(err.response?.data?.detail || err.message || 'Checkout failed');
    } finally {
      setSubmitting(false);
    }
  };

  if (!isAuthenticated) {
    return (
      <div className="container py-5 text-center">
        <h3>Please login to checkout</h3>
        <Link to="/" className="btn btn-primary mt-3">Go to Home</Link>
      </div>
    );
  }

  if (loading) {
    return <div className="container py-5 text-center"><div className="spinner-border"></div></div>;
  }

  if (!cartData || !cartData.cart_items || cartData.cart_items.length === 0) {
    return (
      <div className="container py-5 text-center">
        <h3>Your cart is empty</h3>
        <Link to="/shop" className="btn btn-primary mt-3">
          Continue Shopping
        </Link>
      </div>
    );
  }

  return (
    <div className="checkout-page">
      <div className="container-fluid page-header py-5">
        <div className="container text-center py-5">
          <h1 className="display-4 text-white mb-3">Checkout</h1>
        </div>
      </div>

      <div className="container-fluid py-5">
        <div className="container py-5">
          <form onSubmit={handleSubmit}>
            <div className="row g-5">
              {/* Billing Details */}
              <div className="col-lg-8">
                <h4 className="mb-4">Billing Details</h4>
                <div className="row g-3">
                  <div className="col-md-6">
                    <label className="form-label">First Name *</label>
                    <input
                      type="text"
                      className="form-control"
                      name="firstName"
                      value={formData.firstName}
                      onChange={handleInputChange}
                      required
                    />
                  </div>
                  <div className="col-md-6">
                    <label className="form-label">Last Name *</label>
                    <input
                      type="text"
                      className="form-control"
                      name="lastName"
                      value={formData.lastName}
                      onChange={handleInputChange}
                      required
                    />
                  </div>
                  <div className="col-md-6">
                    <label className="form-label">Email *</label>
                    <input
                      type="email"
                      className="form-control"
                      name="email"
                      value={formData.email}
                      onChange={handleInputChange}
                      required
                    />
                  </div>
                  <div className="col-md-6">
                    <label className="form-label">Phone *</label>
                    <input
                      type="tel"
                      className="form-control"
                      name="phone"
                      value={formData.phone}
                      onChange={handleInputChange}
                      required
                    />
                  </div>
                  <div className="col-12">
                    <label className="form-label">Address *</label>
                    <input
                      type="text"
                      className="form-control"
                      name="address"
                      value={formData.address}
                      onChange={handleInputChange}
                      required
                    />
                  </div>
                  <div className="col-md-6">
                    <label className="form-label">City *</label>
                    <input
                      type="text"
                      className="form-control"
                      name="city"
                      value={formData.city}
                      onChange={handleInputChange}
                      required
                    />
                  </div>
                  <div className="col-md-6">
                    <label className="form-label">State/Province *</label>
                    <input
                      type="text"
                      className="form-control"
                      name="state"
                      value={formData.state}
                      onChange={handleInputChange}
                      required
                    />
                  </div>
                  <div className="col-md-6">
                    <label className="form-label">ZIP Code *</label>
                    <input
                      type="text"
                      className="form-control"
                      name="zipCode"
                      value={formData.zipCode}
                      onChange={handleInputChange}
                      required
                    />
                  </div>
                  <div className="col-md-6">
                    <label className="form-label">Country *</label>
                    <select
                      className="form-select"
                      name="country"
                      value={formData.country}
                      onChange={handleInputChange}
                      required
                    >
                      <option value="">Select Country</option>
                      <option value="USA">United States</option>
                      <option value="UK">United Kingdom</option>
                      <option value="Canada">Canada</option>
                      <option value="Australia">Australia</option>
                    </select>
                  </div>
                </div>

                {/* Payment Method */}
                <h4 className="mt-5 mb-4">Payment Method</h4>
                <div className="payment-methods">
                  <div className="form-check mb-3">
                    <input
                      className="form-check-input"
                      type="radio"
                      name="paymentMethod"
                      id="card"
                      value="card"
                      checked={formData.paymentMethod === 'card'}
                      onChange={handleInputChange}
                    />
                    <label className="form-check-label" htmlFor="card">
                      Credit/Debit Card
                    </label>
                  </div>
                  <div className="form-check mb-3">
                    <input
                      className="form-check-input"
                      type="radio"
                      name="paymentMethod"
                      id="paypal"
                      value="paypal"
                      checked={formData.paymentMethod === 'paypal'}
                      onChange={handleInputChange}
                    />
                    <label className="form-check-label" htmlFor="paypal">
                      PayPal
                    </label>
                  </div>
                  <div className="form-check">
                    <input
                      className="form-check-input"
                      type="radio"
                      name="paymentMethod"
                      id="cod"
                      value="cod"
                      checked={formData.paymentMethod === 'cod'}
                      onChange={handleInputChange}
                    />
                    <label className="form-check-label" htmlFor="cod">
                      Cash on Delivery
                    </label>
                  </div>
                </div>
              </div>

              {/* Order Summary */}
              <div className="col-lg-4">
                <div className="bg-light rounded p-4 sticky-top" style={{ top: '100px' }}>
                  <h4 className="mb-4">Your Order</h4>
                  {error && <div className="alert alert-danger">{error}</div>}
                  <div className="order-items">
                    {cartData && cartData.cart_items && cartData.cart_items.map((item) => (
                      <div key={item.cart_item_id} className="d-flex justify-content-between mb-3">
                        <div>
                          <h6 className="mb-0">{item.product_name}</h6>
                          <small className="text-muted">{item.variant_name} - Qty: {item.quantity}</small>
                        </div>
                        <strong>${(item.price * item.quantity).toFixed(2)}</strong>
                      </div>
                    ))}
                  </div>
                  <hr />
                  <div className="d-flex justify-content-between mb-2">
                    <span>Subtotal:</span>
                    <strong>${cartData ? Number(cartData.total_amount).toFixed(2) : '0.00'}</strong>
                  </div>
                  <div className="d-flex justify-content-between mb-2">
                    <span>Shipping:</span>
                    <strong className="text-success">Free</strong>
                  </div>
                  <div className="d-flex justify-content-between mb-3">
                    <span>Tax (10%):</span>
                    <strong>${cartData ? (Number(cartData.total_amount) * 0.1).toFixed(2) : '0.00'}</strong>
                  </div>
                  <hr />
                  <div className="d-flex justify-content-between mb-4">
                    <h5>Total:</h5>
                    <h5 className="text-primary">${cartData ? (Number(cartData.total_amount) * 1.1).toFixed(2) : '0.00'}</h5>
                  </div>
                  <button type="submit" className="btn btn-primary w-100 rounded-pill py-3" disabled={submitting || !cartData}>
                    {submitting ? 'Placing Order...' : 'Place Order'}
                  </button>
                </div>
              </div>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default Checkout;
