# ✅ Admin Features Testing Checklist

Use this checklist to verify all admin features are working correctly.

## Prerequisites Setup

- [ ] Backend dependencies installed: `pip install python-jose[cryptography] mysql-connector-python`
- [ ] Database is running and accessible
- [ ] At least one user exists with `user_type = 'admin'` in database
- [ ] Backend server is running on http://127.0.0.1:8020
- [ ] Frontend server is running on http://localhost:3000

---

## 1. Create Admin User

### Option A: Using Python Helper
```bash
cd backend
python database/create_admin_helper.py
```
- [ ] Script runs without errors
- [ ] Can create new admin user OR upgrade existing user
- [ ] Admin user shows in "List all admin users" option

### Option B: Using SQL
```sql
UPDATE user SET user_type = 'admin' WHERE email = 'test@example.com';
SELECT user_id, user_name, email, user_type FROM user WHERE user_type = 'admin';
```
- [ ] SQL updates successfully
- [ ] Admin user appears in query results

---

## 2. Backend Authentication

### Test Login Endpoint
```bash
curl -X POST http://127.0.0.1:8020/auth/login \
  -H "Content-Type: application/json" \
  -d '{"identifier": "admin@example.com", "password": "yourpassword"}'
```

**Expected Response**:
- [ ] Status: 200 OK
- [ ] Response includes `user_type: "admin"`
- [ ] Response includes `access_token`
- [ ] Response includes `token_type: "bearer"`

**Copy the access_token for next tests** 📋

---

## 3. Backend Admin Endpoints

Set your token:
```bash
TOKEN="your_access_token_here"
```

### Test GET /admin/users
```bash
curl http://127.0.0.1:8020/admin/users \
  -H "Authorization: Bearer $TOKEN"
```
- [ ] Returns list of users (array)
- [ ] Each user has: user_id, user_name, email, name, user_type

### Test GET /admin/orders
```bash
curl http://127.0.0.1:8020/admin/orders \
  -H "Authorization: Bearer $TOKEN"
```
- [ ] Returns list of orders (array)
- [ ] Each order has: order_id, user_id, order_date, total_amount, delivery_status, payment_method

### Test POST /admin/products
```bash
curl -X POST "http://127.0.0.1:8020/admin/products?product_name=Test+Product&category_id=4&description=Test+Description" \
  -H "Authorization: Bearer $TOKEN"
```
- [ ] Status: 201 Created
- [ ] Response includes new product_id
- [ ] Product created in database

### Test PUT /admin/variants/{id}/quantity
```bash
curl -X PUT "http://127.0.0.1:8020/admin/variants/1/quantity?quantity=50" \
  -H "Authorization: Bearer $TOKEN"
```
- [ ] Status: 200 OK
- [ ] Response confirms quantity updated
- [ ] Variant quantity changed in database

### Test DELETE /admin/products/{id}
```bash
curl -X DELETE "http://127.0.0.1:8020/admin/products/999" \
  -H "Authorization: Bearer $TOKEN"
```
- [ ] Status: 200 OK (if product exists) or 404 (if not found)
- [ ] Product removed from database (if existed)

---

## 4. Backend Security Tests

### Test Without Token
```bash
curl http://127.0.0.1:8020/admin/users
```
- [ ] Status: 403 Forbidden
- [ ] Error message about credentials

### Test With Invalid Token
```bash
curl http://127.0.0.1:8020/admin/users \
  -H "Authorization: Bearer invalid_token_here"
```
- [ ] Status: 401 Unauthorized
- [ ] Error message about invalid credentials

### Test Customer Token (if you have one)
```bash
# Login as customer first, get token
curl -X POST http://127.0.0.1:8020/auth/login \
  -H "Content-Type: application/json" \
  -d '{"identifier": "customer@example.com", "password": "password"}'

# Try accessing admin endpoint with customer token
curl http://127.0.0.1:8020/admin/users \
  -H "Authorization: Bearer customer_token_here"
```
- [ ] Status: 403 Forbidden
- [ ] Error: "Admin privileges required"

---

## 5. Frontend - Login Flow

### Open http://localhost:3000

1. **Click "Login" button**
   - [ ] Login modal appears
   - [ ] Form has identifier and password fields

2. **Try logging in as customer (if you have one)**
   - [ ] Login succeeds
   - [ ] Welcome message appears with username
   - [ ] NO "Admin Dashboard" link visible
   - [ ] Can logout successfully

3. **Login as admin**
   - [ ] Login succeeds
   - [ ] Welcome message appears with username
   - [ ] "Admin Dashboard" link IS visible (red, bold)
   - [ ] Link text: "Admin Dashboard"

---

## 6. Frontend - Admin Dashboard

### Navigate to /admin

1. **Access Control**
   - [ ] Logged out users: Can't access /admin (redirected to home)
   - [ ] Customer users: Can't access /admin (redirected to home)
   - [ ] Admin users: CAN access /admin

2. **Dashboard Layout**
   - [ ] Page title: "Admin Dashboard"
   - [ ] Three tabs visible: Users, Orders, Products
   - [ ] No console errors

### Users Tab
- [ ] Tab switches to Users
- [ ] Table displays user data
- [ ] Columns: User ID, Username, Email, Name, Role
- [ ] Role badges: admin (red), customer (blue)
- [ ] Data loads successfully

### Orders Tab
- [ ] Tab switches to Orders
- [ ] Table displays order data
- [ ] Columns: Order ID, User ID, Date, Total, Delivery Status, Payment Method, Payment Status
- [ ] Dates formatted correctly
- [ ] Totals show as currency ($X.XX)
- [ ] Data loads successfully

### Products Tab
- [ ] Tab switches to Products
- [ ] Two forms visible:
  - Add New Product
  - Update Variant Quantity
- [ ] Product table displays below forms
- [ ] Columns: Product ID, Product Name, Category, Description, Actions

---

## 7. Frontend - Product Management

### Add Product
1. Fill form:
   - Product Name: "Test Widget"
   - Category: Select any
   - Description: "Testing"
2. Click "Add Product"
   - [ ] Loading indicator appears
   - [ ] Success message appears
   - [ ] Product appears in table
   - [ ] Form clears

### Update Variant Quantity
1. Get a variant ID from database or product page
2. Fill form:
   - Variant ID: (valid ID)
   - New Quantity: 100
3. Click "Update"
   - [ ] Loading indicator appears
   - [ ] Success message appears
   - [ ] Quantity updated in database

### Delete Product
1. Find a test product in table
2. Click "Delete" button
   - [ ] Confirmation dialog appears
   - [ ] Click OK
   - [ ] Success message appears
   - [ ] Product removed from table
   - [ ] Product deleted from database

---

## 8. Frontend - Error Handling

### Network Errors
1. Stop backend server
2. Try any admin action
   - [ ] Error message displays
   - [ ] No console crashes
   - [ ] Can dismiss error

### Invalid Data
1. Try updating variant with invalid ID (99999)
   - [ ] Error message: "Variant not found"
   - [ ] No crash

2. Try adding product with missing fields
   - [ ] Form validation works
   - [ ] Required field indicators

---

## 9. React Bug Fix Verification

### Maximum Update Depth Fix
- [ ] Open http://localhost:3000
- [ ] No "Maximum update depth exceeded" error in console
- [ ] Header renders correctly
- [ ] Login modal can open/close
- [ ] No infinite render loops

---

## 10. Cross-Browser Testing

Test on at least 2 browsers:

**Browser 1: _____________**
- [ ] Login works
- [ ] Admin dashboard loads
- [ ] All tabs function
- [ ] Forms submit correctly

**Browser 2: _____________**
- [ ] Login works
- [ ] Admin dashboard loads
- [ ] All tabs function
- [ ] Forms submit correctly

---

## 11. Responsive Design

Test admin dashboard on different screen sizes:

**Desktop (1920x1080)**
- [ ] Tables display correctly
- [ ] Forms are usable
- [ ] No horizontal scroll

**Laptop (1366x768)**
- [ ] Tables display correctly
- [ ] Forms are usable
- [ ] Layout adapts

**Tablet (iPad - 768x1024)**
- [ ] Tables scroll horizontally if needed
- [ ] Forms stack correctly
- [ ] Tabs are tappable

---

## 12. Database Verification

After testing, verify database state:

```sql
-- Check admin users
SELECT user_id, user_name, email, user_type 
FROM user 
WHERE user_type = 'admin';

-- Check products (should include test product if not deleted)
SELECT product_id, product_name, category_id 
FROM product 
ORDER BY product_id DESC 
LIMIT 5;

-- Check variant quantities (should reflect any updates)
SELECT variant_id, variant_name, quantity 
FROM variant 
WHERE variant_id = 1;  -- Replace with your test variant ID

-- Check recent orders
SELECT order_id, user_id, total_amount, order_date 
FROM orders 
ORDER BY order_date DESC 
LIMIT 5;
```

- [ ] Admin users exist and correct
- [ ] Products match expectations
- [ ] Variant quantities match updates
- [ ] Orders data intact

---

## Summary

### ✅ All Tests Passed
- **Backend Auth**: JWT working correctly
- **Admin Endpoints**: All CRUD operations functional
- **Security**: Proper access control enforced
- **Frontend**: Admin dashboard operational
- **Bug Fixes**: React infinite loop resolved
- **Data Integrity**: Database updates correct

### ❌ Issues Found
Document any issues here:
```
Issue 1: ___________________________________________
Issue 2: ___________________________________________
Issue 3: ___________________________________________
```

---

## Performance Notes

- Average API response time: _______ms
- Dashboard load time: _______ms
- Large table performance (>100 rows): ___________

---

## Next Steps After Testing

Once all tests pass:

1. **Security**:
   - [ ] Update `SECRET_KEY` to production value
   - [ ] Move secrets to `.env` file
   - [ ] Enable HTTPS

2. **Documentation**:
   - [ ] Share admin credentials with team
   - [ ] Document admin workflows
   - [ ] Create user training materials

3. **Monitoring**:
   - [ ] Set up error logging
   - [ ] Monitor admin actions
   - [ ] Track API usage

4. **Enhancements**:
   - [ ] Add pagination (if needed)
   - [ ] Implement search/filter
   - [ ] Add more analytics

---

**Testing Date**: _______________  
**Tester Name**: _______________  
**Version**: 1.0.0  
**Status**: ⬜ Pass | ⬜ Fail | ⬜ Partial

---

📝 **Notes**:
