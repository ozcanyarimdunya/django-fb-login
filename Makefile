run:
	python manage.py runserver

migrations:
	python manage.py makemigrations
	python manage.py migrate

static:
	python manage.py collectstatic --noinput --clear

user:
	python manage.py createsuperuser

test:
	python manage.py test demo
