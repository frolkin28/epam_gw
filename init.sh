source ~/envs/gw/bin/activate
gunicorn -c gconfig.py wsgi:app
python3.7 manage.py runserver
