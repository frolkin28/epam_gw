'''Basic configuration for web-application'''


class ApplicationConfig:
	DEBUG = True
	SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:012810@localhost/app'
	SQLALCHEMY_TRACK_MODIFICATIONS = True
	SECRET_KEY = '86e3e066e3beebefb70d33de9343e1af'


class RestConfig:
	DEBUG = True
	SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:012810@localhost/app'
	SQLALCHEMY_TRACK_MODIFICATIONS = True
	SERVER_NAME = '127.0.0.1:8000'
