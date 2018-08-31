from sqlalchemy import *
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
 
engine = create_engine('sqlite:///userpass.db', echo=True)
Base = declarative_base()
 
########################################################################
class User(Base):
    """"""
    __tablename__ = "users"
 
    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    is_active = True
    get_id = True
    is_anonymous = False
    #----------------------------------------------------------------------
    def __init__(self, username, password, isactive, get_id(), is_anonymous):
        """"""
        self.username = username
        self.password = password
        self.is_active = isactive
        self.get_id = get_id()
        self.is_anonymous = is_anonymous
 
# create tables
Base.metadata.create_all(engine)