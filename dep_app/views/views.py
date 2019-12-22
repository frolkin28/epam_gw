from datetime import datetime
import re
import requests
from flask import render_template, request, redirect, url_for
from dep_app.forms import DepartmentForm, EmployeeForm, EditEmployeeForm
from dep_app.service.service import EmployeesSchema, DepartmentsSchema
from dep_app import app

url = 'http://0.0.0.0:8000'


@app.route('/', methods=['GET', 'POST'])
@app.route('/departments', methods=['GET', 'POST'])
def departments():
	'''View function which returns template with all departments'''

	r = requests.get(url + '/department')
	data = r.json()
	schema = DepartmentsSchema(many=True)
	dep = schema.load(data)
	r = requests.get(url + '/salary/average')
	response = r.json()
	salary = dict()
	for i in response.keys():
		salary[int(i)] = response[i]
	return render_template('departments.html', departments=dep, avg_salary=salary)


@app.route('/employees', methods=['GET', 'POST'])
def employees():
	'''View function which returns template with employees table'''

	r = requests.get(url + '/employee')
	data = r.json()
	schema = EmployeesSchema(many=True)
	employees = schema.load(data)
	return render_template('employees.html', employees=employees)


@app.route('/department/<id>', methods=['GET', 'POST'])
def department(id):
	'''View function which returns template with search field and a list of employees in special department.
	Also provides ability for deletion and edition'''

	pattern1 = re.compile(r'\b\d{4}-\d{2}-\d{2}\b')
	pattern2 = re.compile(r'\b\d{4}-\d{2}-\d{2}:\d{4}-\d{2}-\d{2}\b')

	r = requests.get(url + '/department/by_id/{}'.format(id))
	data = r.json()
	schema = DepartmentsSchema()
	department = schema.load(data)
	employees = department.employs

	if request.method == 'POST':
		date = request.form.get('date', '')
		if re.search(pattern2, date):
			dates = date.split(':')
			for i in range(len(dates)):
				dates[i] = datetime.strptime(dates[i], '%Y-%m-%d').date()
			r = requests.get(url + '/search/{}/{}/{}'.format(id, dates[0], dates[1]))
			data = r.json()
			schema = EmployeesSchema(many=True)
			employees = schema.load(data)
		elif re.search(pattern1, date):
			date = datetime.strptime(date, '%Y-%m-%d').date()
			r = requests.get(url + '/search/{}/{}'.format(id, date))
			data = r.json()
			schema = EmployeesSchema(many=True)
			employees = schema.load(data)
	return render_template('department.html', department=department, employees=employees)


@app.route('/employee/<id>', methods=['GET', 'POST'])
def employee(id):
	'''View function which returns template with all information about employee with a special id.
	Provides functionality to edit and delete'''

	r = requests.get(url + '/employee/{}'.format(id))
	data = r.json()
	schema = EmployeesSchema()
	employee = schema.load(data)
	return render_template('employee.html', employee=employee)


@app.route('/departments/add', methods=['GET', 'POST'])
def add_department():
	'''View function which returns template with form to add new department (also use validation)'''
	form = DepartmentForm()
	if form.validate_on_submit():
		requests.post(url + '/department', data={'title': form.title.data})
		return redirect(url_for('departments'))
	return render_template('add_department.html', form=form)


@app.route('/employee/add/<dep_id>', methods=['GET', 'POST'])
def add_employee(dep_id):
	'''View function which returns template with form to add new employee (also use validation)'''

	form = EmployeeForm()
	if form.validate_on_submit():
		data = {'name': form.name.data, 'dob': form.dob.data, 'salary': form.salary.data, 'dep_id': dep_id}
		requests.post(url + '/employee', data=data)
		return redirect(url_for('department', id=dep_id))
	return render_template('add_employee.html', form=form, title='Add department')


@app.route('/employee/delete/<id>')
def employee_delete(id):
	'''View function which handles delete requests and make delete request for api'''

	requests.delete(url + '/employee/{}'.format(id))
	return redirect(url_for('employees'))


@app.route('/department/delete/<id>')
def department_delete(id):
	'''View function which handles delete requests and make delete request for api'''

	requests.delete(url + '/department/by_id/{}'.format(id))
	return redirect(url_for('departments'))


@app.route('/department/edit/<id>', methods=['GET', 'POST'])
def edit_department(id):
	'''View function which returns template with form to edit existing department (also use validation)'''

	form = DepartmentForm()
	r = requests.get(url + '/department/by_id/{}'.format(id))
	data = r.json()
	schema = DepartmentsSchema()
	department = schema.load(data)
	if form.validate_on_submit():
		if form.title.data == department.title:
			return redirect(url_for('department', id=department.id))
		r = requests.get(url + '/department/by_title/{}'.format(form.title.data))
		data = r.json()
		if data:
			return redirect(url_for('edit_department', id=id))
		requests.put(url + '/department', data={'title': form.title.data, 'id': id})
		return redirect(url_for('departments'))
	return render_template('edit_department.html', form=form, title='edit department', department=department)


@app.route('/employee/edit/<id>', methods=['GET', 'POST'])
def edit_employee(id):
	'''View function which returns template with form to edit existing employee (also use validation)'''

	form = EditEmployeeForm()
	r = requests.get(url + '/employee/{}'.format(id))
	data = r.json()
	schema = EmployeesSchema()
	employee = schema.load(data)
	if form.validate_on_submit():
		r = requests.get(url + '/department/by_title/{}'.format(form.department.data))
		data = r.json()
		if data:
			data_to_put = {'id': id, 'name': form.name.data, 'dob': form.dob.data, 'salary': form.salary.data,
						   'dep_id': data['id']}
			requests.put(url + '/employee', data=data_to_put)
			return redirect(url_for('employees'))
		else:
			return redirect(url_for('edit_employee', id=id))
	return render_template('edit_employee.html', form=form, title='edit employee', employee=employee)
