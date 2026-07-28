from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.todo import TodoCreate, TodoUpdate, TodoOut, PaginatedTodos
from app.services.todo_service import (
    create_todo,
    get_todos,
    update_todo,
    delete_todo
)


router = APIRouter(tags=["Todos"])


@router.post("/todos", response_model=TodoOut, status_code=status.HTTP_201_CREATED)
def create(
    data: TodoCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)  # 🔒 protected route
):
    """
    POST /todos

    Creates a new todo for the logged in user.
    current_user is automatically injected by get_current_user.
    If token is missing or invalid, get_current_user raises 401
    before this function even runs.
    """
    return create_todo(data, current_user, db)


@router.get("/todos", response_model=PaginatedTodos)
def get_all(
    page: int = 1,        # default page is 1
    limit: int = 10,      # default limit is 10
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)  # 🔒 protected route
):
    """
    GET /todos?page=1&limit=10

    Returns paginated list of todos for logged in user.
    page and limit come from query parameters automatically.
    FastAPI reads ?page=1&limit=10 from the URL for you.
    """
    return get_todos(current_user, db, page, limit)


@router.put("/todos/{todo_id}", response_model=TodoOut)
def update(
    todo_id: int,         # comes from the URL path /todos/1
    data: TodoUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)  # 🔒 protected route
):
    """
    PUT /todos/{todo_id}

    Updates a specific todo by id.
    todo_id comes from the URL — /todos/1 means todo_id=1.
    Service checks ownership before updating.
    """
    return update_todo(todo_id, data, current_user, db)


@router.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(
    todo_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)  # 🔒 protected route
):
    """
    DELETE /todos/{todo_id}

    Deletes a specific todo by id.
    Returns 204 No Content on success — no response body needed.
    Service checks ownership before deleting.
    """
    delete_todo(todo_id, current_user, db)