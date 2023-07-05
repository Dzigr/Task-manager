install:
	poetry install

check:
	poetry check

PORT ?= 8000
local:
	poetry run python manage.py runserver 0.0.0.0:$(PORT)

start:
	poetry run gunicorn task_manager.wsgi

shell:
	poetry run python manage.py shell

migration:
	poetry run python manage.py makemigrations
	poetry run python manage.py migrate