# Admin Features - Quick Start

## What Was Added

### Backend (FastAPI)
✅ **JWT Authentication** - Secure token-based auth with role verification  
✅ **Admin Routes** - Protected endpoints for admin operations  
✅ **Role-Based Access Control** - Only admin users can access admin endpoints  

### Frontend (React)
✅ **Admin Dashboard** - View users, orders, and manage products  
✅ **Role Detection** - Auto-detect admin users and show admin links  
✅ **Secure API Calls** - JWT token included in all admin requests  

### Features
- **View Users** - See all registered users with roles
- **View Orders** - Monitor all orders with delivery/payment status
- **Add Products** - Create new products with category and description
- **Delete Products** - Remove products from the catalog
- **Update Quantities** - Modify variant stock levels

## Quick Setup

### 1. Install Dependencies
```bash
cd backend
pip install python-jose[cryptography] mysql-connector-python
```

### 2. Create Admin User
```bash
cd backend
python database/create_admin_helper.py
```
Follow the prompts to create or upgrade a user to admin.

OR run SQL directly:
```sql
UPDATE user SET user_type = 'admin' WHERE email = 'your@email.com';
```

### 3. Start Backend
```bash
cd backend
python app/main.py
```
Backend runs at `http://127.0.0.1:8020`

### 4. Start Frontend
```bash
cd frontend
npm start
```
Frontend runs at `http://localhost:3000`

### 5. Login as Admin
1. Go to `http://localhost:3000`
2. Click "Login"
3. Enter admin credentials
4. You'll see "Admin Dashboard" link in the header
5. Click it to access `/admin`

## API Endpoints

All admin endpoints require `Authorization: Bearer <token>` header.

- `GET /admin/users` - List all users
- `GET /admin/orders` - List all orders
- `POST /admin/products?product_name=X&category_id=Y&description=Z` - Create product
- `DELETE /admin/products/{id}` - Delete product
- `PUT /admin/variants/{id}/quantity?quantity=N` - Update variant stock

## Testing

### Get Token
```bash
curl -X POST http://127.0.0.1:8020/auth/login \
  -H "Content-Type: application/json" \
  -d '{"identifier": "admin@example.com", "password": "yourpassword"}'
```

### Call Admin Endpoint
```bash
curl http://127.0.0.1:8020/admin/users \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## Files Changed

### Backend
- ✅ `backend/app/security.py` - JWT auth utilities
- ✅ `backend/app/routes/admin.py` - Admin endpoints
- ✅ `backend/app/routes/auth.py` - Updated login with JWT
- ✅ `backend/app/main.py` - Registered admin routes
- ✅ `backend/requirements.txt` - Added dependencies

### Frontend
- ✅ `frontend/src/pages/Admin.jsx` - Admin dashboard
- ✅ `frontend/src/pages/Admin.css` - Dashboard styles
- ✅ `frontend/src/context/AuthContext.jsx` - Fixed loop, added isAdmin
- ✅ `frontend/src/components/layout/Header.jsx` - Admin link
- ✅ `frontend/src/App.jsx` - Admin route

### Documentation
- ✅ `ADMIN_SETUP_GUIDE.md` - Complete setup guide
- ✅ `backend/database/create_admin_user.sql` - SQL helper
- ✅ `backend/database/create_admin_helper.py` - Python helper

## Security Notes

⚠️ **IMPORTANT**: Update `SECRET_KEY` in `backend/app/security.py` before production!

Move to `.env`:
```
SECRET_KEY=your-super-secret-random-key-here
```

## Troubleshooting

**403 Forbidden on admin endpoints?**
- Check user has `user_type = 'admin'` in database
- Verify JWT token is in Authorization header
- Token may have expired (24h default)

**Admin Dashboard not showing?**
- Clear localStorage and re-login
- Check browser console for `user.user_type`
- Verify login response includes `user_type` field

**"Maximum update depth exceeded"?**
- Fixed! `registerLoginModalHandler` now wrapped in `useCallback`

## Next Steps

Consider adding:
- Pagination for large datasets
- Search and filter capabilities
- Bulk operations
- Audit logging
- More granular permissions
- Analytics charts

---

**Setup Complete!** 🎉

Admin privileges are now live. Login as admin to access the dashboard at `/admin`.
