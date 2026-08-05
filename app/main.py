from fastapi import FastAPI, Response, status,HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor

app=FastAPI()
my_post=[{"title":"title 1","content":"Content 1","id": randrange(0,100000000)},{"title":"title 2","content":"Content 2","id": randrange(0,100000000)}] #we are using this as database

#specifies post fields
class Post(BaseModel):
    title:str
    content: str
    published: bool=True      #optional
    # rating: Optional[int] = None    #optional

while True: 
    try:
        conn=psycopg2.connect(host='localhost',database="social media",user='postgres',password='1234',cursor_factory=RealDictCursor)
        cursor=conn.cursor()
        print("Database connection Successfull")
        break
    except Exception as error:
        print("Database connection failed")
        print("Error: ",error)
        

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
    cursor.execute("SELECT * from posts") #to write a single line command we use "", but to write a multiple line command we use """ """"
    posts=cursor.fetchall()
    return({"feed": posts})

#we should have a field to post anything like title, content caption 
#but here we simply writting body so there is no proper field maintained as a result everything that will be written will be involved here so we
# are moving to the mext part of code where field for the post is mentioned 
# @app.post("/publish")
# def create(payload: dict=Body(...)):
#     print (payload)
#     return (f"title: {payload["Title"]} , content: {payload["Caption"]} ")

#creating a post
# @app.post("/posts",status_code=status.HTTP_201_CREATED)
# def create(post:Post):
#     post_dict=post.dict()
#     post_dict["id"]=randrange(0,100000000)
#     my_post.append(post_dict)
#     # print(post)          #pydantic type
#     # print(post.dict())   #convert pydantic type to dictionary type
#     print(my_post)
#     return {"Response": "Post uploaded"}
@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create(post:Post):
    cursor.execute("""Insert into posts (title,content, published) values (%s,%s,%s) returning *""",
                                            (post.title, post.content, post.published))   #prevents from sql injection if the user puts some command as title
    new_post=cursor.fetchone()      #returning the last row because returning is used in the previous line. if returing is not used then it will return no result to fetch
    conn.commit()         #ADDS INTO THE POSTGRESQL DATABASE 
    return {"Response": new_post}

@app.get("/posts/latest")
def latest_post():
    return my_post[-1]

#getting a specific post
@app.get("/posts/{id}")
def get_post(id:int): #, response: Response):   # id:int----I want the id to be integer
    cursor.execute("SELECT * FROM  posts WHERE id=(%s)",(str(id)))
    post=cursor.fetchone()
    if not post:
        
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Result not")
        # # response.status_code=404---- not used because we have to memorise all the error code for this approach
        # response.status_code=status.HTTP_404_NOT_FOUND
        # return ({"message":"result not found"})
    return ({"data": post})

@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete(id:int):
    # idx=find_idx(id)
    cursor.execute("DELETE FROM posts WHERE id=%s returning *",(str(id)))
    del_post=cursor.fetchone()
    conn.commit()
    if del_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No such post")
    # my_post.pop(idx)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update(id:int, post:Post):
    cursor.execute (("UPDATE posts SET title=%s,content=%s , published=%s WHERE id=%s returning*"),(post.title,post.content,post.published,(str(id))) )
    updated_post=cursor.fetchone()
    conn.commit()
    if updated_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No such id exists")
    # post_dict=post.dict()
    # post_dict["id"]=id
    # my_post[idx]=post_dict
    return updated_post