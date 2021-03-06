# This dockerfile is kicked off from the docker-compose command, it starts the server after ensure the mysql service is already running.
FROM python:3.9

# Prevents python from writing pyc files to disc
ENV PYTHONUNBUFFERED 1
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY . /app

CMD python manage.py wait_for_db && python manage.py runserver 0.0.0.0:8000
