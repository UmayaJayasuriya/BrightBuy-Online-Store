from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.database import get_db
from app.schemas.user import UserCreate, UserOut
import bcrypt

router = APIRouter(prefix="/users", tags=["Users"])

# Create user + address
@router.post("/", response_model=UserOut)
def create_user(user: UserCreate, db=Depends(get_db)):
    cursor = None
    try:
        cursor = db.cursor(dictionary=True)
        print(f" Received signup request for: {user.email}")
        
        # Backend validation: Check email format
        if '@' not in user.email:
            print(f" Invalid email format: {user.email}")
            raise HTTPException(
                status_code=400, 
                detail='Please enter a valid email address. It must include the "@" symbol (e.g., name@example.com).'
            )
        
        # Step 1: Resolve city_id from city name
        cursor.execute("SELECT city_id, city FROM location WHERE city = %s", (user.address.city,))
        city = cursor.fetchone()
        if not city:
            print(f" City not found: {user.address.city}")
            raise HTTPException(status_code=400, detail=f"City '{user.address.city}' not found in the system. Please use a valid city.")

        print(f" City found: {city['city']} (ID: {city['city_id']})")

        # Hash password using bcrypt
        password_bytes = user.password.encode('utf-8')[:72]
        hashed_pw = bcrypt.hashpw(password_bytes, bcrypt.gensalt()).decode('utf-8')

        print(f" Password hashed successfully")

        # Step 2: Call stored procedure
        print(f" Calling stored procedure AddUserWithAddress...")
        args = [
            None,  # p_user_id (NULL for auto_increment)
            user.user_name,
            user.email,
            user.name,
            hashed_pw,
            "customer",
            city['city_id'],
            user.address.house_number,
            user.address.street,
            user.address.city,
            user.address.state
        ]
        
        cursor.callproc('AddUserWithAddress', args)
        db.commit()
        print(f" Stored procedure executed successfully")

        # Fetch the newly created user
        cursor.execute("SELECT * FROM user WHERE email = %s", (user.email,))
        new_user = cursor.fetchone()
        if not new_user:
            print(f" User not found after creation")
            raise HTTPException(status_code=500, detail="User creation failed")

        print(f" User created successfully: {new_user['user_id']}")
        cursor.close()
        return new_user

    except HTTPException:
        db.rollback()
        if cursor:
            cursor.close()
        raise
    except Exception as e:
        db.rollback()
        if cursor:
            cursor.close()
        print(f" Error creating user: {str(e)}")
        
        error_msg = str(e)
        if "Please enter a valid email address" in error_msg or "45000" in error_msg:
            raise HTTPException(
                status_code=400, 
                detail='Please enter a valid email address. It must include the "@" symbol (e.g., name@example.com).'
            )
        
        raise HTTPException(status_code=500, detail=str(e))


# Get all users
@router.get("/", response_model=List[UserOut])
def get_users(db=Depends(get_db)):
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user")
    users = cursor.fetchall()
    cursor.close()
    return users


# Get user by ID
@router.get("/{user_id}", response_model=UserOut)
def get_user_by_id(user_id: int, db=Depends(get_db)):
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user WHERE user_id = %s", (user_id,))
    user = cursor.fetchone()
    cursor.close()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
