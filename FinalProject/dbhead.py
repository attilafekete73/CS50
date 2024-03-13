import sqlalchemy as db
from sqlalchemy.orm import sessionmaker, declarative_base


engine=db.create_engine("postgresql://postgres:Gerzson4Vilagmindenseg!@localhost:5432/CS50FP")
Base = declarative_base()
metaData=db.MetaData()
metaData.reflect(bind=engine)
USERS=metaData.tables["users"]
COURSES=metaData.tables["courses"]
DOCUMENTS=metaData.tables["documents"]
TAGS=metaData.tables["tags"]
COMMENTS=metaData.tables["comments"]
USERCOURSES=metaData.tables["usercourses"]
DOCUTAGS=metaData.tables["docutags"]

class User(Base):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    username = db.Column(db.String)
    hash=db.Column(db.String)
    
class Course(Base):
    __tablename__='courses'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    coursename = db.Column(db.String)
    
class Document(Base):
    __tablename__='documents'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    path = db.Column(db.String)
    name = db.Column(db.String)
    date = db.Column(db.Date)
    courseid = db.Column(db.Integer,db.ForeignKey('courses.id'))
    userid = db.Column(db.Integer,db.ForeignKey('users.id'))
    
class Tag(Base):
    __tablename__='tags'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String)
    
class Comment(Base):
    __tablename__='comments'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    content = db.Column(db.String)
    date = db.Column(db.DateTime)
    documentid = db.Column(db.Integer,db.ForeignKey('documents.id'))
    userid = db.Column(db.Integer,db.ForeignKey('users.id'))
    
    
class UserCourses(Base):
    __tablename__='usercourses'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    userid=db.Column(db.Integer,db.ForeignKey('users.id'))
    courseid=db.Column(db.Integer,db.ForeignKey('courses.id'))
    
class Docutags(Base):
    __tablename__='docutags'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    documentid = db.Column(db.Integer,db.ForeignKey('documents.id'))
    tagid = db.Column(db.Integer,db.ForeignKey('tags.id'))
    
    
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)