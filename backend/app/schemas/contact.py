"""
Contact Schemas
"""
from pydantic import BaseModel, EmailStr, field_validator


class ContactCreate(BaseModel):
    customer_name: str
    email: EmailStr
    subject_name: str
    message: str

    @field_validator('customer_name')
    @classmethod
    def validate_customer_name(cls, v):
        if len(v) > 100:
            raise ValueError('Name must be 100 characters or less')
        return v

    @field_validator('email')
    @classmethod
    def validate_email(cls, v):
        if len(v) > 100:
            raise ValueError('Email must be 100 characters or less')
        return v

    @field_validator('subject_name')
    @classmethod
    def validate_subject(cls, v):
        if len(v) > 200:
            raise ValueError('Subject must be 200 characters or less')
        return v

    @field_validator('message')
    @classmethod
    def validate_message(cls, v):
        if len(v) > 2000:
            raise ValueError('Message must be 2000 characters or less')
        return v

    class Config:
        from_attributes = True


class ContactOut(BaseModel):
    contact_id: int
    customer_name: str
    email: str
    subject_name: str
    message: str

    class Config:
        from_attributes = True
