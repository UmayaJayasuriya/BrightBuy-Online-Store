/**
 * Profile Page Component
 * Displays user information and order history
 */
import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import { useAuth } from '../context/AuthContext';
import Spinner from '../components/common/Spinner';
import './Profile.css';

const Profile = () => {
  const { user, isAuthenticated } = useAuth();
  const [loading, setLoading] = useState(true);
  const [userDetails, setUserDetails] = useState(null);
  const [orders, setOrders] = useState([]);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchUserData = async () => {
      if (!isAuthenticated || !user) {
        setLoading(false);
        return;
      }

      try {
        setLoading(true);
        
        // Fetch user details
        const userResponse = await axios.get(`http://127.0.0.1:8020/users/${user.user_id}`);
        setUserDetails(userResponse.data);
        
        // Fetch user's orders
        const ordersResponse = await axios.get(`http://127.0.0.1:8020/orders/user/${user.user_id}`);
        setOrders(ordersResponse.data);
        
      } catch (err) {
        console.error('Error fetching user data:', err);
        setError('Failed to load profile information');
      } finally {
        setLoading(false);
      }
    };

    fetchUserData();
  }, [isAuthenticated, user]);

  if (!isAuthenticated) {
    return (
      <div className="profile-page">
        <div className="container py-5 text-center">
          <i className="fas fa-user-lock fa-5x text-muted mb-4"></i>
          <h3>Please Login</h3>
          <p className="text-muted mb-4">You need to be logged in to view your profile.</p>
          <Link to="/" className="btn btn-primary rounded-pill py-3 px-5">
            Go to Home
          </Link>
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

  if (error) {
    return (
      <div className="profile-page">
        <div className="container py-5 text-center">
          <i className="fas fa-exclamation-circle fa-5x text-danger mb-4"></i>
          <h3>{error}</h3>
          <Link to="/" className="btn btn-primary rounded-pill py-3 px-5 mt-3">
            Go to Home
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="profile-page">
      {/* Page Header */}
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
          <h1 className="display-4 text-white mb-3 fw-bolder">My Profile</h1>
          <p className="text-white fw-bolder">Welcome back, {user?.user_name}!</p>
        </div>
      </div>

      {/* Profile Content */}
      <div className="container py-5">
        <div className="row g-4">
          {/* User Information Card */}
          <div className="col-lg-4">
            <div className="card shadow-sm border-0 h-100">
              <div className="card-body p-4">
                <div className="text-center mb-4">
                  <div className="profile-avatar mx-auto mb-3">
                    <i className="fas fa-user fa-4x text-primary"></i>
                  </div>
                  <h4 className="mb-1">{userDetails?.name || user?.user_name}</h4>
                  <p className="text-muted">{userDetails?.user_type || 'Customer'}</p>
                </div>

                <hr />

                <div className="profile-info">
                  <h5 className="mb-3">
                    <i className="fas fa-info-circle text-primary me-2"></i>
                    Account Information
                  </h5>
                  
                  <div className="info-item mb-3">
                    <label className="text-muted small">Username</label>
                    <p className="mb-0 fw-bold">{userDetails?.user_name || user?.user_name}</p>
                  </div>

                  <div className="info-item mb-3">
                    <label className="text-muted small">Email</label>
                    <p className="mb-0 fw-bold">{userDetails?.email || user?.email}</p>
                  </div>

                  <div className="info-item mb-3">
                    <label className="text-muted small">Full Name</label>
                    <p className="mb-0 fw-bold">{userDetails?.name || 'N/A'}</p>
                  </div>

                  <div className="info-item mb-3">
                    <label className="text-muted small">Account Type</label>
                    <p className="mb-0">
                      <span className="badge bg-primary">
                        {userDetails?.user_type || 'Customer'}
                      </span>
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Orders Section */}
          <div className="col-lg-8">
            <div className="card shadow-sm border-0">
              <div className="card-body p-4">
                <h4 className="mb-4">
                  <i className="fas fa-shopping-bag text-primary me-2"></i>
                  My Orders
                </h4>

                {orders.length === 0 ? (
                  <div className="text-center py-5">
                    <i className="fas fa-shopping-cart fa-4x text-muted mb-3"></i>
                    <h5 className="text-muted">No orders yet</h5>
                    <p className="text-muted mb-4">Start shopping to see your orders here!</p>
                    <Link to="/shop" className="btn btn-primary rounded-pill py-2 px-4">
                      Browse Products
                    </Link>
                  </div>
                ) : (
                  <div className="orders-list">
                    {orders.map((order) => (
                      <div key={order.order_id} className="order-card mb-3 p-3 border rounded">
                        <div className="row align-items-center">
                          <div className="col-md-3">
                            <div className="order-info">
                              <label className="text-muted small">Order ID</label>
                              <p className="mb-0 fw-bold">#{order.order_id}</p>
                            </div>
                          </div>
                          <div className="col-md-3">
                            <div className="order-info">
                              <label className="text-muted small">Date</label>
                              <p className="mb-0">
                                {new Date(order.order_date).toLocaleDateString()}
                              </p>
                            </div>
                          </div>
                          <div className="col-md-3">
                            <div className="order-info">
                              <label className="text-muted small">Total</label>
                              <p className="mb-0 fw-bold text-primary">
                                ${parseFloat(order.total_amount).toFixed(2)}
                              </p>
                            </div>
                          </div>
                          <div className="col-md-3">
                            <div className="order-info">
                              <label className="text-muted small">Items</label>
                              <p className="mb-0">
                                {order.order_items?.length || 0} item(s)
                              </p>
                            </div>
                          </div>
                        </div>
                        
                        {order.order_items && order.order_items.length > 0 && (
                          <div className="order-items mt-3 pt-3 border-top">
                            {order.order_items.map((item, index) => (
                              <div key={index} className="d-flex justify-content-between align-items-center mb-2">
                                <span className="text-muted">
                                  {item.product_name} - {item.variant_name}
                                </span>
                                <span className="text-muted">
                                  Qty: {item.quantity} × ${parseFloat(item.price).toFixed(2)}
                                </span>
                              </div>
                            ))}
                          </div>
                        )}
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Profile;
