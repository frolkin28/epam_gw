'''Module with forms'''
from flask_wtf import FlaskForm
from wtforms import DateField, SubmitField, StringField, FloatField
from wtforms.validators import DataRequired


class DepartmentForm(FlaskForm):
	'''Form class with validators to add and edit departments'''

	title = StringField('Title', validators=[DataRequired()])
	submit = SubmitField('Submit')


class EmployeeForm(FlaskForm):
	'''Form class with validators to add employee'''

	name = StringField('Name', validators=[DataRequired()])
	dob = DateField('Date of birth', validators=[DataRequired()])
	salary = FloatField('Salary', validators=[DataRequired()])
	submit = SubmitField('Submit')


class EditEmployeeForm(EmployeeForm):
	'''Form class with validators to edit employee, inherits EmployeeForm, but adds new field'''

	department = StringField('Department', validators=[DataRequired()])
