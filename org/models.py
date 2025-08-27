from typing import TYPE_CHECKING, List
from sqlmodel import Relationship, SQLModel, Field

if TYPE_CHECKING:
    from auth.models import User


class Organisation(SQLModel, table= True):
    '''details for a specific organisation'''
    id: int = Field(default=None, primary_key=True)
    name :str
    email: str
    phone_number: str
    kra_pin: str
    users: List["User"] =Relationship(
        back_populates="organisation",
        sa_relationship_kwargs= {"cascade":"all, delete-orphan"},
    )