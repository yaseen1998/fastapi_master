from sqlalchemy import Boolean, Column, ForeignKey, Integer, String,DATETIME
from db.database import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__='users'
    id = Column(Integer,primary_key=True,index=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)
    items = relationship('Artical',back_populates='user')
    post = relationship('DbPost2',back_populates='user') 
    
class Artical(Base):
    __tablename__='articals'
    id = Column(Integer,primary_key=True,index=True)
    title = Column(String)
    content = Column(String)
    published = Column(Boolean)
    user_id = Column(Integer,ForeignKey('users.id'))
    user = relationship('User',back_populates='items')
    

class DbPost(Base):
    __tablename__='dbposts'
    id = Column(Integer,primary_key=True,index=True)
    title = Column(String)
    content = Column(String)
    creator = Column(String)
    timstamp = Column(DATETIME)
    image_url = Column(String)
    
    
    
class DbPost2(Base):
    __tablename__='dbposts2'
    id = Column(Integer,primary_key=True,index=True)
    title = Column(String)
    timestamp = Column(DATETIME)
    image_url = Column(String)
    image_url_type = Column(String)
    caption= Column(String)
    user_id = Column(Integer,ForeignKey('users.id'))
    user = relationship('User',back_populates='post')
    comments = relationship('DbComment',back_populates='post')
    
    
class DbComment(Base):
    __tablename__='dbcomments'
    id = Column(Integer,primary_key=True,index=True)
    username = Column(String)
    text = Column(String)
    post_id = Column(Integer,ForeignKey('dbposts2.id'))
    timestamp = Column(DATETIME)
    post = relationship('DbPost2',back_populates='comments')
