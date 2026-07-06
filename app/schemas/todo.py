from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from app.model.todo import TodoStatus


class TodoCreate(BaseModel):
    """shape of the data we ACCEPT when creating a todo
    description can be option """

    title : str
    description : Optional[str] = None

class TodoUpdate(BaseMOdel):
    """shape of the data we ACCEPT WHEN updating a todo
    all fields are optional here user can update .
    just a title , just the status , or everything right"""
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None


class TodoOut(BaseModel):
    """shape of the data we RETURN for a single todo item
    we show everything except owner id """
    id:int
    title:str
    description:Optional[str]
    status: TodoStatus
    created_at:datetime
    updated_at:Optional[str]

    class Config:
        from_attributes = True
    
class PaginatedTodos(BaseModel):
    """shape of the data we RETURN for the todo list endpoint.
    Wraps   the list of todos with pagination info."""
    data : List[TodoOut]   #list of todo items
    page : int     #current page no.
    limit : int    #hwo many per page
    total : int    #total todos in database                     