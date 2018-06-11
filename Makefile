default:  test

test:
	python manage.py test --testrunner=green.djangorunner.DjangoRunner

runserver:
	python manage.py runserver

migrations:
	python manage.py makemigrations

migrate:
	python manage.py migrate

cov:
	@make test
	coverage report
	coverage html

install:
	pip install -r requirements.txt
