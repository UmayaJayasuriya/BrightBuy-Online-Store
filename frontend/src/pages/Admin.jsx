/**
 * Admin Dashboard Component
 * - View users, orders
 * - Add/delete products
 * - Manage variant quantities (Quantities tab only)
 * - Category-wise listing for Products and Quantities tabs
 */
import React, { useEffect, useState } from 'react';
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

  const [expandedOrders, setExpandedOrders] = useState({});
  const [orderItems, setOrderItems] = useState({});

  const [selectedCategory, setSelectedCategory] = useState(null);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [successMessage, setSuccessMessage] = useState('');

  // New product form
  const [newProduct, setNewProduct] = useState({
    product_name: '',
    category_id: '',
    description: '',
    variants: []
  });

  // For new variant input
  const [newVariant, setNewVariant] = useState({
    variant_name: '',
    price: '',
    quantity: '',
    SKU: ''
  });

  // Variant quantity update (Quantities tab only)
  const [variantUpdate, setVariantUpdate] = useState({
    variant_id: '',
    quantity: ''
  });

  // Reports parameters
  const [reportParams, setReportParams] = useState({
    year: new Date().getFullYear(),
    startDate: '',
    endDate: '',
    limit: 50,
    userId: ''
  });

  // For adding variant to existing product
  const [addVariantToProduct, setAddVariantToProduct] = useState({
    product_id: '',
    variant_name: '',
    price: '',
    quantity: '',
    SKU: ''
  });

  // For expanding product variants in Products tab
  const [expandedProducts, setExpandedProducts] = useState({});
  const [productVariants, setProductVariants] = useState({});

  useEffect(() => {
    if (!isAdmin) navigate('/');
  }, [isAdmin, navigate]);

  useEffect(() => {
    if (!isAdmin) return;
    if (activeTab === 'users') fetchUsers();
    if (activeTab === 'orders') fetchOrders();
    if (activeTab === 'products') {
      fetchProducts();
      fetchCategories();
    }
    if (activeTab === 'quantities') {
      fetchCategories();
      fetchProducts();
      fetchVariants();
    }
    if (activeTab === 'reports') {
      // Set default year to current year
      setReportParams(prev => ({ ...prev, year: new Date().getFullYear() }));
    }
  }, [activeTab, isAdmin]);

  const axiosConfig = () => {
    const token = user?.access_token;
    if (!token) return { headers: {} };
    return { headers: { Authorization: `Bearer ${token}` } };
  };

  const fetchUsers = async () => {
    setLoading(true); setError('');
    try {
      const config = axiosConfig();
      if (!config.headers.Authorization) { setError('Not authenticated. Please log in as admin.'); return; }
      const res = await axios.get('http://127.0.0.1:8020/admin/users', config);
      setUsers(res.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to fetch users');
    } finally { setLoading(false); }
  };

  const fetchOrders = async () => {
    setLoading(true); setError('');
    try {
      const config = axiosConfig();
      if (!config.headers.Authorization) { setError('Not authenticated. Please log in as admin.'); return; }
      const res = await axios.get('http://127.0.0.1:8020/admin/orders', config);
      setOrders(res.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to fetch orders');
    } finally { setLoading(false); }
  };

  const fetchProducts = async () => {
    setLoading(true); setError('');
    try {
      const res = await axios.get('http://127.0.0.1:8020/products/');
      setProducts(res.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to fetch products');
    } finally { setLoading(false); }
  };

  const fetchCategories = async () => {
    try {
      const res = await axios.get('http://127.0.0.1:8020/categories/');
      setCategories(res.data);
    } catch (err) {
      // Non-fatal
    }
  };

  const fetchVariants = async () => {
    setLoading(true); setError('');
    try {
      // get all products, then per-product variants
      const prodRes = await axios.get('http://127.0.0.1:8020/products/');
      const allProducts = prodRes.data || [];
      const variantLists = await Promise.all(
        allProducts.map(async (p) => {
          try {
            const res = await axios.get(`http://127.0.0.1:8020/products/${p.product_id}/variants/`);
            return res.data.variants || [];
          } catch {
            return [];
          }
        })
      );
      setVariants(variantLists.flat());
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to fetch variants');
    } finally { setLoading(false); }
  };

  const handleAddProduct = async (e) => {
    e.preventDefault(); setLoading(true); setError(''); setSuccessMessage('');
    try {
      const config = axiosConfig();
      if (!config.headers.Authorization) { setError('Not authenticated. Please log in as admin.'); return; }
      // Send product and variants as JSON
      const payload = {
        product_name: newProduct.product_name,
        category_id: parseInt(newProduct.category_id),
        description: newProduct.description || null,
        variants: newProduct.variants.length > 0 ? newProduct.variants : null
      };
      const res = await axios.post('http://127.0.0.1:8020/admin/products', payload, config);
      setSuccessMessage(`Product "${res.data.product_name}" added successfully!`);
      setNewProduct({ product_name: '', category_id: '', description: '', variants: [] });
      setNewVariant({ variant_name: '', price: '', quantity: '', SKU: '' });
      fetchProducts();
    } catch (err) {
      // Handle FastAPI validation errors
      if (err.response?.data?.detail) {
        if (Array.isArray(err.response.data.detail)) {
          // Format validation errors
          const errorMessages = err.response.data.detail.map(e => `${e.loc.join('.')}: ${e.msg}`).join(', ');
          setError(errorMessages);
        } else {
          setError(err.response.data.detail);
        }
      } else {
        setError('Failed to add product');
      }
    } finally { setLoading(false); }
  };

  const handleDeleteProduct = async (productId, productName) => {
    if (!window.confirm(`Are you sure you want to delete "${productName}"?`)) return;
    setLoading(true); setError(''); setSuccessMessage('');
    try {
      const config = axiosConfig();
      if (!config.headers.Authorization) { setError('Not authenticated. Please log in as admin.'); return; }
      await axios.delete(`http://127.0.0.1:8020/admin/products/${productId}`, config);
      setSuccessMessage(`Product "${productName}" deleted successfully!`);
      fetchProducts();
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to delete product');
    } finally { setLoading(false); }
  };

  const handleAddVariantToExistingProduct = async (e) => {
    e.preventDefault(); setLoading(true); setError(''); setSuccessMessage('');
    try {
      const config = axiosConfig();
      if (!config.headers.Authorization) { setError('Not authenticated. Please log in as admin.'); return; }
      
      const payload = {
        variant_name: addVariantToProduct.variant_name,
        price: parseFloat(addVariantToProduct.price),
        quantity: parseInt(addVariantToProduct.quantity),
        SKU: addVariantToProduct.SKU || null
      };
      
      const res = await axios.post(
        `http://127.0.0.1:8020/admin/products/${addVariantToProduct.product_id}/variants`,
        payload,
        config
      );
      
      setSuccessMessage(`Variant "${res.data.variant_name}" added successfully to product!`);
      setAddVariantToProduct({ product_id: '', variant_name: '', price: '', quantity: '', SKU: '' });
      
      // Refresh variants for this product if it's expanded
      if (expandedProducts[addVariantToProduct.product_id]) {
        fetchProductVariants(addVariantToProduct.product_id);
      }
      
      fetchVariants(); // Refresh all variants
    } catch (err) {
      if (err.response?.data?.detail) {
        if (Array.isArray(err.response.data.detail)) {
          const errorMessages = err.response.data.detail.map(e => `${e.loc.join('.')}: ${e.msg}`).join(', ');
          setError(errorMessages);
        } else {
          setError(err.response.data.detail);
        }
      } else {
        setError('Failed to add variant to product');
      }
    } finally { setLoading(false); }
  };

  const toggleProductVariants = async (productId) => {
    setExpandedProducts(prev => ({ ...prev, [productId]: !prev[productId] }));
    if (!expandedProducts[productId] && !productVariants[productId]) {
      await fetchProductVariants(productId);
    }
  };

  const fetchProductVariants = async (productId) => {
    try {
      const res = await axios.get(`http://127.0.0.1:8020/products/${productId}/variants/`);
      setProductVariants(prev => ({ ...prev, [productId]: res.data.variants || [] }));
    } catch (err) {
      setProductVariants(prev => ({ ...prev, [productId]: [] }));
    }
  };

  const handleUpdateVariantQuantity = async (e) => {
    e.preventDefault(); setLoading(true); setError(''); setSuccessMessage('');
    try {
      const config = axiosConfig();
      if (!config.headers.Authorization) { setError('Not authenticated. Please log in as admin.'); return; }
      const res = await axios.put(
        `http://127.0.0.1:8020/admin/variants/${variantUpdate.variant_id}/quantity?quantity=${variantUpdate.quantity}`,
        {},
        config
      );
      setSuccessMessage(`Variant quantity updated to ${res.data.quantity}!`);
      setVariantUpdate({ variant_id: '', quantity: '' });
      fetchVariants();
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to update variant quantity');
    } finally { setLoading(false); }
  };

  // Mark order as delivered (done)
  const markOrderDelivered = (orderId) => {
    setLoading(true); setError(''); setSuccessMessage('');
    const config = axiosConfig();
    if (!config.headers.Authorization) { setError('Not authenticated. Please log in as admin.'); setLoading(false); return; }
    axios.put(`http://127.0.0.1:8020/analytics/orders/${orderId}/status`, { status: 'Delivered' }, config)
      .then(() => {
        setSuccessMessage(`Order ${orderId} marked as Delivered`);
        fetchOrders();
      })
      .catch(err => {
        setError(err.response?.data?.detail || 'Failed to update order status');
      })
      .finally(() => setLoading(false));
  };

  // Mark payment as completed
  const markPaymentCompleted = (orderId) => {
    setLoading(true); setError(''); setSuccessMessage('');
    const config = axiosConfig();
    if (!config.headers.Authorization) { setError('Not authenticated. Please log in as admin.'); setLoading(false); return; }
    axios.put(`http://127.0.0.1:8020/admin/orders/${orderId}/payment-status`, {}, config)
      .then((response) => {
        setSuccessMessage(response.data.message || `Payment marked as completed for order ${orderId}`);
        fetchOrders();
      })
      .catch(err => {
        setError(err.response?.data?.detail || 'Failed to update payment status');
      })
      .finally(() => setLoading(false));
  };

  const toggleOrderItems = async (orderId) => {
    setExpandedOrders(prev => ({ ...prev, [orderId]: !prev[orderId] }));
    if (!expandedOrders[orderId] && !orderItems[orderId]) {
      try {
        const config = axiosConfig();
        const res = await axios.get(`http://127.0.0.1:8020/admin/orders/${orderId}/items`, config);
        setOrderItems(prev => ({ ...prev, [orderId]: res.data }));
      } catch {
        setOrderItems(prev => ({ ...prev, [orderId]: [] }));
        setError('Failed to fetch order items');
      }
    }
  };

  if (!isAdmin) return null;

  const renderUsers = () => (
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
  );

  const renderOrders = () => (
    <div className="orders-section">
      <h2>Orders</h2>
      <table className="table table-hover">
        <thead>
          <tr>
            <th>Order ID</th>
            <th>User ID</th>
            <th>Date</th>
            <th>Total</th>
            <th>Delivery Status</th>
            <th>Payment Method</th>
            <th>Payment Status</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {orders.map(o => (
            <React.Fragment key={o.order_id}>
              <tr>
                <td>{o.order_id}</td>
                <td>{o.user_id}</td>
                <td>{new Date(o.order_date).toLocaleDateString()}</td>
                <td>${parseFloat(o.total_amount).toFixed(2)}</td>
                <td>
                  <div className="d-flex align-items-center gap-2">
                    <span>{o.delivery_status ? (o.delivery_status.charAt(0).toUpperCase() + o.delivery_status.slice(1)) : 'N/A'}</span>
                    {(o.delivery_status || '').toLowerCase() !== 'delivered' && (
                      <button
                        className="btn btn-sm btn-success"
                        onClick={() => markOrderDelivered(o.order_id)}
                        disabled={loading}
                      >
                        Mark Done
                      </button>
                    )}
                  </div>
                </td>
                <td>{o.payment_method || 'N/A'}</td>
                <td>
                  <div className="d-flex align-items-center gap-2">
                    <span>{o.payment_status || 'N/A'}</span>
                    {(o.payment_status || '').toLowerCase() === 'pending' && (o.payment_method || '').toLowerCase() === 'cod' && (
                      <button
                        className="btn btn-sm btn-warning"
                        onClick={() => markPaymentCompleted(o.order_id)}
                        disabled={loading}
                      >
                        Mark Paid
                      </button>
                    )}
                  </div>
                </td>
                <td>
                  <button className="btn btn-sm btn-info" onClick={() => toggleOrderItems(o.order_id)}>
                    {expandedOrders[o.order_id] ? '▼ Hide Products' : '▶ View Products'}
                  </button>
                </td>
              </tr>
              {expandedOrders[o.order_id] && orderItems[o.order_id] && (
                <tr>
                  <td colSpan="8" style={{ backgroundColor: '#f8f9fa', padding: '15px' }}>
                    <h6>Order Items:</h6>
                    <table className="table table-sm table-bordered mb-0">
                      <thead>
                        <tr>
                          <th>Item ID</th>
                          <th>Product Name</th>
                          <th>Variant</th>
                          <th>SKU</th>
                          <th>Quantity</th>
                          <th>Price</th>
                          <th>Subtotal</th>
                        </tr>
                      </thead>
                      <tbody>
                        {orderItems[o.order_id].map(item => (
                          <tr key={item.order_item_id}>
                            <td>{item.order_item_id}</td>
                            <td>{item.product_name || 'N/A'}</td>
                            <td>{item.variant_name || 'N/A'}</td>
                            <td>{item.SKU || 'N/A'}</td>
                            <td>{item.quantity}</td>
                            <td>${parseFloat(item.price).toFixed(2)}</td>
                            <td>${(parseFloat(item.price) * item.quantity).toFixed(2)}</td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </td>
                </tr>
              )}
            </React.Fragment>
          ))}
        </tbody>
      </table>
    </div>
  );

  const renderProducts = () => (
    <div className="products-section">
      <h2>Products</h2>
      
      {/* Add Variant to Existing Product Section */}
      <div className="card mb-4">
        <div className="card-body">
          <h5 className="card-title">Add Variant to Existing Product</h5>
          <form onSubmit={handleAddVariantToExistingProduct}>
            <div className="row">
              <div className="col-md-2">
                <input
                  type="number"
                  className="form-control"
                  placeholder="Product ID"
                  value={addVariantToProduct.product_id}
                  onChange={(e) => setAddVariantToProduct({ ...addVariantToProduct, product_id: e.target.value })}
                  required
                />
              </div>
              <div className="col-md-3">
                <input
                  type="text"
                  className="form-control"
                  placeholder="Variant Name"
                  value={addVariantToProduct.variant_name}
                  onChange={(e) => setAddVariantToProduct({ ...addVariantToProduct, variant_name: e.target.value })}
                  required
                />
              </div>
              <div className="col-md-2">
                <input
                  type="number"
                  step="0.01"
                  className="form-control"
                  placeholder="Price"
                  value={addVariantToProduct.price}
                  onChange={(e) => setAddVariantToProduct({ ...addVariantToProduct, price: e.target.value })}
                  required
                />
              </div>
              <div className="col-md-2">
                <input
                  type="number"
                  className="form-control"
                  placeholder="Quantity"
                  value={addVariantToProduct.quantity}
                  onChange={(e) => setAddVariantToProduct({ ...addVariantToProduct, quantity: e.target.value })}
                  required
                />
              </div>
              <div className="col-md-2">
                <input
                  type="text"
                  className="form-control"
                  placeholder="SKU (optional)"
                  value={addVariantToProduct.SKU}
                  onChange={(e) => setAddVariantToProduct({ ...addVariantToProduct, SKU: e.target.value })}
                />
              </div>
              <div className="col-md-1">
                <button type="submit" className="btn btn-success w-100" disabled={loading}>Add</button>
              </div>
            </div>
          </form>
        </div>
      </div>

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
                  onChange={(e) => setNewProduct({ ...newProduct, product_name: e.target.value })}
                  required
                />
              </div>
              <div className="col-md-3">
                <select
                  className="form-select"
                  value={newProduct.category_id}
                  onChange={(e) => setNewProduct({ ...newProduct, category_id: e.target.value })}
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
                  onChange={(e) => setNewProduct({ ...newProduct, description: e.target.value })}
                />
              </div>
              <div className="col-md-2">
                <button type="submit" className="btn btn-primary w-100" disabled={loading}>Add Product</button>
              </div>
            </div>
            {/* Add Variant Section */}
            <div className="mt-3">
              <h6>Add Variants (optional)</h6>
              <div className="row">
                <div className="col-md-3">
                  <input
                    type="text"
                    className="form-control"
                    placeholder="Variant Name"
                    value={newVariant.variant_name}
                    onChange={(e) => setNewVariant({ ...newVariant, variant_name: e.target.value })}
                  />
                </div>
                <div className="col-md-2">
                  <input
                    type="number"
                    className="form-control"
                    placeholder="Price"
                    value={newVariant.price}
                    onChange={(e) => setNewVariant({ ...newVariant, price: e.target.value })}
                  />
                </div>
                <div className="col-md-2">
                  <input
                    type="number"
                    className="form-control"
                    placeholder="Quantity"
                    value={newVariant.quantity}
                    onChange={(e) => setNewVariant({ ...newVariant, quantity: e.target.value })}
                  />
                </div>
                <div className="col-md-3">
                  <input
                    type="text"
                    className="form-control"
                    placeholder="SKU (optional)"
                    value={newVariant.SKU}
                    onChange={(e) => setNewVariant({ ...newVariant, SKU: e.target.value })}
                  />
                </div>
                <div className="col-md-2">
                  <button
                    type="button"
                    className="btn btn-secondary w-100"
                    onClick={() => {
                      if (!newVariant.variant_name || !newVariant.price || !newVariant.quantity) return;
                      setNewProduct({
                        ...newProduct,
                        variants: [...newProduct.variants, {
                          variant_name: newVariant.variant_name,
                          price: parseFloat(newVariant.price),
                          quantity: parseInt(newVariant.quantity),
                          SKU: newVariant.SKU || null
                        }]
                      });
                      setNewVariant({ variant_name: '', price: '', quantity: '', SKU: '' });
                    }}
                  >Add Variant</button>
                </div>
              </div>
              {/* List added variants */}
              {newProduct.variants.length > 0 && (
                <div className="mt-2">
                  <ul className="list-group">
                    {newProduct.variants.map((v, idx) => (
                      <li key={idx} className="list-group-item d-flex justify-content-between align-items-center">
                        {v.variant_name} | Price: {v.price} | Qty: {v.quantity} | SKU: {v.SKU}
                        <button type="button" className="btn btn-sm btn-danger" onClick={() => {
                          setNewProduct({
                            ...newProduct,
                            variants: newProduct.variants.filter((_, i) => i !== idx)
                          });
                        }}>Remove</button>
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          </form>
        </div>
      </div>

      <div className="mb-3">
        <h5>Select Category</h5>
        <div className="btn-group" role="group">
          {categories.map(c => (
            <button
              key={c.category_id}
              className={`btn btn-outline-primary mx-1 ${c.category_id === selectedCategory ? 'active' : ''}`}
              onClick={() => setSelectedCategory(c.category_id)}
            >
              {c.category_name}
            </button>
          ))}
        </div>
      </div>

      {selectedCategory && (
        <table className="table table-striped">
          <thead>
            <tr>
              <th>Product ID</th>
              <th>Product Name</th>
              <th>Description</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {products.filter(p => p.category_id === selectedCategory).map(p => (
              <React.Fragment key={p.product_id}>
                <tr>
                  <td>{p.product_id}</td>
                  <td>{p.product_name}</td>
                  <td>{p.description || 'N/A'}</td>
                  <td>
                    <button 
                      className="btn btn-sm btn-info me-2" 
                      onClick={() => toggleProductVariants(p.product_id)}
                    >
                      {expandedProducts[p.product_id] ? '▼ Hide Variants' : '▶ View Variants'}
                    </button>
                    <button 
                      className="btn btn-sm btn-danger" 
                      onClick={() => handleDeleteProduct(p.product_id, p.product_name)} 
                      disabled={loading}
                    >
                      Delete
                    </button>
                  </td>
                </tr>
                {expandedProducts[p.product_id] && productVariants[p.product_id] && (
                  <tr>
                    <td colSpan="4" style={{ backgroundColor: '#f8f9fa', padding: '15px' }}>
                      <h6>Variants for {p.product_name}:</h6>
                      {productVariants[p.product_id].length > 0 ? (
                        <table className="table table-sm table-bordered mb-0">
                          <thead>
                            <tr>
                              <th>Variant ID</th>
                              <th>Variant Name</th>
                              <th>Price</th>
                              <th>Quantity</th>
                              <th>SKU</th>
                              <th>Actions</th>
                            </tr>
                          </thead>
                          <tbody>
                            {productVariants[p.product_id].map(variant => (
                              <tr key={variant.variant_id}>
                                <td>{variant.variant_id}</td>
                                <td>{variant.variant_name}</td>
                                <td>${parseFloat(variant.price).toFixed(2)}</td>
                                <td>{variant.quantity}</td>
                                <td>{variant.SKU || 'N/A'}</td>
                                <td>
                                  <button
                                    className="btn btn-sm btn-danger"
                                    onClick={async () => {
                                      if (!window.confirm(`Are you sure you want to delete variant '${variant.variant_name}'?`)) return;
                                      setLoading(true); setError(''); setSuccessMessage('');
                                      try {
                                        const config = axiosConfig();
                                        if (!config.headers.Authorization) { setError('Not authenticated. Please log in as admin.'); setLoading(false); return; }
                                        await axios.delete(`http://127.0.0.1:8020/admin/variants/${variant.variant_id}`, config);
                                        setSuccessMessage(`Variant '${variant.variant_name}' deleted successfully!`);
                                        fetchProductVariants(p.product_id);
                                        fetchVariants();
                                      } catch (err) {
                                        setError(err.response?.data?.detail || 'Failed to delete variant');
                                      } finally { setLoading(false); }
                                    }}
                                    disabled={loading}
                                  >Delete</button>
                                </td>
                              </tr>
                            ))}
                          </tbody>
                        </table>
                      ) : (
                        <p className="text-muted">No variants found for this product.</p>
                      )}
                    </td>
                  </tr>
                )}
              </React.Fragment>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );

  const renderQuantities = () => (
    <div className="quantities-section">
      <h2>Variant Quantities</h2>
      <div className="mb-3">
        <h5>Select Category</h5>
        <div className="btn-group" role="group">
          {categories.map(c => (
            <button
              key={c.category_id}
              className={`btn btn-outline-primary mx-1 ${c.category_id === selectedCategory ? 'active' : ''}`}
              onClick={() => setSelectedCategory(c.category_id)}
            >
              {c.category_name}
            </button>
          ))}
        </div>
      </div>

      {selectedCategory && (
        <table className="table table-bordered">
          <thead>
            <tr>
              <th>Variant ID</th>
              <th>Product ID</th>
              <th>Variant Name</th>
              <th>Quantity</th>
            </tr>
          </thead>
          <tbody>
            {(() => {
              const productIds = new Set(products.filter(p => p.category_id === selectedCategory).map(p => p.product_id));
              return variants
                .filter(v => productIds.has(v.product_id))
                .map(v => (
                  <tr key={v.variant_id}>
                    <td>{v.variant_id}</td>
                    <td>{v.product_id}</td>
                    <td>{v.variant_name}</td>
                    <td>{v.quantity}</td>
                  </tr>
                ));
            })()}
          </tbody>
        </table>
      )}

      <form className="row g-3 align-items-center" onSubmit={handleUpdateVariantQuantity}>
        <div className="col-auto">
          <input
            type="text"
            className="form-control"
            placeholder="Variant ID"
            value={variantUpdate.variant_id}
            onChange={(e) => setVariantUpdate({ ...variantUpdate, variant_id: e.target.value })}
            required
          />
        </div>
        <div className="col-auto">
          <input
            type="number"
            className="form-control"
            placeholder="New Quantity"
            value={variantUpdate.quantity}
            onChange={(e) => setVariantUpdate({ ...variantUpdate, quantity: e.target.value })}
            required
          />
        </div>
        <div className="col-auto">
          <button type="submit" className="btn btn-primary">Update Quantity</button>
        </div>
      </form>
    </div>
  );

  const downloadReport = async (endpoint, filename) => {
    setLoading(true); setError(''); setSuccessMessage('');
    try {
      const config = axiosConfig();
      if (!config.headers.Authorization) {
        setError('Not authenticated. Please log in as admin.');
        return;
      }

      const response = await axios.get(`http://127.0.0.1:8020${endpoint}`, {
        ...config,
        responseType: 'blob'
      });

      // Create download link
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', filename);
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);

      setSuccessMessage(`${filename} downloaded successfully!`);
    } catch (err) {
      setError(err.response?.data?.detail || `Failed to download ${filename}`);
    } finally {
      setLoading(false);
    }
  };

  const renderReports = () => (
    <div className="reports-section">
      <h2>Download Reports</h2>
      <p className="text-muted">Generate and download PDF reports for sales analysis and business insights.</p>

      <div className="row g-4">
        {/* Quarterly Sales Report */}
        <div className="col-md-12">
          <div className="card h-100">
            <div className="card-body">
              <h5 className="card-title">
                <i className="bi bi-calendar-range"></i> Quarterly Sales Report
              </h5>
              <p className="card-text">Get sales breakdown by quarter for a specific year.</p>
              <div className="mb-3">
                <label className="form-label">Year</label>
                <input
                  type="number"
                  className="form-control"
                  value={reportParams.year}
                  onChange={(e) => setReportParams({ ...reportParams, year: e.target.value })}
                  min="2020"
                  max="2030"
                />
              </div>
              <button
                className="btn btn-primary w-100"
                onClick={() => downloadReport(
                  `/reports/quarterly-sales/${reportParams.year}`,
                  `quarterly_sales_${reportParams.year}.pdf`
                )}
                disabled={loading || !reportParams.year}
              >
                <i className="bi bi-download"></i> Download Report
              </button>
            </div>
          </div>
        </div>

        {/* Top Selling Products */}
        <div className="col-md-12">
          <div className="card h-100">
            <div className="card-body">
              <h5 className="card-title">
                <i className="bi bi-trophy"></i> Top Selling Products
              </h5>
              <p className="card-text">View best-selling products with optional date filters.</p>
              <div className="mb-2">
                <label className="form-label">Start Date (Optional)</label>
                <input
                  type="date"
                  className="form-control"
                  value={reportParams.startDate}
                  onChange={(e) => setReportParams({ ...reportParams, startDate: e.target.value })}
                />
              </div>
              <div className="mb-2">
                <label className="form-label">End Date (Optional)</label>
                <input
                  type="date"
                  className="form-control"
                  value={reportParams.endDate}
                  onChange={(e) => setReportParams({ ...reportParams, endDate: e.target.value })}
                />
              </div>
              <div className="mb-3">
                <label className="form-label">Limit</label>
                <input
                  type="number"
                  className="form-control"
                  value={reportParams.limit}
                  onChange={(e) => setReportParams({ ...reportParams, limit: e.target.value })}
                  min="1"
                  max="100"
                />
              </div>
              <button
                className="btn btn-primary w-100"
                onClick={() => {
                  let endpoint = `/reports/top-selling-products?limit=${reportParams.limit}`;
                  if (reportParams.startDate) endpoint += `&start_date=${reportParams.startDate}`;
                  if (reportParams.endDate) endpoint += `&end_date=${reportParams.endDate}`;
                  downloadReport(endpoint, `top_selling_products.pdf`);
                }}
                disabled={loading}
              >
                <i className="bi bi-download"></i> Download Report
              </button>
            </div>
          </div>
        </div>

        {/* Category Orders Report */}
        <div className="col-md-12">
          <div className="card h-100">
            <div className="card-body">
              <h5 className="card-title">
                <i className="bi bi-tags"></i> Category-wise Orders
              </h5>
              <p className="card-text">Analyze total orders and revenue by product category.</p>
              <button
                className="btn btn-primary w-100"
                onClick={() => downloadReport(
                  `/reports/category-orders`,
                  `category_orders_report.pdf`
                )}
                disabled={loading}
              >
                <i className="bi bi-download"></i> Download Report
              </button>
            </div>
          </div>
        </div>

        {/* Customer Order Summary */}
        <div className="col-md-12">
          <div className="card h-100">
            <div className="card-body">
              <h5 className="card-title">
                <i className="bi bi-person-badge"></i> Customer Order Summary
              </h5>
              <p className="card-text">Get detailed order history and payment status for a specific customer.</p>
              <div className="mb-3">
                <label className="form-label">User ID</label>
                <input
                  type="number"
                  className="form-control"
                  value={reportParams.userId}
                  onChange={(e) => setReportParams({ ...reportParams, userId: e.target.value })}
                  placeholder="Enter customer user ID"
                />
              </div>
              <button
                className="btn btn-primary w-100"
                onClick={() => downloadReport(
                  `/reports/customer-orders/${reportParams.userId}`,
                  `customer_${reportParams.userId}_orders.pdf`
                )}
                disabled={loading || !reportParams.userId}
              >
                <i className="bi bi-download"></i> Download Report
              </button>
            </div>
          </div>
        </div>

        {/* All Customers Summary */}
        <div className="col-md-12">
          <div className="card">
            <div className="card-body">
              <h5 className="card-title">
                <i className="bi bi-people"></i> All Customers Summary
              </h5>
              <p className="card-text">Comprehensive report of top customers with order statistics and spending analysis.</p>
              <button
                className="btn btn-primary w-100"
                onClick={() => downloadReport(
                  `/reports/all-customers-summary`,
                  `all_customers_summary.pdf`
                )}
                disabled={loading}
              >
                <i className="bi bi-download"></i> Download Report
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );

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
          <button className={`nav-link ${activeTab === 'users' ? 'active' : ''}`} onClick={() => setActiveTab('users')}>Users</button>
        </li>
        <li className="nav-item">
          <button className={`nav-link ${activeTab === 'orders' ? 'active' : ''}`} onClick={() => setActiveTab('orders')}>Orders</button>
        </li>
        <li className="nav-item">
          <button className={`nav-link ${activeTab === 'products' ? 'active' : ''}`} onClick={() => setActiveTab('products')}>Products</button>
        </li>
        <li className="nav-item">
          <button className={`nav-link ${activeTab === 'quantities' ? 'active' : ''}`} onClick={() => setActiveTab('quantities')}>Quantities</button>
        </li>
        <li className="nav-item">
          <button className={`nav-link ${activeTab === 'reports' ? 'active' : ''}`} onClick={() => setActiveTab('reports')}>Reports</button>
        </li>
      </ul>

      {loading && <div className="text-center"><div className="spinner-border" role="status"></div></div>}

      {activeTab === 'users' && renderUsers()}
      {activeTab === 'orders' && renderOrders()}
      {activeTab === 'products' && renderProducts()}
      {activeTab === 'quantities' && renderQuantities()}
      {activeTab === 'reports' && renderReports()}
    </div>
  );
};

export default Admin;
