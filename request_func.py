from typing import List

import requests
import json
from schemes import UsersCreate, DialoguesCreate, MessagesCreate, PostsCreate
link = "http://127.0.0.1:8000/"


def get_user(user_id: int):
    return json.loads(requests.get(link + f"user/{user_id}").text)


def get_user_by_name(name: str, second_name: str = ""):
    if second_name == "":
        return json.loads(requests.get(link + f"user_by_name/{name}").text)
    else:
        return json.loads(requests.get(link + f"user/{name}/{second_name}").text)


def get_users(skip: int = 0, limit: int = 100):
    return json.loads(requests.get(link + f"users/{skip}/{limit}").text)


def get_user_login_by_id(user_id):
    return json.loads(requests.get(link + f'user_login/{user_id}').text)


def get_user_id_by_login(user_login):
    return json.loads(requests.get(link + f'user_id/{user_login}').text)


def get_user_dialogues(user_id: int):
    return json.loads(requests.get(link + f'user_dialogues/{user_id}').text)


def get_dialogue_users(dialogue_id: int):
    return json.loads(requests.get(link + f'dialogue_users/{dialogue_id}').text)


def get_dialogue(dialogue_id: int):
    return json.loads(requests.get(link + f'dialogue/{dialogue_id}').text)


def get_dialogues(skip: int = 0, limit: int = 100):
    return json.loads(requests.get(link + f'dialogues/{skip}/{limit}').text)


def get_post(post_id: int):
    return json.loads(requests.get(link + f'post/{post_id}').text)


def get_posts(skip: int = 0, limit: int = 100):
    return json.loads(requests.get(link + f'posts/{skip}/{limit}').text)


def get_user_posts(user_id: int, skip: int = 0, limit: int = 100):
    return json.loads(requests.get(link + f'user_posts/{user_id}/{skip}/{limit}').text)


def get_message(message_id: int):
    return json.loads(requests.get(link + f'message/{message_id}').text)


def get_messages(dialogue_id, skip: int = 0, limit: int = 100):
    return json.loads(requests.get(link + f'messages/{dialogue_id}/{skip}/{limit}').text)


def get_friends_id(user_id: int):
    return json.loads(requests.get(link + f'friends_id/{user_id}').text)


def get_friends(user_id: int):
    return json.loads(requests.get(link + f'friends/{user_id}').text)


def create_user(user: UsersCreate):
    return requests.post(link + 'users', json=user)


def create_dialogue(dialogue: DialoguesCreate):
    return requests.post(link + 'dialogues', json=dialogue)


def create_message(message: MessagesCreate):
    return requests.post(link + 'messages', json=message)


def create_post(new_post: PostsCreate):
    return requests.post(link + 'posts', json=new_post)


def create_dialogue_connection(user_id: int, dialogue_id: int):
    return requests.post(link + f'dialogue_connection/{user_id}/{dialogue_id}')


def create_friend(user_id: int, friends_id: int):
    return requests.post(link + f'friends/{user_id}/{friends_id}')


def create_friend_by_login(user_id: int, friend_login: str):
    return requests.post(link + f'friend_by_login/{user_id}/{friend_login}')


def delete_user(user_id: int):
    return requests.delete(link + f'user/{user_id}')


def delete_post(post_id: int):
    return requests.delete(link + f'post/{post_id}')


def delete_dialogue(dialogue_id: int):
    return requests.delete(link + f'dialogue/{dialogue_id}')


def delete_message(message_id: int):
    return requests.delete(link + f'message/{message_id}')


def delete_friend(user_id: int, friend_id: int):
    return requests.delete(link + f'friend/{user_id}/{friend_id}')


def delete_friend_by_login(user_id: int, friend_login: str):
    return requests.delete(link + f'friend_by_login/{user_id}/{friend_login}')


def delete_dialogue_connection(user_id: int, dialogue_id: int):
    return requests.delete(link + f'dialogue_connection/{user_id}/{dialogue_id}')


def update_user(user_id: int, user: UsersCreate):
    return requests.patch(link + f'user/{user_id}', json=user)


def update_user_is_online(user_id: int, is_online: int):
    return requests.patch(link + f'user/{user_id}/{is_online}')


def update_message(message_id: int, new_text: str):
    return requests.patch(link + f'message_text/{message_id}/{new_text}')


def update_message_status(message_id: int, is_read: int):
    return requests.patch(link + f'message_is_read/{message_id}/{is_read}')


def update_post_title(post_id: int, title: str):
    return requests.patch(link + f'post_title/{post_id}/{title}')


def update_post_img(post_id: int, img: str):
    return requests.patch(link + f'post_img/{post_id}/{img}')


def update_post_text(post_id: int, text: str):
    return requests.patch(link + f'post_text/{post_id}/{text}')


def update_post_likes(post_id: int, likes: int):
    return requests.patch(link + f'post_likes/{post_id}/{likes}')


def update_dialogue_name(dialogue_id: int, name: str):
    return requests.patch(link + f'dialogue_name/{dialogue_id}/{name}')


def update_dialogue_img(dialogue_id: int, img: str):
    return requests.patch(link + f'dialogue_img/{dialogue_id}/{img}')


def update_dialogue_users(dialogue_id: int, users: List[int]):
    return requests.patch(link + f'dialogue_users/{dialogue_id}/{users}')

