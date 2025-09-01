from fastapi import Depends, HTTPException,status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlmodel import Session

from auth.models import User
from auth.security import decode_access_token
from auth.service import AuthService
from db.db import get_session

security =HTTPBearer()

def get_auth_service(db: Session = Depends(get_session)) ->AuthService:
    '''Dependancy to get AuthService'''

    return AuthService(db)
def get_current_user(
        credentials:HTTPAuthorizationCredentials = Depends(security),
        db: Session = Depends(get_session),
) -> User:
    '''Get current authenticated user'''
    token = credentials.credentials
    payload  = decode_access_token(token)

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail= "Invalid authentication credentials"
        )
    user = db.get(User, int(user_id))

    if not user:
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail= "User not found"
        )
    return user