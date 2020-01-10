# epam_gw
Here is a project of web application and rest api, which provides tools for departments management.
Api could be deployed with gunicorn, migration script presents as well.
Here is GitHub link: https://github.com/frolkin28/epam_gw

Install this package this way:
$ git clone https://github.com/frolkin28/epam_gw.git
$ cd epam_gw
$ python setup.py install

Run api using gunicorn:
$ gunicorn -c gconfig.py wsgi:app

Run api using python scrip:
$ python wsgi.py

Run web application (run the api firstly):
$ python manage.py runserver

Run unitests:
- for api:
$ python -m unittest -v dep_app/tests/test_rest.py

- for web-application using selenium (run api and web-app firstly):
$ python -m unittest -v dep_app/tests/test_rest.py

Migration script:
$ python manage.py db init
$ python manage.py db migrate
$ python manage.py db upgrade

Rest service is avaliable on adresss http://0.0.0.0:8000. Web application is avaliable on http://127.0.0.1:5000.
