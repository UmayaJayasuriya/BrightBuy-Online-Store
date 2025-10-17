# Admin System Architecture & Flow

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                     FRONTEND (React)                            │
│                   http://localhost:3000                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌────────────┐      ┌────────────┐      ┌────────────┐       │
│  │  Header    │      │   Login    │      │   Admin    │       │
│  │            │      │   Modal    │      │  Dashboard │       │
│  │ Show admin │─────▶│            │─────▶│            │       │
│  │ link if    │      │ Get JWT    │      │ 3 Tabs:    │       │
│  │ isAdmin    │      │ token      │      │ - Users    │       │
│  │            │      │            │      │ - Orders   │       │
│  └────────────┘      └────────────┘      │ - Products │       │
│                                           └────────────┘       │
│                                                                 │
│  AuthContext: Stores user, token, isAdmin                      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                           │
                           │ HTTP Requests
                           │ Authorization: Bearer <JWT>
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                    BACKEND (FastAPI)                            │
│                  http://127.0.0.1:8020                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌────────────┐      ┌────────────┐      ┌────────────┐       │
│  │  auth.py   │      │ security.py│      │  admin.py  │       │
│  │            │      │            │      │            │       │
│  │ POST /auth/│      │ Verify JWT │      │ Protected  │       │
│  │ login      │─────▶│ Extract    │─────▶│ Endpoints: │       │
│  │            │      │ user_type  │      │            │       │
│  │ Issue JWT  │      │            │      │ GET /users │       │
│  │ with role  │      │ Check      │      │ GET /orders│       │
│  │            │      │ is_admin   │      │ POST /prod │       │
│  └────────────┘      └────────────┘      │ DELETE /pr │       │
│                                           │ PUT /varia │       │
│                                           └────────────┘       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                           │
                           │ SQL Queries
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                    DATABASE (MySQL)                             │
│                      brightbuy                                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐      │
│  │   user   │  │  orders  │  │ product  │  │ variant  │      │
│  │          │  │          │  │          │  │          │      │
│  │ user_id  │  │ order_id │  │ prod_id  │  │ var_id   │      │
│  │ name     │  │ user_id  │  │ name     │  │ name     │      │
│  │ email    │  │ total    │  │ cat_id   │  │ price    │      │
│  │ user_type│  │ date     │  │ desc     │  │ quantity │      │
│  │          │  │          │  │          │  │          │      │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Authentication Flow

```
┌──────────┐                                              ┌──────────┐
│  User    │                                              │ Database │
└────┬─────┘                                              └────┬─────┘
     │                                                         │
     │ 1. Enter email & password                              │
     ├──────────────────────────────────────────▶             │
     │         POST /auth/login                  │            │
     │                                            │            │
     │                           2. Query user   │            │
     │                           by email ───────┼───────────▶│
     │                                            │            │
     │                           3. User data    │            │
     │                           with user_type◀─┼────────────┤
     │                                            │            │
     │                           4. Verify        │            │
     │                           password (bcrypt)│            │
     │                                            │            │
     │                           5. Create JWT    │            │
     │                           with user_type   │            │
     │                                            │            │
     │ 6. Return JWT + user_type                 │            │
     │◀──────────────────────────────────────────┤            │
     │                                                         │
     │ 7. Store in localStorage                               │
     │    user.user_type = "admin"                            │
     │    user.access_token = "eyJ..."                        │
     │                                                         │
```

## Admin Request Flow

```
┌──────────┐                                              ┌──────────┐
│  Admin   │                                              │ Backend  │
│Dashboard │                                              │  API     │
└────┬─────┘                                              └────┬─────┘
     │                                                         │
     │ 1. Click "Users" tab                                   │
     ├──────────────────────────────────────────▶             │
     │   GET /admin/users                        │            │
     │   Authorization: Bearer eyJ...            │            │
     │                                            │            │
     │                         2. Decode JWT     │            │
     │                         Extract payload   │            │
     │                         {                 │            │
     │                           sub: "1",       │            │
     │                           user_type: "admin"           │
     │                         }                 │            │
     │                                            │            │
     │                         3. Check          │            │
     │                         user_type == "admin"           │
     │                         ✓ Authorized      │            │
     │                                            │            │
     │                         4. Query database │            │
     │                         SELECT * FROM user            │
     │                                            │            │
     │ 5. Return user list                       │            │
     │◀──────────────────────────────────────────┤            │
     │   [                                                    │
     │     {user_id: 1, name: "Admin", type: "admin"},       │
     │     {user_id: 2, name: "John", type: "customer"}      │
     │   ]                                                    │
     │                                                         │
     │ 6. Display in table                                    │
     │                                                         │
```

## Security Checks

```
Request Flow with Security:

   ┌─────────────────┐
   │ Client Request  │
   └────────┬────────┘
            │
            ▼
   ┌─────────────────┐
   │ Has Auth Header?│
   └────────┬────────┘
            │
     ┌──────┴──────┐
     │ YES         │ NO ──────────▶ 403 Forbidden
     ▼             │
   ┌─────────────────┐
   │ Valid JWT?      │
   └────────┬────────┘
            │
     ┌──────┴──────┐
     │ YES         │ NO ──────────▶ 401 Unauthorized
     ▼             │
   ┌─────────────────┐
   │ user_type=admin?│
   └────────┬────────┘
            │
     ┌──────┴──────┐
     │ YES         │ NO ──────────▶ 403 Admin Required
     ▼             │
   ┌─────────────────┐
   │ Process Request │
   └────────┬────────┘
            │
            ▼
   ┌─────────────────┐
   │ Return 200 OK   │
   └─────────────────┘
```

## Component Hierarchy

```
App.jsx
├─ AuthProvider (context)
│  └─ CartProvider (context)
│     └─ Router
│        ├─ Header
│        │  ├─ Login (modal)
│        │  └─ SignUp (modal)
│        │
│        ├─ Navbar
│        │
│        ├─ Routes
│        │  ├─ Home
│        │  ├─ Shop
│        │  ├─ Cart
│        │  ├─ Profile
│        │  ├─ Admin ◀── NEW! Protected route
│        │  │  ├─ Users Tab
│        │  │  ├─ Orders Tab
│        │  │  └─ Products Tab
│        │  │     ├─ Add Product Form
│        │  │     ├─ Update Quantity Form
│        │  │     └─ Product Table
│        │  └─ ...
│        │
│        └─ Footer
```

## Data Flow: Add Product

```
    Admin Dashboard                  Backend API                 Database
         │                               │                          │
         │ 1. Fill form                  │                          │
         │    - name: "iPhone"           │                          │
         │    - category_id: 4           │                          │
         │    - desc: "Latest"           │                          │
         │                               │                          │
         │ 2. Click "Add Product"        │                          │
         ├──────────────────────────────▶│                          │
         │ POST /admin/products          │                          │
         │ ?product_name=iPhone&         │                          │
         │  category_id=4&               │                          │
         │  description=Latest           │                          │
         │ Auth: Bearer <JWT>            │                          │
         │                               │                          │
         │                               │ 3. Verify admin          │
         │                               │                          │
         │                               │ 4. INSERT INTO product   │
         │                               ├─────────────────────────▶│
         │                               │                          │
         │                               │ 5. product_id = 42       │
         │                               │◀─────────────────────────┤
         │                               │                          │
         │ 6. Success response           │                          │
         │◀──────────────────────────────┤                          │
         │ {product_id: 42, ...}         │                          │
         │                               │                          │
         │ 7. Show success message       │                          │
         │    "Product added!"           │                          │
         │                               │                          │
         │ 8. Refresh product list       │                          │
         ├──────────────────────────────▶│                          │
         │ GET /products/                │                          │
         │                               │                          │
         │ 9. Updated product list       │                          │
         │◀──────────────────────────────┤                          │
         │                               │                          │
```

## JWT Token Structure

```
Header:
{
  "typ": "JWT",
  "alg": "HS256"
}

Payload:
{
  "sub": "1",              // user_id
  "user_name": "admin",
  "email": "admin@example.com",
  "user_type": "admin",    // ◀── Key for access control
  "exp": 1729209600,       // Expiration timestamp
  "iat": 1729123200        // Issued at timestamp
}

Signature:
HMACSHA256(
  base64UrlEncode(header) + "." +
  base64UrlEncode(payload),
  SECRET_KEY
)

Complete Token:
eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.
eyJzdWIiOiIxIiwidXNlcl9uYW1lIjoiYWRtaW4iLCJlbWFpbCI6ImFkbWluQGV4YW1wbGUuY29tIiwidXNlcl90eXBlIjoiYWRtaW4iLCJleHAiOjE3MjkyMDk2MDAsImlhdCI6MTcyOTEyMzIwMH0.
xYzAbCdEfGhIjKlMnOpQrStUvWxYz
```

## Database Schema (Relevant Tables)

```sql
user table:
┌─────────┬───────────┬─────────────┬──────────┬──────────────┬───────────┐
│ user_id │ user_name │ email       │ name     │ password_hash│ user_type │
├─────────┼───────────┼─────────────┼──────────┼──────────────┼───────────┤
│    1    │  admin    │ admin@...   │  Admin   │  $2b$12$...  │   admin   │ ◀─ Admin
│    2    │  john     │ john@...    │  John D  │  $2b$12$...  │  customer │
│    3    │  jane     │ jane@...    │  Jane S  │  $2b$12$...  │  customer │
└─────────┴───────────┴─────────────┴──────────┴──────────────┴───────────┘

product table:
┌────────────┬──────────────┬─────────────┬─────────────────────────┐
│ product_id │ product_name │ category_id │ description             │
├────────────┼──────────────┼─────────────┼─────────────────────────┤
│     1      │  iPhone 15   │      4      │  Latest smartphone      │
│     2      │  MacBook Pro │      5      │  M3 chip laptop         │
└────────────┴──────────────┴─────────────┴─────────────────────────┘

variant table:
┌────────────┬──────────────┬────────────┬─────────┬──────────┐
│ variant_id │ variant_name │ product_id │  price  │ quantity │
├────────────┼──────────────┼────────────┼─────────┼──────────┤
│     1      │ iPhone Black │      1     │  999.99 │    50    │ ◀─ Admin can update
│     2      │ iPhone White │      1     │  999.99 │    30    │
└────────────┴──────────────┴────────────┴─────────┴──────────┘
```

## File Structure

```
BrightBuy-Online-Store/
│
├── backend/
│   ├── app/
│   │   ├── main.py                    # Registers admin routes
│   │   ├── security.py                # ✨ NEW: JWT utilities
│   │   ├── database.py                # DB connection
│   │   ├── routes/
│   │   │   ├── auth.py                # ✏️ MODIFIED: Issues JWT
│   │   │   ├── admin.py               # ✨ NEW: Admin endpoints
│   │   │   ├── user.py
│   │   │   ├── product.py
│   │   │   └── ...
│   │   └── schemas/
│   │       └── ...
│   ├── database/
│   │   ├── create_admin_helper.py     # ✨ NEW: Admin creator
│   │   └── create_admin_user.sql      # ✨ NEW: SQL script
│   └── requirements.txt               # ✏️ MODIFIED: Added JWT libs
│
├── frontend/
│   └── src/
│       ├── App.jsx                    # ✏️ MODIFIED: Added /admin route
│       ├── context/
│       │   └── AuthContext.jsx        # ✏️ MODIFIED: Added isAdmin, fixed loop
│       ├── components/
│       │   └── layout/
│       │       └── Header.jsx         # ✏️ MODIFIED: Admin link
│       └── pages/
│           ├── Admin.jsx              # ✨ NEW: Dashboard
│           └── Admin.css              # ✨ NEW: Styles
│
├── ADMIN_SETUP_GUIDE.md               # ✨ NEW: Complete guide
├── ADMIN_QUICK_START.md               # ✨ NEW: Quick reference
├── README_ADMIN.md                    # ✨ NEW: Feature summary
├── TESTING_CHECKLIST.md               # ✨ NEW: Test plan
├── START_HERE.md                      # ✨ NEW: Quick start
└── ADMIN_ARCHITECTURE.md              # ✨ NEW: This file

✨ = New file
✏️ = Modified file
```

---

This diagram-based documentation helps visualize how all components interact in the admin system.
