from flask import Flask, render_template, request, redirect, url_for, flash, session
import pygal
from flask_sqlalchemy import SQLAlchemy
from flask.ext.bcrypt import Bcrypt

DB_URL = 'postgresql://postgres:root@127.0.0.1:5433/projectManagement'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'some-secret-string'

db = SQLAlchemy(app)
from models import ProjectModel
from userModel import UserModel

@app.before_first_request
def createTables():
    db.create_all()

@app.route('/authentication', methods=['GET'])
def authentication():
    return render_template('authentication.html')

@app.route('/register', methods=['POST'])
def addNewUser():
    fullName = request.form['fullName']
    email = request.form['email']
    password = request.form['password']
    confirmPassword = request.form['confirmPassword']

    # Check if password and confirm password are the same
    if password != confirmPassword:
        flash("Passwords do not match")
        return render_template('authentication.html')
    elif (UserModel.emailChecker(email)):
        flash("User with the email entered already exists")
        return render_template('authentication.html')
    else:
        # Create User
        user = UserModel(fullName=fullName, email=email, password=password)
        user.createUser()

        session['email'] = email
        flash("You have successfully Registered! Now sign in to view projects")
        return redirect(url_for('home'))

#
# @app.route('/login', methods=['POST'])
# def login():
#      # If email and password exists
#      try:
# 
#
#      return redirect(url_for('home'))

@app.route('/', methods=['GET'])
def home():
    print(session)
    if session:
        # Is logged in
        records = ProjectModel.fetchAll()
        status = [x.status for x in records]
        pie_chart = pygal.Pie()
        pie_chart._title = "completed vs pending"
        pie_chart.add("pending projects", status.count("pending"))
        pie_chart.add("completed projects", status.count("completed"))
        graph = pie_chart.render_data_uri()
        return render_template('index.html', records=records, graph=graph)
    else:
        # Is not logged in
        return render_template('authentication.html')

@app.route('/project/create',methods=['POST'])
def addNewProject():
    if request.method == "POST":
        title = request.form['title']
        description = request.form['description']
        startDate = request.form['startDate']
        endDate = request.form['endDate']
        cost = request.form['cost']
        status = request.form['status']

        project = ProjectModel(title=title, description=description, startDate=startDate, endDate=endDate, cost=cost, status=status)
        project.createRecord()

    return redirect(url_for('home'))


@app.route('/project/edit/<int:id>',methods=['POST'])
def editProject(id):
    newTitle = request.form['title']
    newDescription = request.form['description']
    newStartDate = request.form['startDate']
    newEndDate = request.form['endDate']
    newCost = request.form['cost']
    newStatus = request.form['status']

    updated = ProjectModel.updateByIdRecord(id=id, newTitle=newTitle, newDescription=newDescription, newStartDate=newStartDate, newEndDate=newEndDate, newCost=newCost, newStatus=newStatus )
    if (updated):
        flash("Updated Successfully")
        return redirect(url_for('home'))
    else:
        flash("No record found")
        return redirect(url_for('home'))


@app.route('/project/delete/<int:id>',methods=['POST'])
def deleteProject(id):
    delete = ProjectModel.deleteByIdRecord(id=id)
    if(delete):
        flash("Deleted Successfully")
        return redirect(url_for('home'))
    else:
        flash("No record found")
        return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(port = 5001, debug=True)

# Flask
# SQL-Alchemy
# ORM - Object Relational Mapper   sqlachemy
#         Connector -- psycopg2

# .venv is a package manager