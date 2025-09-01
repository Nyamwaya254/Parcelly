from enum import Enum
from sqlalchemy.types import Enum as SAEnum
from sqlmodel import Column, Relationship, SQLModel, Field, String

from org.models import Organisation

class UserRole(str,Enum):
    ADMIN = "ADMIN"
    CUSTOMER = "CUSTOMER"

class User(SQLModel,table= True):
    '''Details for a user'''
    id: int = Field(default=None, primary_key=True)
    first_name: str
    last_name: str
    email: str
    # is_verified: bool = Field(default=False)
    password_hash: str = Field(...,
                               description="Hashed Password")
    
    # parcels_sent: List[Parcel] = Relationship(
    #     back_populates="sender",
    #     sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    # )
    # parcels_received: List[Parcel] = Relationship(
    #     back_populates="receiver",
    #     sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    # )  
    organisation_id: int = Field(default=None, foreign_key="organisation.id", nullable=False)
    organisation : "Organisation" = Relationship(
        back_populates= "users",
    )
    role: UserRole = Field(
        default= UserRole.CUSTOMER,
        sa_column = Column(
            SAEnum(UserRole, name="user_role", native_enum= False),
            nullable = False,
            server_default= UserRole.CUSTOMER.value,

        ),
    )