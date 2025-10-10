from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List
from app.database import SessionLocal
from app.models.user import User, Address
from app.schemas.user import UserCreate, UserOut
import bcrypt
from app import schemas, models


router = APIRouter(prefix="/users", tags=["Users"])

# DB session dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create user + address
@router.post("/", response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        print(f"🔍 Received signup request for: {user.email}")
        
        # 🔍 Step 1: Resolve city_id from city name
        city = db.query(models.Location).filter(models.Location.city == user.address.city).first()
        if not city:
            print(f"❌ City not found: {user.address.city}")
            raise HTTPException(status_code=400, detail=f"City '{user.address.city}' not found in the system. Please use a valid city.")

        print(f"✅ City found: {city.city} (ID: {city.city_id})")

        # Hash password using bcrypt (truncate to 72 bytes max)
        password_bytes = user.password.encode('utf-8')[:72]
        hashed_pw = bcrypt.hashpw(password_bytes, bcrypt.gensalt()).decode('utf-8')

        print(f"🔐 Password hashed successfully")

        # 📞 Step 2: Call stored procedure to create user with address atomically
        # Note: user_id is set to NULL to let auto_increment handle it
        print(f"📞 Calling stored procedure AddUserWithAddress...")
        db.execute(
            text(
                "CALL AddUserWithAddress(:p_user_id, :p_user_name, :p_email, :p_name, :p_password_hash, :p_user_type, :p_city_id, :p_house_number, :p_street, :p_city, :p_state)"
            ),
            {
                "p_user_id": None,  # NULL for auto_increment
                "p_user_name": user.user_name,
                "p_email": user.email,
                "p_name": user.name,
                "p_password_hash": hashed_pw,
                "p_user_type": "customer",
                "p_city_id": city.city_id,
                "p_house_number": user.address.house_number,
                "p_street": user.address.street,
                "p_city": user.address.city,
                "p_state": user.address.state
            }
        )
        db.commit()
        print(f"✅ Stored procedure executed successfully")

        # 🔄 Fetch the newly created user to return
        new_user = db.query(models.User).filter(models.User.email == user.email).first()
        if not new_user:
            print(f"❌ User not found after creation")
            raise HTTPException(status_code=500, detail="User creation failed")

        print(f"✅ User created successfully: {new_user.user_id}")
        return new_user

    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        print(f"❌ Error creating user: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# Optional: Get all users
@router.get("/", response_model=List[UserOut])
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()
