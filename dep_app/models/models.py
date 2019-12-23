'''Database models module'''
from dep_app import db


class Departments(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(140), nullable=False)
	employs = db.relationship('Employees', backref='department', lazy=True)

	def __repr__(self):
		return 'Department(title: {} id: {})'.format(self.title, self.id)


class Employees(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(140), nullable=False)
	dob = db.Column(db.Date, nullable=False)
	salary = db.Column(db.Float)
	dep_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=False)

	def __repr__(self):
		return 'Employee(name: {} id: {})'.format(self.name, self.id)
