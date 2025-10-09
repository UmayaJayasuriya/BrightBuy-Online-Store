/**
 * Login Component
 * Handles user authentication with the backend
 */
import React, { useState } from 'react';
import axios from 'axios';
import './Login.css';

const Login = ({ isOpen, onClose, onLoginSuccess }) => {
  const [formData, setFormData] = useState({
    identifier: '',
    password: ''
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
    setError(''); // Clear error when user starts typing
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const response = await axios.post('http://127.0.0.1:8020/auth/login', {
        identifier: formData.identifier,
        password: formData.password
      });

      if (response.data) {
        // Store user data in localStorage
        localStorage.setItem('user', JSON.stringify(response.data));
        onLoginSuccess(response.data);
        onClose();
        setFormData({ identifier: '', password: '' });
      }
    } catch (err) {
      setError(err.response?.data?.detail || 'Login failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="login-overlay">
      <div className="login-modal">
        <div className="login-header">
          <h2>Login to BrightBuy</h2>
          <button className="close-btn" onClick={onClose}>
            <i className="fa-solid fa-times"></i>
          </button>
        </div>

        <form onSubmit={handleSubmit} className="login-form">
          {error && (
            <div className="alert alert-danger">
              {error}
            </div>
          )}

          <div className="form-group">
            <label htmlFor="identifier">Email or Username</label>
            <input
              type="text"
              id="identifier"
              name="identifier"
              value={formData.identifier}
              onChange={handleChange}
              placeholder="Enter your email or username"
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="password">Password</label>
            <input
              type="password"
              id="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              placeholder="Enter your password"
              required
            />
          </div>

          <button 
            type="submit" 
            className="login-btn"
            disabled={loading}
          >
            {loading ? (
              <>
                <i className="fa-solid fa-spinner fa-spin me-2"></i>
                Logging in...
              </>
            ) : (
              'Login'
            )}
          </button>

          <div className="login-footer">
            <p>Don't have an account? <a href="#register">Sign up here</a></p>
          </div>
        </form>
      </div>
    </div>
  );
};

export default Login;