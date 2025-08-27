from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from auth.models import User, UserRole
from auth.schemas import UserCreate, UserRead
from auth.security import hash_password
from db.db import get_session

router = APIRouter(prefix= "/auth", tags=["auth"])

@router.post("/signup")
def signup(payload: UserCreate, session: Session = Depends(get_session)):
    '''Signup the user'''
    #Normalization of inputs
    email_norm = payload.email.strip().lower()
    first_name = payload.first_name.strip()
    last_name = payload.last_name.strip()

    #check if user already exists
    existing = session.exec(select(User).where (User.email == email_norm)).first()
    if existing:
        raise HTTPException(
            status_code= status.HTTP_409_CONFLICT,
            detail = "An account with this email already exists",
        )
    #hashing the password
    pwd_hash = hash_password(payload.password)

    #persist user
    user = User(
        first_name= first_name,
        last_name= last_name,
        email= email_norm,
        password= pwd_hash,
    )
    user.role =UserRole.ADMIN
    session.add(user)
    session.commit()
    session.refresh(user)

    #return UserREad to the user
    return UserRead.model_validate(user)
