from sqlalchemy import Column, Integer, String, ForeignKey, Table, Date, Time
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()

friends_table = Table('Friends_table', Base.metadata,
                      Column('First_User', Integer, ForeignKey('Users.id')),
                      Column('Second_User', Integer, ForeignKey('Users.id'))
                      )

dialogues_table = Table('Dialogues_table', Base.metadata,
                        Column('User', Integer, ForeignKey('Users.id')),
                        Column('Dialogue', Integer, ForeignKey('Dialogues.id'))
                        )

users_group_table = Table('Users_group_table', Base.metedata,
                          Column("Users", Integer, ForeignKey('Users.id')),
                          Column("Groups", Integer, ForeignKey("Groups.id")),
                          )


class Users(Base):
    __tablename__ = 'Users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    second_name = Column(String)
    login = Column(String)
    password = Column(String)
    data_born = Column(Date)
    is_online = Column(Integer)  # 1 - online, 0 - offline, (2 - <5 minutes offline)
    avatar_img = Column(Integer)  # link for string
    email = Column(String)
    users_posts = relationship("Posts", backref="user")
    users_friends = relationship("Friends", backref="user", cascade="all,delete,save-update",
                                 secondary=friends_table)
    users_dialogues = relationship("Dialogues", backref="user", cascade="all,delete,save-update",
                                   secondary=dialogues_table)
    users_groups = relationship("Groups", backref="user", cascade="all,delete,save-update",
                                secondary=users_group_table)

    def __repr__(self):
        return "<Person('%s','%s', '%s')>" % (self.name, self.second_name, self.is_online)


class Dialogues(Base):
    __tablename__ = 'Dialogues'
    id = Column(Integer, primary_key=True)
    dialogues_messages = relationship("Messages", backref="dialogue")
    name = Column(String)  # - если надо
    img_dialogue = Column(String)  # - link for string
    data_dialogues = Column(Date)
    dialogues_users = relationship("Users", backref="dialogue", cascade="all,delete,save-update",
                                   secondary=dialogues_table)


class FileM(Base):
    __tablename__ = 'FileM'
    id = Column(Integer, primary_key=True)
    link = Column(String)  # - link for string
    message_id = Column(Integer, ForeignKey("Messages.id"))
    data_loading = Column(Date)


class Messages(Base):
    __tablename__ = 'Messages'
    id = Column(Integer, primary_key=True)
    num_user = Column(Integer)  # 1 - first person, 2 - second person
    dialogue_id = Column(Integer, ForeignKey("Dialogues.id"))
    message = Column(String)
    date_messages = Column(Time)
    is_read = Column(Integer)  # 1 - read, 0 - not read
    files = relationship("FileM", backref="message")


class Groups(Base):
    __tablename__ = 'Groups'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    date_born = Column(Date)
    posts = relationship("Posts", backref="group")
    users = relationship("Users", backref="group", cascade="all,delete,save-update",
                         secondary=users_group_table)


class Posts(Base):
    __tablename__ = 'Posts'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    img_post = Column(String)  # link for string
    text = Column(String)
    user_id = Column(Integer, ForeignKey("Users.id"))
    group_id = Column(Integer, ForeignKey("Groups.id"))
    date_posts = Column(Date)
    #  likes = Column(Integer)
