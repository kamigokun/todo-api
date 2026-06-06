from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from app.config import settings


# create_engine() is the actual connection to your PostgreSQL database.
# it uses the DATABASE_URL from your .env file.
engine = create_engine(settings.DATABASE_URL)

# Creates database sessions
# A session is like a temporary workspace where you 
# make changes before committing them to the databse.
# autocommit= false means changes won't save until you explicitly say so
# autoflush = false means won't send queries to DB until you ask
SessionLocal = sessionmaker(autocommit = False,
                            autoflush= False,
                            bind= engine
                            )
# Parent class for all databse models/tables
class Base(DeclarativeBase):
    pass



def get_db():
    """
    This is a dependency function used by FastAPI.
    
    it creates a new databse session for each request,
    hands it to the route that need it,
    and ALWAYS closes it when the request is done -
    even if an error occurred. That's what try/finally does.
    """
    db = SessionLocal()



    try:
        yield db         #gives the session to whoever asked for it



    finally:
        db.close()       #always runs after, no matter what

