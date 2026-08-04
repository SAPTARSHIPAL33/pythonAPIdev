from fastapi import FastAPI, Response, status,HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange

app=FastAPI()
my_post=[{"title":"title 1","content":"Content 1","id": randrange(0,100000000)},{"title":"title 2","content":"Content 2","id": randrange(0,100000000)}] #we are using this as database

#specifies post fields
class Post(BaseModel):
    title:str
    content: str
    # published: bool=True      #optional
    # rating: Optional[int] = None    #optional

#used in finding specific post section
def find_post(id):
    for p in my_post:
        if p['id']==id:
            return p

def find_idx(id):
    for i,e in enumerate(my_post):
        if e["id"]==id:
            return i
@app.get("/")     #"/" --- path parameter
def root():       #async is totally optional but it is used where to handle multiple request simultaneously
    return ("This is my social media web server")

#this is the feed of social media
@app.get("/posts")
def feed():
    return({"feed": my_post})

#we should have a field to post anything like title, content caption 
#but here we simply writting body so there is no proper field maintained as a result everything that will be written will be involved here so we
# are moving to the mext part of code where field for the post is mentioned 
# @app.post("/publish")
# def create(payload: dict=Body(...)):
#     print (payload)
#     return (f"title: {payload["Title"]} , content: {payload["Caption"]} ")

#creating a post
@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create(post:Post):
    post_dict=post.dict()
    post_dict["id"]=randrange(0,100000000)
    my_post.append(post_dict)
    # print(post)          #pydantic type
    # print(post.dict())   #convert pydantic type to dictionary type
    print(my_post)
    return {"Response": "Post uploaded"}

@app.get("/posts/latest")
def latest_post():
    return my_post[-1]

#getting a specific post
@app.get("/posts/{id}")
def get_post(id:int): #, response: Response):   # id:int----I want the id to be integer
    post=find_post(id)
    if not post:
        
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Result not")
        # # response.status_code=404---- not used because we have to memorise all the error code for this approach
        # response.status_code=status.HTTP_404_NOT_FOUND
        # return ({"message":"result not found"})
    return ({"data": post})

@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete(id:int):
    idx=find_idx(id)
    if idx is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, details="No such post")
    my_post.pop(idx)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update(id:int, post:Post):
    idx=find_idx(id)
    if idx is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,details="No such id exists")
    post_dict=post.dict()
    post_dict["id"]=id
    my_post[idx]=post_dict
    return my_post[idx]