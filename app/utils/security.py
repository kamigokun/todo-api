from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.config import settings


# This tells passlib to use bcrypt as the hashing algorithm.
# bcrypt is the industry standard for password hashing.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """
    Turns a plain password into a bcrypt hash.
    Example:
        "mypassword123" → "$2b$12$KIXxkM..."
    We store the hash, NEVER the original password.
    """
    password = password[:72]
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Checks if a plain password matches the stored hash.
    Used during login — user sends password, we verify it.
    Returns True if match, False if wrong password.
    """
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    """
    Creates a JWT token containing the user's data.
    
    JWT = JSON Web Token — a string that proves who you are.
    It has 3 parts separated by dots:
    header.payload.signature
    
    We set an expiry so tokens don't last forever.
    """
    to_encode = data.copy()

    # Token expires after X minutes (set in .env)
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    # Sign the token with our SECRET_KEY — only we can verify it
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> dict:
    """
    Decodes a JWT token and returns the data inside it.
    Raises JWTError if token is invalid or expired.
    Used when user sends a request — we decode their token
    to find out who they are.
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None