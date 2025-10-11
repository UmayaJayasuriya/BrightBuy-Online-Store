import React, { useState } from 'react';
import axios from 'axios';
import './SignUp.css';

const SignUp = ({ isOpen, onClose, onSignUpSuccess, onSwitchToLogin }) => {
  const [form, setForm] = useState({
    user_name: '',
    email: '',
    name: '',
    password: '',
    address: {
      house_number: '',
      street: '',
      city: '',
      state: ''
    }
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [successMsg, setSuccessMsg] = useState('');

  if (!isOpen) return null;

  const handleChange = (e) => {
    const { name, value } = e.target;
    if (name.startsWith('address.')) {
      const key = name.split('.')[1];
      setForm(prev => ({ ...prev, address: { ...prev.address, [key]: value } }));
    } else {
      setForm(prev => ({ ...prev, [name]: value }));
    }
    setError('');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setSuccessMsg('');

    try {
      // Ensure house_number is an integer
      const payload = {
        user_name: form.user_name,
        email: form.email,
        name: form.name,
        password: form.password,
        address: {
          house_number: parseInt(form.address.house_number, 10),
          street: form.address.street,
          city: form.address.city,
          state: form.address.state
        }
      };

      const resp = await axios.post('http://127.0.0.1:8020/users', payload);
      setSuccessMsg('Account created successfully.');

      // Optionally, set the authenticated user in parent/context
      if (resp.data) {
        onSignUpSuccess(resp.data);
      }

      // Close after short delay to show success
      setTimeout(() => {
        onClose();
      }, 800);
    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'Sign up failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="signup-overlay">
      <div className="signup-modal">
        <div className="signup-header">
          <h2>Create an account</h2>
          <button className="close-btn" onClick={onClose} aria-label="Close">
            <i className="fa-solid fa-times"></i>
          </button>
        </div>

        <form className="signup-form" onSubmit={handleSubmit}>
          {error && <div className="alert alert-danger">{error}</div>}
          {successMsg && <div className="alert alert-success">{successMsg}</div>}

          <div className="form-row">
            <div className="form-group">
              <label>Username</label>
              <input name="user_name" value={form.user_name} onChange={handleChange} required />
            </div>
            <div className="form-group">
              <label>Email</label>
              <input type="email" name="email" value={form.email} onChange={handleChange} required />
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>Full name</label>
              <input name="name" value={form.name} onChange={handleChange} required />
            </div>
            <div className="form-group">
              <label>Password</label>
              <input type="password" name="password" value={form.password} onChange={handleChange} required />
            </div>
          </div>

          <fieldset className="address-fieldset">
            <legend>Address</legend>
            <div className="form-row">
              <div className="form-group">
                <label>House number</label>
                <input name="address.house_number" value={form.address.house_number} onChange={handleChange} required />
              </div>
              <div className="form-group">
                <label>Street</label>
                <input name="address.street" value={form.address.street} onChange={handleChange} required />
              </div>
            </div>

            <div className="form-row">
              <div className="form-group">
                <label>City</label>
                <input name="address.city" value={form.address.city} onChange={handleChange} required />
              </div>
              <div className="form-group">
                <label>State</label>
                <input name="address.state" value={form.address.state} onChange={handleChange} required />
              </div>
            </div>
          </fieldset>

          <button className="signup-btn" type="submit" disabled={loading}>
            {loading ? (<><i className="fa-solid fa-spinner fa-spin me-2" /> Creating...</>) : 'Create account'}
          </button>

          <div className="signup-footer">
            <p>
              Already have an account? 
              <a 
                href="#login" 
                onClick={(e) => {
                  e.preventDefault();
                  if (onSwitchToLogin) {
                    onSwitchToLogin();
                  }
                }}
              >
                Login here
              </a>
            </p>
          </div>
        </form>
      </div>
    </div>
  );
};

export default SignUp;
