from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import psycopg2
from psycopg2.extras import RealDictCursor
from .config import settings

# SQLALCHEMY_DATABASE_URL= 'postgresql://<username>:<password>@<ip-address/hostname>:<database_port>/<databse_name>'
SQLALCHEMY_DATABASE_URL=f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'
engine=create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal=sessionmaker(autoflush=False,autocommit=False,bind=engine) #responsible to talk to our databases
base=declarative_base()
def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()


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
        