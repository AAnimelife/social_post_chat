from typing import List

from models import Users, Posts, Dialogues, dialogues_table, Messages
from sqlalchemy.orm import Session
import schemes


def get_user(db: Session, user_id: int):
    return db.query(Users).filter(Users.id == user_id).first()


def get_user_login_by_id(db: Session, user_id: int):
    user = get_user(db, user_id)
    return user.login


def update_user_is_online(db: Session, user_id: int, new_status: int):
    db.query(Users).filter(Users.id == user_id).all()[0].is_online = new_status
    db.commit()
    return db.query(Users).filter(Users.id == user_id).all()[0]


def get_friends_id(db: Session, user_id: int):
    user = get_user(db, user_id)
    friends = list(map(int, list(user.users_friends.split('&'))))
    return friends


def get_friends(db: Session, user_id: int):
    friends_id = get_friends_id(db, user_id)
    friends = []
    for friend_id in friends_id:
        friends.append(get_user(db, friend_id))
    return friends


def update_user(db: Session, user_id: int, new_user: schemes.UsersCreate):
    user = get_user(db, user_id)
    user.name = new_user.name
    user.second_name = new_user.second_name
    user.login = new_user.login
    user.password = new_user.password
    user.data_born = new_user.data_born
    user.email = new_user.email
    user.avatar_img = new_user.avatar_img
    friends = user.users_friends
    user.users_dialogues = []
    if friends:
        friends = list(map(int, list(friends.split('&'))))
        for i in friends:
            delete_friend(db, i, user_id)
    for dialogue_id in new_user.dialogues:
        create_dialogue_connection(db, user_id, dialogue_id)

    for friend_id in new_user.friends:
        create_friend(db, user_id, friend_id)
    db.commit()
    return user


def get_user_id_by_login(db: Session, login: str):
    user = get_user_by_login(db, login)
    return user.id


def get_user_by_email(db: Session, email: str):
    return db.query(Users).filter(Users.email == email).first()


def get_user_by_name(db: Session, name: str, second_name: str = ""):
    if second_name == "":
        return db.query(Users).filter(Users.name == name).first()
    return db.query(Users).filter(Users.name == name and Users.second_name == second_name).first()


def get_user_by_login(db: Session, login: str):
    return db.query(Users).filter(Users.login == login).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Users).offset(skip).limit(limit).all()


def get_users_id_in_dialogue(db: Session, dialogue_id: int):
    dialogue = get_dialogue(db, dialogue_id)
    users_id = []
    for i in dialogue.dialogues_users:
        users_id.append(i.id)
    return users_id


def get_dialogue_users(db: Session, dialogue_id: int):
    users = []
    for user_id in get_users_id_in_dialogue(db, dialogue_id):
        users.append(get_user(db, user_id))
    return users


def create_user(db: Session, user: schemes.UsersCreate):
    new_id = 1
    if len(db.query(Users).all()) > 0:
        new_id = db.query(Users).all()[-1].id + 1
    user_bd = Users(id=new_id, name=user.name, second_name=user.second_name, login=user.login, password=user.password,
                    data_born=user.data_born, is_online=user.is_online, avatar_img=user.avatar_img, email=user.email,
                    users_friends="")

    for dialogue_id in user.dialogues:
        dialogue = get_dialogue(db, dialogue_id)
        user_bd.users_dialogues.append(dialogue)

    for friend_id in user.friends:
        if get_user(db, friend_id):
            user_bd.users_friends += str(friend_id) + '&'
            user1 = get_user(db, friend_id)
            if len(user1.users_friends) == 0:
                user1.users_friends += str(new_id)
            else:
                user1.users_friends += '&' + str(new_id)

    if len(user.friends) > 0:
        user_bd.users_friends = user_bd.users_friends[:-1]
    db.add(user_bd)
    db.commit()
    db.refresh(user_bd)


def create_friend(db: Session, user_id: int, friend_id: int):
    user = get_user(db, user_id)
    friends_id = []
    friends_id += user.users_friends.split('&')
    if friends_id.count(str(friend_id)) > 0:
        return "already been"
    friend = get_user(db, friend_id)
    if len(user.users_friends) == 0:
        user.users_friends += str(friend_id)
    else:
        user.users_friends += '&' + str(friend_id)
    if len(friend.users_friends) == 0:
        friend.users_friends += str(user_id)
    else:
        friend.users_friends += '&' + str(user_id)
    db.commit()


def create_friend_by_login(db: Session, user_id: int, friend_login: str):
    friend_id = get_user_id_by_login(db, friend_login)
    return create_friend(db, user_id, friend_id)


def delete_friend_fake(db: Session, user_id: int, friend_id: int):
    user = get_user(db, user_id)
    friends_id = list(map(int, list(user.users_friends.split('&'))))
    if friends_id.count(friend_id) > 0:
        friends_id.pop(friends_id.index(friend_id))
    if len(friends_id) == 0:
        db.query(Users).filter(Users.id == user_id).all()[0].users_friends = ""
    else:
        db.query(Users).filter(Users.id == user_id).all()[0].users_friends = ""
        for j in friends_id:
            db.query(Users).filter(Users.id == user_id).all()[0].users_friends += str(j) + '&'
        db.query(Users).filter(Users.id == user_id).all()[0].users_friends = \
            db.query(Users).filter(Users.id == user_id).all()[0].users_friends[:-1]
    db.commit()


def delete_friends(db: Session, user_id: int):
    user = get_user(db, user_id)
    if len(user.users_friends) == 0:
        return 0
    friends_id = list(map(int, list(user.users_friends.split('&'))))
    user.users_friends = ""
    for friend_id in friends_id:
        friend = get_user(db, friend_id)
        friend_friends_id = list(map(int, list(friend.users_friends.split('&'))))
        if friend_friends_id.count(user_id) > 0:
            friend_friends_id.pop(friend_friends_id.index(user_id))
        if len(friend_friends_id) == 0:
            friend.users_friends = ""
        else:
            friend.users_friends = ""
            for j in friend_friends_id:
                friend.users_friends += str(j) + '&'
            friend.users_friends = friend.users_friends[:-1]
    db.commit()


def delete_friend(db: Session, user_id: int, friend_id: int):
    delete_friend_fake(db, user_id, friend_id)
    delete_friend_fake(db, friend_id, user_id)


def delete_friend_by_login(db: Session, user_id: int, friend_login: str):
    friend_id = get_user_id_by_login(db, friend_login)
    delete_friend(db, user_id, friend_id)


def get_dialogue(db: Session, dialogue_id: int):
    return db.query(Dialogues).filter(Dialogues.id == dialogue_id).first()


def create_dialogue_connection(db: Session, user_id: int, dialogue_id: int):
    dialogue = get_dialogue(db, dialogue_id)
    if get_users_id_in_dialogue(db, dialogue_id).count(user_id) > 0:
        return "already been"
    else:
        user = get_user(db, user_id)
        dialogue.dialogues_users.append(user)
        db.commit()


def get_dialogues_by_user_id(db: Session, user_id: int):
    user = get_user(db, user_id)
    return user.users_dialogues


def get_dialogues(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Dialogues).offset(skip).limit(limit).all()


def create_dialogue(db: Session, dialogue: schemes.DialoguesCreate):
    if len(db.query(Dialogues).all()) == 0:
        new_id = 1
    else:
        new_id = db.query(Dialogues).all()[-1].id + 1
    response = Dialogues(id=new_id, name=dialogue.name, img_dialogue=dialogue.img, date_dialogues=dialogue.data_post)

    for user_id in dialogue.users:
        user = get_user(db, user_id)
        response.dialogues_users.append(user)

    db.add(response)
    db.commit()
    db.refresh(response)


def delete_dialogue_connection(db: Session, user_id: int, dialogue_id: int):
    user = get_user(db, user_id)
    user.users_dialogues.pop(user.users_dialogues.index(get_dialogue(db, dialogue_id)))
    db.commit()


def get_post(db: Session, post_id: int):
    return db.query(Posts).filter(Posts.id == post_id).first()


def get_posts_by_user_id(db: Session, user_id, skip: int = 0, limit: int = 100):
    return db.query(Posts).filter(Posts.user_id == user_id).offset(skip).limit(limit).all()


def get_posts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Posts).offset(skip).limit(limit).all()


def create_post(db: Session, post: schemes.PostsCreate):
    if len(db.query(Posts).all()) == 0:
        new_id = 1
    else:
        new_id = db.query(Posts).all()[-1].id + 1
    response = Posts(id=new_id, title=post.title, text=post.text, img_post=post.img, user_id=post.user_id,
                     date_posts=post.date_post, likes=post.likes)
    db.add(response)
    db.commit()
    db.refresh(response)
    return post


def get_message(db: Session, message_id: int):
    return db.query(Messages).filter(Messages.id == message_id).first()


def get_messages_by_user_id(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(Messages).filter(Messages.user_id == user_id).offset(skip).limit(limit).all()


def get_messages_by_dialogue_id(db: Session, dialogue_id: int, skip: int = 0, limit: int = 100):
    return db.query(Messages).filter(Messages.dialogue_id == dialogue_id).offset(skip).limit(limit).all()


def get_messages(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Messages).offset(skip).limit(limit).all()


def create_message(db: Session, message: schemes.MessagesCreate):
    if len(db.query(Messages).all()) == 0:
        new_id = 1
    else:
        new_id = db.query(Messages).all()[-1].id + 1
    response = Messages(id=new_id, user_id=message.id_user, dialogue_id=message.dialogue_id, text=message.text,
                        date_messages=message.date_post, is_read=message.is_read)
    db.add(response)
    db.commit()
    db.refresh(response)
    return message


def delete_user(db: Session, user_id: int):
    user = get_user(db, user_id)
    user.users_dialogues = []
    delete_friends(db, user_id)
    db.delete(db.query(Users).filter(Users.id == user_id).first())
    db.commit()


def delete_post(db: Session, post_id):
    post = get_post(db, post_id)
    if post.user_id:
        user = get_user(db, post.user_id)
        user.users_posts.pop(user.users_posts.index(post))
        db.delete(post)
    db.commit()


def delete_dialogue(db: Session, dialogue_id):
    dialogue = get_dialogue(db, dialogue_id)
    dialogue.dialogues_users = []
    db.delete(db.query(Dialogues).filter(Dialogues.id == dialogue_id).first())
    db.commit()


def delete_message(db: Session, message_id: int):
    message = get_message(db, message_id)
    if message.dialogue_id:
        dialogue = get_dialogue(db, message.dialogue_id)
        dialogue.dialogues_messages.pop(dialogue.dialogues_messages.index(message))
        db.delete(message)
    db.commit()


def update_message_text(db: Session, message_id: int, text: str):
    if get_message(db, message_id):
        message = get_message(db, message_id)
        message.text = text
    db.commit()


def update_message_is_read(db: Session, message_id: int, is_read: int):
    if get_message(db, message_id):
        message = get_message(db, message_id)
        message.is_read = is_read
    db.commit()


def update_post_title(db: Session, post_id: int, title: str):
    if get_post(db, post_id):
        post = get_post(db, post_id)
        post.title = title
    db.commit()


def update_post_img(db: Session, post_id: int, img: str):
    if get_post(db, post_id):
        post = get_post(db, post_id)
        post.img_post = img
    db.commit()


def update_post_text(db: Session, post_id: int, text: str):
    if get_post(db, post_id):
        post = get_post(db, post_id)
        post.text = text
    db.commit()


def update_post_likes(db: Session, post_id: int, likes: int):
    if get_post(db, post_id):
        post = get_post(db, post_id)
        post.likes = likes
    db.commit()


def update_dialogue_name(db: Session, dialogue_id: int, name: str):
    if get_dialogue(db, dialogue_id):
        dialogue = get_dialogue(db, dialogue_id)
        dialogue.name = name
    db.commit()


def update_dialogue_img(db: Session, dialogue_id: int, img: str):
    if get_dialogue(db, dialogue_id):
        dialogue = get_dialogue(db, dialogue_id)
        dialogue.img_dialogue = img
    db.commit()


def update_dialogue_users(db: Session, dialogue_id: int, users: List[int]):
    if get_dialogue(db, dialogue_id):
        dialogue = get_dialogue(db, dialogue_id)
        dialogue.dialogues_users = []
        for user_id in users:
            if get_user(db, user_id):
                dialogue.dialogues_users.append(get_user(db, user_id))
    db.commit()

