from pydantic import BaseModel
from typing import Optional

class LoginRequest(BaseModel):
    identifier: str
    password: str

class VerifyCodeRequest(BaseModel):
    user_id: int
    verification_code: str

class LoginResponse(BaseModel):
    message: str
    user_id: int
    user_name: str
    email: str
    user_type: str
    access_token: Optional[str] = None
    token_type: Optional[str] = None
    requires_2fa: bool = False