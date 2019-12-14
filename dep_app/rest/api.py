from flask import Flask
from flask_restful import Api
from dep_app.service.service import DepartmentManagement, EmployeeManagement, AverageSalary, Search
from dep_app import db

app = Flask(__name__)
app.config.from_pyfile('rest_config.py')
db.init_app(app)
api = Api(app)

api.add_resource(EmployeeManagement, '/employee/<id>', '/employee')
api.add_resource(DepartmentManagement, '/department/by_id/<id>', '/department/by_title/<title>', '/department')
api.add_resource(AverageSalary, '/salary/average')
api.add_resource(Search, '/search/<dep_id>/<fr>/<to>', '/search/<dep_id>/<dob>')

if __name__ == '__main__':
	app.run(host='0.0.0.0', port='8000', debug=True)
