from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

#specifies post fields
class Post(BaseModel):
    title:str
    content: str
    published: bool=True      #optional
    # rating: Optional[int] = None    #optional

class postCreate(Post):
    pass

class createResponse(BaseModel):
    id:int
    email:EmailStr
    created_at:datetime

class response(Post):
    id:int
    owner_id:int
    owner:createResponse

    class Config:    #converts sqlalchemy model to dict
        from_attributes=True

    # In modern FastAPI (using Pydantic v2), FastAPI’s internal response serializer 
    # automatically inspects object attributes when serializing the route's return value to JSON.

class userCreate(BaseModel):
    email:EmailStr
    password:str



class userLogin(BaseModel):
    email:EmailStr 
    password: str

class Token(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    id:Optional[int]=0