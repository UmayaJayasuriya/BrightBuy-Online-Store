# 🎯 Admin Quick Reference Card

## 🚀 Setup (One-Time)

```bash
# Install
pip install python-jose[cryptography] mysql-connector-python

# Create admin user
python backend/database/create_admin_helper.py
# OR run SQL: UPDATE user SET user_type = 'admin' WHERE email = 'your@email.com';
```

## ▶️ Start Servers

```bash
# Terminal 1 - Backend
cd backend
python app/main.py
# → http://127.0.0.1:8020

# Terminal 2 - Frontend  
cd frontend
npm start
# → http://localhost:3000
```

## 🔐 Login & Access

1. Go to `http://localhost:3000`
2. Click **"Login"** button
3. Enter admin credentials
4. Click **"Admin Dashboard"** link (red text in header)

## 🎛️ Admin Dashboard

### 👥 Users Tab
- View all registered users
- See roles: admin (red) / customer (blue)

### 📦 Orders Tab
- View all orders
- Check delivery & payment status

### 🛍️ Products Tab
**Add Product**:
- Enter: Name, Category, Description
- Click "Add Product"

**Update Quantity**:
- Enter: Variant ID, New Quantity
- Click "Update"

**Delete Product**:
- Click "Delete" button
- Confirm

## 🔌 API Endpoints

```bash
# Login (get token)
POST /auth/login
{
  "identifier": "admin@example.com",
  "password": "yourpassword"
}
# Returns: access_token, user_type

# Admin endpoints (require Authorization: Bearer <token>)
GET /admin/users
GET /admin/orders
POST /admin/products?product_name=X&category_id=Y&description=Z
DELETE /admin/products/{id}
PUT /admin/variants/{id}/quantity?quantity=N
```

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| 403 Forbidden | Check `user_type = 'admin'` in database |
| No admin link | Clear localStorage, re-login |
| Backend won't start | Check `.env` database credentials |
| React infinite loop | Already fixed! Just refresh |

## 📚 Documentation

| Need | Read |
|------|------|
| Quick start | [START_HERE.md](START_HERE.md) |
| Full guide | [ADMIN_SETUP_GUIDE.md](ADMIN_SETUP_GUIDE.md) |
| Features | [README_ADMIN.md](README_ADMIN.md) |
| Architecture | [ADMIN_ARCHITECTURE.md](ADMIN_ARCHITECTURE.md) |
| Testing | [TESTING_CHECKLIST.md](TESTING_CHECKLIST.md) |
| All docs | [ADMIN_DOCS_INDEX.md](ADMIN_DOCS_INDEX.md) |

## ⚠️ Security Notes

**Production Checklist**:
- [ ] Update `SECRET_KEY` in `backend/app/security.py`
- [ ] Move `SECRET_KEY` to `.env` file
- [ ] Use HTTPS in production
- [ ] Restrict CORS origins

## 📊 Quick Stats

- **5** admin API endpoints
- **3** dashboard tabs
- **8** documentation files
- **24h** token expiration (default)

## 🎯 What Admin Can Do

✅ View all users  
✅ View all orders  
✅ Add products  
✅ Delete products  
✅ Update variant quantities  

## ❌ What Customers Cannot Do

❌ Access `/admin` route  
❌ Call admin API endpoints  
❌ See admin UI elements  

---

**🎉 Ready to use!**

Login as admin → Click "Admin Dashboard" → Start managing!

---

*Quick Reference v1.0*
