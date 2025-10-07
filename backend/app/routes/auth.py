from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import bcrypt
from app.database import get_db
from app import models
from app.schemas.auth import LoginRequest

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

        return {
            "message": "Login successful",
            "user_id": user.user_id,
            "user_name": user.user_name,
            "email": user.email
        }
    except Exception as e:
        print("🔥 Internal Error:", e)
        raise HTTPException(status_code=500, detail=str(e))
