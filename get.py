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


@app.post('/groups', response_model=GroupsGet)
def create_group(group: GroupsCreate):
    if len(list(data["groups"].keys())) == 0:
        new_id = 1
    else:
        new_id = list(data["groups"].keys())[-1] + 1
    data["groups"][new_id] = group.dict()
    response = GroupsGet(id=new_id, **group.dict())
    return response
