from fastapi import APIRouter , Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.user import UserCreate, TokenResponses
from app.services.auth_service import register_user, login_user
from pydantic import BaseModel


# APIRouter is like a  mini FastApi app - groups related routes together.
# prefix = "/auth" means all routes here start with /auth...
# actually for this project i don't use prefix to match the PRD exactly 
router = APIRouter(tags=["Authentication"])


class LoginRequest(BaseModel):
    """shape of the login request body"""
    email: str
    password: str

@router.post("/regiter", response_model=TokenResponses)
def register(data: UserCreate, db: Session = Depends(get_db)):
    """
    POST /register
    
    
    Receives name,email,passowrd.
    calls register_user service which handles all logic.
    Return a JWT token.
    
    
    response_model = TokenResponses means FastAPI will automatically 
    format the response to match TokenResponse schema.
    """

    token = register_user(data,
                          db)
    return {"token": token}

@router.post("/login", response_model = TokenResponses)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    """
    POST /login
    
    Receives email and password
    Calls login_user service which handle all the logic.
    Return a JWT token.
    """

    token = login_user(data.email, 
                       data.password , 
                       db)
    return{"token": token}