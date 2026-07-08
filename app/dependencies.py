from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database import get_db
from app.utils.security import decode_access_token
from app.models.user import User


# This tells FastAPI "tokens come from the /login endpoint"
# and they arrive in the Authorization header as "Bearer <token>"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl= "/login")


def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db)
) -> User:
    # This function runs automatically on every protected route


    # it does 3 things :
    # 1: Extract the token from the request header.
    # 2: Decodes the token to find who this user is.
    # 3: Fetches that user from the database and return them 


    # if anythings fails like -- missing token ,expired token,
    # user not found -- it raises a 401 unauthorized error.

    # This error is ready to throw if anything goes wrong   
    credentials_exception = HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail = "Could not validate credentials",
        headers = {"WWW-Authenticate": "Bearer"},

    )


    # step 1 - decode the token
    # decode_access_token returns the payload dict or None if invalid
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception
    
    # step 2 - extract email from the payload 
    # remember we stored email as "sub" when creating the token
    email: str = payload.get("sub")
    if email is None:
        raise credentials_exception
    

    # step 3 - find the user in the database 
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception
    


    # if everything passed then - return the user object
    return user
    


