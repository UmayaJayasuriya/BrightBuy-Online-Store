# Admin Privileges Setup Guide

## Overview
Admin functionality has been added to BrightBuy to allow administrators to:
- View all users
- View all orders
- Add new products
- Delete existing products
- Update variant quantities

## Backend Changes

### 1. Security Module (`backend/app/security.py`)
- JWT-based authentication using `python-jose`
- `create_access_token()`: Creates signed JWT tokens with user info and role
- `get_current_user()`: Validates JWT from Authorization header
- `get_admin_user()`: Enforces admin-only access (checks `user_type == 'admin'`)

### 2. Auth Route Update (`backend/app/routes/auth.py`)
- Login endpoint now returns:
  - `user_type`: "admin" or "customer"
  - `access_token`: JWT bearer token
  - `token_type`: "bearer"

### 3. Admin Routes (`backend/app/routes/admin.py`)
All endpoints require `Authorization: Bearer <token>` header with admin JWT.

**GET /admin/users**
- Lists all users (user_id, user_name, email, name, user_type)

**GET /admin/orders**
- Lists all orders with delivery and payment status

**POST /admin/products?product_name=X&category_id=Y&description=Z**
- Creates a new product
- Returns created product with ID

**DELETE /admin/products/{product_id}**
- Deletes a product by ID
- Confirms deletion

**PUT /admin/variants/{variant_id}/quantity?quantity=N**
- Updates stock quantity for a variant
- Returns updated quantity

### 4. Dependencies
Added to `requirements.txt`:
```
python-jose[cryptography]
mysql-connector-python
```

Install with:
```bash
pip install python-jose[cryptography] mysql-connector-python
```

## Frontend Changes

### 1. AuthContext Update (`frontend/src/context/AuthContext.jsx`)
- Fixed infinite loop by wrapping `registerLoginModalHandler` in `useCallback`
- Added `isAdmin` boolean: checks if `user.user_type === 'admin'`
- Stores `access_token` from login response

### 2. Admin Dashboard (`frontend/src/pages/Admin.jsx`)
React component with three tabs:
- **Users**: Table of all users with roles
- **Orders**: Table of all orders with status
- **Products**: Table of products with add/delete/update quantity forms

Protected route: redirects to home if not admin.

All API calls include `Authorization: Bearer ${user.access_token}` header.

### 3. App Route (`frontend/src/App.jsx`)
Added route: `/admin` -> `<Admin />`

### 4. Header Update (`frontend/src/components/layout/Header.jsx`)
Conditional "Admin Dashboard" link shown only for admin users in the greeting bar.

## Database Setup

### Creating an Admin User
To create an admin user in your database, run:

```sql
-- Option 1: Update existing user to admin
UPDATE user SET user_type = 'admin' WHERE email = 'admin@brightbuy.com';

-- Option 2: Create new admin user (after hashing password)
-- You'll need to insert with hashed password using the signup flow first, then update:
UPDATE user SET user_type = 'admin' WHERE user_id = 1;
```

The `user` table has a `user_type` column that defaults to `'customer'`. Set it to `'admin'` for admin privileges.

## Testing the Admin Flow

### 1. Start Backend
```bash
cd backend
python app/main.py
```

Backend runs on `http://127.0.0.1:8020`

### 2. Start Frontend
```bash
cd frontend
npm start
```

Frontend runs on `http://localhost:3000`

### 3. Login as Admin
1. Go to `http://localhost:3000`
2. Click "Login" button
3. Enter admin credentials (email/username and password)
4. Upon successful login, you'll see "Admin Dashboard" link in the greeting bar
5. Click "Admin Dashboard" to access `/admin`

### 4. Test Admin Features
- **Users tab**: View all registered users
- **Orders tab**: View all orders with status
- **Products tab**:
  - Add new product: Fill form and submit
  - Update variant quantity: Enter variant ID and new quantity
  - Delete product: Click "Delete" button on any product

### 5. Verify JWT Protection
Try accessing `/admin` endpoints without token:
```bash
curl http://127.0.0.1:8020/admin/users
# Should return 403 Forbidden

curl -H "Authorization: Bearer <customer_token>" http://127.0.0.1:8020/admin/users
# Should return 403 Forbidden (not admin)

curl -H "Authorization: Bearer <admin_token>" http://127.0.0.1:8020/admin/users
# Should return list of users
```

## Security Notes

1. **Secret Key**: Update `SECRET_KEY` in `backend/app/security.py` to a strong random value in production
2. **Environment Variable**: Move `SECRET_KEY` to `.env` file:
   ```
   SECRET_KEY=your-super-secret-key-here
   JWT_ALGORITHM=HS256
   ```
3. **Token Expiration**: Default is 24 hours; adjust `ACCESS_TOKEN_EXPIRE_MINUTES` as needed
4. **HTTPS**: In production, always use HTTPS to protect tokens in transit

## API Testing Examples

### Login (get token)
```bash
curl -X POST http://127.0.0.1:8020/auth/login \
  -H "Content-Type: application/json" \
  -d '{"identifier": "admin@brightbuy.com", "password": "admin123"}'
```

Response includes `access_token` and `user_type`.

### Get Users (admin only)
```bash
curl http://127.0.0.1:8020/admin/users \
  -H "Authorization: Bearer eyJ0eXAi..."
```

### Add Product (admin only)
```bash
curl -X POST "http://127.0.0.1:8020/admin/products?product_name=Test+Product&category_id=4&description=Test" \
  -H "Authorization: Bearer eyJ0eXAi..."
```

### Update Variant Quantity (admin only)
```bash
curl -X PUT "http://127.0.0.1:8020/admin/variants/1/quantity?quantity=100" \
  -H "Authorization: Bearer eyJ0eXAi..."
```

### Delete Product (admin only)
```bash
curl -X DELETE http://127.0.0.1:8020/admin/products/42 \
  -H "Authorization: Bearer eyJ0eXAi..."
```

## Troubleshooting

### "403 Forbidden" on Admin Endpoints
- Ensure you're logged in as admin user (`user_type = 'admin'` in database)
- Check that `Authorization: Bearer <token>` header is included
- Verify token hasn't expired (24h default)

### "Maximum update depth exceeded" in React
- Fixed by wrapping `registerLoginModalHandler` in `useCallback`
- Ensure no other effects have missing dependencies

### Admin Dashboard Not Showing
- Check `user.user_type === 'admin'` in browser console
- Verify login response includes `user_type` field
- Clear localStorage and re-login

### JWT Decode Errors
- Ensure `python-jose[cryptography]` is installed
- Check `SECRET_KEY` matches between token creation and validation
- Verify token format is `Bearer <token>` not just `<token>`

## Future Enhancements

1. **Pagination**: Add pagination for users/orders/products lists
2. **Search/Filter**: Add search and filtering capabilities
3. **Bulk Operations**: Support bulk product updates
4. **Audit Log**: Track admin actions (who deleted/modified what)
5. **Role Permissions**: Add more granular permissions (e.g., read-only admin)
6. **Email Notifications**: Notify on low stock, new orders, etc.
7. **Analytics Dashboard**: Add charts and metrics for sales, inventory
8. **User Management**: Allow admins to create/edit/disable users
9. **Order Management**: Update delivery status, cancel orders, refunds

## Files Modified/Created

### Backend
- **Created**: `backend/app/security.py`
- **Created**: `backend/app/routes/admin.py`
- **Modified**: `backend/app/routes/auth.py`
- **Modified**: `backend/app/main.py`
- **Modified**: `backend/requirements.txt`

### Frontend
- **Created**: `frontend/src/pages/Admin.jsx`
- **Created**: `frontend/src/pages/Admin.css`
- **Modified**: `frontend/src/context/AuthContext.jsx`
- **Modified**: `frontend/src/components/layout/Header.jsx`
- **Modified**: `frontend/src/App.jsx`

---

**Setup Complete!** Your BrightBuy store now has admin privileges with JWT authentication and a full admin dashboard.
