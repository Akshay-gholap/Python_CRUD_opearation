from .. import schemas,models
from .. import database, utils
from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session

router = APIRouter(tags=['users'])

@router.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate,db: Session = Depends(database.get_db)):
    #hash the password
    hashed_password = utils.get_password_hash(user.password) #for hashing password
    user.password = hashed_password
    new_user= models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/users/{id}",response_model=schemas.UserOut)
def get_user(id:int,db: Session = Depends(database.get_db) ):
    user = db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"user with id {id} was not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {}
    return user  