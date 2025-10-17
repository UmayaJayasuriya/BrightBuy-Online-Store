# BrightBuy-Online-Store
Full-stack Retail Inventory &amp; Online Order Management System for BrightBuy. Built with FastAPI, MySQL, and React, it supports product browsing, cart &amp; checkout, stock validation, delivery estimation, payment simulation, admin reporting, and **admin privileges with JWT authentication**.

## 🔐 New: Admin Features
BrightBuy now includes a complete admin dashboard with role-based access control:
- **View Users** - Monitor all registered users and their roles
- **View Orders** - Track orders with delivery and payment status
- **Add Products** - Create new products with categories
- **Delete Products** - Remove products from catalog
- **Update Quantities** - Manage variant stock levels

### Quick Start for Admins
```bash
# 1. Install dependencies
pip install python-jose[cryptography] mysql-connector-python

# 2. Create admin user
python backend/database/create_admin_helper.py

# 3. Start servers
cd backend && python app/main.py  # Terminal 1
cd frontend && npm start           # Terminal 2

# 4. Login as admin at http://localhost:3000
# 5. Click "Admin Dashboard" link in header
```

**Documentation**: See [ADMIN_DOCS_INDEX.md](ADMIN_DOCS_INDEX.md) for complete admin documentation or [START_HERE.md](START_HERE.md) for a 3-step quick start.
