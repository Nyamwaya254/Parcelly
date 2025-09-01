from datetime import timedelta
from fastapi import  HTTPException,status
from sqlmodel import Session, select

from auth.models import User
from auth.schemas import LoginRequest, LoginResponse
from auth.security import create_access_token, verify_password


class AuthService:
    def __init__(self, db:Session):
        self.db = db

    def authenticate_user(self, email:str, password:str)-> User:
        '''Authenticate user with email and password'''
        #Finding user by email
        statement = select(User).where(User.email == email)
        user = self.db.exec(statement).first()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        #check if user is verified
        # if not user.is_verified:
        #     raise HTTPException(
        #         status_code=status.HTTP_401_UNAUTHORIZED,
        #         detail="Account is not verified.Please verify your email"
        #     )
        
        #verify password
        if not verify_password(password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        return user
    
    def login(self, login_data: LoginRequest) -> LoginResponse:
        '''Login user and return JWT access token'''
        #normalization of inputs
        email_norm = login_data.email.strip().lower()
        

        #authenticate the user
        user = self.authenticate_user(email_norm, login_data.password)

        #create JWT access token
        access_token_expires = timedelta(minutes=30)
        token_data = {
            "sub": str(user.id),
            "email": user.email,
            "role": user.role.value,
            "organisation_id": user.organisation_id,
        }
        access_token = create_access_token(
            data= token_data,
            expires_delta= access_token_expires
        )

        return LoginResponse(
            access_token= access_token,
            token_type= "bearer",
            first_name= user.first_name,
            last_name= user.last_name,
            role= user.role.value,
        )
    
    
        
