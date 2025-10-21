"""
Quick test script to verify email configuration
"""
import sys
from pathlib import Path

# Add project root to path
repo_root = Path(__file__).resolve().parent
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from app.services.email_service import send_verification_code, test_email_configuration

print("=" * 60)
print("Testing Email Configuration")
print("=" * 60)

# Test 1: Check configuration
print("\n1. Checking email configuration...")
if test_email_configuration():
    print("   ✓ Email configuration is valid")
else:
    print("   ✗ Email configuration failed")
    print("\n   Please check your .env file has:")
    print("   - MAIL_USERNAME=himandhikuruppu@gmail.com")
    print("   - MAIL_PASSWORD=yleh emoy zygc zamb")
    print("   - MAIL_SERVER=smtp.gmail.com")
    print("   - MAIL_PORT=587")
    sys.exit(1)

# Test 2: Send test email
print("\n2. Sending test verification code...")
test_email = input("   Enter email to send test code to (or press Enter for himandhikuruppu@gmail.com): ")
if not test_email:
    test_email = "himandhikuruppu@gmail.com"

success = send_verification_code(test_email, "123456", "Test User")

if success:
    print(f"   ✓ Test email sent successfully to {test_email}")
    print("   📧 Check your inbox!")
else:
    print(f"   ✗ Failed to send test email to {test_email}")
    print("\n   Common issues:")
    print("   1. Gmail App Password might be incorrect")
    print("   2. 2-Step Verification not enabled on Google account")
    print("   3. Network/firewall blocking port 587")
    print("   4. Check server console for detailed error messages")

print("\n" + "=" * 60)
