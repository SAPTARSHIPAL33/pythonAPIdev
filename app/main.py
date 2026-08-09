from fastapi import FastAPI, Response, status,HTTPException, Depends
from fastapi.params import Body
from typing import Optional,List
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session
from . import model,schemas,utils
from .database import base,get_db,engine

model.base.metadata.create_all(bind=engine)

app=FastAPI()
# my_post=[{"title":"title 1","content":"Content 1","id": randrange(0,100000000)},{"title":"title 2","content":"Content 2","id": randrange(0,100000000)}] #we are using this as database

# THIS IS USED TO CONNECT TO POSTGRESQL DATABASE IF WE ARE USING RAW SQL
# while True: 
#     try:
#         conn=psycopg2.connect(host='localhost',database="social media",user='postgres',password='1234',cursor_factory=RealDictCursor)
#         cursor=conn.cursor()
#         print("Database connection Successfull")
#         break
#     except Exception as error:
#         print("Database connection failed")
#         print("Error: ",error)
        

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
@app.get("/posts",response_model=List[schemas.response])
def feed(db: Session=Depends(get_db)):
    post=db.query(model.Post).all()
    # cursor.execute("SELECT * from posts") #to write a single line command we use "", but to write a multiple line command we use """ """"
    # posts=cursor.fetchall()
    return(post)

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
@app.post("/posts",status_code=status.HTTP_201_CREATED,response_model=schemas.response)
def create(post:schemas.postCreate,db:Session=Depends(get_db)):
    # cursor.execute("""Insert into posts (title,content, published) values (%s,%s,%s) returning *""",
    #                                         (post.title, post.content, post.published))   #prevents from sql injection if the user puts some command as title
    # new_post=cursor.fetchone()      #returning the last row because returning is used in the previous line. if returing is not used then it will return no result to fetch
    # conn.commit()         #ADDS INTO THE POSTGRESQL DATABASE 

    new_post=model.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@app.get("/posts/latest")
def latest_post():
    return my_post[-1]

#getting a specific post
@app.get("/posts/{id}",response_model=schemas.response)
def get_post(id:int,db:Session=Depends(get_db)): #, response: Response):   # id:int----I want the id to be integer
    # cursor.execute("SELECT * FROM  posts WHERE id=(%s)",(str(id)))
    # post=cursor.fetchone()
    post=db.query(model.Post).filter(model.Post.id==id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Result not")
        # # response.status_code=404---- not used because we have to memorise all the error code for this approach
        # response.status_code=status.HTTP_404_NOT_FOUND
        # return ({"message":"result not found"})
    return (post)

@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete(id:int,db:Session=Depends(get_db)):
    del_post=db.query(model.Post).filter(model.Post.id==id)

    # # idx=find_idx(id)
    # cursor.execute("DELETE FROM posts WHERE id=%s returning *",(str(id)))
    # del_post=cursor.fetchone()
    # conn.commit()
    if del_post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No such post")
    # my_post.pop(idx)
    del_post.delete()
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update(id:int, post:schemas.postCreate,db:Session=Depends(get_db),response_model=schemas.response):
    # cursor.execute (("UPDATE posts SET title=%s,content=%s , published=%s WHERE id=%s returning*"),(post.title,post.content,post.published,(str(id))) )
    # updated_post=cursor.fetchone()
    # conn.commit()
    updated_post=db.query(model.Post).filter(model.Post.id==id)
    if updated_post.first is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No such id exists")
    updated_post.update(updated_post.dict())
    db.commit()
    ## post_dict=post.dict()
    ## post_dict["id"]=id
    ## my_post[idx]=post_dict
    return updated_post

@app.post("/users", status_code=status.HTTP_201_CREATED,response_model=schemas.createResponse)
def createUser(user:schemas.userCreate,db:Session=Depends(get_db)):
    hashed_password=utils.hash(user.password)
    user.password=hashed_password
    new_user=model.registration(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user