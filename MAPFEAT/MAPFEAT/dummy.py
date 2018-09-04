import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tabledef import *
 
engine = create_engine('sqlite:///userpass.db', echo=True)

 
# create a Session
Session = sessionmaker(bind=engine)
session = Session()
 
user = User("manjeet.dev1@ucalgary.ca","password1")
session.add(user)
 
user = User("bob@hotmail.com","boss")
session.add(user)
 
user = User("hello@yahoo.ca","man")
session.add(user)
 
# commit the record the database
session.commit()
 
session.commit()