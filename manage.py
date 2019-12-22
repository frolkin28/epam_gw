import logging
import os
from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand
from dep_app import db, app


console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
filehandler = logging.FileHandler(os.path.abspath('app_log.log'))
filehandler.setLevel(logging.DEBUG)
logging.basicConfig(handlers=[console, filehandler])

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)
manager.add_command('runserver', Server(host='127.0.0.1', port=5000))

if __name__ == '__main__':
	manager.run()
