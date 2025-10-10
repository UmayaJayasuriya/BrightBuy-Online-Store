from pydantic import BaseModel, EmailStr
from typing import Optional

# Address input
class AddressCreate(BaseModel):
    #city_id: int
    house_number: int
    street: str
    city: str
    state: str

# User input with nested address
class UserCreate(BaseModel):
    user_name: str
    email: EmailStr
    name: str
    password: str
    address: AddressCreate

# Response
class UserOut(BaseModel):
    user_id: int
    user_name: str
    email: EmailStr
    name: str
    user_type: str
    address_id: Optional[int]

    class Config:
        from_attributes = True
