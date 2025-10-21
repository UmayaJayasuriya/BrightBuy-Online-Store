# Admin 2FA (Two-Factor Authentication) Setup Guide

## Overview
This system implements email-based two-factor authentication (2FA) for admin users. When an admin attempts to log in, they will receive a 6-digit verification code via email that must be entered to complete the login process.

## Features
- ✅ 6-digit verification codes sent via email
- ✅ Codes expire after 10 minutes
- ✅ Maximum 5 verification attempts per code
- ✅ Automatic cleanup of old/used codes
- ✅ Beautiful HTML email templates
- ✅ Only applies to admin users (regular customers login normally)

## Setup Instructions

### 1. Create Database Table
Run the database migration script to create the verification codes table:

```bash
cd backend
python database/create_admin_2fa_table.py
```

This creates the `admin_verification_codes` table with the following structure:
- `id`: Auto-increment primary key
- `user_id`: Foreign key to user table
- `verification_code`: 6-digit code
- `created_at`: Timestamp when code was created
- `expires_at`: Timestamp when code expires (10 minutes from creation)
- `is_used`: Boolean flag indicating if code has been used
- `attempts`: Counter for failed verification attempts

### 2. Configure Email Settings

#### Option A: Using Gmail (Recommended for Testing)

1. **Enable 2-Step Verification** on your Google account:
   - Go to https://myaccount.google.com/security
   - Enable "2-Step Verification"

2. **Generate App Password**:
   - Go to https://myaccount.google.com/apppasswords
   - Select "Mail" and your device
   - Copy the 16-character password

3. **Update .env file**:
```env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_16_char_app_password
FROM_EMAIL=your_email@gmail.com
FROM_NAME=BrightBuy
```

#### Option B: Using Other Email Providers

**Outlook/Hotmail:**
```env
SMTP_HOST=smtp-mail.outlook.com
SMTP_PORT=587
SMTP_USER=your_email@outlook.com
SMTP_PASSWORD=your_password
```

**Yahoo:**
```env
SMTP_HOST=smtp.mail.yahoo.com
SMTP_PORT=587
SMTP_USER=your_email@yahoo.com
SMTP_PASSWORD=your_app_password
```

**Custom SMTP Server:**
```env
SMTP_HOST=your_smtp_host
SMTP_PORT=587
SMTP_USER=your_username
SMTP_PASSWORD=your_password
```

### 3. Test Email Configuration

Test if your email configuration is working:

```python
from app.services.email_service import test_email_configuration

if test_email_configuration():
    print("✓ Email configuration is valid")
else:
    print("✗ Email configuration failed")
```

## API Endpoints

### 1. Login Endpoint (Modified)
**POST** `/auth/login`

**Request Body:**
```json
{
  "identifier": "admin_username_or_email",
  "password": "admin_password"
}
```

**Response for Admin Users (requires 2FA):**
```json
{
  "message": "Verification code sent to your email",
  "user_id": 1,
  "user_name": "admin",
  "email": "admin@example.com",
  "user_type": "admin",
  "requires_2fa": true,
  "access_token": null,
  "token_type": null
}
```

**Response for Regular Users (no 2FA):**
```json
{
  "message": "Login successful",
  "user_id": 2,
  "user_name": "customer",
  "email": "customer@example.com",
  "user_type": "customer",
  "requires_2fa": false,
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### 2. Verify 2FA Code Endpoint (New)
**POST** `/auth/verify-2fa`

**Request Body:**
```json
{
  "user_id": 1,
  "verification_code": "123456"
}
```

**Success Response:**
```json
{
  "message": "Login successful",
  "user_id": 1,
  "user_name": "admin",
  "email": "admin@example.com",
  "user_type": "admin",
  "requires_2fa": false,
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Error Responses:**
- `401`: Invalid or expired verification code
- `429`: Too many failed attempts (max 5)
- `404`: User not found
- `500`: Server error

## Frontend Integration Guide

### Login Flow

```javascript
// Step 1: Initial login
async function login(identifier, password) {
  const response = await fetch('/auth/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ identifier, password })
  });
  
  const data = await response.json();
  
  if (data.requires_2fa) {
    // Admin user - show 2FA code input form
    showVerificationCodeForm(data.user_id);
  } else {
    // Regular user - proceed with login
    saveToken(data.access_token);
    redirectToDashboard();
  }
}

// Step 2: Verify 2FA code
async function verify2FA(userId, code) {
  const response = await fetch('/auth/verify-2fa', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      user_id: userId,
      verification_code: code
    })
  });
  
  if (response.ok) {
    const data = await response.json();
    saveToken(data.access_token);
    redirectToDashboard();
  } else {
    const error = await response.json();
    showError(error.detail);
  }
}
```

### Example UI Flow

1. **Login Page**: User enters username/email and password
2. **For Admin Users**: 
   - Show message: "A verification code has been sent to your email"
   - Display input field for 6-digit code
   - Show "Resend Code" button (triggers new login)
   - Code expires in 10 minutes
3. **For Regular Users**: 
   - Direct login without 2FA

## Security Features

### Code Generation
- Uses cryptographically secure random number generation (`secrets` module)
- 6-digit codes (000000 - 999999)
- Each code is unique per user

### Code Expiration
- Codes expire after 10 minutes
- Expired codes cannot be used
- Old codes are automatically cleaned up on new login attempts

### Attempt Limiting
- Maximum 5 failed attempts per code
- After 5 failed attempts, code is invalidated
- User must request a new code

### Database Security
- Verification codes stored with user_id foreign key
- Cascade delete when user is deleted
- Indexed for fast lookups
- Parameterized queries prevent SQL injection

## Troubleshooting

### Email Not Sending

1. **Check SMTP credentials**:
   ```python
   from app.services.email_service import test_email_configuration
   test_email_configuration()
   ```

2. **Gmail specific issues**:
   - Ensure 2-Step Verification is enabled
   - Use App Password, not regular password
   - Check "Less secure app access" is OFF (use App Password instead)

3. **Check firewall/network**:
   - Ensure port 587 is not blocked
   - Try port 465 with SSL if 587 doesn't work

4. **Check logs**:
   - Look for error messages in console output
   - Email service logs errors with details

### Code Not Working

1. **Check expiration**: Codes expire after 10 minutes
2. **Check attempts**: Max 5 attempts per code
3. **Check database**: Verify code exists and is not marked as used
4. **Request new code**: Login again to generate a fresh code

### Database Issues

1. **Table doesn't exist**:
   ```bash
   python database/create_admin_2fa_table.py
   ```

2. **Foreign key constraint fails**:
   - Ensure user table exists
   - Ensure user_id is valid

## Testing

### Manual Testing

1. **Create an admin user** (if not exists):
   ```sql
   UPDATE user SET user_type = 'admin' WHERE user_id = 1;
   ```

2. **Test login flow**:
   - Login with admin credentials
   - Check email for verification code
   - Enter code in verification form
   - Verify successful login

3. **Test expiration**:
   - Login and wait 11 minutes
   - Try to use the code (should fail)

4. **Test attempt limiting**:
   - Login and get code
   - Enter wrong code 5 times
   - Verify code is invalidated

### Automated Testing

```python
import requests

# Test admin login
response = requests.post('http://localhost:8000/auth/login', json={
    'identifier': 'admin',
    'password': 'admin_password'
})
data = response.json()
assert data['requires_2fa'] == True
assert data['access_token'] is None

# Test 2FA verification (use actual code from email)
response = requests.post('http://localhost:8000/auth/verify-2fa', json={
    'user_id': data['user_id'],
    'verification_code': '123456'  # Replace with actual code
})
data = response.json()
assert 'access_token' in data
```

## Maintenance

### Cleanup Old Codes

Add a scheduled task to clean up expired codes:

```python
# Run daily
DELETE FROM admin_verification_codes 
WHERE expires_at < NOW() - INTERVAL 1 DAY;
```

### Monitor Failed Attempts

Query to check for suspicious activity:

```sql
SELECT user_id, COUNT(*) as failed_attempts, MAX(created_at) as last_attempt
FROM admin_verification_codes
WHERE attempts >= 5
GROUP BY user_id
ORDER BY failed_attempts DESC;
```

## Support

For issues or questions:
1. Check this documentation
2. Review error logs
3. Test email configuration
4. Verify database table exists
5. Check .env configuration
