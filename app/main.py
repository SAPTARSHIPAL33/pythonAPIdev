from fastapi import FastAPI, Response, status,HTTPException, Depends
from fastapi.params import Body
from typing import Optional,List
# from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session
from . import model,schemas,utils
from .database import base,get_db,engine
from .routers import post,user,auth

model.base.metadata.create_all(bind=engine)

app=FastAPI()
# my_post=[{"title":"title 1","content":"Content 1","id": randrange(0,100000000)},{"title":"title 2","content":"Content 2","id": randrange(0,100000000)}] #we are using this as database

# THIS IS USED TO CONNECT TO POSTGRESQL DATABASE IF WE ARE USING RAW SQL
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

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)