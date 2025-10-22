# 🛍️ BrightBuy Online Store# BrightBuy-Online-Store

Full-stack Retail Inventory &amp; Online Order Management System for BrightBuy. Built with FastAPI, MySQL, and React, it supports product browsing, cart &amp; checkout, stock validation, delivery estimation, payment simulation, admin reporting, and **admin privileges with JWT authentication**.

A full-stack e-commerce platform designed for seamless online shopping with robust inventory management, order tracking, and admin capabilities.

## 🔐 New: Admin Features

## 📋 Project OverviewBrightBuy now includes a complete admin dashboard with role-based access control:

- **View Users** - Monitor all registered users and their roles

BrightBuy is a modern retail e-commerce system that provides a complete shopping experience for customers and comprehensive management tools for administrators. Built with cutting-edge technologies, it combines a responsive React frontend with a powerful FastAPI backend and MySQL database.- **View Orders** - Track orders with delivery and payment status

- **Add Products** - Create new products with categories

### Key Features- **Delete Products** - Remove products from catalog

- **Update Quantities** - Manage variant stock levels

#### 🛒 Customer Features

- **Product Browsing** - Browse products by category with intuitive filtering### Quick Start for Admins

- **Search & Filter** - Find products by name and category```bash

- **Shopping Cart** - Add/remove products with real-time quantity management# 1. Install dependencies

- **Checkout Process** - Streamlined multi-step checkout with order summarypip install python-jose[cryptography] mysql-connector-python

- **Payment Integration** - Simulated payment gateway for secure transactions

- **Wishlist/Favorites** - Save favorite products for later# 2. Create admin user

- **Order Tracking** - Monitor order status and delivery informationpython backend/database/create_admin_helper.py

- **User Accounts** - Register, login, and manage profile information

- **Delivery Estimation** - Automatic delivery date calculation# 3. Start servers

- **Contact Support** - Direct messaging system to support teamcd backend && python app/main.py # Terminal 1

cd frontend && npm start # Terminal 2

#### 👨‍💼 Admin Features

- **Dashboard Overview** - Key metrics and business analytics# 4. Login as admin at http://localhost:3000

- **User Management** - View and manage customer accounts# 5. Click "Admin Dashboard" link in header

- **Product Management** - Add, edit, delete products with variants```

- **Inventory Control** - Real-time stock level management

- **Order Management** - Track and update order status**Documentation**: See [ADMIN_DOCS_INDEX.md](ADMIN_DOCS_INDEX.md) for complete admin documentation or [START_HERE.md](START_HERE.md) for a 3-step quick start.

- **Delivery Management** - Manage delivery information and status
- **Sales Analytics** - View bestsellers, revenue reports, and trends
- **Report Generation** - Generate comprehensive business reports
- **Two-Factor Authentication** - Enhanced security for admin accounts
- **Role-Based Access Control** - JWT authentication and authorization

#### 📊 Advanced Features

- **Product Variants** - Support for different sizes, colors, and configurations
- **Order Details Tracking** - Line-item level order information
- **Delivery Status Updates** - Real-time delivery tracking
- **CVV Validation** - Payment security validation
- **Quarterly Reports** - Business performance analysis
- **Stock Triggers** - Automatic alerts for low stock levels

## 🏗️ Architecture

### Tech Stack

**Frontend:**

- React 18+ - UI library
- React Router - Client-side routing
- Axios - HTTP client for API communication
- Bootstrap 5 - Responsive styling and components
- CSS3 - Modern styling

**Backend:**

- FastAPI - Python web framework
- MySQL - Relational database
- SQLAlchemy - ORM (where applicable)
- JWT (Python-Jose) - Authentication and authorization
- CORS Middleware - Cross-origin support

**DevOps:**

- Docker & Docker Compose - Containerization
- MySQL Docker Container - Database service
- Multi-stage builds - Optimized container images

### Directory Structure

```
BrightBuy-Online-Store/
├── frontend/                    # React application
│   ├── src/
│   │   ├── pages/             # Page components (Shop, Home, Admin, etc.)
│   │   ├── components/        # Reusable components
│   │   ├── context/           # React context (Auth, Cart)
│   │   ├── styles/            # CSS files
│   │   └── App.jsx            # Main app component
│   ├── package.json           # Dependencies
│   └── Dockerfile             # Frontend Docker configuration
│
├── backend/                     # FastAPI application
│   ├── app/
│   │   ├── main.py            # FastAPI app entry point
│   │   ├── database.py        # Database connection
│   │   ├── security.py        # JWT authentication
│   │   ├── routes/            # API endpoints (products, users, orders, etc.)
│   │   ├── schemas/           # Pydantic models
│   │   ├── services/          # Business logic
│   │   └── utils/             # Helper functions
│   ├── database/              # Database setup and migrations
│   ├── requirements.txt       # Python dependencies
│   ├── Dockerfile             # Backend Docker configuration
│   └── procfile               # Deployment configuration
│
├── docker-compose.yml         # Multi-container orchestration
└── README.md                  # This file
```

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- Node.js 16+
- MySQL 8.0+
- Docker & Docker Compose (optional, for containerized setup)

### Local Development Setup

#### 1. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Set up environment variables
# Create a .env file with database credentials

# Initialize database
python database/create_admin_helper.py

# Run the FastAPI server
python app/main.py
```

Backend will be available at `http://127.0.0.1:8020`

#### 2. Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install Node dependencies
npm install

# Start the development server
npm start
```

Frontend will be available at `http://localhost:3000`

### Docker Setup

For a complete containerized setup:

```bash
# Build and start all services
docker-compose up --build

# Access the application
# Frontend: http://localhost:3000
# Backend API: http://localhost:8020
# MySQL: localhost:3306
```

See [DOCKER_QUICKSTART.md](DOCKER_QUICKSTART.md) for detailed Docker instructions.

## 📚 API Documentation

### Core Endpoints

#### Products

- `GET /products/` - Get all products
- `GET /products/?category_name=Electronics` - Filter by category
- `GET /products/{product_id}/variants/` - Get product with variants
- `GET /products/bestsellers/` - Get top selling products

#### Users

- `POST /users/register` - Register new user
- `POST /auth/login` - User login
- `GET /users/{user_id}` - Get user profile

#### Categories

- `GET /categories/` - Get all categories

#### Orders

- `POST /orders/` - Create new order
- `GET /orders/{user_id}` - Get user's orders
- `GET /orders/{order_id}/details` - Get order details

#### Cart

- `POST /cart/` - Add to cart
- `GET /cart/{user_id}` - Get cart items
- `DELETE /cart/{item_id}` - Remove from cart

#### Admin Endpoints

- `GET /admin/users` - List all users (admin only)
- `GET /admin/orders` - View all orders (admin only)
- `POST /admin/products` - Add product (admin only)
- `DELETE /admin/products/{product_id}` - Delete product (admin only)
- `PUT /admin/variants/{variant_id}` - Update inventory (admin only)

See [API_ENDPOINTS.md](backend/API_ENDPOINTS.md) for complete endpoint documentation.

## 🔐 Authentication

### User Authentication

- Standard email/password registration and login
- JWT tokens for session management
- Secure password hashing

### Admin Authentication

- Role-based access control (RBAC)
- JWT-based admin authentication
- Two-factor authentication support
- Enhanced security checks

### Quick Start for Admins

```bash
# 1. Create admin user
python backend/database/create_admin_helper.py

# 2. Start backend and frontend
cd backend && python app/main.py  # Terminal 1
cd frontend && npm start           # Terminal 2

# 3. Login with admin credentials at http://localhost:3000

# 4. Access Admin Dashboard from header menu
```

See [ADMIN_2FA_SETUP.md](backend/ADMIN_2FA_SETUP.md) for two-factor authentication setup.

## 📖 Documentation

- **[START_HERE.md](START_HERE.md)** - 3-step quick start guide
- **[ADMIN_DOCS_INDEX.md](ADMIN_DOCS_INDEX.md)** - Complete admin documentation
- **[API_ENDPOINTS.md](backend/API_ENDPOINTS.md)** - Full API reference
- **[DOCKER_QUICKSTART.md](DOCKER_QUICKSTART.md)** - Docker setup guide
- **[DATABASE_INITIALIZATION.md](DATABASE_INITIALIZATION.md)** - Database setup
- **[STORED_PROCEDURES_GUIDE.md](backend/database/STORED_PROCEDURES_GUIDE.md)** - Database procedures
- **[TROUBLESHOOT_EMAIL.md](backend/TROUBLESHOOT_EMAIL.md)** - Email configuration

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the backend directory:

```env
# Database Configuration
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=brightbuy

# JWT Configuration
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256

# Email Configuration (optional)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=your_email@gmail.com
SENDER_PASSWORD=your_app_password
```

## 🛠️ Troubleshooting

### Common Issues

**Products not loading:**

- Check backend is running on port 8020
- Verify database connection
- Check browser console for CORS errors

**Login not working:**

- Ensure admin user exists: `python backend/database/create_admin_helper.py`
- Check JWT secret key is configured
- Verify database table permissions

**Docker issues:**

- Ensure Docker daemon is running
- Check port availability (3000, 8020, 3306)
- View logs: `docker-compose logs -f`

See individual documentation files for specific troubleshooting steps.

## 📊 Database Schema

Key tables:

- **users** - Customer and admin accounts
- **product** - Product catalog
- **category** - Product categories
- **variant** - Product variations (size, color, etc.)
- **cart** - Shopping cart items
- **order** - Customer orders
- **order_item** - Line items in orders
- **favorites** - User wishlist items
- **admin_2fa** - Two-factor authentication data

See [DATABASE_FEATURES_SUMMARY.md](backend/database/DATABASE_FEATURES_SUMMARY.md) for complete schema details.

## 🤝 Contributing

This project is part of the CSE 3rd Semester coursework at University of Moratuwa.

## 📝 License

All rights reserved - BrightBuy Online Store © 2025

## 👥 Team

Developed as part of CSE coursework at University of Moratuwa

---

**Need Help?** Check the [documentation files](.) for detailed guides, or review the [troubleshooting section](#-troubleshooting).
