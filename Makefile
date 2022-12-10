up:
	cd ./infrastructure && sudo docker compose up

updm:
	cd ./infrastructure && sudo docker compose up -d
	sleep 1
	./venv/bin/python3 manage.py migrate

makemig:
	./venv/bin/python3 manage.py makemigrations

mig:
	./venv/bin/python3 manage.py migrate

superuser:
	python3 manage.py createsuperuser

clear:
	cd ./infrastructure/data && sudo rm -r db && sudo docker compose down