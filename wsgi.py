'''Scrip for running rest api with gunicorn'''
from dep_app.rest.api import app

if __name__ == '__main__':
	app.run()
