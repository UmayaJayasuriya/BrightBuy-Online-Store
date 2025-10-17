from fastapi import APIRouter, Depends, HTTPException
import bcrypt
from app.database import get_db
from app.schemas.auth import LoginRequest
from app.security import create_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login")
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
            "token_type": "bearer"
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
