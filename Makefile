up:
	docker-compose up
down:
	docker-compose down
build:
	docker-compose build

test:
	docker-compose run --rm app sh -c "python manage.py test"
migrations:
	sudo docker-compose run --rm app sh -c "python manage.py makemigrations"
create-superuser:
	 docker-compose run --rm app sh -c "python manage.py createsuperuser"