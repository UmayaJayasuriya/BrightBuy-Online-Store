# Email Troubleshooting Guide

## Quick Fix Steps

### 1. Verify .env File Configuration

Make sure your `.env` file in the `backend` folder has these EXACT lines:

```env
MAIL_USERNAME=himandhikuruppu@gmail.com
MAIL_PASSWORD=yleh emoy zygc zamb
MAIL_FROM=himandhikuruppu@gmail.com
MAIL_PORT=587
MAIL_SERVER=smtp.gmail.com
MAIL_STARTTLS=True
MAIL_SSL_TLS=False
FROM_NAME=BrightBuy
```

**Important Notes:**
- No quotes around values
- No spaces around the `=` sign
- Password should be: `yleh emoy zygc zamb` (with spaces)
- File must be named `.env` (not `.env.txt` or anything else)

### 2. Test Email Configuration

Run this test script:
```bash
cd backend
python test_email.py
```

This will:
- Check if email configuration is loaded correctly
- Attempt to send a test email
- Show detailed error messages if it fails

### 3. Check Server Logs

When you try to login as admin, check the server console output. You should see:
```
Email config loaded - Server: smtp.gmail.com:587, User: himandhikuruppu@gmail.com, STARTTLS: True
```

If you see empty values, the .env file is not being loaded.

### 4. Common Issues and Solutions

#### Issue: "SMTP Authentication failed"
**Solution:**
- The password `yleh emoy zygc zamb` is a Gmail App Password
- Make sure 2-Step Verification is enabled on your Google account
- The spaces in the password are correct - don't remove them

#### Issue: "Failed to send verification code"
**Possible causes:**
1. **Wrong .env location** - Must be in `backend/.env`
2. **Server not restarted** - Restart the FastAPI server after changing .env
3. **Firewall blocking** - Port 587 might be blocked
4. **Network issues** - Check internet connection

#### Issue: Email config shows empty user
**Solution:**
```bash
# Check if .env file exists
cd backend
dir .env

# If not found, create it with the correct content
```

### 5. Manual Test with Python

Create a file `test_smtp.py` and run:

```python
import smtplib
from email.mime.text import MIMEText

# Test SMTP connection
try:
    server = smtplib.SMTP('smtp.gmail.com', 587, timeout=10)
    server.starttls()
    server.login('himandhikuruppu@gmail.com', 'yleh emoy zygc zamb')
    
    # Send test email
    msg = MIMEText('Test email from BrightBuy')
    msg['Subject'] = 'Test'
    msg['From'] = 'himandhikuruppu@gmail.com'
    msg['To'] = 'himandhikuruppu@gmail.com'
    
    server.send_message(msg)
    server.quit()
    print("✓ Email sent successfully!")
    
except Exception as e:
    print(f"✗ Error: {e}")
```

### 6. Restart Server

After making any changes to .env:
```bash
# Stop the server (Ctrl+C)
# Then restart:
python -m uvicorn app.main:app --reload
```

### 7. Check Gmail Settings

1. Go to https://myaccount.google.com/security
2. Ensure "2-Step Verification" is ON
3. Go to https://myaccount.google.com/apppasswords
4. Verify the app password is: `yleh emoy zygc zamb`

### 8. Alternative: Use Less Secure Apps (Not Recommended)

If app password doesn't work:
1. Go to https://myaccount.google.com/lesssecureapps
2. Turn ON "Allow less secure apps"
3. Use your regular Gmail password instead

**Note:** This is less secure and not recommended.

## Still Not Working?

Run these diagnostic commands:

```bash
cd backend

# Test 1: Check if .env is loaded
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('MAIL_USERNAME:', os.getenv('MAIL_USERNAME'))"

# Test 2: Test email service
python test_email.py

# Test 3: Check server logs
python -m uvicorn app.main:app --reload
# Then try to login as admin and watch the console output
```

## Contact Information

If still having issues, check:
1. Server console logs for detailed error messages
2. Make sure the admin user exists in database
3. Verify the password is correct for login
4. Check that the database table was created
