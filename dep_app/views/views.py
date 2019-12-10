from dep_app import app, db
from flask import render_template, request
from dep_app.models.models import Departments, Employees
from sqlalchemy.sql import func
from datetime import datetime
import re
from sqlalchemy import and_


@app.route('/', methods=['GET', 'POST'])
@app.route('/departments', methods=['GET', 'POST'])
def departments():
	if request.method == 'GET':
		dep = Departments.query.all()
		salary = dict()
		for i in dep:
			average = db.session.query(func.avg(Employees.salary)).filter(Employees.dep_id == i.id).first()
			if average[0]:
				salary[i.id] = average[0]
	return render_template('departments.html', departments=dep, avg_salary=salary)


@app.route('/employees', methods=['GET', 'POST'])
def employees():
	if request.method == 'GET':
		employees = Employees.query.all()
	return render_template('employees.html', employees=employees)


@app.route('/department/<id>', methods=['GET', 'POST'])
def department(id):
	pattern1 = re.compile(r'\b\d{4}-\d{2}-\d{2}\b')
	pattern2 = re.compile(r'\b\d{4}-\d{2}-\d{2}:\d{4}-\d{2}-\d{2}\b')
	department = Departments.query.filter(Departments.id == id).first()
	employees = department.employs
	if request.method == 'POST':
		date = request.form.get('date', '')
		if re.search(pattern2, date):
			dates = date.split(':')
			for i in range(len(dates)):
				dates[i] = datetime.strptime(dates[i], '%Y-%m-%d').date	()
			employees = Employees.query.filter(Employees.dep_id == id).filter(and_(Employees.dob < dates[1], Employees.dob > dates[0])).all()
		elif re.search(pattern1, date):
			date = datetime.strptime(date, '%Y-%m-%d').date()
			employees = Employees.query.filter(Employees.dep_id == id).filter(Employees.dob == date).all()
	return render_template('department.html', department=department, employees=employees)


@app.route('/employee/<id>', methods=['GET', 'POST'])
def employee(id):
	if request.method == 'GET':
		employee = Employees.query.filter(Employees.id == id).first()
	return render_template('employee.html', employee=employee)


@app.route('/departments/add')
def add():
	return render_template('add.html')
