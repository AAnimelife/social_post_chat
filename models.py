from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


def row_to_dict(row):
    d = {}
    for column in row.__table__.columns:
        d[column.name] = str(getattr(row, column.name))

    return d


friends_table = Table('Friends_table', Base.metadata,
                      Column('First_User', Integer, ForeignKey('Users.id')),
                      Column('Second_User', Integer)
                      )

dialogues_table = Table('Dialogues_table', Base.metadata,
                        Column('User', Integer, ForeignKey('Users.id')),
                        Column('Dialogue', Integer, ForeignKey('Dialogues.id'))
                        )


class Users(Base):
    __tablename__ = 'Users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    second_name = Column(String)
    login = Column(String)
    password = Column(String)
    data_born = Column(String)
    is_online = Column(Integer)  # 1 - online, 0 - offline, (2 - <5 minutes offline)
    avatar_img = Column(String)  # link for string
    email = Column(String)
    users_posts = relationship("Posts", backref="user")

    users_dialogues = relationship("Dialogues", backref="user", cascade="all,delete,save-update",
                                   secondary=dialogues_table, overlaps="users_dialogues,user")
    users_friends = Column(String)

    def __repr__(self):
        return "<Person('%s','%s', '%s')>" % (self.name, self.second_name, self.is_online)


class Dialogues(Base):
    __tablename__ = 'Dialogues'
    id = Column(Integer, primary_key=True)
    dialogues_messages = relationship("Messages", backref="dialogue")
    name = Column(String)  # - если надо
    img_dialogue = Column(String)  # - link for string
    date_dialogues = Column(String)
    dialogues_users = relationship("Users", backref="dialogue", cascade="all,delete,save-update",
                                   secondary=dialogues_table, overlaps="users_dialogues,user")


class Messages(Base):
    __tablename__ = 'Messages'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)  # 1 - first person, 2 - second person
    dialogue_id = Column(Integer, ForeignKey("Dialogues.id"))
    text = Column(String)
    date_messages = Column(String)
    is_read = Column(Integer)  # 1 - read, 0 - not read


class Posts(Base):
    __tablename__ = 'Posts'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    img_post = Column(String)  # link for string
    text = Column(String)
    user_id = Column(Integer, ForeignKey("Users.id"))
    date_posts = Column(String)
    likes = Column(Integer)  # likes count
