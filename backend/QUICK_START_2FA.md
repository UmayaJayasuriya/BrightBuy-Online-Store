# Quick Start Guide - Admin 2FA Setup

## 🚀 Quick Setup (5 minutes)

### Step 1: Create Database Table
```bash
cd backend
python database/create_admin_2fa_table.py
```

Expected output:
```
✓ admin_verification_codes table created successfully
```

### Step 2: Configure Email (Gmail Example)

1. **Get Gmail App Password:**
   - Go to: https://myaccount.google.com/apppasswords
   - Sign in to your Google account
   - Click "Select app" → Choose "Mail"
   - Click "Select device" → Choose "Other" → Type "BrightBuy"
   - Click "Generate"
   - Copy the 16-character password (e.g., `abcd efgh ijkl mnop`)

2. **Update your `.env` file:**
```env
# Add these lines to your .env file
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=abcdefghijklmnop
FROM_EMAIL=your_email@gmail.com
FROM_NAME=BrightBuy
```

### Step 3: Restart Your Server
```bash
# Stop the server (Ctrl+C) and restart
python -m uvicorn app.main:app --reload
```

### Step 4: Test It!

**Option A: Using the test script**
```bash
python test_admin_2fa.py
```

**Option B: Manual testing with curl/Postman**

1. **Login as admin:**
```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"identifier": "admin", "password": "your_password"}'
```

Expected response:
```json
{
  "message": "Verification code sent to your email",
  "user_id": 1,
  "requires_2fa": true,
  "access_token": null
}
```

2. **Check your email** for the 6-digit code

3. **Verify the code:**
```bash
curl -X POST http://localhost:8000/auth/verify-2fa \
  -H "Content-Type: application/json" \
  -d '{"user_id": 1, "verification_code": "123456"}'
```

Expected response:
```json
{
  "message": "Login successful",
  "access_token": "eyJhbGc...",
  "token_type": "bearer"
}
```

## ✅ That's it! Your admin 2FA is now active.

---

## 📋 Checklist

- [ ] Database table created
- [ ] Email credentials configured in .env
- [ ] Server restarted
- [ ] Test email received
- [ ] Successfully logged in with 2FA code

---

## 🔧 Troubleshooting

### "Email not sending"
- Check SMTP credentials in .env
- For Gmail: Use App Password, not regular password
- Ensure 2-Step Verification is enabled on Google account

### "Table doesn't exist"
```bash
python database/create_admin_2fa_table.py
```

### "No admin user"
Create one in your database:
```sql
UPDATE user SET user_type = 'admin' WHERE user_id = 1;
```

---

## 📖 Full Documentation
See `ADMIN_2FA_SETUP.md` for complete documentation including:
- Detailed setup instructions
- API endpoint documentation
- Frontend integration guide
- Security features
- Testing procedures
