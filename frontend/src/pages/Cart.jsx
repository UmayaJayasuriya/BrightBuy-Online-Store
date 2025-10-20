/**
 * Cart Page Component
 * Shopping cart with item management from database
 */
import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import axios from 'axios';
import { useAuth } from '../context/AuthContext';
import Spinner from '../components/common/Spinner';
import './Cart.css';

const Cart = () => {
  const { isAuthenticated, user } = useAuth();
  const navigate = useNavigate();
  const [cartData, setCartData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  // Fetch cart data from backend
  useEffect(() => {
    const fetchCart = async () => {
      if (!isAuthenticated || !user) {
        setLoading(false);
        return;
      }

      try {
        setLoading(true);
        const response = await axios.get(`http://127.0.0.1:8020/cart/${user.user_id}`);
        setCartData(response.data);
        console.log('Cart data:', response.data);
      } catch (err) {
        console.error('Error fetching cart:', err);
        setError('Failed to load cart');
      } finally {
        setLoading(false);
      }
    };

    fetchCart();
  }, [isAuthenticated, user]);

  const handleQuantityChange = async (cartItemId, newQuantity) => {
    if (newQuantity < 1) return;

    try {
      await axios.put(`http://127.0.0.1:8020/cart/update/${cartItemId}?quantity=${newQuantity}`);
      
      // Refresh cart
      const response = await axios.get(`http://127.0.0.1:8020/cart/${user.user_id}`);
      setCartData(response.data);
    } catch (err) {
      console.error('Error updating quantity:', err);
      alert('Failed to update quantity');
    }
  };

  const handleRemoveItem = async (cartItemId) => {
    if (!window.confirm('Remove this item from cart?')) return;

    try {
      await axios.delete(`http://127.0.0.1:8020/cart/remove/${cartItemId}`);
      
      // Refresh cart
      const response = await axios.get(`http://127.0.0.1:8020/cart/${user.user_id}`);
      setCartData(response.data);
    } catch (err) {
      console.error('Error removing item:', err);
      alert('Failed to remove item');
    }
  };

  const handleClearCart = async () => {
    if (!window.confirm('Clear all items from cart?')) return;

    try {
      await axios.delete(`http://127.0.0.1:8020/cart/clear/${user.user_id}`);
      
      // Refresh cart
      const response = await axios.get(`http://127.0.0.1:8020/cart/${user.user_id}`);
      setCartData(response.data);
    } catch (err) {
      console.error('Error clearing cart:', err);
      alert('Failed to clear cart');
    }
  };

  // Redirect if not logged in
  if (!isAuthenticated) {
    return (
      <div className="cart-page">
        <div className="container py-5">
          <div className="text-center">
            <i className="fas fa-lock fa-5x text-muted mb-4"></i>
            <h3>Please Login to View Cart</h3>
            <p className="text-muted mb-4">You need to be logged in to access your shopping cart.</p>
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
      <div className="cart-page">
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
            <h1 className="display-4 text-white mb-3" style={{ fontWeight: '700' }}>Shopping Cart</h1>
          </div>
        </div>
        <div className="container py-5">
          <div className="text-center">
            <i className="fas fa-shopping-cart fa-5x text-muted mb-4"></i>
            <h3>Your cart is empty</h3>
            <p className="text-muted mb-4">Add some products to get started!</p>
            <Link to="/shop" className="btn btn-primary rounded-pill py-3 px-5">
              Continue Shopping
            </Link>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="cart-page">
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
          <h1 className="display-4 text-white mb-3" style={{ fontWeight: '700' }}>Shopping Cart</h1>
          <nav aria-label="breadcrumb">
            <ol className="breadcrumb justify-content-center mb-0">
              <li className="breadcrumb-item"><Link to="/">Home</Link></li>
              <li className="breadcrumb-item active text-white">Cart</li>
            </ol>
          </nav>
        </div>
      </div>

      {/* Cart Content */}
      <div className="container-fluid py-5">
        <div className="container py-5">
          <div className="row g-5">
            {/* Cart Items */}
            <div className="col-lg-8">
              <div className="table-responsive">
                <table className="table table-borderless">
                  <thead className="bg-light">
                    <tr>
                      <th>Product</th>
                      <th>Price</th>
                      <th>Quantity</th>
                      <th>Total</th>
                      <th>Remove</th>
                    </tr>
                  </thead>
                  <tbody>
                    {cartData.cart_items.map((item) => (
                      <tr key={item.cart_item_id} className="border-bottom">
                        <td>
                          <div className="d-flex align-items-center">
                            <img
                              src={`/img/Variants/${item.variant_id}.jpg`}
                              alt={item.variant_name}
                              style={{ width: '80px', height: '80px', objectFit: 'cover', backgroundColor: '#f8f9fa' }}
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
                              <h6 className="mb-1">{item.product_name}</h6>
                              <small className="text-muted">{item.variant_name}</small>
                            </div>
                          </div>
                        </td>
                        <td className="align-middle">
                          <strong>${parseFloat(item.price).toFixed(2)}</strong>
                        </td>
                        <td className="align-middle">
                          <div className="input-group" style={{ width: '130px' }}>
                            <button
                              className="btn btn-sm btn-outline-secondary"
                              onClick={() => handleQuantityChange(item.cart_item_id, item.quantity - 1)}
                            >
                              <i className="fas fa-minus"></i>
                            </button>
                            <input
                              type="number"
                              className="form-control form-control-sm text-center"
                              value={item.quantity}
                              onChange={(e) =>
                                handleQuantityChange(item.cart_item_id, parseInt(e.target.value) || 1)
                              }
                              min="1"
                            />
                            <button
                              className="btn btn-sm btn-outline-secondary"
                              onClick={() => handleQuantityChange(item.cart_item_id, item.quantity + 1)}
                            >
                              <i className="fas fa-plus"></i>
                            </button>
                          </div>
                        </td>
                        <td className="align-middle">
                          <strong className="text-primary">
                            ${(parseFloat(item.price) * item.quantity).toFixed(2)}
                          </strong>
                        </td>
                        <td className="align-middle">
                          <button
                            className="btn btn-sm btn-danger rounded-circle"
                            onClick={() => handleRemoveItem(item.cart_item_id)}
                          >
                            <i className="fas fa-times"></i>
                          </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>

              <div className="d-flex justify-content-between mt-4">
                <Link to="/shop" className="btn btn-outline-primary">
                  <i className="fas fa-arrow-left me-2"></i>
                  Continue Shopping
                </Link>
                <button onClick={handleClearCart} className="btn btn-outline-danger">
                  <i className="fas fa-trash me-2"></i>
                  Clear Cart
                </button>
              </div>
            </div>

            {/* Cart Summary */}
            <div className="col-lg-4">
              <div className="bg-light rounded p-4">
                <h4 className="mb-4">Cart Summary</h4>
                
                <div className="d-flex justify-content-between mb-3">
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

                <Link
                  to="/checkout"
                  className="btn btn-primary w-100 rounded-pill py-3"
                >
                  Proceed to Checkout
                </Link>
              </div>

              {/* Payment Methods */}
              <div className="mt-4 text-center">
                <p className="text-muted mb-2">We Accept:</p>
                <div className="d-flex justify-content-center gap-2">
                  <i className="fab fa-cc-visa fa-2x text-primary"></i>
                  <i className="fab fa-cc-mastercard fa-2x text-primary"></i>
                  <i className="fab fa-cc-paypal fa-2x text-primary"></i>
                  <i className="fab fa-cc-amex fa-2x text-primary"></i>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Cart;
