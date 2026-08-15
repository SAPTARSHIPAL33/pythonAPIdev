from fastapi import Depends, APIRouter,status,HTTPException
from .. import database , schemas,utils,model,oauth
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

router=APIRouter(tags=["AUTHENTICATION"])

@router.post("/login")
def login(user_credentials:OAuth2PasswordRequestForm=Depends(), db:Session=Depends(database.get_db)):
    # {
    #     'username':"random",
    #     'password':"random"
    # }
    user=db.query(model.registration).filter(model.registration.email==user_credentials.username).first()
    
    if not user or not utils.verify(user_credentials.password , user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid credentials")
    
    access_token=oauth.create_access_token(data={"user_id":user.id})
    return {"access_token":access_token,"token_type":"bearer"}
