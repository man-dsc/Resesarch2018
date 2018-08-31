import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tabledef import *
 
engine = create_engine('sqlite:///userpass.db', echo=True)

 
# create a Session
Session = sessionmaker(bind=engine)
session = Session()
 
user = User("admin","password", True, True, True)
session.add(user)
 
user = User("manjeet","boss",True, True, True)
session.add(user)
 
user = User("jump","man",True, True, True)
session.add(user)
 
# commit the record the database
session.commit()
 
session.commit()