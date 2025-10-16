/**
 * Admin Categories Component
 * Simple admin view to list categories
 */
import React, { useEffect, useState } from 'react';
import { useAuth } from '../../context/AuthContext';

const AdminCategories = () => {
  const { makeAuthenticatedRequest, hasAdminPrivileges } = useAuth();
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    if (hasAdminPrivileges) fetchCategories();
  }, [hasAdminPrivileges]);

  const fetchCategories = async () => {
    try {
      setLoading(true);
      const res = await makeAuthenticatedRequest('/admin/categories');
      if (!res.ok) {
        const err = await res.json().catch(() => ({}));
        throw new Error(err.detail || `HTTP ${res.status}`);
      }
      const data = await res.json();
      setCategories(data);
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
    return <div className="admin-loading"><div className="spinner"></div><p>Loading categories...</p></div>;
  }

  return (
    <div className="admin-categories">
      <div className="admin-header">
        <h1>Category Management</h1>
      </div>
      {error && <div className="alert alert-danger">{error}</div>}
      <div className="table-responsive">
        <table className="table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Name</th>
              <th>Description</th>
            </tr>
          </thead>
          <tbody>
            {categories.map(c => (
              <tr key={c.category_id}>
                <td>{c.category_id}</td>
                <td>{c.category_name}</td>
                <td>{c.description || '-'}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default AdminCategories;
