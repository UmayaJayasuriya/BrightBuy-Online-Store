from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import bcrypt
from app.database import get_db
from app import models
from app.schemas.auth import LoginRequest
from app.utils.auth import create_access_token, get_current_user
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login")
def login_user(login_data: LoginRequest, db: Session = Depends(get_db)):
    try:
        user = (
            db.query(models.User)
            .filter(
                (models.User.email == login_data.identifier) |
                (models.User.user_name == login_data.identifier)
            )
            .first()
        )

        if not user:
            raise HTTPException(status_code=401, detail="User not found")

        # Verify password using bcrypt (truncate to 72 bytes)
        password_bytes = login_data.password.encode('utf-8')[:72]
        stored_hash = user.password_hash.encode('utf-8')
        if not bcrypt.checkpw(password_bytes, stored_hash):
            raise HTTPException(status_code=401, detail="Invalid password")

        # Create JWT token
        access_token = create_access_token(data={"sub": str(user.user_id)})
        
        return {
            "message": "Login successful",
            "access_token": access_token,
            "token_type": "bearer",
            "user_id": user.user_id,
            "user_name": user.user_name,
            "email": user.email,
            "user_type": user.user_type,
            "is_admin": user.has_admin_privileges()
        }
    except Exception as e:
        print("🔥 Internal Error:", e)
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/me")
def get_current_user_profile(current_user: User = Depends(get_current_user)):
    """Get current user profile"""
    return {
        "user_id": current_user.user_id,
        "user_name": current_user.user_name,
        "email": current_user.email,
        "name": current_user.name,
        "user_type": current_user.user_type,
        "is_admin": current_user.has_admin_privileges()
    }
