setupdev:
	docker exec -it fusus_dev-web_1 python manage.py makemigrations
	docker exec -it fusus_dev-web_1 python manage.py migrate
	docker exec -it fusus_dev-web_1 python manage.py createsuperuser --noinput
