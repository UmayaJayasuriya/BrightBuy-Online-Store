/**
 * Products Data
 * Mock product data for the e-commerce site
 */
export const products = [
  {
    id: 1,
    name: 'Apple iPad Mini G2356',
    category: 'SmartPhone',
    price: 1050.00,
    oldPrice: 1250.00,
    discount: 16,
    rating: 4.5,
    reviews: 125,
    image: '/img/product-1.png',
    description: 'High-quality tablet with advanced features and sleek design.',
    inStock: true,
    features: ['10.5" Display', '256GB Storage', 'A15 Bionic Chip', '5G Capable']
  },
  {
    id: 2,
    name: 'Samsung Galaxy Tab',
    category: 'Tablets',
    price: 850.00,
    oldPrice: 950.00,
    discount: 11,
    rating: 4,
    reviews: 98,
    image: '/img/product-2.png',
    description: 'Premium Android tablet with stunning display.',
    inStock: true,
    features: ['11" Display', '128GB Storage', 'S Pen Included', 'WiFi 6']
  },
  {
    id: 3,
    name: 'Dell XPS 15 Laptop',
    category: 'Laptops & Desktops',
    price: 1899.00,
    oldPrice: 2199.00,
    discount: 14,
    rating: 5,
    reviews: 203,
    image: '/img/product-3.png',
    description: 'Powerful laptop for professionals and creators.',
    inStock: true,
    features: ['15.6" 4K Display', 'Intel i7', '16GB RAM', '512GB SSD']
  },
  {
    id: 4,
    name: 'Sony WH-1000XM5',
    category: 'Accessories',
    price: 399.00,
    oldPrice: 449.00,
    discount: 11,
    rating: 5,
    reviews: 542,
    image: '/img/product-4.png',
    description: 'Industry-leading noise canceling headphones.',
    inStock: true,
    features: ['30hr Battery', 'Active Noise Canceling', 'Touch Controls', 'Premium Sound']
  },
  {
    id: 5,
    name: 'iPhone 15 Pro Max',
    category: 'Mobiles & Tablets',
    price: 1299.00,
    oldPrice: 1399.00,
    discount: 7,
    rating: 5,
    reviews: 876,
    image: '/img/product-5.png',
    description: 'Latest flagship smartphone with titanium design.',
    inStock: true,
    features: ['6.7" Display', 'A17 Pro Chip', '256GB Storage', '5x Optical Zoom']
  },
  {
    id: 6,
    name: 'Samsung 65" Smart TV',
    category: 'SmartPhone & Smart TV',
    price: 1699.00,
    oldPrice: 1999.00,
    discount: 15,
    rating: 4.5,
    reviews: 321,
    image: '/img/product-6.png',
    description: '4K QLED Smart TV with incredible picture quality.',
    inStock: true,
    features: ['65" QLED', '4K Resolution', 'HDR10+', 'Smart Hub']
  },
  {
    id: 7,
    name: 'HP Pavilion Desktop',
    category: 'Laptops & Desktops',
    price: 899.00,
    oldPrice: 1099.00,
    discount: 18,
    rating: 4,
    reviews: 156,
    image: '/img/product-7.png',
    description: 'Reliable desktop computer for home and office.',
    inStock: true,
    features: ['Intel i5', '8GB RAM', '1TB HDD', 'Windows 11']
  },
  {
    id: 8,
    name: 'Logitech MX Master 3',
    category: 'Accessories',
    price: 99.00,
    oldPrice: 129.00,
    discount: 23,
    rating: 5,
    reviews: 678,
    image: '/img/product-8.png',
    description: 'Advanced wireless mouse for productivity.',
    inStock: true,
    features: ['Multi-Device', 'Ergonomic Design', 'USB-C Charging', 'Customizable Buttons']
  },
  {
    id: 9,
    name: 'MacBook Pro 16"',
    category: 'Laptops & Desktops',
    price: 2499.00,
    oldPrice: 2799.00,
    discount: 11,
    rating: 5,
    reviews: 432,
    image: '/img/product-9.png',
    description: 'Professional laptop with M3 Pro chip.',
    inStock: true,
    features: ['16" Liquid Retina', 'M3 Pro Chip', '18GB RAM', '512GB SSD']
  },
  {
    id: 10,
    name: 'Google Pixel 8',
    category: 'Mobiles & Tablets',
    price: 699.00,
    oldPrice: 799.00,
    discount: 13,
    rating: 4.5,
    reviews: 289,
    image: '/img/product-10.png',
    description: 'Smart Android phone with incredible AI features.',
    inStock: true,
    features: ['6.2" Display', 'Google Tensor G3', '128GB Storage', 'Advanced Camera']
  },
  {
    id: 11,
    name: 'iPad Pro 12.9"',
    category: 'Tablets',
    price: 1299.00,
    oldPrice: 1499.00,
    discount: 13,
    rating: 5,
    reviews: 567,
    image: '/img/product-11.png',
    description: 'Ultimate tablet for creative professionals.',
    inStock: true,
    features: ['12.9" Liquid Retina', 'M2 Chip', '256GB Storage', 'ProMotion Technology']
  },
  {
    id: 12,
    name: 'Bose QuietComfort Earbuds',
    category: 'Accessories',
    price: 279.00,
    oldPrice: 329.00,
    discount: 15,
    rating: 4.5,
    reviews: 423,
    image: '/img/product-12.png',
    description: 'Premium wireless earbuds with noise cancellation.',
    inStock: true,
    features: ['Active Noise Canceling', '6hr Battery', 'IPX4 Water Resistant', 'Touch Controls']
  }
];

/**
 * Get product by ID
 */
export const getProductById = (id) => {
  return products.find(product => product.id === parseInt(id));
};

/**
 * Get products by category
 */
export const getProductsByCategory = (category) => {
  if (!category || category === 'All Category') {
    return products;
  }
  return products.filter(product => product.category === category);
};

/**
 * Get featured/bestseller products
 */
export const getFeaturedProducts = () => {
  return products.filter(product => product.rating >= 4.5);
};
