/**
 * Admin Dashboard Component
 * Main dashboard showing overview statistics and quick actions
 */
import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import './AdminDashboard.css';

const AdminDashboard = () => {
  const { makeAuthenticatedRequest, hasAdminPrivileges } = useAuth();
  const [dashboardData, setDashboardData] = useState({
    total_users: 0,
    total_products: 0,
    total_orders: 0,
    total_revenue: 0,
    recent_orders: 0,
    low_stock_products: 0
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    if (hasAdminPrivileges) {
      fetchDashboardData();
    }
  }, [hasAdminPrivileges]);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
  const response = await makeAuthenticatedRequest('/admin/dashboard');
      if (response.ok) {
        const data = await response.json();
        setDashboardData(data);
      } else {
        let errDetail = '';
        try {
          const errJson = await response.json();
          errDetail = errJson.detail || JSON.stringify(errJson);
        } catch (e) {
          errDetail = `HTTP ${response.status}`;
        }
        setError(`Failed to fetch dashboard data: ${errDetail}`);
      }
    } catch (err) {
      setError('Error loading dashboard: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  if (!hasAdminPrivileges) {
    return (
      <div className="admin-access-denied">
        <h2>Access Denied</h2>
        <p>You don't have permission to access the admin dashboard.</p>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="admin-loading">
        <div className="spinner"></div>
        <p>Loading dashboard...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="admin-error">
        <h3>Error</h3>
        <p>{error}</p>
        <button onClick={fetchDashboardData} className="retry-btn">
          Retry
        </button>
      </div>
    );
  }

  return (
    <div className="admin-dashboard">
      <div className="admin-header">
        <h1>Admin Dashboard</h1>
        <p>Welcome to the BrightBuy administration panel</p>
      </div>

      {/* Statistics Cards */}
      <div className="stats-grid">
        <div className="stat-card users">
          <div className="stat-icon">
            <i className="fas fa-users"></i>
          </div>
          <div className="stat-content">
            <h3>{dashboardData.total_users}</h3>
            <p>Total Users</p>
          </div>
        </div>

        <div className="stat-card products">
          <div className="stat-icon">
            <i className="fas fa-box"></i>
          </div>
          <div className="stat-content">
            <h3>{dashboardData.total_products}</h3>
            <p>Total Products</p>
          </div>
        </div>

        <div className="stat-card orders">
          <div className="stat-icon">
            <i className="fas fa-shopping-cart"></i>
          </div>
          <div className="stat-content">
            <h3>{dashboardData.total_orders}</h3>
            <p>Total Orders</p>
          </div>
        </div>

        <div className="stat-card revenue">
          <div className="stat-icon">
            <i className="fas fa-dollar-sign"></i>
          </div>
          <div className="stat-content">
            <h3>${dashboardData.total_revenue.toFixed(2)}</h3>
            <p>Total Revenue</p>
          </div>
        </div>

        <div className="stat-card recent-orders">
          <div className="stat-icon">
            <i className="fas fa-clock"></i>
          </div>
          <div className="stat-content">
            <h3>{dashboardData.recent_orders}</h3>
            <p>Recent Orders</p>
          </div>
        </div>

        <div className="stat-card low-stock">
          <div className="stat-icon">
            <i className="fas fa-exclamation-triangle"></i>
          </div>
          <div className="stat-content">
            <h3>{dashboardData.low_stock_products}</h3>
            <p>Low Stock Items</p>
          </div>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="quick-actions">
        <h2>Quick Actions</h2>
        <div className="actions-grid">
          <Link to="/admin/users" className="action-card">
            <i className="fas fa-users-cog"></i>
            <h3>Manage Users</h3>
            <p>View, edit, and manage user accounts</p>
          </Link>

          <Link to="/admin/products" className="action-card">
            <i className="fas fa-boxes"></i>
            <h3>Manage Products</h3>
            <p>Add, edit, and organize products</p>
          </Link>

          <Link to="/admin/categories" className="action-card">
            <i className="fas fa-tags"></i>
            <h3>Manage Categories</h3>
            <p>Create and organize product categories</p>
          </Link>

          <Link to="/admin/orders" className="action-card">
            <i className="fas fa-receipt"></i>
            <h3>View Orders</h3>
            <p>Monitor and manage customer orders</p>
          </Link>

          <Link to="/admin/analytics" className="action-card">
            <i className="fas fa-chart-bar"></i>
            <h3>Analytics</h3>
            <p>View sales and performance reports</p>
          </Link>

          <Link to="/admin/settings" className="action-card">
            <i className="fas fa-cogs"></i>
            <h3>Settings</h3>
            <p>Configure system settings</p>
          </Link>
        </div>
      </div>

      {/* Recent Activity */}
      <div className="recent-activity">
        <h2>Recent Activity</h2>
        <div className="activity-list">
          <div className="activity-item">
            <i className="fas fa-user-plus activity-icon user"></i>
            <div className="activity-content">
              <p><strong>New user registered</strong></p>
              <span className="activity-time">2 hours ago</span>
            </div>
          </div>
          
          <div className="activity-item">
            <i className="fas fa-shopping-cart activity-icon order"></i>
            <div className="activity-content">
              <p><strong>New order placed</strong></p>
              <span className="activity-time">4 hours ago</span>
            </div>
          </div>
          
          <div className="activity-item">
            <i className="fas fa-box activity-icon product"></i>
            <div className="activity-content">
              <p><strong>Product stock updated</strong></p>
              <span className="activity-time">6 hours ago</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AdminDashboard;