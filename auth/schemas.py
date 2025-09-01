from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr
from sqlmodel import Field

class UserCreate(BaseModel):
    '''What we request the user to provide when creating an account'''
    first_name: str =Field(min_length=1, max_length=50)
    last_name: str =Field(min_length=1, max_length=50)
    email: EmailStr
    password: str =Field(min_length=6, max_length=100)
    organisation_id: int

class UserRead(BaseModel):
    '''What we return to the user when they request their info'''
    model_config = ConfigDict(from_attributes=True)
    id: int
    first_name: str
    last_name: str
    email: EmailStr

class LoginRequest(BaseModel):
    #What we request the user to provide when logging in
    email: EmailStr
    password: str
  


class LoginResponse(BaseModel):
    #What we return to the user when they log in
    access_token: str
    token_type: str = "bearer"
    role: str
    first_name: str
    last_name: str
    