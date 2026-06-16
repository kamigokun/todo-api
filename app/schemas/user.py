from pydantic import BaseModel , EmailStr
from datetime import datetime



class UserCreate(BaseModel):
    """shape of the data we ACCEPT when user registers
    user must send ALL 3 of these fields
    EmailStr use for validate email format automatically
    """

    name : str
    email : EmailStr
    password: str

class UserOut (BaseModel):
    """shape of the data we RETURN after registration or login
    we NEVER Send password or hashed_password back
    so noo password field here"""

    id : str
    name : str
    email: EmailStr
    created_at : datetime


    class config:
        """this tells pyndatic to read data from SQLAlchemy
        model attributes, not just plain dictonaries"""
        from_attributes = True


class TokenResponses(BaseModel):
    """shape of the towen response  after register or login 
    just one field - the JWT TOKEN string"""
    token : str 