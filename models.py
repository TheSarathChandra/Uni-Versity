from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.orm import relationship
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

class Student(Base):
    __tablename__ = 'Students'
    
    ID = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(120))
    password = db.Column(db.String(50))
    address = db.Column(db.String(50))
    phone1 = db.Column(db.Integer())
    phone2 = db.Column(db.Integer())
    yos = db.Column(db.Integer())

    def __init__(self, ID, name, email,password,address,phone1,phone2,yos):
        self.ID = ID
        self.name = name
        self.email = email
        self.password = password
        self.address = address
        self.phone1 = phone1
        self.phone2 = phone2
        self.yos = yos

class Course(Base):
    __tablename__ = 'Courses'
    
    courseID = db.Column(db.String(50), primary_key=True)
    courseName = db.Column(db.String(50))
    credits = db.Column(db.Integer())
    department = db.Column(db.String(50))

    def __init__(self, courseID, courseName, credits,department):
        self.courseID = courseID
        self.courseName = courseName
        self.credits = credits
        self.department = department

class StudentCourse(Base):
    __tablename__='studentCourses'

    courseID = db.Column(db.String(50),ForeignKey('Courses.courseID'),primary_key=True,unique=False)
    studentID =  db.Column(db.String(50),ForeignKey('Students.ID'),primary_key=True,unique=False)
    marks = db.Column(db.Integer(),unique=False)
    attendance = db.Column(db.Integer(),unique=False)
    status = db.Column(db.Integer(),unique=False)
    Courses = relationship("Course")
    Students = relationship("Student")

    def __init__(self, courseID, studentID, marks,attendance,status):
        self.courseID = courseID
        self.studentID = studentID
        self.marks = marks
        self.attendance = attendance
        self.status = status


class Department(Base):
    __tablename__ = 'Departments'
    
    departmentID = db.Column(db.String(50), primary_key=True)
    departmentName = db.Column(db.String(50))

    def __init__(self, departmentID, departmentName):
        self.departmentID = departmentID
        self.departmentName = departmentName



   # def is_authenticated(self):
    #    return True

   # def __repr__(self):
    #    return '<User %r>' % (self.name)

Base.metadata.create_all(bind=engine)