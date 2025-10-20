/**
 * Checkout Page Component
 * Order checkout with billing and payment information
 */
import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import axios from 'axios';
import { useAuth } from '../context/AuthContext';
import Spinner from '../components/common/Spinner';
import './Checkout.css';

const Checkout = () => {
  const { isAuthenticated, user } = useAuth();
  const navigate = useNavigate();
  
  const [cartData, setCartData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [processingOrder, setProcessingOrder] = useState(false);
  const [error, setError] = useState('');
  const [deliveryEstimate, setDeliveryEstimate] = useState(null);
  
  const [formData, setFormData] = useState({
    firstName: '',
    lastName: '',
    email: user?.email || '',
    phone: '',
    houseNumber: '',
    street: '',
    city: '',
    state: '',
    paymentMethod: 'card',
    deliveryMethod: 'home_delivery',
    addressId: user?.address_id || null
  });

  const [cities, setCities] = useState([]);

  // Fetch cart data and cities
  useEffect(() => {
    const fetchData = async () => {
      if (!isAuthenticated || !user) {
        setLoading(false);
        return;
      }

      try {
        setLoading(true);
        
        // Fetch cart
        const cartResponse = await axios.get(`http://127.0.0.1:8020/cart/${user.user_id}`);
        setCartData(cartResponse.data);
        
        // Fetch cities
        const citiesResponse = await axios.get('http://127.0.0.1:8020/locations/cities');
        setCities(citiesResponse.data);
      } catch (err) {
        console.error('Error fetching data:', err);
        setError('Failed to load data');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [isAuthenticated, user]);

  // Fetch delivery estimate when delivery method or city changes
  useEffect(() => {
    const fetchDeliveryEstimate = async () => {
      if (!user || !formData.deliveryMethod) return;

      try {
        let url = `http://127.0.0.1:8020/cart/delivery-estimate/${user.user_id}?delivery_method=${formData.deliveryMethod}`;
        
        if (formData.deliveryMethod === 'home_delivery' && formData.city) {
          url += `&city=${encodeURIComponent(formData.city)}`;
        }

        console.log('Fetching delivery estimate from:', url);
        const response = await axios.get(url);
        console.log('Delivery estimate response:', response.data);
        setDeliveryEstimate(response.data);
      } catch (err) {
        console.error('Error fetching delivery estimate:', err);
        setDeliveryEstimate(null);
      }
    };

    fetchDeliveryEstimate();
  }, [user, formData.deliveryMethod, formData.city]);

  const handleInputChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!user) {
      alert('Please login to place an order');
      return;
    }

    // Validate delivery method and address
    if (formData.deliveryMethod === 'home_delivery') {
      if (!formData.addressId && (!formData.houseNumber || !formData.street || !formData.city || !formData.state)) {
        alert('Please fill in all address fields for home delivery');
        return;
      }
    }

    // Prepare order data
    const orderData = {
      user_id: user.user_id,
      payment_method: formData.paymentMethod,
      delivery_method: formData.deliveryMethod,
      address_id: null,
      address_details: null,
      total_amount: cartData.total_amount
    };

    // If home delivery, include address
    if (formData.deliveryMethod === 'home_delivery') {
      if (formData.addressId) {
        orderData.address_id = formData.addressId;
      } else {
        // Create new address
        orderData.address_details = {
          house_number: parseInt(formData.houseNumber),
          street: formData.street,
          city: formData.city,
          state: formData.state
        };
      }
    }

    // If card payment, navigate to payment page
    if (formData.paymentMethod === 'card') {
      navigate('/payment', { state: { orderData } });
      return;
    }

    // For COD, process order directly
    setProcessingOrder(true);
    try {
      const response = await axios.post('http://127.0.0.1:8020/orders/checkout', orderData);

      const order = response.data;
      console.log('Order created:', order);

      // Show success message
      const deliveryMsg = formData.deliveryMethod === 'home_delivery' ? 'Home Delivery' : 'Store Pickup';
      
      alert(`Order #${order.order_id} placed successfully!\nTotal: $${parseFloat(order.total_amount).toFixed(2)}\nPayment: Cash on Delivery\nDelivery: ${deliveryMsg}`);
      
      // Navigate to home page
      navigate(`/`);
      
    } catch (err) {
      console.error('Error creating order:', err);
      alert(err.response?.data?.detail || 'Failed to place order. Please try again.');
    } finally {
      setProcessingOrder(false);
    }
  };

  // Redirect if not logged in
  if (!isAuthenticated) {
    return (
      <div className="checkout-page">
        <div className="container py-5">
          <div className="text-center">
            <i className="fas fa-lock fa-5x text-muted mb-4"></i>
            <h3>Please Login to Checkout</h3>
            <p className="text-muted mb-4">You need to be logged in to place an order.</p>
            <button onClick={() => navigate('/')} className="btn btn-primary rounded-pill py-3 px-5">
              Go to Login
            </button>
          </div>
        </div>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="container py-5">
        <Spinner />
      </div>
    );
  }

  if (!cartData || !cartData.cart_items || cartData.cart_items.length === 0) {
    return (
      <div className="checkout-page">
        <div className="container py-5 text-center">
          <i className="fas fa-shopping-cart fa-5x text-muted mb-4"></i>
          <h3>Your cart is empty</h3>
          <p className="text-muted mb-4">Add some products before checking out.</p>
          <Link to="/shop" className="btn btn-primary rounded-pill py-3 px-5">
            Continue Shopping
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="checkout-page">
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
          backgroundColor: 'rgba(0,0,0,0.45)',
          zIndex: 1
        }}></div>
        <div className="container text-center py-5" style={{ position: 'relative', zIndex: 2 }}>
          <h1 className="display-4 text-white mb-3 fw-bolder">Checkout</h1>
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
                  {formData.deliveryMethod === 'home_delivery' && (
                    <>
                      <div className="col-md-6">
                        <label className="form-label">House Number *</label>
                        <input
                          type="number"
                          className="form-control"
                          name="houseNumber"
                          value={formData.houseNumber}
                          onChange={handleInputChange}
                          placeholder="e.g., 123"
                          required={formData.deliveryMethod === 'home_delivery'}
                        />
                      </div>
                      <div className="col-md-6">
                        <label className="form-label">Street *</label>
                        <input
                          type="text"
                          className="form-control"
                          name="street"
                          value={formData.street}
                          onChange={handleInputChange}
                          placeholder="e.g., Main Street"
                          required={formData.deliveryMethod === 'home_delivery'}
                        />
                      </div>
                      <div className="col-md-6">
                        <label className="form-label">City *</label>
                        <select
                          className="form-select"
                          name="city"
                          value={formData.city}
                          onChange={handleInputChange}
                          required={formData.deliveryMethod === 'home_delivery'}
                        >
                          <option value="">Select City</option>
                          {cities.map((city) => (
                            <option key={city.city_id} value={city.city}>
                              {city.city} {city.Is_main_city ? '(Main City)' : ''}
                            </option>
                          ))}
                        </select>
                      </div>
                      <div className="col-md-6">
                        <label className="form-label">State *</label>
                        <input
                          type="text"
                          className="form-control"
                          name="state"
                          value={formData.state}
                          onChange={handleInputChange}
                          placeholder="e.g., California"
                          required={formData.deliveryMethod === 'home_delivery'}
                        />
                      </div>
                    </>
                  )}
                </div>

                {/* Delivery Method */}
                <h4 className="mt-5 mb-4">Delivery Method</h4>
                <div className="delivery-methods mb-4">
                  <div className="form-check mb-3 p-3 border rounded">
                    <input
                      className="form-check-input"
                      type="radio"
                      name="deliveryMethod"
                      id="home_delivery"
                      value="home_delivery"
                      checked={formData.deliveryMethod === 'home_delivery'}
                      onChange={handleInputChange}
                    />
                    <label className="form-check-label" htmlFor="home_delivery">
                      <strong>Home Delivery</strong>
                      <br />
                      {formData.deliveryMethod === 'home_delivery' && deliveryEstimate && deliveryEstimate.estimated_days !== null && deliveryEstimate.estimated_days !== undefined ? (
                        // Exact estimate when city is selected
                        <small className="text-muted">
                          <strong className="text-primary">Estimated: {deliveryEstimate.estimated_days} days</strong>
                          {deliveryEstimate.has_low_stock && (
                            <span className="text-warning ms-2">
                              <i className="fas fa-exclamation-triangle"></i> Low stock items
                            </span>
                          )}
                        </small>
                      ) : formData.deliveryMethod === 'home_delivery' && deliveryEstimate && deliveryEstimate.main_city_estimate ? (
                        // Range estimate when no city selected but we have stock info
                        <small className="text-muted">
                          <span className="text-primary">Main cities: {deliveryEstimate.main_city_estimate} days</span>
                          <br />
                          <span className="text-primary">Other cities: {deliveryEstimate.other_city_estimate} days</span>
                          {deliveryEstimate.has_low_stock && (
                            <span className="text-warning d-block mt-1">
                              <i className="fas fa-exclamation-triangle"></i> Includes 3 extra days for low stock items
                            </span>
                          )}
                        </small>
                      ) : (
                        // Default message while loading
                        <small className="text-muted">
                          Main cities: 5 days<br />
                          Other cities: 7 days
                        </small>
                      )}
                    </label>
                  </div>
                  <div className="form-check p-3 border rounded">
                    <input
                      className="form-check-input"
                      type="radio"
                      name="deliveryMethod"
                      id="store_pickup"
                      value="store_pickup"
                      checked={formData.deliveryMethod === 'store_pickup'}
                      onChange={handleInputChange}
                    />
                    <label className="form-check-label" htmlFor="store_pickup">
                      <strong>Store Pickup</strong>
                      <br />
                      {formData.deliveryMethod === 'store_pickup' && deliveryEstimate && deliveryEstimate.estimated_days !== null && deliveryEstimate.estimated_days !== undefined ? (
                        <small className="text-muted">
                          <strong className="text-primary">Ready in {deliveryEstimate.estimated_days} business days</strong>
                        </small>
                      ) : (
                        <small className="text-muted">Ready for pickup in 2 business days</small>
                      )}
                    </label>
                  </div>
                </div>

                {formData.deliveryMethod === 'home_delivery' && deliveryEstimate && deliveryEstimate.estimated_days && (
                  <div className={`alert ${deliveryEstimate.has_low_stock ? 'alert-warning' : 'alert-info'}`}>
                    <i className={`fas ${deliveryEstimate.has_low_stock ? 'fa-exclamation-triangle' : 'fa-info-circle'} me-2`}></i>
                    {deliveryEstimate.has_low_stock ? (
                      <>
                        Some items in your cart have low stock. Your order will be delivered in approximately <strong>{deliveryEstimate.estimated_days} days</strong> {deliveryEstimate.is_main_city ? '(main city)' : '(other city)'}.
                      </>
                    ) : (
                      <>
                        Your order will be delivered in approximately <strong>{deliveryEstimate.estimated_days} days</strong> {deliveryEstimate.is_main_city ? '(main city)' : '(other city)'}.
                      </>
                    )}
                  </div>
                )}
                
                {formData.deliveryMethod === 'home_delivery' && !formData.city && deliveryEstimate && deliveryEstimate.has_low_stock !== undefined && (
                  <div className={`alert ${deliveryEstimate.has_low_stock ? 'alert-warning' : 'alert-info'}`}>
                    <i className={`fas ${deliveryEstimate.has_low_stock ? 'fa-exclamation-triangle' : 'fa-info-circle'} me-2`}></i>
                    {deliveryEstimate.has_low_stock ? (
                      <>
                        <strong>Low stock detected!</strong> Please select your city to see the exact delivery time.
                        Expected: {deliveryEstimate.main_city_estimate} days (main cities) or {deliveryEstimate.other_city_estimate} days (other cities).
                      </>
                    ) : (
                      <>
                        Please select your city to see the exact delivery time.
                      </>
                    )}
                  </div>
                )}

                {/* Payment Method */}
                <h4 className="mt-5 mb-4">Payment Method</h4>
                <div className="payment-methods">
                  <div className="form-check mb-3 p-3 border rounded">
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
                      <strong>Credit/Debit Card</strong>
                      <br />
                      <small className="text-muted">Payment will be processed immediately</small>
                    </label>
                  </div>
                  <div className="form-check p-3 border rounded">
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
                      <strong>Cash on Delivery</strong>
                      <br />
                      <small className="text-muted">Pay when you receive your order</small>
                    </label>
                  </div>
                </div>
              </div>

              {/* Order Summary */}
              <div className="col-lg-4">
                <div className="bg-light rounded p-4 sticky-top" style={{ top: '100px' }}>
                  <h4 className="mb-4">Your Order</h4>
                  <div className="order-items" style={{ maxHeight: '300px', overflowY: 'auto' }}>
                    {cartData.cart_items.map((item) => (
                      <div key={item.cart_item_id} className="d-flex justify-content-between mb-3 pb-3 border-bottom">
                        <div className="d-flex align-items-center">
                          <img
                            src={`/img/Variants/${item.variant_id}.jpg`}
                            alt={item.variant_name}
                            style={{ width: '50px', height: '50px', objectFit: 'cover', backgroundColor: '#f8f9fa' }}
                            className="rounded me-3"
                            onError={(e) => {
                              // Try different image formats
                              if (e.target.src.includes('.jpg')) {
                                e.target.src = `/img/Variants/${item.variant_id}.png`;
                              } else if (e.target.src.includes('.png')) {
                                e.target.src = `/img/Variants/${item.variant_id}.jpeg`;
                              } else if (e.target.src.includes('.jpeg')) {
                                e.target.src = `/img/Variants/${item.variant_id}.webp`;
                              } else if (e.target.src.includes('.webp')) {
                                e.target.src = `/img/Variants/${item.variant_id}.avif`;
                              } else {
                                // Final fallback to product image
                                e.target.src = `/img/product-${item.product_id}.png`;
                              }
                            }}
                          />
                          <div>
                            <h6 className="mb-0" style={{ fontSize: '14px' }}>{item.product_name}</h6>
                            <small className="text-muted">{item.variant_name}</small>
                            <br />
                            <small className="text-muted">Qty: {item.quantity}</small>
                          </div>
                        </div>
                        <div className="text-end">
                          <strong>${(parseFloat(item.price) * item.quantity).toFixed(2)}</strong>
                        </div>
                      </div>
                    ))}
                  </div>
                  <hr />
                  <div className="d-flex justify-content-between mb-2">
                    <span>Subtotal:</span>
                    <strong>${parseFloat(cartData.total_amount || 0).toFixed(2)}</strong>
                  </div>
                  <div className="d-flex justify-content-between mb-3">
                    <span>Shipping:</span>
                    <strong className="text-success">Free</strong>
                  </div>
                  <hr />
                  <div className="d-flex justify-content-between mb-4">
                    <h5>Total:</h5>
                    <h5 className="text-primary">${parseFloat(cartData.total_amount || 0).toFixed(2)}</h5>
                  </div>
                  <button 
                    type="submit" 
                    className="btn btn-primary w-100 rounded-pill py-3"
                    disabled={processingOrder}
                  >
                    {processingOrder ? (
                      <>
                        <i className="fas fa-spinner fa-spin me-2"></i>
                        Processing...
                      </>
                    ) : formData.paymentMethod === 'card' ? (
                      <>
                        <i className="fas fa-credit-card me-2"></i>
                        Proceed to Payment
                      </>
                    ) : (
                      <>
                        <i className="fas fa-check me-2"></i>
                        Place Order
                      </>
                    )}
                  </button>
                  <Link to="/cart" className="btn btn-outline-secondary w-100 rounded-pill py-2 mt-2">
                    <i className="fas fa-arrow-left me-2"></i>
                    Back to Cart
                  </Link>
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
