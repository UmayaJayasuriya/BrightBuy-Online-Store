"""
Email service for sending verification codes and notifications
"""
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import logging

load_dotenv()

logger = logging.getLogger(__name__)

# Email configuration from environment variables
SMTP_HOST = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
SMTP_PORT = int(os.getenv('MAIL_PORT', 587))
SMTP_USER = os.getenv('MAIL_USERNAME', '')
SMTP_PASSWORD = os.getenv('MAIL_PASSWORD', '')
FROM_EMAIL = os.getenv('MAIL_FROM', SMTP_USER)
FROM_NAME = os.getenv('FROM_NAME', 'BrightBuy')
MAIL_STARTTLS = os.getenv('MAIL_STARTTLS', 'True').lower() == 'true'
MAIL_SSL_TLS = os.getenv('MAIL_SSL_TLS', 'False').lower() == 'true'

# Log configuration (without password) for debugging
logger.info(f"Email config loaded - Server: {SMTP_HOST}:{SMTP_PORT}, User: {SMTP_USER}, STARTTLS: {MAIL_STARTTLS}")

def send_verification_code(to_email: str, code: str, user_name: str) -> bool:
    """
    Send 2FA verification code to admin user's email
    
    Args:
        to_email: Recipient email address
        code: 6-digit verification code
        user_name: User's name for personalization
    
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    try:
        # Create message
        message = MIMEMultipart('alternative')
        message['Subject'] = 'BrightBuy Admin Login - Verification Code'
        message['From'] = f'{FROM_NAME} <{FROM_EMAIL}>'
        message['To'] = to_email
        
        # Create HTML content
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    color: #333;
                }}
                .container {{
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 20px;
                    background-color: #f9f9f9;
                }}
                .header {{
                    background-color: #4CAF50;
                    color: white;
                    padding: 20px;
                    text-align: center;
                    border-radius: 5px 5px 0 0;
                }}
                .content {{
                    background-color: white;
                    padding: 30px;
                    border-radius: 0 0 5px 5px;
                }}
                .code {{
                    font-size: 32px;
                    font-weight: bold;
                    color: #4CAF50;
                    text-align: center;
                    padding: 20px;
                    background-color: #f0f0f0;
                    border-radius: 5px;
                    letter-spacing: 5px;
                    margin: 20px 0;
                }}
                .warning {{
                    color: #d32f2f;
                    font-size: 14px;
                    margin-top: 20px;
                }}
                .footer {{
                    text-align: center;
                    margin-top: 20px;
                    font-size: 12px;
                    color: #666;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🔐 Admin Login Verification</h1>
                </div>
                <div class="content">
                    <p>Hello <strong>{user_name}</strong>,</p>
                    
                    <p>You are attempting to log in to your BrightBuy admin account. Please use the verification code below to complete your login:</p>
                    
                    <div class="code">{code}</div>
                    
                    <p>This code will expire in <strong>10 minutes</strong>.</p>
                    
                    <p class="warning">
                        ⚠️ <strong>Security Notice:</strong> If you did not attempt to log in, please ignore this email and ensure your account password is secure.
                    </p>
                    
                    <p>Thank you,<br>
                    The BrightBuy Team</p>
                </div>
                <div class="footer">
                    <p>This is an automated message. Please do not reply to this email.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Create plain text version as fallback
        text_content = f"""
        BrightBuy Admin Login - Verification Code
        
        Hello {user_name},
        
        You are attempting to log in to your BrightBuy admin account.
        
        Your verification code is: {code}
        
        This code will expire in 10 minutes.
        
        If you did not attempt to log in, please ignore this email and ensure your account password is secure.
        
        Thank you,
        The BrightBuy Team
        
        ---
        This is an automated message. Please do not reply to this email.
        """
        
        # Attach both versions
        part1 = MIMEText(text_content, 'plain')
        part2 = MIMEText(html_content, 'html')
        message.attach(part1)
        message.attach(part2)
        
        # Send email
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=30) as server:
            server.set_debuglevel(0)  # Set to 1 for debugging
            if MAIL_STARTTLS:
                server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.send_message(message)
        
        logger.info(f"Verification code sent successfully to {to_email}")
        return True
        
    except smtplib.SMTPAuthenticationError as e:
        logger.error(f"SMTP Authentication failed for {to_email}: {str(e)}")
        logger.error("Check MAIL_USERNAME and MAIL_PASSWORD in .env file")
        return False
    except smtplib.SMTPException as e:
        logger.error(f"SMTP error sending to {to_email}: {str(e)}")
        return False
    except Exception as e:
        logger.error(f"Failed to send verification code to {to_email}: {str(e)}")
        logger.error(f"Error type: {type(e).__name__}")
        return False

def test_email_configuration() -> bool:
    """
    Test if email configuration is valid
    
    Returns:
        bool: True if configuration is valid, False otherwise
    """
    if not SMTP_USER or not SMTP_PASSWORD:
        logger.warning("Email configuration incomplete. SMTP_USER or SMTP_PASSWORD not set.")
        return False
    
    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=10) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
        logger.info("Email configuration is valid")
        return True
    except Exception as e:
        logger.error(f"Email configuration test failed: {str(e)}")
        return False
