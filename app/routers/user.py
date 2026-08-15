from fastapi import FastAPI, Response, status,HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db, base
from .. import model,utils,schemas


router=APIRouter(
    tags=["USERS"]
)
#new user sign up
@router.post("/users", status_code=status.HTTP_201_CREATED,response_model=schemas.createResponse)
def createUser(user:schemas.userCreate,db:Session=Depends(get_db)):
    hashed_password=utils.hash(user.password)
    user.password=hashed_password
    new_user=model.registration(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

#finding user
@router.get("/users/{id}",status_code=status.HTTP_200_OK, response_model=schemas.createResponse)
def get_user(id:int,db:Session=(Depends(get_db))):
    user=db.query(model.registration).filter(model.registration.id==id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No such user")
    return user