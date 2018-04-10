#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Flask,redirect,session,url_for,abort
from flask import Flask, render_template, request
#from db_setup import init_db
#from database import db_session
import os
from flask_sqlalchemy import SQLAlchemy
from models import *


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'

app.config['SECRET_KEY'] = 'my precious'

db = SQLAlchemy(app)

@app.route('/')
def main():
    return render_template('index.html')


@app.route('/showSignUp', methods=['POST', 'GET'])
def showSignUp():
    
    if request.method == 'POST':
        user = User(request.form['inputName'], request.form['inputEmail'], request.form['inputPassword'])
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('main'))

    if request.method == 'GET':
        return render_template('signup.html')


@app.route('/showSignIn',methods=['POST','GET'])
def showSignIn():
    if request.method == 'POST':
        user = User.query.filter_by(name=request.form['inputName']).first()
    
        if request.form['inputPassword']== user.password :
            session['inputName'] = request.form['inputName']
            return redirect(url_for('showDepartments'))
        else:
            user = not_found_error
    return render_template('signin.html')


@app.route('/showTables')
def showTables():
    return render_template('table.html')


@app.route('/showSignUp1', methods=['POST', 'GET'])
def showSignUp1():
    if request.method == 'POST':
        student = Student(request.form['inputID'],request.form['inputName'], request.form['inputEmail'], request.form['inputPassword'], request.form['inputAddress'], request.form['inputPhone'])
        db.session.add(student)
        db.session.commit()
        return redirect(url_for('main'))

    if request.method == 'GET':
        return render_template('signup1.html')


@app.route('/showSignIn1',methods=['POST','GET'])
def showSignIn1():
    if request.method == 'POST':
        student = Student.query.filter_by(ID=request.form['inputID']).first()
    
        if request.form['inputPassword']== student.password :
            session['inputID'] = request.form['inputID']
            return redirect(url_for('showStudentDetails'))
        else:
            student = not_found_error
    return render_template('signin1.html')


@app.route('/showTables1')
def showTables1():
    return render_template('table.html')

@app.route('/showStudents', methods=['GET', 'POST'])
def showStudents():
    stud = Student.query.all()
    return render_template('student.html', stud=stud)


#Departments

@app.route('/showDepartments',methods=['POST','GET'])
def showDepartments():
    if request.method == 'GET' and session['inputName']:
        depart = Department.query.all() 
        return render_template('department.html', depart=depart, sessionid=session['inputName'])
    
@app.route('/editDepartments',methods=['POST','GET'])
def editDepartments():
    
    if request.method == 'POST':
        department = Department(request.form['inputDepartmentID'], request.form['inputDepartmentName'])
        db.session.add(department)
        db.session.commit() 
        return redirect(url_for('showDepartments'))


    if request.method == 'GET' and session['inputName']:    
        return render_template('department1.html')

@app.route('/changeDepartments',methods=['POST','GET'])
def changeDepartments():
    if request.method == 'POST':
        changedepart = Department.query.filter_by(departmentID=request.form['inputDepartmentID']).first()
        changedepart.departmentName = request.form['inputDepartmentName']
        db.session.commit() 
        return redirect(url_for('showDepartments'))

    if request.method == 'GET' and session['inputName']:    
        return render_template('department2.html')

@app.route('/deleteDepartments',methods=['POST','GET'])
def deleteDepartments():
    if request.method == 'POST':
        deletedepart = Department.query.filter_by(departmentID=request.form['inputDepartmentID']).delete()
        db.session.commit()
        return redirect(url_for('showDepartments'))

    if request.method == 'GET' and session['inputName']:    
        return render_template('department3.html')

#Courses

@app.route('/Search',methods=['POST','GET'])
def Search():

    if request.method=='POST' and session['inputName']:
        cours = Course.query.filter_by(courseID=request.form['inputCourseID'])
        result = db.engine.execute(cours)
        print('1111')
        print(cours)
        print('2222')
        for row in result:
            print("username:", row['courseID'])
        return render_template('course.html',cours=cours)
    return render_template('course.html')


@app.route('/showAllCourses',methods=['POST','GET'])
def showAllCourses():
    if request.method == 'GET' and session['inputName']:
        cours = Course.query.all()
        return render_template('course.html', cours=cours)


@app.route('/showCourses',methods=['POST','GET'])
def showCourses():
    if request.method == 'GET' and session['inputName']:
        rof = request.args.get('department')
        cours = Course.query.filter_by(department=rof)
        return render_template('course.html', cours=cours,rof=rof)

@app.route('/editCourses',methods=['POST','GET'])
def editCourses():
    if request.method == 'POST':
        course = Course(request.form['inputCourseID'], request.form['inputCourseName'], request.form['inputCredits'], request.form['inputDepartment'])
        db.session.add(course)
        db.session.commit() 
        return redirect(url_for('showAllCourses'))

    if request.method == 'GET' and session['inputName']:    
        return render_template('course1.html')


@app.route('/changeCourses',methods=['POST','GET'])
def changeCourses():
    if request.method == 'POST':
        changecours = Course.query.filter_by(courseID=request.form['inputCourseID']).first()
        changecours.courseName = request.form['inputCourseName']
        changecours.credits = request.form['inputCredits']
        changecours.department = request.form['inputDepartment']
        db.session.commit() 
        return redirect(url_for('showAllCourses'))

    if request.method == 'GET' and session['inputName']:    
        return render_template('course2.html')

@app.route('/deleteCourses',methods=['POST','GET'])
def deleteCourses():
    if request.method == 'POST':
        deletecours = Course.query.filter_by(courseID=request.form['inputCourseID']).delete()
        db.session.commit()
        return redirect(url_for('showAllCourses'))

    if request.method == 'GET' and session['inputName']:    
        return render_template('course3.html')
#obj = user.query.filter_by(courseID=courseID).first()
#obj.courseName =  request.form['inputCourseName']


#StudentCourse

@app.route('/showAllStudentCourses',methods=['POST','GET'])
def showAllStudentCourses():
    if request.method == 'GET' and session['inputName']:
        studcours = StudentCourse.query.all()
        return render_template('studentcourse.html', studcours=studcours)

@app.route('/showStudentCourses',methods=['POST','GET'])
def showStudentCourses():
    if request.method == 'GET' and session['inputName']:
        rop = request.args.get('courseID')
        studcours = StudentCourse.query.filter_by(courseID=rop)
        return render_template('studentcourse.html', studcours=studcours)

@app.route('/editStudentCourses',methods=['POST','GET'])
def editStudentCourses():
    if request.method == 'POST':
        studentcourse = StudentCourse(request.form['inputCourseID'],request.form['inputCourseName'],request.form['inputStudentID'],request.form['inputStudentName'],request.form['inputMarks'], request.form['inputAttendance'])
        db.session.add(studentcourse)
        db.session.commit() 
        return redirect(url_for('showAllStudentCourses'))

    if request.method == 'GET' and session['inputName']:    
        return render_template('studentcourse1.html')

@app.route('/changeStudentCourses',methods=['POST','GET'])
def changeStudentCourses():
    if request.method == 'POST':
        changestudcours = StudentCourse.query.filter_by(courseID=request.form['inputCourseID']).first()
        changestudcours.courseName = request.form['inputCourseName']
        changestudcours.studentID = request.form['inputStudentID']
        changestudcours.studentName = request.form['inputStudentName']
        changestudcours.marks = request.form['inputMarks']
        changestudcours.attendance = request.form['inputAttendance']
        db.session.commit() 
        return redirect(url_for('showAllStudentCourses'))

    if request.method == 'GET' and session['inputName']:    
        return render_template('studentcourse2.html')

@app.route('/deleteStudentCourses',methods=['POST','GET'])
def deleteStudentCourses():
    if request.method == 'POST':
        deletestudcours = StudentCourse.query.filter_by(courseID=request.form['inputCourseID']).delete()
        db.session.commit()
        return redirect(url_for('showAllStudentCourses'))

    if request.method == 'GET' and session['inputName']:    
        return render_template('studentcourse3.html')


@app.route('/showStudentDetails',methods=['POST','GET'])
def showStudentDetails():
    if request.method == 'GET' and session['inputID']:
        sessionlol=session['inputID']
        studdet = StudentCourse.query.filter_by(studentID=session['inputID']).first()
        studdet = db.engine.execute("SELECT * from StudentCourses") 
        return render_template('studentdetails.html', studdet=studdet,sessionlol=session['inputID'])



@app.route('/logout',methods=['POST','GET'])
def logout():
    session.pop('inputName')
    return redirect(url_for('main'))

@app.route('/studentLogout',methods=['POST','GET'])
def studentLogout():
    session.pop('inputID')
    return redirect(url_for('main'))

@app.route('/logoutAll',methods=['POST','GET'])
def logoutAll():
    session.clear()
    return redirect(url_for('main'))


    
#@app.teardown_appcontext
#def shutdown_session(exception=None):
 #   db_session.remove()

if __name__ == '__main__':
    app.run(debug=True)
