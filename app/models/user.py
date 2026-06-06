from xml.dom.domreg import registered

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class User(Base):
    """
    This class = the 'users' table in my PostgreSQL database.
    Each attribute below = one column in that table.
    """

    __tablename__ = "users"  #exact name of the table in PostgreSQL
    # index = True makes searching by ID faster
    id = Column(Integer , primary_key=True, index=True)

    # User's full name - cannot be empty(nullable = True)'
    name =Column(String, nullable=False)

    # Email cannot be empty
    email = Column(String, unique=True, index=True, nullable=False)

    # we NEVER store the real password, only the hashed version
    hashed_password = Column(String, nullable=False)

    # Automatically saaves the exact time the User registered
    # server_default= func.now() means PostgreSQL sets this , not python 
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # One user can have many todos
    todos = relationship("Todo", back_populates="owner", cascade="all, delete") 


