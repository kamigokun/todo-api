from fastapi import Depends, HTTPException, status

from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from sqlalchemy.orm import Session

from app.database import get_db

from app.utils.security import decode_access_token

from app.models.user import User


# This tells FastAPI that the token comes from the
# Authorization header as "Bearer <token>".
#
# Unlike OAuth2PasswordBearer, HTTPBearer gives us a simple
# "Authorize" button in Swagger where we can paste the JWT token.
security = HTTPBearer()


def get_current_user(

        credentials: HTTPAuthorizationCredentials = Depends(security),

        db: Session = Depends(get_db)

) -> User:

    # This function runs automatically on every protected route.
    
    # It does 3 things:
    # 1: Extracts the token from the Authorization header.
    # 2: Decodes the token to find out who this user is.
    # 3: Fetches that user from the database and returns them.
    
    # If anything fails, like:
    # - missing/invalid token
    # - expired token
    # - user not found
    #
    # it raises a 401 Unauthorized error.


    # This error is ready to throw if anything goes wrong.
    credentials_exception = HTTPException(

        status_code=status.HTTP_401_UNAUTHORIZED,

        detail="Could not validate credentials",

        headers={"WWW-Authenticate": "Bearer"},

    )


    # STEP 1 - Extract and decode the token.
    
    # credentials.credentials is the actual JWT token.
    #
    # HTTPBearer already takes care of getting the token
    # from the Authorization header for us.
    
    # decode_access_token returns the payload dictionary
    # if the token is valid, or None if the token is invalid.
    
    payload = decode_access_token(credentials.credentials)

    if payload is None:

        raise credentials_exception


    # STEP 2 - Extract email from the payload.
    
    # Remember: when we created the JWT token,
    # we stored the user's email as "sub".
    
    # Example:
    # payload = {
    #     "sub": "user@gmail.com"
    # }
    
    email: str = payload.get("sub")

    if email is None:

        raise credentials_exception


    # STEP 3 - Find the user in the database.
    
    # We search for the user whose email matches
    # the email stored inside the JWT token.
    
    user = db.query(User).filter(User.email == email).first()

    if user is None:

        raise credentials_exception


    # If everything passed successfully,
    # return the user object.
    
    # This returned user is then available in protected routes
    # through:
    #
    # current_user: User = Depends(get_current_user)

    return user