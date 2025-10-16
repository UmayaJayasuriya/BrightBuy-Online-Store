/**
 * User Management Component
 * Admin interface for managing users
 */
import React, { useState, useEffect } from 'react';
import { useAuth } from '../../context/AuthContext';
import './AdminUsers.css';

const AdminUsers = () => {
  const { makeAuthenticatedRequest, hasAdminPrivileges, isSuperAdmin } = useAuth();
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [editingUser, setEditingUser] = useState(null);
  const [formData, setFormData] = useState({
    user_name: '',
    email: '',
    name: '',
    password: '',
    user_type: 'customer'
  });

  useEffect(() => {
    if (hasAdminPrivileges) {
      fetchUsers();
    }
  }, [hasAdminPrivileges]);

  const fetchUsers = async () => {
    try {
      setLoading(true);
  const response = await makeAuthenticatedRequest('/admin/users');
      
      if (response.ok) {
        const data = await response.json();
        setUsers(data);
      } else {
        setError('Failed to fetch users');
      }
    } catch (err) {
      setError('Error loading users: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateUser = async (e) => {
    e.preventDefault();
    try {
  const response = await makeAuthenticatedRequest('/admin/users', {
        method: 'POST',
        body: JSON.stringify(formData)
      });

      if (response.ok) {
        setShowCreateModal(false);
        setFormData({
          user_name: '',
          email: '',
          name: '',
          password: '',
          user_type: 'customer'
        });
        fetchUsers();
      } else {
        const errorData = await response.json();
        setError(errorData.detail || 'Failed to create user');
      }
    } catch (err) {
      setError('Error creating user: ' + err.message);
    }
  };

  const handleUpdateUser = async (userId) => {
    try {
      const updateData = {
        user_name: editingUser.user_name,
        email: editingUser.email,
        name: editingUser.name,
        user_type: editingUser.user_type
      };

  const response = await makeAuthenticatedRequest(`/admin/users/${userId}`, {
        method: 'PUT',
        body: JSON.stringify(updateData)
      });

      if (response.ok) {
        setEditingUser(null);
        fetchUsers();
      } else {
        const errorData = await response.json();
        setError(errorData.detail || 'Failed to update user');
      }
    } catch (err) {
      setError('Error updating user: ' + err.message);
    }
  };

  const handleDeleteUser = async (userId) => {
    if (window.confirm('Are you sure you want to delete this user?')) {
      try {
  const response = await makeAuthenticatedRequest(`/admin/users/${userId}`, {
          method: 'DELETE'
        });

        if (response.ok) {
          fetchUsers();
        } else {
          const errorData = await response.json();
          setError(errorData.detail || 'Failed to delete user');
        }
      } catch (err) {
        setError('Error deleting user: ' + err.message);
      }
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    if (editingUser) {
      setEditingUser({ ...editingUser, [name]: value });
    } else {
      setFormData({ ...formData, [name]: value });
    }
  };

  if (!hasAdminPrivileges) {
    return (
      <div className="admin-access-denied">
        <h2>Access Denied</h2>
        <p>You don't have permission to manage users.</p>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="admin-loading">
        <div className="spinner"></div>
        <p>Loading users...</p>
      </div>
    );
  }

  return (
    <div className="admin-users">
      <div className="admin-header">
        <h1>User Management</h1>
        {isSuperAdmin && (
          <button 
            className="create-btn"
            onClick={() => setShowCreateModal(true)}
          >
            <i className="fas fa-plus"></i>
            Create User
          </button>
        )}
      </div>

      {error && (
        <div className="alert alert-danger">
          {error}
          <button className="close-btn" onClick={() => setError('')}>×</button>
        </div>
      )}

      <div className="users-table-container">
        <table className="users-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Username</th>
              <th>Email</th>
              <th>Name</th>
              <th>User Type</th>
              <th>Admin</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {users.map(user => (
              <tr key={user.user_id}>
                <td>{user.user_id}</td>
                <td>
                  {editingUser?.user_id === user.user_id ? (
                    <input
                      type="text"
                      name="user_name"
                      value={editingUser.user_name}
                      onChange={handleInputChange}
                    />
                  ) : (
                    user.user_name
                  )}
                </td>
                <td>
                  {editingUser?.user_id === user.user_id ? (
                    <input
                      type="email"
                      name="email"
                      value={editingUser.email}
                      onChange={handleInputChange}
                    />
                  ) : (
                    user.email
                  )}
                </td>
                <td>
                  {editingUser?.user_id === user.user_id ? (
                    <input
                      type="text"
                      name="name"
                      value={editingUser.name}
                      onChange={handleInputChange}
                    />
                  ) : (
                    user.name
                  )}
                </td>
                <td>
                  {editingUser?.user_id === user.user_id ? (
                    <select
                      name="user_type"
                      value={editingUser.user_type}
                      onChange={handleInputChange}
                      disabled={!isSuperAdmin}
                    >
                      <option value="customer">Customer</option>
                      <option value="manager">Manager</option>
                      <option value="admin">Admin</option>
                    </select>
                  ) : (
                    <span className={`user-type ${user.user_type}`}>
                      {user.user_type}
                    </span>
                  )}
                </td>
                <td>
                  <span className={`admin-badge ${user.is_admin ? 'yes' : 'no'}`}>
                    {user.is_admin ? 'Yes' : 'No'}
                  </span>
                </td>
                <td>
                  <div className="action-buttons">
                    {editingUser?.user_id === user.user_id ? (
                      <>
                        <button
                          className="save-btn"
                          onClick={() => handleUpdateUser(user.user_id)}
                        >
                          Save
                        </button>
                        <button
                          className="cancel-btn"
                          onClick={() => setEditingUser(null)}
                        >
                          Cancel
                        </button>
                      </>
                    ) : (
                      <>
                        <button
                          className="edit-btn"
                          onClick={() => setEditingUser(user)}
                        >
                          Edit
                        </button>
                        {isSuperAdmin && (
                          <button
                            className="delete-btn"
                            onClick={() => handleDeleteUser(user.user_id)}
                          >
                            Delete
                          </button>
                        )}
                      </>
                    )}
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Create User Modal */}
      {showCreateModal && (
        <div className="modal-overlay">
          <div className="modal">
            <div className="modal-header">
              <h2>Create New User</h2>
              <button
                className="close-btn"
                onClick={() => setShowCreateModal(false)}
              >
                ×
              </button>
            </div>
            <form onSubmit={handleCreateUser} className="modal-form">
              <div className="form-group">
                <label>Username</label>
                <input
                  type="text"
                  name="user_name"
                  value={formData.user_name}
                  onChange={handleInputChange}
                  required
                />
              </div>
              <div className="form-group">
                <label>Email</label>
                <input
                  type="email"
                  name="email"
                  value={formData.email}
                  onChange={handleInputChange}
                  required
                />
              </div>
              <div className="form-group">
                <label>Full Name</label>
                <input
                  type="text"
                  name="name"
                  value={formData.name}
                  onChange={handleInputChange}
                  required
                />
              </div>
              <div className="form-group">
                <label>Password</label>
                <input
                  type="password"
                  name="password"
                  value={formData.password}
                  onChange={handleInputChange}
                  required
                />
              </div>
              <div className="form-group">
                <label>User Type</label>
                <select
                  name="user_type"
                  value={formData.user_type}
                  onChange={handleInputChange}
                >
                  <option value="customer">Customer</option>
                  <option value="manager">Manager</option>
                  <option value="admin">Admin</option>
                </select>
              </div>
              <div className="modal-actions">
                <button type="submit" className="submit-btn">
                  Create User
                </button>
                <button
                  type="button"
                  className="cancel-btn"
                  onClick={() => setShowCreateModal(false)}
                >
                  Cancel
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default AdminUsers;