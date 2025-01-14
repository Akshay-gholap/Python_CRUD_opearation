from .. import schemas,models
from ..database import engine, get_db
from fastapi import APIRouter, Response, status, HTTPException, Depends
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import func
from .. import oauth2
router = APIRouter(tags=['posts'])

#@router.get("/posts",response_model=List[schemas.PostOut])
@router.get("/posts",response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db),current_user:int = Depends(oauth2.get_current_user),
limit:int = 10,skip:int=0, search:Optional[str]=""):
    # cursor.execute("""SELECT * FROM posts;""")
    # posts =cursor.fetchall()
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    postsWithVotes = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, 
    models.Post.id==models.Vote.post_id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    
    return postsWithVotes

@router.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate,db: Session = Depends(get_db),current_user:int = Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s,%s,%s) RETURNING 
    # * """,(post.title,post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    # print(current_user.email)
    print(current_user.id)
    new_post= models.Post(owner_id = current_user.id,**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/posts/{id}", response_model=schemas.PostOut)
def get_post(id:int, response:Response,db: Session = Depends(get_db),current_user:int = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s """,(str(id)))
    # post = cursor.fetchone()
    #post = db.query(models.Post).filter(models.Post.id==id).first()
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, 
    models.Post.id==models.Vote.post_id, isouter=True).group_by(models.Post.id).filter(models.Post.id==id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"post with id {id} was not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {}
    return post

@router.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db: Session = Depends(get_db),current_user:int = Depends(oauth2.get_current_user)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """,(str(id)))
    # delete_post = cursor.fetchone()
    post_query = db.query(models.Post).filter(models.Post.id==id)
    deleted_post = post_query.first()
    if deleted_post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"post with id {id} was not found")
    if deleted_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail='''not autherized 
        to perform requested action''')
    else:
        # conn.commit()
        post_query.delete(synchronize_session=False)
        db.commit()

@router.put("/posts/{id}",response_model=schemas.Post)
def update_post(id:int, post:schemas.PostCreate,db: Session = Depends(get_db),current_user:int = Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published=%s WHERE id=%s 
    # RETURNING * """,(post.title,post.content,post.published,str(id)))
    # update_post = cursor.fetchone()
    post_query = db.query(models.Post).filter(models.Post.id==id)
    updated_post = post_query.first()
    print(post.dict())
    if updated_post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"post with id {id} was not found")
    if updated_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail='''not autherized to perform requested action''')

    else:
        # conn.commit()
        post_query.update(post.dict(),synchronize_session=False)
        db.commit()
        
        return post_query.first()