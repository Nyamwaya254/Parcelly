from passlib.context import CryptContext

_pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password:str) -> str:
    '''Used to hash passwords put by the user'''
    return _pwd.hash(password)

def verify_password(plain_password:str, password_hash:str) ->bool:
    '''Used to verify passwords put by the user'''
    return _pwd.verify(plain_password, password_hash)