'''Main rest api module'''
import logging
import os
from flask import Flask
from flask_restful import Api
from dep_app.service.service import DepartmentManagement, EmployeeManagement, AverageSalary, Search
from dep_app import db
from dep_app.config import RestConfig


console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
filehandler = logging.FileHandler((os.path.abspath('rest_log.log')))
filehandler.setLevel(logging.DEBUG)
logging.basicConfig(handlers=[console, filehandler])

app = Flask(__name__)
app.config.from_object(RestConfig)
db.init_app(app)
api = Api(app)

api.add_resource(EmployeeManagement, '/employee/<id>', '/employee')
api.add_resource(DepartmentManagement, '/department/by_id/<id>', '/department/by_title/<title>', '/department')
api.add_resource(AverageSalary, '/salary/average')
api.add_resource(Search, '/search/<dep_id>/<fr>/<to>', '/search/<dep_id>/<dob>')
