import os
from sqlmodel import SQLModel,create_engine,Session
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///database.db")

engine = create_engine(DATABASE_URL, echo=True, pool_pre_ping=True)

def init_db() ->None:
    '''Auto creates tables in dev, but in prod we use alembic to handle migrations'''
    from auth import models as auth_models #noqa
    from parcels import models as parcel_models #noqa
    from org import models as org_models #noqa

    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session