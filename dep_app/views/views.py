from dep_app import app, db
from flask import render_template, request, redirect, url_for
from dep_app.models.models import Departments, Employees
from sqlalchemy.sql import func
from sqlalchemy import and_
from datetime import datetime
import re
from dep_app.forms import DepartmentForm, EmployeeForm


@app.route('/', methods=['GET', 'POST'])
@app.route('/departments', methods=['GET', 'POST'])
def departments():
	dep = Departments.query.all()
	salary = dict()
	for i in dep:
		average = Employees.query.with_entities(func.avg(Employees.salary)).filter(
			(Employees.dep_id == i.id)).first()
		if average[0]:
			salary[i.id] = average[0]
	return render_template('departments.html', departments=dep, avg_salary=salary)


@app.route('/employees', methods=['GET', 'POST'])
def employees():
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
				dates[i] = datetime.strptime(dates[i], '%Y-%m-%d').date()
			employees = Employees.query.filter(Employees.dep_id == id).filter(
				and_(Employees.dob < dates[1], Employees.dob > dates[0])).all()
		elif re.search(pattern1, date):
			date = datetime.strptime(date, '%Y-%m-%d').date()
			employees = Employees.query.filter(Employees.dep_id == id).filter(Employees.dob == date).all()
	return render_template('department.html', department=department, employees=employees)


@app.route('/employee/<id>', methods=['GET', 'POST'])
def employee(id):
	employee = Employees.query.filter(Employees.id == id).first()
	return render_template('employee.html', employee=employee)


@app.route('/departments/add', methods=['GET', 'POST'])
def add_department():
	form = DepartmentForm()
	if form.validate_on_submit():
		department = Departments(title=form.title.data)
		db.session.add(department)
		db.session.commit()
		return redirect(url_for('departments'))
	return render_template('add_department.html', form=form)


@app.route('/employee/add/<dep_id>', methods=['GET', 'POST'])
def add_employee(dep_id):
	form = EmployeeForm()
	if form.validate_on_submit():
		employee = Employees(name=form.name.data, dob=form.dob.data, salary=form.salary.data, dep_id=dep_id)
		db.session.add(employee)
		db.session.commit()
		return redirect(url_for('department', id=dep_id))
	return render_template('add_employee.html', form=form)


@app.route('/employee/delete/<id>')
def employee_delete(id):
	employee = Employees.query.filter(Employees.id==id).first()
	db.session.delete(employee)
	db.session.commit()
	return redirect(url_for('employees'))
