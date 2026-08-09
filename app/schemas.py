from pydantic import BaseModel, EmailStr
#specifies post fields
class Post(BaseModel):
    title:str
    content: str
    published: bool=True      #optional
    # rating: Optional[int] = None    #optional

class postCreate(Post):
    pass

class response(Post):
    id:int

    class Config:    #converts sqlalchemy model to dict
        from_attributes=True

    # In modern FastAPI (using Pydantic v2), FastAPI’s internal response serializer 
    # automatically inspects object attributes when serializing the route's return value to JSON.

class userCreate(BaseModel):
    email:EmailStr
    password:str

class createResponse(BaseModel):
    id:int
    email:EmailStr