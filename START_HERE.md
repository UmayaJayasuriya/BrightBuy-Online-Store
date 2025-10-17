# 🚀 Start Here - Admin Setup

## What You Need to Do (3 Steps)

### Step 1: Install Dependencies (1 minute)
```bash
cd backend
pip install python-jose[cryptography] mysql-connector-python
```

### Step 2: Create Admin User (2 minutes)

**Option A - Interactive Python Script** (Recommended):
```bash
cd backend
python database/create_admin_helper.py
```
Choose option 1 or 2, follow prompts.

**Option B - Direct SQL**:
```sql
-- If you already have a user account, upgrade it:
UPDATE user SET user_type = 'admin' WHERE email = 'your@email.com';

-- Verify:
SELECT user_name, email, user_type FROM user WHERE user_type = 'admin';
```

### Step 3: Start Your Servers (30 seconds)

**Terminal 1 - Backend**:
```bash
cd backend
python app/main.py
```
Wait for: `Application startup complete.`

**Terminal 2 - Frontend**:
```bash
cd frontend
npm start
```
Wait for: Browser opens to `http://localhost:3000`

---

## ✅ You're Ready!

1. Go to **http://localhost:3000**
2. Click **"Login"** button
3. Enter your admin credentials
4. Look for **"Admin Dashboard"** link in the header (red text)
5. Click it to access `/admin`

---

## 🎯 What You Can Do

### In Admin Dashboard:

**👥 Users Tab**
- See all registered users
- View their roles (admin/customer)

**📦 Orders Tab**
- View all orders
- Check payment and delivery status

**🛍️ Products Tab**
- **Add Product**: Fill form with name, category, description
- **Delete Product**: Click Delete button (with confirmation)
- **Update Stock**: Enter variant ID and new quantity

---

## 🐛 If Something Doesn't Work

### "403 Forbidden" on admin endpoints
→ Check database: User must have `user_type = 'admin'`
```sql
SELECT email, user_type FROM user WHERE email = 'your@email.com';
```

### "Admin Dashboard" link not showing
→ Clear browser localStorage and re-login:
```javascript
// In browser console:
localStorage.clear();
location.reload();
```

### Backend won't start
→ Check database connection in `.env` file:
```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=yourpassword
DB_NAME=brightbuy
DB_PORT=3306
```

### React "Maximum update depth exceeded"
→ Already fixed! Just refresh the page.

---

## 📚 More Info

- **Full Setup Guide**: `ADMIN_SETUP_GUIDE.md`
- **Quick Reference**: `ADMIN_QUICK_START.md`
- **Feature Summary**: `README_ADMIN.md`
- **Testing Guide**: `TESTING_CHECKLIST.md`

---

## 🎉 That's It!

Three simple steps and you have a fully functional admin dashboard.

**Questions?** Check the guides above or look at the code comments.

**Happy Administering! 🚀**
