/**
 * Admin Dashboard Component
 * View users, orders, add/delete products, and manage variant quantities
 */
import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import './Admin.css';

const Admin = () => {
  const { user, isAdmin } = useAuth();
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState('users');
  
  const [users, setUsers] = useState([]);
  const [orders, setOrders] = useState([]);
  const [products, setProducts] = useState([]);
  const [categories, setCategories] = useState([]);
  const [variants, setVariants] = useState([]);
  
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [successMessage, setSuccessMessage] = useState('');
  
  // New product form
  const [newProduct, setNewProduct] = useState({
    product_name: '',
    category_id: '',
    description: ''
  });
  
  // Variant quantity update
  const [variantUpdate, setVariantUpdate] = useState({
    variant_id: '',
    quantity: ''
  });

  useEffect(() => {
    if (!isAdmin) {
      navigate('/');
    }
  }, [isAdmin, navigate]);

  useEffect(() => {
    if (isAdmin) {
      if (activeTab === 'users') fetchUsers();
      if (activeTab === 'orders') fetchOrders();
      if (activeTab === 'products') {
        fetchProducts();
        fetchCategories();
      }
      if (activeTab === 'quantities') {
        fetchVariants();
      }
    }
  }, [activeTab, isAdmin]);

  const axiosConfig = () => {
    const token = user?.access_token;
    console.log('User object:', user);
    console.log('Token:', token);
    
    if (!token) {
      console.error('No access token found! User must log in as admin.');
      return { headers: {} };
    }
    
    return {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    };
  };

  const fetchUsers = async () => {
    setLoading(true);
    setError('');
    try {
      const config = axiosConfig();
      if (!config.headers.Authorization) {
        setError('Not authenticated. Please log in as admin.');
        setLoading(false);
        return;
      }
      const response = await axios.get('http://127.0.0.1:8020/admin/users', config);
      setUsers(response.data);
    } catch (err) {
      console.error('Fetch users error:', err);
      setError(err.response?.data?.detail || 'Failed to fetch users');
    } finally {
      setLoading(false);
    }
  };

  const fetchOrders = async () => {
    setLoading(true);
    setError('');
    try {
      const config = axiosConfig();
      if (!config.headers.Authorization) {
        setError('Not authenticated. Please log in as admin.');
        setLoading(false);
        return;
      }
      const response = await axios.get('http://127.0.0.1:8020/admin/orders', config);
      setOrders(response.data);
    } catch (err) {
      console.error('Fetch orders error:', err);
      setError(err.response?.data?.detail || 'Failed to fetch orders');
    } finally {
      setLoading(false);
    }
  };

  const fetchProducts = async () => {
    setLoading(true);
    setError('');
    try {
      const response = await axios.get('http://127.0.0.1:8020/products/');
      setProducts(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to fetch products');
    } finally {
      setLoading(false);
    }
  };

  const fetchCategories = async () => {
    try {
      const response = await axios.get('http://127.0.0.1:8020/categories/');
      setCategories(response.data);
    } catch (err) {
      console.error('Failed to fetch categories', err);
    }
  };

  const fetchVariants = async () => {
    setLoading(true);
    setError('');
    try {
      // Fetch all products with their variants
      const productsResponse = await axios.get('http://127.0.0.1:8020/products/');
      const allProducts = productsResponse.data;
      
      // Fetch variants for each product
      const variantsPromises = allProducts.map(async (product) => {
        try {
          const response = await axios.get(`http://127.0.0.1:8020/products/${product.product_id}/variants/`);
          return response.data.variants || [];
        } catch (err) {
          console.error(`Failed to fetch variants for product ${product.product_id}`, err);
          return [];
        }
      });
      
      const variantsArrays = await Promise.all(variantsPromises);
      const allVariants = variantsArrays.flat();
      setVariants(allVariants);
    } catch (err) {
      console.error('Failed to fetch variants', err);
      setError(err.response?.data?.detail || 'Failed to fetch variants');
    } finally {
      setLoading(false);
    }
  };

  const handleAddProduct = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setSuccessMessage('');
    
    try {
      const config = axiosConfig();
      if (!config.headers.Authorization) {
        setError('Not authenticated. Please log in as admin.');
        setLoading(false);
        return;
      }
      
      const params = new URLSearchParams();
      params.append('product_name', newProduct.product_name);
      params.append('category_id', newProduct.category_id);
      if (newProduct.description) params.append('description', newProduct.description);
      
      const response = await axios.post(
        `http://127.0.0.1:8020/admin/products?${params.toString()}`,
        {},
        config
      );
      
      setSuccessMessage(`Product "${response.data.product_name}" added successfully!`);
      setNewProduct({ product_name: '', category_id: '', description: '' });
      fetchProducts();
    } catch (err) {
      console.error('Add product error:', err);
      setError(err.response?.data?.detail || 'Failed to add product');
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteProduct = async (productId, productName) => {
    if (!window.confirm(`Are you sure you want to delete "${productName}"?`)) {
      return;
    }
    
    setLoading(true);
    setError('');
    setSuccessMessage('');
    
    try {
      const config = axiosConfig();
      if (!config.headers.Authorization) {
        setError('Not authenticated. Please log in as admin.');
        setLoading(false);
        return;
      }
      await axios.delete(`http://127.0.0.1:8020/admin/products/${productId}`, config);
      setSuccessMessage(`Product "${productName}" deleted successfully!`);
      fetchProducts();
    } catch (err) {
      console.error('Delete product error:', err);
      setError(err.response?.data?.detail || 'Failed to delete product');
    } finally {
      setLoading(false);
    }
  };

  const handleUpdateVariantQuantity = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setSuccessMessage('');
    
    try {
      const config = axiosConfig();
      if (!config.headers.Authorization) {
        setError('Not authenticated. Please log in as admin.');
        setLoading(false);
        return;
      }
      
      const response = await axios.put(
        `http://127.0.0.1:8020/admin/variants/${variantUpdate.variant_id}/quantity?quantity=${variantUpdate.quantity}`,
        {},
        config
      );
      
      setSuccessMessage(`Variant quantity updated to ${response.data.quantity}!`);
      setVariantUpdate({ variant_id: '', quantity: '' });
      fetchVariants(); // Refresh the variants list
    } catch (err) {
      console.error('Update variant error:', err);
      setError(err.response?.data?.detail || 'Failed to update variant quantity');
    } finally {
      setLoading(false);
    }
  };

  if (!isAdmin) {
    return null;
  }

  return (
    <div className="admin-dashboard container my-5">
      <h1 className="text-center mb-4">Admin Dashboard</h1>
      
      {error && (
        <div className="alert alert-danger alert-dismissible fade show" role="alert">
          {error}
          <button type="button" className="btn-close" onClick={() => setError('')}></button>
        </div>
      )}
      
      {successMessage && (
        <div className="alert alert-success alert-dismissible fade show" role="alert">
          {successMessage}
          <button type="button" className="btn-close" onClick={() => setSuccessMessage('')}></button>
        </div>
      )}

      <ul className="nav nav-tabs mb-4">
        <li className="nav-item">
          <button
            className={`nav-link ${activeTab === 'users' ? 'active' : ''}`}
            onClick={() => setActiveTab('users')}
          >
            Users
          </button>
        </li>
        <li className="nav-item">
          <button
            className={`nav-link ${activeTab === 'orders' ? 'active' : ''}`}
            onClick={() => setActiveTab('orders')}
          >
            Orders
          </button>
        </li>
        <li className="nav-item">
          <button
            className={`nav-link ${activeTab === 'products' ? 'active' : ''}`}
            onClick={() => setActiveTab('products')}
          >
            Products
          </button>
        </li>
      </ul>

      {loading && <div className="text-center"><div className="spinner-border" role="status"></div></div>}

      {activeTab === 'users' && (
        <div className="users-section">
          <h2>Users</h2>
          <table className="table table-striped">
            <thead>
              <tr>
                <th>User ID</th>
                <th>Username</th>
                <th>Email</th>
                <th>Name</th>
                <th>Role</th>
              </tr>
            </thead>
            <tbody>
              {users.map(u => (
                <tr key={u.user_id}>
                  <td>{u.user_id}</td>
                  <td>{u.user_name}</td>
                  <td>{u.email}</td>
                  <td>{u.name}</td>
                  <td><span className={`badge ${u.user_type === 'admin' ? 'bg-danger' : 'bg-primary'}`}>{u.user_type}</span></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {activeTab === 'orders' && (
        <div className="orders-section">
          <h2>Orders</h2>
          <table className="table table-striped">
            <thead>
              <tr>
                <th>Order ID</th>
                <th>User ID</th>
                <th>Date</th>
                <th>Total</th>
                <th>Delivery Status</th>
                <th>Payment Method</th>
                <th>Payment Status</th>
              </tr>
            </thead>
            <tbody>
              {orders.map(o => (
                <tr key={o.order_id}>
                  <td>{o.order_id}</td>
                  <td>{o.user_id}</td>
                  <td>{new Date(o.order_date).toLocaleDateString()}</td>
                  <td>${parseFloat(o.total_amount).toFixed(2)}</td>
                  <td>{o.delivery_status || 'N/A'}</td>
                  <td>{o.payment_method || 'N/A'}</td>
                  <td>{o.payment_status || 'N/A'}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {activeTab === 'products' && (
        <div className="products-section">
          <h2>Products</h2>
          
          <div className="card mb-4">
            <div className="card-body">
              <h5 className="card-title">Add New Product</h5>
              <form onSubmit={handleAddProduct}>
                <div className="row">
                  <div className="col-md-4">
                    <input
                      type="text"
                      className="form-control"
                      placeholder="Product Name"
                      value={newProduct.product_name}
                      onChange={(e) => setNewProduct({...newProduct, product_name: e.target.value})}
                      required
                    />
                  </div>
                  <div className="col-md-3">
                    <select
                      className="form-select"
                      value={newProduct.category_id}
                      onChange={(e) => setNewProduct({...newProduct, category_id: e.target.value})}
                      required
                    >
                      <option value="">Select Category</option>
                      {categories.map(c => (
                        <option key={c.category_id} value={c.category_id}>{c.category_name}</option>
                      ))}
                    </select>
                  </div>
                  <div className="col-md-3">
                    <input
                      type="text"
                      className="form-control"
                      placeholder="Description (optional)"
                      value={newProduct.description}
                      onChange={(e) => setNewProduct({...newProduct, description: e.target.value})}
                    />
                  </div>
                  <div className="col-md-2">
                    <button type="submit" className="btn btn-primary w-100" disabled={loading}>
                      Add Product
                    </button>
                  </div>
                </div>
              </form>
            </div>
          </div>

          <div className="card mb-4">
            <div className="card-body">
              <h5 className="card-title">Update Variant Quantity</h5>
              <form onSubmit={handleUpdateVariantQuantity}>
                <div className="row">
                  <div className="col-md-5">
                    <input
                      type="number"
                      className="form-control"
                      placeholder="Variant ID"
                      value={variantUpdate.variant_id}
                      onChange={(e) => setVariantUpdate({...variantUpdate, variant_id: e.target.value})}
                      required
                    />
                  </div>
                  <div className="col-md-5">
                    <input
                      type="number"
                      className="form-control"
                      placeholder="New Quantity"
                      value={variantUpdate.quantity}
                      onChange={(e) => setVariantUpdate({...variantUpdate, quantity: e.target.value})}
                      required
                      min="0"
                    />
                  </div>
                  <div className="col-md-2">
                    <button type="submit" className="btn btn-warning w-100" disabled={loading}>
                      Update
                    </button>
                  </div>
                </div>
              </form>
            </div>
          </div>

          <table className="table table-striped">
            <thead>
              <tr>
                <th>Product ID</th>
                <th>Product Name</th>
                <th>Category</th>
                <th>Description</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {products.map(p => (
                <tr key={p.product_id}>
                  <td>{p.product_id}</td>
                  <td>{p.product_name}</td>
                  <td>{p.category?.category_name || 'N/A'}</td>
                  <td>{p.description || 'N/A'}</td>
                  <td>
                    <button
                      className="btn btn-sm btn-danger"
                      onClick={() => handleDeleteProduct(p.product_id, p.product_name)}
                      disabled={loading}
                    >
                      Delete
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

export default Admin;
