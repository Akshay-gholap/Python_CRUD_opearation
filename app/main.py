

from fastapi import FastAPI

from app import models
from .database import engine, get_db
from .routers import post,user ,auth, vote



models.Base.metadata.create_all(bind=engine)

app = FastAPI()


my_posts = [
    {"title":"1st post",
    "content":"content of post 1",
    "id":1},
    {"title":"favourite food",
    "content":"I like pizza",
    "id":2}
]
def find_post(id):
    for post in my_posts:
        if id == post["id"]:
            return post 
def find_index_post(id):
    for i, post in enumerate(my_posts):
        if id == post["id"]:
            return i
        
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
async def root():
    return {"message": "Welcome to api !!!!"}


