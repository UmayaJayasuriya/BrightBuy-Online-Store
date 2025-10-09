/**
 * Single Product Page Component
 * Detailed product view with images, description, and add to cart
 */
import React, { useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { useCart } from '../context/CartContext';
import { getProductById, products } from '../data/products';
import ProductCard from '../components/common/ProductCard';
import './Single.css';

const Single = () => {
  const { id } = useParams();
  const product = getProductById(id);
  const { addToCart, addToWishlist } = useCart();
  const [quantity, setQuantity] = useState(1);
  const [selectedImage, setSelectedImage] = useState(0);

  if (!product) {
    return (
      <div className="container py-5 text-center">
        <h2>Product not found</h2>
        <Link to="/shop" className="btn btn-primary mt-3">
          Back to Shop
        </Link>
      </div>
    );
  }

  const relatedProducts = products.filter(
    (p) => p.category === product.category && p.id !== product.id
  ).slice(0, 4);

  const handleAddToCart = () => {
    addToCart(product, quantity);
  };

  const handleQuantityChange = (delta) => {
    const newQuantity = quantity + delta;
    if (newQuantity >= 1) {
      setQuantity(newQuantity);
    }
  };

  const productImages = [product.image, product.image, product.image]; // Mock multiple images

  return (
    <div className="single-page">
      {/* Page Header */}
      <div className="container-fluid page-header py-5" style={{
        backgroundImage: 'url(/img/carousel-1.jpg)',
        backgroundSize: '250%',
        backgroundPosition: 'center 10%',
        backgroundRepeat: 'no-repeat',
        position: 'relative'
      }}>
        <div style={{
          position: 'absolute',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          backgroundColor: 'rgba(0, 0, 0, 0.5)',
          zIndex: 1
        }}></div>
        <div className="container text-center py-5" style={{ position: 'relative', zIndex: 2 }}>
          <h1 className="display-4 text-white mb-3" style={{ fontWeight: '700' }}>Single Product</h1>
          <nav aria-label="breadcrumb">
            <ol className="breadcrumb justify-content-center mb-0">
              <li className="breadcrumb-item"><Link to="/">Home</Link></li>
              <li className="breadcrumb-item"><Link to="/shop">Pages</Link></li>
              <li className="breadcrumb-item active text-white">Single Product</li>
            </ol>
          </nav>
        </div>
      </div>

      {/* Product Details */}
      <div className="container-fluid py-5">
        <div className="container py-5">
          <div className="row g-4 mb-5">
            {/* Product Images */}
            <div className="col-lg-6">
              <div className="product-images">
                <div className="main-image mb-3">
                  <img
                    src={productImages[selectedImage]}
                    className="img-fluid rounded"
                    alt={product.name}
                  />
                </div>
                <div className="image-thumbnails d-flex gap-2">
                  {productImages.map((img, index) => (
                    <img
                      key={index}
                      src={img}
                      className={`img-thumbnail cursor-pointer ${
                        selectedImage === index ? 'border-primary' : ''
                      }`}
                      style={{ width: '100px', height: '100px', objectFit: 'cover' }}
                      alt={`${product.name} ${index + 1}`}
                      onClick={() => setSelectedImage(index)}
                    />
                  ))}
                </div>
              </div>
            </div>

            {/* Product Info */}
            <div className="col-lg-6">
              <div className="product-details">
                <h2 className="mb-3">{product.name}</h2>
                
                {/* Rating */}
                <div className="d-flex align-items-center mb-3">
                  <div className="text-warning me-2">
                    {'★'.repeat(Math.floor(product.rating))}
                    {'☆'.repeat(5 - Math.floor(product.rating))}
                  </div>
                  <span className="text-muted">({product.reviews} reviews)</span>
                </div>

                {/* Price */}
                <div className="mb-4">
                  {product.oldPrice && (
                    <del className="me-3 text-muted fs-4">${product.oldPrice.toFixed(2)}</del>
                  )}
                  <span className="text-primary fw-bold fs-2">${product.price.toFixed(2)}</span>
                  {product.discount && (
                    <span className="badge bg-danger ms-3">{product.discount}% OFF</span>
                  )}
                </div>

                {/* Description */}
                <p className="mb-4">{product.description}</p>

                {/* Features */}
                <div className="mb-4">
                  <h5>Key Features:</h5>
                  <ul>
                    {product.features.map((feature, index) => (
                      <li key={index}>{feature}</li>
                    ))}
                  </ul>
                </div>

                {/* Category & Stock */}
                <div className="mb-4">
                  <p className="mb-2">
                    <strong>Category:</strong>{' '}
                    <Link to={`/shop?category=${product.category}`}>{product.category}</Link>
                  </p>
                  <p className="mb-0">
                    <strong>Availability:</strong>{' '}
                    <span className={product.inStock ? 'text-success' : 'text-danger'}>
                      {product.inStock ? 'In Stock' : 'Out of Stock'}
                    </span>
                  </p>
                </div>

                {/* Quantity Selector */}
                <div className="quantity-selector mb-4">
                  <label className="mb-2"><strong>Quantity:</strong></label>
                  <div className="d-flex align-items-center gap-3">
                    <div className="input-group" style={{ width: '150px' }}>
                      <button
                        className="btn btn-outline-secondary"
                        onClick={() => handleQuantityChange(-1)}
                      >
                        <i className="fas fa-minus"></i>
                      </button>
                      <input
                        type="number"
                        className="form-control text-center"
                        value={quantity}
                        onChange={(e) => setQuantity(Math.max(1, parseInt(e.target.value) || 1))}
                      />
                      <button
                        className="btn btn-outline-secondary"
                        onClick={() => handleQuantityChange(1)}
                      >
                        <i className="fas fa-plus"></i>
                      </button>
                    </div>
                  </div>
                </div>

                {/* Action Buttons */}
                <div className="d-flex gap-3 mb-4">
                  <button
                    className="btn btn-primary btn-lg flex-grow-1"
                    onClick={handleAddToCart}
                    disabled={!product.inStock}
                  >
                    <i className="fas fa-shopping-cart me-2"></i>
                    Add to Cart
                  </button>
                  <button
                    className="btn btn-outline-primary btn-lg"
                    onClick={() => addToWishlist(product)}
                  >
                    <i className="fas fa-heart"></i>
                  </button>
                </div>

                {/* Social Share */}
                <div className="social-share">
                  <strong>Share:</strong>
                  <div className="d-inline-flex gap-2 ms-3">
                    <a href="#facebook" className="btn btn-sm btn-outline-primary rounded-circle">
                      <i className="fab fa-facebook-f"></i>
                    </a>
                    <a href="#twitter" className="btn btn-sm btn-outline-info rounded-circle">
                      <i className="fab fa-twitter"></i>
                    </a>
                    <a href="#pinterest" className="btn btn-sm btn-outline-danger rounded-circle">
                      <i className="fab fa-pinterest"></i>
                    </a>
                  </div>
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
                  <div key={relatedProduct.id} className="col-md-6 col-lg-3">
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
