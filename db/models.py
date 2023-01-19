from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from db.database import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__='users'
    id = Column(Integer,primary_key=True,index=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)
    items = relationship('Artical',back_populates='user')
    
    
class Artical(Base):
    __tablename__='articals'
    id = Column(Integer,primary_key=True,index=True)
    title = Column(String)
    content = Column(String)
    published = Column(Boolean)
    user_id = Column(Integer,ForeignKey('users.id'))
    user = relationship('User',back_populates='items')