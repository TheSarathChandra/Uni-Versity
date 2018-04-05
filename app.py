#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Flask,redirect,session,url_for,abort
from flask import Flask, render_template, request
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
            return render_template('table.html')
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
            return render_template('table1.html')
        else:
            student = not_found_error
    return render_template('signin1.html')


@app.route('/showTables1')
def showTables1():
    return render_template('table.html')

    


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

if __name__ == '__main__':
    app.run(debug=True)
