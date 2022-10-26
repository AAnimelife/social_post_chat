from schemes import Users, UsersGet, UsersCreate, Dialogues, DialoguesGet, DialoguesCreate, MessagesCreate, Messages, \
    MessagesGet, FileMCreate, FileM, FileMGet, GroupsCreate, Groups, GroupsGet, PostsCreate, Posts, PostsGet
from api_and_func_in_api import app

# ДЛЯ ПРИМЕРОВ И ТЕСТОВ/
data = {
    "users": {
        1: {'login': 'test', 'password': 'test', 'is_online': True},
    },
    "dialogues": {
        1: {'date_post': 'test'}
    },
    "messages": {
        1: {'id_user': 1, 'dialogue_id': 1, 'text': 'test', 'date_post': 'test', 'is_read': True}
    },
    "fileM": {
        1: {'message_id': 1, 'date_loading': 'test'}
    },
    "groups": {
        1: {'name': 'test', 'date_post': 'test'}
    },
    "posts": {
        1: {'title': 'test', 'text': 'test', 'user_id': 1, 'date_post': 'test'}
    }
}


# /ДЛЯ ПРИМЕРОВ И ТЕСТОВ


@app.post('/users', response_model=UsersGet)
def create_user(user: UsersCreate):
    if len(list(data["users"].keys())) == 0:
        new_id = 1
    else:
        new_id = list(data["users"].keys())[-1] + 1
    data["users"][new_id] = user.dict()
    response = UsersGet(id=new_id, **user.dict())
    return response


@app.post('/dialogues', response_model=DialoguesGet)
def create_dialogue(dialogue: DialoguesCreate):
    if len(list(data["dialogues"].keys())) == 0:
        new_id = 1
    else:
        new_id = list(data["dialogues"].keys())[-1] + 1
    data["dialogues"][new_id] = dialogue.dict()
    response = DialoguesGet(id=new_id, **dialogue.dict())
    return response


@app.post('/messages', response_model=MessagesGet)
def create_message(message: MessagesCreate):
    if len(list(data["messages"].keys())) == 0:
        new_id = 1
    else:
        new_id = list(data["messages"].keys())[-1] + 1
    data["messages"][new_id] = message.dict()
    response = MessagesGet(id=new_id, **message.dict())
    return response


@app.post('/fileM', response_model=FileMGet)
def create_file_m(file_m: FileMCreate):
    if len(list(data["fileM"].keys())) == 0:
        new_id = 1
    else:
        new_id = list(data["fileM"].keys())[-1] + 1
    data["fileM"][new_id] = file_m.dict()
    response = FileMGet(id=new_id, **file_m.dict())
    return response


@app.post('/groups', response_model=GroupsGet)
def create_group(group: GroupsCreate):
    if len(list(data["groups"].keys())) == 0:
        new_id = 1
    else:
        new_id = list(data["groups"].keys())[-1] + 1
    data["groups"][new_id] = group.dict()
    response = GroupsGet(id=new_id, **group.dict())
    return response


@app.post('/posts', response_model=PostsGet)
def create_post(post: PostsCreate):
    if len(list(data["posts"].keys())) == 0:
        new_id = 1
    else:
        new_id = list(data["posts"].keys())[-1] + 1
    data["posts"][new_id] = post.dict()
    response = PostsGet(id=new_id, **post.dict())
    return response
