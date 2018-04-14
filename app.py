#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Flask,redirect,session,url_for,abort
from flask import Flask, flash,render_template, request
import os
from sqlalchemy import create_engine
from flask_sqlalchemy import SQLAlchemy
from models import *


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
engine = create_engine('sqlite:///user.db', echo=True)

app.config['SECRET_KEY'] = 'my precious'

db = SQLAlchemy(app)

@app.route('/')
def main():
    return render_template('index.html')

#Login...........................................................................................................................

#Admin Signup

@app.route('/showSignUp', methods=['POST', 'GET'])
def showSignUp():
    
    if request.method == 'POST':
        user = User(request.form['inputName'], request.form['inputEmail'], request.form['inputPassword'])
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('main'))

    if request.method == 'GET':
        return render_template('signup.html')


#Admin SignIn

@app.route('/showSignIn',methods=['POST','GET'])
def showSignIn():
    if request.method == 'POST':
        user = User.query.filter_by(name=request.form['inputName']).first()
    
        if request.form['inputPassword']== user.password :
            session['inputName'] = request.form['inputName']
            flash('You were successfully logged in')
            return redirect(url_for('showDepartments'))
        else:
            flash('You were not successfully logged in')
            return render_template('error.html')
    return render_template('signin.html')

@app.route('/AdminForgotPassword',methods=['POST','GET'])
def AdminForgotPassword():
    if request.method == 'POST':
        user = User.query.filter_by(name=request.form['inputName']).first()
        if request.form['inputEmail']== user.email :
            adminpass = user.password
            return render_template('showadminpassword.html',adminpass=adminpass)
            
    if request.method == 'GET':
        return render_template('adminforgotpassword.html')
    



#Student SignUp

@app.route('/showSignUp1', methods=['POST', 'GET'])
def showSignUp1():
    if request.method == 'POST':
        student = Student(request.form['inputID'],request.form['inputName'], request.form['inputEmail'], request.form['inputPassword'], request.form['inputAddress'], request.form['inputPhone1'],request.form['inputPhone2'])
        db.session.add(student)
        db.session.commit()
        return redirect(url_for('main'))

    if request.method == 'GET':
        return render_template('signup1.html')


#Student SignIn

@app.route('/showSignIn1',methods=['POST','GET'])
def showSignIn1():
    if request.method == 'POST':
        student = Student.query.filter_by(ID=request.form['inputID']).first()
    
        if request.form['inputPassword']== student.password :
            session['inputID'] = request.form['inputID']
            return redirect(url_for('showStudentDetails'))
        else:
            return render_template('error1.html')
            student = not_found_error
    return render_template('signin1.html')

@app.route('/StudentForgotPassword',methods=['POST','GET'])
def StudentForgotPassword():
    if request.method == 'POST':
        student = Student.query.filter_by(ID=request.form['inputID']).first()
        if request.form['inputEmail']== student.email :
            studentpass = student.password
            return render_template('showstudentpassword.html',studentpass=studentpass)
            
    if request.method == 'GET':
        return render_template('studentforgotpassword.html')

#............................................................................................................................


#Departments.................................................................................................................


#Show All Departments

@app.route('/showDepartments',methods=['POST','GET'])
def showDepartments():
    if request.method == 'GET' and session['inputName']:
        depart = Department.query.all() 
        return render_template('department.html', depart=depart, sessionid=session['inputName'])


#Add Departments
    
@app.route('/editDepartments',methods=['POST','GET'])
def editDepartments():
    
    if request.method == 'POST':
        department = Department(request.form['inputDepartmentID'], request.form['inputDepartmentName'])
        db.session.add(department)
        db.session.commit() 
        return redirect(url_for('showDepartments'))


    if request.method == 'GET' and session['inputName']:    
        return render_template('department1.html')


#Change Details of Departments

@app.route('/changeDepartments',methods=['POST','GET'])
def changeDepartments():
    if request.method == 'POST':
        changedepart = Department.query.filter_by(departmentID=request.form['inputDepartmentID']).first()
        changedepart.departmentName = request.form['inputDepartmentName']
        db.engine.execute("UPDATE Departments SET departmentName = '"+request.form['inputDepartmentName']+"' WHERE departmentID='"+request.form['inputDepartmentID']+"'")
        db.session.commit() 
        return redirect(url_for('showDepartments'))

    if request.method == 'GET' and session['inputName']:    
        return render_template('department2.html')


#Delete Departments

@app.route('/deleteDepartments',methods=['POST','GET'])
def deleteDepartments():
    if request.method == 'POST':
        deletedepart = Department.query.filter_by(departmentID=request.form['inputDepartmentID']).delete()
        db.session.commit()
        return redirect(url_for('showDepartments'))

    if request.method == 'GET' and session['inputName']:    
        return render_template('department3.html')

#.................................................................................................


#Courses..........................................................................................

#Show All The Courses

@app.route('/showAllCourses',methods=['POST','GET'])
def showAllCourses():
    if request.method == 'GET' and session['inputName']:
        cours = Course.query.all()
        return render_template('course.html', cours=cours)

#Show the Courses in that particular Department

@app.route('/showCourses',methods=['POST','GET'])
def showCourses():
    if request.method == 'GET' and session['inputName']:
        rof = request.args.get('department')
        cours = Course.query.filter_by(department=rof)
        return render_template('course.html', cours=cours,rof=rof)

#Add the courses in that particular Department

@app.route('/editCourses',methods=['POST','GET'])
def editCourses():
    if request.method == 'POST':
        course = Course(request.form['inputCourseID'], request.form['inputCourseName'], request.form['inputCredits'], request.form['inputDepartment'])
        db.session.add(course)
        db.session.commit() 
        return redirect(url_for('showCourses',department=request.form['inputDepartment']))

    if request.method == 'GET' and session['inputName']:    
        return render_template('course1.html')

#Change the Course Details in that Particular Department

@app.route('/changeCourses',methods=['POST','GET'])
def changeCourses():
    if request.method == 'POST':
        changecours = Course.query.filter_by(courseID=request.form['inputCourseID']).first()
        changecours.courseName = request.form['inputCourseName']
        db.engine.execute("UPDATE Courses SET courseName = '"+request.form['inputCourseName']+"' WHERE courseID='"+request.form['inputCourseID']+"'")
        changecours.credits = request.form['inputCredits']
        db.engine.execute("UPDATE Courses SET credits = '"+request.form['inputCredits']+"' WHERE courseID='"+request.form['inputCourseID']+"'")
        changecours.department = request.form['inputDepartment']
        db.engine.execute("UPDATE Courses SET department = '"+request.form['inputDepartment']+"' WHERE courseID='"+request.form['inputCourseID']+"'")
        db.session.commit() 
        return redirect(url_for('showCourses',department=request.form['inputDepartment']))

    if request.method == 'GET' and session['inputName']:    
        return render_template('course2.html')



# @app.route('/changeCourses',methods=['POST','GET'])
# def changeCourses():
#     if request.method == 'POST':
#         department=request.form['inputDepartment']
#         print(department)
#         changecours = Course.query.filter_by(courseID=request.form['inputCourseID'])
#         changecours.courseName = request.form['inputCourseName']
#         db.engine.execute("UPDATE Courses SET courseName = '"+request.form['inputcourseName']+"' WHERE courseID='"+request.form['inputCourseID']+"'")
#         changecours.credits = request.form['inputCredits']
#         db.engine.execute("UPDATE Courses SET credits = '"+request.form['inputCredits']+"' WHERE courseID='"+request.form['inputCourseID']+"'")
#         changecours.department = request.form['inputDepartment']
#         db.engine.execute("UPDATE Courses SET department = '"+request.form['inputDepartment']+"' WHERE courseID='"+request.form['inputCourseID']+"'")
#         department=request.form['inputDepartment']
#         print(department)
#         print(request.form['inputDepartment'])
#         db.session.commit() 
#         return redirect(url_for('showCourses',department='department'))

#     if request.method == 'GET' and session['inputName']:    
#         return render_template('course2.html')

#Delete courses in that Particular Department

@app.route('/deleteCourses',methods=['POST','GET'])
def deleteCourses():
    if request.method == 'POST':
        deletecours = Course.query.filter_by(courseID=request.form['inputCourseID']).delete()
        db.session.commit()
        return redirect(url_for('showCourses',department=request.form['inputDepartment']))

    if request.method == 'GET' and session['inputName']:    
        return render_template('course3.html')

#..........................................................................................................


#StudentCourse............................................................................................

#Show All the Courses & the Students in it

@app.route('/showAllStudentCourses',methods=['POST','GET'])
def showAllStudentCourses():
    if request.method == 'GET' and session['inputName']:
        studcours = StudentCourse.query.all()
        return render_template('studentcourse.html', studcours=studcours)

#Show the the students in that particular Course

@app.route('/showStudentCourses',methods=['POST','GET'])
def showStudentCourses():
    if request.method == 'GET' and session['inputName']:
        rop = request.args.get('courseID')
        studcours = StudentCourse.query.filter_by(courseID=rop)
        return render_template('studentcourse.html', studcours=studcours)

#Add the students in that particular Course

@app.route('/editStudentCourses',methods=['POST','GET'])
def editStudentCourses():
    if request.method == 'POST':
        studentcourse = StudentCourse(request.form['inputCourseID'],request.form['inputStudentID'],request.form['inputMarks'], request.form['inputAttendance'], request.form['inputStatus'])
        db.session.add(studentcourse)
        db.session.commit() 
        return redirect(url_for('showStudentCourses',courseID=request.form['inputCourseID']))

    if request.method == 'GET' and session['inputName']:    
        return render_template('studentcourse1.html')

#Change the details of Students enrolled in that Particular Course or Change the Details of Course of that Particular Student

@app.route('/changeStudentCourses',methods=['POST','GET'])
def changeStudentCourses():
    if request.method == 'POST':
        changestudcours = StudentCourse.query.filter_by(courseID=request.form['inputCourseID'])
        changestudcours.studentID = request.form['inputStudentID']

        changestudcours.marks = request.form['inputMarks']
        db.engine.execute("UPDATE studentCourses SET marks = '"+request.form['inputMarks']+"' WHERE courseID='"+request.form['inputCourseID']+"' AND studentID = '"+request.form['inputStudentID']+"' ")
        changestudcours.attendance = request.form['inputAttendance']
        db.engine.execute("UPDATE studentCourses SET attendance = '"+request.form['inputAttendance']+"' where courseID='"+request.form['inputCourseID']+"' AND studentID = '"+request.form['inputStudentID']+"'")
        changestudcours.status = request.form['inputStatus']
        db.engine.execute("UPDATE studentCourses SET status = '"+request.form['inputStatus']+"' where courseID='"+request.form['inputCourseID']+"' AND studentID = '"+request.form['inputStudentID']+"'")
        db.session.commit() 
        return redirect(url_for('showStudentCourses',courseID=request.form['inputCourseID']))

    if request.method == 'GET' and session['inputName']:    
        return render_template('studentcourse2.html')

#Delete that Student enrolled in that Particular Course

@app.route('/deleteStudentCourses',methods=['POST','GET'])
def deleteStudentCourses():
    if request.method == 'POST':
        deletestudcours = StudentCourse.query.filter_by(studentID=request.form['inputStudentID']).delete()
        db.session.commit()
        return redirect(url_for('showStudentCourses',courseID=request.form['inputCourseID']))

    if request.method == 'GET' and session['inputName']:    
        return render_template('studentcourse3.html')
#.............................................................................................................................



#StudentDetails...............................................................................................................


#When the Student is logged in show his details like marks in each course, Address & Phone Number

@app.route('/showStudentDetails',methods=['POST','GET'])
def showStudentDetails():
    if request.method == 'GET' and session['inputID']:
        sessionlol=session['inputID']
        stud = Student.query.all()
        studdet = db.engine.execute("SELECT * from studentCourses where studentID='"+session['inputID']+"'")
        courses = db.engine.execute("SELECT * from studentCourses where studentID='"+session['inputID']+"'")
        #courses = StudentCourse.query.filter_by(studentID=session['inputID']).first()
        cgpa = 0.0
        sum = 0.0
        tot = 0.0
        for item in courses:
           # actualCourse = db.engine.execute("SELECT * from Courses where courseID = item['courseID']")
            print("SELECT * from Courses where courseID = course.courseID")
            actualcourse = Course.query.filter_by(courseID=item['courseID']).first()
            a = actualcourse.credits
            if item.attendance >= 75 and item.status == 1 :
                m = int(item.marks/10) + 1
            else :
                m = 0.0
                a = 0.0
            sum += a*m
            tot += a
        cgpa = sum/tot

        return render_template('studentdetails.html', studdet=studdet,sessionlol=session['inputID'], stud=stud,cgpa=cgpa)


#Change Address or Phone Number of the Student

@app.route('/changeStudentDetails',methods=['POST','GET'])
def changeStudentDetails():
    if request.method == 'POST':
        changestuddet = Student.query.filter_by(ID=request.form['inputID']).first()
        changestuddet.address = request.form['inputAddress']
        changestuddet.phone1 = request.form['inputPhone1']
        changestuddet.phone2 = request.form['inputPhone2']
        db.session.commit() 
        return redirect(url_for('showStudentDetails'))

    if request.method == 'GET' and session['inputID']:    
        return render_template('studentdetails2.html')

#...............................................................................................................................





#AdminLogout....................................................................................................................

@app.route('/logout',methods=['POST','GET'])
def logout():
    session.pop('inputName')
    return redirect(url_for('main'))

#................................................................................................................................


#StudentLogout....................................................................................................................

@app.route('/studentLogout',methods=['POST','GET'])
def studentLogout():
    session.pop('inputID')
    return redirect(url_for('main'))

#..................................................................................................................................


#LogoutOfAllSessions................................................................................................................

@app.route('/logoutAll',methods=['POST','GET'])
def logoutAll():
    session.clear()
    return redirect(url_for('main'))

#......................................................................................................................................



if __name__ == '__main__':
    app.run(debug=True)
