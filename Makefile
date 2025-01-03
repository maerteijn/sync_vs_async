.PHONY: bootstrap install lint format locust uwsgi uwsgi-gevent gunicorn gunicorn-gevent uvicorn locust

default: bootstrap install

clean:  ## Remove all build, test, coverage and Python artifacts
	find . -name '*.pyc' -exec rm -rf {} +
	find . -name '__pycache__' -exec rm -rf {} +
	find . -name '*.egg-info' -exec rm -rf {} +
	find . -name '*.egg' -exec rm -rf {} +

install:
	pip install -e .

lint:
	ruff check

format:
	ruff check --fix
	ruff format

api:
	ROOT_URLCONF=django_sync_or_async.urls.api uvicorn django_sync_or_async.asgi:application --port 5000

uwsgi-2-threads:
	ROOT_URLCONF=django_sync_or_async.urls.sync uwsgi --module django_sync_or_async.wsgi:application --processes 1 --threads 2 --master --die-on-term --http 0.0.0.0:8000 --stats :3030 --stats-http

uwsgi-100-threads:
	ROOT_URLCONF=django_sync_or_async.urls.sync uwsgi --module django_sync_or_async.wsgi:application --processes 1 --threads 100 --master --die-on-term --http 0.0.0.0:8001 --stats :3031 --stats-http

uwsgi-gevent:
	ROOT_URLCONF=django_sync_or_async.urls.sync uwsgi --module django_sync_or_async.wsgi:application --processes 1 --gevent 100 --gevent-monkey-patch --master --die-on-term --http 0.0.0.0:8002 --stats :3032 --stats-http

gunicorn-100-threads:
	ROOT_URLCONF=django_sync_or_async.urls.sync gunicorn django_sync_or_async.wsgi --workers=1 --threads 100 --access-logfile '-' --bind 0.0.0.0:8003

gunicorn-gevent:
	ROOT_URLCONF=django_sync_or_async.urls.sync gunicorn django_sync_or_async.wsgi --workers=1 --worker-class gevent --worker-connections 100 --access-logfile '-' --bind 0.0.0.0:8004

uvicorn:
	ROOT_URLCONF=django_sync_or_async.urls.async uvicorn django_sync_or_async.asgi:application --port 8005

locust:
	 locust --users 100 --spawn-rate 10 -t 30s  -f src/django_sync_or_async/locust.py -H $(HOST)
