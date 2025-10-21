from fastapi import APIRouter, Depends, HTTPException
import bcrypt
import secrets
from datetime import datetime, timedelta
from app.database import get_db
from app.schemas.auth import LoginRequest, VerifyCodeRequest, LoginResponse
from app.security import create_access_token
from app.services.email_service import send_verification_code

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login", response_model=LoginResponse)
def login_user(login_data: LoginRequest, db=Depends(get_db)):
    cursor = None
    try:
        cursor = db.cursor(dictionary=True)
        
        # Find user by email or username
        cursor.execute(
            "SELECT * FROM user WHERE email = %s OR user_name = %s",
            (login_data.identifier, login_data.identifier)
        )
        user = cursor.fetchone()
        cursor.close()

        if not user:
            raise HTTPException(status_code=401, detail="User not found")

        # Verify password using bcrypt
        password_bytes = login_data.password.encode('utf-8')[:72]
        stored_hash = user['password_hash'].encode('utf-8')
        if not bcrypt.checkpw(password_bytes, stored_hash):
            raise HTTPException(status_code=401, detail="Invalid password")

        # Check if user is admin - require 2FA
        if user.get('user_type') == 'admin':
            # Generate 6-digit verification code
            verification_code = ''.join([str(secrets.randbelow(10)) for _ in range(6)])
            
            # Store verification code in database
            cursor = db.cursor()
            expires_at = datetime.now() + timedelta(minutes=10)
            
            # Delete any existing unused codes for this user
            cursor.execute(
                "DELETE FROM admin_verification_codes WHERE user_id = %s AND is_used = FALSE",
                (user['user_id'],)
            )
            
            # Insert new verification code
            cursor.execute(
                """INSERT INTO admin_verification_codes 
                   (user_id, verification_code, expires_at) 
                   VALUES (%s, %s, %s)""",
                (user['user_id'], verification_code, expires_at)
            )
            db.commit()
            cursor.close()
            
            # Send verification code via email
            email_sent = send_verification_code(
                user['email'], 
                verification_code, 
                user.get('name', user['user_name'])
            )
            
            if not email_sent:
                raise HTTPException(
                    status_code=500, 
                    detail="Failed to send verification code. Please try again."
                )
            
            return {
                "message": "Verification code sent to your email",
                "user_id": user['user_id'],
                "user_name": user['user_name'],
                "email": user['email'],
                "user_type": user.get('user_type', 'customer'),
                "requires_2fa": True
            }
        
        # For non-admin users, proceed with normal login
        # Create JWT token including role
        token = create_access_token({
            "sub": str(user['user_id']),
            "user_name": user['user_name'],
            "email": user['email'],
            "user_type": user.get('user_type', 'customer')
        })

        return {
            "message": "Login successful",
            "user_id": user['user_id'],
            "user_name": user['user_name'],
            "email": user['email'],
            "user_type": user.get('user_type', 'customer'),
            "access_token": token,
            "token_type": "bearer",
            "requires_2fa": False
        }
    except HTTPException:
        if cursor:
            cursor.close()
        raise
    except Exception as e:
        if cursor:
            cursor.close()
        print(" Internal Error:", e)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/verify-2fa", response_model=LoginResponse)
def verify_2fa_code(verify_data: VerifyCodeRequest, db=Depends(get_db)):
    """
    Verify the 2FA code sent to admin user's email
    """
    cursor = None
    try:
        cursor = db.cursor(dictionary=True)
        
        # Get the verification code record
        cursor.execute(
            """SELECT * FROM admin_verification_codes 
               WHERE user_id = %s 
               AND verification_code = %s 
               AND is_used = FALSE 
               AND expires_at > NOW()
               ORDER BY created_at DESC 
               LIMIT 1""",
            (verify_data.user_id, verify_data.verification_code)
        )
        code_record = cursor.fetchone()
        
        if not code_record:
            # Increment attempts counter if record exists
            cursor.execute(
                """UPDATE admin_verification_codes 
                   SET attempts = attempts + 1 
                   WHERE user_id = %s 
                   AND is_used = FALSE 
                   AND expires_at > NOW()""",
                (verify_data.user_id,)
            )
            db.commit()
            
            raise HTTPException(
                status_code=401, 
                detail="Invalid or expired verification code"
            )
        
        # Check if too many attempts
        if code_record['attempts'] >= 5:
            cursor.execute(
                "UPDATE admin_verification_codes SET is_used = TRUE WHERE id = %s",
                (code_record['id'],)
            )
            db.commit()
            raise HTTPException(
                status_code=429, 
                detail="Too many failed attempts. Please request a new code."
            )
        
        # Mark code as used
        cursor.execute(
            "UPDATE admin_verification_codes SET is_used = TRUE WHERE id = %s",
            (code_record['id'],)
        )
        db.commit()
        
        # Get user details
        cursor.execute(
            "SELECT * FROM user WHERE user_id = %s",
            (verify_data.user_id,)
        )
        user = cursor.fetchone()
        cursor.close()
        
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Create JWT token
        token = create_access_token({
            "sub": str(user['user_id']),
            "user_name": user['user_name'],
            "email": user['email'],
            "user_type": user.get('user_type', 'customer')
        })
        
        return {
            "message": "Login successful",
            "user_id": user['user_id'],
            "user_name": user['user_name'],
            "email": user['email'],
            "user_type": user.get('user_type', 'customer'),
            "access_token": token,
            "token_type": "bearer",
            "requires_2fa": False
        }
        
    except HTTPException:
        if cursor:
            cursor.close()
        raise
    except Exception as e:
        if cursor:
            cursor.close()
        print(" Internal Error:", e)
        raise HTTPException(status_code=500, detail=str(e))
