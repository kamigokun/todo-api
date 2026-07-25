from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.todo import Todo
from app.models.user import User
from app.schemas.todo import TodoCreate, TodoUpdate


def create_todo(data: TodoCreate, current_user: User, db: Session) -> Todo:
    """Creates a new todo item for the logged in user.
    
    Notice i never ask the user to send their own user_id.
    i already know who they are from the JWT token.
    i just attach owner_id automatically. This is safer -
    users can never create todos pretending to be someone else."""

    new_todo = Todo(
        title = data.title,
        description=data.description,
        owner_id = current_user.id    #automatically set from token
    )


    db.add(new_todo)           #add to session
    db.commit()                #save to database
    db.refresh(new_todo)       #get back the generated id, created_at etc


    return new_todo


def get_todos(current_user: User , db: Session , page: int) -> dict:
    """Returns a paginated list of todos for the logged in user.
    
    things to keep in mind here:
    i have to filter by owner_id so users ONLY see their own todos
    i use offset/limit for pagination(means return the data in a small
    chunks(pages) instead of all record at once to improve performance)
    count total before pagination for the response"""


    # Base query -- only get todos belonging to this user 
    # think of this as building your SQL query step by step 
    query = db.query(Todo).filter(Todo.owner_id == current_user.id)

    # Count total BEFORE applying pagination
    # i need this number to tell the frontend "there are X todos total"
    total = query.count()


    # offset() = skep this many rows (for pagination)
    # limit() = only return this many rows
    # ex = page =2, limit = 10 --> skip 10, take next 10
    todos = query.offset((page - 1) * limit).limit(limit).all()


    return {
        "data" : todos,
        "page" : page,
        "limit": limit,
        "total": total

    }

def update_todo(todo_id: int, data: TodoUpdate, current_user: User, db: Session) -> Todo:
    """
    updates and existing todo item.
    
    two things to check before updating:
    1. Does this todo actually exist?(404 if not)
    2. Does it belong to this user?(403 if not)
    
    only after both checks pass do we actually update.
    """


    # step 1 find the todo by id 
    todo = db.query(Todo).filter(Todo.id == todo_id).first()


    # step 2 does it exist? 
    if not todo:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Todo not found"
        
        )

    # # step 3 does it belong to this user? 
    # this is AUTHORIZATION - different from authentication. 
    # Authentication = are you logged in?
    # Authorization = do you have permission to do THIS action?
    if todo.owner_id != current_user.id:
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail ="You don't have permission to update this todo"
        )


    # step 4 = update only the fields that were actually sent
    # data.model_dump() converts pydantic schema to a dictionary
    # exclude_unset=True means "only include fields the user actually sent"
    # so if user only sent title, i only update title.Not description or status.

    update_data = data.model_dump(exclude_unset = True)


    for field, value in update_data.items():
        setattr(todo,field,value)   #todo.title = "new title" etc

    db.commit()             #save changes
    db.refrest(todo)       #get updated data back

    return todo

def delete_todo(todo_id: int, current_user: User, db: Session) -> None:
    """
    Deletes a todo item.
    
    same ownership checks as update - find it , verify ownership, delte.
    Return nothing - the route will send back 204 No content."""


    # find the todo 
    todo = db.query(Todo).filter(Todo.id == todo_id).first()

    # does it exist? 
    if not todo:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Todo not found"
        )


    # Does it belong to this user? 
    if todo.owner_id != current_user:
        raise HTTPException(
            status_code= status.HTTP_403_FORBIDDEN,
            detail = "You don't have permission to delete this todo"
        )
    db.delete(todo)    #mark for deletion
    db.commit()        #actually delete from database