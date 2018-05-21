web: gunicorn pokebattle.wsgi --limit-request-line 8188 --log-file -
worker: celery worker -A pokebattle -B --loglevel=info
