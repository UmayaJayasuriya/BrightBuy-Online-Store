/**
 * Login Component
 * Handles user authentication with the backend
 */
import React, { useState } from 'react';
import axios from 'axios';
import './Login.css';

const Login = ({ isOpen, onClose, onLoginSuccess, onSwitchToSignUp }) => {
  const [formData, setFormData] = useState({
    identifier: '',
    password: ''
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [show2FA, setShow2FA] = useState(false);
  const [verificationCode, setVerificationCode] = useState('');
  const [userId, setUserId] = useState(null);
  const [userEmail, setUserEmail] = useState('');

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
        // Check if 2FA is required (admin user)
        if (response.data.requires_2fa) {
          setShow2FA(true);
          setUserId(response.data.user_id);
          setUserEmail(response.data.email);
          setError('');
        } else {
          // Regular user - proceed with login
          if (response.data.access_token) {
            localStorage.setItem('token', response.data.access_token);
            console.log('Token saved to localStorage');
          }
          
          localStorage.setItem('user', JSON.stringify(response.data));
          onLoginSuccess(response.data);
          onClose();
          setFormData({ identifier: '', password: '' });
        }
      }
    } catch (err) {
      setError(err.response?.data?.detail || 'Login failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleVerify2FA = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const response = await axios.post('http://127.0.0.1:8020/auth/verify-2fa', {
        user_id: userId,
        verification_code: verificationCode
      });

      if (response.data && response.data.access_token) {
        // Store token and user data
        localStorage.setItem('token', response.data.access_token);
        localStorage.setItem('user', JSON.stringify(response.data));
        console.log('Admin logged in successfully with 2FA');
        
        onLoginSuccess(response.data);
        onClose();
        
        // Reset form
        setFormData({ identifier: '', password: '' });
        setVerificationCode('');
        setShow2FA(false);
      }
    } catch (err) {
      setError(err.response?.data?.detail || 'Invalid verification code. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleBack = () => {
    setShow2FA(false);
    setVerificationCode('');
    setError('');
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

        {!show2FA ? (
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
            <p>
              Don't have an account? 
              <a 
                href="#register" 
                onClick={(e) => {
                  e.preventDefault();
                  if (onSwitchToSignUp) {
                    onSwitchToSignUp();
                  }
                }}
              >
                Sign up here
              </a>
            </p>
          </div>
        </form>
        ) : (
          <form onSubmit={handleVerify2FA} className="login-form">
            <div className="alert alert-info">
              <i className="fa-solid fa-envelope me-2"></i>
              A verification code has been sent to <strong>{userEmail}</strong>
            </div>

            {error && (
              <div className="alert alert-danger">
                {error}
              </div>
            )}

            <div className="form-group">
              <label htmlFor="verificationCode">Verification Code</label>
              <input
                type="text"
                id="verificationCode"
                name="verificationCode"
                value={verificationCode}
                onChange={(e) => {
                  setVerificationCode(e.target.value);
                  setError('');
                }}
                placeholder="Enter 6-digit code"
                maxLength="6"
                pattern="[0-9]{6}"
                required
                autoFocus
                style={{ fontSize: '1.2rem', letterSpacing: '0.5rem', textAlign: 'center' }}
              />
              <small className="form-text text-muted">
                Code expires in 10 minutes
              </small>
            </div>

            <button 
              type="submit" 
              className="login-btn"
              disabled={loading || verificationCode.length !== 6}
            >
              {loading ? (
                <>
                  <i className="fa-solid fa-spinner fa-spin me-2"></i>
                  Verifying...
                </>
              ) : (
                'Verify & Login'
              )}
            </button>

            <button 
              type="button" 
              className="btn btn-secondary mt-2 w-100"
              onClick={handleBack}
              disabled={loading}
            >
              <i className="fa-solid fa-arrow-left me-2"></i>
              Back to Login
            </button>

            <div className="login-footer">
              <p className="text-muted">
                <small>
                  Didn't receive the code? Try logging in again.
                </small>
              </p>
            </div>
          </form>
        )}
      </div>
    </div>
  );
};

export default Login;