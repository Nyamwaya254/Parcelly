from pydantic import EmailStr
from sqlmodel import Field, SQLModel


class UserCreate(SQLModel):
    '''What we request the user to provide when creating an account'''
    first_name: str =Field(min_length=1, max_length=50)
    last_name: str =Field(min_length=1, max_length=50)
    email: EmailStr
    password: str =Field(min_length=6, max_length=100)

class UserRead(SQLModel):
    '''What we return to the user when they request their info'''
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    