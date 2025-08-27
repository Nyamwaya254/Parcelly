from sqlmodel import SQLModel, Field

class Location(SQLModel, table= True):
    '''Details for a location'''
    id: int = Field(default=None, primary_key=True)
    name: str

class Parcel(SQLModel, table= True):
    '''Details for a parcel'''
    id: int = Field(default=None, primary_key=True)
    sender: int | None = Field(default=None, foreign_key="user.id")
    receiver: int | None = Field(default=None, foreign_key="user.id")
    weight: float
    volume: float
    parcel_type: int
    location_from: int | None = Field(default=None, foreign_key="location.id")
    location_to: int | None = Field(default=None, foreign_key="location.id")
    status: str

    