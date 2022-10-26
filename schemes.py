from pydantic import BaseModel
from typing import Optional, List


class Users(BaseModel):
    name:  Optional[str] = None
    second_name: Optional[str] = None
    login: str
    password: str
    data_born: Optional[str]
    is_online: int  # 1 - online, 0 - offline, (2 - <5 minutes offline)
    avatar_img: Optional[str]  # link for string
    email: Optional[str]
    dialogues: Optional[List[int]] = []
    friends: Optional[List[int]] = []


class UsersCreate(Users):
    pass


class UsersGet(Users):
    id = int


class Friends(BaseModel):
    pass


class Dialogues(BaseModel):
    name: Optional[str] = "New Dialogue"
    img: Optional[str]  # link
    data_post: str
    users: Optional[List[int]] = []


class DialoguesCreate(Dialogues):
    pass


class DialoguesGet(Dialogues):
    id = int


class Messages(BaseModel):
    id_user: int
    dialogue_id: int
    text: str
    date_post: str
    is_read: int  # 1 - read, 0 - not read}


class MessagesCreate(Messages):
    pass


class MessagesGet(Messages):
    id = int


class Posts(BaseModel):
    title: str
    img: Optional[str]  # link for string
    text: str
    user_id: int
    date_post: str
    likes: int


class PostsCreate(Posts):
    pass


class PostsGet(Posts):
    id = int
