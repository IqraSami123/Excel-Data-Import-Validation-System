from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config import settings


engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,     #this will check that connection is live or not before using it 
)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,   #we are going to manage transaction with database manually
    autoflush=False,
)


class Base(DeclarativeBase):   #parent base class for the models, that we will create 
    pass


def get_db():     #this function will be used in the apis to get the session 
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()     #after using it, session will be closed, it will enhance the performance overall