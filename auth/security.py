from typing import Optional
from fastapi import HTTPException,status
from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta, timezone
from config import security_settings
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer #noqa

'''Am going to use itsdangerous to generate safe url tokens for email verification and password reset'''
# _serializer =URLSafeTimedSerializer(security_settings.JWT_SECRET)
# def generate_safe_url_token(data :dict,salt:str | None= None) -> str:
#     return _serializer.dumps(data,salt= salt)

# def decode_safe_url_token(token:str,salt:str |None =None, expiry :timedelta | None= None)-> dict |None:
#     try:
#         return _serializer.loads(
#             token,
#             salt=salt,
#             max_age= expiry.total_seconds() if expiry else None,
#         )
#     except(BadSignature, SignatureExpired):
#         return None

_pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password:str) -> str:
    '''Used to hash passwords put by the user'''
    return _pwd.hash(password)

def verify_password(plain_password:str, password_hash:str) ->bool:
    '''Used to verify passwords put by the user'''
    return _pwd.verify(plain_password, password_hash)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    '''Creating a jwt access token'''
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, security_settings.JWT_SECRET, algorithm=security_settings.JWT_ALGORITHM)
    return encoded_jwt
def decode_access_token(token: str)-> dict | None:
    '''Verifying and decoding the jwt access token'''
    try:
        payload = jwt.decode(token, security_settings.JWT_SECRET, algorithms=[security_settings.JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail= "Token has expired"
        )
    except jwt.PyJWTError:
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail= "Invalid token"
        )

