from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app import db

engine = create_engine('sqlite:///user.db', echo=True)
db_session = scoped_session(sessionmaker(autocommit=True,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()
    

class User(Base):
    __tablename__ = 'Users'
    
    name = db.Column(db.String(50), primary_key=True)
    email = db.Column(db.String(120))
    password = db.Column(db.String(50))

    def __init__(self, name, email,password):
        self.name = name
        self.email = email
        self.password = password

   # def is_authenticated(self):
    #    return True

   # def __repr__(self):
    #    return '<User %r>' % (self.name)

Base.metadata.create_all(bind=engine)