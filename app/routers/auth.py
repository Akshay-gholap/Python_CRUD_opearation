from fastapi import APIRouter, Response, status, HTTPException, Depends
from sqlalchemy.orm import Session
from.. import schemas, database, models, utils, oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(tags=['Authentication'])

@router.post("/login", response_model=schemas.Token)
def login(user_credientials :OAuth2PasswordRequestForm = Depends() ,db:Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email==user_credientials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Invalid credientials')
    if not utils.verify_password(user_credientials.password,user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Invalid credientials')

    access_token = oauth2.create_access_token(data={"user_id": user.id},)

    return {"access_token": access_token, "token_type": "bearer"}