release: python manage.py migrate
worker: python manage.py run_huey
web: gunicorn property_hub.wsgi --log-file -