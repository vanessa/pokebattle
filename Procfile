web: gunicorn pokebattle.wsgi --limit-request-line 8188 --log-file -
worker: celery worker --app=pokebattle --loglevel=info
