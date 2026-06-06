from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.database import Base


# This is a Python enum — it limits the status to only these two values.
# A todo can only be 'pending' or 'done', nothing else.
class TodoStatus(str, enum.Enum):
    pending = "pending"
    done = "done"


class Todo(Base):
    """
    This class = the 'todos' table in your PostgreSQL database.
    Each todo item belongs to one user via owner_id.
    """

    __tablename__ = "todos"

    # Primary key — every todo gets a unique ID automatically
    id = Column(Integer, primary_key=True, index=True)

    # Title of the todo — required
    title = Column(String, nullable=False)

    # More detail about the todo — optional (nullable=True)
    description = Column(String, nullable=True)

    # Status can only be 'pending' or 'done', defaults to 'pending'
    status = Column(Enum(TodoStatus), default=TodoStatus.pending, nullable=False)

    # This is the LINK to the users table.
    # It stores the ID of the user who created this todo.
    # If the user is deleted, their todos get deleted too (ondelete="CASCADE")
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    # Timestamps — auto managed by PostgreSQL
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # This lets you do todo.owner to get the full User object
    # and user.todos to get all todos of a user
    owner = relationship("User", back_populates="todos") 
             