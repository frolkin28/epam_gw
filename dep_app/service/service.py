from flask_restful import Resource, reqparse
from dep_app.models.models import Departments, Employees
from .schemas import DepartmentsSchema, EmployeesSchema
from dep_app import db
from sqlalchemy.sql import func
from sqlalchemy import and_

parser1 = reqparse.RequestParser()
parser1.add_argument('id')
parser1.add_argument('title')


class AverageSalary(Resource):
	def get(self):
		dep = Departments.query.all()
		salary = dict()
		for i in dep:
			average = Employees.query.with_entities(func.avg(Employees.salary)).filter(
				(Employees.dep_id == i.id)).first()
			if average[0]:
				salary[i.id] = average[0]
		return salary, 200


class DepartmentManagement(Resource):
	def get(self, id=None, title=None):
		if id:
			department = Departments.query.get(id)
			department_schema = DepartmentsSchema()
		elif title:
			department = Departments.query.filter(Departments.title == title).first()
			department_schema = DepartmentsSchema()
		else:
			department = Departments.query.all()
			department_schema = DepartmentsSchema(many=True)
		res = department_schema.dump(department)
		return res, 200

	def post(self):
		args = parser1.parse_args()
		department_schema = DepartmentsSchema()
		department = Departments(title=args['title'])
		db.session.add(department)
		db.session.commit()
		res = department_schema.dump(department)
		return res, 201

	def put(self):
		args = parser1.parse_args()
		department_schema = DepartmentsSchema()
		department = Departments.query.get(args['id'])
		department.title = args['title']
		db.session.add(department)
		db.session.commit()
		res = department_schema.dump(department)
		return res, 200

	def delete(self, id):
		department_schema = DepartmentsSchema()
		employees = Employees.query.filter(Employees.dep_id == id).all()
		for employee in employees:
			db.session.delete(employee)
			db.session.commit()
		department = Departments.query.get(id)
		res = department_schema.dump(department)
		db.session.delete(department)
		db.session.commit()
		return res, 200


parser2 = reqparse.RequestParser()
parser2.add_argument('id')
parser2.add_argument('name')
parser2.add_argument('dob')
parser2.add_argument('salary')
parser2.add_argument('dep_id')


class EmployeeManagement(Resource):
	def get(self, id=None):
		if id:
			employee = Employees.query.get(id)
			employee_schema = EmployeesSchema()
		else:
			employee = Employees.query.all()
			employee_schema = EmployeesSchema(many=True)
		res = employee_schema.dump(employee)
		return res, 200

	def post(self):
		args = parser2.parse_args()
		employee_schema = EmployeesSchema()
		employee = Employees(name=args['name'], dob=args['dob'], salary=args['salary'], dep_id=args['dep_id'])
		db.session.add(employee)
		db.session.commit()
		res = employee_schema.dump(employee)
		return res, 201

	def put(self):
		args = parser2.parse_args()
		employee = Employees.query.get(args['id'])
		employee.name = args['name']
		employee.dob = args['dob']
		employee.salary = args['salary']
		employee.dep_id = args['dep_id']
		db.session.add(employee)
		db.session.commit()
		employee_schema = EmployeesSchema()
		res = employee_schema.dump(employee)
		return res, 200

	def delete(self, id):
		employee = Employees.query.get(id)
		employee_schema = EmployeesSchema()
		res = employee_schema.dump(employee)
		db.session.delete(employee)
		db.session.commit()
		return res, 200


class Search(Resource):
	def get(self, dep_id=None, fr=None, to=None, dob=None):
		if fr and to:
			employees = Employees.query.filter(Employees.dep_id == dep_id).filter(
				and_(Employees.dob < to, Employees.dob > fr)).all()
		elif dob:
			employees = Employees.query.filter(Employees.dep_id == dep_id).filter(Employees.dob == dob).all()
		employee_schema = EmployeesSchema(many=True)
		res = employee_schema.dump(employees)
		return res, 200
