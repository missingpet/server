run:
	python manage.py runserver 0.0.0.0:8000
migrate:
	python manage.py makemigrations && python manage.py migrate
static:
	python manage.py collectstatic
install:
	pip install -r requirements.txt
upgrade:
	python -m pip install --upgrade pip
superuser:
	python manage.py createsuperuser
test:
	python manage.py test pet.tests
app:
	python manage.py startapp $(name)
show:
	python manage.py showmigrations
