from pydantic import BaseModel
#specifies post fields
class Post(BaseModel):
    title:str
    content: str
    published: bool=True      #optional
    # rating: Optional[int] = None    #optional

class postCreate(Post):
    pass