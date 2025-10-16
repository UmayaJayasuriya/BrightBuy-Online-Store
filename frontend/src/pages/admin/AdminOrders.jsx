/**
 * Admin Orders Component
 * Displays orders list for admin
 */
import React, { useEffect, useState } from 'react';
import { useAuth } from '../../context/AuthContext';

const AdminOrders = () => {
  const { makeAuthenticatedRequest, hasAdminPrivileges } = useAuth();
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    if (hasAdminPrivileges) fetchOrders();
  }, [hasAdminPrivileges]);

  const fetchOrders = async () => {
    try {
      setLoading(true);
      const res = await makeAuthenticatedRequest('/admin/orders');
      if (!res.ok) {
        const err = await res.json().catch(() => ({}));
        throw new Error(err.detail || `HTTP ${res.status}`);
      }
      const data = await res.json();
      setOrders(data);
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  };

  if (!hasAdminPrivileges) {
    return <div className="admin-access-denied"><h2>Access Denied</h2></div>;
  }

  if (loading) {
    return <div className="admin-loading"><div className="spinner"></div><p>Loading orders...</p></div>;
  }

  return (
    <div className="admin-orders">
      <div className="admin-header">
        <h1>Orders</h1>
      </div>

      {error && <div className="alert alert-danger">{error}</div>}

      <div className="table-responsive">
        <table className="table">
          <thead>
            <tr>
              <th>Order ID</th>
              <th>User</th>
              <th>Email</th>
              <th>Total Amount</th>
              <th>Status</th>
              <th>Created At</th>
            </tr>
          </thead>
          <tbody>
            {orders.map(o => (
              <tr key={o.order_id}>
                <td>{o.order_id}</td>
                <td>{o.user_name || '-'}</td>
                <td>{o.user_email || '-'}</td>
                <td>${Number(o.total_amount || 0).toFixed(2)}</td>
                <td>
                  <span className={`badge ${String(o.status).toLowerCase()}`}>
                    {o.status}
                  </span>
                </td>
                <td>{o.created_at ? new Date(o.created_at).toLocaleString() : '-'}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default AdminOrders;
