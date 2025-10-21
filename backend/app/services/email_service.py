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

def send_order_confirmation(
        to_email: str,
        user_name: str,
        order_id: int,
        items: list,
        total_amount: float,
        payment_method: str,
        delivery_method: str,
        estimated_date: str | None = None,
        estimated_days: int | None = None,
):
        """
        Send an order confirmation email to the customer.

        Args:
                to_email: Recipient email address
                user_name: Customer name
                order_id: Order ID
                items: List of dicts with keys: product_name, variant_name, quantity, price
                total_amount: Total order amount
                payment_method: e.g., 'card' or 'cash'
                delivery_method: 'home_delivery' or 'store_pickup'
                estimated_date: ISO date string for delivery estimate (optional)
                estimated_days: Estimated delivery days (optional)

        Returns:
                bool: True on success, False otherwise
        """
        try:
                # Build items HTML rows
                rows_html = "".join([
                        f"<tr><td style='padding:8px;border:1px solid #eee'>{i.get('product_name','')}</td>"
                        f"<td style='padding:8px;border:1px solid #eee'>{i.get('variant_name','')}</td>"
                        f"<td style='padding:8px;border:1px solid #eee;text-align:center'>{i.get('quantity',0)}</td>"
                        f"<td style='padding:8px;border:1px solid #eee;text-align:right'>$ {float(i.get('price',0.0)):.2f}</td></tr>"
                        for i in items
                ])

                est_line = ""
                if delivery_method == "home_delivery":
                        if estimated_date:
                                est_line = f"<p><strong>Estimated Delivery:</strong> {estimated_date}"
                                if estimated_days:
                                        est_line += f" ({estimated_days} days)"
                                est_line += "</p>"
                else:
                        est_line = "<p><strong>Pickup:</strong> Your order will be ready in approximately 2 days.</p>"

                subject = f"Your BrightBuy Order #{order_id} Confirmation"

                html_content = f"""
                <!DOCTYPE html>
                <html>
                <head>
                        <meta charset='utf-8' />
                        <style>
                                body {{ font-family: Arial, sans-serif; color: #333; }}
                                .container {{ max-width: 700px; margin: 0 auto; padding: 20px; background: #f9f9f9; }}
                                .header {{ background: #4CAF50; color: #fff; padding: 18px; border-radius: 6px 6px 0 0; }}
                                .card {{ background: #fff; padding: 24px; border-radius: 0 0 6px 6px; }}
                                table {{ width: 100%; border-collapse: collapse; margin-top: 12px; }}
                                th {{ background:#fafafa; text-align:left; padding:8px; border:1px solid #eee; }}
                        </style>
                </head>
                <body>
                    <div class="container">
                        <div class="header">
                            <h2>✅ Order Confirmation</h2>
                        </div>
                        <div class="card">
                            <p>Hello <strong>{user_name}</strong>,</p>
                            <p>Thanks for your purchase! Your order <strong>#{order_id}</strong> has been received.</p>
                            <p><strong>Payment Method:</strong> {payment_method.title()}<br/>
                                 <strong>Delivery Method:</strong> {delivery_method.replace('_',' ').title()}</p>
                            {est_line}
                            <table>
                                <thead>
                                    <tr>
                                        <th>Product</th>
                                        <th>Variant</th>
                                        <th style="text-align:center">Qty</th>
                                        <th style="text-align:right">Price</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {rows_html}
                                </tbody>
                                <tfoot>
                                    <tr>
                                        <th colspan="3" style="text-align:right;padding:8px;border:1px solid #eee">Total</th>
                                        <th style="text-align:right;padding:8px;border:1px solid #eee">$ {total_amount:.2f}</th>
                                    </tr>
                                </tfoot>
                            </table>
                            <p>If you have any questions, reply to this email or contact support.</p>
                            <p>— The BrightBuy Team</p>
                        </div>
                    </div>
                </body>
                </html>
                """

                text_lines = [
                        f"Hello {user_name},",
                        f"Your order #{order_id} has been received.",
                        f"Payment Method: {payment_method}",
                        f"Delivery Method: {delivery_method}",
                ]
                if est_line:
                        # Plain text estimation
                        if estimated_date:
                                extra = f"Estimated delivery: {estimated_date}"
                                if estimated_days:
                                        extra += f" ({estimated_days} days)"
                                text_lines.append(extra)
                text_lines.append("Items:")
                for i in items:
                        text_lines.append(
                                f" - {i.get('product_name','')} {i.get('variant_name','')} x{i.get('quantity',0)} - $ {float(i.get('price',0.0)):.2f}"
                        )
                text_lines.append(f"Total: $ {total_amount:.2f}")
                text_content = "\n".join(text_lines)

                message = MIMEMultipart('alternative')
                message['Subject'] = subject
                message['From'] = f"{FROM_NAME} <{FROM_EMAIL}>"
                message['To'] = to_email

                part1 = MIMEText(text_content, 'plain')
                part2 = MIMEText(html_content, 'html')
                message.attach(part1)
                message.attach(part2)

                with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=30) as server:
                        server.set_debuglevel(0)
                        if MAIL_STARTTLS:
                                server.starttls()
                        server.login(SMTP_USER, SMTP_PASSWORD)
                        server.send_message(message)

                logger.info(f"Order confirmation sent to {to_email} for order #{order_id}")
                return True
        except Exception as e:
                logger.error(f"Failed to send order confirmation to {to_email}: {str(e)}")
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
