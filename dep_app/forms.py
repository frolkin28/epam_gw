from flask_wtf import FlaskForm
from wtforms import DateField, SubmitField, StringField, FloatField
from wtforms.validators import DataRequired


class DepartmentForm(FlaskForm):
	title = StringField('Title', validators=[DataRequired()])
	submit = SubmitField('Add')


class EmployeeForm(FlaskForm):
	name = StringField('Name', validators=[DataRequired()])
	dob = DateField('Date of birth', validators=[DataRequired()])
	salary = FloatField('Salary', validators=[DataRequired()])
	submit = SubmitField('Add')
