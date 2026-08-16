from fastapi import FastAPI
from .database import base,engine
from .routers import post,user,auth
from . import model 

model.base.metadata.create_all(bind=engine)

app=FastAPI()
# my_post=[{"title":"title 1","content":"Content 1","id": randrange(0,100000000)},{"title":"title 2","content":"Content 2","id": randrange(0,100000000)}] #we are using this as database



app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)