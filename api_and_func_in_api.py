import uvicorn
from fastapi import FastAPI, Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import crud
from crud import *
from models import Base
from schemes import UsersGet, UsersCreate, DialoguesGet, DialoguesCreate, MessagesCreate, MessagesGet, PostsCreate, \
    PostsGet

engine = create_engine('sqlite:///webinar.db', echo=True)
Base.metadata.create_all(engine)
session = sessionmaker(bind=engine)

app = FastAPI()


def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()


@app.get("/user/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    return crud.get_user(db, user_id)


@app.get("/dialogue_users/{dialogue_id}")
def get_dialogue_users(dialogue_id: int, db: Session = Depends(get_db)):
    return crud.get_dialogue_users(db, dialogue_id)


@app.get('/friends_id/{user_id}')
def get_friends(user_id: int, db: Session = Depends(get_db)):
    return crud.get_friends_id(db, user_id)


@app.get('/friends/{user_id}')
def get_friends(user_id: int, db: Session = Depends(get_db)):
    return crud.get_friends(db, user_id)


@app.get("/dialogue/{dialogue_id}")
def get_dialogue(dialogue_id: int, db: Session = Depends(get_db)):
    return crud.get_dialogue(db, dialogue_id)


@app.get("/message/{message_id}")
def get_message(message_id: int, db: Session = Depends(get_db)):
    return crud.get_message(db, message_id)


@app.get("/messages/{dialogue_id}/{skip}/{limit}")
def get_messages(dialogue_id: int, skip: int, limit: int, db: Session = Depends(get_db)):
    return crud.get_messages_by_dialogue_id(db, dialogue_id, skip, limit)


@app.get("/post/{post_id}")
def get_post_api(post_id: int, db: Session = Depends(get_db)):
    return crud.get_post(db, post_id)


@app.get("/user_posts/{user_id}/{skip}/{limit}")
def get_user_posts(user_id: int, skip: int, limit: int, db: Session = Depends(get_db)):
    return crud.get_posts_by_user_id(db, user_id, skip, limit)


@app.get("/user_by_name/{name}")
def get_user_by_name(name: str, db: Session = Depends(get_db)):
    return crud.get_user_by_name(db, name)


@app.get("/user/{name}/{second_name}")
def get_user(name: str, second_name: str, db: Session = Depends(get_db)):
    return crud.get_user_by_name(db, name, second_name)


@app.get("/users/{skip}/{limit}")
def get_users(skip: int, limit: int, db: Session = Depends(get_db)):
    return crud.get_users(db, skip, limit)


@app.get("/dialogues")
def get_dialogues(db: Session = Depends(get_db)):
    return crud.get_dialogues(db)


@app.get("/user_dialogues/{user_id}")
def get_user_dialogues(user_id: int, db: Session = Depends(get_db)):
    return crud.get_dialogues_by_user_id(db, user_id)


@app.get("/dialogues/{skip}")
def get_dialogue(skip: int, db: Session = Depends(get_db)):
    return crud.get_dialogues(db, skip)


@app.get("/dialogues/{skip}/{limit}")
def get_dialogues(skip: int, limit: int, db: Session = Depends(get_db)):
    return crud.get_dialogues(db, skip, limit)


@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    return crud.get_posts(db)


@app.get("/posts/{skip}")
def get_posts(skip: int, db: Session = Depends(get_db)):
    return crud.get_posts(db, skip)


@app.get("/posts/{skip}/{limit}")
def get_posts(skip: int, limit: int, db: Session = Depends(get_db)):
    return crud.get_posts(db, skip, limit)


@app.patch("/user/{user_id}")
def update_user(user_id: int, user: UsersCreate, db: Session = Depends(get_db)):
    return crud.update_user(db, user_id, user)


@app.patch("/user/{user_id}/{is_online}")
def update_user_is_online(user_id: int, is_online: int, db: Session = Depends(get_db)):
    return crud.update_user_is_online(db, user_id, is_online)


@app.delete("/friend/{user_id}/{friend_id}")
def delete_friend(user_id: int, friend_id: int, db: Session = Depends(get_db)):
    return crud.delete_friend(db, user_id, friend_id)


@app.delete("/friend_by_login/{user_id}/{friend_login}")
def delete_friend_by_login(user_id: int, friend_login: str, db: Session = Depends(get_db)):
    return crud.delete_friend_by_login(db, user_id, friend_login)


@app.delete("/all_user_friends/{user_id}")
def delete_user_friends(user_id: int, db: Session = Depends(get_db)):
    return crud.delete_friends(db, user_id)


@app.get("/user_id/{login}")
def get_user_id_by_login(login: str, db: Session = Depends(get_db)):
    return crud.get_user_id_by_login(db, login)


@app.get("/user_login/{user_id}")
def get_user_login_by_id(user_id: int, db: Session = Depends(get_db)):
    return crud.get_user_login_by_id(db, user_id)


@app.delete("/dialogue_connection/{user_id}/{dialogue_id}")
def delete_dialogue_connection(user_id: int, dialogue_id: int, db: Session = Depends(get_db)):
    return crud.delete_dialogue_connection(db, user_id, dialogue_id)


@app.post('/users', response_model=UsersGet)
def create_user(user: UsersCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)


@app.post('/dialogues', response_model=DialoguesGet)
def create_dialogue(dialogue: DialoguesCreate, db: Session = Depends(get_db)):
    return crud.create_dialogue(db=db, dialogue=dialogue)


@app.post('/dialogue_connection/{user_id}/{dialogue_id}')
def create_dialogue_connection(user_id: int, dialogue_id: int, db: Session = Depends(get_db)):
    return crud.create_dialogue_connection(db, user_id, dialogue_id)


@app.post('/messages', response_model=MessagesGet)
def create_message(message: MessagesCreate, db: Session = Depends(get_db)):
    return crud.create_message(db=db, message=message)


@app.post('/posts', response_model=PostsGet)
def create_post(post: PostsCreate, db: Session = Depends(get_db)):
    return crud.create_post(db=db, post=post)


@app.post('/friends/{user_id}/{friend_id}')
def create_friend(user_id: int, friend_id: int, db: Session = Depends(get_db)):
    return crud.create_friend(db=db, user_id=user_id, friend_id=friend_id)


@app.post('/friend_by_login/{user_id}/{friend_login}')
def create_friend(user_id: int, friend_login: str, db: Session = Depends(get_db)):
    return crud.create_friend_by_login(db=db, user_id=user_id, friend_login=friend_login)


@app.delete('/user/{user_id}')
def delete_user(user_id: int, db: Session = Depends(get_db)):
    return crud.delete_user(db, user_id)


@app.delete('/post/{post_id}')
def delete_post(post_id: int, db: Session = Depends(get_db)):
    return crud.delete_post(db, post_id)


@app.delete('/dialogue/{dialogue_id}')
def delete_dialogue(dialogue_id: int, db: Session = Depends(get_db)):
    return crud.delete_dialogue(db, dialogue_id)


@app.delete('/message/{message_id}')
def delete_message(message_id: int, db: Session = Depends(get_db)):
    return crud.delete_message(db, message_id)


@app.patch('/message_text/{message_id}/{new_text}')
def update_message(message_id: int, new_text: str, db: Session = Depends(get_db)):
    return crud.update_message_text(db, message_id, new_text)


@app.patch('/message_is_read/{message_id}/{is_read}')
def update_message_status(message_id: int, is_read: int, db: Session = Depends(get_db)):
    return crud.update_message_is_read(db, message_id, is_read)


@app.patch('/post_title/{post_id}/{title}')
def update_post_title(post_id: int, title: str, db: Session = Depends(get_db)):
    return crud.update_post_title(db, post_id, title)


@app.patch('/post_img/{post_id}/{img}')
def update_post_img(post_id: int, img: str, db: Session = Depends(get_db)):
    return crud.update_post_img(db, post_id, img)


@app.patch('/post_text/{post_id}/{text}')
def update_post_text(post_id: int, text: str, db: Session = Depends(get_db)):
    return crud.update_post_text(db, post_id, text)


@app.patch('/post_likes/{post_id}/{likes}')
def update_post_likes(post_id: int, likes: int, db: Session = Depends(get_db)):
    return crud.update_post_likes(db, post_id, likes)


@app.patch('/dialogue_name/{dialogue_id}/{name}')
def update_dialogue_name(dialogue_id: int, name: str, db: Session = Depends(get_db)):
    return crud.update_dialogue_name(db, dialogue_id, name)


@app.patch('/dialogue_img/{dialogue_id}/{img}')
def update_dialogue_img(dialogue_id: int, img: str, db: Session = Depends(get_db)):
    return crud.update_dialogue_img(db, dialogue_id, img)


@app.patch('/dialogue_users/{dialogue_id}/{users}')
def update_dialogue_users(dialogue_id: int, users, db: Session = Depends(get_db)):
    return crud.update_dialogue_users(db, dialogue_id, users)


uvicorn.run(app, host="127.0.0.1", port=8000)
