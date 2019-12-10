from flask_wtf import FlaskForm
from wtforms import DateField, SubmitField
from wtforms.validators import DataRequired


class DateSearch(FlaskForm):
	date = DateField('Date')
	submit = SubmitField('Find')


class PeriodSearch(FlaskForm):
	start_date = DateField('Start date', validators=DataRequired)
	end_date = DateField('End date', validators=DataRequired)
	submit = SubmitField('Find')
