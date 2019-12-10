from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_pyfile('config.py')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:012810@localhost/app'
db = SQLAlchemy(app)

from dep_app.views import views
