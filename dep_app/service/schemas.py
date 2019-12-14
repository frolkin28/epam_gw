from .service import Departments, Employees
from dep_app import db
from flask_marshmallow import Marshmallow
from marshmallow import post_load

ma = Marshmallow()


class BaseSchema(ma.ModelSchema):
	class Meta:
		sqla_session = db.session


class EmployeesSchema(BaseSchema):
	class Meta(BaseSchema.Meta):
		model = Employees

		@post_load
		def make_employee(self, data, **kwargs):
			return Employees(**data)


class DepartmentsSchema(BaseSchema):
	employs = ma.Nested(EmployeesSchema, many=True)

	class Meta(BaseSchema.Meta):
		model = Departments

		@post_load
		def make_department(self, data, **kwargs):
			return Departments(**data)
