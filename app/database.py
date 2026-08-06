from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
# SQLALCHEMY_DATABASE_URL= 'postgresql://<username>:<password>@<ip-address/hostname>/<databse_name>'
SQLALCHEMY_DATABASE_URL='postgresql://postgres:1234@localhost/social media'
engine=create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal=sessionmaker(autoflush=False,autocommit=False,bind=engine) #responsible to talk to our databases
base=declarative_base()
def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()