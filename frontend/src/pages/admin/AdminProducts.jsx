/**
 * Product Management Component
 * Admin interface for managing products
 */
import React, { useState, useEffect } from 'react';
import { useAuth } from '../../context/AuthContext';
import './AdminProducts.css';

const AdminProducts = () => {
  const { makeAuthenticatedRequest, hasAdminPrivileges } = useAuth();
  const [products, setProducts] = useState([]);
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [editingProduct, setEditingProduct] = useState(null);

  useEffect(() => {
    if (hasAdminPrivileges) {
      fetchProducts();
      fetchCategories();
    }
  }, [hasAdminPrivileges]);

  const fetchProducts = async () => {
    try {
      setLoading(true);
  const response = await makeAuthenticatedRequest('/admin/products');
      
      if (response.ok) {
        const data = await response.json();
        setProducts(data);
      } else {
        setError('Failed to fetch products');
      }
    } catch (err) {
      setError('Error loading products: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  const fetchCategories = async () => {
    try {
      const response = await fetch('http://127.0.0.1:8020/categories/');
      if (response.ok) {
        const data = await response.json();
        setCategories(data);
      }
    } catch (err) {
      console.error('Error fetching categories:', err);
    }
  };

  const handleUpdateProduct = async (productId) => {
    try {
      const updateData = {
        product_name: editingProduct.product_name,
        price: parseFloat(editingProduct.price),
        description: editingProduct.description,
        category_id: parseInt(editingProduct.category_id),
        stock_quantity: parseInt(editingProduct.stock_quantity) || 0
      };

  const response = await makeAuthenticatedRequest(`/admin/products/${productId}`, {
        method: 'PUT',
        body: JSON.stringify(updateData)
      });

      if (response.ok) {
        setEditingProduct(null);
        fetchProducts();
      } else {
        const errorData = await response.json();
        setError(errorData.detail || 'Failed to update product');
      }
    } catch (err) {
      setError('Error updating product: ' + err.message);
    }
  };

  const handleDeleteProduct = async (productId) => {
    if (window.confirm('Are you sure you want to delete this product?')) {
      try {
  const response = await makeAuthenticatedRequest(`/admin/products/${productId}`, {
          method: 'DELETE'
        });

        if (response.ok) {
          fetchProducts();
        } else {
          const errorData = await response.json();
          setError(errorData.detail || 'Failed to delete product');
        }
      } catch (err) {
        setError('Error deleting product: ' + err.message);
      }
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setEditingProduct({ ...editingProduct, [name]: value });
  };

  const getCategoryName = (categoryId) => {
    const category = categories.find(cat => cat.category_id === categoryId);
    return category ? category.category_name : 'Unknown';
  };

  if (!hasAdminPrivileges) {
    return (
      <div className="admin-access-denied">
        <h2>Access Denied</h2>
        <p>You don't have permission to manage products.</p>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="admin-loading">
        <div className="spinner"></div>
        <p>Loading products...</p>
      </div>
    );
  }

  return (
    <div className="admin-products">
      <div className="admin-header">
        <h1>Product Management</h1>
        <div className="header-stats">
          <span className="stat">Total Products: {products.length}</span>
          <span className="stat">
            Low Stock: {products.filter(p => p.stock_quantity < 10).length}
          </span>
        </div>
      </div>

      {error && (
        <div className="alert alert-danger">
          {error}
          <button className="close-btn" onClick={() => setError('')}>×</button>
        </div>
      )}

      <div className="products-table-container">
        <table className="products-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Product Name</th>
              <th>Price</th>
              <th>Category</th>
              <th>Stock</th>
              <th>Description</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {products.map(product => (
              <tr key={product.product_id} className={product.stock_quantity < 10 ? 'low-stock' : ''}>
                <td>{product.product_id}</td>
                <td>
                  {editingProduct?.product_id === product.product_id ? (
                    <input
                      type="text"
                      name="product_name"
                      value={editingProduct.product_name}
                      onChange={handleInputChange}
                    />
                  ) : (
                    product.product_name
                  )}
                </td>
                <td>
                  {editingProduct?.product_id === product.product_id ? (
                    <input
                      type="number"
                      name="price"
                      value={editingProduct.price}
                      onChange={handleInputChange}
                      step="0.01"
                      min="0"
                    />
                  ) : (
                    `$${product.price}`
                  )}
                </td>
                <td>
                  {editingProduct?.product_id === product.product_id ? (
                    <select
                      name="category_id"
                      value={editingProduct.category_id}
                      onChange={handleInputChange}
                    >
                      {categories.map(category => (
                        <option key={category.category_id} value={category.category_id}>
                          {category.category_name}
                        </option>
                      ))}
                    </select>
                  ) : (
                    getCategoryName(product.category_id)
                  )}
                </td>
                <td>
                  {editingProduct?.product_id === product.product_id ? (
                    <input
                      type="number"
                      name="stock_quantity"
                      value={editingProduct.stock_quantity}
                      onChange={handleInputChange}
                      min="0"
                    />
                  ) : (
                    <span className={product.stock_quantity < 10 ? 'low-stock-text' : ''}>
                      {product.stock_quantity}
                    </span>
                  )}
                </td>
                <td>
                  {editingProduct?.product_id === product.product_id ? (
                    <textarea
                      name="description"
                      value={editingProduct.description}
                      onChange={handleInputChange}
                      rows="2"
                    />
                  ) : (
                    <div className="description-cell">
                      {product.description && product.description.length > 50
                        ? `${product.description.substring(0, 50)}...`
                        : product.description || 'No description'
                      }
                    </div>
                  )}
                </td>
                <td>
                  <div className="action-buttons">
                    {editingProduct?.product_id === product.product_id ? (
                      <>
                        <button
                          className="save-btn"
                          onClick={() => handleUpdateProduct(product.product_id)}
                        >
                          Save
                        </button>
                        <button
                          className="cancel-btn"
                          onClick={() => setEditingProduct(null)}
                        >
                          Cancel
                        </button>
                      </>
                    ) : (
                      <>
                        <button
                          className="edit-btn"
                          onClick={() => setEditingProduct(product)}
                        >
                          Edit
                        </button>
                        <button
                          className="delete-btn"
                          onClick={() => handleDeleteProduct(product.product_id)}
                        >
                          Delete
                        </button>
                      </>
                    )}
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {products.length === 0 && !loading && (
        <div className="no-products">
          <i className="fas fa-box-open"></i>
          <h3>No products found</h3>
          <p>Start by adding some products to your inventory.</p>
        </div>
      )}
    </div>
  );
};

export default AdminProducts;