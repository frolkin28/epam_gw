'''Module docstring'''
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dep_app.config import ApplicationConfig

app = Flask(__name__)
app.config.from_object(ApplicationConfig)
db = SQLAlchemy()
db.init_app(app)

from dep_app.views import views
