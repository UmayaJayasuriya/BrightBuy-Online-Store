from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import SessionLocal
from app.models.user import User, Address
from app.schemas.user import UserCreate, UserOut
import bcrypt
from app import schemas, models
from app.schemas.user import UserCreate



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
        # 🔍 Step 1: Resolve city_id from city name
        city = db.query(models.Location).filter(models.Location.city == user.address.city).first()
        if not city:
            raise HTTPException(status_code=400, detail="City not found in the system.")

        # 🏠 Step 2: Create and store address with resolved city_id
        new_address = models.Address(
            city_id=city.city_id,
            house_number=user.address.house_number,
            street=user.address.street,
            city=user.address.city,
            state=user.address.state
        )
        db.add(new_address)
        db.commit()
        db.refresh(new_address)

        # Hash password using bcrypt (truncate to 72 bytes max)
        password_bytes = user.password.encode('utf-8')[:72]
        hashed_pw = bcrypt.hashpw(password_bytes, bcrypt.gensalt()).decode('utf-8')

        
        new_user = models.User(
            user_name=user.user_name,
            email=user.email,
            name=user.name,
            password_hash=hashed_pw,
            user_type="customer",
            address_id=new_address.address_id
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return new_user

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


# Optional: Get all users
@router.get("/", response_model=List[UserOut])
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()
