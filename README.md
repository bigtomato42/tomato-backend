# tomato-backend
Backend of tomato project

How to run

1. Run the postgres docker image using docker compose
docker-compose up

1. activate a pipenv enviroment using:
pipenv shell
(use pip install --user pipenv to install pipenv)

2. run the migrations
./manage.py migrate

2. run the project with
./manage.py runserver


Running tests
./manage.py test

# BOOM
