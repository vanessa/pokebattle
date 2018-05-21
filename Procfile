web: NEW_RELIC_CONFIG_FILE=newrelic.ini newrelic-admin run-program gunicorn pokebattle.wsgi --limit-request-line 8188 --log-file -
worker: celery worker -A pokebattle -B --loglevel=info
