/**
 * Cart Page Component
 * Shopping cart with item management
 */
import React from 'react';
import { Link } from 'react-router-dom';
import { useCart } from '../context/CartContext';
import './Cart.css';

const Cart = () => {
  const { cartItems, removeFromCart, updateQuantity, getCartTotal } = useCart();

  const handleQuantityChange = (productId, newQuantity) => {
    if (newQuantity >= 1) {
      updateQuantity(productId, newQuantity);
    }
  };

  if (cartItems.length === 0) {
    return (
      <div className="cart-page">
        <div className="container-fluid page-header py-5" style={{
          backgroundImage: 'url(/img/carousel-1.jpg)',
          backgroundSize: '200%',
          backgroundPosition: 'center 15%',
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
        backgroundImage: 'url(/img/carousel-1.jpg)',
        backgroundSize: '200%',
        backgroundPosition: 'center 15%',
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
                    {cartItems.map((item) => (
                      <tr key={item.id} className="border-bottom">
                        <td>
                          <div className="d-flex align-items-center">
                            <img
                              src={item.image}
                              alt={item.name}
                              style={{ width: '80px', height: '80px', objectFit: 'cover' }}
                              className="rounded me-3"
                            />
                            <div>
                              <h6 className="mb-1">{item.name}</h6>
                              <small className="text-muted">{item.category}</small>
                            </div>
                          </div>
                        </td>
                        <td className="align-middle">
                          <strong>${item.price.toFixed(2)}</strong>
                        </td>
                        <td className="align-middle">
                          <div className="input-group" style={{ width: '130px' }}>
                            <button
                              className="btn btn-sm btn-outline-secondary"
                              onClick={() => handleQuantityChange(item.id, item.quantity - 1)}
                            >
                              <i className="fas fa-minus"></i>
                            </button>
                            <input
                              type="number"
                              className="form-control form-control-sm text-center"
                              value={item.quantity}
                              onChange={(e) =>
                                handleQuantityChange(item.id, parseInt(e.target.value) || 1)
                              }
                              min="1"
                            />
                            <button
                              className="btn btn-sm btn-outline-secondary"
                              onClick={() => handleQuantityChange(item.id, item.quantity + 1)}
                            >
                              <i className="fas fa-plus"></i>
                            </button>
                          </div>
                        </td>
                        <td className="align-middle">
                          <strong className="text-primary">
                            ${(item.price * item.quantity).toFixed(2)}
                          </strong>
                        </td>
                        <td className="align-middle">
                          <button
                            className="btn btn-sm btn-danger rounded-circle"
                            onClick={() => removeFromCart(item.id)}
                            title="Remove item"
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
              </div>
            </div>

            {/* Cart Summary */}
            <div className="col-lg-4">
              <div className="bg-light rounded p-4">
                <h4 className="mb-4">Cart Summary</h4>
                
                <div className="d-flex justify-content-between mb-3">
                  <span>Subtotal:</span>
                  <strong>${getCartTotal().toFixed(2)}</strong>
                </div>
                
                <div className="d-flex justify-content-between mb-3">
                  <span>Shipping:</span>
                  <strong className="text-success">Free</strong>
                </div>
                
                <div className="d-flex justify-content-between mb-3">
                  <span>Tax (10%):</span>
                  <strong>${(getCartTotal() * 0.1).toFixed(2)}</strong>
                </div>
                
                <hr />
                
                <div className="d-flex justify-content-between mb-4">
                  <h5>Total:</h5>
                  <h5 className="text-primary">${(getCartTotal() * 1.1).toFixed(2)}</h5>
                </div>

                {/* Coupon Code */}
                <div className="mb-4">
                  <label className="form-label">Coupon Code</label>
                  <div className="input-group">
                    <input
                      type="text"
                      className="form-control"
                      placeholder="Enter coupon"
                    />
                    <button className="btn btn-secondary">Apply</button>
                  </div>
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
