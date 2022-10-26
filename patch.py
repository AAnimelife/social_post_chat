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
        1: {'id_user': 1, 'dialogue_id': 1, 'text': 'test', 'date_post': 'test',

