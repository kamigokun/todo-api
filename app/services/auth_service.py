from sqlalchemy.orm import Session
from fastapi import HTTPException , status
from app.model.user import User
from app.schemas.user import UserCreate
from app.utils.security import hash_password, verify_password, create_access_token


def register_user(data:UserCreate , db: Session) -> str:
    """it handles new user registration and does 4 things:
    --- Checks if email already exists
    --- Hashes the password
    --- Saves the new user to database
    --- Return a JWT token
    """

    # step 1 check if email is already taken
    # .first() returns the user if found or None if not

    existing_user = db.query(User).filter(User.email == data.email).first()
    if existing_user:
        raise HTTPException(
            status_code = statu.HTTP_400_BAD_REQUEST
            detail = "Email already registered"
        )
    
    # step 2 hash the passwrod before saving
    # NEVER save plain text password 
    hashed = hash_password(data.password)


    # step 3 create the user object and save to database
    new_user = User(
        name = data.name,
        email = data.email,
        hashed_password = hashed
    )
    db.add(new_user)            #add to the session (notepad)
    db.commit()                  # save to database permanently
    db.refresh(new_user)          # refresh to get the auto generated id and created_at

    

    # step 4 create and return a JWT token 
    # "sub" is JWT standard for "subject" = who this taken belongs to 
    token = create_access_token({"sub": new_user.email})
    return token


def login_user(email: str, password: str, db:Session) -> str:
    """
    handles user login. it does 3 things:
    --- Finds the user by email
    --- Verifies the passsword 
    --- Returns a JWT token
    """

    # step 1 find user by email 
    user = db.query(User).filter(User.email == email).first()


    # step 2 verify password 
    # we check both in one if block - this is intentional 
    # if we did them separately , a hacker coudl tell from the error
    # whether the email is exists or the password was wrong 
    # giving the same error for both keeps your API safer.

    if not User or not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Invalid email or password"
        )
    
    # step 3 create and return JWT token 
    token = create_access_token({"sub": user.email})
    return token
