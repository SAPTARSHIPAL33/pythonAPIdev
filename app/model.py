from sqlalchemy import Column,Integer,String,Boolean,TIMESTAMP, ForeignKey
from sqlalchemy.sql.expression import text
from .database import base
from sqlalchemy.orm import relationship
# These are an orm model
class Post(base):
    __tablename__='posts'
    id = Column(Integer,primary_key=True,nullable=False)
    title=Column(String, nullable=False)
    content=Column(String,nullable=False)
    published=Column(Boolean,server_default="TRUE",nullable=False)
    created_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text("now()"))
    owner_id=Column(Integer,ForeignKey("user.id", ondelete="CASCADE"),nullable=False)
    owner= relationship("registration")
class registration(base):
    __tablename__="user"
    id = Column(Integer,primary_key=True,nullable=False)
    email=Column(String,unique=True,nullable=False)
    password=Column(String,nullable=False)
    created_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text("now()"))