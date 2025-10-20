/**
 * Single Product Page Component
 * Detailed product view with variants, images, description, and add to cart
 */
import React, { useState, useEffect } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import axios from 'axios';
import { useCart } from '../context/CartContext';
import { useAuth } from '../context/AuthContext';
import ProductCard from '../components/common/ProductCard';
import Spinner from '../components/common/Spinner';
import './Single.css';

const Single = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { addToCart, addToWishlist } = useCart();
  const { isAuthenticated, user, openLoginModal, isAdmin } = useAuth();
  const [productData, setProductData] = useState(null);
  const [selectedVariant, setSelectedVariant] = useState(null);
  const [quantity, setQuantity] = useState(1);
  const [relatedProducts, setRelatedProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [addingToCart, setAddingToCart] = useState(false);
  const [deletingVariant, setDeletingVariant] = useState(false);

  // Fetch product with variants
  useEffect(() => {
    const fetchProduct = async () => {
      setLoading(true);
      setError('');
      try {
        // Fetch product with variants
        const response = await axios.get(`http://127.0.0.1:8020/products/${id}/variants/`);
        setProductData(response.data);
        
        // Set first variant as selected by default
        if (response.data.variants && response.data.variants.length > 0) {
          setSelectedVariant(response.data.variants[0]);
        }

        // Fetch related products (from same category)
        if (response.data.category) {
          const relatedResponse = await axios.get(
            `http://127.0.0.1:8020/products/?category_name=${encodeURIComponent(response.data.category.category_name)}`
          );
          // Filter out current product and take first 4
          const related = relatedResponse.data.filter(p => p.product_id !== parseInt(id)).slice(0, 4);
          setRelatedProducts(related);
        }
      } catch (err) {
        console.error('Error fetching product:', err);
        setError('Failed to load product. Please try again.');
      } finally {
        setLoading(false);
      }
    };

    if (id) {
      fetchProduct();
    }
  }, [id]);

  const handleAddToCart = async () => {
    // Check if user is logged in
    if (!isAuthenticated) {
      // Open login modal instead of navigating away
      openLoginModal();
      return;
    }

    if (!selectedVariant) {
      alert('Please select a variant');
      return;
    }

    setAddingToCart(true);
    try {
      // Add to cart via backend API
      const response = await axios.post(
        `http://127.0.0.1:8020/cart/add?user_id=${user.user_id}`,
        {
          variant_id: selectedVariant.variant_id,
          quantity: quantity
        }
      );

      console.log('Added to cart:', response.data);
      
      // Also update local cart context for immediate UI feedback
      addToCart({
        ...productData,
        ...selectedVariant,
        name: `${productData.product_name} - ${selectedVariant.variant_name}`
      }, quantity);

      alert(`Added ${quantity} ${selectedVariant.variant_name} to cart!`);
      
    } catch (err) {
      console.error('Error adding to cart:', err);
      alert(err.response?.data?.detail || 'Failed to add to cart. Please try again.');
    } finally {
      setAddingToCart(false);
    }
  };

  const handleQuantityChange = (delta) => {
    const newQuantity = quantity + delta;
    if (newQuantity >= 1 && newQuantity <= (selectedVariant?.quantity || 1)) {
      setQuantity(newQuantity);
    }
  };

  const handleVariantSelect = (variant) => {
    setSelectedVariant(variant);
    setQuantity(1); // Reset quantity when changing variant
  };

  const handleDeleteVariant = async () => {
    if (!selectedVariant) {
      alert('Please select a variant to delete');
      return;
    }

    const confirmDelete = window.confirm(
      `Are you sure you want to delete the variant "${selectedVariant.variant_name}"?\n\nThis action cannot be undone.`
    );

    if (!confirmDelete) {
      return;
    }

    setDeletingVariant(true);
    try {
      const token = localStorage.getItem('token');
      
      // Check if token exists
      if (!token) {
        alert('You are not logged in. Please log in as an admin to delete variants.');
        navigate('/');
        return;
      }

      console.log('Deleting variant with token:', token.substring(0, 20) + '...');
      
      await axios.delete(
        `http://127.0.0.1:8020/admin/variants/${selectedVariant.variant_id}`,
        {
          headers: {
            Authorization: `Bearer ${token}`
          }
        }
      );

      alert(`Variant "${selectedVariant.variant_name}" deleted successfully!`);
      
      // Refresh the product data to show updated variants
      const response = await axios.get(`http://127.0.0.1:8020/products/${id}/variants/`);
      setProductData(response.data);
      
      // Select first remaining variant or reload to show "No variants available"
      if (response.data.variants && response.data.variants.length > 0) {
        setSelectedVariant(response.data.variants[0]);
      } else {
        setSelectedVariant(null);
        // Page will now show "No variants available" message with Go Back button
      }
      
    } catch (err) {
      console.error('Error deleting variant:', err);
      const errorMessage = err.response?.data?.detail || 'Failed to delete variant. Please try again.';
      
      // Show a more user-friendly error message for order-related deletions
      if (errorMessage.includes('existing orders') || errorMessage.includes('part of existing orders')) {
        alert(
          `The variant "${selectedVariant.variant_name}" cannot be deleted because it is part of existing customer orders.`
        );
      } else {
        alert(`Error: ${errorMessage}`);
      }
    } finally {
      setDeletingVariant(false);
    }
  };

  if (loading) {
    return (
      <div className="container py-5">
        <div className="text-center">
          <Spinner />
        </div>
      </div>
    );
  }

  if (error || !productData) {
    return (
      <div className="container py-5 text-center">
        <h2>{error || 'Product not found'}</h2>
        <Link to="/shop" className="btn btn-primary mt-3">
          Back to Shop
        </Link>
      </div>
    );
  }

  // Check if product has no variants
  if (!productData.variants || productData.variants.length === 0) {
    return (
      <div className="single-page">
        {/* Page Header */}
        <div className="container-fluid page-header py-5" style={{
          backgroundImage: 'url(/img/topbar.png)',
          backgroundSize: 'cover',
          backgroundPosition: 'center',
          backgroundRepeat: 'no-repeat',
          position: 'relative',
          minHeight: '260px'
        }}>
          <div style={{
            position: 'absolute',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            backgroundColor: 'rgba(0, 0, 0, 0.45)',
            zIndex: 1
          }}></div>
          <div className="container text-center py-5" style={{ position: 'relative', zIndex: 2 }}>
            <h1 className="display-4 text-white mb-3 fw-bolder">{productData.product_name}</h1>
            <nav aria-label="breadcrumb">
              <ol className="breadcrumb justify-content-center mb-0">
                <li className="breadcrumb-item"><Link to="/" className="text-white">Home</Link></li>
                <li className="breadcrumb-item"><Link to="/shop" className="text-white">Shop</Link></li>
                <li className="breadcrumb-item active text-white">{productData.product_name}</li>
              </ol>
            </nav>
          </div>
        </div>

        {/* No Variants Available Message */}
        <div className="container py-5">
          <div className="row justify-content-center">
            <div className="col-lg-8 text-center">
              <div className="card shadow-sm p-5">
                <div className="mb-4">
                  <i className="fas fa-box-open fa-5x text-muted mb-3"></i>
                </div>
                <h2 className="mb-3">No Variants Available</h2>
                <p className="text-muted mb-4">
                  Unfortunately, there are currently no available variants for this product. 
                  {isAdmin && " As an admin, you can add new variants to make this product available for purchase."}
                </p>
                <div className="d-flex gap-3 justify-content-center">
                  <button 
                    onClick={() => navigate(-1)} 
                    className="btn btn-secondary px-4"
                  >
                    <i className="fas fa-arrow-left me-2"></i>
                    Go Back
                  </button>
                  <Link to="/shop" className="btn btn-primary px-4">
                    <i className="fas fa-shopping-bag me-2"></i>
                    Continue Shopping
                  </Link>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="single-page">
      {/* Page Header */}
      <div className="container-fluid page-header py-5" style={{
        backgroundImage: 'url(/img/topbar.png)',
        backgroundSize: 'cover',
        backgroundPosition: 'center',
        backgroundRepeat: 'no-repeat',
        position: 'relative',
        minHeight: '260px'
      }}>
        <div style={{
          position: 'absolute',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          backgroundColor: 'rgba(0, 0, 0, 0.45)',
          zIndex: 1
        }}></div>
        <div className="container text-center py-5" style={{ position: 'relative', zIndex: 2 }}>
          <h1 className="display-4 text-white mb-3 fw-bolder">{productData.product_name}</h1>
          <nav aria-label="breadcrumb">
            <ol className="breadcrumb justify-content-center mb-0">
              <li className="breadcrumb-item"><Link to="/" className="text-white">Home</Link></li>
              <li className="breadcrumb-item"><Link to="/shop" className="text-white">Shop</Link></li>
              <li className="breadcrumb-item active text-white">{productData.product_name}</li>
            </ol>
          </nav>
        </div>
      </div>

      {/* Product Details */}
      <div className="container-fluid py-5">
        <div className="container py-5">
          <div className="row g-4 mb-5">
            {/* Product Image */}
            <div className="col-lg-6">
              <div className="product-images">
                <div className="main-image mb-3">
                  <img
                    src={selectedVariant ? `/img/variants/${selectedVariant.variant_id}.png` : `/img/products/${productData.product_id}.png`}
                    className="img-fluid rounded"
                    alt={selectedVariant?.variant_name || productData.product_name}
                    style={{ width: '100%', height: '350px', objectFit: 'contain', backgroundColor: '#f8f9fa', padding: '20px' }}
                    onError={(e) => {
                      if (e.target.src.endsWith('.png')) {
                        e.target.src = selectedVariant ? `/img/variants/${selectedVariant.variant_id}.jpg` : `/img/products/${productData.product_id}.jpg`;
                      } else {
                        e.target.src = '/img/product-1.png';
                      }
                    }}
                  />
                </div>
                
                {/* Variant Thumbnails */}
                {productData.variants && productData.variants.length > 0 && (
                  <div className="variant-thumbnails d-flex gap-3 justify-content-center flex-wrap">
                    {productData.variants.map((variant) => (
                      <div
                        key={variant.variant_id}
                        className={`variant-thumbnail ${
                          selectedVariant?.variant_id === variant.variant_id ? 'border-primary border-3' : 'border'
                        }`}
                        style={{
                          width: '150px',
                          height: '150px',
                          cursor: 'pointer',
                          borderRadius: '8px',
                          overflow: 'hidden',
                          transition: 'all 0.3s ease',
                          position: 'relative'
                        }}
                        onClick={() => handleVariantSelect(variant)}
                      >
                        <img
                          src={`/img/variants/${variant.variant_id}.png`}
                          className="img-fluid w-100 h-100"
                          alt={variant.variant_name}
                          style={{ objectFit: 'contain', backgroundColor: '#f8f9fa', padding: '10px' }}
                          onError={(e) => {
                            if (e.target.src.endsWith('.png')) {
                              e.target.src = `/img/variants/${variant.variant_id}.jpg`;
                            } else {
                              e.target.src = '/img/product-1.png';
                            }
                          }}
                        />
                        {/* Out of Stock Badge */}
                        {variant.quantity < 1 && (
                          <div
                            style={{
                              position: 'absolute',
                              top: '5px',
                              right: '5px',
                              backgroundColor: '#dc3545',
                              color: 'white',
                              padding: '4px 8px',
                              borderRadius: '4px',
                              fontSize: '12px',
                              fontWeight: 'bold',
                              zIndex: 10
                            }}
                          >
                            Out of Stock
                          </div>
                        )}
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>

            {/* Product Info */}
            <div className="col-lg-6">
              <div className="product-details">
                <h2 className="mb-3">{productData.product_name}</h2>
                
                {selectedVariant && (
                  <div className="mb-3">
                    <h5 className="text-primary">{selectedVariant.variant_name}</h5>
                  </div>
                )}

                {/* Price & SKU */}
                {selectedVariant && (
                  <div className="mb-4">
                    <div className="d-flex align-items-center gap-3 mb-2">
                      <span className="text-primary fw-bold fs-2">
                        ${parseFloat(selectedVariant.price).toFixed(2)}
                      </span>
                    </div>
                    <p className="text-muted mb-0">
                      <strong>SKU:</strong> {selectedVariant.SKU}
                    </p>
                  </div>
                )}

                {/* Variant Attributes */}
                {selectedVariant && selectedVariant.attributes && selectedVariant.attributes.length > 0 && (
                  <div className="mb-4">
                    <h5>Specifications:</h5>
                    <div className="table-responsive">
                      <table className="table table-borderless">
                        <tbody>
                          {selectedVariant.attributes.map((attr, index) => (
                            <tr key={index}>
                              <td className="fw-bold" style={{ width: '40%' }}>{attr.attribute_name}:</td>
                              <td>{attr.value}</td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  </div>
                )}

                {/* Description */}
                {productData.description && (
                  <div className="mb-4">
                    <h5>Description:</h5>
                    <p>{productData.description}</p>
                  </div>
                )}

                {/* Category & Stock */}
                <div className="mb-4">
                  {productData.category && (
                    <p className="mb-2">
                      <strong>Category:</strong>{' '}
                      <span className="text-capitalize">{productData.category.category_name}</span>
                    </p>
                  )}
                  {selectedVariant && (
                    <p className="mb-0">
                      <strong>Availability:</strong>{' '}
                      <span className={selectedVariant.quantity > 0 ? 'text-success' : 'text-danger'}>
                        {selectedVariant.quantity > 0 ? `In Stock (${selectedVariant.quantity} available)` : 'Out of Stock'}
                      </span>
                    </p>
                  )}
                </div>

                {/* Quantity Selector */}
                {selectedVariant && selectedVariant.quantity > 0 && (
                  <div className="quantity-selector mb-4">
                    <label className="mb-2"><strong>Quantity:</strong></label>
                    <div className="d-flex align-items-center gap-3">
                      <div className="input-group" style={{ width: '150px' }}>
                        <button
                          className="btn btn-outline-secondary"
                          onClick={() => handleQuantityChange(-1)}
                          disabled={quantity <= 1}
                        >
                          <i className="fas fa-minus"></i>
                        </button>
                        <input
                          type="number"
                          className="form-control text-center"
                          value={quantity}
                          min="1"
                          max={selectedVariant.quantity}
                          onChange={(e) => {
                            const val = parseInt(e.target.value) || 1;
                            setQuantity(Math.min(Math.max(1, val), selectedVariant.quantity));
                          }}
                        />
                        <button
                          className="btn btn-outline-secondary"
                          onClick={() => handleQuantityChange(1)}
                          disabled={quantity >= selectedVariant.quantity}
                        >
                          <i className="fas fa-plus"></i>
                        </button>
                      </div>
                    </div>
                  </div>
                )}

                {/* Action Buttons */}
                <div className="d-flex gap-3 mb-4">
                  {isAdmin ? (
                    <button
                      className="btn btn-danger btn-lg flex-grow-1"
                      onClick={handleDeleteVariant}
                      disabled={!selectedVariant || deletingVariant}
                    >
                      <i className="fas fa-trash me-2"></i>
                      {deletingVariant ? 'Deleting...' : 'Delete Variant'}
                    </button>
                  ) : (
                    <button
                      className="btn btn-primary btn-lg flex-grow-1"
                      onClick={handleAddToCart}
                      disabled={!selectedVariant || selectedVariant.quantity === 0 || addingToCart}
                    >
                      <i className="fas fa-shopping-cart me-2"></i>
                      {addingToCart ? 'Adding...' : 
                       selectedVariant && selectedVariant.quantity > 0 ? 'Add to Cart' : 'Out of Stock'}
                    </button>
                  )}
                </div>
              </div>
            </div>
          </div>

          {/* Related Products */}
          {relatedProducts.length > 0 && (
            <div className="related-products mt-5">
              <h3 className="mb-4">Related Products</h3>
              <div className="row g-4">
                {relatedProducts.map((relatedProduct) => (
                  <div key={relatedProduct.product_id} className="col-md-6 col-lg-3">
                    <ProductCard product={relatedProduct} />
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Single;
